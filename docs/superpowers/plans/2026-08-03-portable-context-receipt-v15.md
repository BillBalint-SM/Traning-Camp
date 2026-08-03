# Portable context receipt v15 implementation plan

- [x] Add failing API and CLI assertions for export and module hashes.
- [x] Refactor the loader to verify once and retain the verified manifest.
- [x] Add deterministic receipt fields and preserve the v14 route contract.
- [x] Run focused tests, full tests, lint, and real-export integrity gates.
- [ ] Commit, push, merge into `feature`, and create the next clean dev
      worktree from the synchronized feature branch.

## Verification evidence

- Focused receipt/API/CLI tests: 4 passed.
- Full suite: 167 passed.
- Ruff: all checks passed.
- Real v10 export: export digest
  `bb210e0f528ea31a83c1eeaf6011fdecbdc60fa7ed63f99e55be0a456cdcc2` and
  selected module hash
  `b4d74634402b8533da063e0542267df8a1c10288a8ecf3269e72811201aaa47b`.
- Package/archive, export self-delta, and public neutrality gates remain green.
