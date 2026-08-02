from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest
from knowledge_forge.epub import MAX_EPUB_MEMBERS, extract_epub
from knowledge_forge.errors import KnowledgeForgeError


def _write_minimal_epub(path: Path) -> None:
    container = """<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="OEBPS/content.opf"/></rootfiles>
</container>"""
    opf = """<?xml version="1.0"?>
<package xmlns="http://www.idpf.org/2007/opf">
  <manifest>
    <item id="second" href="second.xhtml" media-type="application/xhtml+xml"/>
    <item id="first" href="first.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine><itemref idref="first"/><itemref idref="second"/></spine>
</package>"""
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("META-INF/container.xml", container)
        archive.writestr("OEBPS/content.opf", opf)
        archive.writestr(
            "OEBPS/first.xhtml",
            "<h1>First</h1><p>Alpha</p><pre>print(1)\n  indented</pre>"
            "<img src='loop.svg' alt='agent loop'/><script>bad()</script>",
        )
        archive.writestr("OEBPS/second.xhtml", "<h1>Second</h1><p>Beta</p>")


def test_extract_epub_uses_spine_order_and_preserves_safe_structure(
    tmp_path: Path,
) -> None:
    path = tmp_path / "sample.epub"
    _write_minimal_epub(path)
    documents = extract_epub(path, "a" * 64)
    assert [item["spine_index"] for item in documents] == [0, 1]
    assert [item["logical_path"] for item in documents] == [
        "OEBPS/first.xhtml",
        "OEBPS/second.xhtml",
    ]
    assert documents[0]["text"] == (
        "# First\n\nAlpha\n\n```\nprint(1)\n  indented\n```\n\n[Figure: agent loop]"
    )
    assert "bad" not in documents[0]["text"]


def test_extract_epub_rejects_excessive_member_count(tmp_path: Path) -> None:
    path = tmp_path / "oversized.epub"
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        for index in range(MAX_EPUB_MEMBERS + 1):
            archive.writestr(f"empty/{index}.txt", "")
    with pytest.raises(KnowledgeForgeError, match="too many members"):
        extract_epub(path, "a" * 64)


def test_extract_epub_rejects_rootfile_path_escape(tmp_path: Path) -> None:
    path = tmp_path / "escaped.epub"
    container = """<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles><rootfile full-path="../content.opf"/></rootfiles>
</container>"""
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        archive.writestr("META-INF/container.xml", container)
    with pytest.raises(KnowledgeForgeError, match="Unsafe EPUB member path"):
        extract_epub(path, "a" * 64)
