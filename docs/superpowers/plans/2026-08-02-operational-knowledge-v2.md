# Operational Knowledge v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the portable Hungarian agent knowledge package from 51 to 87 source-neutral modules with operational guidance for system design, context, memory, retrieval, and tools.

**Architecture:** The public corpus remains Markdown L2 modules with stable metadata. The existing five L1 areas own every new module exactly once; the forge regenerates all derived indexes, graph, and manifest. Private review mapping remains ignored and is never a package input.

**Tech Stack:** Python 3.10+, `uv`, PyYAML, jsonschema, pytest, Ruff, Markdown, JSON.

## Global Constraints

- Public `pack/` contains no origin, author, publication, acquisition, private-unit, URL, or workspace references.
- Each new module uses a stable lowercase dot-separated ID, `language: hu`, `maturity: reviewed`, a non-ambiguous alias, a valid relation, and all eight body sections.
- `pack/**` remains LF-only; generated indexes, graph, and manifest are created only through the forge.
- Private review records remain ignored beneath `private/` and are validated for leakage but never exported.
- No consuming platform, hosted retrieval service, embedding index, model training, or derived tool map is changed.

---

### Task 1: Define observable operational routing behaviour

**Files:**
- Modify: `tests/test_routing.py`

**Interfaces:**
- Consumes: `route_query(query: str, indexes: dict[str, object]) -> dict[str, object]` and the package built from `pack/`.
- Produces: six end-user routing assertions that resolve to exactly one detailed module.

- [x] **Step 1: Add the failing routing table**

```python
@pytest.mark.parametrize(
    ("query", "area_id", "module_id"),
    [
        ("Hogyan válasszak modellt egy eszközhasználó agenthez?", "core-agent-systems", "decision-guide.agent-model-selection"),
        ("Hova kerüljön a stabil kontextus a cache találati arányához?", "context-and-knowledge", "procedure.cache-stable-context-layout"),
        ("Milyen memóriaszinteket kezeljek egy felhasználóhoz?", "context-and-knowledge", "pattern.memory-hierarchy"),
        ("Mikor egyesítsem a sűrű és ritka keresési találatokat?", "context-and-knowledge", "procedure.hybrid-retrieval-fusion"),
        ("Mikor készítsek dedikált eszközt skill és általános végrehajtó helyett?", "tool-execution", "decision-guide.tool-or-skill-executor"),
        ("Hogyan kommunikáljak a felhasználóval hosszú aszinkron futás közben?", "tool-execution", "procedure.user-communication-during-async-execution"),
    ],
)
def test_route_query_selects_operational_module(...):
    ...
```

- [x] **Step 2: Run the table and confirm that every new route is absent before promotion**

Run: `uv run pytest -q tests/test_routing.py::test_route_query_selects_operational_module`

Expected: FAIL because the six detailed module IDs are not yet exported.

### Task 2: Promote core, context, and memory knowledge

**Files:**
- Create: `pack/knowledge/concept.observation-action-interface.md`
- Create: `pack/knowledge/decision-guide.agent-model-selection.md`
- Create: `pack/knowledge/checklist.harness-function-coverage.md`
- Create: `pack/knowledge/procedure.guardrail-design.md`
- Create: `pack/knowledge/procedure.human-escalation-design.md`
- Create: `pack/knowledge/concept.api-message-context-model.md`
- Create: `pack/knowledge/procedure.cache-stable-context-layout.md`
- Create: `pack/knowledge/pattern.editable-context-notes.md`
- Create: `pack/knowledge/procedure.prompt-structure-design.md`
- Create: `pack/knowledge/decision-guide.process-instructions-or-rule-stack.md`
- Create: `pack/knowledge/procedure.business-rule-compilation.md`
- Create: `pack/knowledge/decision-guide.few-shot-example-selection.md`
- Create: `pack/knowledge/procedure.status-signal-design.md`
- Create: `pack/knowledge/decision-guide.status-update-placement.md`
- Create: `pack/knowledge/concept.context-isolation-strategy.md`
- Create: `pack/knowledge/decision-guide.memory-capability-evaluation.md`
- Create: `pack/knowledge/pattern.memory-hierarchy.md`
- Create: `pack/knowledge/decision-guide.memory-representation-selection.md`
- Create: `pack/knowledge/checklist.memory-privacy-sanitization.md`
- Create: `pack/knowledge/procedure.memory-consolidation.md`
- Modify: `pack/indexes/areas.json`

