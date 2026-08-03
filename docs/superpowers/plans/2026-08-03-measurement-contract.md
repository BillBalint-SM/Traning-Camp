# M3 Runtime-Neutral Measurement Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement an explicit metadata-only context trace recorder and export-backed verifier without changing the existing loader APIs.

**Architecture:** Add a focused `measurement.py` module that normalizes existing loader receipts into a closed trace contract, computes query/export/module/trace digests, and writes canonical JSONL atomically. Add a JSON Schema plus semantic Python invariants, then expose explicit `record-context-trace` and `verify-context-trace` commands. The loaders remain read-only and no model, telemetry transport, or answer evaluator is introduced.

**Tech Stack:** Python 3.10+, standard-library `hashlib`, `pathlib`, `typing`, existing `jsonschema` contract validation, canonical JSON/JSONL I/O, `KnowledgeForgeError`, `verify_portable_export`, `pytest`, `uv`, and `ruff`.

**Status:** Implemented and verified.

## Global Constraints

- The trace is a derived metadata-only artifact; the portable export remains the only content authority.
- The query string, module text, model output, credentials, and absolute filesystem paths must never be serialized or emitted in errors.
- The trace JSON Schema is closed with `additionalProperties: false`; incompatible changes require a new format version and fail closed.
- `query_sha256` hashes exact UTF-8 query bytes; `trace_sha256` hashes canonical JSON with its own field removed.
- All ID arrays are sorted and unique; `relation_depth` is `0` or `1`; timing values are nonnegative integer milliseconds.
- `export_sha256` and admitted module hashes must match a verified portable export when export-backed verification runs.
- Existing loader functions remain read-only and are not instrumented automatically.
- Trace writes are atomic; runtime traces are ignored local artifacts under `dist/` or `work/`.
- No new third-party dependency is added; use the repository's existing `uv` environment and Python 3.10+ floor.

## File Map

- Create: `forge/schemas/context-trace.schema.json` — closed JSON Schema for one JSONL record.
- Create: `forge/src/knowledge_forge/measurement.py` — recorder, semantic validators, atomic JSONL writer, and export-backed verifier.
- Modify: `forge/src/knowledge_forge/cli.py:45-55,155-190,300-470` — parser entries, path-safe dispatch, and stable summaries.
- Create: `tests/test_measurement.py` — recorder, schema, privacy, invariant, determinism, and export verification tests.
- Modify: `tests/test_cli_package.py:1-20,760-end` — portable context fixture, CLI argument helpers, and record/verify tests.
- Modify: `exports/README.md` — metadata-only trace usage and verification commands.

## Public Interfaces

```python
def build_context_trace(
    query: str,
    context: dict[str, object],
    relation_depth: int,
    timing_ms: dict[str, int],
) -> dict[str, object]:
    """Create and validate one metadata-only trace record."""


def write_context_traces(
    trace_path: Path,
    records: list[dict[str, object]],
) -> None:
    """Validate and atomically write JSONL trace records."""


def validate_context_trace(record: dict[str, object]) -> None:
    """Validate schema and content-free trace invariants."""


def verify_context_traces(
    trace_path: Path,
    export_root: Path,
) -> list[dict[str, object]]:
    """Validate JSONL records and resolve them against one export."""
```

---

### Task 1: Add schema and failing measurement contract tests

**Files:**
- Create: `forge/schemas/context-trace.schema.json`
- Create: `tests/test_measurement.py`

**Interfaces:**
- Consumes: existing loader result fixtures from `tests/test_portability.py`, `canonical_json_bytes`, and the public interfaces above.
- Produces: the closed record contract and executable expectations for Task 2.

- [x] **Step 1: Add the closed JSON Schema**

Define required top-level fields `format_version`, `kind`, `query_sha256`,
`export_sha256`, `route`, `context`, `module_hashes`, `budget`,
`timing_ms`, and `trace_sha256`. Use lowercase 64-hex digest patterns,
explicit enums for route status, integer bounds for depth/timing/budget, and
`additionalProperties: false` at every object level. Permit only `null` or a
positive integer for `budget.max_chars`.

- [x] **Step 2: Add a valid recorder fixture test**

```python
def test_build_context_trace_is_metadata_only(tmp_path: Path) -> None:
    output_root = tmp_path / "derived" / "portable-exports"
    build_portable_exports(PACK_ROOT, SCHEMA_ROOT, output_root)
    context = load_portable_context_budgeted(
        output_root, "Eszközszerződés", 1, 2000
    )

    trace = build_context_trace(
        "Eszközszerződés", context, 1, {"route": 4, "load": 11, "total": 15}
    )

    validate_context_trace(trace)
    serialized = canonical_json_bytes(trace).decode("utf-8")
    assert "text" not in serialized
    assert "Eszközszerződés" not in serialized
    assert trace["kind"] == "portable-context-trace"
    assert trace["route"]["status"] == "covered"
```

