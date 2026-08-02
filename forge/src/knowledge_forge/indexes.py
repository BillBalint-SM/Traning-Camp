from pathlib import Path
from typing import cast

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.io import read_json, write_json_atomic
from knowledge_forge.models import KnowledgeModule


def _strings(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not value or not all(
        isinstance(item, str) and item for item in value
    ):
        raise KnowledgeForgeError(f"Area field must be a non-empty string list: {label}")
    return cast(list[str], value)


def load_areas(areas_path: Path) -> list[dict[str, object]]:
    payload = read_json(areas_path)
    if not isinstance(payload, dict):
        raise KnowledgeForgeError("Area declaration root must be an object")
    raw_areas = payload.get("areas")
    if not isinstance(raw_areas, list) or not raw_areas:
        raise KnowledgeForgeError("Area declaration must contain a non-empty areas list")
    areas: list[dict[str, object]] = []
    identifiers: set[str] = set()
    for raw_area in raw_areas:
        if not isinstance(raw_area, dict):
            raise KnowledgeForgeError("Area declaration must contain only objects")
        required = {
            "id",
            "title",
            "aliases",
            "summary",
            "decision_boundary",
            "module_ids",
        }
        if set(raw_area) != required:
            raise KnowledgeForgeError("Area declaration has invalid fields")
        identifier = raw_area["id"]
        title = raw_area["title"]
        summary = raw_area["summary"]
        boundary = raw_area["decision_boundary"]
        if not all(
            isinstance(value, str) and value
            for value in (identifier, title, summary, boundary)
        ):
            raise KnowledgeForgeError("Area declaration text fields must be non-empty")
        if identifier in identifiers:
            raise KnowledgeForgeError(f"Duplicate area ID: {identifier}")
        identifiers.add(identifier)
        areas.append(
            {
                "id": identifier,
                "title": title,
                "aliases": _strings(raw_area["aliases"], str(identifier)),
                "summary": summary,
                "decision_boundary": boundary,
                "module_ids": _strings(raw_area["module_ids"], str(identifier)),
            }
        )
    return sorted(areas, key=lambda area: str(area["id"]))


def _module_descriptor(module: KnowledgeModule) -> dict[str, object]:
    metadata = module["metadata"]
    return {
        "id": metadata["id"],
        "title": metadata["title"],
        "maturity": metadata["maturity"],
        "tags": sorted(metadata["tags"]),
        "aliases": sorted(metadata["aliases"]),
    }


def _validate_area_assignments(
    areas: list[dict[str, object]], modules: list[KnowledgeModule]
) -> dict[str, KnowledgeModule]:
    by_id = {module["metadata"]["id"]: module for module in modules}
    assigned: set[str] = set()
    for area in areas:
        for module_id in cast(list[str], area["module_ids"]):
            if module_id not in by_id:
                raise KnowledgeForgeError(
                    f"Area references missing module ID: {area['id']} -> {module_id}"
                )
            if module_id in assigned:
                raise KnowledgeForgeError(f"Module is assigned to multiple areas: {module_id}")
            assigned.add(module_id)
    missing = sorted(set(by_id) - assigned)
    if missing:
        raise KnowledgeForgeError("Modules have no assigned area: " + ", ".join(missing))
    return by_id


def build_indexes(
    modules: list[KnowledgeModule], areas: list[dict[str, object]]
) -> dict[str, object]:
    by_id = _validate_area_assignments(areas, modules)
    l0_areas: list[dict[str, object]] = []
    l1: dict[str, dict[str, object]] = {}
    for area in areas:
        area_id = cast(str, area["id"])
        l0_areas.append(
            {
                "id": area_id,
                "title": area["title"],
                "aliases": sorted(cast(list[str], area["aliases"])),
                "l1_path": f"indexes/l1/{area_id}.json",
            }
        )
        descriptors = [
            _module_descriptor(by_id[module_id])
            for module_id in cast(list[str], area["module_ids"])
        ]
        l1[area_id] = {
            "format_version": 1,
            "scope": "l1",
            "area_id": area_id,
            "title": area["title"],
            "summary": area["summary"],
            "decision_boundary": area["decision_boundary"],
            "modules": sorted(descriptors, key=lambda descriptor: str(descriptor["id"])),
        }
    return {
        "l0": {
            "format_version": 1,
            "scope": "l0",
            "areas": sorted(l0_areas, key=lambda area: str(area["id"])),
        },
        "l1": l1,
    }


def write_indexes(pack_root: Path, indexes: dict[str, object]) -> None:
    write_json_atomic(pack_root / "indexes" / "l0.json", indexes["l0"])
    l1 = cast(dict[str, object], indexes["l1"])
    for area_id in sorted(l1):
        write_json_atomic(pack_root / "indexes" / "l1" / f"{area_id}.json", l1[area_id])


def load_indexes(pack_root: Path) -> dict[str, object]:
    l0 = read_json(pack_root / "indexes" / "l0.json")
    if not isinstance(l0, dict):
        raise KnowledgeForgeError("L0 package index must be an object")
    areas = l0.get("areas")
    if not isinstance(areas, list):
        raise KnowledgeForgeError("L0 package index must contain an areas list")
    l1: dict[str, object] = {}
    for area in areas:
        if not isinstance(area, dict):
            raise KnowledgeForgeError("L0 package index must contain only area objects")
        area_id = area.get("id")
        if not isinstance(area_id, str) or not area_id:
            raise KnowledgeForgeError("L0 package area must have an ID")
        l1[area_id] = read_json(pack_root / "indexes" / "l1" / f"{area_id}.json")
    return {"l0": l0, "l1": l1}
