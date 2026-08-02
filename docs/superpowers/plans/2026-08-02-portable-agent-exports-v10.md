# Portable Agent Exports v10 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build one guarded command that exports the validated package into Agent Skills, RAG JSONL, and graph JSONL profiles with reproducible hashes.

**Architecture:** `knowledge_forge.portability` validates the existing package, renders all three profiles into an in-memory file map, creates a canonical export manifest, and publishes the tree through a sibling temporary directory. The CLI resolves the output beneath `derived/` using the existing symlink-safe directory guard. No generated export enters `pack/` or the archive.

**Tech Stack:** Python 3.10+, existing package validators, canonical JSON/SHA-256 helpers, pytest, Ruff, JSONL, YAML frontmatter text contract.

## Global Constraints

- Read only validated public package artifacts under `pack/` and `forge/schemas/`.
- Write only to a new caller-selected child beneath `derived/`.
- Preserve exact public module IDs, area ownership, 193 module records, and 196 typed edges.
- Keep all generated paths relative and all output bytes deterministic; exclude timestamps and runtime paths.
- Use no external model, embedding service, network call, or additional dependency.
- Never modify `pack/`, `pack/manifest.json`, or the portable archive.
- Diagnostics must not expose absolute paths, credentials, private identifiers, or external-origin markers.
- `main` remains unchanged; only `dev-knowledge-portability-v10` targets `feature`.

---

### Task 1: Add failing contract tests for the three profiles

**Files:**
- Create: `tests/test_portability.py`

**Interfaces:**
- Planned builder: `build_portable_exports(pack_root: Path, schema_root: Path, output_root: Path) -> dict[str, object]`.
- Planned verifier: `verify_portable_export(output_root: Path) -> dict[str, object]`.

- [x] **Step 1: Add a real-package fixture and wished-for builder tests**

Write tests against the real `pack/` and `forge/schemas/` with a temporary output root. Assert that the returned manifest and files contain:

```python
assert manifest["kind"] == "portable-agent-exports"
assert manifest["module_count"] == 193
assert manifest["area_count"] == 10
assert manifest["relation_count"] == 196
assert manifest["profiles"]["rag"]["document_count"] == 193
assert manifest["profiles"]["graph"]["node_count"] == 193
assert manifest["profiles"]["graph"]["edge_count"] == 196
```

Check that `skill/SKILL.md`, `rag/documents.jsonl`, `graph/nodes.jsonl`, and `graph/edges.jsonl` exist. Parse every JSONL line and require unique sorted module IDs, complete text, area metadata, and closed graph endpoints.

- [x] **Step 2: Add frontmatter and reference-closure assertions**

Require the first and last frontmatter delimiters in `skill/SKILL.md`, the exact `name: portable-agent-knowledge`, a non-empty `description`, and only relative references. For every `skill/references/` file, assert the path is declared by the export manifest and the byte hash matches.

- [x] **Step 3: Add deterministic-build and output-boundary tests**

Build two independent output directories and assert byte equality for every relative file and equality of `export_sha256`. Create an existing output with a sentinel and assert the builder fails without changing it.

- [x] **Step 4: Add malformed-input tests**

Copy the package into `tmp_path`, mutate one canonical graph endpoint or one graph node hash, and assert the builder raises an actionable `KnowledgeForgeError` before creating a final directory. Also mutate one area module list and assert the ownership mismatch is rejected.

- [x] **Step 5: Run the focused tests and confirm RED**

Run:

```powershell
uv run pytest -q tests/test_portability.py
```

Expected: collection fails because `knowledge_forge.portability` does not yet exist. Fix only test typos if needed; do not add production code before this RED result.

---

### Task 2: Implement validated input loading and profile renderers

**Files:**
- Create: `forge/src/knowledge_forge/portability.py`
- Modify: `tests/test_portability.py`

**Interfaces:**
- Consumes: `inspect_package`, `discover_modules`, `load_areas`, `read_json`, `canonical_json_bytes`, and `sha256_bytes`.
- Produces: `build_portable_exports(pack_root: Path, schema_root: Path, output_root: Path) -> dict[str, object]` and `verify_portable_export(output_root: Path) -> dict[str, object]`.

- [x] **Step 1: Implement canonical input validation**

