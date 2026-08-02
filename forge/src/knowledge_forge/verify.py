from pathlib import Path
from typing import cast

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.intake import verify_input_record
from knowledge_forge.io import read_json, read_jsonl
from knowledge_forge.models import (
    ExtractedDocument,
    InputRecord,
    NormalizedUnit,
    PdfProbe,
)
from knowledge_forge.provenance import build_provenance_ledger


def _require_unique(values: list[str], label: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise KnowledgeForgeError(f"Duplicate {label}: {value}")
        seen.add(value)


def verify_foundation(
    workspace_root: Path,
    schema_dir: Path,
    registry_path: Path,
    documents_path: Path,
    probe_path: Path,
    units_path: Path,
    ledger_path: Path,
) -> None:
    registry_payload = read_json(registry_path)
    if not isinstance(registry_payload, list):
        raise KnowledgeForgeError("Input registry root must be an array")
    inputs = cast(list[InputRecord], registry_payload)
    if not inputs:
        raise KnowledgeForgeError("Input registry must not be empty")
    for record in inputs:
        validate_record(schema_dir / "input-record.schema.json", record, "input record")
        verify_input_record(record, workspace_root)
    _require_unique([record["role"] for record in inputs], "input role")

    documents = cast(list[ExtractedDocument], read_jsonl(documents_path))
    if not documents:
        raise KnowledgeForgeError("Extracted document set must not be empty")
    for document in documents:
        validate_record(
            schema_dir / "extracted-document.schema.json",
            document,
            "extracted document",
        )
    _require_unique(
        [document["document_id"] for document in documents],
        "extracted document ID",
    )
    spine_indices = sorted(document["spine_index"] for document in documents)
    if spine_indices != list(range(len(documents))):
        raise KnowledgeForgeError("Extracted document spine indices are not contiguous")
    epub_hashes = {
        record["sha256"]
        for record in inputs
        if record["media_type"] == "application/epub+zip"
    }
    if not epub_hashes or any(document["input_sha256"] not in epub_hashes for document in documents):
        raise KnowledgeForgeError("Extracted documents do not match an EPUB input")

    probe = cast(PdfProbe, read_json(probe_path))
    validate_record(schema_dir / "pdf-probe.schema.json", probe, "PDF probe")
    pdf_hashes = {
        record["sha256"]
        for record in inputs
        if record["media_type"] == "application/pdf"
    }
    if probe["input_sha256"] not in pdf_hashes:
        raise KnowledgeForgeError("PDF probe does not match a PDF input")

    units = cast(list[NormalizedUnit], read_jsonl(units_path))
    if not units:
        raise KnowledgeForgeError("Normalized unit set must not be empty")
    for unit in units:
        validate_record(
            schema_dir / "normalized-unit.schema.json",
            unit,
            "normalized unit",
        )
    _require_unique([unit["unit_id"] for unit in units], "normalized unit ID")
    document_ids = {document["document_id"] for document in documents}
    missing_document_ids = sorted(
        {unit["document_id"] for unit in units} - document_ids
    )
    if missing_document_ids:
        raise KnowledgeForgeError(
            "Normalized units reference missing document IDs: "
            + ", ".join(missing_document_ids)
        )

    ledger = read_json(ledger_path)
    validate_record(
        schema_dir / "provenance-ledger.schema.json",
        ledger,
        "provenance ledger",
    )
    expected_ledger = build_provenance_ledger(inputs, documents, units, probe)
    if ledger != expected_ledger:
        raise KnowledgeForgeError("Provenance ledger does not match current artifacts")

    pack_path = workspace_root / "pack"
    if pack_path.exists():
        raise KnowledgeForgeError("Foundation slice must not create a pack directory")
