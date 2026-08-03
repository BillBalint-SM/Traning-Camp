import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import cast

from knowledge_forge.audit import inspect_package
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.indexes import load_areas
from knowledge_forge.io import canonical_json_bytes, read_json, read_jsonl
from knowledge_forge.models import KnowledgeModule
from knowledge_forge.package import discover_modules


def _area_ownership(areas: list[dict[str, object]]) -> dict[str, str]:
    ownership: dict[str, str] = {}
    for area in areas:
        area_id = cast(str, area["id"])
        for module_id in cast(list[str], area["module_ids"]):
            if module_id in ownership:
                raise KnowledgeForgeError(
                    f"Portable export module has multiple areas: {module_id}"
                )
            ownership[module_id] = area_id
    return ownership


def _validate_context(
    areas: list[dict[str, object]],
    graph: dict[str, object],
    modules: list[KnowledgeModule],
) -> dict[str, str]:
    ownership = _area_ownership(areas)
    module_hashes = {
        module["metadata"]["id"]: module["content_sha256"] for module in modules
    }
    module_ids = set(module_hashes)
    nodes = cast(list[dict[str, object]], graph["nodes"])
    node_ids = [cast(str, node["id"]) for node in nodes]
    if len(node_ids) != len(set(node_ids)):
        raise KnowledgeForgeError("Portable export graph contains duplicate nodes")
    if set(node_ids) != module_ids or set(ownership) != module_ids:
        raise KnowledgeForgeError("Portable export module sets differ")
    for node in nodes:
        module_id = cast(str, node["id"])
        if node["content_sha256"] != module_hashes[module_id]:
            raise KnowledgeForgeError(
                f"Portable export graph hash mismatch: {module_id}"
            )
    edge_keys: set[tuple[str, str, str]] = set()
    for edge in cast(list[dict[str, object]], graph["edges"]):
        source = cast(str, edge["source"])
        relation_type = cast(str, edge["type"])
        target = cast(str, edge["target"])
        if source not in module_ids or target not in module_ids:
            raise KnowledgeForgeError(
                f"Portable export graph has unresolved endpoint: {source} -> {target}"
            )
        if source == target:
            raise KnowledgeForgeError(
                f"Portable export graph has self relation: {source}"
            )
        key = (source, relation_type, target)
        if key in edge_keys:
            raise KnowledgeForgeError(
                f"Portable export graph has duplicate edge: {source} -> {target}"
            )
        edge_keys.add(key)
    return ownership


def _skill_text() -> bytes:
    content = """---
name: portable-agent-knowledge
description: Route agent-system questions through the validated knowledge references.
---

# Portable agent knowledge

Before using this skill, verify `../export.json` and its declared file hashes.
Load `references/indexes/l0.json` to select one area, then load only that area's
L1 index and the smallest sufficient modules from `references/knowledge/`.
For an ambiguous question, report the competing areas and request clarification.
For an uncovered question, state that no reliable route exists in this package.
Use `references/graph/canonical.json` only to expand direct relations after a
module has been selected.
"""
    return content.encode("utf-8")


def _skill_files(
    pack_root: Path,
    areas: list[dict[str, object]],
) -> dict[str, bytes]:
    files = {"skill/SKILL.md": _skill_text()}
    references = [
        Path("graph/canonical.json"),
        Path("indexes/areas.json"),
        Path("indexes/l0.json"),
    ]
    references.extend(
        Path("indexes/l1") / f"{cast(str, area['id'])}.json" for area in areas
    )
    references.extend(
        Path("knowledge") / path.name
        for path in sorted((pack_root / "knowledge").glob("*.md"))
    )
    for relative in references:
        source = pack_root / relative
        if not source.is_file() or source.is_symlink():
            raise KnowledgeForgeError(
                f"Portable export reference is not a regular file: {relative.name}"
            )
        files[f"skill/references/{relative.as_posix()}"] = source.read_bytes()
    return files


def _rag_file(
    modules: list[KnowledgeModule],
    ownership: dict[str, str],
    pack_root: Path,
) -> bytes:
    lines: list[bytes] = []
    for module in modules:
        metadata = module["metadata"]
        module_id = metadata["id"]
        raw = (pack_root / "knowledge" / f"{module_id}.md").read_text(
            encoding="utf-8"
        )
        record = {
            "id": module_id,
            "title": metadata["title"],
            "text": raw,
            "metadata": {
                "area_id": ownership[module_id],
                "kind": metadata["kind"],
                "maturity": metadata["maturity"],
                "confidence": metadata["confidence"],
                "tags": sorted(metadata["tags"]),
            },
        }
        lines.append(canonical_json_bytes(record))
    return b"".join(lines)


