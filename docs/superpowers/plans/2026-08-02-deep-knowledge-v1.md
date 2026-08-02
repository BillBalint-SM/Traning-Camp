# Deep Knowledge v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the portable Hungarian agent knowledge package from 15 to 51 source-neutral modules while preserving deterministic routing, graph integrity, and archive portability.

**Architecture:** The public corpus remains Markdown L2 modules with stable metadata. Five L1 areas own every module exactly once; the forge regenerates indexes, graph, and manifest from those declarations. Private semantic review mappings remain under ignored `private/` paths and never become package inputs.

**Tech Stack:** Python 3.10+, `uv`, PyYAML, jsonschema, pytest, Ruff, Markdown, JSON.

## Global Constraints

- Public `pack/` content contains no origin, author, publication, acquisition, chapter, private-unit, URL, or workspace references.
- New module IDs are stable lowercase dot-separated identifiers; all new modules use `language: hu`, `maturity: reviewed`, and explicit verification criteria.
- Each public module has all eight required body sections and at least one non-ambiguous alias.
- `pack/**` stays LF-only so byte-level manifest validation is portable on Windows.
- No consumer platform, hosted retrieval service, model training, or derived tool map is changed in this delivery.
- The package must remain valid when relocated and when archived.

---

### Task 1: Define observable deep-routing behaviour

**Files:**
- Modify: `tests/test_routing.py`

**Interfaces:**
- Consumes: `route_query(query: str, indexes: dict[str, object]) -> dict[str, object]` and the package built from `pack/`.
- Produces: five real, end-user routing assertions that fail until the deep modules and L1 aliases exist.

- [x] **Step 1: Add the failing routing table**

```python
@pytest.mark.parametrize(
    ("query", "area_id", "module_id"),
    [
        (
            "Mikor válasszak determinisztikus workflow-t autonóm döntéshozatal helyett?",
            "core-agent-systems",
            "decision-guide.workflow-or-autonomy",
        ),
        (
            "Mikor kell hibrid retrievalt használnom a tudás visszakereséséhez?",
            "context-and-knowledge",
            "decision-guide.retrieval-strategy-selection",
        ),
        (
            "Hogyan szakítsak meg biztonságosan egy aszinkron agent futást?",
            "tool-execution",
            "procedure.async-interruption-handling",
        ),
        (
            "Milyen agent observability jeleket gyűjtsek?",
            "evaluation-and-improvement",
            "checklist.agent-observability",
        ),
        (
            "Mit tartalmazzon egy több agent közötti átadási szerződés?",
            "interaction-and-collaboration",
            "procedure.multi-agent-handoff-contract",
        ),
    ],
)
def test_route_query_selects_deep_module(
    query: str, area_id: str, module_id: str
) -> None:
    result = route_query(query, _indexes())

    assert result == {
        "status": "covered",
        "area_id": area_id,
        "module_ids": [module_id],
    }
```

- [x] **Step 2: Confirm the test fails because the deep routes do not exist**

Run: `uv run pytest -v tests/test_routing.py::test_route_query_selects_deep_module`

Expected: the current package returns `not-covered` or a different route for at least one declared deep query.

### Task 2: Add core-system and context-knowledge modules

**Files:**
- Create: `pack/knowledge/principle.harness-engineering.md`
- Create: `pack/knowledge/pattern.react-observe-act-loop.md`
- Create: `pack/knowledge/decision-guide.workflow-or-autonomy.md`
- Create: `pack/knowledge/checklist.agent-task-contract.md`
- Create: `pack/knowledge/pattern.agent-status-representation.md`
- Create: `pack/knowledge/failure-mode.model-only-system-design.md`
- Create: `pack/knowledge/concept.context-cache-architecture.md`
- Create: `pack/knowledge/procedure.system-prompt-architecture.md`
- Create: `pack/knowledge/checklist.prompt-injection-boundary.md`
- Create: `pack/knowledge/pattern.dynamic-skill-loading.md`
- Create: `pack/knowledge/pattern.hierarchical-context-compression.md`
- Create: `pack/knowledge/procedure.retrieval-pipeline-design.md`
- Create: `pack/knowledge/decision-guide.retrieval-strategy-selection.md`
- Create: `pack/knowledge/concept.structured-knowledge-index.md`

