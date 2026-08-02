import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.knowledge_map import (
    build_knowledge_map_projection,
    validate_projection_inputs,
)

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def _load_payload(path: Path) -> dict[str, object]:
    return cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))


def _projection_files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _projection_inputs() -> tuple[
    list[dict[str, object]], dict[str, object], dict[str, str]
]:
    areas_payload = _load_payload(PACK_ROOT / "indexes" / "areas.json")
    areas = cast(list[dict[str, object]], areas_payload["areas"])
    graph = _load_payload(PACK_ROOT / "graph" / "canonical.json")
    nodes = cast(list[dict[str, object]], graph["nodes"])
    hashes = {
        cast(str, node["id"]): cast(str, node["content_sha256"])
        for node in nodes
    }
    return areas, graph, hashes


def test_build_knowledge_map_projection_renders_complete_wiki(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "knowledge-map"

    manifest = build_knowledge_map_projection(PACK_ROOT, SCHEMA_ROOT, output_root)

    assert manifest["package_sha256"] == (
        "d71cbf0d2e27bd057c55a951aab7d92a71c5914e0dfd7b58b7d13276ed2102a8"
    )
    assert manifest["area_count"] == 10
    assert manifest["article_count"] == 193
    assert manifest["relation_count"] == 196
    assert len(cast(list[object], manifest["files"])) == 194
    assert len(cast(str, manifest["projection_sha256"])) == 64

    index_text = (output_root / "wiki" / "index.md").read_text(encoding="utf-8")
    assert index_text.startswith("# Agentrendszerek tudástérképe\n\n")
    assert index_text.count("\n## ") == 10
    assert index_text.count("[[modules/") == 193

    article_path = (
        output_root / "wiki" / "modules" / "principle.context-is-finite.md"
    )
    article_text = article_path.read_text(encoding="utf-8")
    original_text = (
        PACK_ROOT / "knowledge" / "principle.context-is-finite.md"
    ).read_text(encoding="utf-8")
    assert "# A kontextus véges erőforrás" in article_text
    assert "## Lényeg" in article_text
    assert original_text.split("---", 2)[2].strip() in article_text
    assert (
        "[[modules/pattern.context-budget-allocation|supports: "
        "Kontextuskeret elosztása]]"
    ) in article_text


def test_build_knowledge_map_projection_is_byte_deterministic(tmp_path: Path) -> None:
    first_root = tmp_path / "derived" / "first"
    second_root = tmp_path / "derived" / "second"

    first = build_knowledge_map_projection(PACK_ROOT, SCHEMA_ROOT, first_root)
    second = build_knowledge_map_projection(PACK_ROOT, SCHEMA_ROOT, second_root)

    assert first == second
    assert _projection_files(first_root) == _projection_files(second_root)


def test_build_knowledge_map_projection_rejects_existing_output(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "knowledge-map"
    output_root.mkdir(parents=True)
    sentinel = output_root / "keep.txt"
    sentinel.write_text("user state", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="already exists"):
        build_knowledge_map_projection(PACK_ROOT, SCHEMA_ROOT, output_root)

    assert sentinel.read_text(encoding="utf-8") == "user state"


def test_validate_projection_inputs_rejects_missing_edge_target() -> None:
    areas, graph, hashes = _projection_inputs()
    changed = deepcopy(graph)
    edges = cast(list[dict[str, object]], changed["edges"])
    edges[0]["target"] = "principle.unknown"

    with pytest.raises(KnowledgeForgeError, match="missing target"):
        validate_projection_inputs(areas, changed, hashes)


def test_validate_projection_inputs_rejects_duplicate_relation() -> None:
    areas, graph, hashes = _projection_inputs()
    changed = deepcopy(graph)
    edges = cast(list[dict[str, object]], changed["edges"])
    edges.append(deepcopy(edges[0]))

    with pytest.raises(KnowledgeForgeError, match="Duplicate projection relation"):
        validate_projection_inputs(areas, changed, hashes)


def test_validate_projection_inputs_rejects_self_relation() -> None:
    areas, graph, hashes = _projection_inputs()
    changed = deepcopy(graph)
    edges = cast(list[dict[str, object]], changed["edges"])
    edges[0]["target"] = edges[0]["source"]

    with pytest.raises(KnowledgeForgeError, match="self relation"):
        validate_projection_inputs(areas, changed, hashes)


def test_validate_projection_inputs_rejects_module_set_mismatch() -> None:
    areas, graph, hashes = _projection_inputs()
    changed_areas = deepcopy(areas)
    module_ids = cast(list[str], changed_areas[0]["module_ids"])
    module_ids.pop()

    with pytest.raises(KnowledgeForgeError, match="module sets differ"):
        validate_projection_inputs(changed_areas, graph, hashes)


def test_validate_projection_inputs_rejects_content_hash_mismatch() -> None:
    areas, graph, hashes = _projection_inputs()
    changed_hashes = dict(hashes)
    changed_hashes[min(changed_hashes)] = "0" * 64

    with pytest.raises(KnowledgeForgeError, match="content hash mismatch"):
        validate_projection_inputs(areas, graph, changed_hashes)
