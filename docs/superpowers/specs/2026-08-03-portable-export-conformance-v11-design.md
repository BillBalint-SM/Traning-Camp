# Portable Export Conformance v11

Status: Implemented and verified

## Objective

Provide a consumer-side, read-only contract check for portable agent exports.
The check must prove that an export is internally coherent before an Agent
runtime loads any knowledge content.

## Scope

- Validate the existing export manifest and every declared file hash.
- Validate the three profiles semantically: Skill references, RAG JSONL, and
  graph JSONL.
- Expose the check as a guarded `verify-portable-exports` CLI command.
- Keep output deterministic, source-neutral, and free of absolute paths.
- Do not rewrite or regenerate the export, package, archive, or indexes.

## Contract

`verify_portable_export(output_root)` returns the validated manifest and raises
`KnowledgeForgeError` on the first actionable contract violation. In addition
to the existing manifest checks, it verifies:

- required profile files and exact manifest profile counts;
- Skill frontmatter, relative reference closure, and declared reference hashes;
- RAG record uniqueness, completeness, metadata shape, and module count;
- graph node/edge uniqueness, counts, and closed endpoints;
- agreement between RAG IDs and graph node IDs.

The CLI command accepts a workspace-relative export directory, rejects absolute
or symlinked paths, prints the canonical manifest on success, and returns the
standard error code `2` on a contract failure.

## Non-goals

- No runtime-specific installation or activation.
- No model calls, embeddings, network access, or new dependencies.
- No mutation of the export while verifying it.

## Acceptance evidence

- Focused tests cover success and malformed/modified/extra/missing profile data.
- CLI tests cover safe path resolution and read-only verification.
- Full pytest, Ruff, package verification, routing verification, and archive
  regression remain green; the v10 package and archive digests do not change.

Verified v11 evidence:

- `152 passed`; full Ruff check passed.
- Export: 193 modules, 10 areas, 196 relations; RAG and graph profiles each
  verified through the new CLI gate.
- Package digest: `d71cbf0d2e27bd057c55a951aab7d92a71c5914e0dfd7b58b7d13276ed2102a8`.
- Export digest: `bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2`.
- Routing: 263 cases, status `passed`, digest
  `d4be0f1f87243bbab6efb20c275d12c59e4026daaa37348e5d14722d91acf4b9`.
- Two archive builds retained the digest
  `04E60A70F0462DC92036A421563FBFFD6D9936768C765055727B909000387861`.
- Public package/export neutrality scan found no external-origin markers.
