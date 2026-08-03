# Portable Export Delta v12

Status: Implemented and verified

## Objective

Make portable knowledge updates auditable before import. A consumer must be
able to compare two verified export trees and see exactly what changed without
loading either tree into an Agent runtime.

## Scope

- Verify both input exports with the v11 conformance gate.
- Compare module content hashes, area membership, graph relations, and profile
  file hashes.
- Emit one deterministic JSON delta with stable sorted arrays and a digest.
- Expose a read-only guarded `diff-portable-exports` CLI command.
- Leave both exports and the canonical package untouched.

## Contract

`diff_portable_exports(base_root, target_root)` returns:

```json
{
  "format_version": 1,
  "kind": "portable-agent-export-delta",
  "base_export_sha256": "...",
  "target_export_sha256": "...",
  "status": "unchanged|changed",
  "modules": {"added": [], "removed": [], "changed": [], "unchanged_count": 0},
  "areas": {"added": [], "removed": [], "changed": []},
  "relations": {"added": [], "removed": []},
  "files": {"added": [], "removed": [], "changed": []},
  "delta_sha256": "..."
}
```

The report is canonical JSON, contains no absolute paths, and is valid only
when both input exports pass the full v11 verifier.

## Non-goals

- No automatic merge, patch, installation, or deletion.
- No model calls, embeddings, network access, or new dependencies.
- No package regeneration or provenance exposure.

## Acceptance evidence

- Identical exports produce an unchanged, byte-stable delta.
- A valid modified export reports module, relation, area, and file changes.
- Invalid or unsafe paths fail closed through the workspace guard.

Verified v12 evidence:

- `157 passed`; full Ruff check passed.
- Identical exports produced `status: unchanged`, `unchanged_count: 193`, and
  delta digest `d814ab7b13eb125512f9697c153a1a80994436587b1c02288d608693b8b6aa39`.
- Export digest for both inputs: `bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2`.
- Package digest: `d71cbf0d2e27bd057c55a951aab7d92a71c5914e0dfd7b58b7d13276ed2102a8`.
- Routing: 263 cases, status `passed`, digest
  `d4be0f1f87243bbab6efb20c275d12c59e4026daaa37348e5d14722d91acf4b9`.
- Two archive builds retained digest
  `04E60A70F0462DC92036A421563FBFFD6D9936768C765055727B909000387861`.
- Public export scans found zero external-origin and absolute-path matches.
