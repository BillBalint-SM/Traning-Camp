# Learning and Evolution Knowledge v4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the portable Hungarian agent knowledge package from 122 to 155 source-neutral modules with operational model post-training and continual-evolution guidance.

**Architecture:** Add separate `model-post-training` and `continual-evolution` L1 areas. This prevents the existing evaluation index from exceeding its context budget and gives queries a clear boundary between weight-changing training and artifact-level operational learning. Canonical indexes, graph, and manifest remain forge-generated; semantic review evidence remains private and ignored.

**Tech Stack:** Python 3.10+, `uv`, PyYAML, jsonschema, pytest, Ruff, Markdown, JSON.

## Acceptance Criteria

- The package contains exactly 155 valid modules and every graph relation resolves.
- Six representative queries resolve to one exact module in the correct new area.
- All L0 and L1 canonical JSON indexes remain at or below 8192 bytes.
- Public `pack/` contains no origin, author, publication, acquisition, URL, private ID, or workspace reference.
- All 33 promoted modules have reviewed private endpoints; private records remain ignored.
- Two independent archives are byte-identical; the full test suite, Ruff, package verification, staged-scope review, and public-boundary scan pass.
- The bounded dev commit is pushed, fast-forwarded into `feature`, reverified there, and the next unique dev branch starts from the synchronized feature head.

## Scope and Risks

- In scope: model-development stages, SFT/RL choice, environments, data, rewards, tool-call learning, distillation, trajectory learning, experience encoding, controlled release, rollback, safety, and offline consolidation.
- Out of scope: training a model, cloning external frameworks, selecting a hosted provider, changing a consuming platform, or publishing private provenance.
- Primary risks: overlapping aliases causing ambiguous routing, reward guidance without verification boundaries, progressive-disclosure budget overflow, and accidental origin leakage.

## Verification Strategy

- Define exact routing behavior first and observe RED before adding areas and modules.
- Regenerate derived package artifacts only through `knowledge-forge build-package`.
- Run focused routing and graph tests, then package verification, deterministic archive comparison, full pytest, Ruff, diff review, and boundary scans.
- Re-run all gates from the merged `feature` head and compare archive hashes across the isolated and root environments.

---

### Task 1: Define the two new routing boundaries

- [x] Add failing exact-route tests for SFT-before-RL, process versus outcome reward, tool-call reinforcement learning, operational trajectory learning, experience-encoding choice, and evolution rollback.
- [x] Add `model-post-training` and `continual-evolution` area declarations with non-overlapping aliases and explicit decision boundaries.
- [x] Confirm the focused test is RED before modules exist.

### Task 2: Add twenty model post-training modules

- [x] Add: `concept.three-stage-model-development`, `principle.sft-behavior-imitation`, `decision-guide.sft-before-rl`, `concept.agent-environment-learning-loop`, `concept.variable-length-agent-policy`, `procedure.sft-data-pipeline`, `decision-guide.post-training-method-selection`, `concept.preference-modeling`, `decision-guide.rl-algorithm-selection`, and `principle.training-environment-data-priority`.
- [x] Add: `pattern.model-simulated-environment`, `checklist.training-data-quality`, `concept.multi-turn-credit-assignment`, `decision-guide.reward-signal-density`, `decision-guide.process-or-outcome-reward`, `pattern.outcome-reward-process-constraints`, `procedure.tool-call-reinforcement-learning`, `pattern.on-policy-distillation`, `pattern.on-policy-self-distillation`, and `checklist.post-training-readiness`.
- [x] Assign each module exactly once, regenerate derived artifacts, and make all post-training routes green.

### Task 3: Add thirteen continual-evolution modules

- [x] Add: `concept.operational-trajectory-learning-signal`, `decision-guide.experience-encoding-layer`, `procedure.knowledge-consolidation-from-experience`, `procedure.instruction-evolution`, `procedure.programmatic-skill-evolution`, and `procedure.parameter-update-from-experience`.
- [x] Add: `principle.meta-evolution`, `pattern.continual-evolution-closed-loop`, `procedure.failure-diagnosis-to-improvement`, `procedure.evolution-validation-release-rollback`, `checklist.verifiable-improvement-boundary`, `checklist.continual-evolution-safety`, and `pattern.offline-consolidation-cycle`.
- [x] Assign each module exactly once, regenerate derived artifacts, and make all evolution routes green.

### Task 4: Review, archive, and integrate

- [x] Map all 33 new public IDs to reviewed private normalized units and verify both endpoint sets.
- [x] Verify schema, graph, routing, context budgets, neutrality, and deterministic archive construction.
- [x] Run the full suite, Ruff, staged-scope review, and public-boundary scan.
- [x] Commit and push the dev slice, fast-forward it into `feature`, preserve ignored artifacts, revalidate the feature head, clean the merged worktree, and start the next unique dev branch.

## Plan Self-Review

The two-area split expresses the true operational boundary: post-training changes model behavior through data and optimization, while continual evolution first changes knowledge, instructions, programs, or release artifacts and only optionally reaches parameters. Every planned module has a stable ID, an intended routing role, and a verification path; no public artifact depends on external source metadata or an unspecified service.
