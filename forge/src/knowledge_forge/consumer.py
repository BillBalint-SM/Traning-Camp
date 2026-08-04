import re
from pathlib import Path
from typing import cast

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.io import write_json_atomic
from knowledge_forge.portability import (
    load_portable_context_budgeted,
    load_portable_context_graph,
    verify_portable_export,
)

_IDENTIFIER_PATTERN = re.compile(r"^[a-z][a-z0-9.-]*$")


def _require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise KnowledgeForgeError(f"Consumer result {label} must be a non-empty string")
    return value


def _require_digest(value: object, label: str) -> str:
    digest = _require_string(value, label)
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise KnowledgeForgeError(f"Consumer result {label} must be a lowercase SHA-256 digest")
    return digest


def _require_identifier(value: object, label: str) -> str:
    identifier = _require_string(value, label)
    if not _IDENTIFIER_PATTERN.fullmatch(identifier):
        raise KnowledgeForgeError(f"Consumer result {label} is not a valid identifier")
    return identifier


def _require_identifier_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list):
        raise KnowledgeForgeError(f"Consumer result {label} must be an array")
    identifiers = [_require_identifier(item, label) for item in value]
    if identifiers != sorted(identifiers):
        raise KnowledgeForgeError(f"Consumer result {label} must be sorted")
    if len(identifiers) != len(set(identifiers)):
        raise KnowledgeForgeError(f"Consumer result {label} contains duplicates")
    return identifiers


