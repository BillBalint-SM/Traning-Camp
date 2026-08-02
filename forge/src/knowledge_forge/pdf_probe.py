import hashlib
import unicodedata
from pathlib import Path

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.models import PdfLimits, PdfProbe
from knowledge_forge.paths import require_regular_file

DEFAULT_PDF_LIMITS: PdfLimits = {
    "max_bytes": 256 * 1024 * 1024,
    "max_pages": 2_000,
    "max_text_chars": 50_000_000,
}


def probe_pdf(pdf_path: Path, input_sha256: str, limits: PdfLimits) -> PdfProbe:
    require_regular_file(pdf_path, "PDF probe input")
    if pdf_path.stat().st_size > limits["max_bytes"]:
        raise KnowledgeForgeError("PDF input size exceeds safety limit")
    try:
        reader = PdfReader(pdf_path)
    except PdfReadError as error:
        raise KnowledgeForgeError("PDF parsing failed") from error
    if reader.is_encrypted:
        raise KnowledgeForgeError("PDF input is encrypted and cannot be probed")
    if len(reader.pages) > limits["max_pages"]:
        raise KnowledgeForgeError("PDF page count exceeds safety limit")
    page_text: list[str] = []
    text_char_count = 0
    for page in reader.pages:
        text = page.extract_text() or ""
        text_char_count += len(text)
        if text_char_count > limits["max_text_chars"]:
            raise KnowledgeForgeError("PDF extracted text exceeds safety limit")
        page_text.append(text)
    normalized_text = unicodedata.normalize("NFC", "\n".join(page_text))
    return {
        "input_sha256": input_sha256,
        "page_count": len(reader.pages),
        "encrypted": False,
        "text_char_count": len(normalized_text),
        "text_sha256": hashlib.sha256(normalized_text.encode()).hexdigest(),
    }
