# Coding and Evaluation Knowledge v3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the portable Hungarian agent knowledge package from 87 to 122 source-neutral modules with production-grade coding-agent and evaluation guidance.

**Architecture:** A new `coding-agents` L1 area isolates code-centric routing from the core-system area. Evaluation modules extend the existing `evaluation-and-improvement` area. All indexes, graph data, and manifest entries remain forge-generated, while semantic review evidence remains private and ignored.

**Tech Stack:** Python 3.10+, `uv`, PyYAML, jsonschema, pytest, Ruff, Markdown, JSON.

## Global Constraints

- Public `pack/` contains no origin, author, publication, acquisition, private-unit, URL, or workspace references.
- Each new module uses a stable lowercase dot-separated ID, `language: hu`, `maturity: reviewed`, unique aliases, valid relations, and all eight body sections.
- Every L0 and L1 index remains at or below 8192 canonical JSON bytes.
- Private review records remain ignored beneath `private/` and never become package inputs.
- No consuming platform, external benchmark repository, hosted service, model training, or derived map is changed.

---

### Task 1: Define coding and evaluation routes

**Files:**
- Modify: `tests/test_routing.py`
- Modify: `pack/indexes/areas.json`

**Interfaces:**
- Consumes: `route_query(query: str, indexes: dict[str, object]) -> dict[str, object]`.
- Produces: six exact routes and the new `coding-agents` area.

- [x] **Step 1: Add a failing parametrized routing test**

```python
@pytest.mark.parametrize(
    ("query", "area_id", "module_id"),
    [
        ("Hogyan építsek session nélküli coding agentet?", "coding-agents", "pattern.sessionless-coding-agent"),
        ("Hogyan szerkesszen biztonságosan fájlokat egy coding agent?", "coding-agents", "procedure.safe-file-editing"),
        ("Hogyan álljon helyre a coding agent hibás módosítás után?", "coding-agents", "procedure.coding-error-recovery"),
        ("Hogyan kalibráljam az LLM-as-a-judge értékelést?", "evaluation-and-improvement", "procedure.llm-judge-calibration"),
        ("Mekkora mintán statisztikailag szignifikáns az agent javulása?", "evaluation-and-improvement", "procedure.statistical-significance-check"),
        ("Hogyan mérjem egy agent teljes futási költségét?", "evaluation-and-improvement", "procedure.agent-cost-analysis"),
    ],
)
def test_route_query_selects_coding_and_evaluation_module(...):
    ...
```

- [x] **Step 2: Run the test and confirm RED**

Run: `uv run pytest -q tests/test_routing.py::test_route_query_selects_coding_and_evaluation_module`

Expected: FAIL because the area and detailed module IDs do not yet exist.

### Task 2: Add coding-agent operational knowledge

**Files:**
- Create 14 files under `pack/knowledge/` using the IDs below.
- Modify: `pack/indexes/areas.json`

**Interfaces:**
- Consumes: existing harness, safety, tool-contract, evaluation-loop, and experience-improvement modules.
- Produces: a complete `coding-agents` L1 area with fourteen modules.

- [x] **Step 1: Write the coding-agent modules with these required relations**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `principle.code-as-meta-capability` | principle | supports `principle.harness-engineering` |
| `pattern.sessionless-coding-agent` | pattern | depends_on `principle.code-as-meta-capability` |
| `checklist.coding-agent-security` | checklist | supports `checklist.isolated-tool-execution` |
| `procedure.coding-agent-workflow` | procedure | depends_on `pattern.react-observe-act-loop` |
| `checklist.coding-harness-design` | checklist | supports `checklist.harness-function-coverage` |
| `procedure.coding-error-recovery` | procedure | depends_on `procedure.coding-agent-workflow` |
| `procedure.coding-agent-search` | procedure | supports `procedure.coding-agent-workflow` |
| `procedure.safe-file-editing` | procedure | supports `procedure.coding-agent-workflow` |
| `principle.code-as-reasoning-medium` | principle | supports `principle.code-as-meta-capability` |
| `pattern.executable-business-rules` | pattern | supports `procedure.business-rule-compilation` |
| `procedure.code-driven-media-generation` | procedure | applies_to `principle.code-as-meta-capability` |
| `pattern.code-system-adapter` | pattern | supports `procedure.tool-contract-design` |
| `pattern.generative-ui` | pattern | applies_to `principle.code-as-meta-capability` |
| `principle.agent-tool-bootstrapping` | principle | depends_on `principle.code-as-meta-capability` |

- [x] **Step 2: Add `coding-agents` to `areas.json` and assign all fourteen IDs exactly once**

Use aliases `coding agent`, `kódagent`, `kódolás`, `fájlszerkesztés`, `kódgenerálás`, and `session nélküli`.

