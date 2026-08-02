import hashlib
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.models import ExtractedDocument

MAX_EPUB_MEMBERS = 10_000
MAX_EPUB_MEMBER_BYTES = 64 * 1024 * 1024
MAX_EPUB_TOTAL_BYTES = 512 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1_000


def _validate_archive_limits(archive: ZipFile) -> None:
    members = archive.infolist()
    if len(members) > MAX_EPUB_MEMBERS:
        raise KnowledgeForgeError("EPUB has too many members")
    total_bytes = sum(member.file_size for member in members)
    if total_bytes > MAX_EPUB_TOTAL_BYTES:
        raise KnowledgeForgeError("EPUB uncompressed size exceeds safety limit")
    for member in members:
        if member.file_size > MAX_EPUB_MEMBER_BYTES:
            raise KnowledgeForgeError(
                f"EPUB member exceeds safety limit: {member.filename}"
            )
        if (
            member.file_size > 1024 * 1024
            and member.compress_size > 0
            and member.file_size / member.compress_size > MAX_COMPRESSION_RATIO
        ):
            raise KnowledgeForgeError(
                f"EPUB member compression ratio is unsafe: {member.filename}"
            )


def _safe_member(name: str) -> str:
    if "\\" in name:
        raise KnowledgeForgeError("Unsafe EPUB member path: backslash separator")
    member = PurePosixPath(name)
    if member.is_absolute() or ".." in member.parts:
        raise KnowledgeForgeError(f"Unsafe EPUB member path: {member.name}")
    return member.as_posix()


def _rootfile_path(archive: ZipFile) -> str:
    root = ElementTree.fromstring(archive.read("META-INF/container.xml"))
    rootfile = root.find(".//{*}rootfile")
    if rootfile is None or not rootfile.attrib.get("full-path"):
        raise KnowledgeForgeError("EPUB container has no rootfile")
    return _safe_member(rootfile.attrib["full-path"])


def _spine_paths(archive: ZipFile, opf_path: str) -> list[str]:
    package = ElementTree.fromstring(archive.read(opf_path))
    manifest = {
        item.attrib["id"]: item.attrib["href"]
        for item in package.findall(".//{*}manifest/{*}item")
        if item.attrib.get("media-type") == "application/xhtml+xml"
        and item.attrib.get("id")
        and item.attrib.get("href")
    }
    opf_dir = posixpath.dirname(opf_path)
    paths: list[str] = []
    for itemref in package.findall(".//{*}spine/{*}itemref"):
        href = manifest.get(itemref.attrib.get("idref", ""))
        if href is not None:
            resolved_path = posixpath.normpath(posixpath.join(opf_dir, href))
            paths.append(_safe_member(resolved_path))
    if not paths:
        raise KnowledgeForgeError("EPUB spine contains no XHTML documents")
    return paths


class _XhtmlTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._lines: list[str] = []
        self._buffer: list[str] = []
        self._heading_level: int | None = None
        self._ignored_depth = 0
        self._pre_depth = 0
        self._pre_buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "nav"}:
            self._ignored_depth += 1
        if self._ignored_depth > 0:
            return
        if tag == "pre":
            self._flush()
            self._pre_depth += 1
            return
        if tag == "img":
            self._flush()
            attributes = dict(attrs)
            label = attributes.get("alt") or PurePosixPath(
                attributes.get("src") or "unlabelled-figure"
            ).name
            self._lines.append(f"[Figure: {label}]")
            return
        if re.fullmatch(r"h[1-6]", tag):
            self._flush()
            self._heading_level = int(tag[1])
        elif tag in {"p", "li", "blockquote"}:
            self._flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav"} and self._ignored_depth > 0:
            self._ignored_depth -= 1
            return
        if self._ignored_depth > 0:
            return
        if tag == "pre" and self._pre_depth > 0:
            self._pre_depth -= 1
            code = "".join(self._pre_buffer).replace("\r\n", "\n").strip("\n")
            self._pre_buffer.clear()
            if code:
                self._lines.append(f"```\n{code}\n```")
            return
        if re.fullmatch(r"h[1-6]", tag) or tag in {"p", "li", "blockquote"}:
            self._flush()

    def handle_data(self, data: str) -> None:
        if self._ignored_depth > 0:
            return
        if self._pre_depth > 0:
            self._pre_buffer.append(data)
        else:
            self._buffer.append(data)

    def _flush(self) -> None:
        text = " ".join("".join(self._buffer).split())
        self._buffer.clear()
        if not text:
            return
        if self._heading_level is not None:
            text = f"{'#' * self._heading_level} {text}"
            self._heading_level = None
        self._lines.append(text)

    def text(self) -> str:
        self._flush()
        return "\n\n".join(self._lines)


def extract_epub(epub_path: Path, input_sha256: str) -> list[ExtractedDocument]:
    try:
        with ZipFile(epub_path) as archive:
            _validate_archive_limits(archive)
            opf_path = _rootfile_path(archive)
            documents: list[ExtractedDocument] = []
            for index, logical_path in enumerate(_spine_paths(archive, opf_path)):
                parser = _XhtmlTextParser()
                parser.feed(archive.read(logical_path).decode("utf-8-sig"))
                text = parser.text()
                if text:
                    identity = hashlib.sha256(
                        f"{input_sha256}\n{logical_path}".encode()
                    ).hexdigest()[:20]
                    documents.append(
                        {
                            "document_id": f"doc-{identity}",
                            "input_sha256": input_sha256,
                            "spine_index": index,
                            "logical_path": logical_path,
                            "text": text,
                        }
                    )
            return documents
    except (BadZipFile, KeyError, ElementTree.ParseError, UnicodeDecodeError) as error:
        raise KnowledgeForgeError(f"EPUB extraction failed: {type(error).__name__}") from error
