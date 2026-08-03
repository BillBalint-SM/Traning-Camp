# Portable context loader v14

**Status:** Implementing

## Objective

Expose a deterministic, read-only boundary that turns a query into the
validated portable-export module content needed by another agent runtime.
The boundary must verify the export before reading any module and must return
the existing routing result together with the selected Markdown documents.

## Contract

`load_portable_context(output_root, query)` returns the routing fields and a
`modules` list. Each module record contains an `id` and its complete UTF-8
Markdown `text`. Module IDs are sorted and only modules selected by a covered
route are loaded. Ambiguous and not-covered routes return an empty `modules`
list while preserving their routing fields.

The CLI command `load-portable-context` accepts a workspace-relative export
directory and query, emits canonical JSON, and performs no writes.

## Safety and determinism

- `verify_portable_export` runs before any content is loaded.
- Module references must be regular, non-symlink files inside the export's
  knowledge reference directory.
- Module text is decoded as UTF-8 without normalization or rewriting.
- Output field ordering and module ordering are deterministic.

## Non-goals

- No prompt assembly, model invocation, vector indexing, or platform-specific
  adapter is included.
- No changes are made to the canonical package or the export.

## Acceptance criteria

1. A covered query returns the expected route and complete selected Markdown.
2. Ambiguous and not-covered queries return no module content.
3. Invalid or unsafe module references fail with `KnowledgeForgeError`.
4. The CLI emits canonical JSON, preserves the export byte-for-byte, and
   rejects absolute or symbolic-link paths through the workspace guard.
