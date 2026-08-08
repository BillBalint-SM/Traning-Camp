# Deterministic Graph Strategy Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a deterministic, local lexical retrieval candidate and a reproducible, advisory benchmark that decides whether it merits promotion over the verified depth-1 portable-graph baseline.

**Architecture:** The canonical portable export remains read-only. A separate lexical artifact is rebuilt from verified `rag/documents.jsonl`, binds itself to exactly one `export_sha256`, and retrieves at most one verified module. A fixed, digest-bound evaluation suite drives both strategies; the benchmark creates content-free M3 traces, separates deterministic selection evidence from timing evidence, and emits an advisory recommendation only.

**Tech Stack:** Python 3.10+, standard-library Unicode normalization/tokenization/timing/statistics, existing `jsonschema` validation, existing knowledge-forge JSON/hash/path utilities, pytest, Ruff, uv.

## Global Constraints

- Do not modify `exports/portable-exports-v10/` or its `export_sha256` (`bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2`). It is the immutable source of truth.
- The candidate uses no model, embedding, tokenizer, vector database, network request, MCP resource, A2A descriptor, global graph, signed provenance, or dependency addition.
- Normalize every lexical field with Unicode NFKC followed by `casefold`, then tokenize as maximal Unicode `str.isalnum()` runs. Sort all externally visible lists and mappings deterministically.
- Use these exact lexical weights: `title=5`, `alias=4`, `tag=3`, `identifier=3`, `body=1`, `minimum_score=4`, `minimum_margin=2`, and `result_limit=1`.
- Score each distinct query token at most once per document field. A repeated body token must not increase the score.
- The lexical strategy has only `covered`, `ambiguous`, and `not-covered` outcomes. It never loads a module for the latter two outcomes.
- The candidate always uses relation depth `0`, returns no relations, and applies the existing explicit character range `1..100000`; an admitted primary that exceeds the budget is an error, never a truncated result.
- Reuse the M3 `portable-context-trace` validator. Benchmark and answer-request artifacts must never contain raw queries, module text, generated answers, provider/model information, credentials, or telemetry transport data.
- All CLI paths are explicit, relative to `--workspace`, must not escape it or traverse symbolic links, and all M5 outputs are new paths. Index roots and report/request files must preserve an existing sentinel unchanged on failure.
- The benchmark is context-level only: expected module coverage, expected area coverage, negative/ambiguity safety, budget/receipt integrity, determinism, and latency. It defines an answer-evaluation request contract but never invokes an evaluator.
- A benchmark report is advisory. It does not change `load_portable_context_budgeted`, the default loader, or any runtime integration.
- Run focused tests before broader checks. Create a Git commit only after the user has explicitly approved the reviewed working diff.

---

## File Structure

| Path | Responsibility |
| --- | --- |
| `forge/schemas/portable-lexical-index.schema.json` | Structural contract for the derived `index.json` artifact. |
| `forge/schemas/graph-strategy-suite.schema.json` | Structural contract for the immutable, export-bound fixture. |
| `forge/schemas/graph-strategy-benchmark.schema.json` | Structural contract for the content-free benchmark report. |
| `forge/schemas/answer-evaluation-request.schema.json` | Structural contract for the future evaluator request. |
| `forge/evals/graph-strategy-v1.json` | Committed 263-case fixture, copied once from the reviewed routing corpus and bound to the current export digest. |
| `forge/src/knowledge_forge/lexical_index.py` | Index construction, verification, deterministic scoring, and lexical context loading. |
| `forge/src/knowledge_forge/portability.py` | One public verified-module loader that lexical retrieval can reuse without copying the export read path. |
| `forge/src/knowledge_forge/strategy_benchmark.py` | Fixture/report validation, dual-strategy execution, M3 traces, deterministic/timing projections, metrics, and advisory decision. |
| `forge/src/knowledge_forge/answer_evaluation.py` | Content-free answer-evaluation request construction and validation. |
| `forge/src/knowledge_forge/cli.py` | Explicit build, verify, benchmark, and request CLI commands. |
| `tests/test_lexical_index.py` | Index, scoring, candidate-context, hash, budget, and path safety coverage. |
| `tests/test_strategy_benchmark.py` | Fixture, timing/selection projection, metrics, integrity, and decision-gate coverage. |
| `tests/test_answer_evaluation.py` | Request schema, digest, trace binding, and privacy coverage. |
| `tests/test_cli_package.py` | End-to-end M5 CLI and existing-output/escaping failure coverage. |
| `exports/README.md` | Portable lexical-index and advisory-benchmark usage without implying automatic promotion. |

## Fixed Artifact Contracts

### 1. Lexical index (`index.json`)

The index root contains exactly one file, `index.json`. Its canonical JSON payload is:

