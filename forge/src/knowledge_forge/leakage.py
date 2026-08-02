import re
import unicodedata
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError

_ORIGIN_PATTERN = re.compile(
    r"\b(book|author|publication|download|acquisition|chapter|"
    r"könyv|szerző|kiadvány|letöltés|beszerzés|fejezet)\b",
    re.IGNORECASE,
)
_WINDOWS_PATH_PATTERN = re.compile(r"\b[a-z]:[\\/]", re.IGNORECASE)
_UNIX_PATH_PATTERN = re.compile(r"/(?:users|home|tmp|var|etc)/", re.IGNORECASE)
_CREDENTIAL_PATTERN = re.compile(
    r"\b(?:api[_-]?key|token|password|secret)\s*[:=]\s*\S+", re.IGNORECASE
)
_TEXT_SUFFIXES = {".json", ".md"}


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFKC", value).casefold()


def _validate_markers(markers: list[str]) -> list[str]:
    if not all(isinstance(marker, str) and marker.strip() for marker in markers):
        raise KnowledgeForgeError("Private marker list must contain non-empty strings")
    return [_normalized(marker) for marker in markers]


def check_content_neutrality(
    pack_root: Path, relative_paths: list[str], markers: list[str]
) -> None:
    normalized_markers = _validate_markers(markers)
    for relative_path in relative_paths:
        path = pack_root / relative_path
        if path.suffix not in _TEXT_SUFFIXES:
            raise KnowledgeForgeError(f"Unsupported package text file: {relative_path}")
        try:
            content = path.read_text(encoding="utf-8")
        except OSError as error:
            raise KnowledgeForgeError(
                f"Cannot inspect package file: {relative_path}"
            ) from error
        normalized_content = _normalized(content)
        if any(marker in normalized_content for marker in normalized_markers):
            raise KnowledgeForgeError(
                f"Package contains forbidden content marker: {relative_path}"
            )
        if _ORIGIN_PATTERN.search(content):
            raise KnowledgeForgeError(
                f"Package contains forbidden origin reference: {relative_path}"
            )
        if _WINDOWS_PATH_PATTERN.search(content) or _UNIX_PATH_PATTERN.search(content):
            raise KnowledgeForgeError(
                f"Package contains an absolute path: {relative_path}"
            )
        if _CREDENTIAL_PATTERN.search(content):
            raise KnowledgeForgeError(
                f"Package contains a credential-shaped value: {relative_path}"
            )
