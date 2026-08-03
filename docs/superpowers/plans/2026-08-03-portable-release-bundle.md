# M2 Portable Release Bundle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify a deterministic, agent-agnostic ZIP bundle from the validated portable export tree.

**Architecture:** Add a focused `portable_archive` module beside the existing canonical package archiver. It verifies the portable export before writing, archives only the manifest allowlist at the export-root level with fixed ZIP metadata, atomically writes a new destination, and verifies a clean extraction. Add two CLI commands that use the existing workspace path guards; keep GitHub Release publication and canonical package generation outside this slice.

**Tech Stack:** Python 3.10+, standard-library `zipfile`, `pathlib`, `tempfile`, `stat`, and `hashlib`; existing `knowledge_forge.portability.verify_portable_export`, `KnowledgeForgeError`, `pytest`, `uv`, and `ruff`.

**Status:** Implemented and verified.

## Global Constraints

- The input is an existing portable export directory and `export.json` remains the integrity authority.
- Archive members are stored at the export-root level with no wrapper directory.
- Every member uses a normalized POSIX relative path, lexicographic ordering, DOS timestamp `1980-01-01 00:00:00`, Unix regular-file mode `0644`, and `ZIP_STORED`.
- The builder must fail when the destination is an existing file, directory, or symbolic link and must not modify the input export tree.
- The verifier rejects malformed, duplicate, absolute, drive-qualified, backslash, traversal, directory, and symlink members before extraction.
- The ZIP is a derived local artifact under ignored `dist/`; no private input, provenance, absolute path, or generated binary is committed.
- The official Agent Skills validator remains an explicit release gate through `tools/validate_agent_skills.py`; the core library never shells out to it.
- GitHub Release upload is outside M2 and requires a separate publication decision.
- All commands and tests must work on Python 3.10+ and use the repository's `uv` environment.

## File Map

- Create: `forge/src/knowledge_forge/portable_archive.py` — portable-export ZIP construction, safety checks, clean extraction verification, and public library interfaces.
- Modify: `forge/src/knowledge_forge/cli.py:32-45,155-170,373-395` — parser registration, imports, workspace-safe dispatch, and stable success output.
- Create: `tests/test_portable_archive.py` — library contract, deterministic bytes, inventory, tamper, traversal, symlink, and destination tests.
- Modify: `tests/test_cli_package.py:661-end` — CLI argument helpers and success/failure tests for both commands.
- Modify: `exports/README.md` — local build, verify, extraction, and Agent Skills validation instructions.

## Public Interfaces

```python
def build_portable_bundle(
    export_root: Path,
    bundle_path: Path,
) -> dict[str, object]:
    """Verify, atomically build, and re-verify a portable export ZIP."""


def verify_portable_bundle(bundle_path: Path) -> dict[str, object]:
    """Verify a portable export ZIP and return its extracted export manifest."""
```

Both functions raise `KnowledgeForgeError` with a specific message on invalid
input, unsafe ZIP content, destination collisions, or verification failure.

---

### Task 1: Add failing library contract tests

**Files:**
- Create: `tests/test_portable_archive.py`

**Interfaces:**
- Consumes: existing `exports/portable-exports-v10/` and
  `knowledge_forge.portable_archive` public interfaces defined above.
- Produces: executable expectations for the library implementation in Task 2.

- [ ] **Step 1: Add test fixtures and the successful round-trip test**

```python
ROOT = Path(__file__).parents[1]
EXPORT_ROOT = ROOT / "exports" / "portable-exports-v10"


def test_build_portable_bundle_round_trips_manifest_and_root_layout(tmp_path: Path) -> None:
    bundle_path = tmp_path / "portable-exports-v10.zip"

    manifest = build_portable_bundle(EXPORT_ROOT, bundle_path)

    assert manifest["kind"] == "portable-agent-exports"
    assert verify_portable_bundle(bundle_path)["export_sha256"] == manifest["export_sha256"]
    with ZipFile(bundle_path) as archive:
        names = archive.namelist()
    declared = [entry["path"] for entry in manifest["files"]]
    assert names == sorted([*declared, "export.json"])
    assert all("/" in name or name == "export.json" for name in names)
```