def _require_nonnegative_integer(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise KnowledgeForgeError(f"Consumer result {label} must be a non-negative integer")
    return value


def _assert_safe_output_path(output_path: Path) -> None:
    if output_path.is_symlink():
        raise KnowledgeForgeError(
            f"Consumer result output must not be a symbolic link: {output_path.name}"
        )
    for parent in output_path.parents:
        if parent == parent.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise KnowledgeForgeError(
                f"Consumer result output parent must not be a symbolic link: {parent.name}"
            )


def _context_modules(context: dict[str, object]) -> tuple[list[str], dict[str, str]]:
    modules_value = context.get("modules")
    if not isinstance(modules_value, list):
        raise KnowledgeForgeError("Consumer result context modules must be an array")
    admitted: list[str] = []
    hashes: dict[str, str] = {}
    for module_value in modules_value:
        if not isinstance(module_value, dict):
            raise KnowledgeForgeError("Consumer result module must be an object")
        module_id = _require_identifier(module_value.get("id"), "module id")
        if module_id in hashes:
            raise KnowledgeForgeError(f"Consumer result module is duplicated: {module_id}")
        text = module_value.get("text")
        if not isinstance(text, str):
            raise KnowledgeForgeError(f"Consumer result module text is invalid: {module_id}")
        declared_hash = _require_digest(module_value.get("content_sha256"), "module content hash")
        actual_hash = sha256_bytes(text.encode("utf-8"))
        if actual_hash != declared_hash:
            raise KnowledgeForgeError(f"Consumer result module hash mismatch: {module_id}")
        admitted.append(module_id)
        hashes[module_id] = declared_hash
    if admitted != sorted(admitted):
        raise KnowledgeForgeError("Consumer result context modules must be sorted")
    return admitted, hashes


def _build_receipt(
    context: dict[str, object],
    export_sha256: str,
    relation_depth: int,
) -> dict[str, object]:
    admitted, module_hashes = _context_modules(context)
    budget_value = context.get("budget")
    omitted: list[str] = []
    if budget_value is not None:
        if not isinstance(budget_value, dict):
            raise KnowledgeForgeError("Consumer result context budget must be an object")
        omitted = _require_identifier_list(
            budget_value.get("omitted_module_ids"),
            "budget omitted module IDs",
        )
    return {
        "format_version": 1,
        "export_sha256": export_sha256,
        "relation_depth": relation_depth,
        "admitted_module_ids": admitted,
        "omitted_module_ids": omitted,
        "module_hashes": dict(sorted(module_hashes.items())),
    }


def consume_portable_export(
    export_root: Path,
    query: str,
    relation_depth: int,
    max_chars: int | None,
) -> dict[str, object]:
    if export_root.is_symlink() or not export_root.is_dir():
        raise KnowledgeForgeError("Consumer export input must be an existing directory")
    if not isinstance(query, str) or not query:
        raise KnowledgeForgeError("Consumer query must be a non-empty string")
    if isinstance(relation_depth, bool) or relation_depth not in {0, 1}:
        raise KnowledgeForgeError("Consumer relation depth must be 0 or 1")
    if max_chars is not None and (
        isinstance(max_chars, bool)
        or not isinstance(max_chars, int)
        or max_chars <= 0
        or max_chars > 100_000
    ):
        raise KnowledgeForgeError("Consumer character budget must be between 1 and 100000")

    manifest = verify_portable_export(export_root)
    export_sha256 = _require_digest(manifest.get("export_sha256"), "export_sha256")
    if max_chars is None:
        context = load_portable_context_graph(export_root, query, relation_depth)
    else:
        context = load_portable_context_budgeted(
            export_root,
            query,
            relation_depth,
            max_chars,
        )
    if context.get("alternatives") is None:
        context["alternatives"] = []
    context["relation_depth"] = relation_depth
    receipt = _build_receipt(context, export_sha256, relation_depth)
    result: dict[str, object] = {
        "format_version": 1,
        "kind": "portable-consumer-result",
        "export_sha256": export_sha256,
        "context": context,
        "receipt": receipt,
    }
    validate_consumer_result(result)
    return result


def validate_consumer_result(result: dict[str, object]) -> None:
    if not isinstance(result, dict):
        raise KnowledgeForgeError("Consumer result must be an object")
    if set(result) != {"format_version", "kind", "export_sha256", "context", "receipt"}:
        raise KnowledgeForgeError("Consumer result has an invalid field set")
    if result["format_version"] != 1 or result["kind"] != "portable-consumer-result":
        raise KnowledgeForgeError("Consumer result format is incompatible")
    export_sha256 = _require_digest(result["export_sha256"], "export_sha256")
    context_value = result["context"]
    receipt_value = result["receipt"]
    if not isinstance(context_value, dict) or not isinstance(receipt_value, dict):
        raise KnowledgeForgeError("Consumer result context and receipt must be objects")
    context = cast(dict[str, object], context_value)
    receipt = cast(dict[str, object], receipt_value)

    if context.get("format_version") != 1:
        raise KnowledgeForgeError("Consumer context format is incompatible")
    if context.get("export_sha256") != export_sha256:
        raise KnowledgeForgeError("Consumer context export digest does not match result")
    status = context.get("status")
    if status not in {"covered", "ambiguous", "not-covered"}:
        raise KnowledgeForgeError("Consumer context status is invalid")
    area_id = context.get("area_id")
    if area_id is not None:
        _require_identifier(area_id, "context area_id")
    primary_ids = _require_identifier_list(context.get("module_ids"), "context module IDs")
    _require_identifier_list(
        context.get("alternatives"), "context alternatives"
    )
    relation_depth = context.get("relation_depth")
    if isinstance(relation_depth, bool) or relation_depth not in {0, 1}:
        raise KnowledgeForgeError("Consumer context relation depth is invalid")
    expanded = _require_identifier_list(
        context.get("expanded_module_ids"),
        "context expanded module IDs",
    )
    admitted, module_hashes = _context_modules(context)
    admitted_set = set(admitted)
    omitted: list[str] = []
    budget_value = context.get("budget")
    if budget_value is not None:
        if not isinstance(budget_value, dict):
            raise KnowledgeForgeError("Consumer context budget must be an object")
        if budget_value.get("format_version") != 1:
            raise KnowledgeForgeError("Consumer context budget format is incompatible")
        max_chars = budget_value.get("max_chars")
        if max_chars is not None:
            _require_nonnegative_integer(max_chars, "context budget max_chars")
            if max_chars == 0:
                raise KnowledgeForgeError("Consumer context budget max_chars must be positive")
        used_chars = _require_nonnegative_integer(
            budget_value.get("used_chars"),
            "context budget used_chars",
        )
        if max_chars is not None and used_chars > max_chars:
            raise KnowledgeForgeError("Consumer context budget exceeds max_chars")
        omitted = _require_identifier_list(
            budget_value.get("omitted_module_ids"),
            "context budget omitted module IDs",
        )
    relations = context.get("relations")
    if not isinstance(relations, list):
        raise KnowledgeForgeError("Consumer context relations must be an array")
    if status == "covered":
        if area_id is None or not primary_ids:
            raise KnowledgeForgeError("Covered consumer context requires area and primary modules")
    elif area_id is not None or primary_ids or expanded or admitted:
        raise KnowledgeForgeError("Uncovered consumer context contains admitted modules")
    if not set(primary_ids).issubset(admitted_set):
        raise KnowledgeForgeError("Consumer primary modules are not admitted")
    if not admitted_set.issubset(set(expanded)):
        raise KnowledgeForgeError("Consumer admitted modules are not expanded")
    if set(omitted) & set(expanded):
        raise KnowledgeForgeError("Consumer omitted modules overlap expanded modules")

    if set(receipt) != {
        "format_version",
        "export_sha256",
        "relation_depth",
        "admitted_module_ids",
        "omitted_module_ids",
        "module_hashes",
    }:
        raise KnowledgeForgeError("Consumer receipt has an invalid field set")
    if receipt["format_version"] != 1:
        raise KnowledgeForgeError("Consumer receipt format is incompatible")
    if receipt["export_sha256"] != export_sha256:
        raise KnowledgeForgeError("Consumer receipt export digest does not match result")
    if receipt["relation_depth"] != relation_depth:
        raise KnowledgeForgeError("Consumer receipt relation depth does not match context")
    receipt_admitted = _require_identifier_list(
        receipt["admitted_module_ids"],
        "receipt admitted module IDs",
    )
    receipt_omitted = _require_identifier_list(
        receipt["omitted_module_ids"],
        "receipt omitted module IDs",
    )
    receipt_hashes_value = receipt["module_hashes"]
    if not isinstance(receipt_hashes_value, dict):
        raise KnowledgeForgeError("Consumer receipt module hashes must be an object")
    receipt_hashes = {
        _require_identifier(module_id, "receipt module ID"): _require_digest(
            digest,
            "receipt module hash",
        )
        for module_id, digest in receipt_hashes_value.items()
    }
    if receipt_admitted != admitted or receipt_omitted != omitted:
        raise KnowledgeForgeError("Consumer receipt module sets do not match context")
    if receipt_hashes != module_hashes:
        raise KnowledgeForgeError("Consumer receipt module hash set does not match context")


def write_consumer_result(output_path: Path, result: dict[str, object]) -> None:
    validate_consumer_result(result)
    _assert_safe_output_path(output_path)
    if output_path.exists():
        raise KnowledgeForgeError(
            f"Consumer result output already exists: {output_path.name}"
        )
    write_json_atomic(output_path, result)