```json
{
  "format_version": 1,
  "kind": "portable-lexical-index",
  "export_sha256": "<64 lowercase hex>",
  "tokenization": "unicode-nfkc-casefold-v1",
  "scoring": {
    "alias": 4,
    "body": 1,
    "identifier": 3,
    "minimum_margin": 2,
    "minimum_score": 4,
    "result_limit": 1,
    "tag": 3,
    "title": 5
  },
  "postings": [
    {
      "documents": [
        {
          "area_id": "tool-execution",
          "fields": {"title": 1},
          "module_id": "procedure.tool-contract-design"
        }
      ],
      "token": "eszközszerződés"
    }
  ],
  "index_sha256": "<sha256 of the payload without index_sha256>"
}
```

`postings` sorts by `token`; every posting's documents sort by `module_id`; a document's `fields` mapping sorts by field name and contains only `alias`, `body`, `identifier`, `tag`, and `title` with value `1`. The index stores no module text. `verify_portable_lexical_index` rebuilds the expected in-memory payload from the verified export, checks the schema/digest/inventory, and compares canonical payloads. It therefore rejects stale, altered, duplicate, unsorted, or internally inconsistent artifacts.

### 2. Frozen suite (`graph-strategy-v1.json`)

The fixture is a checked-in projection of `forge/evals/routing-v1.json`, created once during this slice. It has these fields only: `format_version`, `kind`, `export_sha256`, `expected_counts`, `cases`, and `suite_sha256`. `kind` is `portable-graph-strategy-suite`; `format_version` is `1`; `export_sha256` is the verified v10 digest above; and `suite_sha256` is calculated over the payload without itself. Each case retains exactly `id`, `category`, `query`, `expected_status`, `expected_area_id`, `expected_module_ids`, and `expected_alternatives`. The suite has 193 canonical, 40 paraphrase, 20 negative, and 10 ambiguous cases, sorted by case ID.

The benchmark validates the fixture against the verified export: known module and area IDs, matching module ownership, sorted/unique IDs and alternatives, unique case IDs, complete canonical coverage, exact category counts, and equal export digest. The report may contain only case IDs and expected/actual metadata; it must omit fixture queries.

### 3. Benchmark report

The report kind is `portable-graph-strategy-benchmark`, format version `1`, and contains these top-level fields: `export_sha256`, `index_sha256`, `suite_sha256`, `max_chars`, `repeat_count`, `minimum_repeat_count`, `cases`, `metrics`, `selection_projection`, `timing_projection`, `decision`, `decision_reasons`, and `benchmark_sha256`.

Each case record contains its ID/category, expected route metadata, per-strategy actual metadata, the complete metadata-only M3 context trace and its digest, selection digest, budget receipt, and integrity result. It contains no raw query or module text. `selection_projection` excludes every timing value and every `trace_sha256`, so canonical JSON bytes must match across repeated benchmark runs. `timing_projection` contains ordered raw elapsed nanoseconds plus median and nearest-rank p95 nanoseconds; it is explicitly allowed to vary.

### 4. Answer-evaluation request

The request contains exactly `format_version`, `kind`, `case_id`, `query_sha256`, `export_sha256`, `strategy_id`, `context_trace_sha256`, `expected_module_ids`, and `request_sha256`. `kind` is `answer-evaluation-request`; `format_version` is `1`; the digest covers the payload without `request_sha256`. It is a binding request only, not an answer, score, model call, or evaluator implementation.

## Promotion Gate

`run_graph_strategy_benchmark` uses the following exact rules. Invalid exports, indexes, suites, traces, output paths, and schemas raise `KnowledgeForgeError`; they never yield a decision.

1. A `repeat_count` of `1` or `2` produces a valid `inconclusive` report with `repeat_count_below_minimum`; zero, negative, or boolean counts raise an error. The minimum promotable repeat count is `3`.
2. With `repeat_count >= 3`, `promote` requires all of the following:
   - all index/export/trace validations and repeat-selection comparisons pass;
   - negative cases are all `not-covered` with zero admitted modules;
   - ambiguous cases are all `ambiguous` with zero admitted modules;
   - candidate expected-primary coverage is at least baseline expected-primary coverage;
   - candidate median admitted characters is at most the baseline median admitted characters;
   - candidate p95 latency is at most `2 * baseline_p95_ns + 5_000_000`;
   - either candidate expected-primary coverage exceeds baseline by at least 5 percentage points, or equal coverage uses at most 75% of the baseline median admitted characters.
3. A valid, comparable result that misses any condition is `do-not-promote`. The report always records sorted machine-readable reasons. No recommendation alters runtime behaviour.

### Task 1: Freeze M5 contracts and the benchmark fixture