- [ ] **Step 2: Add deterministic metadata and byte-identity tests**

```python
def test_build_portable_bundle_is_byte_identical(tmp_path: Path) -> None:
    first = tmp_path / "first.zip"
    second = tmp_path / "second.zip"

    build_portable_bundle(EXPORT_ROOT, first)
    build_portable_bundle(EXPORT_ROOT, second)

    assert first.read_bytes() == second.read_bytes()


def test_build_portable_bundle_uses_store_mode_and_fixed_metadata(tmp_path: Path) -> None:
    bundle_path = tmp_path / "portable.zip"
    build_portable_bundle(EXPORT_ROOT, bundle_path)

    with ZipFile(bundle_path) as archive:
        assert [info.filename for info in archive.infolist()] == sorted(
            info.filename for info in archive.infolist()
        )
        assert {info.compress_type for info in archive.infolist()} == {ZIP_STORED}
        assert {info.date_time for info in archive.infolist()} == {
            (1980, 1, 1, 0, 0, 0)
        }
        assert {info.external_attr >> 16 for info in archive.infolist()} == {
            (stat.S_IFREG | 0o644)
        }
```

- [ ] **Step 3: Add unsafe-member and inventory negative tests**

```python
@pytest.mark.parametrize("member", [
    "../escape.txt",
    "/absolute.txt",
    "C:/drive.txt",
    "skill\\escape.txt",
])
def test_verify_portable_bundle_rejects_unsafe_member(tmp_path: Path, member: str) -> None:
    bundle_path = tmp_path / "unsafe.zip"
    with ZipFile(bundle_path, "w", ZIP_DEFLATED) as archive:
        archive.writestr(member, b"blocked")

    with pytest.raises(KnowledgeForgeError, match="unsafe ZIP member"):
        verify_portable_bundle(bundle_path)


def test_verify_portable_bundle_rejects_duplicate_member(tmp_path: Path) -> None:
    bundle_path = tmp_path / "duplicate.zip"
    with ZipFile(bundle_path, "w") as archive:
        archive.writestr("export.json", b"{}")
        archive.writestr("export.json", b"{}")

    with pytest.raises(KnowledgeForgeError, match="duplicate"):
        verify_portable_bundle(bundle_path)
```

- [ ] **Step 4: Add tamper, missing, extra, collision, and symlink tests**

Add these concrete cases:

```python
def test_build_portable_bundle_rejects_tampered_export(tmp_path: Path) -> None:
    export_root = tmp_path / "export"
    copytree(EXPORT_ROOT, export_root)
    (export_root / "rag" / "documents.jsonl").write_text("tampered\n", encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="hash mismatch"):
        build_portable_bundle(export_root, tmp_path / "tampered.zip")


def test_verify_portable_bundle_rejects_missing_and_extra_members(tmp_path: Path) -> None:
    bundle_path = tmp_path / "portable.zip"
    build_portable_bundle(EXPORT_ROOT, bundle_path)
    with ZipFile(bundle_path) as archive:
        members = [(info.filename, archive.read(info)) for info in archive.infolist()]

    missing_path = tmp_path / "missing.zip"
    with ZipFile(missing_path, "w") as archive:
        for name, content in members[:-1]:
            archive.writestr(name, content)
    with pytest.raises(KnowledgeForgeError, match="inventory"):
        verify_portable_bundle(missing_path)

    extra_path = tmp_path / "extra.zip"
    with ZipFile(extra_path, "w") as archive:
        for name, content in members:
            archive.writestr(name, content)
        archive.writestr("extra.txt", b"unexpected")
    with pytest.raises(KnowledgeForgeError, match="inventory"):
        verify_portable_bundle(extra_path)


def test_build_portable_bundle_rejects_existing_destination(tmp_path: Path) -> None:
    bundle_path = tmp_path / "portable.zip"
    bundle_path.write_bytes(b"existing")

    with pytest.raises(KnowledgeForgeError, match="already exists"):
        build_portable_bundle(EXPORT_ROOT, bundle_path)


def test_verify_portable_bundle_rejects_directory_member(tmp_path: Path) -> None:
    bundle_path = tmp_path / "directory.zip"
    with ZipFile(bundle_path, "w") as archive:
        archive.writestr("skill/", b"")

    with pytest.raises(KnowledgeForgeError, match="unsafe ZIP member"):
        verify_portable_bundle(bundle_path)


def test_build_portable_bundle_rejects_symlink_destination(tmp_path: Path) -> None:
    target = tmp_path / "target.zip"
    target.write_bytes(b"target")
    bundle_path = tmp_path / "link.zip"
    try:
        bundle_path.symlink_to(target)
    except OSError:
        pytest.skip("Symlink creation is unavailable")

    with pytest.raises(KnowledgeForgeError, match="symbolic link"):
        build_portable_bundle(EXPORT_ROOT, bundle_path)
```

