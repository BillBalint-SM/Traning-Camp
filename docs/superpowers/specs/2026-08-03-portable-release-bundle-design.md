# M2 Portable Release Bundle design

## Purpose

Create a public, agent-agnostic ZIP artifact from the already verified portable
knowledge export. The bundle must be importable by extracting it into any
runtime that accepts the `export.json`, `skill/`, `rag/`, and `graph/` layout.
The canonical package and the checked-in export tree remain the source of truth;
the ZIP is a derived release artifact and is never loaded into agent context
automatically.

## Scope

M2 covers one bounded release slice:

- a library builder for a portable export bundle;
- a library verifier that validates the ZIP and a clean extraction;
- CLI commands `build-portable-bundle` and `verify-portable-bundle`;
- deterministic ZIP behavior and negative-path tests;
- documentation for producing and consuming the local artifact.

M2 does not upload a GitHub Release, change the canonical package, regenerate
the knowledge export, or add a vendor-specific adapter. GitHub publication is a
later release gate after the local artifact passes all checks.

## Artifact contract

The input is an existing portable export directory. The builder first runs the
existing portable-export verifier, then archives exactly the files declared by
`export.json` plus `export.json` itself. Archive members are stored at the
export-root level (no extra wrapper directory), so clean extraction produces a
directory accepted directly by `verify_portable_export`.

The output is a caller-selected path such as
`dist/portable-exports-v10.zip`. The builder must fail if the destination is an
existing file, directory, or symbolic link. It writes through a temporary file
in the destination directory and atomically replaces only a new destination.

Every member uses a normalized POSIX relative path, lexicographic ordering, a
fixed DOS timestamp of `1980-01-01 00:00:00`, Unix regular-file mode `0644`, and
`ZIP_STORED`. No host path, source timestamp, symlink, directory entry, or
compression implementation detail may affect the bytes.

## Components and data flow

### `portable_archive` module

Add a small functional module next to the existing package archive module. It
owns only portable-export ZIP concerns:

1. resolve and validate the export root and destination through the existing
   workspace path boundary;
2. call `verify_portable_export` and derive the exact manifest allowlist;
3. write the deterministic ZIP atomically;
4. inspect and verify ZIP inventory, safety properties, extraction, and the
   portable-export manifest.

The canonical `archive.py` contract remains unchanged. Shared ZIP primitives
may be extracted only if the resulting functions have one clear responsibility
and preserve both contracts.

### CLI

`build-portable-bundle` accepts `--workspace`, `--export`, and `--bundle`.
`verify-portable-bundle` accepts `--workspace` and `--bundle`. Both commands
resolve paths relative to the workspace and print a concise success result or a
specific `KnowledgeForgeError`; they do not print private paths or content.

### Verification flow

The verifier must:

- reject malformed ZIPs, duplicate names, absolute paths, drive-qualified
  paths, backslashes, `..` traversal, directories, and symlink entries;
- require the exact member inventory declared by the extracted `export.json`;
- extract into a fresh temporary directory without following links;
- run the existing `verify_portable_export` against the extracted root;
- confirm all ZIP members use the deterministic storage metadata;
- return the export manifest (or a stable summary) for CLI reporting.

The official Agent Skills validator remains an explicit release gate through
`tools/validate_agent_skills.py`; the core library must not shell out to an
optional executable. The M2 verification instructions run that validator on
the extracted `skill/` directory when it is installed.

## Tests and acceptance criteria

Add focused tests for:

- successful build and clean extraction verification;
- exact manifest inventory and root-level layout;
- `ZIP_STORED`, fixed metadata, sorted members, and no directory entries;
- two builds from the same export producing byte-identical ZIPs and SHA-256;
- rejection of ZIP-slip, absolute, backslash, duplicate, directory, symlink,
  tampered, missing, and extra-member cases;
- destination collision and unsafe symlink destination behavior;
- CLI success and actionable failure paths.

The slice is complete only when the following all pass on the merged feature
head:

```text
uv run pytest -q
uv run ruff check .
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
uv run knowledge-forge build-portable-bundle --workspace . --export exports/portable-exports-v10 --bundle dist/portable-exports-v10.zip
uv run knowledge-forge verify-portable-bundle --workspace . --bundle dist/portable-exports-v10.zip
uv run python tools/validate_agent_skills.py <extracted-bundle>/skill
```

The ZIP and any extraction directory are local ignored release artifacts; no
private input, provenance, absolute path, or generated binary is committed.

## Assumptions and decisions

- `export.json` remains the integrity authority; M2 does not introduce a second
  manifest format.
- The ZIP root is the export root, not a nested version directory.
- The first milestone is local deterministic production and verification.
- GitHub Release upload is intentionally separate and requires a fresh
  publication decision after the bundle is reviewed.
- Existing export files are treated as immutable input during a build.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| ZIP produced from an unverified or partial tree | Verify before writing and again after extraction. |
| Cross-platform byte drift | Fixed metadata, sorted POSIX names, `ZIP_STORED`, explicit mode. |
| ZIP-slip or link traversal on import | Reject unsafe names and link entries before extraction. |
| Optional validator missing on a release machine | Keep it as an explicit gate with an actionable install message; do not silently skip it. |
| Accidental public leakage | Archive only the manifest allowlist and keep output under ignored `dist/`. |
