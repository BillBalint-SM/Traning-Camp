# M1 consumer contract and conformance closure

**Status:** Implemented and verified.

## Objective

Make the existing verified portable export/context boundary explicit and
consumer-safe without adding a runtime adapter, telemetry service, MCP/A2A
integration, tokenizer-specific budgets, or global GraphRAG.

## Global constraints

- Canonical Markdown/JSON and the verified portable export remain the source of
  truth; derived projections and runtime adapters stay separate.
- Existing valid v10-v17 exports must remain readable unless a deliberately
  incompatible version is introduced; incompatible versions must fail closed
  with actionable errors.
- Portable export bytes and the current package/export digests must not change
  unless the contract change genuinely requires a format revision.
- Outputs remain deterministic, source-neutral, relative-path-only, and
  read-only at consumption time.
- No secrets, provenance-bearing private records, automatic tool execution, or
  model calls may enter the portable consumer boundary.

## Task 1 — Versioned consumer contract

Inspect the current manifest, receipt, graph, routing, and budget payloads and
add the smallest explicit version fields required to identify export format,
graph schema, routing evaluation, and receipt/budget contracts. Validate them at
the verified consumer boundary. Add focused tests for valid current versions,
missing versions, malformed values, and incompatible versions. Preserve the
existing output shape and digest when no contract revision is required.

## Task 2 — Agent Skills conformance gate

Add a deterministic conformance check for the generated portable `skill/`
profile and its relative reference closure. Prefer the official `skills-ref`
validator when available, but keep the repository gate explicit and fail closed
when the validator is unavailable or the profile is invalid. Cover the real
export and a focused invalid fixture without introducing a runtime dependency
on an agent platform.

## Task 3 — Documentation and full verification

Correct stale v14-v17 status language and document the consumer contract,
version policy, and conformance command. Run focused tests, Ruff, real-export
verify/route/load/graph/budget smoke checks, and the complete `uv run pytest -q`
with a normal exit code. Record any remaining non-blocking limitations.

## Acceptance criteria

1. A clean copy of the real portable export passes all consumer conformance
   checks and remains byte-stable.
2. Invalid or incompatible version fields fail closed with actionable errors.
3. The generated `skill/SKILL.md` passes the repository conformance gate and,
   when installed, the official `skills-ref` validator.
4. Route, receipt, graph, and budget outputs remain deterministic and relative
   path safe.
5. The full test suite exits normally with zero failures, and Ruff plus real
   export smoke checks pass.
