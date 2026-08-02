# Knowledge Forge Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, fail-closed local foundation that privately intakes, verifies, extracts, and normalizes the approved long-form inputs into stable addressable units without producing an Agent-visible knowledge package yet.

**Architecture:** A small functional Python package performs content-addressed intake, format-specific extraction, normalization, schema validation, and private provenance generation. All private and generated artifacts live behind Git and export boundaries; tracked code and tests contain no input content. EPUB is the structural text authority for this slice, while PDF is an independent page/text/visual cross-check.

**Tech Stack:** Python 3.10+, uv with committed lockfile, Python standard library, pypdf, jsonschema, pytest, Ruff, Poppler `pdfinfo`/`pdftoppm` for PDF verification.

## Global Constraints

- Private intake, neutral output.
- Deterministic before intelligent.
- Knowledge is reorganized by use.
- Canonical data stays simple.
- Fail closed.
- No hidden portability dependencies.
- Only `pack/` is eligible for knowledge injection; this plan does not create trusted `pack/` content.
- `inputs/`, `private/`, `work/`, `derived/`, and `dist/` must remain outside Agent context and outside any future export.
- Errors must name the failed stage and logical artifact without printing private content, credentials, or absolute source paths.
- No changes to AI Booster Kit, no GitHub publication, no model training, no embeddings, and no GraphRAG.
- Use functional, single-purpose functions; make every function parameter explicit; use classes only where a library protocol requires one.
- Work on Windows and normalize persisted relative paths to POSIX separators.
- Context7 is intentionally omitted: this slice uses stable local Python APIs and the resolved dependency versions will be fixed by `uv.lock`.

---

## Scope decomposition

The approved design contains three independently reviewable systems:

1. **Foundation — this plan:** private intake, hashing, EPUB extraction, PDF probing, normalization, contracts, provenance, and end-to-end verification.
2. **Portable knowledge v0 — next plan:** topic taxonomy, candidate review, trusted modules, L0/L1 indexes, canonical graph, routing skill, leakage gate, and ZIP export.
3. **Deep v1 — later plan:** complete semantic coverage, contradiction review, routing evaluation, semantic back-checking, and derived Understand Anything/Graphify maps.

This plan ends with deterministic normalized units and a verified private ledger. It deliberately does not promote knowledge or write into `pack/`.

### Approved-spec coverage

| Approved design area | This plan | Routed follow-up |
|---|---|---|
| Private intake, hashes, trust boundaries | Tasks 1-3 and 9 | — |
| Deterministic extraction and normalization | Tasks 4-6 and 9 | — |
| Private provenance and semantic traceability base | Tasks 7-9 | Candidate-to-module mapping extends in portable-v0 |
| Explicit errors, contracts, negative paths | Tasks 1-9 | Export-specific failures extend in portable-v0 |
| Knowledge module contract and maturity | Boundary only | Portable-v0 plan |
| L0/L1/L2 routing and host-neutral skill | Not created | Portable-v0 plan |
| Canonical module graph and manifest | Not created | Portable-v0 plan |
| Leakage allowlist and relocatable ZIP | Git boundary only | Portable-v0 plan |
| Full semantic coverage and contradiction review | Not started | Deep-v1 plan |
| Understand Anything and Graphify projections | Not run | Deep-v1 plan after a validated `pack/` exists |

There is no uncovered requirement inside the declared foundation slice. All remaining approved-spec requirements are explicitly assigned to one of the two follow-up plans.

## Acceptance criteria

1. Both approved inputs are copied into `inputs/` under content-addressed names, and the copied bytes match their recorded SHA-256 values.
2. Re-running intake is idempotent and never overwrites different bytes.
3. EPUB content is read in OPF spine order, active content is ignored, and extracted document JSONL is byte-for-byte stable across identical runs.
4. PDF page count, encryption state, text character count, and extracted-text digest are recorded independently; representative rendered pages are visually inspected.
5. Normalized unit IDs and content digests are stable across identical runs and unaffected by line-ending differences.
6. Every generated JSON or JSONL record passes its declared Draft 2020-12 JSON Schema.
7. The private provenance ledger maps inputs to extracted documents and normalized units without writing anything to `pack/`.
8. A tampered intake copy causes an explicit non-zero verification failure.
9. Git confirms that all private inputs and generated working files are ignored while source code, schemas, tests, the spec, and this plan remain reviewable.
10. `uv run pytest`, `uv run ruff check .`, and the actual-input foundation verification all pass.

## Locked file map

```text
.gitignore                                      private/generated boundaries
pyproject.toml                                  package metadata, CLI, dependencies, tool config
uv.lock                                         reproducible resolved environment
forge/config/forge.json                         tracked relative directory contract
forge/schemas/input-record.schema.json          private intake record contract
forge/schemas/extracted-document.schema.json    extracted EPUB document contract
forge/schemas/pdf-probe.schema.json             independent PDF probe contract
forge/schemas/normalized-unit.schema.json        normalized unit contract
forge/schemas/provenance-ledger.schema.json      private traceability contract
forge/src/knowledge_forge/__init__.py            package identity only
forge/src/knowledge_forge/__main__.py            module entry point
forge/src/knowledge_forge/errors.py              explicit domain errors
forge/src/knowledge_forge/paths.py               workspace boundary enforcement
forge/src/knowledge_forge/io.py                  canonical JSON/JSONL and atomic writes
forge/src/knowledge_forge/hashing.py             streaming SHA-256
forge/src/knowledge_forge/models.py              TypedDict record interfaces
forge/src/knowledge_forge/intake.py              content-addressed private intake
forge/src/knowledge_forge/epub.py                ordered EPUB structural extraction
forge/src/knowledge_forge/pdf_probe.py            PDF metadata/text cross-check
forge/src/knowledge_forge/normalize.py            deterministic normalized units
forge/src/knowledge_forge/contracts.py            JSON Schema loading and validation
forge/src/knowledge_forge/provenance.py           private input-to-unit ledger
forge/src/knowledge_forge/verify.py               foundation-wide invariant checks
forge/src/knowledge_forge/cli.py                  explicit subcommand orchestration
tests/test_paths.py                               path traversal and file checks
tests/test_io_hashing.py                          canonical bytes, atomic output, file digests
tests/test_intake.py                              idempotence and tamper behavior
tests/test_epub.py                                real minimal EPUB integration fixture
tests/test_pdf_probe.py                           real pypdf-created PDF integration fixture
tests/test_normalize.py                           stable unit segmentation and IDs
tests/test_contracts.py                           positive and negative schema checks
tests/test_provenance.py                          complete private lineage
tests/test_cli_foundation.py                      full command-line integration flow
```

