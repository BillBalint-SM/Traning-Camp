# Normalized Unit Disposition v7 Implementation Plan

**Goal:** Prove that every one of the 309 normalized private knowledge units has an explicit reviewed outcome: directly promoted, structurally non-content-bearing, corroborating an existing module, or intentionally excluded.

**Architecture:** Extend the read-only audit module with `verify-unit-disposition`. The command combines exact promotion links with a strict private disposition ledger, validates all unit and module endpoints, forbids overlap and duplicate disposition, requires reason/state consistency, and writes a deterministic ignored aggregate report only on 309/309 coverage.

## Acceptance Criteria

- Positive and negative CLI tests cover complete disposition, missing unit, duplicate/overlap, invalid module endpoint, and invalid state/reason combinations.
- A private ledger classifies all 136 units not directly linked by promotion maps.
- The combined audit reports exactly 309 units: 173 directly promoted plus 136 explicitly dispositioned, with zero pending units.
- No private unit ID, heading, path, or disposition enters `pack/`, the manifest, or the archive.
- Full tests, Ruff, package verification, neutrality, deterministic archive, staged scope, merged-feature verification, and private report hash all pass.

## Steps

- [x] Define RED CLI tests for complete and incomplete unit disposition.
- [x] Implement strict parsing, endpoint validation, overlap prevention, exact union coverage, canonical hashing, and success-only report writing.
- [x] Review and classify all 136 remaining units in the ignored ledger.
- [x] Run the real 309-unit audit and inspect state/reason counts for plausibility.
- [x] Run all public and private gates, stage only public implementation/tests/plan/status, commit, push, and fast-forward into `feature`.
- [x] Preserve the ignored ledger/report/archive, revalidate `feature`, remove the merged worktree, and start the next unique clean dev branch.

## Plan Self-Review

This audit distinguishes semantic coverage from raw extraction coverage. It prevents a complete module review map from hiding unexamined normalized material, while keeping every origin-bearing record outside the portable package.
