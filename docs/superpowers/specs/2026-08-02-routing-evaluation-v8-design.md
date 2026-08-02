# Deterministic Routing Evaluation v8 — design specification

**Status:** Approved design, pending implementation plan
**Date:** 2026-08-02
**Workspace:** `Traning Camp`
**Delivery branch:** `dev-knowledge-evolution-v8`

## 1. Purpose

Turn knowledge routing from a small collection of hand-selected smoke tests into a deterministic, measurable quality contract. The evaluation must prove which trusted modules can be reached from natural Hungarian questions, reject unsupported questions, expose genuine ambiguity, and produce a reproducible audit report without external models, embeddings, APIs, or credentials.

The evaluation is development infrastructure. It does not enter Agent context or the portable knowledge archive.

## 2. Current baseline

The router normalizes a query with Unicode NFKC and case folding, tokenizes it, selects an L0 area by alias overlap, then selects one L1 module by overlap with its tags, aliases, and title. It returns `not-covered` when no area matches and `ambiguous` when multiple areas share the highest score. A module-score tie currently resolves to the lexicographically first module identifier.

The existing routing tests contain 30 positive module selections, one unsupported query, and one cross-area ambiguous query. They prove representative behavior but do not measure aggregate accuracy, paraphrase robustness, false routing, or reachability across all 193 modules.

## 3. Selected approach

Implement a versioned JSON evaluation suite, a strict deterministic evaluator, a CLI verification command, and an ignored audit report. Establish the unchanged router baseline before changing routing metadata or scoring. Correct only demonstrated root causes, then rerun the complete suite as a release gate.

This approach is preferred over adding only parameterized tests because it produces comparable metrics and a durable audit artifact. It is preferred over model-judged evaluation because it remains reproducible, offline, inexpensive, and transparent.

## 4. Scope

### Included

- A machine-readable routing-evaluation schema.
- A tracked, source-neutral Hungarian routing suite.
- Strict validation of suite structure and all referenced area and module identifiers.
- Deterministic case execution against the real package indexes and router.
- Category, area, and aggregate metrics.
- A canonical report digest and package/suite identity.
- An explicit quality gate with actionable case-level failures.
- Targeted routing metadata or scoring corrections supported by baseline failures.
- Full package, provenance-coverage, unit-disposition, neutrality, context-budget, and archive-regression checks.

### Excluded

- External LLM judges, embeddings, vector databases, or API calls.
- Automatic rewriting of aliases, tags, modules, or routing code.
- Automatic promotion or maturity changes for knowledge modules.
- Changes to a consuming platform.
- Derived Understand Anything or Graphify projections; those belong to the next bounded slice.
- Promotion from `feature` to `main`.

## 5. Evaluation suite contract

The suite uses `format_version: 1`, declares its thresholds, and contains uniquely identified cases. Every case has exactly these fields:

- `id`: stable lowercase dot-separated identifier;
- `category`: `canonical`, `paraphrase`, `negative`, or `ambiguous`;
- `query`: non-empty Hungarian natural-language question;
- `expected_status`: `covered`, `not-covered`, or `ambiguous`;
- `expected_area_id`: one known area identifier or `null`;
- `expected_module_ids`: sorted known module identifiers;
- `expected_alternatives`: sorted known area identifiers.

Category constraints are strict:

- `canonical` and `paraphrase` require `covered`, one area, exactly one module, and no alternatives.
- `negative` requires `not-covered`, no area, no modules, and no alternatives.
- `ambiguous` requires `ambiguous`, no selected area, no modules, and at least two alternatives.

Unknown keys, duplicate case IDs, unknown endpoints, invalid combinations, empty queries, unsorted identifier lists, and case-count mismatches are fatal.

## 6. Suite composition

The v1 suite contains exactly 263 reviewed cases:

| Category | Count | Purpose |
|---|---:|---|
| Canonical | 193 | One natural question for every trusted module |
| Paraphrase | 40 | Four less alias-adjacent formulations per area |
| Negative | 20 | Unsupported requests that must not invent a route |
| Ambiguous | 10 | Genuine cross-area boundary questions |

Canonical target coverage must equal the current public module set: 193 unique target module identifiers with no duplicate target and no missing module. Paraphrase cases complement rather than replace canonical coverage.

## 7. Evaluator architecture

Create a focused `routing_evaluation` module with three responsibilities implemented as separate functions:

1. load and validate the suite against its schema and the current package endpoints;
2. run every case through the existing `route_query` interface and produce deterministic case results;
3. aggregate metrics, enforce thresholds, and write a canonical audit report.

The evaluator consumes only the validated portable package and the tracked suite. It never reads private intake, provenance, normalized units, or origin-bearing records.

The CLI command is:

```powershell
uv run knowledge-forge verify-routing-evaluation `
  --workspace . `
  --pack pack `
  --schemas forge/schemas `
  --suite forge/evals/routing-v1.json `
  --report private/audit/routing-evaluation-v8.json
