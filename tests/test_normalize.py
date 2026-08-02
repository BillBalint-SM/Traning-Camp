from knowledge_forge.models import ExtractedDocument
from knowledge_forge.normalize import normalize_documents, normalize_text


def test_normalize_text_stabilizes_unicode_line_endings_and_blank_lines() -> None:
    assert normalize_text("A\u0301\r\n\r\n\r\nB  \r\n") == "Á\n\nB"


def test_normalize_documents_splits_headings_without_splitting_fenced_code() -> None:
    documents: list[ExtractedDocument] = [
        {
            "document_id": "doc-a",
            "input_sha256": "a" * 64,
            "spine_index": 0,
            "logical_path": "one.xhtml",
            "text": (
                "Intro\n\n# First\n\nAlpha\n\n```python\n# not a heading\n```"
                "\n\n## Second\n\nBeta"
            ),
        }
    ]
    first = normalize_documents(documents)
    second = normalize_documents(documents)
    assert first == second
    assert [unit["heading"] for unit in first] == ["Preamble", "First", "Second"]
    assert "# not a heading" in first[1]["text"]
    assert all(unit["unit_id"].startswith("unit-") for unit in first)
