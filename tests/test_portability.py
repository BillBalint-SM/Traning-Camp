import json
from copy import deepcopy
from pathlib import Path
from shutil import copytree
from typing import cast

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.portability import (
    build_portable_exports,
    verify_portable_export,
)

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_ROOT = ROOT / "forge" / "schemas"


def _read_json(path: Path) -> dict[str, object]:
    return cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))


def _files(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _jsonl(path: Path) -> list[dict[str, object]]:
    return [
        cast(dict[str, object], json.loads(line))
        for line in path.read_text(encoding="utf-8").splitlines()
    ]


def test_build_portable_exports_renders_three_complete_profiles(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"

    manifest = build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    assert manifest["format_version"] == 1
    assert manifest["kind"] == "portable-agent-exports"
    assert manifest["module_count"] == 193
    assert manifest["area_count"] == 10
    assert manifest["relation_count"] == 196
    profiles = cast(dict[str, dict[str, object]], manifest["profiles"])
    assert profiles["rag"]["document_count"] == 193
    assert profiles["graph"]["node_count"] == 193
    assert profiles["graph"]["edge_count"] == 196

    skill = (output_root / "skill" / "SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith(
        "---\nname: portable-agent-knowledge\n"
        "description: Route agent-system questions through the validated knowledge references.\n---\n"
    )
    assert "references/indexes/l0.json" in skill
    assert "../export.json" in skill

    rag_records = _jsonl(output_root / "rag" / "documents.jsonl")
    assert [record["id"] for record in rag_records] == sorted(
        cast(str, record["id"]) for record in rag_records
    )
    assert len(rag_records) == 193
    assert all(cast(str, record["text"]).strip() for record in rag_records)
    assert all(
        cast(str, cast(dict[str, object], record["metadata"])["area_id"])
        for record in rag_records
    )

    nodes = _jsonl(output_root / "graph" / "nodes.jsonl")
    edges = _jsonl(output_root / "graph" / "edges.jsonl")
    node_ids = {cast(str, node["id"]) for node in nodes}
    assert len(nodes) == 193
    assert len(node_ids) == 193
    assert len(edges) == 196
    assert all(
        cast(str, edge["source"]) in node_ids
        and cast(str, edge["target"]) in node_ids
        for edge in edges
    )

    verified = verify_portable_export(output_root)
    assert verified == manifest


def test_build_portable_exports_is_byte_deterministic(tmp_path: Path) -> None:
    first_root = tmp_path / "derived" / "first"
    second_root = tmp_path / "derived" / "second"

    first = build_portable_exports(PACK_ROOT, SCHEMA_ROOT, first_root)
    second = build_portable_exports(PACK_ROOT, SCHEMA_ROOT, second_root)

    assert first == second
    assert _files(first_root) == _files(second_root)


def test_build_portable_exports_rejects_existing_output_without_mutation(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    output_root.mkdir(parents=True)
    sentinel = output_root / "sentinel.txt"
    sentinel.write_text("preserve", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="already exists"):
        build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    assert sentinel.read_text(encoding="utf-8") == "preserve"


def test_verify_portable_export_rejects_modified_generated_file(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    path = output_root / "rag" / "documents.jsonl"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="hash mismatch"):
        verify_portable_export(output_root)


def test_verify_portable_export_rejects_undeclared_file(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    extra = output_root / "rag" / "extra.jsonl"
    extra.write_text("{}\n", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="undeclared"):
        verify_portable_export(output_root)


@pytest.mark.parametrize(
    ("artifact", "message"),
    [("graph/canonical.json", "Stale manifest hash"),
     ("indexes/areas.json", "Stale manifest hash")],
)
def test_build_portable_exports_rejects_stale_canonical_artifact(
    tmp_path: Path,
    artifact: str,
    message: str,
) -> None:
    workspace = tmp_path / "workspace"
    copytree(PACK_ROOT, workspace / "pack")
    copytree(SCHEMA_ROOT, workspace / "forge" / "schemas")
    path = workspace / "pack" / artifact
    payload = _read_json(path)
    changed = deepcopy(payload)
    if artifact.endswith("canonical.json"):
        edges = cast(list[dict[str, object]], changed["edges"])
        edges[0]["target"] = "principle.unknown"
    else:
        areas = cast(list[dict[str, object]], changed["areas"])
        module_ids = cast(list[str], areas[0]["module_ids"])
        module_ids.pop()
    path.write_text(json.dumps(changed, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match=message):
        build_portable_exports(
            workspace / "pack",
            workspace / "forge" / "schemas",
            workspace / "derived" / "portable-exports",
        )
