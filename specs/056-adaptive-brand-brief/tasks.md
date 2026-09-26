# Tasks: Adaptive Brand Brief and Two Approval Gates

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/workflow.md](contracts/workflow.md)

## Phase 1: Setup

- [x] T001 Inspect the existing interview, approval ledger, continuity protocol, generated entry point, and hosted manual projection.

## Phase 2: Foundation

- [x] T002 Add scenario-based workflow checks to `skill/templates/test_pipeline.py` and confirm they fail on the old instructions.

## Phase 3: User Story 1 - Develop a useful brief

- [x] T003 [US1] Add the reusable facts/constraints/proposals/unresolved brief and social-copy decision record in `skill/references/03-interview.md` and `skill/templates/authoring_brief.py`.
- [x] T004 [US1] Replace the minimal-input questionnaire and numbered discovery gates in `skill/references/03-interview.md` with adaptive questions and specific decision purposes.

## Phase 4: User Story 2 - Approve actual logo source

- [x] T005 [US2] Align `skill/references/06-logo-protocol.md`, `skill/references/identity-continuity.md`, and `skill/SKILL.md` on Gate 1 source-bound approval and silence/revision behavior.

## Phase 5: User Story 3 - Approve assembled fundamentals

- [x] T006 [US3] Define and validate the private Gate 2 packet, distinct social-image preview, exact copy choice, and final-compilation boundary in `skill/references/03-interview.md` and `skill/templates/authoring_brief.py`.
- [x] T007 [US3] Regenerate `skill/AGENTS.md` from `skill/SKILL.md`; verify hosted and packaged references include revised instructions.

## Phase 6: Integration and verification

- [x] T008 Update `CHANGELOG.md` and `skill/CHANGELOG.md` with migration and decision notes.
- [x] T009 Run Spec Kit analysis, focused workflow tests, full kit/site validation, encoding/mojibake checks, and record results in `evidence.md`.
- [ ] T010 Commit, push, open the official PR, handle required CI and up to two review rounds, then hand off for merge.

## Dependencies

T002 precedes implementation. T003 and T004 establish the brief for T005 and T006. T007 follows source guidance changes. T008 and T009 follow implementation; T010 follows green local validation. Tests and docs can be edited independently but run together before completion.
