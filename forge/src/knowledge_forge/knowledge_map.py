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


def _area_module_ownership(
    areas: list[dict[str, object]],
) -> dict[str, str]:
    ownership: dict[str, str] = {}
    for area in areas:
        area_id = cast(str, area["id"])
        for module_id in cast(list[str], area["module_ids"]):
            if module_id in ownership:
                raise KnowledgeForgeError(
                    f"Projection module has multiple areas: {module_id}"
                )
            ownership[module_id] = area_id
    return ownership


def validate_projection_inputs(
    areas: list[dict[str, object]],
    graph: dict[str, object],
    module_hashes: dict[str, str],
) -> dict[str, str]:
    ownership = _area_module_ownership(areas)
    nodes = cast(list[dict[str, object]], graph["nodes"])
    node_ids = [cast(str, node["id"]) for node in nodes]
    if len(node_ids) != len(set(node_ids)):
        raise KnowledgeForgeError("Projection graph contains duplicate node IDs")
    graph_ids = set(node_ids)
    module_ids = set(module_hashes)
    indexed_ids = set(ownership)
    if graph_ids != module_ids or indexed_ids != module_ids:
        raise KnowledgeForgeError("Projection module sets differ across package artifacts")

    for node in nodes:
        module_id = cast(str, node["id"])
        if node["content_sha256"] != module_hashes[module_id]:
            raise KnowledgeForgeError(
                f"Graph node content hash mismatch: {module_id}"
            )

    edge_keys: set[tuple[str, str, str]] = set()
    for edge in cast(list[dict[str, object]], graph["edges"]):
        source = cast(str, edge["source"])
        relation_type = cast(str, edge["type"])
        target = cast(str, edge["target"])
        if source not in module_ids:
            raise KnowledgeForgeError(f"Graph edge has missing source: {source}")
        if target not in module_ids:
            raise KnowledgeForgeError(f"Graph edge has missing target: {target}")
        if source == target:
            raise KnowledgeForgeError(f"Projection self relation is not allowed: {source}")
        key = (source, relation_type, target)
        if key in edge_keys:
            raise KnowledgeForgeError(
                f"Duplicate projection relation: {source} -> {target}"
            )
        edge_keys.add(key)
    return ownership


def _render_index(
    areas: list[dict[str, object]], titles: dict[str, str]
) -> bytes:
    sections = ["# Agentrendszerek tudástérképe", ""]
    for area in areas:
        sections.extend(
            [
                f"## {area['title']}",
                "",
                cast(str, area["summary"]),
                "",
            ]
        )
        for module_id in cast(list[str], area["module_ids"]):
            sections.append(f"- [[modules/{module_id}|{titles[module_id]}]]")
        sections.append("")
    return "\n".join(sections).encode("utf-8")


def _split_module(raw: str, module_id: str) -> tuple[str, str]:
    normalized = raw.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise KnowledgeForgeError(f"Projection module has no frontmatter: {module_id}")
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            frontmatter = "".join(lines[: index + 1]).rstrip("\n")
            body = "".join(lines[index + 1 :]).strip("\n")
            return frontmatter, body
    raise KnowledgeForgeError(f"Projection module has open frontmatter: {module_id}")


def _render_article(
    raw: str,
    module_id: str,
    title: str,
    relations: list[dict[str, str]],
    titles: dict[str, str],
) -> bytes:
    frontmatter, body = _split_module(raw, module_id)
    sections = [frontmatter, "", f"# {title}", "", body]
    if relations:
        sections.extend(["", "## Kapcsolati térkép", ""])
        sections.extend(
            f"- [[modules/{relation['target']}|{relation['type']}: "
            f"{titles[relation['target']]}]]"
            for relation in relations
        )
    return ("\n".join(sections).rstrip() + "\n").encode("utf-8")


