# Derived Knowledge Map v9 — design specification

**Status:** Approved for implementation
**Date:** 2026-08-02
**Workspace:** `Traning Camp`
**Delivery branch:** `dev-knowledge-map-v9`

## 1. Purpose

Create a deterministic, disposable knowledge-map projection that makes the portable knowledge package directly readable by Understand Anything without changing the canonical package. The projection exposes every trusted module, area membership, and declared relation as a browsable wiki graph while preserving the package as the sole authority.

## 2. Confirmed compatibility gap

The canonical package contains 193 Markdown modules, JSON L0/L1 indexes, and an explicit canonical graph. Understand Anything knowledge mode detects a Karpathy-pattern wiki only when it finds an `index.md` plus multiple Markdown articles containing resolvable `[[wikilinks]]`.

The unchanged package copy fails detection with `has_index: false`, `md_count: 193`, and `format: unknown`. This is an input-shape mismatch. It must be solved by projection rather than by adding tool-specific files to `pack/`.

## 3. Selected architecture

Add a focused forge projection module and one CLI command. The module validates the package, reads only public canonical artifacts, and writes a new wiki tree beneath an explicitly supplied output directory. The output is ignored, reproducible, and safe to delete.

The projection contains:

- `wiki/index.md`: ten area sections with 193 stable module links;
- `wiki/modules/<module-id>.md`: the unchanged public module body plus one H1 and a generated relation section;
- `projection.json`: canonical package identity, file hashes, counts, and mapping metadata;
- `.ua/intermediate/scan-manifest.json`: generated later by the external UA parser, never by the forge.

No raw intake, private provenance, normalized units, origin identifiers, local absolute paths, credentials, or acquisition metadata enter the projection.

## 4. Canonical and derived boundaries

`pack/` remains canonical. Its module IDs, area ownership, graph endpoints, relation types, titles, and content hashes define projection content. The projection never feeds changes back into the package automatically.

Understand Anything output is an orientation artifact. Its inferred or normalized edges are review candidates only. When it disagrees with `pack/graph/canonical.json`, the canonical graph wins.

The v9 projection is excluded from the portable archive and agent context. It lives beneath ignored `derived/` paths and can be regenerated from a validated package at any time.

## 5. Deterministic mapping

Areas are emitted in canonical area order. Modules within each area follow the canonical `module_ids` order. Graph relations are emitted in sorted `(source, type, target)` order.

Each article path is:

```text
wiki/modules/<module-id>.md
```

Each index link is:

```text
[[modules/<module-id>|<module-title>]]
```

Each outgoing relation link is:

```text
[[modules/<target-id>|<relation-type>: <target-title>]]
```

The original module bytes are not edited in place. The adapter preserves frontmatter, inserts one H1 immediately after it, preserves the existing body, and appends a generated `Kapcsolati térkép` section only when outgoing relations exist.

## 6. Projection manifest

`projection.json` uses canonical JSON and contains no timestamp or absolute path. It records:

- `format_version` and projection kind;
- canonical package SHA-256;
- 10 area, 193 article, and 196 relation counts;
- one record per projected file with relative path and SHA-256;
- module-to-area mappings;
- a projection SHA-256 computed without the digest field.

Repeated builds from identical package bytes must produce byte-identical trees and an identical projection digest.

## 7. Safety contract

The CLI is:

```powershell
uv run knowledge-forge build-knowledge-map-projection `
  --workspace . `
  --pack pack `
  --schemas forge/schemas `
  --output derived/knowledge-map-v9
```

All paths must remain within the workspace. `--output` must resolve beneath the workspace's `derived/` directory, must not be a symlink, and must not already exist. Absolute output paths, traversal, symlink ancestors, output aliases to the package, and writes outside `derived/` fail explicitly.

The forge builds into a sibling temporary directory and renames it only after every file, endpoint, count, and digest has been verified. A failed build leaves no final output directory.

## 8. Validation rules

Before writing, the builder requires:

- a valid canonical package;
- exactly one area owner for every module;
- exact equality between indexed module IDs and graph node IDs;
- every graph endpoint to resolve to a projected module;
- no self relation or duplicate `(source, type, target)` edge;
- graph node paths and content hashes to match the actual modules;
- all generated paths to remain within the temporary projection root.

After writing, it re-reads every projected file, verifies recorded hashes, checks exact article and link counts, and computes the final projection digest.

## 9. UA verification contract

The external parser runs only after forge projection succeeds. A passing scan must report:

- format `karpathy`;
- 193 articles;
- 10 topics;
- 196 wikilinks;
- zero raw inputs;
- zero unresolved wikilinks;
- 389 total graph edges: 196 related plus 193 categorized-under edges.

The UA scan manifest must contain only relative projected paths. No LLM analysis phase or implicit multi-agent enrichment is required for v9; deterministic scan output is sufficient for the portable graph contract.

## 10. Test strategy

Test-driven implementation covers:

- exact deterministic index and article rendering;
- preservation of public module content;
- exact relation and category counts;
- equality of two independently built projection trees;
- missing/dangling graph endpoint rejection;
- index/graph module-set mismatch rejection;
- output-exists and output-outside-derived rejection;
- absolute, traversal, and symlink output rejection;
- cleanup after a controlled build failure;
- CLI success and actionable exit-code-2 failures.

Final verification includes the complete pytest suite, Ruff, package verification, neutrality scan, deterministic archive regression, two independent projections, the real UA parser, projection-manifest hash verification, and staged-path review.

## 11. File boundaries

Tracked changes are limited to:

- `forge/src/knowledge_forge/knowledge_map.py`;
- `forge/src/knowledge_forge/cli.py`;
- `tests/test_knowledge_map.py`;
- `tests/test_cli_package.py`;
- this specification and its implementation plan.

Ignored outputs remain under `derived/`. No `pack/` content change is expected. `main` remains unchanged.

## 12. Acceptance criteria

The slice is complete only when:

1. the exact unchanged-package detection failure is preserved as evidence;
2. the forge creates a deterministic 193-article, 10-area, 196-relation projection;
3. two independent output trees have identical manifests and file hashes;
4. the real UA parser detects the projection and reports zero unresolved links;
5. the canonical package and archive digests remain unchanged;
6. no private or origin-bearing data enters tracked or derived public content;
7. all tests, Ruff, package, neutrality, and archive gates pass;
8. the verified dev slice is pushed and fast-forwarded into `feature`;
9. `feature` and `origin/feature` converge while `main` remains unchanged;
10. a clean unique next dev worktree is created from synchronized `feature`.
