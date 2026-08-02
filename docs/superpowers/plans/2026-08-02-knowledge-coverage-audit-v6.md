# Knowledge Coverage Audit v6 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish the initial knowledge-forge delivery with reproducible machine-readable package inspection and exact private review-coverage verification for all 193 public modules.

**Architecture:** Add a read-only `audit` module. `inspect-package` validates the portable package and emits a canonical profile of its hash, module/area/relation counts, metadata distributions, and index sizes. `verify-promotion-coverage` validates ignored review maps against public module IDs and normalized private unit IDs, then writes an ignored canonical report. Neither command copies private data into the package.

## Acceptance Criteria

- `inspect-package` emits stable canonical JSON for the validated package, including 193 modules, 10 areas, the manifest digest, relation count, metadata counts, area sizes, and index byte sizes.
- `verify-promotion-coverage` fails on missing, duplicate, extra, unreviewed, malformed, or dangling mappings and writes a deterministic report only on exact coverage.
- All six retained review maps cover all 193 public modules exactly once and reference existing private normalized units.
- The routing skill documents manifest-first verification, progressive disclosure, and graph use without embedding knowledge bodies.
- Full tests, Ruff, package verification, neutrality, deterministic archive, CLI smoke, staged-scope review, and merged-feature verification pass.
- The audit dev slice is committed, pushed, fast-forwarded into `feature`, and the clean feature head is retained as the completed initial delivery stream; `main` is not changed without fresh approval.

## Risks and Verification

- Fail closed on malformed review artifacts and do not include private text, headings, paths, or IDs in public outputs.
- Keep audit output deterministic through sorted keys, sorted records, canonical JSON, and content hashing.
- Define positive and negative CLI behavior first, observe RED, implement the smallest functions, then validate against both temporary fixtures and the retained real private artifacts.

---

### Task 1: Define audit contracts with failing tests

- [x] Add CLI tests for canonical package inspection and exact promotion coverage.
- [x] Add negative tests for missing and duplicate module coverage.
- [x] Run focused tests and confirm RED because the commands do not exist.

### Task 2: Implement package inspection

- [x] Add pure counting/profile functions that validate the package before reporting.
- [x] Add `inspect-package` CLI arguments and canonical stdout.
- [x] Verify exact counts, digest, distributions, areas, relations, and index sizes.

### Task 3: Implement promotion coverage verification

- [x] Parse normalized unit IDs and all sorted review maps with strict shapes and fail-fast errors.
- [x] Enforce exact one-time public module coverage, reviewed state, non-empty unit links, and valid private endpoints.
- [x] Write a deterministic private report and verify failure paths do not write a report.

### Task 4: Final package and delivery audit

- [x] Strengthen the routing skill with manifest-first and graph-expansion rules, rebuild the manifest, and verify neutrality.
- [x] Run the real six-map coverage audit, two archive builds, full pytest, Ruff, CLI smoke, index budgets, and public-boundary scan.
- [x] Stage only public code, tests, skill, manifest, plan, and status; review the complete diff and rerun all gates.
- [x] Commit, push, fast-forward into `feature`, retain the ignored report/archive, verify the synchronized feature head, and remove the merged audit worktree.

## Plan Self-Review

This slice closes the two remaining evidence gaps without expanding into a consuming platform or exposing provenance. Consumers get a compact import profile; maintainers get a reproducible exact-coverage gate. The package remains source-neutral, progressively loadable, deterministic, and independently verifiable.