Call `inspect_package(pack_root, schema_root)` before rendering. Load areas, modules, and canonical graph. Validate exact equality between module IDs, graph node IDs, and area ownership; validate node content hashes, edge endpoints, self edges, and duplicate `(source, type, target)` tuples. Use explicit `KnowledgeForgeError` messages without absolute paths.

- [x] **Step 2: Implement the Agent Skills profile**

Render a fixed UTF-8 `skill/SKILL.md` with this frontmatter and relative routing instructions:

```text
---
name: portable-agent-knowledge
description: Route agent-system questions through the validated knowledge references.
---
```

Copy exact canonical `graph/canonical.json`, `indexes/areas.json`, `indexes/l0.json`, every L1 index, and every module into `skill/references/`. Do not copy the package manifest or any ignored artifact.

- [x] **Step 3: Implement the RAG JSONL profile**

Emit one `canonical_json_bytes` record per sorted module:

```python
{
    "id": module_id,
    "title": title,
    "text": raw_module_text,
    "metadata": {
        "area_id": area_id,
        "kind": kind,
        "maturity": maturity,
        "confidence": confidence,
        "tags": sorted(tags),
    },
}
```

Write exactly 193 newline-terminated records. Preserve each module's complete public Markdown text without adding export-specific headers.

- [x] **Step 4: Implement the graph JSONL profile**

Emit sorted canonical node records with `id`, `title`, `kind`, `maturity`, `confidence`, `tags`, and `content_sha256`, followed by sorted edge records with `source`, `type`, and `target`. Emit exactly 193 nodes and 196 edges with no endpoint outside the node set.

- [x] **Step 5: Run focused tests and Ruff**

Run:

```powershell
uv run pytest -q tests/test_portability.py
uv run ruff check forge/src/knowledge_forge/portability.py tests/test_portability.py
```

Expected: profile rendering, counts, content, and deterministic-build tests pass.

- [x] **Step 6: Commit the renderer**

```powershell
git add forge/src/knowledge_forge/portability.py tests/test_portability.py
git commit -m "feat: render portable agent export profiles"
```

---

### Task 3: Implement export manifest, verification, and atomic publication

**Files:**
- Modify: `forge/src/knowledge_forge/portability.py`
- Modify: `tests/test_portability.py`

**Interfaces:**
- Consumes: the validated profile file map from Task 2.
- Produces: `export.json` with relative file hashes and `verify_portable_export(output_root)` that returns the validated manifest.

- [ ] **Step 1: Add manifest identity tests**

Assert that `export.json` has `format_version: 1`, `kind: portable-agent-exports`, the package digest, exact counts, profile counts, a sorted file list, and a 64-character `export_sha256`. Recompute the digest from the manifest with `export_sha256` removed and require equality.

- [ ] **Step 2: Add per-file verification tests**

After a successful build, mutate one generated file and assert `verify_portable_export` reports a hash mismatch. Add an undeclared extra file and assert verification rejects it. Assert that a missing generated file is rejected.

- [ ] **Step 3: Implement manifest and verifier**

Build the manifest from sorted relative file paths, hash every profile byte, compute `export_sha256` from canonical JSON without the digest field, and write `export.json`. The verifier must reject absolute paths, `..` components, undeclared files, missing files, hash mismatches, duplicate IDs, and endpoint drift.

- [ ] **Step 4: Implement temporary-directory publication**

Write all files to a sibling directory created with `tempfile.mkdtemp`, verify the complete tree, then rename it to the new output target. On any exception, remove only the exact temporary directory created by this invocation; never remove an existing output directory.

- [ ] **Step 5: Run focused tests and Ruff**

Run:

```powershell
uv run pytest -q tests/test_portability.py
uv run ruff check forge/src/knowledge_forge/portability.py tests/test_portability.py
```

Expected: all export contract, digest, mutation, and cleanup tests pass.

- [ ] **Step 6: Commit manifest and publication**

```powershell
git add forge/src/knowledge_forge/portability.py tests/test_portability.py
git commit -m "feat: verify portable export manifests"
```

---

### Task 4: Add the guarded CLI command and integration tests

**Files:**
- Modify: `forge/src/knowledge_forge/cli.py`
- Modify: `tests/test_cli_package.py`

**Interfaces:**
- Consumes: `build_portable_exports(pack_root, schema_root, output_root)` and `resolve_new_directory_within`.
- Produces: `build-portable-exports --workspace --pack --schemas --output`, returning `0` on success and `2` on `KnowledgeForgeError`.

