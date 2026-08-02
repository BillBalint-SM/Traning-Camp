import json
from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.indexes import load_indexes
from knowledge_forge.routing_evaluation import load_routing_suite

ROOT = Path(__file__).parents[1]
PACK_ROOT = ROOT / "pack"
SCHEMA_PATH = ROOT / "forge" / "schemas" / "routing-evaluation.schema.json"


def _suite_payload() -> dict[str, object]:
    indexes = load_indexes(PACK_ROOT)
    l1 = cast(dict[str, dict[str, object]], indexes["l1"])
    module_areas = {
        cast(str, module["id"]): area_id
        for area_id, area_index in l1.items()
        for module in cast(list[dict[str, object]], area_index["modules"])
    }
    canonical_cases = [
        {
            "id": f"canonical.{module_id}.01",
            "category": "canonical",
            "query": f"Működési kérdés ehhez: {module_id}",
            "expected_status": "covered",
            "expected_area_id": module_areas[module_id],
            "expected_module_ids": [module_id],
            "expected_alternatives": [],
        }
        for module_id in sorted(module_areas)
    ]
    area_ids = sorted(l1)
    paraphrase_cases = [
        {
            "id": f"paraphrase.{area_id}.{number:02d}",
            "category": "paraphrase",
            "query": f"Átfogalmazott működési kérdés {area_id} {number}",
            "expected_status": "covered",
            "expected_area_id": area_id,
            "expected_module_ids": [
                cast(list[dict[str, object]], l1[area_id]["modules"])[0]["id"]
            ],
            "expected_alternatives": [],
        }
        for area_id in area_ids
        for number in range(1, 5)
    ]
    negative_cases = [
        {
            "id": f"negative.unsupported.{number:02d}",
            "category": "negative",
            "query": f"Nem támogatott működési kérdés {number}",
            "expected_status": "not-covered",
            "expected_area_id": None,
            "expected_module_ids": [],
            "expected_alternatives": [],
        }
        for number in range(1, 21)
    ]
    alternatives = area_ids[:2]
    ambiguous_cases = [
        {
            "id": f"ambiguous.cross-area.{number:02d}",
            "category": "ambiguous",
            "query": f"Két területet érintő kérdés {number}",
            "expected_status": "ambiguous",
            "expected_area_id": None,
            "expected_module_ids": [],
            "expected_alternatives": alternatives,
        }
        for number in range(1, 11)
    ]
    return {
        "format_version": 1,
        "expected_counts": {
            "canonical": 193,
            "paraphrase": 40,
            "negative": 20,
            "ambiguous": 10,
        },
        "thresholds": {
            "canonical_area_percent": 100,
            "canonical_module_percent": 100,
            "paraphrase_percent": 90,
            "negative_percent": 100,
            "ambiguous_percent": 100,
        },
        "cases": canonical_cases
        + paraphrase_cases
        + negative_cases
        + ambiguous_cases,
    }


def _write_suite(tmp_path: Path, payload: dict[str, object]) -> Path:
    suite_path = tmp_path / "routing-suite.json"
    suite_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return suite_path


def _load(tmp_path: Path, payload: dict[str, object]) -> dict[str, object]:
    return load_routing_suite(
        _write_suite(tmp_path, payload), SCHEMA_PATH, load_indexes(PACK_ROOT)
    )


def test_load_routing_suite_accepts_complete_contract(tmp_path: Path) -> None:
    suite = _load(tmp_path, _suite_payload())

    cases = cast(list[dict[str, object]], suite["cases"])
    assert len(cases) == 263
    assert [case["id"] for case in cases] == sorted(
        cast(str, case["id"]) for case in cases
    )


def test_load_routing_suite_rejects_schema_violation(tmp_path: Path) -> None:
    payload = _suite_payload()
    payload["unexpected"] = True

    with pytest.raises(KnowledgeForgeError, match="Schema validation failed"):
        _load(tmp_path, payload)


def test_load_routing_suite_rejects_duplicate_case_id(tmp_path: Path) -> None:
    payload = _suite_payload()
    cases = cast(list[dict[str, object]], payload["cases"])
    cases[1]["id"] = cases[0]["id"]

    with pytest.raises(KnowledgeForgeError, match="duplicate case ID"):
        _load(tmp_path, payload)


def test_load_routing_suite_rejects_canonical_target_coverage_mismatch(
    tmp_path: Path,
) -> None:
    payload = _suite_payload()
    cases = cast(list[dict[str, object]], payload["cases"])
    canonical_cases = [case for case in cases if case["category"] == "canonical"]
    first = canonical_cases[0]
    second = next(
        case
        for case in canonical_cases[1:]
        if case["expected_area_id"] == first["expected_area_id"]
    )
    second["expected_module_ids"] = deepcopy(first["expected_module_ids"])

    with pytest.raises(KnowledgeForgeError, match="canonical target coverage"):
        _load(tmp_path, payload)


def test_load_routing_suite_rejects_unknown_module(tmp_path: Path) -> None:
    payload = _suite_payload()
    cases = cast(list[dict[str, object]], payload["cases"])
    cases[0]["expected_module_ids"] = ["principle.unknown"]

    with pytest.raises(KnowledgeForgeError, match="unknown module"):
        _load(tmp_path, payload)


def test_load_routing_suite_rejects_unknown_area(tmp_path: Path) -> None:
    payload = _suite_payload()
    cases = cast(list[dict[str, object]], payload["cases"])
    cases[0]["expected_area_id"] = "unknown-area"

    with pytest.raises(KnowledgeForgeError, match="unknown area"):
        _load(tmp_path, payload)


def test_load_routing_suite_rejects_unsorted_alternatives(tmp_path: Path) -> None:
    payload = _suite_payload()
    cases = cast(list[dict[str, object]], payload["cases"])
    ambiguous = next(case for case in cases if case["category"] == "ambiguous")
    alternatives = cast(list[str], ambiguous["expected_alternatives"])
    ambiguous["expected_alternatives"] = list(reversed(alternatives))

    with pytest.raises(KnowledgeForgeError, match="sorted alternatives"):
        _load(tmp_path, payload)


def test_load_routing_suite_rejects_category_expectation_mismatch(
    tmp_path: Path,
) -> None:
    payload = _suite_payload()
    cases = cast(list[dict[str, object]], payload["cases"])
    cases[0]["expected_status"] = "not-covered"

    with pytest.raises(KnowledgeForgeError, match="invalid canonical expectation"):
        _load(tmp_path, payload)
