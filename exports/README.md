# Portable agent knowledge export

`portable-exports-v10/` is a verified, source-neutral interchange artifact.
It can be copied into an agent runtime without the forge workspace.

Use `portable-exports-v10/export.json` as the integrity entrypoint. The
manifest contains the export digest and every profile file hash.

- `skill/` contains the progressive-disclosure Agent Skills profile.
- `rag/` contains complete JSONL documents for retrieval imports.
- `graph/` contains stable nodes and typed edges for graph imports.

The verified export digest is:

```text
bb210e0f528ea31a83c1eeaf6011fdecdbcbd60fa7ed63f99e55be0a456cdcc2
```

## Portable release bundle

Create the deterministic local ZIP from the verified export tree and verify it
after writing:

```text
uv run knowledge-forge build-portable-bundle --workspace . --export exports/portable-exports-v10 --bundle dist/portable-exports-v10.zip
uv run knowledge-forge verify-portable-bundle --workspace . --bundle dist/portable-exports-v10.zip
```

The ZIP is a derived local artifact. Extracting it produces `export.json`,
`skill/`, `rag/`, and `graph/` at the destination root; that directory can be
copied into a compatible agent runtime without the forge workspace.

Before distributing the bundle, validate the extracted Agent Skills profile:

```text
uv run python tools/validate_agent_skills.py <extracted-bundle>/skill
```

## Context measurement trace

The portable context loader remains the content authority. When a runtime
needs a reproducible measurement receipt, create a metadata-only JSONL trace
explicitly; loading is not instrumented implicitly.

```text
# PowerShell: set $env:PYTHONIOENCODING = "utf-8" before redirecting JSON output.
uv run knowledge-forge load-portable-context-graph --workspace . --export exports/portable-exports-v10 --query "Eszközszerződés" --depth 1 > private/context.json
uv run knowledge-forge record-context-trace --workspace . --context private/context.json --query "Eszközszerződés" --depth 1 --route-ms 3 --load-ms 7 --total-ms 10 --trace derived/context-traces.jsonl
uv run knowledge-forge verify-context-trace --workspace . --trace derived/context-traces.jsonl --export exports/portable-exports-v10
```

Each record contains only versioned route status, module identifiers and
content hashes, relation/budget counts, timing fields, the export digest, and
record digests. It does not contain the query, module text, model output, or
telemetry transport data. Verification first validates the export and then
binds every recorded module hash to that exact export.
