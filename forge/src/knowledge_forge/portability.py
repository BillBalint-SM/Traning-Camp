import os
import shutil
import tempfile
from pathlib import Path
from typing import cast

from knowledge_forge.audit import inspect_package
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.indexes import load_areas
from knowledge_forge.io import canonical_json_bytes, read_json
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