- [ ] **Step 5: Run the new tests to establish the expected failures**

Run:

```text
uv run pytest -q tests/test_portable_archive.py
```

Expected: collection succeeds and the tests fail because
`knowledge_forge.portable_archive` does not yet exist.

- [ ] **Step 6: Commit the contract tests**

```text
git add tests/test_portable_archive.py
git commit -m "test: specify portable release bundle contract"
```

### Task 2: Implement deterministic portable ZIP construction and verification

**Files:**
- Create: `forge/src/knowledge_forge/portable_archive.py`

**Interfaces:**
- Consumes: Task 1 tests, `verify_portable_export`, `read_json`, `sha256_bytes`, and `KnowledgeForgeError`.
- Produces: `build_portable_bundle(export_root, bundle_path)` and `verify_portable_bundle(bundle_path)` returning the verified export manifest.

- [ ] **Step 1: Implement manifest member extraction and ZIP metadata helpers**

Implement `_archive_members(manifest)` to require an array of object entries
with string `path` values, reject duplicates and unsafe paths, add
`export.json`, and return sorted names. Implement `_safe_zip_member(name)` with
`PurePosixPath`, rejecting backslashes, absolute paths, empty names, and any
`..` component. Implement `_zip_info(member)` with timestamp
`(1980, 1, 1, 0, 0, 0)`, `ZIP_STORED`, Unix creator system, and regular-file
mode `0644`.

- [ ] **Step 2: Implement atomic bundle writing**

Implement `_write_bundle(export_root, bundle_path, members)` using a temporary
file in `bundle_path.parent`, `ZipFile(..., ZIP_STORED)`, sorted members, and
`os.replace`. Reject an existing destination, symlink destination, symlink
parent, or non-regular source member before writing. Remove the temporary file
in `finally` and translate filesystem failures into an actionable
`KnowledgeForgeError` without exposing private content.

- [ ] **Step 3: Implement clean-extraction verification**

Implement `verify_portable_bundle` to open the ZIP, reject malformed archives,
duplicate names, unsafe members, directories, symlink modes, non-`ZIP_STORED`
members, non-fixed timestamps, or non-regular modes. Extract every member to a
fresh `TemporaryDirectory` only after those checks, require the extracted
inventory to equal the `export.json` manifest allowlist plus `export.json`, and
call `verify_portable_export` on the extracted root. Return that manifest.

- [ ] **Step 4: Implement the public build function**

Implement `build_portable_bundle` to reject an invalid/symlink export root,
call `verify_portable_export(export_root)` before reading bytes, derive the
member allowlist, write atomically, call `verify_portable_bundle(bundle_path)`,
and return the verified manifest. Do not mutate the export root.

- [ ] **Step 5: Run the library tests and lint**

Run:

```text
uv run pytest -q tests/test_portable_archive.py
uv run ruff check forge/src/knowledge_forge/portable_archive.py tests/test_portable_archive.py
```

Expected: all portable archive tests pass and Ruff reports no violations.

- [ ] **Step 6: Commit the library implementation**

```text
git add forge/src/knowledge_forge/portable_archive.py tests/test_portable_archive.py
git commit -m "feat: add deterministic portable release bundle"
```

