# Portable Export Routing v13

Status: Implemented and verified

## Objective

Provide a consumer-side routing entry point that works directly on a verified
portable export. A runtime should be able to select an area and module IDs
without access to the forge package or any build-time directory.

## Scope

- Verify the export through the v11 conformance gate before routing.
- Load only the exported Skill index tree and reuse the deterministic routing
  algorithm.
- Return the existing routing contract (`covered`, `ambiguous`, or
  `not-covered`) with stable IDs.
- Expose a guarded read-only `route-portable-export` CLI command.
- Do not mutate the export or emit absolute paths.

## Contract

`route_portable_export(output_root, query)` returns the same structured result
as `route_query`. The command accepts a workspace-relative export directory and
query, verifies the directory, routes through `skill/references/indexes/`, and
prints canonical JSON. Invalid exports or unsafe paths fail closed with code 2.

## Non-goals

- No model call, embedding, vector database, or runtime-specific installation.
- No automatic module loading; the returned IDs remain the consumer's load
  decision.
- No package or export mutation.

## Acceptance evidence

- Real export queries reproduce canonical and negative routing outcomes.
- Read-only and unsafe-path tests pass.
- Full package, routing, export, delta, and archive gates remain unchanged.

Verified v13 evidence:

- `161 passed`; full Ruff check passed.
- Real export route: `Eszközszerződés` -> area `tool-execution`, module
  `procedure.tool-contract-design`.
- Export: 193 modules, 10 areas, 196 relations; export digest
  `bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2`.
- Package digest: `d71cbf0d2e27bd057c55a951aab7d92a71c5914e0dfd7b58b7d13276ed2102a8`.
- Delta self-compare: `unchanged`, digest
  `d814ab7b13eb125512f9697c153a1a80994436587b1c02288d608693b8b6aa39`.
- Routing: 263 cases, status `passed`, digest
  `d4be0f1f87243bbab6efb20c275d12c59e4026daaa37348e5d14722d91acf4b9`.
- Two archive builds retained digest
  `04E60A70F0462DC92036A421563FBFFD6D9936768C765055727B909000387861`.
- Public export scans found zero external-origin and absolute-path matches.
