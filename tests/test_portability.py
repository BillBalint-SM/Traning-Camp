import json
from copy import deepcopy
from pathlib import Path
from shutil import copytree
from typing import cast

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes
from knowledge_forge.portability import (
    build_portable_exports,
    diff_portable_exports,
    load_portable_context,
    load_portable_context_budgeted,
    load_portable_context_graph,
    route_portable_export,
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


def _refresh_manifest(output_root: Path) -> None:
    manifest_path = output_root / "export.json"
    manifest = _read_json(manifest_path)
    entries = cast(list[dict[str, object]], manifest["files"])
    for entry in entries:
        relative = cast(str, entry["path"])
        entry["sha256"] = sha256_bytes((output_root / relative).read_bytes())
    manifest_without_digest = dict(manifest)
    manifest_without_digest.pop("export_sha256", None)
    manifest["export_sha256"] = sha256_bytes(
        canonical_json_bytes(manifest_without_digest)
    )
    manifest_path.write_bytes(canonical_json_bytes(manifest))


def _mutate_valid_export(output_root: Path) -> tuple[str, str]:
    rag_path = output_root / "rag" / "documents.jsonl"
    records = _jsonl(rag_path)
    module_id = cast(str, records[0]["id"])
    records[0]["text"] = cast(str, records[0]["text"]) + "\n\nDelta változás.\n"
    rag_path.write_bytes(b"".join(canonical_json_bytes(record) for record in records))
    module_path = output_root / "skill" / "references" / "knowledge" / f"{module_id}.md"
    module_path.write_bytes(cast(str, records[0]["text"]).encode("utf-8"))
    content_sha256 = sha256_bytes(cast(str, records[0]["text"]).encode("utf-8"))

    nodes_path = output_root / "graph" / "nodes.jsonl"
    nodes = _jsonl(nodes_path)
    for node in nodes:
        if node["id"] == module_id:
            node["content_sha256"] = content_sha256
    nodes_path.write_bytes(b"".join(canonical_json_bytes(node) for node in nodes))

    canonical_path = output_root / "skill" / "references" / "graph" / "canonical.json"
    canonical = _read_json(canonical_path)
    canonical_nodes = cast(list[dict[str, object]], canonical["nodes"])
    for node in canonical_nodes:
        if node["id"] == module_id:
            node["content_sha256"] = content_sha256
    canonical_edges = cast(list[dict[str, object]], canonical["edges"])
    old_edge = canonical_edges[0]
    old_edge["target"] = cast(str, canonical_nodes[0]["id"])
    if old_edge["source"] == old_edge["target"]:
        old_edge["target"] = cast(str, canonical_nodes[1]["id"])
    old_edge["type"] = "delta_relation"
    canonical_path.write_bytes(canonical_json_bytes(canonical))
    edges_path = output_root / "graph" / "edges.jsonl"
    edges = _jsonl(edges_path)
    edges[0] = canonical_edges[0]
    edges_path.write_bytes(b"".join(canonical_json_bytes(edge) for edge in edges))

    areas_path = output_root / "skill" / "references" / "indexes" / "areas.json"
    areas = _read_json(areas_path)
    area_records = cast(list[dict[str, object]], areas["areas"])
    changed_area_id = cast(str, area_records[0]["id"])
    area_records[0]["summary"] = "Módosított area összefoglaló."
    areas_path.write_bytes(canonical_json_bytes(areas))
    _refresh_manifest(output_root)
    return module_id, changed_area_id


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


def test_verify_portable_export_rejects_missing_file(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    (output_root / "graph" / "edges.jsonl").unlink()

    with pytest.raises(KnowledgeForgeError, match="missing"):
        verify_portable_export(output_root)


def test_verify_portable_export_rejects_manifest_digest_tamper(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    manifest_path = output_root / "export.json"
    manifest = _read_json(manifest_path)
    manifest["export_sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="digest mismatch"):
        verify_portable_export(output_root)


@pytest.mark.parametrize(
    ("format_version", "message"),
    [
        (None, "format version is missing"),
        ("1", "format version is malformed"),
        (2, "format version is incompatible"),
    ],
)
def test_verify_portable_export_rejects_invalid_format_versions(
    tmp_path: Path, format_version: object, message: str
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    manifest_path = output_root / "export.json"
    manifest = _read_json(manifest_path)
    if format_version is None:
        del manifest["format_version"]
    else:
        manifest["format_version"] = format_version
    manifest_without_digest = dict(manifest)
    manifest_without_digest.pop("export_sha256", None)
    manifest["export_sha256"] = sha256_bytes(canonical_json_bytes(manifest_without_digest))
    manifest_path.write_bytes(canonical_json_bytes(manifest))

    with pytest.raises(KnowledgeForgeError, match=message):
        verify_portable_export(output_root)


@pytest.mark.parametrize(
    ("format_version", "message"),
    [
        (None, "canonical graph format version is missing"),
        (True, "canonical graph format version is malformed"),
        ("1", "canonical graph format version is malformed"),
        (2, "canonical graph format version is incompatible"),
    ],
)
def test_verify_portable_export_rejects_invalid_graph_versions(
    tmp_path: Path, format_version: object, message: str
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    graph_path = output_root / "skill/references/graph/canonical.json"
    graph = _read_json(graph_path)
    if format_version is None:
        del graph["format_version"]
    else:
        graph["format_version"] = format_version
    graph_path.write_bytes(canonical_json_bytes(graph))
    _refresh_manifest(output_root)

    with pytest.raises(KnowledgeForgeError, match=message):
        verify_portable_export(output_root)


@pytest.mark.parametrize(
    ("format_version", "message"),
    [
        (None, "routing L0 index format version is missing"),
        (True, "routing L0 index format version is malformed"),
        ("1", "routing L0 index format version is malformed"),
        (2, "routing L0 index format version is incompatible"),
    ],
)
def test_route_portable_export_rejects_invalid_routing_versions(
    tmp_path: Path, format_version: object, message: str
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    index_path = output_root / "skill/references/indexes/l0.json"
    index = _read_json(index_path)
    if format_version is None:
        del index["format_version"]
    else:
        index["format_version"] = format_version
    index_path.write_bytes(canonical_json_bytes(index))
    _refresh_manifest(output_root)

    with pytest.raises(KnowledgeForgeError, match=message):
        route_portable_export(output_root, "Eszközszerződés")


def test_verify_portable_export_rejects_skill_reference_drift(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    skill_path = output_root / "skill" / "SKILL.md"
    skill_path.write_text(
        skill_path.read_text(encoding="utf-8").replace(
            "references/indexes/l0.json",
            "references/indexes/missing.json",
        ),
        encoding="utf-8",
    )
    _refresh_manifest(output_root)

    with pytest.raises(KnowledgeForgeError, match="Skill reference"):
        verify_portable_export(output_root)


def test_verify_portable_export_rejects_rag_identity_drift(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    rag_path = output_root / "rag" / "documents.jsonl"
    records = _jsonl(rag_path)
    records[0]["id"] = "module.unknown"
    rag_path.write_bytes(b"".join(canonical_json_bytes(record) for record in records))
    _refresh_manifest(output_root)

    with pytest.raises(KnowledgeForgeError, match="RAG"):
        verify_portable_export(output_root)


def test_verify_portable_export_rejects_graph_endpoint_drift(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    edges_path = output_root / "graph" / "edges.jsonl"
    edges = _jsonl(edges_path)
    edges[0]["target"] = "module.unknown"
    edges_path.write_bytes(b"".join(canonical_json_bytes(edge) for edge in edges))
    _refresh_manifest(output_root)

    with pytest.raises(KnowledgeForgeError, match="graph"):
        verify_portable_export(output_root)


def test_verify_portable_export_rejects_profile_count_drift(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    manifest_path = output_root / "export.json"
    manifest = _read_json(manifest_path)
    profiles = cast(dict[str, dict[str, object]], manifest["profiles"])
    profiles["rag"]["document_count"] = 192
    manifest["export_sha256"] = sha256_bytes(
        canonical_json_bytes({key: value for key, value in manifest.items() if key != "export_sha256"})
    )
    manifest_path.write_bytes(canonical_json_bytes(manifest))

    with pytest.raises(KnowledgeForgeError, match="profile"):
        verify_portable_export(output_root)


def test_diff_portable_exports_reports_unchanged_exports(tmp_path: Path) -> None:
    first_root = tmp_path / "derived" / "first"
    second_root = tmp_path / "derived" / "second"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, first_root)
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, second_root)

    delta = diff_portable_exports(first_root, second_root)

    assert delta["kind"] == "portable-agent-export-delta"
    assert delta["status"] == "unchanged"
    assert delta["modules"] == {
        "added": [],
        "removed": [],
        "changed": [],
        "unchanged_count": 193,
    }
    assert delta["relations"] == {"added": [], "removed": []}
    assert isinstance(delta["delta_sha256"], str)
    assert delta == diff_portable_exports(first_root, second_root)


def test_diff_portable_exports_reports_valid_target_changes(tmp_path: Path) -> None:
    base_root = tmp_path / "derived" / "base"
    target_root = tmp_path / "derived" / "target"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, base_root)
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, target_root)
    module_id, area_id = _mutate_valid_export(target_root)

    delta = diff_portable_exports(base_root, target_root)

    assert delta["status"] == "changed"
    modules = cast(dict[str, object], delta["modules"])
    assert modules["changed"] == [module_id]
    assert modules["unchanged_count"] == 192
    areas = cast(dict[str, object], delta["areas"])
    assert areas["changed"] == [area_id]
    relations = cast(dict[str, object], delta["relations"])
    assert len(cast(list[object], relations["added"])) == 1
    assert len(cast(list[object], relations["removed"])) == 1
    files = cast(dict[str, object], delta["files"])
    assert "rag/documents.jsonl" in files["changed"]
    assert "graph/edges.jsonl" in files["changed"]


def test_route_portable_export_reproduces_routing_contract(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    covered = route_portable_export(output_root, "Eszközszerződés")
    not_covered = route_portable_export(output_root, "Hogyan süssek kovászos kenyeret?")
    ambiguous = route_portable_export(output_root, "MCP vagy több ügynök együttműködés?")

    assert covered == {
        "format_version": 1,
        "status": "covered",
        "area_id": "tool-execution",
        "module_ids": ["procedure.tool-contract-design"],
    }
    assert not_covered == {
        "format_version": 1,
        "status": "not-covered",
        "area_id": None,
        "module_ids": [],
    }
    assert ambiguous == {
        "format_version": 1,
        "status": "ambiguous",
        "area_id": None,
        "module_ids": [],
        "alternatives": ["interaction-and-collaboration", "tool-execution"],
    }


def test_load_portable_context_returns_selected_markdown(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    manifest = build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    result = load_portable_context(output_root, "Eszközszerződés")
    module_path = (
        output_root
        / "skill"
        / "references"
        / "knowledge"
        / "procedure.tool-contract-design.md"
    )
    node_hashes = {
        node["id"]: node["content_sha256"]
        for node in _jsonl(output_root / "graph" / "nodes.jsonl")
    }

    assert result["status"] == "covered"
    assert result["area_id"] == "tool-execution"
    assert result["module_ids"] == ["procedure.tool-contract-design"]
    assert result["export_sha256"] == manifest["export_sha256"]
    assert result["modules"] == [
        {
            "id": "procedure.tool-contract-design",
            "content_sha256": node_hashes["procedure.tool-contract-design"],
            "text": module_path.read_text(encoding="utf-8"),
        }
    ]
    module = result["modules"][0]
    assert module["content_sha256"] == sha256_bytes(
        module["text"].encode("utf-8")
    )


@pytest.mark.parametrize(
    "query",
    ["Hogyan süssek kovászos kenyeret?", "MCP vagy több ügynök együttműködés?"],
)
def test_load_portable_context_does_not_load_unresolved_routes(
    tmp_path: Path, query: str
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    manifest = build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    result = load_portable_context(output_root, query)

    assert result["export_sha256"] == manifest["export_sha256"]
    assert result["modules"] == []


def test_load_portable_context_verifies_before_loading(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    module_path = (
        output_root
        / "skill"
        / "references"
        / "knowledge"
        / "procedure.tool-contract-design.md"
    )
    module_path.unlink()

    with pytest.raises(KnowledgeForgeError, match="missing"):
        load_portable_context(output_root, "Eszközszerződés")


def test_load_portable_context_graph_depth_zero_preserves_route(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    result = load_portable_context_graph(output_root, "Eszközszerződés", 0)

    assert result["module_ids"] == ["procedure.tool-contract-design"]
    assert result["expanded_module_ids"] == ["procedure.tool-contract-design"]
    assert result["relations"] == []
    assert len(result["modules"]) == 1


def test_load_portable_context_graph_depth_one_loads_direct_neighbors(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    result = load_portable_context_graph(output_root, "Eszközszerződés", 1)
    edges = _jsonl(output_root / "graph" / "edges.jsonl")
    seed = "procedure.tool-contract-design"
    expected_relations = sorted(
        (edge for edge in edges if seed in {edge["source"], edge["target"]}),
        key=lambda edge: (edge["source"], edge["type"], edge["target"]),
    )
    expected_ids = sorted(
        {seed}
        | {
            endpoint
            for edge in expected_relations
            for endpoint in (edge["source"], edge["target"])
        }
    )

    assert result["module_ids"] == [seed]
    assert result["expanded_module_ids"] == expected_ids
    assert result["relations"] == expected_relations
    assert [module["id"] for module in result["modules"]] == expected_ids
    assert all(
        module["content_sha256"] == sha256_bytes(module["text"].encode("utf-8"))
        for module in result["modules"]
    )


@pytest.mark.parametrize(
    "query",
    ["Hogyan süssek kovászos kenyeret?", "MCP vagy több ügynök együttműködés?"],
)
def test_load_portable_context_graph_keeps_unresolved_routes_empty(
    tmp_path: Path, query: str
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    result = load_portable_context_graph(output_root, query, 1)

    assert result["modules"] == []
    assert result["expanded_module_ids"] == []
    assert result["relations"] == []


@pytest.mark.parametrize("depth", [-1, 2, True, 1.5])
def test_load_portable_context_graph_rejects_invalid_depth(
    tmp_path: Path, depth: object
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    with pytest.raises(KnowledgeForgeError, match="relation depth"):
        load_portable_context_graph(output_root, "Eszközszerződés", depth)


def test_load_portable_context_budgeted_keeps_primary_and_records_omissions(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    primary_path = (
        output_root
        / "skill"
        / "references"
        / "knowledge"
        / "procedure.tool-contract-design.md"
    )
    primary_chars = len(primary_path.read_text(encoding="utf-8"))

    result = load_portable_context_budgeted(
        output_root, "Eszközszerződés", 1, primary_chars + 1
    )

    assert result["module_ids"] == ["procedure.tool-contract-design"]
    assert result["expanded_module_ids"] == ["procedure.tool-contract-design"]
    assert len(result["modules"]) == 1
    budget = result["budget"]
    assert budget["max_chars"] == primary_chars + 1
    assert budget["used_chars"] == primary_chars
    assert len(budget["omitted_module_ids"]) == 8
    assert result["relations"] == []


def test_load_portable_context_budgeted_admits_deterministic_neighbor(
    tmp_path: Path,
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    primary_id = "procedure.tool-contract-design"
    primary_chars = len(
        (
            output_root
            / "skill"
            / "references"
            / "knowledge"
            / f"{primary_id}.md"
        ).read_text(encoding="utf-8")
    )
    neighbor_id = "checklist.tool-safety-boundary"
    neighbor_chars = len(
        (
            output_root
            / "skill"
            / "references"
            / "knowledge"
            / f"{neighbor_id}.md"
        ).read_text(encoding="utf-8")
    )

    result = load_portable_context_budgeted(
        output_root,
        "Eszközszerződés",
        1,
        primary_chars + neighbor_chars,
    )

    assert result["expanded_module_ids"] == [neighbor_id, primary_id]
    assert result["budget"]["used_chars"] == primary_chars + neighbor_chars
    assert neighbor_id not in result["budget"]["omitted_module_ids"]
    assert all(
        edge["source"] in result["expanded_module_ids"]
        and edge["target"] in result["expanded_module_ids"]
        for edge in result["relations"]
    )


@pytest.mark.parametrize("max_chars", [-1, 0, 100001, True, 1.5])
def test_load_portable_context_budgeted_rejects_invalid_budget(
    tmp_path: Path, max_chars: object
) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)

    with pytest.raises(KnowledgeForgeError, match="character budget"):
        load_portable_context_budgeted(
            output_root, "Eszközszerződés", 1, max_chars
        )


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
