import json
import os
import tempfile
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError


def canonical_json_bytes(payload: object) -> bytes:
    text = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return f"{text}\n".encode()


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
            temporary_path = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def write_json_atomic(path: Path, payload: object) -> None:
    _atomic_write(path, canonical_json_bytes(payload))


def write_jsonl_atomic(path: Path, records: list[dict[str, object]]) -> None:
    content = b"".join(canonical_json_bytes(record) for record in records)
    _atomic_write(path, content)


def read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise KnowledgeForgeError(f"Cannot read JSON artifact: {path.name}") from error


def read_jsonl(path: Path) -> list[dict[str, object]]:
    try:
        records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    except (OSError, json.JSONDecodeError) as error:
        raise KnowledgeForgeError(f"Cannot read JSONL artifact: {path.name}") from error
    if not all(isinstance(record, dict) for record in records):
        raise KnowledgeForgeError(f"JSONL artifact must contain only objects: {path.name}")
    return records