def _graph_files(graph: dict[str, object]) -> dict[str, bytes]:
    nodes = cast(list[dict[str, object]], graph["nodes"])
    edges = cast(list[dict[str, object]], graph["edges"])
    node_records = [
        {
            "id": node["id"],
            "title": node["title"],
            "kind": node["kind"],
            "maturity": node["maturity"],
            "confidence": node["confidence"],
            "tags": sorted(cast(list[str], node["tags"])),
            "content_sha256": node["content_sha256"],
        }
        for node in sorted(nodes, key=lambda item: cast(str, item["id"]))
    ]
    edge_records = [
        {
            "source": edge["source"],
            "type": edge["type"],
            "target": edge["target"],
        }
        for edge in sorted(
            edges,
            key=lambda item: (
                cast(str, item["source"]),
                cast(str, item["type"]),
                cast(str, item["target"]),
            ),
        )
    ]
    return {
        "graph/nodes.jsonl": b"".join(
            canonical_json_bytes(node) for node in node_records
        ),
        "graph/edges.jsonl": b"".join(
            canonical_json_bytes(edge) for edge in edge_records
        ),
    }


def _manifest(
    package_sha256: str,
    ownership: dict[str, str],
    relation_count: int,
    files: dict[str, bytes],
) -> dict[str, object]:
    skill_count = sum(path.startswith("skill/") for path in files)
    manifest: dict[str, object] = {
        "format_version": 1,
        "kind": "portable-agent-exports",
        "package_sha256": package_sha256,
        "module_count": len(ownership),
        "area_count": len(set(ownership.values())),
        "relation_count": relation_count,
        "profiles": {
            "skill": {"file_count": skill_count},
            "rag": {"file_count": 1, "document_count": len(ownership)},
            "graph": {
                "file_count": 2,
                "node_count": len(ownership),
                "edge_count": relation_count,
            },
        },
        "files": [
            {"path": path, "sha256": sha256_bytes(content)}
            for path, content in sorted(files.items())
        ],
    }
    manifest["export_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    return manifest


def _load_export_manifest(output_root: Path) -> dict[str, object]:
    manifest_path = output_root / "export.json"
    if output_root.is_symlink() or not output_root.is_dir():
        raise KnowledgeForgeError("Portable export output must be a directory")
    try:
        payload = read_json(manifest_path)
    except KnowledgeForgeError as error:
        raise KnowledgeForgeError("Portable export manifest cannot be read") from error
    if not isinstance(payload, dict):
        raise KnowledgeForgeError("Portable export manifest must be an object")
    return cast(dict[str, object], payload)


def _manifest_integer(manifest: dict[str, object], key: str) -> int:
    value = manifest.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise KnowledgeForgeError(f"Portable export manifest {key} is invalid")
    return value


def _manifest_profile(
    manifest: dict[str, object], profile_name: str
) -> dict[str, object]:
    profiles = manifest.get("profiles")
    if not isinstance(profiles, dict):
        raise KnowledgeForgeError("Portable export manifest profiles are invalid")
    profile = profiles.get(profile_name)
    if not isinstance(profile, dict):
        raise KnowledgeForgeError(
            f"Portable export manifest profile is missing: {profile_name}"
        )
    return cast(dict[str, object], profile)


def _verify_profile_counts(
    manifest: dict[str, object], declared: dict[str, str]
) -> None:
    expected_profiles = ("skill", "rag", "graph")
    for profile_name in expected_profiles:
        profile = _manifest_profile(manifest, profile_name)
        declared_count = sum(
            path.startswith(f"{profile_name}/") for path in declared
        )
        if profile.get("file_count") != declared_count:
            raise KnowledgeForgeError(
                f"Portable export {profile_name} profile file count mismatch"
            )
    module_count = _manifest_integer(manifest, "module_count")
    _manifest_integer(manifest, "area_count")
    relation_count = _manifest_integer(manifest, "relation_count")
    package_sha256 = manifest.get("package_sha256")
    if not isinstance(package_sha256, str) or len(package_sha256) != 64:
        raise KnowledgeForgeError("Portable export package hash is invalid")
    rag_profile = _manifest_profile(manifest, "rag")
    if rag_profile.get("document_count") != module_count:
        raise KnowledgeForgeError("Portable export rag profile count mismatch")
    graph_profile = _manifest_profile(manifest, "graph")
    if graph_profile.get("node_count") != module_count:
        raise KnowledgeForgeError("Portable export graph profile node count mismatch")
    if graph_profile.get("edge_count") != relation_count:
        raise KnowledgeForgeError("Portable export graph profile edge count mismatch")


def _verify_skill_profile(
    output_root: Path, declared: dict[str, str]
) -> None:
    skill_path = output_root / "skill" / "SKILL.md"
    try:
        text = skill_path.read_text(encoding="utf-8")
    except OSError as error:
        raise KnowledgeForgeError("Portable export Skill file cannot be read") from error
    lines = text.splitlines()
    if len(lines) < 4 or lines[0] != "---":
        raise KnowledgeForgeError("Portable export Skill frontmatter is invalid")
    try:
        closing = lines.index("---", 1)
    except ValueError as error:
        raise KnowledgeForgeError("Portable export Skill frontmatter is invalid") from error
    fields = {
        key: value.strip()
        for key, value in (
            line.split(":", 1)
            for line in lines[1:closing]
            if ":" in line
        )
    }
    if fields.get("name") != "portable-agent-knowledge":
        raise KnowledgeForgeError("Portable export Skill name is invalid")
    if not fields.get("description"):
        raise KnowledgeForgeError("Portable export Skill description is missing")
    if re.search(r"(?:[A-Za-z]:[\\/]|(?<![A-Za-z0-9._-])/)", text):
        raise KnowledgeForgeError("Portable export Skill references must be relative")
    if "../export.json" not in text:
        raise KnowledgeForgeError("Portable export Skill reference is missing: export.json")
    references = re.findall(r"references/[A-Za-z0-9._/-]+", text)
    for reference in references:
        if reference.endswith("/") or reference in {
            "references/indexes/l1",
            "references/knowledge",
        }:
            prefix = f"skill/{reference.rstrip('/')}/"
            if not any(path.startswith(prefix) for path in declared):
                raise KnowledgeForgeError(
                    f"Portable export Skill reference is unresolved: {reference}"
                )
            continue
        path = f"skill/{reference}"
        if path not in declared:
            raise KnowledgeForgeError(
                f"Portable export Skill reference is unresolved: {reference}"
            )


def _verify_rag_profile(
    output_root: Path, manifest: dict[str, object]
) -> dict[str, dict[str, object]]:
    records = read_jsonl(output_root / "rag" / "documents.jsonl")
    expected_count = _manifest_integer(manifest, "module_count")
    if len(records) != expected_count:
        raise KnowledgeForgeError("Portable export RAG document count mismatch")
    by_id: dict[str, dict[str, object]] = {}
    previous_id: str | None = None
    for record in records:
        module_id = record.get("id")
        title = record.get("title")
        text = record.get("text")
        metadata = record.get("metadata")
        if not isinstance(module_id, str) or not module_id or "/" in module_id:
            raise KnowledgeForgeError("Portable export RAG record has invalid id")
        if module_id in by_id:
            raise KnowledgeForgeError(f"Portable export RAG id is duplicated: {module_id}")
        if previous_id is not None and module_id < previous_id:
            raise KnowledgeForgeError("Portable export RAG records are not sorted")
        if not isinstance(title, str) or not title:
            raise KnowledgeForgeError(f"Portable export RAG title is invalid: {module_id}")
        if not isinstance(text, str) or not text:
            raise KnowledgeForgeError(f"Portable export RAG text is empty: {module_id}")
        if not isinstance(metadata, dict):
            raise KnowledgeForgeError(
                f"Portable export RAG metadata is invalid: {module_id}"
            )
        area_id = metadata.get("area_id")
        tags = metadata.get("tags")
        if not isinstance(area_id, str) or not area_id:
            raise KnowledgeForgeError(
                f"Portable export RAG area metadata is invalid: {module_id}"
            )
        if not isinstance(tags, list) or not all(
            isinstance(tag, str) for tag in tags
        ):
            raise KnowledgeForgeError(
                f"Portable export RAG tags are invalid: {module_id}"
            )
        module_path = output_root / "skill" / "references" / "knowledge" / f"{module_id}.md"
        if module_path.is_symlink() or not module_path.is_file():
            raise KnowledgeForgeError(
                f"Portable export RAG module reference is missing: {module_id}"
            )
        if module_path.read_bytes() != text.encode("utf-8"):
            raise KnowledgeForgeError(
                f"Portable export RAG text does not match Skill module: {module_id}"
            )
        by_id[module_id] = record
        previous_id = module_id
    return by_id


def _verify_graph_profile(
    output_root: Path, manifest: dict[str, object]
) -> tuple[dict[str, str], set[tuple[str, str, str]]]:
    nodes = read_jsonl(output_root / "graph" / "nodes.jsonl")
    expected_nodes = _manifest_integer(manifest, "module_count")
    if len(nodes) != expected_nodes:
        raise KnowledgeForgeError("Portable export graph node count mismatch")
    node_hashes: dict[str, str] = {}
    for node in nodes:
        module_id = node.get("id")
        content_sha256 = node.get("content_sha256")
        if not isinstance(module_id, str) or not module_id:
            raise KnowledgeForgeError("Portable export graph node id is invalid")
        if module_id in node_hashes:
            raise KnowledgeForgeError(
                f"Portable export graph node is duplicated: {module_id}"
            )
        if not isinstance(content_sha256, str) or len(content_sha256) != 64:
            raise KnowledgeForgeError(
                f"Portable export graph node hash is invalid: {module_id}"
            )
        node_hashes[module_id] = content_sha256
    edges = read_jsonl(output_root / "graph" / "edges.jsonl")
    expected_edges = _manifest_integer(manifest, "relation_count")
    if len(edges) != expected_edges:
        raise KnowledgeForgeError("Portable export graph edge count mismatch")
    edge_keys: set[tuple[str, str, str]] = set()
    for edge in edges:
        source = edge.get("source")
        relation_type = edge.get("type")
        target = edge.get("target")
        if not all(isinstance(value, str) and value for value in (source, relation_type, target)):
            raise KnowledgeForgeError("Portable export graph edge is invalid")
        assert isinstance(source, str)
        assert isinstance(relation_type, str)
        assert isinstance(target, str)
        if source not in node_hashes or target not in node_hashes:
            raise KnowledgeForgeError(
                f"Portable export graph has unresolved endpoint: {source} -> {target}"
            )
        if source == target:
            raise KnowledgeForgeError(
                f"Portable export graph has self relation: {source}"
            )
        key = (source, relation_type, target)
        if key in edge_keys:
            raise KnowledgeForgeError(
                f"Portable export graph edge is duplicated: {source} -> {target}"
            )
        edge_keys.add(key)
    return node_hashes, edge_keys


def _verify_graph_reference(
    output_root: Path,
    node_hashes: dict[str, str],
    edge_keys: set[tuple[str, str, str]],
) -> None:
    payload = read_json(output_root / "skill" / "references" / "graph" / "canonical.json")
    if not isinstance(payload, dict):
        raise KnowledgeForgeError("Portable export canonical graph is invalid")
    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise KnowledgeForgeError("Portable export canonical graph is incomplete")
    reference_hashes: dict[str, str] = {}
    for node in nodes:
        if not isinstance(node, dict):
            raise KnowledgeForgeError("Portable export canonical graph node is invalid")
        module_id = node.get("id")
        content_sha256 = node.get("content_sha256")
        if not isinstance(module_id, str) or not isinstance(content_sha256, str):
            raise KnowledgeForgeError("Portable export canonical graph node is invalid")
        reference_hashes[module_id] = content_sha256
    if len(reference_hashes) != len(nodes):
        raise KnowledgeForgeError("Portable export canonical graph node is duplicated")
    if reference_hashes != node_hashes:
        raise KnowledgeForgeError("Portable export canonical graph node drift")
    reference_edges: set[tuple[str, str, str]] = set()
    for edge in edges:
        if not isinstance(edge, dict):
            raise KnowledgeForgeError("Portable export canonical graph edge is invalid")
        source = edge.get("source")
        relation_type = edge.get("type")
        target = edge.get("target")
        if not all(isinstance(value, str) for value in (source, relation_type, target)):
            raise KnowledgeForgeError("Portable export canonical graph edge is invalid")
        assert isinstance(source, str)
        assert isinstance(relation_type, str)
        assert isinstance(target, str)
        reference_edges.add((source, relation_type, target))
    if len(reference_edges) != len(edges):
        raise KnowledgeForgeError("Portable export canonical graph edge is duplicated")
    if reference_edges != edge_keys:
        raise KnowledgeForgeError("Portable export canonical graph edge drift")


def verify_portable_export(output_root: Path) -> dict[str, object]:
    manifest = _load_export_manifest(output_root)
    if manifest.get("format_version") != 1:
        raise KnowledgeForgeError("Portable export manifest has invalid format")
    if manifest.get("kind") != "portable-agent-exports":
        raise KnowledgeForgeError("Portable export manifest has invalid kind")
    claimed_digest = manifest.get("export_sha256")
    if not isinstance(claimed_digest, str):
        raise KnowledgeForgeError("Portable export manifest is missing export digest")
    without_digest = dict(manifest)
    del without_digest["export_sha256"]
    if sha256_bytes(canonical_json_bytes(without_digest)) != claimed_digest:
        raise KnowledgeForgeError("Portable export manifest digest mismatch")
    entries = manifest.get("files")
    if not isinstance(entries, list):
        raise KnowledgeForgeError("Portable export manifest files must be an array")
    declared: dict[str, str] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise KnowledgeForgeError("Portable export file entry must be an object")
        relative = entry.get("path")
        digest = entry.get("sha256")
        if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
            raise KnowledgeForgeError("Portable export file path must be relative")
        relative_path = Path(relative)
        if ".." in relative_path.parts or relative_path.parts[0] not in {
            "skill",
            "rag",
            "graph",
        }:
            raise KnowledgeForgeError("Portable export file path is outside a profile")
        if not isinstance(digest, str) or len(digest) != 64:
            raise KnowledgeForgeError("Portable export file hash is invalid")
        if relative in declared:
            raise KnowledgeForgeError(f"Portable export file is duplicated: {relative}")
        declared[relative] = digest
    actual = {
        path.relative_to(output_root).as_posix()
        for path in output_root.rglob("*")
        if path.is_file() and path.name != "export.json"
    }
    if actual != set(declared):
        extra = sorted(actual - set(declared))
        missing = sorted(set(declared) - actual)
        detail = extra[0] if extra else missing[0]
        kind = "undeclared" if extra else "missing"
        raise KnowledgeForgeError(f"Portable export file is {kind}: {detail}")
    for relative, expected in declared.items():
        actual_digest = sha256_bytes((output_root / relative).read_bytes())
        if actual_digest != expected:
            raise KnowledgeForgeError(f"Portable export file hash mismatch: {relative}")
    required_files = {
        "skill/SKILL.md",
        "rag/documents.jsonl",
        "graph/nodes.jsonl",
        "graph/edges.jsonl",
    }
    if not required_files.issubset(declared):
        missing = min(required_files - set(declared))
        raise KnowledgeForgeError(f"Portable export required file is missing: {missing}")
    _verify_profile_counts(manifest, declared)
    _verify_skill_profile(output_root, declared)
    rag_records = _verify_rag_profile(output_root, manifest)
    node_hashes, edge_keys = _verify_graph_profile(output_root, manifest)
    if set(rag_records) != set(node_hashes):
        raise KnowledgeForgeError("Portable export RAG and graph module sets differ")
    for module_id, record in rag_records.items():
        text = cast(str, record["text"])
        expected_hash = node_hashes[module_id]
        if sha256_bytes(text.encode("utf-8")) != expected_hash:
            raise KnowledgeForgeError(
                f"Portable export RAG content hash mismatch: {module_id}"
            )
    _verify_graph_reference(output_root, node_hashes, edge_keys)
    return manifest


def _write_export(
    output_root: Path,
    files: dict[str, bytes],
    manifest: dict[str, object],
) -> None:
    output_root.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(
        tempfile.mkdtemp(prefix=f".{output_root.name}.", dir=output_root.parent)
    )
    try:
        for relative, content in sorted(files.items()):
            target = staging_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        (staging_root / "export.json").write_bytes(canonical_json_bytes(manifest))
        verify_portable_export(staging_root)
        if output_root.exists() or output_root.is_symlink():
            raise KnowledgeForgeError(
                f"Portable export output already exists: {output_root.name}"
            )
        os.replace(staging_root, output_root)
    except OSError as error:
        raise KnowledgeForgeError(
            f"Cannot publish portable export: {output_root.name}"
        ) from error
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root)


def build_portable_exports(
    pack_root: Path,
    schema_root: Path,
    output_root: Path,
) -> dict[str, object]:
    if output_root.exists() or output_root.is_symlink():
        raise KnowledgeForgeError(
            f"Portable export output already exists: {output_root.name}"
        )
    profile = inspect_package(pack_root, schema_root)
    modules = discover_modules(
        pack_root, schema_root / "knowledge-module.schema.json"
    )
    areas = cast(list[dict[str, object]], load_areas(pack_root / "indexes" / "areas.json"))
    graph_payload = read_json(pack_root / "graph" / "canonical.json")
    if not isinstance(graph_payload, dict):
        raise KnowledgeForgeError("Canonical graph root must be an object")
    graph = cast(dict[str, object], graph_payload)
    ownership = _validate_context(areas, graph, modules)
    files = _skill_files(pack_root, areas)
    files["rag/documents.jsonl"] = _rag_file(modules, ownership, pack_root)
    files.update(_graph_files(graph))
    manifest = _manifest(
        cast(str, profile["package_sha256"]),
        ownership,
        len(cast(list[object], graph["edges"])),
        files,
    )
    _write_export(output_root, files, manifest)
    return manifest
