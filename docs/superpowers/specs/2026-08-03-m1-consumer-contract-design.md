# Portable consumer contract M1

**Status:** Implemented and verified

## Objective

Define the smallest explicit contract that lets another runtime consume a
verified portable export without importing package internals, executing tools,
or coupling to a model or platform SDK.

## Version policy

All current contract surfaces use integer format version `1`:

- `export.json.format_version` identifies the portable export manifest;
- `skill/references/graph/canonical.json.format_version` identifies the
  canonical graph payload;
- `skill/references/indexes/l0.json.format_version` identifies the routing
  index consumed by the portable route;
- route and context receipts expose top-level `format_version`;
- budget receipts expose `budget.format_version`.

Missing, malformed, boolean, or unsupported versions fail closed before module
content is read. A future incompatible format must introduce an explicit
version and a deliberate migration; consumers must not guess or silently
continue.

## Conformance gates

The repository gate is read-only and verifies the complete export, including
manifest hashes, the Skill reference closure, RAG records, and graph
endpoints:

```text
uv run knowledge-forge verify-portable-exports \
  --workspace . \
  --export exports/portable-exports-v10
```

The generated `skill/` profile can additionally be checked with the official
Agent Skills validator through the explicit wrapper:

```text
uv run python tools/validate_agent_skills.py exports/portable-exports-v10/skill
```

The wrapper fails closed when `agentskills` is unavailable and never installs
dependencies automatically. Because the portable profile is intentionally
stored beneath the stable `skill/` path, the wrapper validates a temporary
copy named from the Skill front matter; the export itself is not changed.
Install the validator separately when needed:

```text
uvx --from skills-ref==0.1.1 agentskills validate <skill-directory>
```

## Consumer boundary

Routing, receipt, graph expansion, and budgeted loading are deterministic and
read-only. Paths are relative to the supplied export root, module IDs and
relations are sorted, and all loaded Markdown bytes remain tied to the
verified manifest and graph hashes. The contract returns data for a consumer;
it does not assemble prompts, invoke models, create embeddings, or execute
tools.
