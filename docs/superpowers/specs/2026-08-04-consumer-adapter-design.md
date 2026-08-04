# M4 Read-Only Consumer Adapter Design

**Status:** Design approved; implementation pending specification review.

## Goal

Provide the first direct, vendor-neutral import boundary for the verified
portable export. A Python caller or an explicit CLI command can verify an
external export, route a query, load deterministic context, and receive a
metadata-only integrity receipt without importing the repository's canonical
`pack/` tree.

## Scope

The adapter supports these operations in one read-only call:

1. verify the portable export manifest, file hashes, graph endpoints, and
   profile closure;
2. route one transient query through the verified export;
3. load either direct context or deterministic depth-1 graph context;
4. optionally apply the existing model-neutral character budget;
5. return the context together with a versioned receipt containing export and
   admitted-module digests.

The adapter accepts an already extracted portable export directory. A ZIP must
be verified/extracted by the existing portable-bundle boundary first; direct
archive extraction is not added to this slice.

## Non-goals and guardrails

- No MCP, A2A, Agent Skills host integration, vector database, embedding,
  GraphRAG global/community layer, model call, tool execution, or write path.
- The adapter never mutates the export and never imports `pack/`, `private/`,
  or repository-local knowledge modules.
- Query text is transient and is not serialized in the result or receipt.
- Module text is returned only in the explicit context payload; the nested
  receipt remains metadata-only.
- Existing portable loader and M3 trace contracts remain backward compatible.
- No new third-party dependency is introduced; Python 3.10+ remains the floor.

## Architecture

Add one focused `consumer.py` module that composes the existing public
portable functions instead of reimplementing verification, routing, graph
expansion, or budget selection. The adapter verifies once, chooses the
existing loader based on explicit arguments, derives a metadata-only receipt
from the returned context, validates the result invariants, and returns it.

The existing CLI receives one new explicit command. It resolves the export as
an existing directory and the result path as a new, workspace-contained file,
then writes canonical JSON atomically. Stdout contains only a compact
canonical PASS summary so callers can use the result file without parsing
module content from terminal output.

## Public interfaces

```python
def consume_portable_export(
    export_root: Path,
    query: str,
    relation_depth: int,
    max_chars: int | None,
) -> dict[str, object]:
    """Verify, route, load, and return a portable consumer result."""


def validate_consumer_result(result: dict[str, object]) -> None:
    """Validate result shape and export/receipt invariants."""


def write_consumer_result(
    output_path: Path,
    result: dict[str, object],
) -> None:
    """Validate and atomically write one canonical JSON result."""
```

`max_chars=None` selects the non-budgeted loader. An integer selects the
existing budgeted loader and must obey its 1–100000 character contract.
`relation_depth` is exactly `0` or `1`; booleans and other integers fail
closed.

## Result contract

The canonical result shape is:

```json
{
  "format_version": 1,
  "kind": "portable-consumer-result",
  "export_sha256": "<64 lowercase hex characters>",
  "context": {
    "format_version": 1,
    "status": "covered|ambiguous|not-covered",
    "area_id": "<area>|null",
    "module_ids": ["<sorted primary ids>"],
    "alternatives": ["<sorted area ids>"],
    "export_sha256": "<same export digest>",
    "modules": [
      {
        "id": "<module id>",
        "content_sha256": "<64 lowercase hex characters>",
        "text": "<explicit context payload>"
      }
    ],
    "expanded_module_ids": ["<sorted ids>"],
    "relations": ["<deterministic relation objects>"],
    "budget": "<existing budget object when requested>"
  },
  "receipt": {
    "format_version": 1,
    "export_sha256": "<same export digest>",
    "relation_depth": 0,
    "admitted_module_ids": ["<sorted ids>"],
    "omitted_module_ids": ["<sorted ids>"],
    "module_hashes": {
      "<module id>": "<content hash>"
    }
  }
}
```

The adapter preserves the existing loader context fields, including graph
relations and budget fields, instead of inventing a second context model. The
receipt is derived from `context.modules`: it has no query, text, absolute
path, model output, or telemetry field. For ambiguous or not-covered routes,
the context and receipt contain no admitted modules, matching the existing
fail-closed boundary.

## CLI contract

```text
knowledge-forge consume-portable-export \
  --workspace . \
  --export exports/portable-exports-v10 \
  --query "Eszközszerződés" \
  --depth 1 \
  [--max-chars 10000] \
  --receipt work/consumer-result.json
```

`--max-chars` is optional at the CLI boundary and maps explicitly to
`max_chars=None` when absent. `--receipt` must be a new relative path inside
the workspace; existing files, symlinked ancestors, absolute paths, and
workspace escapes fail before any write. A successful command prints a
canonical summary with `status`, `kind`, `export_sha256`, and `module_count`.

## Error and trust boundary

The adapter calls `verify_portable_export` before routing or loading. Any
manifest digest drift, undeclared/missing file, invalid graph endpoint,
unknown module hash, malformed receipt, invalid depth, invalid budget, or
unsafe output path raises `KnowledgeForgeError` and performs no output write.
Errors identify the failed contract field or operation but never echo query
text, module text, credentials, or absolute filesystem paths.

## Testing and acceptance gate

Add focused tests for:

- covered, ambiguous, and not-covered results;
- depth 0, depth 1, and budgeted context selection;
- receipt hash equality with the verified export and admitted modules;
- deterministic result bytes across repeated calls;
- query/text/path absence from the receipt metadata;
- tampered export, invalid depth/budget, unknown module, and unsafe output
  rejection without mutation;
- CLI success, clean summary, path safety, and preserved existing output;
- a clean temporary environment that installs the built package and imports
  the consumer API against a copied portable export without repository paths.

Required gates before publication:

```text
uv run ruff check .
uv run pytest -q
uv run knowledge-forge verify-portable-exports --workspace . --export exports/portable-exports-v10
uv build --wheel --out-dir work/m4-wheel
```

The temporary-environment smoke must run the installed wheel, not the source
checkout. The real export digest and byte-stable profiles must remain
unchanged.