- [x] **Step 3: Regenerate and verify coding routes**

Run: `uv run knowledge-forge build-package --workspace . --pack pack --schemas forge/schemas` then the coding rows of the Task 1 test.

Expected: PASS with the new L1 index at or below 8192 bytes.

### Task 3: Add evaluation-system knowledge

**Files:**
- Create 21 files under `pack/knowledge/` using the IDs below.
- Modify: `pack/indexes/areas.json`

**Interfaces:**
- Consumes: existing evaluation environment, metric selection, observability, ablation, task-distribution, and release-loop modules.
- Produces: twenty-one evaluation modules assigned to `evaluation-and-improvement`.

- [x] **Step 1: Write environment and dataset modules**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `experiment.task-success-baseline` | experiment | validated_by `procedure.agent-evaluation-loop` |
| `checklist.evaluation-environment-components` | checklist | supports `procedure.evaluation-environment-design` |
| `procedure.tool-evaluation-environment` | procedure | depends_on `procedure.evaluation-environment-design` |
| `procedure.hci-evaluation-environment` | procedure | depends_on `procedure.evaluation-environment-design` |
| `procedure.evaluation-task-specification` | procedure | supports `procedure.evaluation-environment-design` |
| `pattern.task-complexity-ladder` | pattern | supports `pattern.task-distribution-coverage` |
| `checklist.objective-verifiability` | checklist | supports `procedure.evaluation-task-specification` |
| `procedure.dataset-quality-loop` | procedure | depends_on `pattern.task-distribution-coverage` |

- [x] **Step 2: Write metrics, model-selection, and improvement modules**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `concept.evaluation-metric-stack` | concept | supports `decision-guide.metric-selection` |
| `procedure.llm-judge-calibration` | procedure | depends_on `decision-guide.metric-selection` |
| `procedure.pairwise-model-ranking` | procedure | supports `decision-guide.agent-model-selection` |
| `decision-guide.model-selection-dimensions` | decision-guide | supports `decision-guide.agent-model-selection` |
| `procedure.agent-cost-analysis` | procedure | supports `decision-guide.model-selection-dimensions` |
| `procedure.statistical-significance-check` | procedure | supports `procedure.agent-evaluation-loop` |
| `procedure.benchmark-error-analysis` | procedure | supports `procedure.ablation-and-experiment-loop` |
| `procedure.improvement-hypothesis-roadmap` | procedure | depends_on `procedure.benchmark-error-analysis` |
| `pattern.two-layer-feature-flags` | pattern | supports `procedure.continual-improvement-release-loop` |
| `procedure.prompt-sensitivity-assessment` | procedure | supports `procedure.ablation-and-experiment-loop` |
| `checklist.privacy-aware-analytics` | checklist | supports `checklist.agent-observability` |
| `decision-guide.simulation-fidelity` | decision-guide | supports `procedure.evaluation-environment-design` |
| `pattern.domain-randomization` | pattern | supports `decision-guide.simulation-fidelity` |

- [x] **Step 3: Assign all modules, regenerate, and run routing, graph, manifest, and budget checks**

Run: `uv run pytest -q tests/test_routing.py tests/test_manifest.py tests/test_package.py`.

Expected: 122 modules, valid graph endpoints, exact package membership, and every index within budget.

### Task 4: Review, archive, and integrate

**Files:**
- Modify generated `pack/indexes/**`, `pack/graph/canonical.json`, and `pack/manifest.json`.
- Create locally only: `private/provenance/promotion-map-v3.json`.
- Create locally only: `dist/knowledge-package-v3.zip`.
- Modify: this plan and the design status.

**Interfaces:**
- Consumes: all 122 modules and private normalized units.
- Produces: validated public package, private review evidence, deterministic archive, and integrated `feature` head.

- [x] **Step 1: Map all 35 new module IDs to reviewed normalized units and verify both endpoint sets**

- [x] **Step 2: Validate neutrality and deterministic archive construction with private markers**

Run `verify-package`, build two archives, and compare SHA-256 digests.

- [x] **Step 3: Run the full suite, Ruff, staged-scope review, and public-boundary scan**

- [x] **Step 4: Commit, push, fast-forward merge into `feature`, revalidate, preserve ignored artifacts, and clean the merged worktree**

## Plan Self-Review

### Spec coverage

The plan adds production coding-agent knowledge, rigorous evaluation knowledge, exact routing, progressive-disclosure budgets, private traceability, deterministic export, and branch integration without touching a consuming platform.

### Placeholder scan

All 35 module IDs, relations, routing queries, area ownership, verification commands, and artifacts are explicit. No public content depends on an unspecified external service.

### Type consistency

All modules use the existing `KnowledgeModule` contract. `areas.json` remains the sole ownership declaration and all derived artifacts remain forge-generated.