**Interfaces:**
- Consumes: the module schema plus existing agent operating model, context boundary, prompt architecture, memory lifecycle, and safety modules.
- Produces: twenty source-neutral modules assigned exactly once to `core-agent-systems` or `context-and-knowledge`.

- [x] **Step 1: Write the five core-system modules with these relations**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `concept.observation-action-interface` | concept | supports `principle.agent-operating-model` |
| `decision-guide.agent-model-selection` | decision-guide | depends_on `principle.harness-engineering` |
| `checklist.harness-function-coverage` | checklist | supports `principle.harness-engineering` |
| `procedure.guardrail-design` | procedure | supports `checklist.tool-safety-boundary` |
| `procedure.human-escalation-design` | procedure | depends_on `procedure.guardrail-design` |

- [x] **Step 2: Write the ten context-design modules with these relations**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `concept.api-message-context-model` | concept | supports `procedure.system-prompt-architecture` |
| `procedure.cache-stable-context-layout` | procedure | depends_on `concept.context-cache-architecture` |
| `pattern.editable-context-notes` | pattern | supports `procedure.cache-stable-context-layout` |
| `procedure.prompt-structure-design` | procedure | depends_on `procedure.system-prompt-architecture` |
| `decision-guide.process-instructions-or-rule-stack` | decision-guide | depends_on `procedure.prompt-structure-design` |
| `procedure.business-rule-compilation` | procedure | supports `procedure.prompt-structure-design` |
| `decision-guide.few-shot-example-selection` | decision-guide | supports `procedure.system-prompt-architecture` |
| `procedure.status-signal-design` | procedure | supports `pattern.agent-status-representation` |
| `decision-guide.status-update-placement` | decision-guide | depends_on `procedure.status-signal-design` |
| `concept.context-isolation-strategy` | concept | supports `pattern.hierarchical-context-compression` |

- [x] **Step 3: Write the five memory modules with these relations**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `decision-guide.memory-capability-evaluation` | decision-guide | supports `procedure.user-memory-lifecycle` |
| `pattern.memory-hierarchy` | pattern | depends_on `procedure.user-memory-lifecycle` |
| `decision-guide.memory-representation-selection` | decision-guide | depends_on `pattern.memory-hierarchy` |
| `checklist.memory-privacy-sanitization` | checklist | supports `procedure.user-memory-lifecycle` |
| `procedure.memory-consolidation` | procedure | depends_on `pattern.memory-hierarchy` |

- [x] **Step 4: Add each module to exactly one of the two owning areas and run structural checks**

Run: `uv run pytest -q tests/test_frontmatter.py tests/test_package.py`

Expected: PASS with every new identifier, relation endpoint, body section, and ownership declaration valid.

### Task 3: Promote retrieval and tool-operation knowledge

**Files:**
- Create: `pack/knowledge/procedure.document-chunking-strategy.md`
- Create: `pack/knowledge/concept.dense-retrieval.md`
- Create: `pack/knowledge/concept.sparse-retrieval.md`
- Create: `pack/knowledge/procedure.hybrid-retrieval-fusion.md`
- Create: `pack/knowledge/decision-guide.multimodal-information-processing.md`
- Create: `pack/knowledge/pattern.filesystem-knowledge-organization.md`
- Create: `pack/knowledge/checklist.knowledge-freshness-governance.md`
- Create: `pack/knowledge/pattern.agentic-retrieval-control.md`
- Create: `pack/knowledge/pattern.contextual-retrieval.md`
- Create: `pack/knowledge/decision-guide.tool-or-skill-executor.md`
- Create: `pack/knowledge/principle.tool-interface-fidelity.md`
- Create: `pack/knowledge/procedure.mcp-tool-selection.md`
- Create: `pack/knowledge/concept.perception-execution-collaboration-tools.md`
- Create: `pack/knowledge/procedure.user-communication-during-async-execution.md`
- Create: `pack/knowledge/checklist.isolated-tool-execution.md`
- Create: `pack/knowledge/procedure.proactive-tool-discovery.md`
- Modify: `pack/indexes/areas.json`

**Interfaces:**
- Consumes: existing retrieval pipeline, knowledge index, tool contract, capability taxonomy, and asynchronous execution modules.
- Produces: nine context-and-knowledge and seven tool-execution modules with valid directed graph edges.

