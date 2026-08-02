# Derived Knowledge Map v9 Implementation Plan

> **Execution route:** Use `superpowers:executing-plans`, `superpowers:test-driven-development`, `understand-anything:understand-knowledge`, and `superpowers:verification-before-completion` task by task.

**Goal:** Produce a deterministic, ignored Karpathy-wiki projection of all 193 public modules and prove it with the real Understand Anything parser without changing the canonical package.

**Architecture:** A functional projection builder validates public package indexes and graph data, renders one deterministic index plus one article per module, records canonical file hashes, and atomically publishes only beneath `derived/`. The UA parser consumes the projection afterward and remains outside the canonical build path.

**Tech Stack:** Python 3.10+, existing canonical JSON/SHA-256 helpers, pytest, Ruff, Understand Anything 2.9.4 knowledge parser.

## Global constraints

- Read only `pack/` and `forge/schemas/`; never read private intake or provenance.
- Write only beneath a caller-selected, non-existing `derived/` child.
- Do not modify or package generated UA artifacts.
- Preserve all 193 module IDs, 10 area IDs, and 196 typed canonical relations.
- Produce no timestamps, absolute paths, random IDs, or environment-specific bytes.
- Treat the canonical graph as authoritative and UA output as derived.
- Keep `main` unchanged; deliver `dev-knowledge-map-v9` only to `feature`.

---

### Task 1: Record the contract and failing compatibility evidence

**Files:**
- Create: `docs/superpowers/specs/2026-08-02-derived-knowledge-map-v9-design.md`
- Create: `docs/superpowers/plans/2026-08-02-derived-knowledge-map-v9.md`
- Preserve ignored: `derived/ua-input-v9/`

- [x] Reproduce the unchanged projection attempt with the real UA parser.
- [x] Require exit `1`, `has_index: false`, `md_count: 193`, and no scan manifest.
- [x] Record canonical/derived boundaries, safety rules, exact counts, and acceptance criteria.
- [x] Review the documents for origin neutrality and commit the approved plan.

---

### Task 2: Define rendering and validation behavior with RED tests

**Files:**
- Create: `tests/test_knowledge_map.py`

- [ ] Add a fixture that copies the real validated package into `tmp_path`.
- [ ] Specify exact `index.md` sections, module links, H1 insertion, and outgoing typed relation links.
- [ ] Require 193 articles, 10 areas, 196 relation links, and exact module ownership.
- [ ] Require identical bytes from two independent builds.
- [ ] Mutate graph/index fixtures to prove explicit failure for missing endpoints, duplicate edges, self edges, content-hash mismatch, and module-set mismatch.
- [ ] Require an existing output directory to remain untouched on failure.
- [ ] Run `uv run pytest -q tests/test_knowledge_map.py` and preserve the expected import failure.

---

### Task 3: Implement the deterministic projection builder

**Files:**
- Create: `forge/src/knowledge_forge/knowledge_map.py`
- Modify: `tests/test_knowledge_map.py`

- [ ] Implement pure loaders for areas, graph nodes/edges, and module bytes.
- [ ] Implement exact cross-artifact validation before rendering.
- [ ] Implement pure index, H1, and relation-section renderers.
- [ ] Build a complete file map in memory and hash canonical output bytes.
- [ ] Write through a sibling temporary directory, verify every output, then rename to the non-existing target.
- [ ] On failure, remove only the exact temporary directory created by the current invocation.
- [ ] Run focused tests and Ruff until green.
- [ ] Commit the builder as one cohesive change.

---

### Task 4: Expose a guarded CLI boundary

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py`
- Modify: `tests/test_cli_package.py`

- [ ] Add RED tests for success, existing output, absolute path, traversal, output outside `derived/`, symlink output, and symlink ancestor.
- [ ] Add `build-knowledge-map-projection --workspace --pack --schemas --output`.
- [ ] Resolve package/schema paths within the workspace and validate output lexically and physically beneath `derived/`.
- [ ] Preserve actionable `KnowledgeForgeError` to exit-code-2 behavior without absolute-path leakage.
- [ ] Run focused CLI tests, the complete CLI suite, and Ruff.
- [ ] Commit the CLI boundary.

---

### Task 5: Build twice and verify with Understand Anything

**Ignored outputs:**
- Create: `derived/knowledge-map-v9-a/`
- Create: `derived/knowledge-map-v9-b/`

- [ ] Build two independent projections from the same validated package.
- [ ] Compare `projection.json` bytes and every recorded relative file SHA-256.
- [ ] Run the real UA 2.9.4 knowledge parser against both projections.
- [ ] Assert format `karpathy`, 193 articles, 10 topics, 196 wikilinks, zero unresolved links, and 389 total edges.
- [ ] Scan both trees for forbidden origin markers, private paths, secrets, and absolute workspace paths.
- [ ] Preserve one final ignored projection for local visualization.

---

### Task 6: Full regression, documentation status, and branch delivery

**Files:**
- Modify: v9 design and implementation-plan status only after evidence exists.

- [ ] Run full pytest and Ruff.
- [ ] Verify package, inspect exact counts/budgets, and rerun routing evaluation.
- [ ] Build two portable archives and prove their SHA-256 hashes equal the pre-v9 digest.
- [ ] Run public neutrality, secret, placeholder, `git diff --check`, and staged allowlist reviews.
- [ ] Update this plan and the design status with verified evidence.
- [ ] Commit final v9 evidence, push `dev-knowledge-map-v9`, and run a fresh work-state preflight.
- [ ] Fast-forward verified dev into synchronized `feature`, rerun required gates, and push `feature`.
- [ ] Preserve ignored projections, remove only the clean merged v9 worktree, and delete only the merged local v9 branch.
- [ ] Start a unique clean next dev worktree from synchronized `feature`; leave `main` unchanged.

---

## Plan self-review

- The compatibility failure has one root cause and one bounded adapter solution.
- Tool-specific files never enter the canonical package.
- Cross-artifact validation prevents a visually plausible but structurally false graph.
- Determinism is proven at the file tree, manifest, UA scan, and archive levels.
- Output containment and temporary cleanup cover the destructive boundary.
- The delivery workflow follows the three-level branch model and does not promote to `main`.
