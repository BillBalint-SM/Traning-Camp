from pathlib import Path
from typing import cast

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import (
    canonical_json_bytes,
    read_jsonl,
    write_jsonl_atomic,
)
from knowledge_forge.portability import verify_portable_export

_SCHEMA_PATH = Path(__file__).parents[2] / "schemas" / "context-trace.schema.json"


def _require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise KnowledgeForgeError(f"Context trace {label} must be a non-empty string")
    return value


def _require_sha256(value: object, label: str) -> str:
    digest = _require_string(value, label)
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise KnowledgeForgeError(f"Context trace {label} must be a lowercase SHA-256 digest")
    return digest


def _require_identifier_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise KnowledgeForgeError(f"Context trace {label} must be a string array")
    items = cast(list[str], value)
    if len(items) != len(set(items)):
        raise KnowledgeForgeError(f"Context trace {label} contains duplicates")
    return items


def _require_integer(value: object, label: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise KnowledgeForgeError(f"Context trace {label} must be an integer >= {minimum}")
    return value


def _route_projection(context: dict[str, object]) -> dict[str, object]:
    status = context.get("status")
    if status not in {"covered", "ambiguous", "not-covered"}:
        raise KnowledgeForgeError("Context trace route status is invalid")
    area_id = context.get("area_id")
    if area_id is not None:
        _require_string(area_id, "route area_id")
    primary = _require_identifier_list(context.get("module_ids", []), "route module_ids")
    alternatives = _require_identifier_list(
        context.get("alternatives", []), "route alternatives"
    )
    if status == "covered" and (area_id is None or not primary):
        raise KnowledgeForgeError("Context trace covered route requires area and primary module")
    if status != "covered" and (area_id is not None or primary):
        raise KnowledgeForgeError("Context trace uncovered route cannot admit primary modules")
    return {
        "status": status,
        "area_id": area_id,
        "primary_module_ids": sorted(primary),
        "alternative_area_ids": sorted(alternatives),
    }


def _module_projection(
    context: dict[str, object],
) -> tuple[dict[str, str], list[str], list[str], int]:
    modules_value = context.get("modules", [])
    if not isinstance(modules_value, list):
        raise KnowledgeForgeError("Context trace context modules must be an array")
    hashes: dict[str, str] = {}
    admitted: list[str] = []
    for module_value in modules_value:
        if not isinstance(module_value, dict):
            raise KnowledgeForgeError("Context trace module receipt must be an object")
        module_id = _require_string(module_value.get("id"), "module id")
        if module_id in hashes:
            raise KnowledgeForgeError(f"Context trace module receipt is duplicated: {module_id}")
        text = module_value.get("text")
        if not isinstance(text, str):
            raise KnowledgeForgeError(f"Context trace module text is invalid: {module_id}")
        declared_hash = _require_sha256(module_value.get("content_sha256"), "module content hash")
        actual_hash = sha256_bytes(text.encode("utf-8"))
        if actual_hash != declared_hash:
            raise KnowledgeForgeError(f"Context trace module content hash mismatch: {module_id}")
        hashes[module_id] = declared_hash
        admitted.append(module_id)
    expanded_value = context.get("expanded_module_ids", admitted)
    expanded = sorted(_require_identifier_list(expanded_value, "expanded module IDs"))
    admitted = sorted(admitted)
    if not set(admitted).issubset(expanded):
        raise KnowledgeForgeError("Context trace admitted modules must be expanded modules")
    relations_value = context.get("relations", [])
    if not isinstance(relations_value, list):
        raise KnowledgeForgeError("Context trace relations must be an array")
    relation_count = len(relations_value)
    return hashes, expanded, admitted, relation_count


def _budget_projection(
    context: dict[str, object], admitted: list[str], module_lengths: dict[str, int]
) -> dict[str, object]:
    budget_value = context.get("budget")
    if budget_value is None:
        return {
            "format_version": 1,
            "max_chars": None,
            "used_chars": sum(module_lengths.values()),
            "omitted_module_ids": [],
        }
    if not isinstance(budget_value, dict):
        raise KnowledgeForgeError("Context trace budget must be an object")
    if budget_value.get("format_version") != 1:
        raise KnowledgeForgeError("Context trace budget format version is incompatible")
    max_chars = budget_value.get("max_chars")
    if max_chars is not None:
        _require_integer(max_chars, "budget max_chars", 1)
    used_chars = _require_integer(budget_value.get("used_chars"), "budget used_chars", 0)
    omitted = sorted(
        _require_identifier_list(budget_value.get("omitted_module_ids"), "budget omitted modules")
    )
    if max_chars is not None and used_chars > max_chars:
        raise KnowledgeForgeError("Context trace budget used_chars exceeds max_chars")
    if set(omitted) & set(admitted):
        raise KnowledgeForgeError("Context trace budget omits an admitted module")
    return {
        "format_version": 1,
        "max_chars": max_chars,
        "used_chars": used_chars,
        "omitted_module_ids": omitted,
    }


def _timing_projection(timing_ms: dict[str, int]) -> dict[str, int]:
    if set(timing_ms) != {"route", "load", "total"}:
        raise KnowledgeForgeError("Context trace timing must contain route, load, and total")
    timing = {
        key: _require_integer(timing_ms.get(key), f"timing {key}", 0)
        for key in ("route", "load", "total")
    }
    if timing["total"] < timing["route"] or timing["total"] < timing["load"]:
        raise KnowledgeForgeError("Context trace total timing is smaller than a phase")
    return timing


def build_context_trace(
    query: str,
    context: dict[str, object],
    relation_depth: int,
    timing_ms: dict[str, int],
) -> dict[str, object]:
    if not isinstance(query, str) or not query:
        raise KnowledgeForgeError("Context trace query must be a non-empty string")
    if not isinstance(context, dict):
        raise KnowledgeForgeError("Context trace context must be an object")
    if context.get("format_version") != 1:
        raise KnowledgeForgeError("Context trace context format version is incompatible")
    if isinstance(relation_depth, bool) or relation_depth not in {0, 1}:
        raise KnowledgeForgeError("Context trace relation depth must be 0 or 1")
    export_sha256 = _require_sha256(context.get("export_sha256"), "export_sha256")
    route = _route_projection(context)
    hashes, expanded, admitted, relation_count = _module_projection(context)
    primary = cast(list[str], route["primary_module_ids"])
    if not set(primary).issubset(admitted):
        raise KnowledgeForgeError("Context trace primary modules must be admitted")
    omitted_source = context.get("budget", {})
    omitted_ids = []
    if isinstance(omitted_source, dict):
        omitted_ids = _require_identifier_list(
            omitted_source.get("omitted_module_ids", []), "budget omitted modules"
        )
    if set(omitted_ids) & set(expanded):
        raise KnowledgeForgeError("Context trace omitted modules must not be expanded")
    module_lengths = {
        _require_string(module.get("id"), "module id"): len(cast(str, module.get("text")))
        for module in cast(list[dict[str, object]], context.get("modules", []))
    }
    budget = _budget_projection(context, admitted, module_lengths)
    trace_without_digest: dict[str, object] = {
        "format_version": 1,
        "kind": "portable-context-trace",
        "query_sha256": sha256_bytes(query.encode("utf-8")),
        "export_sha256": export_sha256,
        "route": route,
        "context": {
            "relation_depth": relation_depth,
            "expanded_module_ids": expanded,
            "admitted_module_ids": admitted,
            "omitted_module_ids": sorted(cast(list[str], budget["omitted_module_ids"])),
            "relation_count": relation_count,
        },
        "module_hashes": dict(sorted(hashes.items())),
        "budget": budget,
        "timing_ms": _timing_projection(timing_ms),
    }
    trace = dict(trace_without_digest)
    trace["trace_sha256"] = sha256_bytes(canonical_json_bytes(trace_without_digest))
    validate_context_trace(trace)
    return trace


def _semantic_validate(record: dict[str, object]) -> None:
    route = cast(dict[str, object], record["route"])
    context = cast(dict[str, object], record["context"])
    hashes = cast(dict[str, str], record["module_hashes"])
    status = route["status"]
    primary = set(cast(list[str], route["primary_module_ids"]))
    expanded = set(cast(list[str], context["expanded_module_ids"]))
    admitted = set(cast(list[str], context["admitted_module_ids"]))
    omitted = set(cast(list[str], context["omitted_module_ids"]))
    if status == "covered" and not primary:
        raise KnowledgeForgeError("Context trace covered route has no primary module")
    if status != "covered" and (primary or expanded or admitted):
        raise KnowledgeForgeError("Context trace uncovered route contains admitted context")
    if not primary.issubset(admitted) or not admitted.issubset(expanded):
        raise KnowledgeForgeError("Context trace module containment invariant failed")
    if omitted & expanded or omitted & admitted:
        raise KnowledgeForgeError("Context trace omitted module invariant failed")
    if set(hashes) != admitted:
        raise KnowledgeForgeError("Context trace module hash set does not match admitted modules")
    budget = cast(dict[str, object], record["budget"])
    max_chars = budget["max_chars"]
    used_chars = cast(int, budget["used_chars"])
    if max_chars is not None and used_chars > cast(int, max_chars):
        raise KnowledgeForgeError("Context trace budget used_chars exceeds max_chars")
    timing = cast(dict[str, int], record["timing_ms"])
    if timing["total"] < timing["route"] or timing["total"] < timing["load"]:
        raise KnowledgeForgeError("Context trace total timing is smaller than a phase")
    without_digest = {key: value for key, value in record.items() if key != "trace_sha256"}
    if sha256_bytes(canonical_json_bytes(without_digest)) != record["trace_sha256"]:
        raise KnowledgeForgeError("Context trace digest mismatch")


def validate_context_trace(record: dict[str, object]) -> None:
    if not isinstance(record, dict):
        raise KnowledgeForgeError("Context trace record must be an object")
    validate_record(_SCHEMA_PATH, record, "context trace")
    _semantic_validate(record)


def _assert_safe_trace_path(trace_path: Path) -> None:
    if trace_path.is_symlink():
        raise KnowledgeForgeError(f"Context trace output must not be a symbolic link: {trace_path.name}")
    for parent in trace_path.parents:
        if parent == parent.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise KnowledgeForgeError(
                f"Context trace output parent must not be a symbolic link: {parent.name}"
            )


def write_context_traces(trace_path: Path, records: list[dict[str, object]]) -> None:
    if not records:
        raise KnowledgeForgeError("Context trace output requires at least one record")
    for record in records:
        validate_context_trace(record)
    _assert_safe_trace_path(trace_path)
    write_jsonl_atomic(trace_path, records)


def verify_context_traces(trace_path: Path, export_root: Path) -> list[dict[str, object]]:
    _assert_safe_trace_path(trace_path)
    records = read_jsonl(trace_path)
    if not records:
        raise KnowledgeForgeError("Context trace artifact requires at least one record")
    for record in records:
        validate_context_trace(record)
    manifest = verify_portable_export(export_root)
    export_sha256 = _require_sha256(manifest.get("export_sha256"), "manifest export_sha256")
    module_nodes = read_jsonl(export_root / "graph" / "nodes.jsonl")
    module_hashes = {
        _require_string(node.get("id"), "export module id"): _require_sha256(
            node.get("content_sha256"), "export module hash"
        )
        for node in module_nodes
    }
    for record in records:
        if record["export_sha256"] != export_sha256:
            raise KnowledgeForgeError("Context trace export digest does not match export")
        trace_hashes = cast(dict[str, str], record["module_hashes"])
        for module_id, expected_hash in trace_hashes.items():
            if module_id not in module_hashes:
                raise KnowledgeForgeError(f"Context trace references unknown module: {module_id}")
            if module_hashes[module_id] != expected_hash:
                raise KnowledgeForgeError(f"Context trace module hash mismatch: {module_id}")
    return records
