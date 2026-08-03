# Graph context expansion v16

**Status:** Implemented and verified

## Objective

Allow a consuming runtime to request a small, explicit graph neighborhood
around the module selected by deterministic routing. The expansion makes the
portable graph useful for context injection while keeping the default loader
minimal and preventing unbounded context growth.

## Contract

`load_portable_context_graph(output_root, query, relation_depth)` returns the
v15 receipt fields and adds:

- `expanded_module_ids`: all module IDs whose Markdown is included, sorted;
- `relations`: typed graph edges connecting the selected module and its
  one-hop neighborhood, sorted by `(source, type, target)`.

The primary route `module_ids` remains unchanged. `relation_depth` is required
and must be `0` or `1`; depth `0` loads only the routed modules and no edges.
Depth `1` loads every direct incoming or outgoing neighbor, with complete
Markdown and graph content hashes for all loaded modules.

Ambiguous and not-covered routes return no modules, no expanded IDs, and no
relations while preserving the verified export receipt.

The receipt retains top-level `format_version: 1` and the graph payload is
required to declare its own compatible `format_version: 1`.

## Safety and determinism

- Verify the export once before routing, graph traversal, or content reads.
- Reject negative, non-integer, boolean, or greater-than-one depth values.
- Use only closed, verified graph endpoints and regular module files beneath
  the export root.
- Sort IDs and edge records deterministically; never mutate the export.

## Non-goals

- No recursive graph database, embedding, model call, prompt assembly, or
  platform-specific adapter.
- No implicit expansion in `load_portable_context`.

## Acceptance criteria

1. Depth `0` is equivalent to the routed context plus empty graph fields.
2. Depth `1` includes the exact direct neighborhood and typed relations.
3. Invalid depth values fail closed with an actionable `KnowledgeForgeError`.
4. The CLI emits canonical JSON and preserves export bytes.