**Files:**
- Create: `forge/schemas/portable-lexical-index.schema.json`
- Create: `forge/schemas/graph-strategy-suite.schema.json`
- Create: `forge/schemas/graph-strategy-benchmark.schema.json`
- Create: `forge/schemas/answer-evaluation-request.schema.json`
- Create: `forge/evals/graph-strategy-v1.json`
- Test: `tests/test_strategy_benchmark.py`

**Interfaces:**
- Consumes: `validate_record(schema_path: Path, record: object, label: str) -> None`, `canonical_json_bytes(payload: object) -> bytes`, and the immutable v10 portable export digest.
- Produces: four Draft 2020-12 schemas and a static fixture consumed by `load_graph_strategy_suite(suite_path: Path, export_root: Path) -> dict[str, object]` in Task 4.

- [ ] **Step 1: Write static contract and fixture tests before writing contracts.**

```python
def test_graph_strategy_fixture_is_canonical_and_bound_to_v10() -> None:
    suite = cast(dict[str, object], read_json(GRAPH_STRATEGY_SUITE))
    validate_record(SUITE_SCHEMA, suite, "graph strategy suite")

    without_digest = {key: value for key, value in suite.items() if key != "suite_sha256"}
    assert suite["export_sha256"] == V10_EXPORT_SHA256
    assert suite["suite_sha256"] == sha256_bytes(canonical_json_bytes(without_digest))


def test_answer_request_schema_rejects_an_unexpected_field() -> None:
    with pytest.raises(KnowledgeForgeError, match="Schema validation failed"):
        validate_record(REQUEST_SCHEMA, {"unexpected": "value"}, "answer request")
```

- [ ] **Step 2: Run the focused rejection tests and confirm that the missing contracts/imports fail.**

Run: `uv run pytest tests/test_strategy_benchmark.py -q`

Expected: FAIL because the schemas and frozen fixture do not yet exist.

- [ ] **Step 3: Create the four schemas with exact field closure and canonical digest requirements.**

Use the existing `context-trace.schema.json` pattern: Draft 2020-12, `additionalProperties: false`, local `$defs` for lowercase SHA-256 digests and identifiers, and required `format_version`/`kind` constants. Define report case records without `query` or `text`, and define request records without provider/model/answer fields.

```json
{
  "$id": "https://knowledge-forge.local/schemas/answer-evaluation-request.schema.json",
  "type": "object",
  "additionalProperties": false,
  "required": ["format_version", "kind", "case_id", "query_sha256", "export_sha256", "strategy_id", "context_trace_sha256", "expected_module_ids", "request_sha256"],
  "properties": {
    "format_version": {"const": 1},
    "kind": {"const": "answer-evaluation-request"}
  }
}
```

- [ ] **Step 4: Create the frozen suite by copying each reviewed case once, not by generating it at benchmark runtime.**

Read `forge/evals/routing-v1.json`, retain each case's seven fields exactly, sort the case array by `id`, add the fixed current `export_sha256`, and calculate `suite_sha256` using `sha256_bytes(canonical_json_bytes(payload_without_digest))`. Add the resulting canonical JSON file as a fixed fixture. Do not alter `routing-v1.json` and do not include its routing thresholds, because M5 owns its distinct promotion gate.

```python
suite_without_digest = {
    "format_version": 1,
    "kind": "portable-graph-strategy-suite",
    "export_sha256": export_sha256,
    "expected_counts": {
        "ambiguous": 10,
        "canonical": 193,
        "negative": 20,
        "paraphrase": 40,
    },
    "cases": sorted(cases, key=lambda case: cast(str, case["id"])),
}
suite["suite_sha256"] = sha256_bytes(canonical_json_bytes(suite_without_digest))
```

- [ ] **Step 5: Add fixture and schema regression tests.**

Cover a changed `suite_sha256`, a changed `export_sha256`, wrong category counts, an unknown schema field, an invalid SHA-256 shape, and a request/report schema field named `query`, `text`, `answer`, `model`, or `provider`. Semantic suite errors such as duplicate IDs or unknown module/area references are covered with the loader in Task 4.

- [ ] **Step 6: Run the Task 1 test group.**

Run: `uv run pytest tests/test_strategy_benchmark.py -q`

Expected: PASS for schema/fixture validation cases implemented so far.

- [ ] **Step 7: Inspect the source-controlled fixture and request explicit commit approval.**

Run: `git diff --check; git diff -- forge/schemas forge/evals/graph-strategy-v1.json tests/test_strategy_benchmark.py`

Expected: the new fixture has 263 cases, one stable export digest, no raw module text, and no unrelated changes. Do not create a commit until the user explicitly approves this reviewed diff.

### Task 2: Build and verify the deterministic lexical index

**Files:**
- Create: `forge/src/knowledge_forge/lexical_index.py`
- Modify: `forge/src/knowledge_forge/portability.py`
- Test: `tests/test_lexical_index.py`