**Interfaces:**
- Consumes: the knowledge-module schema and existing `principle.agent-operating-model`, `principle.context-is-finite`, and `pattern.context-compression` modules.
- Produces: six core-system and eight context-knowledge modules connected to their prerequisites with only valid graph relation types.

- [x] **Step 1: Write the six core-system modules**

Use the required eight-section module body. Apply this identity and relation map:

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `principle.harness-engineering` | principle | supports `principle.agent-operating-model` |
| `pattern.react-observe-act-loop` | pattern | depends_on `principle.agent-operating-model` |
| `decision-guide.workflow-or-autonomy` | decision-guide | depends_on `principle.harness-engineering` |
| `checklist.agent-task-contract` | checklist | supports `decision-guide.workflow-or-autonomy` |
| `pattern.agent-status-representation` | pattern | supports `pattern.react-observe-act-loop` |
| `failure-mode.model-only-system-design` | failure-mode | contrasts_with `principle.harness-engineering` |

- [x] **Step 2: Write the eight context and knowledge modules**

Use this identity and relation map:

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `concept.context-cache-architecture` | concept | depends_on `principle.context-is-finite` |
| `procedure.system-prompt-architecture` | procedure | supports `principle.harness-engineering` |
| `checklist.prompt-injection-boundary` | checklist | supports `procedure.system-prompt-architecture` |
| `pattern.dynamic-skill-loading` | pattern | supports `procedure.system-prompt-architecture` |
| `pattern.hierarchical-context-compression` | pattern | depends_on `pattern.context-compression` |
| `procedure.retrieval-pipeline-design` | procedure | supports `decision-guide.memory-vs-retrieval` |
| `decision-guide.retrieval-strategy-selection` | decision-guide | depends_on `procedure.retrieval-pipeline-design` |
| `concept.structured-knowledge-index` | concept | supports `procedure.retrieval-pipeline-design` |

- [x] **Step 3: Run structural parsing before changing area declarations**

Run: `uv run pytest -v tests/test_frontmatter.py tests/test_package.py`

Expected: module parsing, uniqueness, and relation target checks pass.

### Task 3: Add tool-execution and evaluation-improvement modules

**Files:**
- Create: `pack/knowledge/concept.tool-capability-taxonomy.md`
- Create: `pack/knowledge/decision-guide.tool-granularity.md`
- Create: `pack/knowledge/pattern.event-driven-agent-execution.md`
- Create: `pack/knowledge/procedure.async-interruption-handling.md`
- Create: `pack/knowledge/checklist.tool-result-verification.md`
- Create: `pack/knowledge/failure-mode.unsafe-tool-expansion.md`
- Create: `pack/knowledge/procedure.evaluation-environment-design.md`
- Create: `pack/knowledge/pattern.task-distribution-coverage.md`
- Create: `pack/knowledge/checklist.agent-observability.md`
- Create: `pack/knowledge/decision-guide.metric-selection.md`
- Create: `pack/knowledge/procedure.ablation-and-experiment-loop.md`
- Create: `pack/knowledge/pattern.sft-rl-learning-boundary.md`
- Create: `pack/knowledge/principle.environment-data-before-algorithm.md`
- Create: `pack/knowledge/procedure.continual-improvement-release-loop.md`

**Interfaces:**
- Consumes: the existing tool contract, safety boundary, evaluation loop, post-training, and experience-improvement modules.
- Produces: tool lifecycle coverage and a measurement-first improvement loop without silently treating a model-weight change as a runtime configuration change.