- [ ] **Step 1: Add failing CLI tests**

Add tests for a successful copied workspace, existing output, absolute output, workspace escape, output outside `derived/`, output symlink, and symlink ancestor. Require a successful manifest with 193 documents and a failure message containing no absolute workspace path.

- [ ] **Step 2: Run CLI tests to confirm RED**

Run:

```powershell
uv run pytest -q tests/test_cli_package.py -k "portable_exports"
```

Expected: argparse rejects the unknown command.

- [ ] **Step 3: Add parser and dispatch**

Register `build-portable-exports` with required `--workspace`, `--pack`, `--schemas`, and `--output` arguments. Resolve package/schema via `resolve_within` and output via `resolve_new_directory_within(workspace_root, output, Path("derived"), "Portable export output")`.

- [ ] **Step 4: Run CLI and complete regression tests**

Run:

```powershell
uv run pytest -q tests/test_cli_package.py -k "portable_exports"
uv run pytest -q tests/test_cli_package.py tests/test_portability.py
uv run ruff check forge/src/knowledge_forge/cli.py forge/src/knowledge_forge/portability.py tests/test_cli_package.py tests/test_portability.py
```

- [ ] **Step 5: Commit the CLI boundary**

```powershell
git add forge/src/knowledge_forge/cli.py tests/test_cli_package.py
git commit -m "feat: expose portable agent exports"
```

---

### Task 5: Build, import-smoke, and complete the v10 gate

**Ignored outputs:**
- Create: `derived/portable-exports-v10-a/`
- Create: `derived/portable-exports-v10-b/`

- [ ] **Step 1: Build two independent exports**

Run the CLI twice with distinct output paths. Compare every relative file SHA-256 and require identical `export_sha256` values.

- [ ] **Step 2: Run profile smoke checks**

Read `export.json`, every RAG record, every graph node/edge, and the skill reference tree. Require 193 RAG records, 193 graph nodes, 196 graph edges, valid relative references, complete text, and zero unresolved endpoints.

- [ ] **Step 3: Run full repository gates**

Run:

```powershell
uv run pytest -q
uv run ruff check .
uv run knowledge-forge verify-package --workspace . --pack pack --schemas forge/schemas --markers private/leakage/markers.json
uv run knowledge-forge verify-routing-evaluation --workspace . --pack pack --schemas forge/schemas --suite forge/evals/routing-v1.json --report private/audit/routing-evaluation-v10.json
```

- [ ] **Step 4: Verify neutrality and archive regression**

Scan both exports and all changed public files for external-origin markers, absolute paths, secrets, and placeholders. Build two v10 archive copies and require their SHA-256 to equal `04E60A70F0462DC92036A421563FBFFD6D9936768C765055727B909000387861`.

- [ ] **Step 5: Update design and plan evidence**

Change the v10 design status to `Implemented and verified`, mark only evidence-backed plan checkboxes, record export and smoke hashes, and run `git diff --check` plus changed-path allowlist review.

---

### Task 6: Deliver v10 and start the next isolated slice

- [ ] **Step 1: Commit final evidence**

After a fresh preflight and clean tracked diff:

```powershell
git add docs/superpowers/specs/2026-08-02-portable-agent-exports-v10-design.md docs/superpowers/plans/2026-08-02-portable-agent-exports-v10.md
git commit -m "docs: record verified portable agent exports v10"
```

- [ ] **Step 2: Push the dev branch**

Verify the current branch, HEAD, worktree, and `origin/feature` ancestry, then push `dev-knowledge-portability-v10`.

- [ ] **Step 3: Fast-forward into feature**

In the root feature worktree, verify local `feature == origin/feature`, merge `origin/dev-knowledge-portability-v10` with `--ff-only`, rerun the full gates, and push `feature`. Do not promote to `main`.

- [ ] **Step 4: Preserve final ignored exports and rotate worktrees**

Preserve one verified v10 export under the root `derived/`, validate its manifest and smoke hash, remove only the clean merged v10 worktree and local v10 branch, then create `dev-knowledge-next-v11` from synchronized `feature`.

## Plan self-review

- Every profile in the design has a renderer, verifier, test set, and final smoke gate.
- The export manifest excludes itself to avoid circular hashing and records every other generated byte.
- CLI safety reuses the existing workspace and symlink guard.
- No package or archive mutation is authorized by this plan.
- No placeholder, external-origin marker, or unresolved interface remains.
