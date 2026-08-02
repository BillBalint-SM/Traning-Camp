from typing import TypedDict


class InputRecord(TypedDict):
    role: str
    media_type: str
    sha256: str
    size_bytes: int
    stored_path: str


class ExtractedDocument(TypedDict):
    document_id: str
    input_sha256: str
    spine_index: int
    logical_path: str
    text: str


class PdfProbe(TypedDict):
    input_sha256: str
    page_count: int
    encrypted: bool
    text_char_count: int
    text_sha256: str


class PdfLimits(TypedDict):
    max_bytes: int
    max_pages: int
    max_text_chars: int


class NormalizedUnit(TypedDict):
    unit_id: str
    document_id: str
    ordinal: int
    heading: str
    text: str
    content_sha256: str
