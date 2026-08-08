from collections import Counter
from math import ceil
from pathlib import Path
from statistics import median_low
from tempfile import TemporaryDirectory
from time import perf_counter_ns
from typing import cast

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import (
    canonical_json_bytes,
    read_json,
    read_jsonl,
    write_json_atomic,
)
from knowledge_forge.lexical_index import (
    load_portable_context_lexical,
    verify_portable_lexical_index,
)
from knowledge_forge.measurement import (
    build_context_trace,
    validate_context_trace,
    verify_context_traces,
    write_context_traces,
)
from knowledge_forge.paths import require_regular_file
from knowledge_forge.portability import (
    load_portable_context_budgeted,
    verify_portable_export,
)

_SUITE_SCHEMA_PATH = (
    Path(__file__).parents[2] / "schemas" / "graph-strategy-suite.schema.json"
)
_REPORT_SCHEMA_PATH = (
    Path(__file__).parents[2] / "schemas" / "graph-strategy-benchmark.schema.json"
)
_COVERED_CATEGORIES = {"canonical", "paraphrase"}
_STRATEGY_IDS = ("baseline-depth-1", "lexical-v1")
_MINIMUM_REPEAT_COUNT = 3


def _require_digest(value: object, label: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise KnowledgeForgeError(f"Graph strategy suite {label} is invalid")
    return value


def _portable_endpoints(export_root: Path) -> tuple[set[str], dict[str, str]]:
    areas_payload = read_json(
        export_root / "skill" / "references" / "indexes" / "areas.json"
    )
    if not isinstance(areas_payload, dict):
        raise KnowledgeForgeError("Graph strategy suite portable areas are invalid")
    areas_value = areas_payload.get("areas")
    if not isinstance(areas_value, list):
        raise KnowledgeForgeError("Graph strategy suite portable areas are incomplete")
    area_ids: set[str] = set()
    module_areas: dict[str, str] = {}
    for area_value in areas_value:
        if not isinstance(area_value, dict):
            raise KnowledgeForgeError("Graph strategy suite portable area is invalid")
        area = cast(dict[str, object], area_value)
        area_id = area.get("id")
        module_ids = area.get("module_ids")
        if not isinstance(area_id, str) or not area_id:
            raise KnowledgeForgeError("Graph strategy suite portable area ID is invalid")
        if area_id in area_ids:
            raise KnowledgeForgeError(f"Graph strategy suite area is duplicated: {area_id}")
        if not isinstance(module_ids, list) or not all(
            isinstance(module_id, str) and module_id for module_id in module_ids
        ):
            raise KnowledgeForgeError(
                f"Graph strategy suite area modules are invalid: {area_id}"
            )
        area_ids.add(area_id)
        for module_id in module_ids:
            assert isinstance(module_id, str)
            if module_id in module_areas:
                raise KnowledgeForgeError(
                    f"Graph strategy suite module is duplicated: {module_id}"
                )
            module_areas[module_id] = area_id
    node_ids = {
        cast(str, node["id"])
        for node in read_jsonl(export_root / "graph" / "nodes.jsonl")
        if isinstance(node.get("id"), str)
    }
    if node_ids != set(module_areas):
        raise KnowledgeForgeError("Graph strategy suite portable module ownership drift")
    return area_ids, module_areas


def _validate_case(
    case: dict[str, object], area_ids: set[str], module_areas: dict[str, str]
) -> None:
    case_id = cast(str, case["id"])
    category = cast(str, case["category"])
    status = cast(str, case["expected_status"])
    area_id = cast(str | None, case["expected_area_id"])
    module_ids = cast(list[str], case["expected_module_ids"])
    alternatives = cast(list[str], case["expected_alternatives"])
    if area_id is not None and area_id not in area_ids:
        raise KnowledgeForgeError(f"Graph strategy suite has unknown area: {case_id}")
    unknown_modules = sorted(set(module_ids) - set(module_areas))
    if unknown_modules:
        raise KnowledgeForgeError(
            f"Graph strategy suite has unknown module: {unknown_modules[0]}"
        )
    unknown_alternatives = sorted(set(alternatives) - area_ids)
    if unknown_alternatives:
        raise KnowledgeForgeError(
            "Graph strategy suite has unknown alternative area: "
            f"{unknown_alternatives[0]}"
        )
    if module_ids != sorted(module_ids) or alternatives != sorted(alternatives):
        raise KnowledgeForgeError(
            f"Graph strategy suite requires sorted expectations: {case_id}"
        )
    if category in _COVERED_CATEGORIES:
        if (
            status != "covered"
            or area_id is None
            or len(module_ids) != 1
            or alternatives
            or module_areas[module_ids[0]] != area_id
        ):
            raise KnowledgeForgeError(
                f"Graph strategy suite has invalid {category} expectation: {case_id}"
            )
        return
    if category == "negative":
        if status != "not-covered" or area_id is not None or module_ids or alternatives:
            raise KnowledgeForgeError(
                f"Graph strategy suite has invalid negative expectation: {case_id}"
            )
        return
    if (
        status != "ambiguous"
        or area_id is not None
        or module_ids
        or len(alternatives) < 2
    ):
        raise KnowledgeForgeError(
            f"Graph strategy suite has invalid ambiguous expectation: {case_id}"
        )


def load_graph_strategy_suite(
    suite_path: Path, export_root: Path
) -> dict[str, object]:
    require_regular_file(suite_path, "Graph strategy suite")
    payload = read_json(suite_path)
    if not isinstance(payload, dict):
        raise KnowledgeForgeError("Graph strategy suite root must be an object")
    suite = cast(dict[str, object], payload)
    validate_record(_SUITE_SCHEMA_PATH, suite, "graph strategy suite")
    claimed_digest = _require_digest(suite.get("suite_sha256"), "digest")
    without_digest = {key: value for key, value in suite.items() if key != "suite_sha256"}
    if sha256_bytes(canonical_json_bytes(without_digest)) != claimed_digest:
        raise KnowledgeForgeError("Graph strategy suite digest mismatch")
    manifest = verify_portable_export(export_root)
    if suite["export_sha256"] != manifest.get("export_sha256"):
        raise KnowledgeForgeError("Graph strategy suite export digest does not match export")
    cases = cast(list[dict[str, object]], suite["cases"])
    case_ids = [cast(str, case["id"]) for case in cases]
    duplicates = sorted(
        case_id for case_id, count in Counter(case_ids).items() if count > 1
    )
    if duplicates:
        raise KnowledgeForgeError(f"Graph strategy suite has duplicate case ID: {duplicates[0]}")
    expected_counts = cast(dict[str, int], suite["expected_counts"])
    actual_counts = Counter(cast(str, case["category"]) for case in cases)
    if dict(sorted(actual_counts.items())) != dict(sorted(expected_counts.items())):
        raise KnowledgeForgeError("Graph strategy suite category counts do not match")
    area_ids, module_areas = _portable_endpoints(export_root)
    for case in cases:
        _validate_case(case, area_ids, module_areas)
    canonical_targets = [
        cast(list[str], case["expected_module_ids"])[0]
        for case in cases
        if case["category"] == "canonical"
    ]
    if Counter(canonical_targets) != Counter(module_areas.keys()):
        raise KnowledgeForgeError(
            "Graph strategy suite canonical target coverage does not match export"
        )
    validated = dict(suite)
    validated["cases"] = sorted(cases, key=lambda case: cast(str, case["id"]))
    return validated


def _route_from_case(case: dict[str, object]) -> dict[str, object]:
    return {
        "status": case["expected_status"],
        "area_id": case["expected_area_id"],
        "module_ids": cast(list[str], case["expected_module_ids"]),
        "alternatives": cast(list[str], case["expected_alternatives"]),
    }


def _route_from_trace(trace: dict[str, object]) -> dict[str, object]:
    route_value = trace.get("route")
    if not isinstance(route_value, dict):
        raise KnowledgeForgeError("Graph strategy trace route is invalid")
    route = cast(dict[str, object], route_value)
    return {
        "status": route["status"],
        "area_id": route["area_id"],
        "module_ids": route["primary_module_ids"],
        "alternatives": route["alternative_area_ids"],
    }


def _selection_projection(
    strategy_id: str, trace: dict[str, object]
) -> dict[str, object]:
    return {
        "strategy_id": strategy_id,
        "route": _route_from_trace(trace),
        "context": trace["context"],
        "module_hashes": trace["module_hashes"],
        "budget": trace["budget"],
        "integrity": True,
    }


def _selection_digest(selection: dict[str, object]) -> str:
    return sha256_bytes(canonical_json_bytes(selection))


def _milliseconds(elapsed_ns: int) -> int:
    return elapsed_ns // 1_000_000


def _run_strategy(
    strategy_id: str,
    export_root: Path,
    index_root: Path,
    query: str,
    max_chars: int,
    repeat_count: int,
) -> tuple[dict[str, object], list[int]]:
    relation_depth = 1 if strategy_id == "baseline-depth-1" else 0
    first_context: dict[str, object] | None = None
    first_elapsed_ns = 0
    first_selection: dict[str, object] | None = None
    elapsed_samples: list[int] = []
    for _ in range(repeat_count):
        started_ns = perf_counter_ns()
        if strategy_id == "baseline-depth-1":
            context = load_portable_context_budgeted(
                export_root, query, relation_depth, max_chars
            )
        else:
            context = load_portable_context_lexical(
                export_root, index_root, query, max_chars
            )
        elapsed_ns = perf_counter_ns() - started_ns
        timing_ms = _milliseconds(elapsed_ns)
        trace = build_context_trace(
            query,
            context,
            relation_depth,
            {"route": 0, "load": timing_ms, "total": timing_ms},
        )
        validate_context_trace(trace)
        selection = _selection_projection(strategy_id, trace)
        if first_selection is not None and selection != first_selection:
            raise KnowledgeForgeError("Graph strategy selection is not deterministic")
        if first_context is None:
            first_context = context
            first_elapsed_ns = elapsed_ns
            first_selection = selection
        elapsed_samples.append(elapsed_ns)
    if first_context is None or first_selection is None:
        raise KnowledgeForgeError("Graph strategy requires at least one repeat")
    trace = build_context_trace(
        query,
        first_context,
        relation_depth,
        {
            "route": 0,
            "load": _milliseconds(first_elapsed_ns),
            "total": _milliseconds(first_elapsed_ns),
        },
    )
    validate_context_trace(trace)
    selection = _selection_projection(strategy_id, trace)
    return {
        "strategy_id": strategy_id,
        "actual": _route_from_trace(trace),
        "context_trace": trace,
        "selection_sha256": _selection_digest(selection),
        "integrity": True,
    }, elapsed_samples


def _run_graph_strategy_case(
    export_root: Path,
    index_root: Path,
    case: dict[str, object],
    max_chars: int,
    repeat_count: int,
) -> tuple[dict[str, object], dict[str, list[int]]]:
    query = case.get("query")
    if not isinstance(query, str) or not query:
        raise KnowledgeForgeError("Graph strategy suite query is invalid")
    strategies: list[dict[str, object]] = []
    timings: dict[str, list[int]] = {}
    for strategy_id in _STRATEGY_IDS:
        result, samples = _run_strategy(
            strategy_id,
            export_root,
            index_root,
            query,
            max_chars,
            repeat_count,
        )
        strategies.append(result)
        timings[strategy_id] = samples
    traces = [
        cast(dict[str, object], strategy["context_trace"])
        for strategy in strategies
    ]
    with TemporaryDirectory(prefix="graph-strategy-traces-") as directory:
        trace_path = Path(directory) / "traces.jsonl"
        write_context_traces(trace_path, traces)
        verify_context_traces(trace_path, export_root)
    return {
        "case_id": case["id"],
        "category": case["category"],
        "expected": _route_from_case(case),
        "strategies": strategies,
    }, timings


def _metric(passed: int, total: int) -> dict[str, int]:
    return {"passed": passed, "total": total, "percent": (passed * 100) // total}


def _strategy_metrics(case_results: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    metrics: dict[str, dict[str, object]] = {}
    for strategy_id in _STRATEGY_IDS:
        covered_total = 0
        primary_passed = 0
        area_passed = 0
        negative_total = 0
        negative_passed = 0
        ambiguous_total = 0
        ambiguous_passed = 0
        integrity_passed = 0
        admitted_chars: list[int] = []
        for case_result in case_results:
            category = cast(str, case_result["category"])
            expected = cast(dict[str, object], case_result["expected"])
            strategy = next(
                strategy
                for strategy in cast(list[dict[str, object]], case_result["strategies"])
                if strategy["strategy_id"] == strategy_id
            )
            actual = cast(dict[str, object], strategy["actual"])
            trace = cast(dict[str, object], strategy["context_trace"])
            trace_context = cast(dict[str, object], trace["context"])
            trace_budget = cast(dict[str, object], trace["budget"])
            admitted = cast(list[str], trace_context["admitted_module_ids"])
            admitted_chars.append(cast(int, trace_budget["used_chars"]))
            if strategy["integrity"] is True:
                integrity_passed += 1
            if category in _COVERED_CATEGORIES:
                covered_total += 1
                if (
                    actual["status"] == "covered"
                    and actual["module_ids"] == expected["module_ids"]
                ):
                    primary_passed += 1
                if (
                    actual["status"] == "covered"
                    and actual["area_id"] == expected["area_id"]
                ):
                    area_passed += 1
            elif category == "negative":
                negative_total += 1
                if actual["status"] == "not-covered" and not admitted:
                    negative_passed += 1
            else:
                ambiguous_total += 1
                if actual["status"] == "ambiguous" and not admitted:
                    ambiguous_passed += 1
        metrics[strategy_id] = {
            "primary_coverage": _metric(primary_passed, covered_total),
            "area_coverage": _metric(area_passed, covered_total),
            "negative_rejection": _metric(negative_passed, negative_total),
            "ambiguity_fail_closed": _metric(ambiguous_passed, ambiguous_total),
            "integrity": _metric(integrity_passed, len(case_results)),
            "median_admitted_chars": median_low(admitted_chars),
        }
    return metrics


def _nearest_rank_p95(samples_ns: list[int]) -> int:
    ordered = sorted(samples_ns)
    return ordered[ceil(len(ordered) * 0.95) - 1]


def _timing_projection(samples: dict[str, list[int]]) -> dict[str, object]:
    return {
        "strategy_ids": list(_STRATEGY_IDS),
        "samples_ns": {strategy_id: samples[strategy_id] for strategy_id in _STRATEGY_IDS},
        "summary_ns": {
            strategy_id: {
                "median_ns": median_low(samples[strategy_id]),
                "p95_ns": _nearest_rank_p95(samples[strategy_id]),
            }
            for strategy_id in _STRATEGY_IDS
        },
    }


def _selection_report_projection(case_results: list[dict[str, object]]) -> dict[str, object]:
    cases: list[dict[str, object]] = []
    for case_result in case_results:
        projected_strategies: list[dict[str, object]] = []
        for strategy in cast(list[dict[str, object]], case_result["strategies"]):
            trace = cast(dict[str, object], strategy["context_trace"])
            projected_strategies.append(
                {
                    "strategy_id": strategy["strategy_id"],
                    "selection_sha256": strategy["selection_sha256"],
                    "route": _route_from_trace(trace),
                    "context": trace["context"],
                    "module_hashes": trace["module_hashes"],
                    "budget": trace["budget"],
                    "integrity": strategy["integrity"],
                }
            )
        cases.append(
            {
                "case_id": case_result["case_id"],
                "category": case_result["category"],
                "expected": case_result["expected"],
                "strategies": projected_strategies,
            }
        )
    projection_without_digest = {"cases": cases}
    projection = dict(projection_without_digest)
    projection["selection_sha256"] = sha256_bytes(
        canonical_json_bytes(projection_without_digest)
    )
    return projection


def _decision(
    metrics: dict[str, dict[str, object]],
    timing: dict[str, object],
    repeat_count: int,
) -> tuple[str, list[str]]:
    if repeat_count < _MINIMUM_REPEAT_COUNT:
        return "inconclusive", ["repeat_count_below_minimum"]
    baseline = cast(dict[str, object], metrics["baseline-depth-1"])
    candidate = cast(dict[str, object], metrics["lexical-v1"])
    baseline_primary = cast(dict[str, int], baseline["primary_coverage"])
    candidate_primary = cast(dict[str, int], candidate["primary_coverage"])
    summary = cast(dict[str, dict[str, int]], timing["summary_ns"])
    reasons: list[str] = []
    for strategy_id, values in (
        ("baseline-depth-1", baseline),
        ("lexical-v1", candidate),
    ):
        integrity = cast(dict[str, int], values["integrity"])
        if integrity["passed"] != integrity["total"]:
            reasons.append(f"{strategy_id}_integrity_incomplete")
    for metric_name in ("negative_rejection", "ambiguity_fail_closed"):
        metric = cast(dict[str, int], candidate[metric_name])
        if metric["passed"] != metric["total"]:
            reasons.append(f"candidate_{metric_name}_incomplete")
    if candidate_primary["passed"] < baseline_primary["passed"]:
        reasons.append("candidate_primary_coverage_below_baseline")
    if cast(int, candidate["median_admitted_chars"]) > cast(
        int, baseline["median_admitted_chars"]
    ):
        reasons.append("candidate_characters_exceed_baseline")
    if summary["lexical-v1"]["p95_ns"] > (
        2 * summary["baseline-depth-1"]["p95_ns"] + 5_000_000
    ):
        reasons.append("candidate_latency_exceeds_cap")
    coverage_gain_is_material = (
        candidate_primary["passed"] * baseline_primary["total"]
        >= baseline_primary["passed"] * candidate_primary["total"]
        + 5 * baseline_primary["total"] * candidate_primary["total"] // 100
    )
    equal_coverage = (
        candidate_primary["passed"] * baseline_primary["total"]
        == baseline_primary["passed"] * candidate_primary["total"]
    )
    character_reduction_is_material = cast(
        int, candidate["median_admitted_chars"]
    ) * 4 <= cast(int, baseline["median_admitted_chars"]) * 3
    if not coverage_gain_is_material and not (
        equal_coverage and character_reduction_is_material
    ):
        reasons.append("material_benefit_not_demonstrated")
    if reasons:
        return "do-not-promote", sorted(reasons)
    return "promote", []


def run_graph_strategy_benchmark(
    export_root: Path,
    index_root: Path,
    suite_path: Path,
    max_chars: int,
    repeat_count: int,
) -> dict[str, object]:
    if isinstance(repeat_count, bool) or not isinstance(repeat_count, int) or repeat_count < 1:
        raise KnowledgeForgeError("Graph strategy repeat count must be a positive integer")
    suite = load_graph_strategy_suite(suite_path, export_root)
    index = verify_portable_lexical_index(export_root, index_root)
    case_results: list[dict[str, object]] = []
    timing_samples = {strategy_id: [] for strategy_id in _STRATEGY_IDS}
    for case in cast(list[dict[str, object]], suite["cases"]):
        case_result, case_timing = _run_graph_strategy_case(
            export_root, index_root, case, max_chars, repeat_count
        )
        case_results.append(case_result)
        for strategy_id in _STRATEGY_IDS:
            timing_samples[strategy_id].extend(case_timing[strategy_id])
    metrics = _strategy_metrics(case_results)
    selection_projection = _selection_report_projection(case_results)
    timing_projection = _timing_projection(timing_samples)
    decision, reasons = _decision(metrics, timing_projection, repeat_count)
    report_without_digest: dict[str, object] = {
        "format_version": 1,
        "kind": "portable-graph-strategy-benchmark",
        "export_sha256": index["export_sha256"],
        "index_sha256": index["index_sha256"],
        "suite_sha256": suite["suite_sha256"],
        "max_chars": max_chars,
        "repeat_count": repeat_count,
        "minimum_repeat_count": _MINIMUM_REPEAT_COUNT,
        "cases": case_results,
        "metrics": metrics,
        "selection_projection": selection_projection,
        "timing_projection": timing_projection,
        "decision": decision,
        "decision_reasons": reasons,
    }
    report = dict(report_without_digest)
    report["benchmark_sha256"] = sha256_bytes(
        canonical_json_bytes(report_without_digest)
    )
    validate_graph_strategy_benchmark(report)
    return report


def validate_graph_strategy_benchmark(report: dict[str, object]) -> None:
    if not isinstance(report, dict):
        raise KnowledgeForgeError("Graph strategy benchmark report must be an object")
    validate_record(_REPORT_SCHEMA_PATH, report, "graph strategy benchmark")
    claimed_digest = _require_digest(report.get("benchmark_sha256"), "report digest")
    without_digest = {
        key: value for key, value in report.items() if key != "benchmark_sha256"
    }
    if sha256_bytes(canonical_json_bytes(without_digest)) != claimed_digest:
        raise KnowledgeForgeError("Graph strategy benchmark report digest mismatch")


def _assert_safe_report_path(report_path: Path) -> None:
    if report_path.is_symlink():
        raise KnowledgeForgeError(
            f"Graph strategy benchmark output must not be a symbolic link: {report_path.name}"
        )
    for parent in report_path.parents:
        if parent == parent.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise KnowledgeForgeError(
                "Graph strategy benchmark output parent must not be a symbolic link: "
                f"{parent.name}"
            )


def write_graph_strategy_benchmark(
    report_path: Path, report: dict[str, object]
) -> None:
    validate_graph_strategy_benchmark(report)
    _assert_safe_report_path(report_path)
    if report_path.exists():
        raise KnowledgeForgeError(
            f"Graph strategy benchmark output already exists: {report_path.name}"
        )
    write_json_atomic(report_path, report)


def load_graph_strategy_benchmark(report_path: Path) -> dict[str, object]:
    require_regular_file(report_path, "Graph strategy benchmark report")
    payload = read_json(report_path)
    if not isinstance(payload, dict):
        raise KnowledgeForgeError("Graph strategy benchmark report root must be an object")
    report = cast(dict[str, object], payload)
    validate_graph_strategy_benchmark(report)
    return report
