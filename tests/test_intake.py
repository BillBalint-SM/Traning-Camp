from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.intake import (
    intake_file,
    upsert_input_record,
    verify_input_record,
)


def test_intake_is_content_addressed_and_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "input.epub"
    source.write_bytes(b"stable input")
    inputs_dir = tmp_path / "inputs"
    first = intake_file(source, "primary-text", "application/epub+zip", inputs_dir)
    second = intake_file(source, "primary-text", "application/epub+zip", inputs_dir)
    assert first == second
    assert first["stored_path"].startswith("inputs/")
    assert len(list(inputs_dir.iterdir())) == 1


def test_verify_input_detects_tampering(tmp_path: Path) -> None:
    source = tmp_path / "input.pdf"
    source.write_bytes(b"verified bytes")
    record = intake_file(source, "layout-crosscheck", "application/pdf", tmp_path / "inputs")
    stored = tmp_path / Path(record["stored_path"])
    stored.write_bytes(b"tampered bytes")
    with pytest.raises(KnowledgeForgeError, match="digest mismatch"):
        verify_input_record(record, tmp_path)


def test_upsert_input_record_rejects_changed_digest_for_existing_role(
    tmp_path: Path,
) -> None:
    first_source = tmp_path / "first.epub"
    first_source.write_bytes(b"first")
    second_source = tmp_path / "second.epub"
    second_source.write_bytes(b"second")
    inputs_dir = tmp_path / "inputs"
    first = intake_file(first_source, "primary-text", "application/epub+zip", inputs_dir)
    second = intake_file(second_source, "primary-text", "application/epub+zip", inputs_dir)
    with pytest.raises(KnowledgeForgeError, match="different digest"):
        upsert_input_record([first], second)
