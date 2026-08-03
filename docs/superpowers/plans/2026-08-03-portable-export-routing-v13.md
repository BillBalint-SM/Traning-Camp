# Portable Export Routing v13 Implementation Plan

## Task 1: Add failing routing and CLI tests

- [x] Add covered, not-covered, and ambiguous queries against a real export.
- [x] Add read-only and absolute/symlink path guard tests.
- [x] Run the focused suite and observe RED failures.

## Task 2: Implement the export routing adapter

- [x] Verify the export before loading its `skill/references/indexes` tree.
- [x] Reuse `load_indexes` and `route_query` without duplicating scoring logic.
- [x] Run focused tests and Ruff.

## Task 3: Add the guarded CLI

- [x] Register and dispatch `route-portable-export`.
- [x] Resolve the existing export with the symlink-safe workspace guard.
- [x] Print canonical JSON and preserve error code `2`.

## Task 4: Verify and deliver

- [x] Run full pytest, Ruff, package/routing/export/delta/archive gates, and
  neutrality scans.
- [ ] Record evidence, review scope, commit, push, fast-forward merge into
  `feature`, and create the next clean dev worktree.
