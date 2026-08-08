import os
import shutil
import tempfile
import unicodedata
from pathlib import Path
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
from knowledge_forge.paths import require_regular_file
from knowledge_forge.portability import (
    _validate_character_budget,
    load_verified_portable_modules,
    verify_portable_export,
)

_SCHEMA_PATH = Path(__file__).parents[2] / "schemas" / "portable-lexical-index.schema.json"
_INDEX_FILE = "index.json"
_SCORING = {
    "title": 5,
    "alias": 4,
    "tag": 3,
    "identifier": 3,
    "body": 1,
    "minimum_score": 4,
    "minimum_margin": 2,
    "result_limit": 1,
}
_FIELD_NAMES = ("title", "alias", "tag", "identifier", "body")


def _tokenize(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    tokens: list[str] = []
    current: list[str] = []
    for character in normalized:
        if character.isalnum():
            current.append(character)
        elif current:
            tokens.append("".join(current))
            current = []
    if current:
        tokens.append("".join(current))
    return tokens


def _require_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise KnowledgeForgeError(f"Portable lexical index {label} must be a non-empty string")
    return value


def _front_matter_parts(text: str, module_id: str) -> tuple[str, str]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise KnowledgeForgeError(
            f"Portable lexical index module front matter is invalid: {module_id}"
        )
    for position, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join(lines[1:position]), "".join(lines[position + 1 :])
    raise KnowledgeForgeError(
        f"Portable lexical index module front matter is incomplete: {module_id}"
    )


def _aliases(front_matter: str, module_id: str) -> list[str]:
    matches = [
        line.removeprefix("aliases:").strip()
        for line in front_matter.splitlines()
        if line.startswith("aliases:")
    ]
    if len(matches) != 1:
        raise KnowledgeForgeError(
            f"Portable lexical index aliases are invalid: {module_id}"
        )
    raw = matches[0]
    if not raw.startswith("[") or not raw.endswith("]"):
        raise KnowledgeForgeError(
            f"Portable lexical index aliases are invalid: {module_id}"
        )
    values = [value.strip().strip("\"'") for value in raw[1:-1].split(",")]
    aliases = [value for value in values if value]
    if len(aliases) != len(set(aliases)):
        raise KnowledgeForgeError(
            f"Portable lexical index aliases are duplicated: {module_id}"
        )
    return aliases


def _record_fields(record: dict[str, object]) -> tuple[str, str, dict[str, set[str]]]:
    module_id = _require_string(record.get("id"), "module ID")
    title = _require_string(record.get("title"), f"title: {module_id}")
    text = _require_string(record.get("text"), f"text: {module_id}")
    metadata_value = record.get("metadata")
    if not isinstance(metadata_value, dict):
        raise KnowledgeForgeError(f"Portable lexical index metadata is invalid: {module_id}")
    metadata = cast(dict[str, object], metadata_value)
    area_id = _require_string(metadata.get("area_id"), f"area ID: {module_id}")
    tags_value = metadata.get("tags")
    if not isinstance(tags_value, list) or not all(
        isinstance(tag, str) and tag for tag in tags_value
    ):
        raise KnowledgeForgeError(f"Portable lexical index tags are invalid: {module_id}")
    front_matter, body = _front_matter_parts(text, module_id)
    aliases = _aliases(front_matter, module_id)
    return module_id, area_id, {
        "title": set(_tokenize(title)),
        "alias": set(_tokenize(" ".join(aliases))),
        "tag": set(_tokenize(" ".join(cast(list[str], tags_value)))),
        "identifier": set(_tokenize(module_id)),
        "body": set(_tokenize(body)),
    }


def _payload_without_digest(export_root: Path) -> dict[str, object]:
    manifest = verify_portable_export(export_root)
    export_sha256 = _require_string(manifest.get("export_sha256"), "export digest")
    postings: dict[str, dict[str, dict[str, object]]] = {}
    module_ids: set[str] = set()
    for record in read_jsonl(export_root / "rag" / "documents.jsonl"):
        module_id, area_id, fields = _record_fields(record)
        if module_id in module_ids:
            raise KnowledgeForgeError(f"Portable lexical index module is duplicated: {module_id}")
        module_ids.add(module_id)
        for field_name in _FIELD_NAMES:
            for token in fields[field_name]:
                document = postings.setdefault(token, {}).setdefault(
                    module_id,
                    {"module_id": module_id, "area_id": area_id, "fields": {}},
                )
                field_hits = cast(dict[str, int], document["fields"])
                field_hits[field_name] = 1
    return {
        "format_version": 1,
        "kind": "portable-lexical-index",
        "export_sha256": export_sha256,
        "tokenization": "unicode-nfkc-casefold-v1",
        "scoring": dict(_SCORING),
        "postings": [
            {
                "token": token,
                "documents": [
                    {
                        "module_id": module_id,
                        "area_id": cast(str, document["area_id"]),
                        "fields": dict(sorted(cast(dict[str, int], document["fields"]).items())),
                    }
                    for module_id, document in sorted(documents.items())
                ],
            }
            for token, documents in sorted(postings.items())
        ],
    }


def _with_digest(payload_without_digest: dict[str, object]) -> dict[str, object]:
    payload = dict(payload_without_digest)
    payload["index_sha256"] = sha256_bytes(canonical_json_bytes(payload_without_digest))
    return payload


def _assert_safe_index_root(index_root: Path, must_not_exist: bool) -> None:
    if index_root.is_symlink():
        raise KnowledgeForgeError(
            f"Portable lexical index root must not be a symbolic link: {index_root.name}"
        )
    if must_not_exist and index_root.exists():
        raise KnowledgeForgeError(
            f"Portable lexical index output already exists: {index_root.name}"
        )
    for parent in index_root.parents:
        if parent == parent.parent:
            break
        if parent.exists() and parent.is_symlink():
            raise KnowledgeForgeError(
                "Portable lexical index root must not use a symbolic link: "
                f"{parent.name}"
            )


def _read_index(index_root: Path) -> dict[str, object]:
    _assert_safe_index_root(index_root, False)
    if not index_root.is_dir():
        raise KnowledgeForgeError(
            f"Portable lexical index root is not an existing directory: {index_root.name}"
        )
    children = list(index_root.iterdir())
    if len(children) != 1 or children[0].name != _INDEX_FILE:
        raise KnowledgeForgeError("Portable lexical index root must contain only index.json")
    index_path = index_root / _INDEX_FILE
    require_regular_file(index_path, "Portable lexical index")
    payload = read_json(index_path)
    if not isinstance(payload, dict):
        raise KnowledgeForgeError("Portable lexical index root must be an object")
    return cast(dict[str, object], payload)


def verify_portable_lexical_index(
    export_root: Path, index_root: Path
) -> dict[str, object]:
    index = _read_index(index_root)
    validate_record(_SCHEMA_PATH, index, "portable lexical index")
    without_digest = {key: value for key, value in index.items() if key != "index_sha256"}
    claimed_digest = _require_string(index.get("index_sha256"), "digest")
    if sha256_bytes(canonical_json_bytes(without_digest)) != claimed_digest:
        raise KnowledgeForgeError("Portable lexical index digest mismatch")
    expected = _with_digest(_payload_without_digest(export_root))
    if canonical_json_bytes(index) != canonical_json_bytes(expected):
        raise KnowledgeForgeError("Portable lexical index content does not match export")
    return index


def build_portable_lexical_index(
    export_root: Path, index_root: Path
) -> dict[str, object]:
    _assert_safe_index_root(index_root, True)
    payload = _with_digest(_payload_without_digest(export_root))
    index_root.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(
        tempfile.mkdtemp(prefix=f".{index_root.name}.", dir=index_root.parent)
    )
    try:
        write_json_atomic(staging_root / _INDEX_FILE, payload)
        verify_portable_lexical_index(export_root, staging_root)
        _assert_safe_index_root(index_root, True)
        os.replace(staging_root, index_root)
    except OSError as error:
        raise KnowledgeForgeError(
            f"Cannot publish portable lexical index: {index_root.name}"
        ) from error
    finally:
        if staging_root.exists():
            shutil.rmtree(staging_root)
    return payload


def _rank_documents(index: dict[str, object], query: str) -> list[dict[str, object]]:
    postings_value = index.get("postings")
    if not isinstance(postings_value, list):
        raise KnowledgeForgeError("Portable lexical index postings are invalid")
    query_tokens = set(_tokenize(query))
    scores: dict[str, int] = {}
    areas: dict[str, str] = {}
    for posting_value in postings_value:
        if not isinstance(posting_value, dict):
            raise KnowledgeForgeError("Portable lexical index posting is invalid")
        posting = cast(dict[str, object], posting_value)
        token = _require_string(posting.get("token"), "posting token")
        if token not in query_tokens:
            continue
        documents_value = posting.get("documents")
        if not isinstance(documents_value, list):
            raise KnowledgeForgeError("Portable lexical index posting documents are invalid")
        for document_value in documents_value:
            if not isinstance(document_value, dict):
                raise KnowledgeForgeError("Portable lexical index posting document is invalid")
            document = cast(dict[str, object], document_value)
            module_id = _require_string(document.get("module_id"), "posting module ID")
            area_id = _require_string(document.get("area_id"), "posting area ID")
            fields_value = document.get("fields")
            if not isinstance(fields_value, dict):
                raise KnowledgeForgeError("Portable lexical index posting fields are invalid")
            if module_id in areas and areas[module_id] != area_id:
                raise KnowledgeForgeError(
                    f"Portable lexical index module area drift: {module_id}"
                )
            areas[module_id] = area_id
            for field_name in fields_value:
                if field_name not in _FIELD_NAMES:
                    raise KnowledgeForgeError(
                        f"Portable lexical index field is invalid: {field_name}"
                    )
                scores[module_id] = scores.get(module_id, 0) + _SCORING[field_name]
    eligible = [
        {"module_id": module_id, "area_id": areas[module_id], "score": score}
        for module_id, score in scores.items()
        if score >= _SCORING["minimum_score"]
    ]
    return sorted(
        eligible,
        key=lambda document: (-cast(int, document["score"]), cast(str, document["module_id"])),
    )


def _uncovered_context(
    export_sha256: str, status: str, alternatives: list[str], max_chars: int
) -> dict[str, object]:
    return {
        "format_version": 1,
        "export_sha256": export_sha256,
        "status": status,
        "area_id": None,
        "module_ids": [],
        "alternatives": alternatives,
        "expanded_module_ids": [],
        "modules": [],
        "relations": [],
        "budget": {
            "format_version": 1,
            "max_chars": max_chars,
            "used_chars": 0,
            "omitted_module_ids": [],
        },
    }


def load_portable_context_lexical(
    export_root: Path, index_root: Path, query: str, max_chars: int
) -> dict[str, object]:
    if not isinstance(query, str) or not query:
        raise KnowledgeForgeError("Portable lexical context query must be a non-empty string")
    _validate_character_budget(max_chars)
    index = verify_portable_lexical_index(export_root, index_root)
    export_sha256 = _require_string(index.get("export_sha256"), "export digest")
    ranked = _rank_documents(index, query)
    if not ranked:
        return _uncovered_context(export_sha256, "not-covered", [], max_chars)
    primary = ranked[0]
    if len(ranked) > 1 and (
        cast(int, primary["score"]) - cast(int, ranked[1]["score"])
        < _SCORING["minimum_margin"]
    ):
        alternatives = sorted(
            {
                cast(str, primary["area_id"]),
                cast(str, ranked[1]["area_id"]),
            }
        )
        return _uncovered_context(export_sha256, "ambiguous", alternatives, max_chars)
    module_id = cast(str, primary["module_id"])
    modules = load_verified_portable_modules(export_root, [module_id])
    module = modules[0]
    used_chars = len(cast(str, module["text"]))
    if used_chars > max_chars:
        raise KnowledgeForgeError(
            "Portable lexical context primary module exceeds character budget"
        )
    return {
        "format_version": 1,
        "export_sha256": export_sha256,
        "status": "covered",
        "area_id": primary["area_id"],
        "module_ids": [module_id],
        "alternatives": [],
        "expanded_module_ids": [module_id],
        "modules": modules,
        "relations": [],
        "budget": {
            "format_version": 1,
            "max_chars": max_chars,
            "used_chars": used_chars,
            "omitted_module_ids": [],
        },
    }
