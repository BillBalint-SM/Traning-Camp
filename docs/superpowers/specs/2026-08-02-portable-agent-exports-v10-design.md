# Portable Agent Exports v10 — design specification

**Status:** Awaiting user review
**Date:** 2026-08-02
**Workspace:** `Traning Camp`
**Delivery branch:** `dev-knowledge-portability-v10`

## 1. Purpose

Make the validated knowledge package directly importable by different agent runtimes without coupling the canonical package to one vendor, one vector database, or one graph application. The export is a deterministic interchange artifact; it does not change the canonical package and does not become agent context automatically.

## 2. Current boundary

The canonical package already contains 193 Hungarian modules, ten area indexes, a 196-edge typed graph, a routing skill, and a verified package manifest. Its format is intentionally compact and optimized for controlled routing. Agent consumers still need profile-specific entrypoints:

- an Agent Skills-compatible directory with a discoverable `SKILL.md`;
- a line-oriented document format for RAG ingestion;
- line-oriented graph nodes and edges for graph databases or graph tooling.

Each profile must be independently usable and independently hashable while retaining one package digest and one module identity scheme.

## 3. Selected architecture

Add a focused `portability` builder and one guarded CLI command. It validates the canonical package first, renders three profiles into a new directory beneath `derived/`, records every generated file hash, and publishes only after the complete tree verifies.

The command is:

```powershell
uv run knowledge-forge build-portable-exports `
  --workspace . `
  --pack pack `
  --schemas forge/schemas `
  --output derived/portable-exports-v10
```

The output contains:

```text
portable-exports-v10/
  export.json
  skill/
    SKILL.md
    references/
      graph/canonical.json
      indexes/areas.json
      indexes/l0.json
      indexes/l1/*.json
      knowledge/*.md
  rag/
    documents.jsonl
  graph/
    nodes.jsonl
    edges.jsonl
```

No private intake, provenance, local absolute path, credential, external URL, or acquisition metadata is emitted.

## 4. Agent Skills profile

`skill/SKILL.md` follows the portable Agent Skills convention:

```yaml
---
name: portable-agent-knowledge
description: Route agent-system questions through the validated knowledge references.
---
```

The body gives the minimum routing protocol: verify `export.json`, load L0, select one area, load only the selected L1, then load the smallest sufficient module set. It points only to relative files beneath `references/` and preserves ambiguity and not-covered behavior.

The references directory contains exact public canonical indexes, graph, and module bytes. The entrypoint stays small enough to fit as a skill instruction; detailed knowledge remains lazy-loadable.

## 5. RAG profile

`rag/documents.jsonl` contains one canonical JSON object per module, sorted by `id`:

```json
{"id":"procedure.tool-contract-design","title":"...","text":"...","metadata":{"area_id":"tool-execution","kind":"procedure","maturity":"validated","confidence":"high","tags":["..."]}}
```

The `text` field is the complete public module Markdown, including its frontmatter and operational sections. Metadata carries area ownership and stable classification fields needed for filtering. No embedding, tokenizer, chunker, database driver, or model call is part of v10.

## 6. Graph profile

`graph/nodes.jsonl` contains one canonical JSON node per module with `id`, `title`, `kind`, `maturity`, `confidence`, `tags`, and `content_sha256`.

`graph/edges.jsonl` contains one canonical JSON edge per typed relation with `source`, `type`, and `target`. Both files are sorted deterministically and use the same stable IDs as the canonical graph. Consumers may import them into a graph database without translating vendor-specific IDs.

## 7. Export manifest and determinism

`export.json` contains:

- `format_version: 1`;
- `kind: portable-agent-exports`;
- canonical package SHA-256;
- exact counts: 193 modules, 10 areas, 196 edges;
- profile names and file counts;
- one relative path plus SHA-256 for every generated profile file;
- `export_sha256`, computed over the manifest without that digest field.

The manifest excludes itself from its own file list to avoid a circular digest. Two independent builds from identical package bytes must have identical profile bytes, file hashes, and export digest.

## 8. Validation and safety

The builder rejects:

- a package that fails existing package verification;
- missing, duplicate, self, or dangling module endpoints;
- area/module ownership mismatch;
- a module content hash that differs from the canonical graph;
- an absolute, escaping, symlinked, or existing output path;
- a final output that contains undeclared files or mismatched hashes.

The CLI resolves package and schema paths inside `--workspace`. The output must be a new child beneath `derived/`; all existing ancestors must be regular directories. Generation uses a sibling temporary directory and publishes with one final rename. A failure leaves no final export directory and does not alter `pack/`.

## 9. Import smoke checks

The v10 gate must prove:

- `skill/SKILL.md` has valid frontmatter and all referenced paths exist;
- RAG JSONL contains exactly 193 unique IDs, complete text, and valid area metadata;
- graph JSONL contains exactly 193 nodes and 196 edges with no unresolved endpoints;
- every profile resolves to the canonical package digest;
- the full export tree is neutral and contains no absolute paths, secrets, or external-origin markers;
- two independent exports are byte-identical.

These checks are local and deterministic. No external model, embedding service, network call, or implicit subagent analysis is required.

## 10. Testing strategy

Test-driven implementation covers:

- profile rendering and exact counts;
- Agent Skills frontmatter and relative reference closure;
- RAG record shape, complete text, sorted IDs, and duplicate rejection;
- graph node/edge endpoint closure and deterministic sorting;
- manifest digest and per-file hash verification;
- byte-identical independent builds;
- package mutation rejection;
- output containment, symlink, existing-output, and failure-cleanup behavior;
- CLI success and actionable exit-code-2 failures.

Final gates include the complete pytest suite, Ruff, package verification, routing evaluation, public neutrality scan, two portable export builds, two deterministic archive builds, and changed-path review.

## 11. File boundaries

Tracked changes are limited to:

- `forge/src/knowledge_forge/portability.py`;
- `forge/src/knowledge_forge/cli.py`;
- `tests/test_portability.py`;
- `tests/test_cli_package.py`;
- this specification and its implementation plan.

Generated exports remain under ignored `derived/`. The canonical `pack/` and its archive are not modified. `main` remains unchanged.

## 12. Acceptance criteria

The slice is complete only when:

1. one validated command creates all three profiles;
2. skill, RAG, and graph profile counts are exactly 193/193/196;
3. two independent exports are byte-identical;
4. all profile paths are relative and closed under the export root;
5. the export digest and package digest are reproducible;
6. no canonical package or archive bytes change;
7. all automated and neutrality gates pass;
8. the dev slice is pushed and fast-forwarded into `feature`;
9. `feature` and `origin/feature` converge while `main` remains unchanged;
10. the next unique dev worktree is created from synchronized `feature`.