### Task 3: Expose build and verify commands through the CLI

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py:32-45,155-170,373-395`
- Modify: `tests/test_cli_package.py:661-end`

**Interfaces:**
- Consumes: Task 2 public functions and existing `resolve_within`, `resolve_existing_directory_within`, and `resolve_regular_within` path guards.
- Produces: `knowledge-forge build-portable-bundle` and `knowledge-forge verify-portable-bundle`.

- [ ] **Step 1: Add CLI parser entries and argument helpers**

Register:

```python
build_portable_bundle_parser = subparsers.add_parser("build-portable-bundle")
_add_workspace(build_portable_bundle_parser)
build_portable_bundle_parser.add_argument("--export", type=Path, required=True)
build_portable_bundle_parser.add_argument("--bundle", type=Path, required=True)

verify_portable_bundle_parser = subparsers.add_parser("verify-portable-bundle")
_add_workspace(verify_portable_bundle_parser)
verify_portable_bundle_parser.add_argument("--bundle", type=Path, required=True)
```

Add `EXPORT_ROOT = ROOT / "exports" / "portable-exports-v10"` and extend the
temporary CLI workspace fixture with
`copytree(EXPORT_ROOT, tmp_path / "exports" / "portable-exports-v10")`.
Add helpers that pass `exports/portable-exports-v10` and
`dist/portable-exports-v10.zip` relative to that workspace.

```python
def _build_portable_bundle_arguments(workspace: Path) -> list[str]:
    return [
        "build-portable-bundle",
        "--workspace",
        str(workspace),
        "--export",
        "exports/portable-exports-v10",
        "--bundle",
        "dist/portable-exports-v10.zip",
    ]


def _verify_portable_bundle_arguments(workspace: Path) -> list[str]:
    return [
        "verify-portable-bundle",
        "--workspace",
        str(workspace),
        "--bundle",
        "dist/portable-exports-v10.zip",
    ]
