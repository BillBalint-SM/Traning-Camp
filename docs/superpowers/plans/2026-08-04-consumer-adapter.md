# M4 Read-Only Consumer Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a vendor-neutral Python API and explicit CLI boundary that verifies an external portable export, routes and loads deterministic context, and returns a metadata-only integrity receipt without repository-local knowledge imports.

**Architecture:** Compose the existing `verify_portable_export`, `load_portable_context_graph`, and `load_portable_context_budgeted` functions in a focused `consumer.py` module. Preserve the loader context payload unchanged, derive a separate metadata-only receipt from admitted modules, validate the combined result, and write it atomically through an explicit workspace-safe CLI command.

**Tech Stack:** Python 3.10+, existing `pathlib`, canonical JSON I/O, `KnowledgeForgeError`, portable export APIs, `pytest`, `ruff`, `uv`, and the existing setuptools wheel configuration.

**Status:** Implemented locally and verified; uncommitted pending publication approval.

## Global Constraints

- The portable export directory is the only consumer input; do not import `pack/`, `private/`, or repository-local knowledge modules.
- The adapter is read-only: no export mutation, model call, tool execution, MCP/A2A integration, vector database, embedding, GraphRAG global/community layer, or signed provenance.
- `relation_depth` is exactly `0` or `1`; `max_chars` is explicitly `None` or an integer accepted by the existing 1–100000 character budget contract.
- Query text is transient and never serialized; module text appears only in the explicit context payload, never in the nested metadata receipt.
- Ambiguous and not-covered routes fail closed with no admitted modules.
- No new third-party dependency is introduced; Python 3.10+ remains supported.
- Result bytes are canonical and deterministic; output paths are relative, new, workspace-contained, and symlink-free at the CLI boundary.
- Do not create a git commit, push, pull request, merge, or branch deletion without explicit user authorization under the current repository instructions.

---

### Task 1: Establish consumer contract tests

**Files:**
- Create: `tests/test_consumer.py`
- Modify: `tests/test_cli_package.py` only for shared fixture helpers if needed

**Interfaces:**
- Consumes: existing `build_portable_exports`, `load_portable_context_graph`, and `load_portable_context_budgeted` fixtures.
- Produces: failing tests that define `consume_portable_export`, `validate_consumer_result`, and `write_consumer_result` behavior for Task 2.

- [x] **Step 1: Add a copied-export fixture and covered result test**

Build a temporary portable export from `PACK_ROOT` and `SCHEMA_ROOT`, call the
future API with query `Eszközszerződés`, depth `0`, and explicit `None` budget,
then assert `format_version == 1`, `kind == "portable-consumer-result"`, a
covered route, matching export digest, context modules, and a receipt whose
admitted IDs equal the context module IDs.

- [x] **Step 2: Add graph, budget, and fail-closed route tests**

Cover depth `1`, a valid character budget, an ambiguous query, and a query that
is not covered. Assert deterministic expanded IDs/relations, budget omissions,
and empty admitted module sets for the two fail-closed statuses.

- [x] **Step 3: Add receipt privacy and determinism tests**

Serialize two repeated results with `canonical_json_bytes`; assert byte
identity, absence of the raw query and absolute paths, presence of hashes, and
absence of `text` under `result["receipt"]` while allowing text under the
explicit context payload.

- [x] **Step 4: Add tamper, validation, and write-safety tests**

Change the copied export after result creation, alter a receipt hash, pass an
invalid depth/budget, write to an existing output, and use a symlinked output
ancestor where supported. Assert `KnowledgeForgeError` and verify the existing
sentinel file remains unchanged.

- [x] **Step 5: Run the RED slice**

Run:

```text
uv run pytest -q tests/test_consumer.py
```

Expected: collection or test failure because `knowledge_forge.consumer` and
its public functions do not exist yet.

### Task 2: Implement the read-only consumer core

**Files:**
- Create: `forge/src/knowledge_forge/consumer.py`
- Test: `tests/test_consumer.py`

**Interfaces:**
- Consumes: the verified portable export APIs and canonical JSON writer.
- Produces:

```python
def consume_portable_export(
    export_root: Path,
    query: str,
    relation_depth: int,
    max_chars: int | None,
) -> dict[str, object]:
    """Verify, route, load, and return one consumer result."""


def validate_consumer_result(result: dict[str, object]) -> None:
    """Validate result shape and export/receipt invariants."""


def write_consumer_result(output_path: Path, result: dict[str, object]) -> None:
    """Validate and atomically write one canonical consumer result."""
```

- [x] **Step 1: Implement export verification and loader selection**

Validate the query, depth, and explicit budget value. Call
`verify_portable_export(export_root)` first. Use
`load_portable_context_graph(export_root, query, relation_depth)` when
`max_chars is None`; use
`load_portable_context_budgeted(export_root, query, relation_depth, max_chars)`
otherwise. Reject every non-dict or incompatible context before constructing a
result.

- [x] **Step 2: Implement receipt derivation**

