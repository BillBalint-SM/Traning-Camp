import os
import shutil
import tempfile
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_file
from knowledge_forge.models import InputRecord
from knowledge_forge.paths import require_regular_file, resolve_within

CHUNK_SIZE = 1024 * 1024


def intake_file(
    source_path: Path,
    role: str,
    media_type: str,
    inputs_dir: Path,
) -> InputRecord:
    require_regular_file(source_path, f"input role {role}")
    digest = sha256_file(source_path, CHUNK_SIZE)
    suffix = source_path.suffix.lower()
    target = inputs_dir / f"{digest}{suffix}"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        existing_digest = sha256_file(target, CHUNK_SIZE)
        if existing_digest != digest:
            raise KnowledgeForgeError(f"Existing intake digest mismatch for role {role}")
    else:
        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(dir=inputs_dir, delete=False) as handle:
                temporary_path = Path(handle.name)
            shutil.copyfile(source_path, temporary_path)
            copied_digest = sha256_file(temporary_path, CHUNK_SIZE)
            if copied_digest != digest:
                raise KnowledgeForgeError(f"Copied intake digest mismatch for role {role}")
            os.replace(temporary_path, target)
        finally:
            if temporary_path is not None and temporary_path.exists():
                temporary_path.unlink()
    return {
        "role": role,
        "media_type": media_type,
        "sha256": digest,
        "size_bytes": target.stat().st_size,
        "stored_path": target.relative_to(inputs_dir.parent).as_posix(),
    }


def verify_input_record(record: InputRecord, workspace_root: Path) -> None:
    stored_path = resolve_within(workspace_root, Path(record["stored_path"]))
    require_regular_file(stored_path, f"stored input role {record['role']}")
    if stored_path.stat().st_size != record["size_bytes"]:
        raise KnowledgeForgeError(f"Stored input size mismatch for role {record['role']}")
    if sha256_file(stored_path, CHUNK_SIZE) != record["sha256"]:
        raise KnowledgeForgeError(f"Stored input digest mismatch for role {record['role']}")


def upsert_input_record(
    records: list[InputRecord],
    record: InputRecord,
) -> list[InputRecord]:
    existing = [item for item in records if item["role"] == record["role"]]
    if existing and existing[0]["sha256"] != record["sha256"]:
        raise KnowledgeForgeError(
            f"Input role already has a different digest: {record['role']}"
        )
    retained = [item for item in records if item["role"] != record["role"]]
    return sorted([*retained, record], key=lambda item: item["role"])
