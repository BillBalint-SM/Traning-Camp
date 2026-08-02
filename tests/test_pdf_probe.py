from pathlib import Path

import pytest
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.pdf_probe import DEFAULT_PDF_LIMITS, probe_pdf
from pypdf import PdfWriter


def _write_blank_pdf(path: Path, encrypted: bool) -> None:
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=300)
    if encrypted:
        writer.encrypt("local-test-password")
    with path.open("wb") as stream:
        writer.write(stream)


def test_probe_pdf_records_page_count(tmp_path: Path) -> None:
    path = tmp_path / "sample.pdf"
    _write_blank_pdf(path, False)
    probe = probe_pdf(path, "b" * 64, DEFAULT_PDF_LIMITS)
    assert probe["page_count"] == 1
    assert probe["encrypted"] is False
    assert probe["text_char_count"] == 0


def test_probe_pdf_rejects_encrypted_input(tmp_path: Path) -> None:
    path = tmp_path / "encrypted.pdf"
    _write_blank_pdf(path, True)
    with pytest.raises(KnowledgeForgeError, match="encrypted"):
        probe_pdf(path, "c" * 64, DEFAULT_PDF_LIMITS)


def test_probe_pdf_rejects_page_limit(tmp_path: Path) -> None:
    path = tmp_path / "sample.pdf"
    _write_blank_pdf(path, False)
    limits = {"max_bytes": 1024 * 1024, "max_pages": 0, "max_text_chars": 100}
    with pytest.raises(KnowledgeForgeError, match="page count exceeds"):
        probe_pdf(path, "d" * 64, limits)


def test_probe_pdf_reports_invalid_pdf(tmp_path: Path) -> None:
    path = tmp_path / "invalid.pdf"
    path.write_bytes(b"not a pdf")
    with pytest.raises(KnowledgeForgeError, match="PDF parsing failed"):
        probe_pdf(path, "e" * 64, DEFAULT_PDF_LIMITS)
