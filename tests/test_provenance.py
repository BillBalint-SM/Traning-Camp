from pathlib import Path

from knowledge_forge.contracts import validate_record
from knowledge_forge.provenance import build_provenance_ledger

SCHEMA_DIR = Path(__file__).parents[1] / "forge" / "schemas"


def test_provenance_is_sorted_complete_and_schema_valid() -> None:
    inputs = [
        {
            "role": "primary-text",
            "media_type": "application/epub+zip",
            "sha256": "a" * 64,
            "size_bytes": 10,
            "stored_path": f"inputs/{'a' * 64}.epub",
        },
        {
            "role": "layout-crosscheck",
            "media_type": "application/pdf",
            "sha256": "b" * 64,
            "size_bytes": 20,
            "stored_path": f"inputs/{'b' * 64}.pdf",
        },
    ]
    documents = [
        {
            "document_id": f"doc-{'c' * 20}",
            "input_sha256": "a" * 64,
            "spine_index": 0,
            "logical_path": "content.xhtml",
            "text": "# Topic\n\nKnowledge",
        }
    ]
    units = [
        {
            "unit_id": f"unit-{'d' * 20}",
            "document_id": f"doc-{'c' * 20}",
            "ordinal": 0,
            "heading": "Topic",
            "text": "Knowledge",
            "content_sha256": "e" * 64,
        }
    ]
    pdf_probe = {
        "input_sha256": "b" * 64,
        "page_count": 1,
        "encrypted": False,
        "text_char_count": 0,
        "text_sha256": "f" * 64,
    }
    ledger = build_provenance_ledger(inputs, documents, units, pdf_probe)
    assert ledger["schema_version"] == 1
    assert [item["role"] for item in ledger["inputs"]] == [
        "layout-crosscheck",
        "primary-text",
    ]
    assert ledger["units"][0]["unit_id"].startswith("unit-")
    validate_record(
        SCHEMA_DIR / "provenance-ledger.schema.json",
        ledger,
        "provenance ledger",
    )