```

All paths resolve within `--workspace`. Symlinks, path traversal, missing files, invalid JSON, invalid schemas, and unknown endpoints fail explicitly.

## 8. Metrics and thresholds

The deterministic report contains:

- package SHA-256;
- suite SHA-256;
- case count and category counts;
- canonical module target coverage;
- canonical area accuracy;
- canonical module Hit@1;
- paraphrase exact-route accuracy;
- negative rejection accuracy;
- ambiguity exact-set accuracy;
- covered responses with no selected module;
- per-area pass counts;
- sorted case-level failures;
- canonical evaluation SHA-256.

The v8 release gate requires:

| Metric | Threshold |
|---|---:|
| Canonical target coverage | 193/193 |
| Canonical area accuracy | 100% |
| Canonical module Hit@1 | 100% |
| Paraphrase exact-route accuracy | at least 90% |
| Negative rejection accuracy | 100% |
| Ambiguity exact-set accuracy | 100% |
| Covered responses without a module | 0 |
| L0 and every L1 index | at most 8192 bytes |

Passing this curated suite proves deterministic regression coverage for its declared cases. It does not claim general semantic understanding outside the suite.

## 9. Baseline and correction loop

The first real execution uses the current package unchanged and preserves its ignored baseline report. Failures are classified as:

- missing or misleading area terminology;
- missing or misleading module terminology;
- false-positive generic token;
- genuine cross-area ambiguity;
- module-score tie hidden by lexicographic selection;
- unsupported request routed as covered;
- benchmark expectation error.

Corrections follow this order:

1. correct an invalid benchmark expectation;
2. replace misleading or redundant metadata;
3. add a missing high-value term only when index budgets permit;
4. change scoring behavior only when metadata cannot express the correct boundary;
5. rerun the entire suite after every material correction.

No evaluator output edits canonical artifacts automatically.

## 10. Context-budget constraint

The `context-and-knowledge` L1 index currently occupies 8184 of the permitted 8192 bytes. Therefore alias accumulation is not an acceptable default correction. Changes in that area must replace redundant terms, improve routing without increasing index size, or otherwise preserve the existing hard limit. The complete index-budget test runs after every routing correction.

## 11. Failure behavior and reporting

Malformed suite input produces no success report. A structurally valid suite that misses quality thresholds writes a deterministic failure report, then exits non-zero with the first failed metric and the report-relative location. Diagnostics contain stable case identifiers and public module identifiers but no secrets, absolute paths, or private unit identifiers.

Reports are written atomically only beneath the resolved workspace. Case results and failure lists are sorted by stable case ID. Timestamps and runtime-specific data are excluded so identical inputs produce identical report bytes.

## 12. File boundaries

Tracked development artifacts:

- `forge/schemas/routing-evaluation.schema.json`
- `forge/evals/routing-v1.json`
- `forge/src/knowledge_forge/routing_evaluation.py`
- `forge/src/knowledge_forge/cli.py`
- `tests/test_routing_evaluation.py`
- this specification and its implementation plan

Potential tracked package changes are limited to demonstrated routing metadata or algorithm corrections plus regenerated indexes, graph, manifest, and routing tests. The evaluation suite and report do not enter `pack/` or `dist/`.

Ignored artifacts:

- `private/audit/routing-evaluation-v8-baseline.json`
- `private/audit/routing-evaluation-v8.json`
- validated v8 archives beneath `dist/`

## 13. Verification strategy

Test-driven implementation covers:

- a passing mixed-category suite;
- invalid schema and unknown endpoint rejection;
- duplicate case and duplicate canonical target rejection;
- missing public-module target rejection;
- category/expectation mismatch rejection;
- exact aggregate metrics;
- threshold failure with a preserved deterministic report;
- no report for structurally invalid input;
- identical report bytes across repeated executions;
- path-containment and symlink rejection through existing workspace guards.

Final gates include the complete pytest suite, Ruff, package verification, exact 193-module promotion coverage, exact 309-unit disposition coverage, package inspection, public neutrality scan, L0/L1 byte budgets, and two independently created archives with identical SHA-256 hashes.

## 14. Delivery workflow

Implementation remains on `dev-knowledge-evolution-v8`. After all gates pass, tracked changes are reviewed for scope and private leakage, committed, pushed, and fast-forwarded into `feature`. The synchronized `feature` is revalidated before publication. The merged v8 worktree is removed only after ignored reports and archives are preserved, then a unique clean `dev-knowledge-map-v9` worktree starts from the updated `feature`.

The local bare origin does not support a GitHub pull request. `main` remains unchanged.

## 15. Acceptance criteria

The slice is complete only when:

1. all 263 cases satisfy the suite schema and endpoint rules;
2. canonical cases target exactly 193 of 193 public modules;
3. every declared metric meets its threshold;
4. the unchanged-router baseline and final report are preserved privately;
5. no private record enters tracked evaluation data, `pack/`, or an archive;
6. no L0 or L1 index exceeds 8192 bytes;
7. full public and private validation gates pass;
8. two v8 archives are byte-identical;
9. `feature` and `origin/feature` converge on the verified v8 commit;
10. `main` remains unchanged and a clean next dev worktree exists.

## 16. Expected active effort

The expected active implementation effort is approximately 6–12 hours. Most effort belongs to writing and reviewing 263 meaningful routing cases, classifying the unchanged baseline failures, and correcting demonstrated routing boundaries without overfitting or breaking the strict context budget.