### Task 1: Establish the Python project and path boundary

**Files:**
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `forge/config/forge.json`
- Create: `forge/src/knowledge_forge/__init__.py`
- Create: `forge/src/knowledge_forge/errors.py`
- Create: `forge/src/knowledge_forge/paths.py`
- Test: `tests/test_paths.py`

**Interfaces:**
- Produces: `KnowledgeForgeError`; `resolve_within(root: Path, relative_path: Path) -> Path`; `require_regular_file(path: Path, label: str) -> None`.
- Produces tracked directory names consumed by every later task: `inputs`, `private/provenance`, `work/extracted`, `work/normalized`, `derived`, `dist`.

- [ ] **Step 1: Write the path-boundary tests**

```python
from pathlib import Path

import pytest

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.paths import require_regular_file, resolve_within


def test_resolve_within_accepts_relative_child(tmp_path: Path) -> None:
    assert resolve_within(tmp_path, Path("work/extracted")) == (
        tmp_path / "work" / "extracted"
    ).resolve()


def test_resolve_within_rejects_parent_escape(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="escapes workspace root"):
        resolve_within(tmp_path, Path("../outside"))


def test_resolve_within_rejects_absolute_path(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="must be relative"):
        resolve_within(tmp_path, (tmp_path / "absolute").resolve())


def test_require_regular_file_rejects_directory(tmp_path: Path) -> None:
    with pytest.raises(KnowledgeForgeError, match="is not a regular file"):
        require_regular_file(tmp_path, "test artifact")


def test_require_regular_file_rejects_symlink(tmp_path: Path) -> None:
    target = tmp_path / "target.txt"
    target.write_text("content", encoding="utf-8")
    link = tmp_path / "link.txt"
    try:
        link.symlink_to(target)
    except OSError as error:
        pytest.skip(f"Filesystem does not permit test symlink creation: {error.winerror}")
    with pytest.raises(KnowledgeForgeError, match="must not be a symbolic link"):
        require_regular_file(link, "test artifact")
```

- [ ] **Step 2: Create project metadata and tracked configuration**

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "portable-knowledge-forge"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
  "jsonschema",
  "pypdf",
]

[project.scripts]
knowledge-forge = "knowledge_forge.cli:main"

[dependency-groups]
dev = [
  "pytest",
  "ruff",
]

[tool.setuptools]
package-dir = {"" = "forge/src"}

