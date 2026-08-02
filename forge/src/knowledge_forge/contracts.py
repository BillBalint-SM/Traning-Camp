from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.io import read_json


def _schema_registry(schema_dir: Path) -> Registry:
    registry = Registry()
    for candidate in sorted(schema_dir.glob("*.schema.json")):
        schema = read_json(candidate)
        if not isinstance(schema, dict):
            raise KnowledgeForgeError(f"Schema root must be an object: {candidate.name}")
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            raise KnowledgeForgeError(f"Schema has no string $id: {candidate.name}")
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry


def validate_record(schema_path: Path, record: object, label: str) -> None:
    schema = read_json(schema_path)
    if not isinstance(schema, dict):
        raise KnowledgeForgeError(f"Schema root must be an object: {schema_path.name}")
    validator = Draft202012Validator(
        schema,
        registry=_schema_registry(schema_path.parent),
    )
    errors = sorted(
        validator.iter_errors(record),
        key=lambda error: tuple(str(part) for part in error.path),
    )
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "root"
        raise KnowledgeForgeError(
            f"Schema validation failed for {label} at {location}: {first.message}"
        )
