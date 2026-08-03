# Budgeted portable context v17

**Status:** Implemented and verified

## Objective

Give a consuming runtime a deterministic character budget for graph-expanded
context. The routed module is always retained; related modules are admitted in
stable ID order only when their complete Markdown fits the remaining budget.

## Contract

`load_portable_context_budgeted(output_root, query, relation_depth, max_chars)`
returns the v16 receipt and graph fields plus:

- `budget.max_chars` and `budget.used_chars`;
- `budget.omitted_module_ids`, sorted.

`expanded_module_ids`, `modules`, and `relations` describe only content that
was actually admitted. The primary routed modules are always considered first;
if they cannot fit, the function fails closed. Neighbors are considered in
lexicographic module-ID order. Relations with an omitted endpoint are omitted
from the returned context.

`max_chars` must be a positive integer no greater than 100,000. Graph depth
keeps the v16 `0`/`1` limit.

## Safety and determinism

- Verify the export exactly once before routing and loading.
- Read complete module documents only; never truncate Markdown.
- Use the existing regular-file path guard and receipt hashes.
- Never mutate the export or silently exceed the requested budget.

## Non-goals

- No tokenizer/model-specific token estimation, prompt template, embedding, or
  runtime adapter.

## Acceptance criteria

1. The primary module is present and `used_chars <= max_chars`.
2. Neighbor inclusion and omission are deterministic and auditable.
3. Invalid budgets fail closed with an actionable error.
4. The CLI emits canonical JSON and preserves export bytes.