- [x] **Step 3: Add deterministic, status, and privacy tests**

Create plain, graph-depth-1, budgeted, ambiguous, and not-covered contexts.
Build the same trace twice and assert canonical bytes and `trace_sha256` are
identical. Assert ambiguous/not-covered traces have empty admitted and
expanded ID arrays. Recursively inspect serialized output to reject `text`,
raw query, absolute Windows paths, and arbitrary extra keys.

- [x] **Step 4: Add negative invariant tests**

Use `copy.deepcopy(valid_trace)` and mutate one field per test. Cover invalid
status, depth, negative timing, `total < route`, over-budget usage, duplicate
IDs, admitted/omitted overlap, module-hash key drift, bad digest length,
wrong trace digest, extra schema field, and mismatched budget omission IDs.
Each mutation must raise `KnowledgeForgeError` with a field-level message.

- [x] **Step 5: Add JSONL and export-backed verifier tests**

Write one valid record and assert `write_context_traces` creates exactly one
canonical JSONL line. Verify it against the real temporary export, then mutate
`export_sha256`, a module hash, and the trace file path to assert verification
fails. Assert verification does not change bytes in the trace or export.

- [x] **Step 6: Run tests to establish the expected failure**

Run:

```text
uv run pytest -q tests/test_measurement.py
```

Expected: collection succeeds for the schema fixture but fails because
`knowledge_forge.measurement` and the schema do not yet exist.

- [x] **Step 7: Commit schema and contract tests**

```text
git add forge/schemas/context-trace.schema.json tests/test_measurement.py
git commit -m "test: specify metadata-only context trace contract"
```

### Task 2: Implement recorder, semantic validation, and verifier

**Files:**
- Create: `forge/src/knowledge_forge/measurement.py`

**Interfaces:**
- Consumes: Task 1 schema/tests, `validate_record`, `canonical_json_bytes`, `read_jsonl`, `write_jsonl_atomic`, `sha256_bytes`, `verify_portable_export`, and path guards.
- Produces: all four public measurement functions with `dict[str, object]` or `list[dict[str, object]]` return values and `KnowledgeForgeError` failures.

- [x] **Step 1: Implement context normalization and hash helpers**

Implement small single-purpose helpers that validate query non-emptiness,
relation depth, timing keys, route status, sorted unique IDs, and the loader
context shape. Normalize missing plain-context fields to empty expanded,
omitted, and relation collections; normalize a missing budget to
`max_chars: null`, `used_chars: 0`, and an empty omission list. Hash each
admitted module's in-memory text and compare it with its declared
`content_sha256` before discarding the text.

- [x] **Step 2: Implement `build_context_trace`**

Construct the exact record shape from the normalized route/context/budget
values, compute `query_sha256`, sort all arrays and module-hash keys, compute
`trace_sha256` from a copy without that field, and call
`validate_context_trace` before returning. Never include the source context's
`modules` objects or query string.

- [x] **Step 3: Implement schema and semantic validation**

Run `validate_record` against `forge/schemas/context-trace.schema.json`, then
enforce subset, disjointness, route-status, budget, timing, lowercase digest,
trace-digest, and content-free invariants. Error messages must name only the
logical field or invariant.

- [x] **Step 4: Implement atomic JSONL writing**

Validate every record, serialize one canonical JSON object per line, and call
the existing atomic JSONL writer. Reject an empty record list, unsafe/symlink
destination paths, and non-regular existing inputs through existing helpers.

- [x] **Step 5: Implement export-backed verification**

Read the trace JSONL, require at least one object, validate every record,
verify the export once, compare each record's `export_sha256` and every
`module_hashes` entry against the export graph, and return the validated
records. Do not rewrite either input.

- [x] **Step 6: Run focused tests and lint**

Run:

```text
uv run pytest -q tests/test_measurement.py
uv run ruff check forge/src/knowledge_forge/measurement.py tests/test_measurement.py
```

Expected: all measurement tests pass and Ruff reports no violations.

- [x] **Step 7: Commit the measurement implementation**

```text
git add forge/src/knowledge_forge/measurement.py forge/schemas/context-trace.schema.json tests/test_measurement.py
git commit -m "feat: add metadata-only context trace measurement"
```

