from collections import Counter
from pathlib import Path
from typing import cast

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.graph import build_graph
from knowledge_forge.hashing import sha256_bytes
from knowledge_forge.indexes import build_indexes, load_areas
from knowledge_forge.io import (
    canonical_json_bytes,
    read_json,
    read_jsonl,
    write_json_atomic,
)
from knowledge_forge.package import discover_modules, validate_package

_MATURITY_VALUES = ("candidate", "reviewed", "validated", "deprecated")
_STRUCTURAL_REASONS = {"navigation", "preamble", "reflection", "summary"}
_EXCLUDED_REASONS = {"case-study", "implementation-detail", "non-operational-context"}


def _count_values(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def inspect_package(pack_root: Path, schema_root: Path) -> dict[str, object]:
    manifest = validate_package(pack_root, schema_root, [])
    modules = discover_modules(
        pack_root, schema_root / "knowledge-module.schema.json"
    )
    areas = load_areas(pack_root / "indexes" / "areas.json")
    indexes = build_indexes(modules, areas)
    graph = build_graph(modules)
    maturity_counts = _count_values(
        [module["metadata"]["maturity"] for module in modules]
    )
    for value in _MATURITY_VALUES:
        maturity_counts.setdefault(value, 0)
    return {
        "format_version": 1,
        "package_sha256": manifest["package_sha256"],
        "module_count": len(modules),
        "area_count": len(areas),
        "relation_count": len(graph["edges"]),
        "language_counts": _count_values(
            [module["metadata"]["language"] for module in modules]
        ),
        "maturity_counts": dict(sorted(maturity_counts.items())),
        "kind_counts": _count_values(
            [module["metadata"]["kind"] for module in modules]
        ),
        "area_module_counts": {
            area["id"]: len(area["module_ids"])
            for area in sorted(areas, key=lambda item: item["id"])
        },
        "index_bytes": {
            "l0": len(canonical_json_bytes(indexes["l0"])),
            "l1": {
                area_id: len(canonical_json_bytes(index))
                for area_id, index in sorted(indexes["l1"].items())
            },
        },
    }


def _known_unit_ids(units_path: Path) -> set[str]:
    records = read_jsonl(units_path)
    identifiers: list[str] = []
    for record in records:
        unit_id = record.get("unit_id")
        if not isinstance(unit_id, str) or not unit_id:
            raise KnowledgeForgeError("Normalized unit is missing a valid unit_id")
        identifiers.append(unit_id)
    if len(identifiers) != len(set(identifiers)):
        raise KnowledgeForgeError("Normalized units contain duplicate unit_id")
    if not identifiers:
        raise KnowledgeForgeError("Normalized units must not be empty")
    return set(identifiers)


def _review_files(reviews_root: Path) -> list[Path]:
    if reviews_root.is_symlink() or not reviews_root.is_dir():
        raise KnowledgeForgeError("Promotion review root must be a directory")
    files = sorted(reviews_root.glob("*.json"), key=lambda path: path.name)
    if not files:
        raise KnowledgeForgeError("Promotion review root has no JSON files")
    if any(path.is_symlink() or not path.is_file() for path in files):
        raise KnowledgeForgeError("Promotion review files must be regular files")
    return files


def _review_entries(review_path: Path) -> list[dict[str, object]]:
    payload = read_json(review_path)
    if not isinstance(payload, dict) or payload.get("format_version") != 1:
        raise KnowledgeForgeError(
            f"Promotion review has invalid format: {review_path.name}"
        )
    entries = payload.get("promotion_review")
    if not isinstance(entries, list):
        raise KnowledgeForgeError(
            f"Promotion review must contain an array: {review_path.name}"
        )
    return cast(list[dict[str, object]], entries)


def _validated_links(
    review_paths: list[Path], known_units: set[str]
) -> list[dict[str, object]]:
    links: list[dict[str, object]] = []
    for review_path in review_paths:
        for entry in _review_entries(review_path):
            if not isinstance(entry, dict) or set(entry) != {
                "module_id",
                "unit_ids",
                "review_state",
            }:
                raise KnowledgeForgeError(
                    f"Promotion review entry has invalid shape: {review_path.name}"
                )
            module_id = entry["module_id"]
            unit_ids = entry["unit_ids"]
            review_state = entry["review_state"]
            if not isinstance(module_id, str) or not module_id:
                raise KnowledgeForgeError("Promotion review has invalid module_id")
            if (
                not isinstance(unit_ids, list)
                or not unit_ids
                or not all(isinstance(unit_id, str) and unit_id for unit_id in unit_ids)
            ):
                raise KnowledgeForgeError(
                    f"Promotion review has invalid unit_ids: {module_id}"
                )
            if review_state != "reviewed":
                raise KnowledgeForgeError(
                    f"Promotion coverage contains unreviewed module: {module_id}"
                )
            unknown = sorted(set(cast(list[str], unit_ids)) - known_units)
            if unknown:
                raise KnowledgeForgeError(
                    f"Promotion coverage has unknown unit endpoint: {module_id}"
                )
            links.append(
                {
                    "module_id": module_id,
                    "unit_ids": sorted(set(cast(list[str], unit_ids))),
                }
            )
    return sorted(links, key=lambda item: cast(str, item["module_id"]))


def _require_exact_module_coverage(
    public_ids: set[str], links: list[dict[str, object]]
) -> None:
    mapped_ids = [cast(str, link["module_id"]) for link in links]
    duplicates = sorted(
        module_id
        for module_id, count in Counter(mapped_ids).items()
        if count > 1
    )
    if duplicates:
        raise KnowledgeForgeError(
            f"Promotion coverage contains duplicate module: {duplicates[0]}"
        )
    missing = sorted(public_ids - set(mapped_ids))
    if missing:
        raise KnowledgeForgeError(
            f"Promotion coverage is missing module: {missing[0]}"
        )
    extra = sorted(set(mapped_ids) - public_ids)
    if extra:
        raise KnowledgeForgeError(
            f"Promotion coverage contains unknown module: {extra[0]}"
        )


def verify_promotion_coverage(
    pack_root: Path,
    schema_root: Path,
    units_path: Path,
    reviews_root: Path,
    report_path: Path,
) -> dict[str, object]:
    modules = discover_modules(
        pack_root, schema_root / "knowledge-module.schema.json"
    )
    public_ids = {module["metadata"]["id"] for module in modules}
    known_units = _known_unit_ids(units_path)
    review_paths = _review_files(reviews_root)
    links = _validated_links(review_paths, known_units)
    _require_exact_module_coverage(public_ids, links)
    linked_units = {
        unit_id for link in links for unit_id in cast(list[str], link["unit_ids"])
    }
    report = {
        "format_version": 1,
        "module_count": len(public_ids),
        "review_file_count": len(review_paths),
        "unique_unit_count": len(linked_units),
        "link_count": sum(
            len(cast(list[str], link["unit_ids"])) for link in links
        ),
        "coverage_sha256": sha256_bytes(canonical_json_bytes(links)),
    }
    write_json_atomic(report_path, report)
    return report


def _validated_dispositions(
    dispositions_path: Path, public_ids: set[str], known_units: set[str]
) -> list[dict[str, object]]:
    payload = read_json(dispositions_path)
    if not isinstance(payload, dict) or payload.get("format_version") != 1:
        raise KnowledgeForgeError("Unit disposition has invalid format")
    entries = payload.get("unit_disposition")
    if not isinstance(entries, list):
        raise KnowledgeForgeError("Unit disposition must contain an array")
    validated: list[dict[str, object]] = []
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {
            "unit_id",
            "state",
            "reason",
            "module_ids",
        }:
            raise KnowledgeForgeError("Unit disposition entry has invalid shape")
        unit_id = entry["unit_id"]
        state = entry["state"]
        reason = entry["reason"]
        module_ids = entry["module_ids"]
        if not isinstance(unit_id, str) or not unit_id:
            raise KnowledgeForgeError("Unit disposition has invalid unit_id")
        if unit_id not in known_units:
            raise KnowledgeForgeError(f"Unit disposition has unknown unit: {unit_id}")
        if not isinstance(module_ids, list) or not all(
            isinstance(module_id, str) and module_id for module_id in module_ids
        ):
            raise KnowledgeForgeError(
                f"Unit disposition has invalid module_ids: {unit_id}"
            )
        typed_module_ids = cast(list[str], module_ids)
        if len(typed_module_ids) != len(set(typed_module_ids)):
            raise KnowledgeForgeError(
                f"Unit disposition contains duplicate module: {unit_id}"
            )
        unknown_modules = sorted(set(typed_module_ids) - public_ids)
        if unknown_modules:
            raise KnowledgeForgeError(
                f"Unit disposition has unknown module: {unknown_modules[0]}"
            )
        if state == "corroborating":
            if reason != "corroborates-existing-module" or not typed_module_ids:
                raise KnowledgeForgeError(
                    f"Unit disposition has invalid corroborating entry: {unit_id}"
                )
        elif state == "structural":
            if reason not in _STRUCTURAL_REASONS or typed_module_ids:
                raise KnowledgeForgeError(
                    f"Unit disposition has invalid structural entry: {unit_id}"
                )
        elif state == "excluded":
            if reason not in _EXCLUDED_REASONS or typed_module_ids:
                raise KnowledgeForgeError(
                    f"Unit disposition has invalid excluded entry: {unit_id}"
                )
        else:
            raise KnowledgeForgeError(
                f"Unit disposition has invalid state: {unit_id}"
            )
        validated.append(
            {
                "unit_id": unit_id,
                "state": state,
                "reason": reason,
                "module_ids": sorted(typed_module_ids),
            }
        )
    identifiers = [cast(str, entry["unit_id"]) for entry in validated]
    duplicates = sorted(
        unit_id for unit_id, count in Counter(identifiers).items() if count > 1
    )
    if duplicates:
        raise KnowledgeForgeError(
            f"Unit disposition contains duplicate unit: {duplicates[0]}"
        )
    return sorted(validated, key=lambda item: cast(str, item["unit_id"]))


def verify_unit_disposition(
    pack_root: Path,
    schema_root: Path,
    units_path: Path,
    reviews_root: Path,
    dispositions_path: Path,
    report_path: Path,
) -> dict[str, object]:
    modules = discover_modules(
        pack_root, schema_root / "knowledge-module.schema.json"
    )
    public_ids = {module["metadata"]["id"] for module in modules}
    known_units = _known_unit_ids(units_path)
    links = _validated_links(_review_files(reviews_root), known_units)
    _require_exact_module_coverage(public_ids, links)
    promoted_units = {
        unit_id for link in links for unit_id in cast(list[str], link["unit_ids"])
    }
    dispositions = _validated_dispositions(
        dispositions_path, public_ids, known_units
    )
    disposition_units = {
        cast(str, disposition["unit_id"]) for disposition in dispositions
    }
    overlap = sorted(promoted_units & disposition_units)
    if overlap:
        raise KnowledgeForgeError(
            f"Unit disposition overlaps promoted unit: {overlap[0]}"
        )
    missing = sorted(known_units - promoted_units - disposition_units)
    if missing:
        raise KnowledgeForgeError(f"Unit disposition is missing unit: {missing[0]}")
    coverage_records = [
        {"unit_id": unit_id, "state": "promoted"}
        for unit_id in sorted(promoted_units)
    ] + dispositions
    report = {
        "format_version": 1,
        "unit_count": len(known_units),
        "promoted_unit_count": len(promoted_units),
        "disposition_count": len(dispositions),
        "state_counts": _count_values(
            [cast(str, disposition["state"]) for disposition in dispositions]
        ),
        "reason_counts": _count_values(
            [cast(str, disposition["reason"]) for disposition in dispositions]
        ),
        "unit_coverage_sha256": sha256_bytes(
            canonical_json_bytes(coverage_records)
        ),
    }
    write_json_atomic(report_path, report)
    return report