def _relations_by_source(
    graph: dict[str, object],
) -> dict[str, list[dict[str, str]]]:
    relations: dict[str, list[dict[str, str]]] = {}
    edges = sorted(
        cast(list[dict[str, str]], graph["edges"]),
        key=lambda edge: (edge["source"], edge["type"], edge["target"]),
    )
    for edge in edges:
        relations.setdefault(edge["source"], []).append(edge)
    return relations


def _projection_manifest(
    package_sha256: str,
    areas: list[dict[str, object]],
    ownership: dict[str, str],
    relation_count: int,
    files: dict[str, bytes],
) -> dict[str, object]:
    manifest: dict[str, object] = {
        "format_version": 1,
        "kind": "understand-anything-karpathy-projection",
        "package_sha256": package_sha256,
        "area_count": len(areas),
        "article_count": len(ownership),
        "relation_count": relation_count,
        "module_areas": [
            {"module_id": module_id, "area_id": ownership[module_id]}
            for module_id in sorted(ownership)
        ],
        "files": [
            {"path": path, "sha256": sha256_bytes(content)}
            for path, content in sorted(files.items())
        ],
    }
    manifest["projection_sha256"] = sha256_bytes(canonical_json_bytes(manifest))
    return manifest


def _write_projection(
    output_root: Path,
    files: dict[str, bytes],
    manifest: dict[str, object],
) -> None:
    output_root.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(
        tempfile.mkdtemp(prefix=f".{output_root.name}.", dir=output_root.parent)
    )
    try:
        for relative_path, content in sorted(files.items()):
            target = staging_root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
            if sha256_bytes(target.read_bytes()) != sha256_bytes(content):
                raise KnowledgeForgeError(
                    f"Projection file verification failed: {relative_path}"
                )
        (staging_root / "projection.json").write_bytes(
            canonical_json_bytes(manifest)
        )
        if output_root.exists() or output_root.is_symlink():
            raise KnowledgeForgeError(
                f"Projection output already exists: {output_root.name}"
            )
        os.replace(staging_root, output_root)
    except OSError as error:
        raise KnowledgeForgeError(
            f"Cannot publish projection output: {output_root.name}"
        ) from error
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root)


def build_knowledge_map_projection(
    pack_root: Path,
    schema_root: Path,
    output_root: Path,
) -> dict[str, object]:
    if output_root.exists() or output_root.is_symlink():
        raise KnowledgeForgeError(
            f"Projection output already exists: {output_root.name}"
        )
    profile = inspect_package(pack_root, schema_root)
    modules = discover_modules(
        pack_root, schema_root / "knowledge-module.schema.json"
    )
    areas = cast(
        list[dict[str, object]],
        load_areas(pack_root / "indexes" / "areas.json"),
    )
    graph_payload = read_json(pack_root / "graph" / "canonical.json")
    if not isinstance(graph_payload, dict):
        raise KnowledgeForgeError("Canonical graph root must be an object")
    graph = cast(dict[str, object], graph_payload)
    module_hashes = {
        module["metadata"]["id"]: module["content_sha256"] for module in modules
    }
    ownership = validate_projection_inputs(areas, graph, module_hashes)
    module_by_id: dict[str, KnowledgeModule] = {
        module["metadata"]["id"]: module for module in modules
    }
    titles = {
        module_id: module["metadata"]["title"]
        for module_id, module in module_by_id.items()
    }
    relations = _relations_by_source(graph)
    files = {"wiki/index.md": _render_index(areas, titles)}
    for module_id in sorted(module_by_id):
        raw = (pack_root / "knowledge" / f"{module_id}.md").read_text(
            encoding="utf-8"
        )
        files[f"wiki/modules/{module_id}.md"] = _render_article(
            raw,
            module_id,
            titles[module_id],
            relations.get(module_id, []),
            titles,
        )
    manifest = _projection_manifest(
        cast(str, profile["package_sha256"]),
        areas,
        ownership,
        len(cast(list[object], graph["edges"])),
        files,
    )
    _write_projection(output_root, files, manifest)
    return manifest
