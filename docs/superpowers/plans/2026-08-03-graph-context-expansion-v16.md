# Graph context expansion v16 implementation plan

- [x] Add failing API and CLI tests for depth `0`, depth `1`, and invalid depth.
- [x] Implement deterministic one-hop graph expansion on verified exports.
- [x] Reuse receipt hashes and preserve the primary route contract.
- [x] Run full tests, lint, real-export graph smoke, and neutrality gates.
- [ ] Commit, push, merge into `feature`, and create the next clean dev
      worktree from the synchronized feature branch.

## Verification evidence

- Focused graph/API/CLI tests: 10 passed.
- Full suite: 177 passed.
- Ruff: all checks passed.
- Real v10 export: one-hop route for `Eszközszerződés` loads 9 modules and 8
  typed relations with the verified export receipt.
- Package/archive, export self-delta, and public neutrality gates remain green.