**Interfaces:**
- Consumes: `verify_portable_export(export_root: Path) -> dict[str, object]`, `read_jsonl(path: Path) -> list[dict[str, object]]`, `canonical_json_bytes(payload: object) -> bytes`, `sha256_bytes(data: bytes) -> str`, `write_json_atomic(path: Path, payload: object) -> None`, and `KnowledgeForgeError`.
- Produces:

```python
def build_portable_lexical_index(export_root: Path, index_root: Path) -> dict[str, object]: ...
def verify_portable_lexical_index(export_root: Path, index_root: Path) -> dict[str, object]: ...
def load_portable_context_lexical(
    export_root: Path, index_root: Path, query: str, max_chars: int
) -> dict[str, object]: ...
def load_verified_portable_modules(
    output_root: Path, module_ids: list[str]
) -> list[dict[str, object]]: ...
```

- [ ] **Step 1: Write deterministic index and tokenization tests.**

```python
def test_index_bytes_are_identical_for_two_clean_verified_exports(tmp_path: Path) -> None:
    first_export, second_export = _two_equivalent_exports(tmp_path)
    first = build_portable_lexical_index(first_export, tmp_path / "derived/first")
    second = build_portable_lexical_index(second_export, tmp_path / "derived/second")

    assert first == second
    assert (tmp_path / "derived/first/index.json").read_bytes() == (
        tmp_path / "derived/second/index.json"
    ).read_bytes()


def test_tokenize_nfkc_casefolds_and_splits_identifier_segments() -> None:
    assert _tokenize("Ａgent-Tool.Contract") == ["agent", "tool", "contract"]
```

- [ ] **Step 2: Run the focused tests and confirm they fail before implementation.**

Run: `uv run pytest tests/test_lexical_index.py -q`

Expected: FAIL because `knowledge_forge.lexical_index` does not exist.

- [ ] **Step 3: Implement private index normalization and record extraction with no third-party parser.**

Read only verified RAG JSONL records after `verify_portable_export`. Extract `title` and `metadata.tags` from the record, module ID segments from `id`, and title/alias/body from the Markdown `text` using a small front-matter line reader that recognizes the repository's single-line `aliases: [a, b]` syntax. It must fail with `KnowledgeForgeError` for malformed required RAG fields or malformed alias lines. Do not call PyYAML or add a dependency; the tokenizer and extraction helpers remain entirely within Python's standard library.

```python
def _tokenize(value: str) -> list[str]:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    tokens: list[str] = []
    current: list[str] = []
    for character in normalized:
        if character.isalnum():
            current.append(character)
        elif current:
            tokens.append("".join(current))
            current = []
    if current:
        tokens.append("".join(current))
    return tokens
```

- [ ] **Step 4: Implement canonical payload construction and atomic root publication.**

Build an in-memory posting map from every unique token and field presence, then serialize it in the exact contract shape. Calculate `index_sha256` from the payload without that field. Use a temporary sibling directory, write its `index.json` with `write_json_atomic`, call `verify_portable_lexical_index` on staging, then atomically publish with `os.replace`. Reject an existing root, a symbolic-link root, and any symbolic-link ancestor before staging. Cleanup only the temporary directory that this function created.

```python
def _with_index_digest(payload_without_digest: dict[str, object]) -> dict[str, object]:
    payload = dict(payload_without_digest)
    payload["index_sha256"] = sha256_bytes(canonical_json_bytes(payload_without_digest))
    return payload
```

- [ ] **Step 5: Implement index verification by rebuilding from the verified export.**

Validate `index.json` with `portable-lexical-index.schema.json`, reject digest/field/order/duplicate drift, rebuild the expected artifact from the verified RAG source, and require byte-equivalent canonical JSON. This binds postings, module IDs, area ownership, tokenization, scoring constants, and export digest to one source of truth.

- [ ] **Step 6: Expose the verified module loader without duplicating the portable read boundary.**

Rename the private module loader in `portability.py` to `load_verified_portable_modules`, retain its sorted-ID and graph-node content-hash behavior, and update existing internal calls. This function assumes its caller already called `verify_portable_export`; `load_portable_context_lexical` will call verification immediately before using it.

- [ ] **Step 7: Add index tamper and path-safety tests.**

Cover an altered posting, altered `index_sha256`, mismatched export digest, duplicate/unsorted posting document, missing module, index root symlink, symlink ancestor, existing root sentinel, malformed alias front matter, and a tampered export. Each failure must leave any pre-existing output untouched.

- [ ] **Step 8: Run the Task 2 test group.**

Run: `uv run pytest tests/test_lexical_index.py tests/test_portability.py -q`

Expected: PASS, including existing portable-context behavior after the loader is made public.

- [ ] **Step 9: Inspect the diff and request explicit commit approval.**

