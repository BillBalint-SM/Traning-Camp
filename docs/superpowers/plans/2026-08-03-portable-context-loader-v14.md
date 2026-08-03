# Portable context loader v14 implementation plan

- [x] Add failing API and CLI tests for route-to-content loading.
- [x] Implement verified module-content loading with path safety checks.
- [x] Register and dispatch `load-portable-context`.
- [x] Run focused tests, full tests, lint, and artifact integrity gates.
- [ ] Commit the bounded slice, push it, merge it into `feature`, and create
      the next clean dev worktree from the updated feature branch.

## Verification evidence

- Focused API and CLI tests: 6 passed.
- Full suite: 167 passed.
- Ruff: all checks passed.
- Real v10 export API smoke: `covered`, `tool-execution`, one module, 1439
  decoded Markdown characters.
- Real v10 export CLI smoke: same route and module selection.