- [x] **Step 1: Write the six tool-execution modules**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `concept.tool-capability-taxonomy` | concept | supports `procedure.tool-contract-design` |
| `decision-guide.tool-granularity` | decision-guide | depends_on `concept.tool-capability-taxonomy` |
| `pattern.event-driven-agent-execution` | pattern | applies_to `procedure.tool-contract-design` |
| `procedure.async-interruption-handling` | procedure | depends_on `pattern.event-driven-agent-execution` |
| `checklist.tool-result-verification` | checklist | supports `checklist.tool-safety-boundary` |
| `failure-mode.unsafe-tool-expansion` | failure-mode | contrasts_with `decision-guide.tool-granularity` |

- [x] **Step 2: Write the eight evaluation and improvement modules**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `procedure.evaluation-environment-design` | procedure | supports `procedure.agent-evaluation-loop` |
| `pattern.task-distribution-coverage` | pattern | depends_on `procedure.evaluation-environment-design` |
| `checklist.agent-observability` | checklist | supports `procedure.agent-evaluation-loop` |
| `decision-guide.metric-selection` | decision-guide | depends_on `procedure.agent-evaluation-loop` |
| `procedure.ablation-and-experiment-loop` | procedure | depends_on `decision-guide.metric-selection` |
| `pattern.sft-rl-learning-boundary` | pattern | supports `decision-guide.sft-or-rl` |
| `principle.environment-data-before-algorithm` | principle | supports `pattern.sft-rl-learning-boundary` |
| `procedure.continual-improvement-release-loop` | procedure | depends_on `pattern.experience-driven-improvement` |

- [x] **Step 3: Run focused routing and graph tests**

Run: `uv run pytest -v tests/test_routing.py tests/test_manifest.py`

Expected: the new asynchrony and observability routes resolve through real package indexes; graph endpoints and manifest checks remain valid after regeneration in Task 5.

### Task 4: Add interaction-collaboration modules and assign every module

**Files:**
- Create: `pack/knowledge/decision-guide.voice-architecture-selection.md`
- Create: `pack/knowledge/pattern.fast-slow-interaction-loop.md`
- Create: `pack/knowledge/procedure.gui-action-grounding.md`
- Create: `pack/knowledge/principle.planning-control-separation.md`
- Create: `pack/knowledge/decision-guide.multi-agent-topology-selection.md`
- Create: `pack/knowledge/procedure.multi-agent-handoff-contract.md`
- Create: `pack/knowledge/checklist.shared-state-concurrency-control.md`
- Create: `pack/knowledge/failure-mode.multi-agent-error-amplification.md`
- Modify: `pack/indexes/areas.json`

**Interfaces:**
- Consumes: existing multimodal boundary, multi-agent context-boundary, and autonomy-safety modules.
- Produces: eight interaction modules plus a complete five-area module assignment that `build_indexes` accepts exactly once per module.

- [x] **Step 1: Write the eight interaction and collaboration modules**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `decision-guide.voice-architecture-selection` | decision-guide | applies_to `concept.multimodal-interaction-boundary` |
| `pattern.fast-slow-interaction-loop` | pattern | supports `decision-guide.voice-architecture-selection` |
| `procedure.gui-action-grounding` | procedure | depends_on `concept.multimodal-interaction-boundary` |
| `principle.planning-control-separation` | principle | supports `procedure.gui-action-grounding` |
| `decision-guide.multi-agent-topology-selection` | decision-guide | depends_on `pattern.multi-agent-context-boundaries` |
| `procedure.multi-agent-handoff-contract` | procedure | supports `decision-guide.multi-agent-topology-selection` |
| `checklist.shared-state-concurrency-control` | checklist | prevents `failure-mode.multi-agent-error-amplification` |
| `failure-mode.multi-agent-error-amplification` | failure-mode | contrasts_with `decision-guide.multi-agent-topology-selection` |

- [x] **Step 2: Replace `areas.json` with the five complete assignments**

Keep the existing five area IDs. Add aliases necessary for the Task 1 queries without making `MCP vagy több ügynök együttműködés?` route to any area beyond `tool-execution` and `interaction-and-collaboration`. Assign exactly these new modules:

| Area | New modules |
| --- | --- |
| `core-agent-systems` | all six Task 2 core modules |
| `context-and-knowledge` | all eight Task 2 context modules |
| `tool-execution` | all six Task 3 tool modules |
| `evaluation-and-improvement` | all eight Task 3 evaluation modules |
| `interaction-and-collaboration` | all eight Task 4 interaction modules |

- [x] **Step 3: Run the deep routing test and graph construction test**

Run: `uv run pytest -v tests/test_routing.py::test_route_query_selects_deep_module tests/test_routing.py::test_build_graph_resolves_every_edge`

Expected: all five declared end-user queries return exactly one correct area and detailed module.

### Task 5: Regenerate, semantically review, validate, archive, and deliver

**Files:**
- Modify: `pack/indexes/l0.json`
- Modify: `pack/indexes/l1/*.json`
- Modify: `pack/graph/canonical.json`
- Modify: `pack/manifest.json`
- Create locally only: `private/provenance/promotion-map-v1.json`
- Create locally only: `private/leakage/markers.json`
- Create locally only: `dist/knowledge-package-v1.zip`
- Modify: `docs/superpowers/specs/2026-08-02-portable-agent-knowledge-forge-design.md`
- Modify: `docs/superpowers/plans/2026-08-02-deep-knowledge-v1.md`

**Interfaces:**
- Consumes: all 51 modules, `areas.json`, and local private review material.
- Produces: generated routing indexes, canonical graph, byte-accurate manifest, a verified archive, and a private promotion map from each new module ID to reviewed normalized units.

- [x] **Step 1: Regenerate public derived package artifacts**

Run:

```powershell
uv run knowledge-forge build-package --workspace . --pack pack --schemas forge/schemas
```

Expected: `l0.json`, all five L1 indexes, `canonical.json`, and `manifest.json` are regenerated from the trusted modules.

- [x] **Step 2: Create and verify the local semantic review map**

Create an ignored `private/provenance/promotion-map-v1.json` that maps all 36 new IDs to relevant normalized unit IDs. Reuse the locally verified marker set only under ignored `private/leakage/markers.json`. Do not copy private content, titles, or unit IDs into `pack/`.

- [x] **Step 3: Verify the full public package and deterministic archive**

Run:

```powershell
uv run knowledge-forge verify-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json
uv run knowledge-forge archive-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json --archive dist/knowledge-package-v1.zip
uv run knowledge-forge archive-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json --archive dist/knowledge-package-v1-repeat.zip
Get-FileHash dist/knowledge-package-v1.zip, dist/knowledge-package-v1-repeat.zip -Algorithm SHA256
```

Expected: both archive hashes are identical; only package allowlist members are present; relocated-package validation remains green.

- [x] **Step 4: Run all quality gates and inspect public boundaries**

Run:

```powershell
uv run pytest -v
uv run ruff check .
git check-ignore -v -- inputs private work derived dist .worktrees
git diff --check feature...HEAD
git diff --stat feature...HEAD
```

Expected: every test and lint check passes, all private paths are ignored, and the tracked diff contains only public package, test, and status-plan changes.

- [x] **Step 5: Record completion, commit, push, and fast-forward merge**

Set this plan's task checkboxes to complete and update the design status only after all quality gates pass. Commit the delivery, push `dev-deep-knowledge-v1`, fast-forward merge it into `feature`, rerun the full suite from `feature`, and create the next scoped `dev` branch from that verified head.

## Plan Self-Review

### Spec coverage

- Semantic corpus expansion and Hungarian source-neutral L2 modules: Tasks 2–4.
- Stable metadata, complete area ownership, route behaviour, and canonical graph: Tasks 1–4.
- Private semantic review isolation, leakage validation, relocation, archive determinism, and package boundaries: Task 5.
- Local-first delivery and only later-derived mapping tools: preserved by the global constraints.

### Placeholder scan

Every module ID, kind, area, required relation, test route, generated artifact, and verification command is named explicitly. No public content is delegated to an unspecified external service.

### Type consistency

All modules retain the `KnowledgeModule` contract. `areas.json` is the sole ownership declaration consumed by `build_indexes`; generated index, graph, and manifest files remain derived from that canonical public data.