Run: `git diff --check; git diff -- forge/src/knowledge_forge/lexical_index.py forge/src/knowledge_forge/portability.py tests/test_lexical_index.py`

Expected: only local derived-index behavior and its tests are changed. Do not commit without explicit user approval.

### Task 3: Load lexical contexts and validate M3 trace compatibility

**Files:**
- Modify: `forge/src/knowledge_forge/lexical_index.py`
- Test: `tests/test_lexical_index.py`
- Test: `tests/test_measurement.py`

**Interfaces:**
- Consumes: Task 2 index verifier and `load_verified_portable_modules`, plus `build_context_trace(query: str, context: dict[str, object], relation_depth: int, timing_ms: dict[str, int]) -> dict[str, object]`.
- Produces the Task 2 `load_portable_context_lexical` public function, whose returned context is accepted by `validate_context_trace` with relation depth `0`.

- [ ] **Step 1: Write lexical outcome and budget tests.**

```python
def test_lexical_context_is_depth_zero_and_receipt_compatible(tmp_path: Path) -> None:
    export_root, index_root = _indexed_export(tmp_path)
    context = load_portable_context_lexical(
        export_root, index_root, "Eszközszerződés", 100000
    )

    assert context["status"] == "covered"
    assert context["relations"] == []
    assert context["expanded_module_ids"] == context["module_ids"]
    assert build_context_trace("Eszközszerződés", context, 0, {"route": 0, "load": 1, "total": 1})


def test_lexical_ambiguous_and_not_covered_admit_no_module(tmp_path: Path) -> None:
    export_root, index_root = _indexed_export(tmp_path)
    for query in ("agent", "zzzxxyy"):
        context = load_portable_context_lexical(export_root, index_root, query, 100000)
        assert context["modules"] == []
        assert context["expanded_module_ids"] == []
```

- [ ] **Step 2: Run the focused lexical-context tests and confirm failure.**

Run: `uv run pytest tests/test_lexical_index.py -q`

Expected: FAIL until lexical scoring and context loading are implemented.

- [ ] **Step 3: Implement exact scoring and tie handling.**

For a query, deduplicate normalized query tokens. For every token posting, add a field's configured weight once to the document's score. Order candidates by `(-score, module_id)`, discard results below score `4`, and inspect only the first two eligible records. Return `not-covered` if none qualify. Return `ambiguous` if the first two scores differ by less than `2`, with sorted unique owning areas as alternatives. Otherwise return the top document as the only primary, expanded, and loaded module.

```python
def _rank_documents(index: dict[str, object], query: str) -> list[dict[str, object]]:
    scores: dict[str, int] = {}
    # Add each configured field weight once per distinct query token.
    return sorted(
        eligible_documents,
        key=lambda document: (-cast(int, document["score"]), cast(str, document["module_id"])),
    )
```

- [ ] **Step 4: Assemble the candidate context without graph expansion.**

For `covered`, load exactly one module with `load_verified_portable_modules`, set `format_version=1`, bind `export_sha256`, set `area_id`, `module_ids`, `expanded_module_ids`, `modules`, `relations=[]`, `alternatives=[]`, and a budget receipt. For `ambiguous` and `not-covered`, use empty module/expanded/relations lists and `used_chars=0`. For a covered primary whose complete module text is longer than `max_chars`, raise `KnowledgeForgeError("Portable lexical context primary module exceeds character budget")`; never omit or truncate it.

- [ ] **Step 5: Add boundary and trace tests.**

Cover title weight outranking body weight, identifier segment matching, alias matching, tag matching, repeated body text contributing once, stable module-ID tie ordering, score exactly `4`, margin exactly `2`, margin `1`, a primary equal to the budget, a primary one character above the budget, an invalid budget, and module-hash drift rejected by `verify_context_traces`.

- [ ] **Step 6: Run focused context and M3 tests.**

Run: `uv run pytest tests/test_lexical_index.py tests/test_measurement.py -q`

Expected: PASS; no change is required to the M3 trace schema or implementation.

- [ ] **Step 7: Inspect the diff and request explicit commit approval.**

Run: `git diff --check; git diff -- forge/src/knowledge_forge/lexical_index.py tests/test_lexical_index.py tests/test_measurement.py`

Expected: candidate contexts remain local, read-only, relation-depth zero, and compatible with the existing trace receipt. Do not commit without explicit user approval.

### Task 4: Implement the benchmark, decision gate, and answer-request contract

**Files:**
- Create: `forge/src/knowledge_forge/strategy_benchmark.py`
- Create: `forge/src/knowledge_forge/answer_evaluation.py`
- Test: `tests/test_strategy_benchmark.py`
- Test: `tests/test_answer_evaluation.py`

