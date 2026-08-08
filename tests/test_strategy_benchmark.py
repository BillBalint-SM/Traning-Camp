from pathlib import Path
from typing import cast

import pytest
from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import canonical_json_bytes, read_json
from knowledge_forge.lexical_index import build_portable_lexical_index
from knowledge_forge.strategy_benchmark import (
    _run_graph_strategy_case,
    load_graph_strategy_suite,
)

ROOT = Path(__file__).parents[1]
SCHEMA_ROOT = ROOT / "forge" / "schemas"
SUITE_SCHEMA = SCHEMA_ROOT / "graph-strategy-suite.schema.json"
REQUEST_SCHEMA = SCHEMA_ROOT / "answer-evaluation-request.schema.json"
GRAPH_STRATEGY_SUITE = ROOT / "forge" / "evals" / "graph-strategy-v1.json"
V10_EXPORT_SHA256 = "bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2"


def test_frozen_graph_strategy_suite_is_canonical_and_bound_to_v10() -> None:
    payload = read_json(GRAPH_STRATEGY_SUITE)
    assert isinstance(payload, dict)
    suite = cast(dict[str, object], payload)

    validate_record(SUITE_SCHEMA, suite, "graph strategy suite")

    without_digest = {
        key: value for key, value in suite.items() if key != "suite_sha256"
    }
    cases = cast(list[dict[str, object]], suite["cases"])
    assert suite["export_sha256"] == V10_EXPORT_SHA256
    assert suite["suite_sha256"] == sha256_bytes(canonical_json_bytes(without_digest))
    assert suite["expected_counts"] == {
        "ambiguous": 10,
        "canonical": 193,
        "negative": 20,
        "paraphrase": 40,
    }
    assert len(cases) == 263
    assert [case["id"] for case in cases] == sorted(case["id"] for case in cases)


def test_answer_evaluation_request_schema_rejects_raw_query() -> None:
    request = {
        "format_version": 1,
        "kind": "answer-evaluation-request",
        "case_id": "canonical.procedure.tool-contract-design.01",
        "query_sha256": "a" * 64,
        "export_sha256": "b" * 64,
        "strategy_id": "lexical-v1",
        "context_trace_sha256": "c" * 64,
        "expected_module_ids": ["procedure.tool-contract-design"],
        "request_sha256": "d" * 64,
        "query": "This must not become part of the evaluator request.",
    }

    with pytest.raises(KnowledgeForgeError, match="Additional properties"):
        validate_record(REQUEST_SCHEMA, request, "answer evaluation request")


def test_graph_strategy_suite_loads_against_the_bound_portable_export() -> None:
    suite = load_graph_strategy_suite(
        GRAPH_STRATEGY_SUITE,
        ROOT / "exports" / "portable-exports-v10",
    )

    cases = cast(list[dict[str, object]], suite["cases"])
    assert len(cases) == 263
    assert suite["export_sha256"] == V10_EXPORT_SHA256
    assert cases[0]["id"] == "ambiguous.cross-area.01"


def test_graph_strategy_case_records_two_traced_real_contexts(tmp_path: Path) -> None:
    export_root = ROOT / "exports" / "portable-exports-v10"
    index_root = tmp_path / "derived" / "index"
    build_portable_lexical_index(export_root, index_root)
    suite = load_graph_strategy_suite(GRAPH_STRATEGY_SUITE, export_root)
    case = next(
        case
        for case in cast(list[dict[str, object]], suite["cases"])
        if case["id"] == "canonical.procedure.tool-contract-design.01"
    )

    result, timing = _run_graph_strategy_case(export_root, index_root, case, 100000, 1)

    strategies = cast(list[dict[str, object]], result["strategies"])
    assert result["case_id"] == "canonical.procedure.tool-contract-design.01"
    assert [strategy["strategy_id"] for strategy in strategies] == [
        "baseline-depth-1",
        "lexical-v1",
    ]
    assert all(strategy["integrity"] is True for strategy in strategies)
    assert all(
        cast(str, case["query"])
        not in canonical_json_bytes(strategy).decode("utf-8")
        for strategy in strategies
    )
    assert set(timing) == {"baseline-depth-1", "lexical-v1"}
