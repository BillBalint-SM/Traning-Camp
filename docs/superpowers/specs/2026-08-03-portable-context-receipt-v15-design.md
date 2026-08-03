# Portable context receipt v15

**Status:** Implemented and verified

## Objective

Make the context returned by the portable loader independently pinable by a
consuming runtime. The response must identify the exact verified export and
the exact content hash of each loaded module, without coupling the response to
any model, vector store, or platform SDK.

## Contract

`load_portable_context(output_root, query)` keeps the v14 routing and module
fields and adds:

- `export_sha256`: the verified portable export manifest digest;
- `content_sha256` on every loaded module, matching its graph node hash.

Ambiguous and not-covered responses also carry `export_sha256` and an empty
`modules` list. The existing route fields, including alternatives, remain
unchanged.

Every receipt carries top-level `format_version: 1`; the version policy is
shared with the graph and budget contracts.

## Integrity behavior

- Verify the export once before routing or reading module bodies.
- Use the verified manifest and graph node hashes as the receipt authority.
- Preserve exact UTF-8 Markdown bytes as decoded text; do not normalize or
  rewrite content.
- Keep output ordering deterministic.

## Non-goals

- No prompt construction, model call, embedding, cache, or consuming-platform
  adapter.
- No export mutation or new canonical package data.

## Acceptance criteria

1. Covered, ambiguous, and not-covered responses expose the export digest.
2. Every loaded module exposes the matching graph content hash.
3. The loader performs one export verification and remains read-only.
4. CLI and API tests prove the receipt against the real portable export.