**Interfaces:**
- Consumes: `load_portable_context_budgeted(export_root: Path, query: str, relation_depth: int, max_chars: int) -> dict[str, object]`, `load_portable_context_lexical`, `build_context_trace`, `validate_context_trace`, `write_context_traces`, `verify_context_traces`, the Task 1 schemas/fixture, and `perf_counter_ns`.
- Produces:

```python
def load_graph_strategy_suite(suite_path: Path, export_root: Path) -> dict[str, object]: ...
def run_graph_strategy_benchmark(
    export_root: Path,
    index_root: Path,
    suite_path: Path,
    max_chars: int,
    repeat_count: int,
) -> dict[str, object]: ...
def validate_graph_strategy_benchmark(report: dict[str, object]) -> None: ...
def write_graph_strategy_benchmark(report_path: Path, report: dict[str, object]) -> None: ...
def load_graph_strategy_benchmark(report_path: Path) -> dict[str, object]: ...
def build_answer_evaluation_request(
    case_id: str,
    query: str,
    strategy_id: str,
    context_trace: dict[str, object],
    expected_module_ids: list[str],
) -> dict[str, object]: ...
def validate_answer_evaluation_request(request: dict[str, object]) -> None: ...
def write_answer_evaluation_request(request_path: Path, request: dict[str, object]) -> None: ...
```

- [ ] **Step 1: Write the dual-strategy benchmark tests.**

```python
def test_benchmark_separates_deterministic_selection_from_timing(tmp_path: Path) -> None:
    export_root, index_root, suite_path = _benchmark_inputs(tmp_path)
    first = run_graph_strategy_benchmark(export_root, index_root, suite_path, 100000, 3)
    second = run_graph_strategy_benchmark(export_root, index_root, suite_path, 100000, 3)

    assert first["selection_projection"] == second["selection_projection"]
    assert "query" not in canonical_json_bytes(first).decode("utf-8")
    assert first["timing_projection"]["strategy_ids"] == ["baseline-depth-1", "lexical-v1"]
```

- [ ] **Step 2: Run the benchmark tests and confirm that they fail before implementation.**

Run: `uv run pytest tests/test_strategy_benchmark.py tests/test_answer_evaluation.py -q`

Expected: FAIL because the benchmark and request modules do not exist.

- [ ] **Step 3: Implement suite loading and export-bound semantic validation.**

Load the JSON through `require_regular_file`, validate it with the Task 1 schema, recompute `suite_sha256`, call `verify_portable_export`, and check its `export_sha256`. Read verified graph nodes and the portable areas index to validate module IDs, area IDs, module ownership, exact canonical coverage, category expectations, ordering, and uniqueness. Return cases sorted by ID.

- [ ] **Step 4: Implement one measurable strategy invocation and one content-free trace per case/strategy.**

Execute baseline `load_portable_context_budgeted(export_root, query, 1, max_chars)` and candidate `load_portable_context_lexical(export_root, index_root, query, max_chars)` exactly `repeat_count` times each. Measure every call with `perf_counter_ns`. Require all repeated selection projections to be canonically identical; otherwise raise `KnowledgeForgeError("Graph strategy selection is not deterministic")`.

Build and validate one M3 trace from the first successful context of each strategy/case using `relation_depth=1` for baseline and `0` for candidate. Store the trace in an in-memory temporary JSONL, call `verify_context_traces` against the same export, then retain the full metadata-only trace and its `trace_sha256` in the report so a future request can bind to the exact context. Convert the measured total nanoseconds to a nonnegative integer millisecond load value for the existing trace contract, with route `0` and total equal to load. Exclude those trace timing fields and the trace digest from `selection_projection`.

```python
def _timed_context(loader: Callable[[], dict[str, object]]) -> tuple[dict[str, object], int]:
    started_ns = perf_counter_ns()
    context = loader()
    return context, perf_counter_ns() - started_ns
```

- [ ] **Step 5: Calculate metadata-only metrics and projections.**

For each strategy calculate expected-primary coverage and expected-area coverage over canonical plus paraphrase cases; negative rejection and ambiguity safety over their respective categories; module/receipt/trace integrity; admitted-character values; and omission IDs. Calculate `median_ns` with `statistics.median_low` and p95 with nearest-rank `sorted_samples[ceil(0.95 * count) - 1]`, preserving integers. Build `selection_projection` from case IDs, strategy IDs, route fields, module/area/alternative IDs, budget metadata, module hashes, integrity booleans, and selection digests only. Keep elapsed values only in `timing_projection`.

- [ ] **Step 6: Implement the advisory decision function with every outcome.**

Return `inconclusive` only for valid repeat counts below `3`. For comparable runs, evaluate the six promotion rules in the declared order and collect exact reasons such as `primary_coverage_not_improved`, `candidate_characters_exceed_baseline`, or `candidate_latency_exceeds_cap`. Return `do-not-promote` when any rule fails and `promote` only when all pass. The function returns a report; it must not call any loader selection/promotion setter.

