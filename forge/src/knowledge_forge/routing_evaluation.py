from collections import Counter
from pathlib import Path
from typing import cast

from knowledge_forge.audit import inspect_package
from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.indexes import load_indexes
from knowledge_forge.io import canonical_json_bytes, read_json, write_json_atomic
from knowledge_forge.paths import require_regular_file
from knowledge_forge.routing import route_query

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


def _metric(passed: int, total: int) -> dict[str, int]:
    return {
        "passed": passed,
        "total": total,
        "percent": (passed * 100) // total,
    }


def _actual_route(result: dict[str, object]) -> dict[str, object]:
    return {
        "status": result["status"],
        "area_id": result.get("area_id"),
        "module_ids": sorted(cast(list[str], result.get("module_ids", []))),
        "alternatives": sorted(cast(list[str], result.get("alternatives", []))),
    }


def _failure_reasons(
    case: dict[str, object], actual: dict[str, object]
) -> list[str]:
    reasons: list[str] = []
    if actual["status"] != case["expected_status"]:
        reasons.append("status")
    if actual["area_id"] != case["expected_area_id"]:
        reasons.append("area")
    if actual["module_ids"] != case["expected_module_ids"]:
        reasons.append("module")
    if actual["alternatives"] != case["expected_alternatives"]:
        reasons.append("alternatives")
    return sorted(reasons)


def evaluate_routing_suite(
    suite: dict[str, object], indexes: dict[str, object], package_sha256: str
) -> dict[str, object]:
    cases = sorted(
        cast(list[dict[str, object]], suite["cases"]),
        key=lambda case: cast(str, case["id"]),
    )
    category_counts = Counter(cast(str, case["category"]) for case in cases)
    metric_totals = {
        "canonical_area": category_counts["canonical"],
        "canonical_module": category_counts["canonical"],
        "paraphrase_route": category_counts["paraphrase"],
        "negative_rejection": category_counts["negative"],
        "ambiguity_exact_set": category_counts["ambiguous"],
    }
    metric_passed = dict.fromkeys(metric_totals, 0)
    per_area: dict[str, dict[str, int]] = {}
    failures: list[dict[str, object]] = []
    covered_without_module_count = 0

    for case in cases:
        actual = _actual_route(
            route_query(cast(str, case["query"]), indexes)
        )
        reasons = _failure_reasons(case, actual)
        passed = not reasons
        category = cast(str, case["category"])
        if actual["status"] == "covered" and not actual["module_ids"]:
            covered_without_module_count += 1
        if category == "canonical":
            if (
                actual["status"] == "covered"
                and actual["area_id"] == case["expected_area_id"]
            ):
                metric_passed["canonical_area"] += 1
            if (
                actual["status"] == "covered"
                and actual["module_ids"] == case["expected_module_ids"]
            ):
                metric_passed["canonical_module"] += 1
        elif category == "paraphrase" and passed:
            metric_passed["paraphrase_route"] += 1
        elif category == "negative" and passed:
            metric_passed["negative_rejection"] += 1
        elif category == "ambiguous" and passed:
            metric_passed["ambiguity_exact_set"] += 1

        if category in _COVERED_CATEGORIES:
            area_id = cast(str, case["expected_area_id"])
            area_metric = per_area.setdefault(area_id, {"passed": 0, "total": 0})
            area_metric["total"] += 1
            if passed:
                area_metric["passed"] += 1
        if reasons:
            failures.append(
                {
                    "case_id": case["id"],
                    "category": category,
                    "reasons": reasons,
                    "actual_status": actual["status"],
                    "actual_area_id": actual["area_id"],
                    "actual_module_ids": actual["module_ids"],
                    "actual_alternatives": actual["alternatives"],
                }
            )

    metrics = {
        name: _metric(metric_passed[name], total)
        for name, total in sorted(metric_totals.items())
    }
    thresholds = cast(dict[str, int], suite["thresholds"])
    threshold_metrics = [
        ("canonical_area_percent", "canonical_area"),
        ("canonical_module_percent", "canonical_module"),
        ("paraphrase_percent", "paraphrase_route"),
        ("negative_percent", "negative_rejection"),
        ("ambiguous_percent", "ambiguity_exact_set"),
    ]
    failed_metrics = [
        threshold_name
        for threshold_name, metric_name in threshold_metrics
        if metrics[metric_name]["percent"] < thresholds[threshold_name]
    ]
    if covered_without_module_count:
        failed_metrics.append("covered_without_module_count")

    suite_for_hash = dict(suite)
    suite_for_hash["cases"] = cases
    report_without_digest: dict[str, object] = {
        "format_version": 1,
        "status": "failed" if failed_metrics else "passed",
        "package_sha256": package_sha256,
        "suite_sha256": sha256_bytes(canonical_json_bytes(suite_for_hash)),
        "case_count": len(cases),
        "category_counts": dict(sorted(category_counts.items())),
        "canonical_target_count": len(
            {
                cast(list[str], case["expected_module_ids"])[0]
                for case in cases
                if case["category"] == "canonical"
            }
        ),
        "metrics": metrics,
        "per_area": dict(sorted(per_area.items())),
        "covered_without_module_count": covered_without_module_count,
        "failures": failures,
        "failed_metrics": failed_metrics,
    }
    report = dict(report_without_digest)
    report["evaluation_sha256"] = sha256_bytes(
        canonical_json_bytes(report_without_digest)
    )
    return report


def verify_routing_evaluation(
    pack_root: Path,
    schema_root: Path,
    suite_path: Path,
    report_path: Path,
) -> dict[str, object]:
    profile = inspect_package(pack_root, schema_root)
    indexes = load_indexes(pack_root)
    suite = load_routing_suite(
        suite_path, schema_root / "routing-evaluation.schema.json", indexes
    )
    report = evaluate_routing_suite(
        suite, indexes, cast(str, profile["package_sha256"])
    )
    write_json_atomic(report_path, report)
    failed_metrics = cast(list[str], report["failed_metrics"])
    if failed_metrics:
        failed_metric = failed_metrics[0].replace("_", " ")
        raise KnowledgeForgeError(f"Routing evaluation failed: {failed_metric}")
    return report
