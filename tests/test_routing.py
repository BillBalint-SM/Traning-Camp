from copy import deepcopy
from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.graph import build_graph
from knowledge_forge.indexes import build_indexes, load_areas
from knowledge_forge.io import canonical_json_bytes
from knowledge_forge.package import discover_modules
from knowledge_forge.routing import route_query

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_PATH = ROOT / "forge" / "schemas" / "knowledge-module.schema.json"


def _indexes() -> dict[str, object]:
    modules = discover_modules(PACK_ROOT, SCHEMA_PATH)
    areas = load_areas(PACK_ROOT / "indexes" / "areas.json")
    return build_indexes(modules, areas)


def test_route_query_selects_minimal_context_for_compression() -> None:
    result = route_query("Kontextustömörítés szükséges?", _indexes())

    assert result["status"] == "covered"
    assert result["area_id"] == "context-and-knowledge"
    assert result["module_ids"] == ["pattern.context-compression"]


@pytest.mark.parametrize(
    ("query", "area_id", "module_id"),
    [
        (
            "Mikor válasszak determinisztikus workflow-t autonóm döntéshozatal helyett?",
            "core-agent-systems",
            "decision-guide.workflow-or-autonomy",
        ),
        (
            "Mikor kell hibrid retrievalt használnom a tudás visszakereséséhez?",
            "context-and-knowledge",
            "decision-guide.retrieval-strategy-selection",
        ),
        (
            "Hogyan szakítsak meg biztonságosan egy aszinkron agent futást?",
            "tool-execution",
            "procedure.async-interruption-handling",
        ),
        (
            "Milyen agent observability jeleket gyűjtsek?",
            "evaluation-and-improvement",
            "checklist.agent-observability",
        ),
        (
            "Mit tartalmazzon egy több agent közötti átadási szerződés?",
            "interaction-and-collaboration",
            "procedure.multi-agent-handoff-contract",
        ),
    ],
)
def test_route_query_selects_deep_module(
    query: str, area_id: str, module_id: str
) -> None:
    result = route_query(query, _indexes())

    assert result == {
        "status": "covered",
        "area_id": area_id,
        "module_ids": [module_id],
    }


@pytest.mark.parametrize(
    ("query", "area_id", "module_id"),
    [
        (
            "Hogyan válasszak modellt egy eszközhasználó agenthez?",
            "core-agent-systems",
            "decision-guide.agent-model-selection",
        ),
        (
            "Hova kerüljön a stabil kontextus a cache találati arányához?",
            "context-and-knowledge",
            "procedure.cache-stable-context-layout",
        ),
        (
            "Milyen memóriaszinteket kezeljek egy felhasználóhoz?",
            "context-and-knowledge",
            "pattern.memory-hierarchy",
        ),
        (
            "Mikor egyesítsem a sűrű és ritka keresési találatokat?",
            "context-and-knowledge",
            "procedure.hybrid-retrieval-fusion",
        ),
        (
            "Mikor készítsek dedikált eszközt skill és általános végrehajtó helyett?",
            "tool-execution",
            "decision-guide.tool-or-skill-executor",
        ),
        (
            "Hogyan kommunikáljak a felhasználóval hosszú aszinkron futás közben?",
            "tool-execution",
            "procedure.user-communication-during-async-execution",
        ),
    ],
)
def test_route_query_selects_operational_module(
    query: str, area_id: str, module_id: str
) -> None:
    result = route_query(query, _indexes())

    assert result == {
        "status": "covered",
        "area_id": area_id,
        "module_ids": [module_id],
    }


def test_route_query_returns_not_covered_without_inventing_route() -> None:
    result = route_query("Melyik notebook gépet válasszam?", _indexes())

    assert result == {"status": "not-covered", "area_id": None, "module_ids": []}


def test_route_query_exposes_ambiguous_areas() -> None:
    result = route_query("MCP vagy több ügynök együttműködés?", _indexes())

    assert result["status"] == "ambiguous"
    assert result["area_id"] is None
    assert set(result["alternatives"]) == {
        "interaction-and-collaboration",
        "tool-execution",
    }


def test_build_graph_resolves_every_edge() -> None:
    graph = build_graph(discover_modules(PACK_ROOT, SCHEMA_PATH))

    identifiers = {node["id"] for node in graph["nodes"]}
    assert len(identifiers) == 87
    assert all(edge["source"] in identifiers for edge in graph["edges"])
    assert all(edge["target"] in identifiers for edge in graph["edges"])
    assert all(edge["source"] != edge["target"] for edge in graph["edges"])


def test_build_graph_rejects_dangling_edge() -> None:
    modules = deepcopy(discover_modules(PACK_ROOT, SCHEMA_PATH))
    modules[0]["metadata"]["relations"] = [
        {"type": "supports", "target": "principle.missing"}
    ]

    with pytest.raises(KnowledgeForgeError, match="missing target"):
        build_graph(modules)


def test_indexes_stay_within_context_budget() -> None:
    indexes = _indexes()

    assert len(canonical_json_bytes(indexes["l0"])) <= 8192
    assert all(
        len(canonical_json_bytes(index)) <= 8192
        for index in indexes["l1"].values()
    )