```python
def _nearest_rank_p95(samples_ns: list[int]) -> int:
    ordered = sorted(samples_ns)
    return ordered[math.ceil(len(ordered) * 0.95) - 1]
```

- [ ] **Step 7: Write report validation and atomic writer/reader tests.**

Test malformed/tampered report rejection, invalid report digest, pre-existing/symlinked/escaping report output, distinct selection versus timing projections, trace-hash absence from deterministic projection, all promotion outcomes, and that a `do-not-promote` report is successfully written rather than raised. Ensure invalid input produces no report.

- [ ] **Step 8: Implement the answer-evaluation request boundary.**

Validate `case_id` and `strategy_id` as identifiers, validate the source trace with `validate_context_trace`, require `sha256_bytes(query.encode("utf-8")) == context_trace["query_sha256"]`, require sorted unique `expected_module_ids`, construct the exact request field set, calculate `request_sha256`, then schema/semantic validate it. The writer uses the same new-file and symbolic-link protections as other one-file artifacts.

```python
request_without_digest = {
    "format_version": 1,
    "kind": "answer-evaluation-request",
    "case_id": case_id,
    "query_sha256": sha256_bytes(query.encode("utf-8")),
    "export_sha256": context_trace["export_sha256"],
    "strategy_id": strategy_id,
    "context_trace_sha256": context_trace["trace_sha256"],
    "expected_module_ids": expected_module_ids,
}
```

- [ ] **Step 9: Add request privacy and negative-path tests.**

Cover query/trace hash mismatch, unsorted or duplicate expected IDs, a changed trace digest, a changed request digest, raw query/module/model/provider/answer fields, existing output preservation, and a successful request whose canonical JSON contains neither the query nor module text.

- [ ] **Step 10: Run the Task 4 test group.**

Run: `uv run pytest tests/test_strategy_benchmark.py tests/test_answer_evaluation.py tests/test_measurement.py -q`

Expected: PASS, including all three advisory decision outcomes and M3 trace verification.

- [ ] **Step 11: Inspect the diff and request explicit commit approval.**

Run: `git diff --check; git diff -- forge/src/knowledge_forge/strategy_benchmark.py forge/src/knowledge_forge/answer_evaluation.py forge/schemas tests/test_strategy_benchmark.py tests/test_answer_evaluation.py`

Expected: no model/provider/runtime adapter code and no automatic promotion path. Do not commit without explicit user approval.

### Task 5: Add CLI commands, usage documentation, and release evidence

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py`
- Modify: `tests/test_cli_package.py`
- Modify: `exports/README.md`

**Interfaces:**
- Consumes all public interfaces from Tasks 2–4 and the existing workspace path resolvers.
- Produces these commands:

```text
build-portable-lexical-index --workspace <root> --export <dir> --index <new-derived-dir>
verify-portable-lexical-index --workspace <root> --export <dir> --index <dir>
benchmark-graph-strategies --workspace <root> --export <dir> --index <dir> --suite <file> --max-chars <int> --repeat-count <int> --report <new-file>
build-answer-evaluation-request --workspace <root> --benchmark <file> --case-id <id> --strategy-id <id> --query-file <file> --request <new-file>
```

- [ ] **Step 1: Write CLI success and failure tests.**

```python
def test_cli_builds_verifies_and_benchmarks_local_lexical_index(
    tmp_path: Path, capsys: CaptureFixture[str]
) -> None:
    workspace = _portable_workspace_with_graph_strategy_suite(tmp_path)
    assert run(_build_index_arguments(workspace)) == 0
    assert run(_verify_index_arguments(workspace)) == 0
    assert run(_benchmark_arguments(workspace)) == 0

    report = json.loads((workspace / "derived/benchmark.json").read_text(encoding="utf-8"))
    assert report["kind"] == "portable-graph-strategy-benchmark"
    assert "query" not in json.dumps(report)
