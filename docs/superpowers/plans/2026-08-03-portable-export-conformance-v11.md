# Portable Export Conformance v11 Implementation Plan

> Execute inline with tests first. Keep `main` unchanged and merge only the
> completed dev slice into `feature`.

## Task 1: Add failing verifier and CLI tests

- [x] Add success assertions for semantic verification of a real v10 export.
- [x] Add negative cases for malformed Skill references/frontmatter, RAG ID or
  metadata drift, graph count/endpoint drift, and manifest/profile mismatch.
- [x] Add CLI tests for success, absolute/escaping/symlink paths, and a clean
  no-write read-only run.
- [x] Run the focused suite and observe the expected RED failures.

## Task 2: Implement semantic verification

- [x] Add small parsing helpers in `knowledge_forge.portability`.
- [x] Extend `verify_portable_export` with required-file, Skill, RAG, and graph
  contract checks while preserving v10 manifest and hash behavior.
- [x] Run focused verifier tests and Ruff.

## Task 3: Add the guarded CLI

- [x] Add a symlink-safe existing-directory path resolver if needed.
- [x] Register and dispatch `verify-portable-exports`.
- [x] Print canonical success output and preserve error code `2`.
- [x] Run focused CLI tests and the combined portability suite.

## Task 4: Verify and deliver

- [x] Run full pytest and Ruff.
- [x] Re-run package, routing, neutrality, and archive regression gates.
- [ ] Review diff and changed-path allowlist, then commit the v11 slice.
- [ ] Push `dev-knowledge-next-v11`, fast-forward merge into `feature`, push
  `feature`, and create the next clean dev worktree.
