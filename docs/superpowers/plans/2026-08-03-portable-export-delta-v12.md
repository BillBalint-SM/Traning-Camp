# Portable Export Delta v12 Implementation Plan

## Task 1: Add failing delta and CLI tests

- [x] Add unchanged-export assertions and deterministic digest checks.
- [x] Add a valid target mutation fixture and assert module, relation, area, and
  file deltas.
- [x] Add CLI success, read-only, absolute-path, and symlink-ancestor tests.
- [x] Run the focused suite and observe RED failures.

## Task 2: Implement the deterministic delta

- [x] Verify both exports with `verify_portable_export`.
- [x] Parse only validated RAG, graph, area, and manifest records.
- [x] Build sorted added/removed/changed sets and canonical `delta_sha256`.
- [x] Run focused tests and Ruff.

## Task 3: Add the guarded CLI

- [x] Register and dispatch `diff-portable-exports`.
- [x] Resolve both existing directories with the symlink-safe workspace guard.
- [x] Print canonical JSON and preserve error code `2`.

## Task 4: Verify and deliver

- [x] Run full pytest, Ruff, package/routing/export/archive gates, and neutrality
  scans.
- [ ] Record evidence, review scope, commit, push, fast-forward merge into
  `feature`, and create the next clean dev worktree.