Derive `receipt` from the returned context and its `modules`: copy the verified
export digest, relation depth, sorted admitted IDs, sorted omitted IDs, and a
sorted module-ID-to-content-hash map. Compute hashes from each returned UTF-8
module text and reject declared-hash drift. Never copy query text, absolute
paths, relation text, or module text into the receipt.

- [x] **Step 3: Implement semantic result validation**

Require the exact top-level version/kind fields and validate route status,
export digest equality, module containment, omitted/admitted disjointness,
receipt hash set equality, budget bounds, and fail-closed behavior for
ambiguous/not-covered routes. Reject unexpected fields and malformed IDs with
actionable `KnowledgeForgeError` messages.

- [x] **Step 4: Implement atomic, symlink-safe result writing**

Validate first, reject an existing output or symlinked path/ancestor, and call
the repository's `write_json_atomic` with the canonical result. Ensure any
validation error occurs before the output path is created or replaced.

- [x] **Step 5: Run the core slice**

Run:

```text
uv run pytest -q tests/test_consumer.py
uv run ruff check forge/src/knowledge_forge/consumer.py tests/test_consumer.py
```

Expected: all consumer tests pass and Ruff reports no violations.

### Task 3: Add the explicit CLI boundary

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py`
- Modify: `tests/test_cli_package.py`
- Reuse: `forge/src/knowledge_forge/paths.py` `resolve_existing_directory_within` and `resolve_new_file_within`

**Interfaces:**
- Consumes: `consume_portable_export` and `write_consumer_result`.
- Produces: `consume-portable-export --workspace --export --query --depth [--max-chars] --receipt`.

- [x] **Step 1: Register parser arguments**

Add a parser with required `--workspace`, `--export`, `--query`, `--depth`, and
`--receipt`, plus optional integer `--max-chars`. Do not add implicit defaults
to the public Python functions; map an absent CLI option explicitly to
`max_chars=None` in dispatch.

- [x] **Step 2: Implement path-safe dispatch and summary**

Resolve the export as an existing workspace-contained directory and the receipt
as a new workspace-contained file. Call the consumer and writer, then print
canonical JSON containing only `status`, `kind`, `export_sha256`, and
`module_count`. A failed call must return the existing CLI error code `2` and
must not create a result file.

- [x] **Step 3: Add CLI success and negative-path tests**

Use a copied real export and assert depth 0, depth 1, and budgeted success. Add
tests for absolute/escaping/symlink paths, existing output preservation,
invalid depth/budget, and tampered export rejection.

- [x] **Step 4: Run the CLI slice**

Run:

```text
uv run pytest -q tests/test_cli_package.py tests/test_consumer.py
uv run ruff check forge/src/knowledge_forge/cli.py forge/src/knowledge_forge/consumer.py tests/test_cli_package.py tests/test_consumer.py
```

Expected: all focused tests pass and Ruff reports no violations.

### Task 4: Document installation and run the release gate

**Files:**
- Modify: `exports/README.md`
- Test artifact only: `work/m4-wheel/` and a temporary environment outside the repository

**Interfaces:**
- Consumes: the CLI/API from Tasks 2–3 and `exports/portable-exports-v10`.
- Produces: clean-environment import instructions and evidence that the real
  export remains byte-stable.

- [x] **Step 1: Document the consumer quickstart**

Add commands for building a wheel, installing it into a clean temporary
environment, and running the consumer against a copied/exported directory.
State that the portable export is an external input and that the adapter is
read-only; do not describe MCP/A2A as required.

- [x] **Step 2: Run the full local gates**

Run:

```text
uv run ruff check .
uv run pytest -q
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
uv build --wheel --out-dir work/m4-wheel
```

Expected: Ruff clean, all tests pass with normal exit, export verification
passes with the existing digest, and a wheel is produced without changing
tracked export bytes.

- [x] **Step 3: Run the clean temporary-environment smoke**

Create a temporary venv, install the produced wheel, import
`knowledge_forge.consumer`, and consume a copied portable export without the
repository on `PYTHONPATH`. Assert the result kind, export digest, and receipt
hashes, then remove only the explicitly created temporary environment.

- [x] **Step 4: Review the final diff and stop for publication approval**

Run the work-state preflight, `git diff --check`, changed-path review, and
confirm that no `work/` result or wheel is staged. Leave all changes
uncommitted and report the exact verification evidence; request separate user
approval before creating a commit or publishing the dev slice.

## Plan self-review

- Spec coverage: Task 1 covers all positive, negative, privacy, determinism,
  and mutation-safety cases; Task 2 covers composition, receipt derivation,
  semantic validation, and atomic writing; Task 3 covers the CLI boundary and
  workspace paths; Task 4 covers documentation, wheel installation, and full
  export/test gates.
- Placeholder scan: no unfinished placeholder instruction or vague fallback step remains.
- Type consistency: the `max_chars: int | None` contract is used consistently
  by the API, dispatch mapping, tests, and documentation.
- Scope check: no protocol adapter, model runtime, or graph strategy benchmark
  is included in this single bounded slice.
