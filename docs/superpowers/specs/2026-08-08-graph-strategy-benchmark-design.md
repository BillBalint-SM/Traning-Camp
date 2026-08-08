# M5 Deterministic Graph Strategy Benchmark Design

**Status:** Approved design; awaiting written-spec review before implementation planning.

## Goal

Determine, with reproducible context-level evidence, whether a deterministic
lexical index derived from a verified portable RAG export is eligible to be
promoted over the existing canonical route plus depth-1 graph baseline.

The benchmark measures selected-module coverage, fail-closed behaviour,
character-budget use, latency, repeatability, and content-hash integrity. It
creates only a model-neutral answer-evaluation adapter request contract; it
does not call a model or evaluate generated answers.

## Decision and Scope

The candidate strategy is a local lexical index built from the verified
`rag/documents.jsonl` profile. It uses only Python standard-library
normalization, tokenization, sorting, and arithmetic. No embedding model,
network call, vector database, tokenizer, MCP resource, A2A descriptor,
global/community graph, or signed provenance is part of this milestone.

The existing portable export remains immutable. Every candidate index and
benchmark result is derived from, and cryptographically bound to, one exact
export digest. A successful benchmark never changes the default context loader
or promotes a strategy by itself.

## Inputs and Derived Artifacts

### Verified portable export

The benchmark accepts only an extracted portable export directory. It calls
`verify_portable_export(export_root)` before reading either `rag/documents.jsonl`
or the graph profile. The verified manifest's `export_sha256` is required in
every derived index, context trace, benchmark report, and answer-evaluation
request.

### Lexical index artifact

`build_portable_lexical_index(export_root, index_root)` produces a new,
previously absent `index.json` below an explicit output root. Its stable shape
is:

```json
{
  "format_version": 1,
  "kind": "portable-lexical-index",
  "export_sha256": "<sha256>",
  "tokenization": "unicode-nfkc-casefold-v1",
  "scoring": {
    "title": 5,
    "alias": 4,
    "tag": 3,
    "identifier": 3,
    "body": 1,
    "minimum_score": 4,
    "minimum_margin": 2,
    "result_limit": 1
  },
  "postings": ["<sorted token-to-document postings>"],
  "index_sha256": "<sha256>"
}
```

The actual `postings` entries are canonical JSON objects, not strings. They
contain only normalized tokens, module IDs, field hit counts, and the owning
area ID; they do not duplicate module text. `index_sha256` is calculated from
the entire object excluding itself. The writer rejects existing output paths
and symbolic-link paths or ancestors, then uses the repository's atomic JSON
writer.

`verify_portable_lexical_index(export_root, index_root)` validates the exact
field set, sorted postings and IDs, scoring constants, index digest, duplicate
prevention, and equality with the verified export digest. A stale, malformed,
or mismatched index fails before any query is scored.

### Frozen benchmark suite

The benchmark suite is a separate, versioned JSON fixture with its own digest.
It contains canonical, paraphrase, negative, and ambiguous cases; each case
has a stable case ID, transient query at execution time, expected route status,
expected area, expected primary modules, and expected alternatives. It is
derived once from the reviewed routing-evaluation corpus, then committed as a
fixed fixture. It is never regenerated during a benchmark run.

The suite loader rejects duplicate IDs, unsorted expectations, unknown modules
or areas, unsupported categories, and a suite whose declared export digest does
not match the current portable export. Benchmark reports retain case IDs and
expectations, but never serialize raw query text.

## Lexical Candidate Semantics

The index extracts tokens from each RAG record's title, front-matter aliases,
metadata tags, identifier segments, and body. Text is normalized with Unicode
NFKC then `casefold`; tokens are deterministic Unicode letter/digit runs.
Repeated body occurrences do not increase a document's score, preventing long
modules from winning merely through length.

For each distinct query token, the candidate adds the configured field weight
once when that document contains the token. Documents are ordered by descending
score and then ascending module ID. The candidate has exactly three outcomes:

- `not-covered`: no document reaches `minimum_score`; no module text is loaded.
- `ambiguous`: the top two eligible documents differ by less than
  `minimum_margin`; no module text is loaded and their owning areas become the
  sorted alternatives.
- `covered`: the unique top document reaches `minimum_score` and the margin;
  it is the sole primary and expanded module.

The covered lexical context mirrors the existing portable context contract:
`format_version`, `export_sha256`, `status`, `area_id`, `module_ids`,
`alternatives`, `expanded_module_ids`, `modules`, `relations`, and `budget`.
It sets `relations` to an empty array and uses relation depth `0`, because the
candidate tests lexical retrieval rather than graph expansion. It loads the
selected module only through the verified portable export and records the
export-provided content hash.

An explicit `max_chars` applies the same 1–100000 character contract as the
baseline. A primary module that cannot fit is an error; the candidate never
silently truncates a module. Ambiguous and not-covered contexts contain no
admitted module, no module hash, and no module text.