[tool.setuptools.packages.find]
where = ["forge/src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
target-version = "py310"
line-length = 88
```

```json
{
  "inputs_dir": "inputs",
  "provenance_dir": "private/provenance",
  "extracted_dir": "work/extracted",
  "normalized_dir": "work/normalized",
  "derived_dir": "derived",
  "dist_dir": "dist"
}
```

- [ ] **Step 3: Add the private/generated Git boundary**

```gitignore
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
*.egg-info/
.env
.env.*

inputs/**
private/**
work/**
derived/**
dist/**
.ua/**

!inputs/.gitkeep
!private/.gitkeep
!work/.gitkeep
!derived/.gitkeep
!dist/.gitkeep
```

- [ ] **Step 4: Run the new test and confirm the expected import failure**

Run: `uv run pytest tests/test_paths.py -v`

Expected: FAIL because `knowledge_forge.errors` and `knowledge_forge.paths` do not exist.

- [ ] **Step 5: Implement the error and path functions**

```python
# forge/src/knowledge_forge/errors.py
class KnowledgeForgeError(RuntimeError):
    """Raised when a forge invariant is violated."""
```

```python
# forge/src/knowledge_forge/paths.py
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError


def resolve_within(root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute():
        raise KnowledgeForgeError(f"Path must be relative: {relative_path.name}")
    resolved_root = root.resolve()
    resolved_path = (resolved_root / relative_path).resolve()
    if not resolved_path.is_relative_to(resolved_root):
        raise KnowledgeForgeError(
            f"Path escapes workspace root: {relative_path.as_posix()}"
        )
    return resolved_path


def require_regular_file(path: Path, label: str) -> None:
    if path.is_symlink():
        raise KnowledgeForgeError(f"{label} must not be a symbolic link: {path.name}")
    if not path.is_file():
        raise KnowledgeForgeError(f"{label} is not a regular file: {path.name}")
```

- [ ] **Step 6: Resolve and lock the environment, then run the test**

Run: `uv lock && uv sync --locked && uv run pytest tests/test_paths.py -v`

Expected: five tests PASS and `uv.lock` is created.

- [ ] **Step 7: Commit the project boundary**

```powershell
git add .gitignore pyproject.toml uv.lock forge/config/forge.json forge/src/knowledge_forge/__init__.py forge/src/knowledge_forge/errors.py forge/src/knowledge_forge/paths.py tests/test_paths.py
git commit -m "feat: establish knowledge forge boundary"
```

### Task 2: Add canonical I/O and streaming hashes

**Files:**
- Create: `forge/src/knowledge_forge/io.py`
- Create: `forge/src/knowledge_forge/hashing.py`
- Test: `tests/test_io_hashing.py`

**Interfaces:**
- Produces: `sha256_file(path: Path, chunk_size: int) -> str`.
- Produces: `canonical_json_bytes(payload: object) -> bytes`; `read_json(path: Path) -> object`; `read_jsonl(path: Path) -> list[dict[str, object]]`; `write_json_atomic(path: Path, payload: object) -> None`; `write_jsonl_atomic(path: Path, records: list[dict[str, object]]) -> None`.

- [ ] **Step 1: Write failing canonicalization and hashing tests**

```python
import hashlib
from pathlib import Path

from knowledge_forge.hashing import sha256_file
from knowledge_forge.io import (
    canonical_json_bytes,
    read_json,
    read_jsonl,
    write_json_atomic,
    write_jsonl_atomic,
)


def test_canonical_json_is_sorted_utf8_and_newline_terminated() -> None:
    payload = {"z": "árvíz", "a": 1}
    assert canonical_json_bytes(payload) == '{"a":1,"z":"árvíz"}\n'.encode()


def test_json_and_jsonl_round_trip(tmp_path: Path) -> None:
    json_path = tmp_path / "record.json"
    jsonl_path = tmp_path / "records.jsonl"
    write_json_atomic(json_path, {"value": 2})
    write_jsonl_atomic(jsonl_path, [{"id": "a"}, {"id": "b"}])
    assert read_json(json_path) == {"value": 2}
    assert read_jsonl(jsonl_path) == [{"id": "a"}, {"id": "b"}]


def test_sha256_file_matches_hashlib(tmp_path: Path) -> None:
    path = tmp_path / "payload.bin"
    path.write_bytes(b"knowledge-forge")
    assert sha256_file(path, 4) == hashlib.sha256(b"knowledge-forge").hexdigest()
```

- [ ] **Step 2: Run the test and confirm the missing-module failure**

Run: `uv run pytest tests/test_io_hashing.py -v`

Expected: FAIL because `knowledge_forge.io` and `knowledge_forge.hashing` do not exist.

- [ ] **Step 3: Implement canonical JSON and atomic writes**

```python
# forge/src/knowledge_forge/io.py
import json
import os
import tempfile
from pathlib import Path


def canonical_json_bytes(payload: object) -> bytes:
    text = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return f"{text}\n".encode("utf-8")


def _atomic_write(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(dir=path.parent, delete=False)
    temporary_path = Path(handle.name)
    try:
        with handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def write_json_atomic(path: Path, payload: object) -> None:
    _atomic_write(path, canonical_json_bytes(payload))


def write_jsonl_atomic(path: Path, records: list[dict[str, object]]) -> None:
    content = b"".join(canonical_json_bytes(record) for record in records)
    _atomic_write(path, content)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
```

- [ ] **Step 4: Implement streaming SHA-256**

```python
# forge/src/knowledge_forge/hashing.py
import hashlib
from pathlib import Path

from knowledge_forge.paths import require_regular_file


def sha256_file(path: Path, chunk_size: int) -> str:
    require_regular_file(path, "hash input")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()
```

- [ ] **Step 5: Run the focused tests**

Run: `uv run pytest tests/test_io_hashing.py -v`

Expected: three tests PASS.

- [ ] **Step 6: Commit canonical I/O**

```powershell
git add forge/src/knowledge_forge/io.py forge/src/knowledge_forge/hashing.py tests/test_io_hashing.py
git commit -m "feat: add canonical forge io"
```

### Task 3: Implement content-addressed private intake

**Files:**
- Create: `forge/src/knowledge_forge/models.py`
- Create: `forge/src/knowledge_forge/intake.py`
- Test: `tests/test_intake.py`

**Interfaces:**
- Produces `InputRecord` with exact keys: `role`, `media_type`, `sha256`, `size_bytes`, `stored_path`.
- Produces: `intake_file(source_path: Path, role: str, media_type: str, inputs_dir: Path) -> InputRecord`.
- Produces: `verify_input_record(record: InputRecord, workspace_root: Path) -> None`.
- Produces: `upsert_input_record(records: list[InputRecord], record: InputRecord) -> list[InputRecord]`; duplicate roles with different hashes fail.

- [ ] **Step 1: Write the intake tests**

```python
from pathlib import Path

import pytest

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.intake import intake_file, verify_input_record


def test_intake_is_content_addressed_and_idempotent(tmp_path: Path) -> None:
    source = tmp_path / "input.epub"
    source.write_bytes(b"stable input")
    inputs_dir = tmp_path / "inputs"
    first = intake_file(source, "primary-text", "application/epub+zip", inputs_dir)
    second = intake_file(source, "primary-text", "application/epub+zip", inputs_dir)
    assert first == second
    assert first["stored_path"].startswith("inputs/")
    assert len(list(inputs_dir.iterdir())) == 1


def test_verify_input_detects_tampering(tmp_path: Path) -> None:
    source = tmp_path / "input.pdf"
    source.write_bytes(b"verified bytes")
    record = intake_file(source, "layout-crosscheck", "application/pdf", tmp_path / "inputs")
    stored = tmp_path / Path(record["stored_path"])
    stored.write_bytes(b"tampered bytes")
    with pytest.raises(KnowledgeForgeError, match="digest mismatch"):
        verify_input_record(record, tmp_path)
```

- [ ] **Step 2: Run the test and confirm failure**

Run: `uv run pytest tests/test_intake.py -v`

Expected: FAIL because the intake module does not exist.

- [ ] **Step 3: Define the shared record interfaces**

```python
# forge/src/knowledge_forge/models.py
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
```

- [ ] **Step 4: Implement verified, atomic intake**

```python
# forge/src/knowledge_forge/intake.py
import os
import shutil
import tempfile
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.hashing import sha256_file
from knowledge_forge.models import InputRecord
from knowledge_forge.paths import require_regular_file, resolve_within

CHUNK_SIZE = 1024 * 1024


def intake_file(
    source_path: Path,
    role: str,
    media_type: str,
    inputs_dir: Path,
) -> InputRecord:
    require_regular_file(source_path, f"input role {role}")
    digest = sha256_file(source_path, CHUNK_SIZE)
    suffix = source_path.suffix.lower()
    target = inputs_dir / f"{digest}{suffix}"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    if target.exists():
        existing_digest = sha256_file(target, CHUNK_SIZE)
        if existing_digest != digest:
            raise KnowledgeForgeError(f"Existing intake digest mismatch for role {role}")
    else:
        handle = tempfile.NamedTemporaryFile(dir=inputs_dir, delete=False)
        temporary_path = Path(handle.name)
        handle.close()
        try:
            shutil.copyfile(source_path, temporary_path)
            copied_digest = sha256_file(temporary_path, CHUNK_SIZE)
            if copied_digest != digest:
                raise KnowledgeForgeError(f"Copied intake digest mismatch for role {role}")
            os.replace(temporary_path, target)
        finally:
            if temporary_path.exists():
                temporary_path.unlink()
    return {
        "role": role,
        "media_type": media_type,
        "sha256": digest,
        "size_bytes": target.stat().st_size,
        "stored_path": target.relative_to(inputs_dir.parent).as_posix(),
    }


def verify_input_record(record: InputRecord, workspace_root: Path) -> None:
    stored_path = resolve_within(workspace_root, Path(record["stored_path"]))
    require_regular_file(stored_path, f"stored input role {record['role']}")
    if stored_path.stat().st_size != record["size_bytes"]:
        raise KnowledgeForgeError(f"Stored input size mismatch for role {record['role']}")
    if sha256_file(stored_path, CHUNK_SIZE) != record["sha256"]:
        raise KnowledgeForgeError(f"Stored input digest mismatch for role {record['role']}")


def upsert_input_record(
    records: list[InputRecord],
    record: InputRecord,
) -> list[InputRecord]:
    retained = [item for item in records if item["role"] != record["role"]]
    existing = [item for item in records if item["role"] == record["role"]]
    if existing and existing[0]["sha256"] != record["sha256"]:
        raise KnowledgeForgeError(f"Input role already has a different digest: {record['role']}")
    return sorted([*retained, record], key=lambda item: item["role"])
```

- [ ] **Step 5: Run intake tests**

Run: `uv run pytest tests/test_intake.py -v`

Expected: two tests PASS.

- [ ] **Step 6: Commit private intake**

```powershell
git add forge/src/knowledge_forge/models.py forge/src/knowledge_forge/intake.py tests/test_intake.py
git commit -m "feat: add verified private intake"
```

### Task 4: Extract EPUB documents in structural order

**Files:**
- Create: `forge/src/knowledge_forge/epub.py`
- Test: `tests/test_epub.py`

**Interfaces:**
- Consumes: `InputRecord`, `sha256_file`, canonical JSONL writer.
- Produces: `extract_epub(epub_path: Path, input_sha256: str) -> list[ExtractedDocument]`.
- Ordering contract: returned documents are sorted by zero-based OPF spine index; non-spine assets, scripts, styles, navigation chrome, and empty documents are excluded.

- [ ] **Step 1: Write a real minimal EPUB integration fixture and failing test**

```python
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


def test_extract_epub_uses_spine_order_and_ignores_script(tmp_path: Path) -> None:
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
```

- [ ] **Step 2: Run the EPUB test and confirm failure**

Run: `uv run pytest tests/test_epub.py -v`

Expected: FAIL because `knowledge_forge.epub` does not exist.

- [ ] **Step 3: Implement safe spine discovery**

```python
# first part of forge/src/knowledge_forge/epub.py
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
            raise KnowledgeForgeError(f"EPUB member exceeds safety limit: {member.filename}")
        if (
            member.file_size > 1024 * 1024
            and member.compress_size > 0
            and member.file_size / member.compress_size > MAX_COMPRESSION_RATIO
        ):
            raise KnowledgeForgeError(f"EPUB member compression ratio is unsafe: {member.filename}")


def _safe_member(name: str) -> str:
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
    }
    opf_dir = posixpath.dirname(opf_path)
    paths: list[str] = []
    for itemref in package.findall(".//{*}spine/{*}itemref"):
        href = manifest.get(itemref.attrib.get("idref", ""))
        if href is not None:
            paths.append(_safe_member(posixpath.normpath(posixpath.join(opf_dir, href))))
    if not paths:
        raise KnowledgeForgeError("EPUB spine contains no XHTML documents")
    return paths
```

- [ ] **Step 4: Implement deterministic XHTML-to-text extraction**

```python
# second part of forge/src/knowledge_forge/epub.py
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
                parser.feed(archive.read(logical_path).decode("utf-8"))
                text = parser.text()
                if text:
                    identity = hashlib.sha256(
                        f"{input_sha256}\n{logical_path}".encode("utf-8")
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
```

- [ ] **Step 5: Run the EPUB tests twice**

Run: `uv run pytest tests/test_epub.py -v && uv run pytest tests/test_epub.py -v`

Expected: both positive and safety-limit tests PASS on both runs with identical assertions.

- [ ] **Step 6: Commit EPUB extraction**

```powershell
git add forge/src/knowledge_forge/epub.py tests/test_epub.py
git commit -m "feat: extract epub spine deterministically"
```

### Task 5: Add the independent PDF probe

**Files:**
- Create: `forge/src/knowledge_forge/pdf_probe.py`
- Test: `tests/test_pdf_probe.py`

**Interfaces:**
- Produces: `probe_pdf(pdf_path: Path, input_sha256: str, limits: PdfLimits) -> PdfProbe`.
- Produces: `DEFAULT_PDF_LIMITS = {"max_bytes": 268435456, "max_pages": 2000, "max_text_chars": 50000000}`.
- The probe records no metadata strings and no page text; it stores only counts, encryption state, and the SHA-256 of normalized extracted text.

- [ ] **Step 1: Write PDF probe tests using real generated PDFs**

```python
from pathlib import Path

import pytest
from pypdf import PdfWriter

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.pdf_probe import DEFAULT_PDF_LIMITS, probe_pdf


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
```

- [ ] **Step 2: Run the test and confirm failure**

Run: `uv run pytest tests/test_pdf_probe.py -v`

Expected: FAIL because `knowledge_forge.pdf_probe` does not exist.

- [ ] **Step 3: Implement the PDF probe**

```python
# forge/src/knowledge_forge/pdf_probe.py
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
        "text_sha256": hashlib.sha256(normalized_text.encode("utf-8")).hexdigest(),
    }
```

- [ ] **Step 4: Run PDF probe tests**

Run: `uv run pytest tests/test_pdf_probe.py -v`

Expected: four tests PASS.

- [ ] **Step 5: Commit PDF probing**

```powershell
git add forge/src/knowledge_forge/pdf_probe.py tests/test_pdf_probe.py
git commit -m "feat: add independent pdf probe"
```

### Task 6: Normalize extracted documents into stable units

**Files:**
- Create: `forge/src/knowledge_forge/normalize.py`
- Test: `tests/test_normalize.py`

**Interfaces:**
- Consumes: `list[ExtractedDocument]`.
- Produces: `normalize_text(text: str) -> str`; `normalize_documents(documents: list[ExtractedDocument]) -> list[NormalizedUnit]`.
- Unit identity: first 20 hex characters of SHA-256 over `document_id`, heading, ordinal, and normalized text, prefixed with `unit-`.

- [ ] **Step 1: Write normalization tests**

```python
from knowledge_forge.models import ExtractedDocument
from knowledge_forge.normalize import normalize_documents, normalize_text


def test_normalize_text_stabilizes_unicode_line_endings_and_blank_lines() -> None:
    assert normalize_text("A\u0301\r\n\r\n\r\nB  \r\n") == "Á\n\nB"


def test_normalize_documents_splits_headings_and_is_idempotent() -> None:
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
```

- [ ] **Step 2: Run the tests and confirm failure**

Run: `uv run pytest tests/test_normalize.py -v`

Expected: FAIL because `knowledge_forge.normalize` does not exist.

- [ ] **Step 3: Implement stable text normalization and segmentation**

```python
# forge/src/knowledge_forge/normalize.py
import hashlib
import re
import unicodedata

from knowledge_forge.models import ExtractedDocument, NormalizedUnit

HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+)$")


def normalize_text(text: str) -> str:
    normalized = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
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
    return [
        (heading, normalize_text("\n".join(lines)))
        for heading, lines in sections
        if normalize_text("\n".join(lines))
    ]


def normalize_documents(
    documents: list[ExtractedDocument],
) -> list[NormalizedUnit]:
    units: list[NormalizedUnit] = []
    for document in sorted(documents, key=lambda item: item["spine_index"]):
        for ordinal, (heading, text) in enumerate(_sections(document["text"])):
            identity_payload = (
                f"{document['document_id']}\n{heading}\n{ordinal}\n{text}"
            ).encode("utf-8")
            content_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
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
```

- [ ] **Step 4: Run normalization tests**

Run: `uv run pytest tests/test_normalize.py -v`

Expected: two tests PASS.

- [ ] **Step 5: Commit normalization**

```powershell
git add forge/src/knowledge_forge/normalize.py tests/test_normalize.py
git commit -m "feat: normalize extracted knowledge units"
```

### Task 7: Add machine-readable contracts and private provenance

**Files:**
- Create: `forge/schemas/input-record.schema.json`
- Create: `forge/schemas/extracted-document.schema.json`
- Create: `forge/schemas/pdf-probe.schema.json`
- Create: `forge/schemas/normalized-unit.schema.json`
- Create: `forge/schemas/provenance-ledger.schema.json`
- Create: `forge/src/knowledge_forge/contracts.py`
- Create: `forge/src/knowledge_forge/provenance.py`
- Test: `tests/test_contracts.py`
- Test: `tests/test_provenance.py`

**Interfaces:**
- Produces: `validate_record(schema_path: Path, record: object, label: str) -> None`.
- Produces: `build_provenance_ledger(inputs: list[InputRecord], documents: list[ExtractedDocument], units: list[NormalizedUnit], pdf_probe: PdfProbe) -> dict[str, object]`.
- Ledger keys are exactly: `schema_version`, `inputs`, `documents`, `units`, `pdf_probe`; records are sorted deterministically.

- [ ] **Step 1: Create the five Draft 2020-12 schemas**

Each schema must set `"$schema": "https://json-schema.org/draft/2020-12/schema"`, `"type": "object"`, `"additionalProperties": false`, and an `$id` under `https://knowledge-forge.local/schemas/<filename>`. Use the following exact required properties:

```text
input-record: role:string, media_type:string, sha256:^[0-9a-f]{64}$,
              size_bytes:integer minimum 0, stored_path:string pattern ^inputs/
extracted-document: document_id:^doc-[0-9a-f]{20}$,
                    input_sha256:^[0-9a-f]{64}$, spine_index:integer minimum 0,
                    logical_path:string, text:string minLength 1
pdf-probe: input_sha256:^[0-9a-f]{64}$, page_count:integer minimum 1,
           encrypted:boolean const false, text_char_count:integer minimum 0,
           text_sha256:^[0-9a-f]{64}$
normalized-unit: unit_id:^unit-[0-9a-f]{20}$, document_id:string,
                 ordinal:integer minimum 0, heading:string minLength 1,
                 text:string minLength 1, content_sha256:^[0-9a-f]{64}$
provenance-ledger: schema_version:integer const 1, inputs:array,
                   documents:array, units:array, pdf_probe:object
```

The ledger schema must use local `$ref` values for the four record schemas, and the validator must load them from `forge/schemas` without network access.

- [ ] **Step 2: Write failing contract tests**

```python
from pathlib import Path

import pytest

from knowledge_forge.contracts import validate_record
from knowledge_forge.errors import KnowledgeForgeError


SCHEMA_DIR = Path(__file__).parents[1] / "forge" / "schemas"


def test_valid_input_record_passes() -> None:
    validate_record(
        SCHEMA_DIR / "input-record.schema.json",
        {
            "role": "primary-text",
            "media_type": "application/epub+zip",
            "sha256": "a" * 64,
            "size_bytes": 10,
            "stored_path": f"inputs/{'a' * 64}.epub",
        },
        "input record",
    )


def test_unknown_property_fails() -> None:
    with pytest.raises(KnowledgeForgeError, match="unexpected"):
        validate_record(
            SCHEMA_DIR / "input-record.schema.json",
            {
                "role": "primary-text",
                "media_type": "application/epub+zip",
                "sha256": "a" * 64,
                "size_bytes": 10,
                "stored_path": f"inputs/{'a' * 64}.epub",
                "unexpected": True,
            },
            "input record",
        )
```

- [ ] **Step 3: Implement local-only schema validation**

```python
# forge/src/knowledge_forge/contracts.py
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from knowledge_forge.errors import KnowledgeForgeError
from knowledge_forge.io import read_json


def _schema_registry(schema_dir: Path) -> Registry:
    registry = Registry()
    for candidate in sorted(schema_dir.glob("*.schema.json")):
        schema = read_json(candidate)
        schema_id = schema.get("$id")
        if not isinstance(schema_id, str):
            raise KnowledgeForgeError(f"Schema has no string $id: {candidate.name}")
        registry = registry.with_resource(schema_id, Resource.from_contents(schema))
    return registry


def validate_record(schema_path: Path, record: object, label: str) -> None:
    schema = read_json(schema_path)
    validator = Draft202012Validator(
        schema,
        registry=_schema_registry(schema_path.parent),
    )
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "root"
        raise KnowledgeForgeError(
            f"Schema validation failed for {label} at {location}: {first.message}"
        )
```

- [ ] **Step 4: Write and implement deterministic provenance tests**

```python
def test_provenance_is_sorted_and_complete() -> None:
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
    ledger = build_provenance_ledger(
        inputs,
        documents,
        units,
        pdf_probe,
    )
    assert ledger["schema_version"] == 1
    assert [item["role"] for item in ledger["inputs"]] == [
        "layout-crosscheck",
        "primary-text",
    ]
    assert ledger["units"][0]["unit_id"].startswith("unit-")
```

```python
# forge/src/knowledge_forge/provenance.py
from knowledge_forge.models import (
    ExtractedDocument,
    InputRecord,
    NormalizedUnit,
    PdfProbe,
)


def build_provenance_ledger(
    inputs: list[InputRecord],
    documents: list[ExtractedDocument],
    units: list[NormalizedUnit],
    pdf_probe: PdfProbe,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "inputs": sorted(inputs, key=lambda item: item["role"]),
        "documents": sorted(documents, key=lambda item: item["spine_index"]),
        "units": sorted(
            units,
            key=lambda item: (item["document_id"], item["ordinal"]),
        ),
        "pdf_probe": pdf_probe,
    }
```

- [ ] **Step 5: Run contract and provenance tests**

Run: `uv run pytest tests/test_contracts.py tests/test_provenance.py -v`

Expected: all schema positive/negative cases and deterministic ledger tests PASS.

- [ ] **Step 6: Commit contracts and provenance**

```powershell
git add forge/schemas forge/src/knowledge_forge/contracts.py forge/src/knowledge_forge/provenance.py tests/test_contracts.py tests/test_provenance.py
git commit -m "feat: validate private provenance contracts"
```

### Task 8: Assemble the fail-closed command-line pipeline

**Files:**
- Create: `forge/src/knowledge_forge/verify.py`
- Create: `forge/src/knowledge_forge/cli.py`
- Create: `forge/src/knowledge_forge/__main__.py`
- Test: `tests/test_cli_foundation.py`

**Interfaces:**
- Produces CLI subcommands: `intake`, `extract-epub`, `probe-pdf`, `normalize`, `verify-foundation`.
- Produces: `verify_foundation(workspace_root: Path, schema_dir: Path, registry_path: Path, documents_path: Path, probe_path: Path, units_path: Path, ledger_path: Path) -> None`.
- Exit contract: success `0`; known invariant failure `2` with one content-safe stderr line; unexpected exceptions propagate with non-zero status and are not hidden.

- [ ] **Step 1: Write an end-to-end CLI test using generated EPUB and PDF files**

The test must call `knowledge_forge.cli.run()` once per subcommand with explicit paths, then assert:

```python
assert registry_path.is_file()
assert documents_path.is_file()
assert probe_path.is_file()
assert units_path.is_file()
assert ledger_path.is_file()
assert not (workspace / "pack").exists()
assert run(["verify-foundation", *verify_arguments]) == 0
```

The test must run `intake` twice and assert the registry bytes remain identical.

- [ ] **Step 2: Run the CLI test and confirm failure**

Run: `uv run pytest tests/test_cli_foundation.py -v`

Expected: FAIL because the CLI and verifier do not exist.

- [ ] **Step 3: Implement the foundation verifier**

`verify_foundation` must perform these checks in this exact order and stop at the first failure:

1. load and schema-validate every input record;
2. verify every content-addressed input size and SHA-256;
3. load and validate every extracted document;
4. require unique document IDs and contiguous spine indices;
5. load and validate the PDF probe;
6. load and validate every normalized unit;
7. require unique unit IDs and existing document IDs;
8. load and validate the provenance ledger;
9. compare ledger records to current registry/documents/probe/units for exact equality;
10. fail if `pack/` exists or contains any file during this foundation slice.

The implementation must use `KnowledgeForgeError` messages such as `Duplicate normalized unit ID: unit-...` and `Provenance ledger does not match normalized units`; it must not print absolute paths or extracted text.

```python
# forge/src/knowledge_forge/verify.py
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


def _require_unique(
    values: list[str],
    label: str,
) -> None:
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
    for record in inputs:
        validate_record(schema_dir / "input-record.schema.json", record, "input record")
        verify_input_record(record, workspace_root)

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

    probe = cast(PdfProbe, read_json(probe_path))
    validate_record(schema_dir / "pdf-probe.schema.json", probe, "PDF probe")

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
```

- [ ] **Step 4: Implement explicit CLI parsing and dispatch**

```python
# forge/src/knowledge_forge/__main__.py
from knowledge_forge.cli import main

raise SystemExit(main())
```

```python
import argparse
import sys
from pathlib import Path

from knowledge_forge.errors import KnowledgeForgeError


def _add_workspace(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument("--workspace", type=Path, required=True)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="knowledge-forge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    intake_parser = subparsers.add_parser("intake")
    _add_workspace(intake_parser)
    intake_parser.add_argument("--role", required=True)
    intake_parser.add_argument("--media-type", required=True)
    intake_parser.add_argument("--source", type=Path, required=True)
    intake_parser.add_argument("--registry", type=Path, required=True)

    epub_parser = subparsers.add_parser("extract-epub")
    _add_workspace(epub_parser)
    epub_parser.add_argument("--role", required=True)
    epub_parser.add_argument("--registry", type=Path, required=True)
    epub_parser.add_argument("--documents", type=Path, required=True)

    pdf_parser = subparsers.add_parser("probe-pdf")
    _add_workspace(pdf_parser)
    pdf_parser.add_argument("--role", required=True)
    pdf_parser.add_argument("--registry", type=Path, required=True)
    pdf_parser.add_argument("--probe", type=Path, required=True)

    normalize_parser = subparsers.add_parser("normalize")
    _add_workspace(normalize_parser)
    normalize_parser.add_argument("--documents", type=Path, required=True)
    normalize_parser.add_argument("--units", type=Path, required=True)
    normalize_parser.add_argument("--registry", type=Path, required=True)
    normalize_parser.add_argument("--probe", type=Path, required=True)
    normalize_parser.add_argument("--ledger", type=Path, required=True)

    verify_parser = subparsers.add_parser("verify-foundation")
    _add_workspace(verify_parser)
    verify_parser.add_argument("--schemas", type=Path, required=True)
    verify_parser.add_argument("--registry", type=Path, required=True)
    verify_parser.add_argument("--documents", type=Path, required=True)
    verify_parser.add_argument("--probe", type=Path, required=True)
    verify_parser.add_argument("--units", type=Path, required=True)
    verify_parser.add_argument("--ledger", type=Path, required=True)
    return parser


def _load_registry(path: Path) -> list[InputRecord]:
    payload = read_json(path)
    if not isinstance(payload, list):
        raise KnowledgeForgeError("Input registry root must be an array")
    return cast(list[InputRecord], payload)


def _record_for_role(records: list[InputRecord], role: str) -> InputRecord:
    matches = [record for record in records if record["role"] == role]
    if len(matches) != 1:
        raise KnowledgeForgeError(f"Input role must resolve exactly once: {role}")
    return matches[0]


def _dispatch(namespace: argparse.Namespace) -> int:
    workspace_root = namespace.workspace.resolve()
    if namespace.command == "intake":
        registry_path = resolve_within(workspace_root, namespace.registry)
        records = _load_registry(registry_path) if registry_path.exists() else []
        record = intake_file(
            namespace.source,
            namespace.role,
            namespace.media_type,
            resolve_within(workspace_root, Path("inputs")),
        )
        write_json_atomic(registry_path, upsert_input_record(records, record))
        return 0
    if namespace.command == "extract-epub":
        registry = _load_registry(resolve_within(workspace_root, namespace.registry))
        record = _record_for_role(registry, namespace.role)
        source_path = resolve_within(workspace_root, Path(record["stored_path"]))
        documents = extract_epub(source_path, record["sha256"])
        write_jsonl_atomic(
            resolve_within(workspace_root, namespace.documents),
            cast(list[dict[str, object]], documents),
        )
        return 0
    if namespace.command == "probe-pdf":
        registry = _load_registry(resolve_within(workspace_root, namespace.registry))
        record = _record_for_role(registry, namespace.role)
        source_path = resolve_within(workspace_root, Path(record["stored_path"]))
        probe = probe_pdf(source_path, record["sha256"], DEFAULT_PDF_LIMITS)
        write_json_atomic(resolve_within(workspace_root, namespace.probe), probe)
        return 0
    if namespace.command == "normalize":
        documents = cast(
            list[ExtractedDocument],
            read_jsonl(resolve_within(workspace_root, namespace.documents)),
        )
        units = normalize_documents(documents)
        units_path = resolve_within(workspace_root, namespace.units)
        write_jsonl_atomic(units_path, cast(list[dict[str, object]], units))
        registry = _load_registry(resolve_within(workspace_root, namespace.registry))
        probe = cast(PdfProbe, read_json(resolve_within(workspace_root, namespace.probe)))
        ledger = build_provenance_ledger(registry, documents, units, probe)
        write_json_atomic(resolve_within(workspace_root, namespace.ledger), ledger)
        return 0
    if namespace.command == "verify-foundation":
        verify_foundation(
            workspace_root,
            resolve_within(workspace_root, namespace.schemas),
            resolve_within(workspace_root, namespace.registry),
            resolve_within(workspace_root, namespace.documents),
            resolve_within(workspace_root, namespace.probe),
            resolve_within(workspace_root, namespace.units),
            resolve_within(workspace_root, namespace.ledger),
        )
        return 0
    raise KnowledgeForgeError(f"Unsupported command: {namespace.command}")


def run(arguments: list[str]) -> int:
    namespace = _parser().parse_args(arguments)
    try:
        return _dispatch(namespace)
    except KnowledgeForgeError as error:
        print(f"knowledge-forge: {error}", file=sys.stderr)
        return 2


def main() -> int:
    return run(sys.argv[1:])
```

The actual `cli.py` imports `cast` from `typing`, every record type from `models`, `DEFAULT_PDF_LIMITS`, and the exact task interfaces referenced in `_dispatch`; no dynamic imports or fallback command paths are allowed.

Tests call `run([...])`; the console script and `__main__.py` call `main()`.

- [ ] **Step 5: Add required arguments to each subcommand**

```text
intake: --role, --media-type, --source, --registry
extract-epub: --role, --registry, --documents
probe-pdf: --role, --registry, --probe
normalize: --documents, --units, --registry, --probe, --ledger
verify-foundation: --schemas, --registry, --documents, --probe, --units, --ledger
```

Every path except `--source` must be workspace-relative and pass through `resolve_within`. The absolute source path is used only during intake and is never persisted.

- [ ] **Step 6: Generate the ledger during normalization**

After writing normalized units, the `normalize` command must load the current registry and PDF probe, build the provenance ledger, validate it, and atomically write it to the explicit `--ledger` path. A missing registry or probe is a hard error.

- [ ] **Step 7: Run CLI integration and full tests**

Run: `uv run pytest tests/test_cli_foundation.py -v && uv run pytest -v`

Expected: CLI test PASS, then the complete suite PASS.

- [ ] **Step 8: Commit the executable foundation**

```powershell
git add forge/src/knowledge_forge/verify.py forge/src/knowledge_forge/cli.py forge/src/knowledge_forge/__main__.py tests/test_cli_foundation.py
git commit -m "feat: assemble fail-closed forge foundation"
```

### Task 9: Validate the foundation against the approved local inputs

**Files:**
- Modify only if a verified defect is found: files introduced by Tasks 1-8.
- Generate, Git-ignored: `inputs/**`, `private/provenance/**`, `work/extracted/**`, `work/normalized/**`, `derived/pdf-review/**`.

**Interfaces:**
- Consumes the completed CLI and the two approved local input files.
- Produces the accepted private foundation state; no tracked knowledge content and no `pack/` files.

- [ ] **Step 1: Run the narrow quality gates**

Run: `uv sync --locked && uv run ruff check . && uv run pytest -v`

Expected: dependency sync succeeds, Ruff reports no errors, and all tests PASS.

- [ ] **Step 2: Intake the structural text input**

```powershell
$trainingEpubPath = 'C:\Users\littl\Downloads\AI-Agents-in-Depth-en.epub'
uv run knowledge-forge intake --workspace . --role primary-text --media-type application/epub+zip --source $trainingEpubPath --registry private/provenance/input-registry.json
```

Expected: exit `0`; one content-addressed `.epub` exists under `inputs/`; the registry contains no absolute path.

- [ ] **Step 3: Intake the independent PDF cross-check**

```powershell
$trainingPdfPath = 'C:\Users\littl\Downloads\AI-Agents-in-Depth-en.pdf'
uv run knowledge-forge intake --workspace . --role layout-crosscheck --media-type application/pdf --source $trainingPdfPath --registry private/provenance/input-registry.json
```

Expected: exit `0`; one content-addressed `.pdf` exists under `inputs/`; both records validate.

- [ ] **Step 4: Extract, probe, normalize, and verify**

```powershell
uv run knowledge-forge extract-epub --workspace . --role primary-text --registry private/provenance/input-registry.json --documents work/extracted/documents.jsonl
uv run knowledge-forge probe-pdf --workspace . --role layout-crosscheck --registry private/provenance/input-registry.json --probe work/extracted/pdf-probe.json
uv run knowledge-forge normalize --workspace . --documents work/extracted/documents.jsonl --units work/normalized/units.jsonl --registry private/provenance/input-registry.json --probe work/extracted/pdf-probe.json --ledger private/provenance/ledger.json
uv run knowledge-forge verify-foundation --workspace . --schemas forge/schemas --registry private/provenance/input-registry.json --documents work/extracted/documents.jsonl --probe work/extracted/pdf-probe.json --units work/normalized/units.jsonl --ledger private/provenance/ledger.json
```

Expected: every command exits `0`; no `pack/` file is created.

- [ ] **Step 5: Independently compare PDF metadata**

```powershell
$registry = Get-Content private/provenance/input-registry.json -Raw | ConvertFrom-Json
$pdfRecord = $registry | Where-Object role -eq 'layout-crosscheck'
$storedPdfPath = Join-Path (Get-Location).Path $pdfRecord.stored_path
$pdfInfoExe = 'C:\Users\littl\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdfinfo.exe'
if (-not (Test-Path -LiteralPath $pdfInfoExe -PathType Leaf)) {
  throw "Verified Poppler pdfinfo binary is missing: $pdfInfoExe"
}
$pdfInfo = & $pdfInfoExe $storedPdfPath
if ($LASTEXITCODE -ne 0) { throw 'pdfinfo failed for the stored PDF intake' }
$pdfInfo
```

Expected: `Pages` equals `399` and equals `page_count` in `work/extracted/pdf-probe.json`; encryption is `no`, page size is A4, and file size is `10198673` bytes.

- [ ] **Step 6: Render and visually inspect representative PDF pages**

```powershell
$probe = Get-Content work/extracted/pdf-probe.json -Raw | ConvertFrom-Json
$reviewDir = 'derived/pdf-review'
New-Item -ItemType Directory -Force -Path $reviewDir | Out-Null
$pdftoppmExe = 'C:\Users\littl\.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
if (-not (Test-Path -LiteralPath $pdftoppmExe -PathType Leaf)) {
  throw "Verified Poppler pdftoppm binary is missing: $pdftoppmExe"
}
$reviewPages = @(1, [Math]::Ceiling($probe.page_count / 2), $probe.page_count) |
  Sort-Object -Unique
foreach ($page in $reviewPages) {
  $prefix = Join-Path $reviewDir ("page-{0:D4}" -f $page)
  & $pdftoppmExe -f $page -l $page -singlefile -png $storedPdfPath $prefix
  if ($LASTEXITCODE -ne 0) { throw "pdftoppm failed for page $page" }
}
```

Inspect every resulting PNG with the local image viewer and record pass/fail for readable text, intact figures, and correct page boundaries. This is a cross-check only; rendered images do not enter normalized text or `pack/`.

- [ ] **Step 7: Prove byte-for-byte idempotence**

```powershell
function Invoke-FoundationPipeline {
  uv run knowledge-forge extract-epub --workspace . --role primary-text --registry private/provenance/input-registry.json --documents work/extracted/documents.jsonl
  if ($LASTEXITCODE -ne 0) { throw 'extract-epub failed' }
  uv run knowledge-forge probe-pdf --workspace . --role layout-crosscheck --registry private/provenance/input-registry.json --probe work/extracted/pdf-probe.json
  if ($LASTEXITCODE -ne 0) { throw 'probe-pdf failed' }
  uv run knowledge-forge normalize --workspace . --documents work/extracted/documents.jsonl --units work/normalized/units.jsonl --registry private/provenance/input-registry.json --probe work/extracted/pdf-probe.json --ledger private/provenance/ledger.json
  if ($LASTEXITCODE -ne 0) { throw 'normalize failed' }
  uv run knowledge-forge verify-foundation --workspace . --schemas forge/schemas --registry private/provenance/input-registry.json --documents work/extracted/documents.jsonl --probe work/extracted/pdf-probe.json --units work/normalized/units.jsonl --ledger private/provenance/ledger.json
  if ($LASTEXITCODE -ne 0) { throw 'verify-foundation failed' }
}

$artifactPaths = @(
  'work/extracted/documents.jsonl',
  'work/extracted/pdf-probe.json',
  'work/normalized/units.jsonl',
  'private/provenance/ledger.json'
)
$before = Get-FileHash -LiteralPath $artifactPaths -Algorithm SHA256
Invoke-FoundationPipeline
$after = Get-FileHash -LiteralPath $artifactPaths -Algorithm SHA256
$differences = Compare-Object $before.Hash $after.Hash
if ($differences) { throw "Foundation outputs changed on identical rerun: $differences" }
```

Expected: `Compare-Object` prints no differences.

- [ ] **Step 8: Prove tamper detection without touching approved inputs**

Run: `uv run pytest tests/test_intake.py::test_verify_input_detects_tampering -v`

Expected: PASS because the test observes the required explicit digest-mismatch exception while touching only its pytest-managed temporary copy; the approved intake files remain unchanged.

- [ ] **Step 9: Verify the Git and export boundary**

```powershell
git check-ignore inputs/* private/provenance/* work/extracted/* work/normalized/* derived/pdf-review/*
git status --short
git diff --check
```

Expected: every private/generated path is reported as ignored; tracked changes are limited to planned source, schema, test, lock, spec, and plan files; no `pack/` artifact, secret, input content, or generated binary appears.

- [ ] **Step 10: Run the final foundation gate**

Run: `uv run ruff check . && uv run pytest -v && uv run knowledge-forge verify-foundation --workspace . --schemas forge/schemas --registry private/provenance/input-registry.json --documents work/extracted/documents.jsonl --probe work/extracted/pdf-probe.json --units work/normalized/units.jsonl --ledger private/provenance/ledger.json`

Expected: all three checks PASS in sequence.

- [ ] **Step 11: Review the complete diff and commit the verified slice**

```powershell
git diff --stat feature...HEAD
git diff --check feature...HEAD
git status --short
git add .gitignore pyproject.toml uv.lock forge tests docs/superpowers/specs/2026-08-02-portable-agent-knowledge-forge-design.md docs/superpowers/plans/2026-08-02-knowledge-forge-foundation.md
git commit -m "feat: complete knowledge forge foundation"
```

Before committing, explicitly confirm that no ignored private path has been force-added and `git diff --cached --name-only` contains no `inputs/`, `private/`, `work/`, `derived/`, `dist/`, `.ua/`, `.env`, PDF, or EPUB file.

## Foundation completion evidence

The implementation handoff must report:

- current branch, HEAD, upstream, worktree, and local-only remote state;
- exact changed-file list;
- input roles, byte sizes, and SHA-256 values without absolute source paths;
- extracted document count and normalized unit count;
- PDF page count and visual-review page numbers;
- idempotence hash comparison result;
- tamper-test result;
- pytest, Ruff, schema, and foundation-verifier pass/fail evidence;
- any semantic or figure coverage not yet addressed, routed explicitly to the v0 or deep-v1 plan.