```

- [ ] **Step 2: Run the CLI tests and confirm they fail before parser/dispatcher work.**

Run: `uv run pytest tests/test_cli_package.py -q`

Expected: FAIL because the M5 command names are not registered.

- [ ] **Step 3: Add parser and dispatch branches with existing safe path helpers.**

Resolve export and index inputs through `resolve_existing_directory_within`. Resolve a new index directory with `resolve_new_directory_within(workspace_root, namespace.index, Path("derived"), "Portable lexical index output")`. Resolve suite/benchmark/query inputs with `resolve_regular_within`, and report/request outputs with `resolve_new_file_within`. Never accept an absolute path, path escape, existing artifact, or symbolic link.

For `build-answer-evaluation-request`, load the validated benchmark report, select exactly one matching `case_id` and `strategy_id`, retrieve its metadata-only trace and expected modules, read the explicit `--query-file`, and call `build_answer_evaluation_request`. If the pair is absent or query hash differs, return code `2` with a clear `knowledge-forge:` error and do not create a request.

- [ ] **Step 4: Print canonical summaries only.**

Each successful command writes its explicit artifact and prints a canonical one-line object. Do not echo a query, module text, full trace, or benchmark case list.

```python
{
  "status": "PASS",
  "kind": "portable-graph-strategy-benchmark",
  "decision": "do-not-promote",
  "export_sha256": "<digest>",
  "benchmark_sha256": "<digest>"
}
```

- [ ] **Step 5: Add CLI negative-path tests.**

Cover invalid/tampered export or index, stale suite, a report path that already contains `sentinel\n`, index/report/request path escapes, symbolic-link inputs/parents where the platform supports them, invalid `--repeat-count`, absent case/strategy pairs, and a query file that does not hash to the selected trace. Assert every existing sentinel remains byte-identical.

- [ ] **Step 6: Document the exact local workflow and advisory boundary.**

Append an `## Deterministic graph strategy benchmark` section to `exports/README.md` with these commands:

```text
uv run knowledge-forge build-portable-lexical-index --workspace . --export exports/portable-exports-v10 --index derived/portable-lexical-index-v1
uv run knowledge-forge verify-portable-lexical-index --workspace . --export exports/portable-exports-v10 --index derived/portable-lexical-index-v1
uv run knowledge-forge benchmark-graph-strategies --workspace . --export exports/portable-exports-v10 --index derived/portable-lexical-index-v1 --suite forge/evals/graph-strategy-v1.json --max-chars 10000 --repeat-count 5 --report derived/graph-strategy-benchmark-v1.json
```

State that the resulting recommendation is evidence for a human decision and does not enable derived retrieval, MCP, A2A, signing, or model-based answer evaluation automatically.

- [ ] **Step 7: Run focused command and documentation checks.**

Run: `uv run pytest tests/test_cli_package.py tests/test_lexical_index.py tests/test_strategy_benchmark.py tests/test_answer_evaluation.py -q; uv run ruff check forge/src tests`

Expected: all focused tests pass and Ruff reports `All checks passed!`.

- [ ] **Step 8: Run final independent verification on the real export.**

Run:

```text
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
uv run knowledge-forge build-portable-lexical-index --workspace . --export exports/portable-exports-v10 --index derived/portable-lexical-index-v1
uv run knowledge-forge verify-portable-lexical-index --workspace . --export exports/portable-exports-v10 --index derived/portable-lexical-index-v1
uv run knowledge-forge benchmark-graph-strategies --workspace . --export exports/portable-exports-v10 --index derived/portable-lexical-index-v1 --suite forge/evals/graph-strategy-v1.json --max-chars 10000 --repeat-count 5 --report derived/graph-strategy-benchmark-v1.json
uv run pytest -q
uv run ruff check forge/src tests
```

Expected: the portable export digest remains `bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2`; focused and full suites pass; the report can be independently loaded and its selection projection/trace hashes validate. The benchmark decision is reported as evidence, not applied.

- [ ] **Step 9: Review the full diff and request explicit commit approval.**

Run: `git diff --check; git status --short; git diff --stat; git diff -- forge/src/knowledge_forge forge/schemas forge/evals tests exports/README.md`

Expected: scope is limited to the lexical index, benchmark gate, request contract, tests, and usage documentation; no `exports/portable-exports-v10` file changes and no generated `derived/` artifact is staged. Do not commit, push, create a pull request, or merge without explicit user approval.

## Final Acceptance Checklist

- [ ] A fresh index built from two clean copies of the same verified export has byte-identical `index.json` content and a matching `index_sha256`.
- [ ] Malformed, stale, tampered, duplicate, unsorted, escaping, or symbolic-link index/suite/report/request inputs fail closed with actionable `KnowledgeForgeError` messages.
- [ ] The lexical candidate deterministically scores title, aliases, tags, identifier segments, and body with the approved constants; it admits at most one verified module and performs no graph expansion.
- [ ] Candidate and baseline both produce M3-valid, export-bound, content-free traces for every benchmark case; selection evidence is deterministic and timing evidence is distinct.
- [ ] Reports contain case IDs and metadata only; raw queries, module texts, answers, model/provider data, and credentials are absent.
- [ ] The advisory decision implements every approved promotion condition and never switches the default retrieval strategy.
- [ ] The answer-evaluation request binds a case/query hash/strategy/trace/expected modules without executing an evaluator.
- [ ] CLI commands preserve existing artifacts on error and operate only within the supplied workspace.
- [ ] Ruff, focused tests, full `uv run pytest -q`, real-export verification, and independent benchmark report read-back pass before release consideration.
