# Sprint priority — first build gate after research

> **Státusz (2026-08-08):** Történeti roadmap-javaslat, nem aktív végrehajtási
> terv. Az itt M1–M3-ként jelölt fogyasztói szerződés, mérési szerződés és
> read-only adapter azóta megvalósult. Az itt M4-ként jelölt graph-strategy gate
> is lezárult: a [merge-elt benchmark](https://github.com/BillBalint-SM/Traning-Camp/pull/9)
> `do-not-promote` döntést adott, ezért a lexical stratégia nem vált alapértelmezetté.
> Új munkához a friss `WORK_STATE` és a jelenlegi `main` az irányadó.

**Dátum:** 2026-08-03
**Decision status:** research-derived proposal; historical as of 2026-08-08.

## Sequenced milestones

### M1 — v17 consumer contract and conformance closure (first milestone)

**Goal:** make the existing verified export/context boundary explicit and consumable without adding a runtime adapter.

**Scope:**

- explicit export-format, graph-schema, routing-evaluation and receipt/budget version fields;
- official `skills-ref` validation for the generated Agent Skills profile;
- backward-compatible and invalid-version tests;
- correct stale documentation status (`v14 Implementing` versus later verified slices);
- consumer conformance fixtures for route, receipt, graph endpoint closure, admitted/omitted modules, budget and byte stability.

**Non-goals:** MCP, A2A, telemetry, global GraphRAG, tokenizer-specific budgets, signed provenance, or platform-specific runtime code.

**Acceptance criteria:**

1. A clean temporary copy of the real portable export passes manifest verification and all v13–v17 consumer checks.
2. Version mismatch and malformed receipts fail closed with actionable errors.
3. Generated `skill/SKILL.md` passes the official skills-ref validator and its reference closure is reported.
4. Route/load/graph/budget outputs are deterministic; export bytes are unchanged.
5. `uv run pytest -q` exits normally with zero failures, and Ruff plus the real-export smoke checks pass.

**Risks:** digest changes, compatibility breakage, and the current test wrapper timeout masking a non-zero exit. Mitigation: focused tests first, then a normal-exit full run and real artifact read-back.

### M2 — runtime-neutral measurement contract

Add a content-free JSONL trace contract containing query hash, route status, export/module digest, admitted/omitted IDs, depth, budget and timing. Pair it with route precision/recall, budget/receipt invariants and a downstream answer-evaluation adapter boundary. Default telemetry must not record module text.

**Dependency:** M1.

### M3 — minimal read-only consumer adapter/import path

Provide a vendor-neutral Python/CLI or wheel/zip import path for `verify → route → load → receipt → optional depth-1/budget`, with explicit installation and clean-temporary-environment documentation. No writes or automatic execution.

**Dependency:** M1; measurement hooks from M2 should be available but not required for basic import.

### M4 — graph strategy benchmark and promotion gate

Compare the existing depth-1 local graph baseline with a separate derived local index using fixed fixtures. Measure context coverage, latency, characters/tokens and adapter-level answer quality. Keep the canonical graph immutable. Only after this gate consider optional MCP read-only resources, an A2A capability descriptor, or signed SLSA/in-toto provenance.

## Prioritization rationale

- **M1 first:** reduces schema/status drift and integrity risk at the boundary every later consumer depends on.
- **M2 second:** makes improvements measurable before adding more runtime surface or multi-agent complexity.
- **M3 third:** converts the already-portable artifact into direct user value with a narrow, reversible integration surface.
- **M4 fourth:** prevents derived GraphRAG or protocol adapters from being selected on intuition alone.

## Assumptions and open questions

- The first reference consumer is still undecided: Agent Skills folder, Python API/CLI, RAG import, or graph import.
- Versioning policy and backward-compatibility window must be chosen before M1 implementation.
- Character budget remains model-neutral unless a separately declared tokenizer adapter is approved.
- The answer-quality evaluator, telemetry retention/PII policy, and latency/budget SLO are not yet named.
- No external protocol owner or signing/registry governance has been assigned.

## Explicitly deferred

Do not build MCP/A2A adapters, global/community GraphRAG summaries or edges, or signed provenance in the first sprint. They require the M1 conformance contract plus explicit security/governance and measurement gates.
