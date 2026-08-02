# Deterministic Routing Evaluation v8 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic 263-case routing quality gate that reaches all 193 public modules, measures paraphrase, negative, and ambiguity behavior, and produces a reproducible private audit report.

**Architecture:** A tracked JSON suite is validated against a strict schema and the current package endpoints. A functional evaluator runs the existing `route_query` interface, aggregates integer metrics, writes a canonical report, and fails when declared thresholds are missed. The unchanged baseline is preserved before any narrowly justified routing correction.

**Tech Stack:** Python 3.10+, JSON Schema Draft 2020-12, pytest, Ruff, canonical JSON and SHA-256 helpers already present in the forge.

## Global Constraints

- The suite contains exactly 193 canonical, 40 paraphrase, 20 negative, and 10 ambiguous cases.
- Canonical targets cover exactly all 193 public module IDs once each.
- Canonical area and module accuracy, negative rejection, and ambiguity exact-set accuracy are 100%; paraphrase exact-route accuracy is at least 90%.
- L0 and every L1 index remain at most 8192 canonical JSON bytes.
- Evaluation data and diagnostics contain no private units, paths, provenance, origin markers, secrets, or credentials.
- The suite and report never enter `pack/` or the portable archive.
- No external model, embedding, network service, or API credential is used.
- No evaluator output edits routing metadata or canonical package artifacts automatically.
- `main` remains unchanged; the slice targets `feature` through `dev-knowledge-evolution-v8`.

---

### Task 1: Routing evaluation schema and structural contract

**Files:**
- Create: `forge/schemas/routing-evaluation.schema.json`
- Create: `forge/src/knowledge_forge/routing_evaluation.py`
- Create: `tests/test_routing_evaluation.py`

**Interfaces:**
- Consumes: `validate_record(schema_path: Path, record: object, label: str)`, `read_json(path: Path)`, and indexes shaped as `{"l0": object, "l1": object}`.
- Produces: `load_routing_suite(suite_path: Path, schema_path: Path, indexes: dict[str, object]) -> dict[str, object]`.

- [ ] **Step 1: Write failing structural validation tests**

Create helpers that copy the real `pack/` and schema directory into `tmp_path`, then write a minimal suite containing one canonical case for every currently discovered module plus the declared category counts. Add focused tests that mutate this valid fixture and assert explicit `KnowledgeForgeError` messages for:

```python
def test_load_routing_suite_rejects_unknown_module(tmp_path: Path) -> None:
    suite_path, schema_path, indexes = _valid_suite(tmp_path)
    payload = json.loads(suite_path.read_text(encoding="utf-8"))
    payload["cases"][0]["expected_module_ids"] = ["principle.unknown"]
    suite_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(KnowledgeForgeError, match="unknown module"):
        load_routing_suite(suite_path, schema_path, indexes)
```

Cover invalid schema shape, duplicate case ID, duplicate canonical target, missing public canonical target, unknown area, unsorted module/alternative identifiers, and category/expectation mismatch. Assert that every failure names the violated routing-evaluation rule without printing the query text.

- [ ] **Step 2: Run the focused tests and confirm RED**

Run:

```powershell
uv run pytest -q tests/test_routing_evaluation.py -k "load_routing_suite"
```

Expected: collection or import failure because `routing_evaluation.py` and `load_routing_suite` do not exist.

- [ ] **Step 3: Add the strict JSON schema**

Define a Draft 2020-12 object with `additionalProperties: false` at the suite, threshold, count, and case levels. Require:

```json
{
  "format_version": 1,
  "expected_counts": {
    "canonical": 193,
    "paraphrase": 40,
    "negative": 20,
    "ambiguous": 10
  },
  "thresholds": {
    "canonical_area_percent": 100,
    "canonical_module_percent": 100,
    "paraphrase_percent": 90,
    "negative_percent": 100,
    "ambiguous_percent": 100
  },
  "cases": []
}
```

Case IDs use `^[a-z][a-z0-9.-]*$`; category and expected status use closed enums; queries have `minLength: 1`; expected identifier arrays contain unique strings.

- [ ] **Step 4: Implement endpoint and semantic validation**

Implement `load_routing_suite` as a single-mode loader:

1. reject a symlink or non-regular suite file with `require_regular_file`;
2. parse with `read_json` and validate using `validate_record`;
3. derive known area IDs from L0 and known module IDs plus module-to-area ownership from L1;
4. enforce exact category field combinations;
5. require unique case IDs;
6. require exact declared category counts;
7. require canonical targets to equal the known module set exactly once;
8. sort cases by ID only after proving their stored order-independent validity.

Return the validated payload without changing query or identifier content.

