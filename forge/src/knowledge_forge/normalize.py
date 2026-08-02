import hashlib
import re
import unicodedata

from knowledge_forge.models import ExtractedDocument, NormalizedUnit

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize(
        "NFC",
        text.replace("\r\n", "\n").replace("\r", "\n"),
    )
    lines = [line.rstrip() for line in normalized.split("\n")]
    compact = re.sub(r"\n{3,}", "\n\n", "\n".join(lines))
    return compact.strip()


def _sections(text: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, list[str]]] = [("Preamble", [])]
    in_fence = False
    for line in normalize_text(text).splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            sections[-1][1].append(line)
            continue
        heading = None if in_fence else HEADING_PATTERN.match(line)
        if heading is not None:
            sections.append((heading.group(2).strip(), []))
        else:
            sections[-1][1].append(line)
    normalized_sections: list[tuple[str, str]] = []
    for heading, lines in sections:
        body = normalize_text("\n".join(lines))
        if body:
            normalized_sections.append((heading, body))
    return normalized_sections


def normalize_documents(documents: list[ExtractedDocument]) -> list[NormalizedUnit]:
    units: list[NormalizedUnit] = []
    for document in sorted(documents, key=lambda item: item["spine_index"]):
        for ordinal, (heading, text) in enumerate(_sections(document["text"])):
            identity_payload = (
                f"{document['document_id']}\n{heading}\n{ordinal}\n{text}"
            ).encode()
            content_sha256 = hashlib.sha256(text.encode()).hexdigest()
            unit_id = f"unit-{hashlib.sha256(identity_payload).hexdigest()[:20]}"
            units.append(
                {
                    "unit_id": unit_id,
                    "document_id": document["document_id"],
                    "ordinal": ordinal,
                    "heading": heading,
                    "text": text,
                    "content_sha256": content_sha256,
                }
            )
    return units
