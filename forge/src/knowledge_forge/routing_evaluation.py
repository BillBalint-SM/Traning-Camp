from collections import Counter
from pathlib import Path
from typing import cast

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.io import read_json
from knowledge_forge.paths import require_regular_file

_COVERED_CATEGORIES = {"canonical", "paraphrase"}


def _known_endpoints(
    indexes: dict[str, object],
) -> tuple[set[str], dict[str, str]]:
    l0 = cast(dict[str, object], indexes["l0"])
    l1 = cast(dict[str, dict[str, object]], indexes["l1"])
    area_ids = {
        cast(str, area["id"])
        for area in cast(list[dict[str, object]], l0["areas"])
    }
    module_areas: dict[str, str] = {}
    for area_id, area_index in l1.items():
        for module in cast(list[dict[str, object]], area_index["modules"]):
            module_id = cast(str, module["id"])
            if module_id in module_areas:
                raise KnowledgeForgeError(
                    f"Routing indexes contain duplicate module: {module_id}"
                )
            module_areas[module_id] = area_id
    return area_ids, module_areas


def _validate_expectation(
    case: dict[str, object], area_ids: set[str], module_areas: dict[str, str]
) -> None:
    case_id = cast(str, case["id"])
    category = cast(str, case["category"])
    status = cast(str, case["expected_status"])
    area_id = cast(str | None, case["expected_area_id"])
    module_ids = cast(list[str], case["expected_module_ids"])
    alternatives = cast(list[str], case["expected_alternatives"])

    if area_id is not None and area_id not in area_ids:
        raise KnowledgeForgeError(f"Routing evaluation has unknown area: {case_id}")
    unknown_modules = sorted(set(module_ids) - set(module_areas))
    if unknown_modules:
        raise KnowledgeForgeError(
            f"Routing evaluation has unknown module: {unknown_modules[0]}"
        )
    unknown_alternatives = sorted(set(alternatives) - area_ids)
    if unknown_alternatives:
        raise KnowledgeForgeError(
            f"Routing evaluation has unknown alternative area: {unknown_alternatives[0]}"
        )
    if alternatives != sorted(alternatives):
        raise KnowledgeForgeError(
            f"Routing evaluation requires sorted alternatives: {case_id}"
        )

    if category in _COVERED_CATEGORIES:
        if (
            status != "covered"
            or area_id is None
            or len(module_ids) != 1
            or alternatives
        ):
            raise KnowledgeForgeError(
                f"Routing evaluation has invalid {category} expectation: {case_id}"
            )
        if module_areas[module_ids[0]] != area_id:
            raise KnowledgeForgeError(
                f"Routing evaluation module is outside expected area: {case_id}"
            )
        return
    if category == "negative":
        if status != "not-covered" or area_id is not None or module_ids or alternatives:
            raise KnowledgeForgeError(
                f"Routing evaluation has invalid negative expectation: {case_id}"
            )
        return
    if (
        status != "ambiguous"
        or area_id is not None
        or module_ids
        or len(alternatives) < 2
    ):
        raise KnowledgeForgeError(
            f"Routing evaluation has invalid ambiguous expectation: {case_id}"
        )


def load_routing_suite(
    suite_path: Path, schema_path: Path, indexes: dict[str, object]
) -> dict[str, object]:
    require_regular_file(suite_path, "Routing evaluation suite")
    payload = read_json(suite_path)
    validate_record(schema_path, payload, suite_path.name)
    suite = cast(dict[str, object], payload)
    cases = cast(list[dict[str, object]], suite["cases"])
    case_ids = [cast(str, case["id"]) for case in cases]
    duplicate_case_ids = sorted(
        case_id for case_id, count in Counter(case_ids).items() if count > 1
    )
    if duplicate_case_ids:
        raise KnowledgeForgeError(
            f"Routing evaluation contains duplicate case ID: {duplicate_case_ids[0]}"
        )

    expected_counts = cast(dict[str, int], suite["expected_counts"])
    actual_counts = Counter(cast(str, case["category"]) for case in cases)
    if dict(sorted(actual_counts.items())) != dict(sorted(expected_counts.items())):
        raise KnowledgeForgeError("Routing evaluation category counts do not match")

    area_ids, module_areas = _known_endpoints(indexes)
    for case in cases:
        _validate_expectation(case, area_ids, module_areas)

    canonical_targets = [
        cast(list[str], case["expected_module_ids"])[0]
        for case in cases
        if case["category"] == "canonical"
    ]
    if Counter(canonical_targets) != Counter(module_areas.keys()):
        raise KnowledgeForgeError(
            "Routing evaluation canonical target coverage does not match public modules"
        )

    validated = dict(suite)
    validated["cases"] = sorted(cases, key=lambda case: cast(str, case["id"]))
    return validated
