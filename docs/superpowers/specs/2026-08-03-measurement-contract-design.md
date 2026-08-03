# M3 Runtime-Neutral Measurement Contract design

## Purpose

Introduce an explicit, metadata-only measurement boundary for portable context
consumption. A caller can turn a verified `load_portable_context*` result into
a compact JSONL trace without changing loader behavior or copying query,
module, or model-response text into telemetry.

The trace identifies the exact export and admitted modules through SHA-256
digests. A verifier can validate one or more records structurally and against a
portable export directory. The trace is a derived measurement artifact; the
portable export remains the only content authority.

## Scope

This slice includes:

- a versioned JSON Schema for one trace record;
- a functional recorder that strips content and computes canonical digests;
- atomic JSONL writing for a list of trace records;
- structural trace validation and export-backed verification;
- CLI commands `record-context-trace` and `verify-context-trace`;
- negative-path, determinism, privacy, and CLI tests;
- documentation for producing and validating metadata-only traces.

This slice does not instrument the existing loaders automatically, store raw
queries or module text, call a model, evaluate answer quality, add telemetry
transport, or introduce MCP/A2A/runtime-specific adapters. A later evaluator
may consume the verified trace contract without changing this schema.

## Trace record contract

Each JSONL line is one object with no unknown fields:

```json
{
  "format_version": 1,
  "kind": "portable-context-trace",
  "query_sha256": "<64 lowercase hex characters>",
  "export_sha256": "<64 lowercase hex characters>",
  "route": {
    "status": "covered",
    "area_id": "tool-execution",
    "primary_module_ids": ["procedure.tool-contract-design"],
    "alternative_area_ids": []
  },
  "context": {
    "relation_depth": 1,
    "expanded_module_ids": ["..."],
    "admitted_module_ids": ["..."],
    "omitted_module_ids": ["..."],
    "relation_count": 1
  },
  "module_hashes": {
    "procedure.tool-contract-design": "<64 lowercase hex characters>"
  },
  "budget": {
    "max_chars": 2000,
    "used_chars": 1842,
    "omitted_module_ids": ["..."]
  },
  "timing_ms": {
    "route": 4,
    "load": 11,
    "total": 15
  },
  "trace_sha256": "<64 lowercase hex characters>"
}
```

`query_sha256` is computed from the exact UTF-8 query bytes and the query is
never persisted. `trace_sha256` is computed from canonical JSON for the record
with `trace_sha256` removed. All ID arrays are sorted and unique. A non-budget
context uses `max_chars: null`, `used_chars: 0`, and an empty budget omission
list.

## Invariants

The recorder and verifier enforce the following:

- trace `format_version` is exactly `1`; any carried context or budget
  `format_version` is also exactly `1`;
- route status is one of `covered`, `ambiguous`, or `not-covered`;
- `covered` has at least one primary module; the other statuses have no
  admitted or expanded modules;
- primary IDs are a subset of expanded IDs; admitted IDs are a subset of
  expanded IDs; admitted and omitted IDs are disjoint;
- `relation_depth` is `0` or `1`, and `relation_count` is nonnegative;
- module-hash keys equal admitted IDs and each hash matches the export graph;
- `max_chars` is null or a positive integer; `used_chars` is nonnegative and
  does not exceed a non-null maximum;
- budget omission IDs equal the context omission IDs;
- timing fields are nonnegative integers and `total >= route` and
  `total >= load`;
- the trace digest recomputes exactly;
- export verification succeeds and `export_sha256` matches;
- no object, key, or serialized value contains module text, raw query text,
  model output, credentials, or absolute filesystem paths.

## Architecture

### Measurement module

Create `forge/src/knowledge_forge/measurement.py` with these public functions:

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

`build_context_trace` accepts the existing loader result in memory, checks any
module `text` against its declared `content_sha256`, then emits only IDs and
hashes. `write_context_traces` uses the existing canonical JSONL/atomic-write
conventions. `verify_context_traces` first validates every record, then calls
`verify_portable_export` and checks module and export digests against the
verified graph.

### Schema

Create `forge/schemas/context-trace.schema.json` as a closed JSON Schema
(`additionalProperties: false`) for the record shape. Semantic relationships
that JSON Schema cannot express—such as subset, digest recomputation, and
export graph closure—remain explicit Python validation rules.

### CLI

`record-context-trace` accepts:

- `--workspace`
- `--context` — an existing JSON context receipt produced by a loader;
- `--query` — transient input used only to compute `query_sha256`;
- `--depth` — `0` or `1`;
- `--route-ms`, `--load-ms`, `--total-ms` — nonnegative timing values;
- `--trace` — new JSONL output path.

It reads the context, creates one trace record, writes one JSONL line, and
prints only a digest/count summary. It never prints the context or query.

`verify-context-trace` accepts `--workspace`, `--trace`, and `--export`,
resolves paths through existing workspace guards, validates every record
against the export, and prints a stable PASS summary.

## Error handling and security

Invalid JSON, missing fields, extra fields, unsupported versions, malformed
digests, duplicate IDs, invariant violations, export mismatch, unsafe paths,
and non-regular inputs raise `KnowledgeForgeError` with an actionable message.
Messages include logical field or artifact names only; they never include raw
query text, module text, absolute paths, credentials, or model output.

The writer is atomic and refuses unsafe symlink paths through existing path
guards. The verifier is read-only and does not mutate the trace, context, or
portable export.

## Testing and acceptance criteria

Add focused tests for:

- plain, graph-depth-1, and budgeted loader contexts;
- exact removal of `text` and raw query from the trace;
- deterministic canonical bytes and `trace_sha256`;
- valid covered, ambiguous, and not-covered records;
- invalid status, depth, timing, budget, ID overlap, module hash, export hash,
  trace digest, missing, extra, duplicate, and absolute-path cases;
- atomic JSONL writing and read-only verification;
- CLI record/verify success, missing inputs, tampering, and path-boundary
  failures.

The slice is complete only when these commands pass:

```text
uv run pytest -q
uv run ruff check .
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
uv run knowledge-forge verify-context-trace --workspace . --trace <trace.jsonl> --export exports/portable-exports-v10
```

Trace fixtures are content-free and may be committed when they contain only
hashes and IDs. Generated runtime traces remain ignored local artifacts under
`dist/` or `work/`.

## Assumptions and deferred decisions

- The reference consumer supplies a loader result and timing measurements; the
  recorder does not measure or execute the loader itself.
- Timing is integer milliseconds and intentionally excludes wall-clock
  timestamps to keep fixtures deterministic and avoid host metadata.
- A later answer-quality evaluator may join a verified trace to an immutable
  export by digest; no evaluator schema or model call is introduced here.
- The first trace version is `1`; incompatible changes require a new version
  and fail closed.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Trace accidentally becomes a second knowledge store | Closed schema and recursive content-free checks. |
| A stale export makes measurements look valid | Require export-backed verification and exact export digest. |
| Timing or omission fields are inconsistent | Cross-field invariants and negative tests. |
| A future adapter writes implicitly | Explicit recorder invocation and no loader instrumentation. |
| Telemetry path leaks private filesystem data | Workspace path guards and sanitized errors. |