```

- [ ] **Step 2: Add dispatch and stable JSON success output**

Import the two functions and add dispatch branches. Resolve `--export` as an
existing directory, resolve `--bundle` with `resolve_within` for build, and
with `resolve_regular_within(..., "Portable bundle")` for verify. Print only a
stable summary containing `status`, `kind`, `export_sha256`, and the declared
member count; do not print absolute paths or content.

- [ ] **Step 3: Add CLI success and failure tests**

Add tests with this command shape:

```python
def test_cli_builds_and_verifies_portable_bundle(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    assert run(_build_portable_bundle_arguments(workspace)) == 0
    build_result = json.loads(capsys.readouterr().out)
    assert build_result["status"] == "PASS"
    assert run(_verify_portable_bundle_arguments(workspace)) == 0
    verify_result = json.loads(capsys.readouterr().out)
    assert verify_result["export_sha256"] == build_result["export_sha256"]


def test_cli_reports_portable_bundle_failures(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    missing = _verify_portable_bundle_arguments(workspace)
    assert run(missing) == 2
    assert "knowledge-forge:" in capsys.readouterr().err
    collision = _build_portable_bundle_arguments(workspace)
    assert run(collision) == 0
    capsys.readouterr()
    assert run(collision) == 2
    assert "already exists" in capsys.readouterr().err
```

Cover the tampered ZIP invocation with this test; it returns `2` and reports
`knowledge-forge:` on stderr:

```python
def test_cli_rejects_tampered_portable_bundle(
    tmp_path: Path, capsys: object
) -> None:
    workspace = _workspace(tmp_path)
    assert run(_build_portable_bundle_arguments(workspace)) == 0
    capsys.readouterr()
    bundle_path = workspace / "dist" / "portable-exports-v10.zip"
    bundle_path.write_bytes(bundle_path.read_bytes()[:-1] + b"x")

    assert run(_verify_portable_bundle_arguments(workspace)) == 2
    assert "knowledge-forge:" in capsys.readouterr().err
```

- [ ] **Step 4: Run focused and full CLI tests**

Run:

```text
uv run pytest -q tests/test_cli_package.py tests/test_portable_archive.py
uv run ruff check forge/src/knowledge_forge/cli.py tests/test_cli_package.py
```

Expected: all focused tests pass and Ruff reports no violations.

- [ ] **Step 5: Commit the CLI slice**

```text
git add forge/src/knowledge_forge/cli.py tests/test_cli_package.py
git commit -m "feat: expose portable bundle CLI commands"
```

### Task 4: Document local release artifact production and consumption

**Files:**
- Modify: `exports/README.md`

**Interfaces:**
- Consumes: Task 3 CLI command names and the verified export layout.
- Produces: concise, source-neutral instructions for another runtime to build,
  verify, extract, and validate the bundle.

- [ ] **Step 1: Add the local build and verify commands**

Document these exact commands:

```text
uv run knowledge-forge build-portable-bundle --workspace . --export exports/portable-exports-v10 --bundle dist/portable-exports-v10.zip
uv run knowledge-forge verify-portable-bundle --workspace . --bundle dist/portable-exports-v10.zip
```

State that extraction yields `export.json`, `skill/`, `rag/`, and `graph/` at
the destination root, and that the ZIP is a derived local artifact.

- [ ] **Step 2: Add the Agent Skills release gate**

Document extracting the ZIP to a temporary directory and running:

```text
uv run python tools/validate_agent_skills.py <extracted-bundle>/skill
```

Retain the existing manifest digest and profile descriptions without adding
external provenance or vendor-specific runtime instructions.

- [ ] **Step 3: Review the documentation diff and commit it**

Run `git diff --check`, then:

```text
git add exports/README.md
git commit -m "docs: document portable release bundle"
```

### Task 5: Run the complete M2 verification gate

**Files:**
- No new files; inspect the full diff and generated ignored artifacts only.

**Interfaces:**
- Consumes: Tasks 1–4 and the current `feature` baseline.
- Produces: verified local `dist/portable-exports-v10.zip`, test evidence, and
  a clean `dev-m2-portable-release` worktree ready for review and publication.

- [ ] **Step 1: Build and verify the release bundle twice**

Run the CLI build to `dist/portable-exports-v10-a.zip` and
`dist/portable-exports-v10-b.zip`, verify both, then compare their SHA-256
values with PowerShell:

```text
uv run knowledge-forge build-portable-bundle --workspace . --export exports/portable-exports-v10 --bundle dist/portable-exports-v10-a.zip
uv run knowledge-forge build-portable-bundle --workspace . --export exports/portable-exports-v10 --bundle dist/portable-exports-v10-b.zip
uv run knowledge-forge verify-portable-bundle --workspace . --bundle dist/portable-exports-v10-a.zip
uv run knowledge-forge verify-portable-bundle --workspace . --bundle dist/portable-exports-v10-b.zip
Get-FileHash dist/portable-exports-v10-a.zip,dist/portable-exports-v10-b.zip -Algorithm SHA256
```

Expected: both verify commands return `PASS` and both hashes are identical.

- [ ] **Step 2: Run the required repository gates**

Run:

```text
uv run pytest -q
uv run ruff check .
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
```

Expected: the full suite passes, Ruff is clean, and the existing export
verification remains green.

- [ ] **Step 3: Validate the extracted Skill profile**

Extract one verified bundle to a fresh temporary directory and run:

```text
uv run python tools/validate_agent_skills.py <extracted-bundle>/skill
```

Expected: `Valid skill: ...portable-agent-knowledge` and exit code `0`.

- [ ] **Step 4: Review scope and worktree state**

Run the work-state preflight, `git diff --stat`, `git status --short`, and a
staged-boundary review. Confirm only planned tracked files changed and that
`dist/` remains ignored. Do not add the ZIP to Git.

- [ ] **Step 5: Commit the verified M2 slice**

If the prior task commits are present and all gates pass, create the final
integration commit only for any remaining plan/status updates:

```text
git add docs/superpowers/plans/2026-08-03-portable-release-bundle.md
git commit -m "docs: mark portable release bundle plan verified"
```

Then the branch is ready for the normal `dev-m2-portable-release -> feature`
pull request and separate GitHub Release publication decision.

## Plan self-review

- Spec coverage: artifact layout and manifest authority are covered by Tasks 1–2; deterministic metadata and clean extraction by Tasks 1–2; CLI boundaries by Task 3; documentation by Task 4; full gates and Agent Skills validation by Task 5; GitHub publication exclusion is repeated in the global constraints and Task 5.
- Placeholder scan: no TODO, TBD, FIXME, or unspecified “handle appropriately” steps remain.
- Type consistency: both public functions accept `Path` values and return `dict[str, object]` in every task; CLI receives the returned manifest and emits a summary.