- [ ] **Step 5: Run focused tests and Ruff**

Run:

```powershell
uv run pytest -q tests/test_routing_evaluation.py -k "load_routing_suite"
uv run ruff check forge/src/knowledge_forge/routing_evaluation.py tests/test_routing_evaluation.py
```

Expected: all Task 1 tests pass and Ruff prints `All checks passed!`.

- [ ] **Step 6: Commit the structural contract**

```powershell
git add forge/schemas/routing-evaluation.schema.json forge/src/knowledge_forge/routing_evaluation.py tests/test_routing_evaluation.py
git commit -m "feat: add routing evaluation contract"
```

---

### Task 2: Deterministic evaluator, metrics, report, and threshold failure

**Files:**
- Modify: `forge/src/knowledge_forge/routing_evaluation.py`
- Modify: `tests/test_routing_evaluation.py`

**Interfaces:**
- Consumes: `route_query(query: str, indexes: dict[str, object]) -> dict[str, object]`, `inspect_package(pack_root: Path, schema_root: Path) -> dict[str, object]`, `canonical_json_bytes(payload: object) -> bytes`, and `write_json_atomic(path: Path, payload: object)`.
- Produces: `evaluate_routing_suite(suite: dict[str, object], indexes: dict[str, object], package_sha256: str) -> dict[str, object]` and `verify_routing_evaluation(pack_root: Path, schema_root: Path, suite_path: Path, report_path: Path) -> dict[str, object]`.

- [ ] **Step 1: Write failing metric and determinism tests**

Use a compact valid fixture with real package endpoints and monkeypatch only `route_query` where a controlled failure is necessary. Assert exact integer numerators, denominators, and percentages for every category. Add tests proving:

```python
def test_verify_routing_evaluation_writes_failure_report_before_raising(
    tmp_path: Path,
) -> None:
    pack_root, schema_root, suite_path, report_path = _evaluation_workspace(tmp_path)
    _replace_one_expected_module_with_a_known_wrong_target(suite_path, pack_root)

    with pytest.raises(KnowledgeForgeError, match="canonical module percent"):
        verify_routing_evaluation(pack_root, schema_root, suite_path, report_path)

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["status"] == "failed"
    assert report["failures"]
```

Also assert that structurally invalid input creates no report, two identical runs create identical bytes, case failures are sorted by ID, a covered result without a module increments `covered_without_module_count`, and the report contains no absolute workspace path.

- [ ] **Step 2: Run the evaluator tests and confirm RED**

Run:

```powershell
uv run pytest -q tests/test_routing_evaluation.py -k "evaluate or verify"
```

Expected: failure because evaluator and verifier functions are not implemented.

- [ ] **Step 3: Implement case comparison and integer metrics**

For each sorted case, call `route_query` exactly once and compare:

- status equality for all cases;
- selected area and exact one-module list for covered cases;
- empty area/module output for negative cases;
- exact sorted area-alternative set for ambiguous cases.

Represent category metrics as:

```python
{
    "passed": passed,
    "total": total,
    "percent": (passed * 100) // total,
}
```

Use integer arithmetic only. A case passes only when its complete expected route matches, while canonical area and canonical module metrics are also counted separately.

- [ ] **Step 4: Implement canonical report identity and verification**

Build the report without timestamps or local paths. Include package and suite digests, declared and actual counts, 193-module coverage, category metrics, per-area counts, covered-without-module count, sorted failures, and failed metric names. Compute:

```python
evaluation_sha256 = sha256_bytes(canonical_json_bytes(report_without_digest))
```

`verify_routing_evaluation` must validate the package through `inspect_package`, load indexes, validate the suite, evaluate it, write the report atomically, then raise `KnowledgeForgeError` after the report write when any threshold fails. A passing report returns normally.

- [ ] **Step 5: Run evaluator tests, the routing suite, and Ruff**

Run:

```powershell
uv run pytest -q tests/test_routing_evaluation.py
uv run pytest -q tests/test_routing.py
uv run ruff check forge/src/knowledge_forge/routing_evaluation.py tests/test_routing_evaluation.py
```

Expected: all tests pass and Ruff is green.

- [ ] **Step 6: Commit the evaluation engine**

```powershell
git add forge/src/knowledge_forge/routing_evaluation.py tests/test_routing_evaluation.py
git commit -m "feat: evaluate routing quality deterministically"
```

---