## Fair Benchmark Flow

For every suite case, the runner executes both strategies against the same
verified export and the same explicit character budget:

1. **Baseline:** `load_portable_context_budgeted(export_root, query, 1, max_chars)`.
2. **Candidate:** `load_portable_context_lexical(export_root, index_root, query, max_chars)`.
3. **Trace:** build a content-free M3 context trace for each context. The trace
   validates status, admitted/omitted IDs, module hashes, budget, export digest,
   and the timing fields.
4. **Measure:** repeat each strategy a fixed explicit number of times with
   `perf_counter_ns`; record median and p95 elapsed milliseconds separately from
   the deterministic selection projection.
5. **Compare:** calculate expected primary-module coverage, expected-area
   coverage, safe negative rejection, safe ambiguity handling, admitted
   character count, omitted IDs, and trace/receipt verification results.

The runner returns a `portable-graph-strategy-benchmark` report. The report has
a content-free deterministic projection (case IDs, strategy IDs, statuses,
module IDs, omissions, hashes, metrics, and decision) and a separate timing
projection. The timing values may vary between runs; all non-timing selection
fields must be byte-identical across repeated runs on the same export and
suite.

## Promotion Decision

The deterministic recommendation is one of `promote`, `do-not-promote`, or
`inconclusive`. It is advisory only.

`promote` requires all of the following:

1. 100% export/index/trace integrity and deterministic selection evidence.
2. 100% negative rejection and ambiguity fail-closed behaviour.
3. Candidate expected primary-module coverage no lower than the baseline.
4. Candidate median admitted characters no higher than the baseline at the
   same budget.
5. Candidate p95 latency no greater than twice the baseline p95 plus 5 ms.
6. A material benefit: either at least five percentage points more expected
   primary-module coverage, or equal coverage with at most 75% of the
   baseline's median admitted characters.

If the evidence is valid but any promotion condition is not met, the report is
`do-not-promote`. `inconclusive` is reserved for valid evidence that cannot be
compared, such as a declared benchmark run count below the required minimum.
Invalid input, integrity failure, unsafe path, or write failure raises
`KnowledgeForgeError`; it is not an `inconclusive` result.

## Answer-Evaluation Adapter Contract

M5 adds a schema and validator for a future evaluator request only. The request
contains `format_version`, `kind`, `case_id`, `query_sha256`, `export_sha256`,
`strategy_id`, `context_trace_sha256`, `expected_module_ids`, and a request
digest. It excludes raw query text, module text, generated answer text, model
name, provider data, credentials, and telemetry transport fields.

The request allows a separately authorized evaluator to bind an answer-quality
record to a precise strategy context later. M5 does not implement an evaluator,
does not define answer-quality thresholds, and does not store an answer.

## Public Interfaces and CLI

All public functions require explicit parameters; none has public default
arguments.

```python
def build_portable_lexical_index(export_root: Path, index_root: Path) -> dict[str, object]: ...
def verify_portable_lexical_index(export_root: Path, index_root: Path) -> dict[str, object]: ...
def load_portable_context_lexical(
    export_root: Path, index_root: Path, query: str, max_chars: int
) -> dict[str, object]: ...
def run_graph_strategy_benchmark(
    export_root: Path,
    index_root: Path,
    suite_path: Path,
    max_chars: int,
    repeat_count: int,
) -> dict[str, object]: ...
def write_graph_strategy_benchmark(
    report_path: Path, report: dict[str, object]
) -> None: ...
def build_answer_evaluation_request(
    case_id: str,
    query: str,
    strategy_id: str,
    context_trace: dict[str, object],
    expected_module_ids: list[str],
) -> dict[str, object]: ...
```

The CLI adds explicit workspace-contained commands for building and verifying
the lexical index, running the benchmark, and writing an answer-evaluation
request. Every output path must be new, relative to the supplied workspace,
and free of existing symbolic links. The commands print canonical summaries;
the full artifacts are written only to the caller's explicit paths.

## Verification Plan

The implementation must add focused unit and CLI coverage for:

- byte-identical index creation from two clean copies of the same export;
- malformed, duplicate, tampered, stale, absolute, escaping, and symlinked
  index inputs or outputs;
- weighted scoring, stable tie-breaking, `not-covered`, `ambiguous`, covered,
  and character-budget behaviours;
- lexical-context module hashes and compatibility with the existing M3 trace
  validator;
- fixed-suite loading, absent-query report privacy, metric arithmetic, latency
  projection, deterministic selection projection, and every promotion outcome;
- answer-evaluation request schema, privacy, and digest validation;
- full CLI negative paths and existing-output preservation.

Release evidence is: focused tests, Ruff, full `uv run pytest -q`, real export
verification with an unchanged digest, a benchmark smoke against the frozen
suite, and an independent read-back of its report and traces. No benchmark
result promotes the candidate automatically; promotion remains an explicit
human decision after reviewing the report.