### Task 3: Add explicit record and verify CLI commands

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py:45-55,155-190,300-470`
- Modify: `tests/test_cli_package.py:1-20,760-end`

**Interfaces:**
- Consumes: Task 2 public functions and existing workspace path guards.
- Produces: `knowledge-forge record-context-trace` and
  `knowledge-forge verify-context-trace` with stable PASS summaries.

- [x] **Step 1: Register parser arguments and test helpers**

Register the exact arguments:

```python
record_trace_parser = subparsers.add_parser("record-context-trace")
_add_workspace(record_trace_parser)
record_trace_parser.add_argument("--context", type=Path, required=True)
record_trace_parser.add_argument("--query", required=True)
record_trace_parser.add_argument("--depth", type=int, required=True)
record_trace_parser.add_argument("--route-ms", type=int, required=True)
record_trace_parser.add_argument("--load-ms", type=int, required=True)
record_trace_parser.add_argument("--total-ms", type=int, required=True)
record_trace_parser.add_argument("--trace", type=Path, required=True)

verify_trace_parser = subparsers.add_parser("verify-context-trace")
_add_workspace(verify_trace_parser)
verify_trace_parser.add_argument("--trace", type=Path, required=True)
verify_trace_parser.add_argument("--export", type=Path, required=True)
```

Add a temporary workspace fixture that copies `exports/portable-exports-v10`
and a valid context JSON generated by an existing loader command/function.

- [x] **Step 2: Implement record dispatch**

Resolve the context as a regular JSON file, read it without printing it, call
`build_context_trace` with the three timing arguments, resolve the new trace
path inside the workspace, write one record, and print only
`{"status":"PASS","trace_sha256":"...","record_count":1}`.

- [x] **Step 3: Implement verify dispatch**

Resolve the trace as a regular file and the export as an existing directory,
call `verify_context_traces`, and print only
`{"status":"PASS","record_count":N,"export_sha256":"..."}`. All
`KnowledgeForgeError` failures must return CLI exit code `2` through the
existing dispatcher.

- [x] **Step 4: Add CLI success and failure tests**

Build a context, record it, parse the summary, verify it against the export,
and assert the matching export digest and record count. Add missing context,
missing trace, tampered trace, export mismatch, absolute-path, and destination
symlink tests; assert exit code `2` and a sanitized `knowledge-forge:` error.

- [x] **Step 5: Run focused CLI tests and lint**

Run:

```text
uv run pytest -q tests/test_cli_package.py tests/test_measurement.py
uv run ruff check forge/src/knowledge_forge/cli.py tests/test_cli_package.py
```

Expected: all focused tests pass and Ruff reports no violations.

- [x] **Step 6: Commit the CLI slice**

```text
git add forge/src/knowledge_forge/cli.py tests/test_cli_package.py
git commit -m "feat: expose context trace CLI commands"
```

### Task 4: Document and complete the measurement gate

**Files:**
- Modify: `exports/README.md`
- Modify: `docs/superpowers/plans/2026-08-03-measurement-contract.md`

**Interfaces:**
- Consumes: Task 3 commands and the verified portable export.
- Produces: local trace quickstart, complete verification evidence, and a clean
  branch ready for PR review.

- [x] **Step 1: Document metadata-only trace usage**

Add exact record and verify commands:

```text
uv run knowledge-forge record-context-trace --workspace . --context work/context.json --query "Eszközszerződés" --depth 1 --route-ms 4 --load-ms 11 --total-ms 15 --trace work/context-traces.jsonl
uv run knowledge-forge verify-context-trace --workspace . --trace work/context-traces.jsonl --export exports/portable-exports-v10
```

State explicitly that query and module text are not stored and that the trace
is only meaningful with the matching export digest.

- [x] **Step 2: Run the complete M3 gate**

Run:

```text
uv run pytest -q
uv run ruff check .
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
```

Then record and verify one real context trace in an ignored `work/` path and
assert that its serialized bytes contain neither the query nor module text.

- [x] **Step 3: Mark the plan verified and review scope**

Update the plan status to `Implemented and verified`, run the work-state
preflight, `git diff --check`, `git diff --stat`, and `git status --short`.
Confirm only planned tracked paths changed and no trace fixture contains raw
content or absolute paths.

- [x] **Step 4: Commit documentation/status and prepare integration**

```text
git add exports/README.md docs/superpowers/plans/2026-08-03-measurement-contract.md
git commit -m "docs: document verified context measurement contract"
```

The clean branch is then ready for the normal `dev-m3-measurement-contract ->
feature` PR, followed by a separately approved feature-to-main promotion.

## Plan self-review

- Spec coverage: schema and closed fields are Task 1; recorder, digest,
  semantic invariants, atomic writing, and export verification are Task 2;
  explicit CLI boundaries and sanitized errors are Task 3; documentation and
  full gates are Task 4.
- Placeholder scan: no TODO, TBD, FIXME, or unspecified fallback step remains.
- Type consistency: public functions and CLI summaries use the exact signatures
  and field names defined in the design; `verify_context_traces` returns a list
  of validated records and the CLI derives its count from that list.