### Task 3: CLI verification command and boundary behavior

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py`
- Modify: `tests/test_cli_package.py`

**Interfaces:**
- Consumes: `verify_routing_evaluation(pack_root, schema_root, suite_path, report_path)`.
- Produces: CLI command `verify-routing-evaluation --workspace --pack --schemas --suite --report` returning `0` on a passing report and `2` with an actionable error on invalid input or a failed quality gate.

- [ ] **Step 1: Write failing CLI tests**

Add `_routing_evaluation_arguments(workspace: Path) -> list[str]` and tests for a passing copied suite, a quality failure that preserves the report, an absolute suite path rejection, a workspace-escape report path rejection, and a suite symlink rejection where the platform permits symlink creation.

The passing assertion is:

```python
assert run(_routing_evaluation_arguments(workspace)) == 0
report = json.loads(
    (workspace / "private/audit/routing-evaluation.json").read_text(encoding="utf-8")
)
assert report["status"] == "passed"
```

- [ ] **Step 2: Run CLI tests and confirm RED**

Run:

```powershell
uv run pytest -q tests/test_cli_package.py -k "routing_evaluation"
```

Expected: argparse rejects the unknown command.

- [ ] **Step 3: Add parser and dispatch integration**

Add one parser with five required arguments. Resolve all four paths through `resolve_within` before calling the verifier. Do not add optional modes or flags. Preserve the existing `KnowledgeForgeError` to exit-code-2 behavior.

- [ ] **Step 4: Run focused and complete CLI tests**

Run:

```powershell
uv run pytest -q tests/test_cli_package.py -k "routing_evaluation"
uv run pytest -q tests/test_cli_package.py
uv run ruff check forge/src/knowledge_forge/cli.py tests/test_cli_package.py
```

Expected: all tests pass.

- [ ] **Step 5: Commit the CLI boundary**

```powershell
git add forge/src/knowledge_forge/cli.py tests/test_cli_package.py
git commit -m "feat: expose routing evaluation gate"
```

---

### Task 4: Curate the 263-case v1 suite and preserve the unchanged baseline

**Files:**
- Create: `forge/evals/routing-v1.json`
- Modify only if the baseline proves a real defect: `pack/indexes/areas.json`, affected `pack/knowledge/*.md`, `forge/src/knowledge_forge/routing.py`, and their focused tests
- Regenerate only if canonical metadata changes: `pack/indexes/l0.json`, `pack/indexes/l1/*.json`, `pack/graph/canonical.json`, `pack/manifest.json`
- Create ignored: `private/audit/routing-evaluation-v8-baseline.json`
- Create ignored: `private/audit/routing-evaluation-v8.json`

**Interfaces:**
- Consumes: every area and module descriptor in the current package.
- Produces: one reviewed canonical query per module, 40 paraphrases distributed four per area, 20 unsupported queries, and 10 exact cross-area ambiguity cases.

- [ ] **Step 1: Build canonical cases in stable module-ID order**

For every module, write one Hungarian task question that expresses its decision or procedure rather than copying only its title. Use the module's owning area and exact ID as the expected route. Validate that the set of 193 expected module IDs equals the discovered package set and each appears once.

Case IDs use this stable form:

```text
canonical.<module-id-with-dots-preserved>.01
```

- [ ] **Step 2: Add paraphrase, negative, and ambiguity cases**

Add exactly four paraphrases for each of the ten areas. Each paraphrase must avoid merely repeating the exact module title and must still have one defensible target. Add 20 clearly unsupported operational questions with `not-covered`. Add ten genuine cross-area cases whose expected alternatives are sorted and contain at least two known area IDs.

- [ ] **Step 3: Run the suite as the unchanged baseline**

Copy the ignored private marker and audit inputs required by the full gates from the clean `feature` worktree using exact path and SHA-256 verification. Then run:

```powershell
uv run knowledge-forge verify-routing-evaluation `
  --workspace . `
  --pack pack `
  --schemas forge/schemas `
  --suite forge/evals/routing-v1.json `
  --report private/audit/routing-evaluation-v8-baseline.json
```

Expected: either a passing baseline or exit `2` with a deterministic failure report. Preserve that report unchanged.

- [ ] **Step 4: Classify every failure before changing behavior**

For each failed case, assign exactly one root-cause class from the design: expectation error, area term, module term, generic-token false positive, real ambiguity, hidden module tie, or unsupported false route. Fix benchmark expectations only when the selected target was objectively incorrect. Do not weaken thresholds.

- [ ] **Step 5: Apply the smallest justified routing corrections**

Prefer replacing misleading or redundant metadata. Add terms only when all L0/L1 indexes remain within 8192 bytes. Change scoring only when metadata cannot represent the boundary. Every algorithm change receives a focused RED test in `tests/test_routing.py` before implementation.

- [ ] **Step 6: Rebuild and verify package artifacts when needed**

If package metadata changed, run:

```powershell
uv run knowledge-forge build-package --workspace . --pack pack --schemas forge/schemas
uv run knowledge-forge verify-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json
```

Review the manifest and generated diff. Reject unrelated module, graph, index, or formatting churn.

- [ ] **Step 7: Produce the final passing evaluation report**

Run the verifier with `private/audit/routing-evaluation-v8.json`. Inspect all counts and hashes. Require 263 cases, 193/193 canonical targets, all 100% gates, at least 90% paraphrase accuracy, and zero covered-without-module responses.

- [ ] **Step 8: Commit the suite and justified corrections**

Stage the tracked suite, tests, evaluator changes, and only demonstrated package corrections. Confirm that no `private/`, `dist/`, `work/`, `inputs/`, or origin-bearing artifact is staged.

```powershell
git commit -m "feat: add complete routing evaluation suite"
```

---

### Task 5: Full verification, documentation status, and branch delivery

**Files:**
- Modify: `docs/superpowers/specs/2026-08-02-routing-evaluation-v8-design.md`
- Modify: `docs/superpowers/plans/2026-08-02-routing-evaluation-v8.md`
- Preserve ignored: v8 baseline/final reports and two independently built archives

**Interfaces:**
- Consumes: completed tracked v8 implementation and retained private v7 audit inputs.
- Produces: verified v8 commit on synchronized `feature`, retained deterministic reports/archive, and clean `dev-knowledge-map-v9` worktree.

- [ ] **Step 1: Run all automated and private gates in the isolated worktree**

```powershell
uv run pytest -q
uv run ruff check .
uv run knowledge-forge verify-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json
uv run knowledge-forge verify-promotion-coverage --workspace . --pack pack --schemas forge/schemas --units private/normalized/units.jsonl --reviews private/provenance --report private/audit/coverage-v8.json
uv run knowledge-forge verify-unit-disposition --workspace . --pack pack --schemas forge/schemas --units private/normalized/units.jsonl --reviews private/provenance --dispositions private/audit/unit-dispositions-v7.json --report private/audit/unit-coverage-v8.json
uv run knowledge-forge verify-routing-evaluation --workspace . --pack pack --schemas forge/schemas --suite forge/evals/routing-v1.json --report private/audit/routing-evaluation-v8.json
uv run knowledge-forge inspect-package --workspace . --pack pack --schemas forge/schemas
```

Expected: every command exits `0`; package inspection still reports 193 modules, 10 areas, and all L0/L1 indexes at most 8192 bytes.

- [ ] **Step 2: Run neutrality and deterministic archive gates**

Require no matches from the public forbidden-term scan. Build `dist/knowledge-package-v8-a.zip` and `dist/knowledge-package-v8-b.zip` with `archive-package`, compare SHA-256, and fail if they differ.

- [ ] **Step 3: Update design and plan status**

Change the design status to implemented and verified. Mark plan checkboxes complete only after their evidence exists. Run `git diff --check`, placeholder scans, staged-path allowlist review, public leakage review, and secret-pattern review.

- [ ] **Step 4: Commit and push the completed v8 slice**

After a fresh work-state preflight confirms the intended repository, branch, HEAD, worktree, upstream, and target:

```powershell
git commit -m "docs: record verified routing evaluation v8"
git push -u origin dev-knowledge-evolution-v8
```

- [ ] **Step 5: Fast-forward into feature and revalidate**

In the root worktree, fetch and prove `feature == origin/feature` and that `origin/feature` is an ancestor of the dev head. Merge with `git merge --ff-only origin/dev-knowledge-evolution-v8`, copy ignored v8 artifacts with hash verification, rerun the complete tests, Ruff, routing evaluation, package inspection, and archive comparison, then push explicit `feature`.

- [ ] **Step 6: Clean the merged worktree and start v9**

Prove the v8 worktree is clean, the commit is contained in `feature`, and retained ignored artifacts exist in the root workspace. Remove only the exact validated v8 worktree, delete only the merged local v8 branch, and create `dev-knowledge-map-v9` from synchronized `feature`. Run work-state preflight, pytest, and Ruff in the new clean worktree. Leave `main` unchanged.

---

## Plan Self-Review

- Every design requirement maps to a task and a final gate.
- Structural invalidity and quality failure have distinct report behavior.
- All public endpoints are validated before evaluation.
- Integer metrics avoid floating-point and runtime drift.
- The suite cannot silently omit a module or duplicate canonical coverage.
- Baseline measurement precedes routing changes and thresholds are never weakened.
- The near-full L1 index has an explicit non-growth constraint.
- Private reports and archives are retained but never staged or exported.
