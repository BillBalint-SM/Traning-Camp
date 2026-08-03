# Budgeted portable context v17 implementation plan

- [x] Add failing API and CLI tests for primary and neighbor budget behavior.
- [x] Implement deterministic whole-module admission under a character cap.
- [x] Preserve graph relations, receipt hashes, and omission evidence.
- [x] Run full tests, lint, real-export budget smoke, and neutrality gates.
- [ ] Commit, push, merge into `feature`, and create the next clean dev
      worktree from the synchronized feature branch.

## Verification evidence

- Focused budget/API/CLI tests: 9 passed.
- Full suite: 186 passed.
- Ruff: all checks passed.
- Real v10 export with `max_chars=2000`: primary content retained at 1439
  characters, 8 neighbor modules explicitly omitted, and receipt digest
  preserved.
- Package/archive, export self-delta, and public neutrality gates remain green.