- [x] **Step 1: Write the nine retrieval modules with these relations**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `procedure.document-chunking-strategy` | procedure | supports `procedure.retrieval-pipeline-design` |
| `concept.dense-retrieval` | concept | supports `decision-guide.retrieval-strategy-selection` |
| `concept.sparse-retrieval` | concept | supports `decision-guide.retrieval-strategy-selection` |
| `procedure.hybrid-retrieval-fusion` | procedure | depends_on `decision-guide.retrieval-strategy-selection` |
| `decision-guide.multimodal-information-processing` | decision-guide | supports `procedure.retrieval-pipeline-design` |
| `pattern.filesystem-knowledge-organization` | pattern | supports `concept.structured-knowledge-index` |
| `checklist.knowledge-freshness-governance` | checklist | supports `concept.structured-knowledge-index` |
| `pattern.agentic-retrieval-control` | pattern | depends_on `procedure.retrieval-pipeline-design` |
| `pattern.contextual-retrieval` | pattern | supports `procedure.hybrid-retrieval-fusion` |

- [x] **Step 2: Write the seven tool-operation modules with these relations**

| Module ID | Kind | Required relation |
| --- | --- | --- |
| `decision-guide.tool-or-skill-executor` | decision-guide | depends_on `concept.tool-capability-taxonomy` |
| `principle.tool-interface-fidelity` | principle | supports `procedure.tool-contract-design` |
| `procedure.mcp-tool-selection` | procedure | depends_on `pattern.tool-discovery` |
| `concept.perception-execution-collaboration-tools` | concept | supports `concept.tool-capability-taxonomy` |
| `procedure.user-communication-during-async-execution` | procedure | depends_on `pattern.event-driven-agent-execution` |
| `checklist.isolated-tool-execution` | checklist | supports `checklist.tool-safety-boundary` |
| `procedure.proactive-tool-discovery` | procedure | supports `pattern.tool-discovery` |

- [x] **Step 3: Run routing and graph checks**

Run: `uv run pytest -q tests/test_routing.py tests/test_manifest.py`

Expected: all six operational routes resolve to exactly one area and detailed module, and every relation endpoint resolves.

### Task 4: Regenerate, review, validate, archive, and integrate

**Files:**
- Modify: `pack/indexes/l0.json`
- Modify: `pack/indexes/l1/*.json`
- Modify: `pack/graph/canonical.json`
- Modify: `pack/manifest.json`
- Modify locally only: `private/provenance/promotion-map-v2.json`
- Modify locally only: `dist/knowledge-package-v2.zip`
- Modify: `docs/superpowers/specs/2026-08-02-portable-agent-knowledge-forge-design.md`
- Modify: `docs/superpowers/plans/2026-08-02-operational-knowledge-v2.md`

**Interfaces:**
- Consumes: all 87 modules, the five area declarations, and private semantic review data.
- Produces: generated public routing artifacts, a validated portable archive, and ignored private review evidence.

- [x] **Step 1: Regenerate the public artifacts**

Run: `uv run knowledge-forge build-package --workspace . --pack pack --schemas forge/schemas`

Expected: the L0/L1 indexes, canonical graph, and manifest are derived from the 87 modules.

- [x] **Step 2: Refresh and verify ignored private review evidence**

Create `private/provenance/promotion-map-v2.json` mapping every newly promoted ID to relevant private normalized units. Verify all recorded public IDs and private unit IDs resolve, without copying private text into `pack/`.

- [x] **Step 3: Validate package, archive determinism, and quality gates**

Run:

```powershell
uv run knowledge-forge verify-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json
uv run knowledge-forge archive-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json --archive dist/knowledge-package-v2.zip
uv run pytest -q
uv run ruff check .
```

Expected: all checks pass, private paths remain ignored, and the public archive contains only manifest-allowlisted package files.

- [x] **Step 4: Commit, push, fast-forward merge into feature, and validate the merged result**

Commit only public modules, generated public artifacts, tests, and plan/spec updates. Push `dev-operational-knowledge-v2`, fast-forward merge into `feature`, rebuild the archive from the merged head, and rerun the full suite.

## Plan Self-Review

### Spec coverage

The plan expands the source-neutral L2 corpus with operational knowledge, preserves the five-area ownership and progressive disclosure model, keeps private review isolated, and verifies routing, graph integrity, manifest integrity, and archive portability.

### Placeholder scan

Every promoted module, area, relation target, route, generated artifact, and verification command is named explicitly. The private review map is intentionally excluded from public content and is verified by identifier only.

### Type consistency

All modules retain the existing `KnowledgeModule` front matter and eight-section Markdown body. Area ownership remains in `areas.json`; derived indexes, graph, and manifest remain forge-generated.
