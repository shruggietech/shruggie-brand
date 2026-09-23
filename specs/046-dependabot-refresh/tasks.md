# Tasks: Post-Merge Dependabot Refresh

**Input**: S046 specification, plan, research, data model, and release-candidate contract.

**Tests**: Required by the existing publication security policy and release gate.

## Phase 1: Setup

- [x] T001 Record eight new bot PRs, upstream action revisions, and the missing tag in `specs/046-dependabot-refresh/research.md`.
- [x] T002 Review requirements and release checklists and resolve clarifications in `specs/046-dependabot-refresh/checklists/`.

## Phase 2: Foundational

- [x] T003 Write a failing exact-version-comment regression in `scripts/test_publication_workflow.py` without loosening the immutable SHA contract.

## Phase 3: User Story 1 - Coordinated maintenance updates (P1)

- [x] T004 [US1] Integrate five verified action revisions and accurate comments in `.github/workflows/build.yml` and update the approved revisions in `scripts/test_publication_workflow.py`.
- [x] T005 [US1] Integrate three current-runtime Python versions in `requirements.txt`, retaining Python 3.8 markers.
- [x] T006 [US1] Run focused contract and compatibility checks and disposition all eight intake PRs.

## Phase 4: User Story 2 - Shippable kits and site (P1)

- [x] T007 [US2] Run full documented repository, site, kit, glyph, accessibility, release archive, and checksum validation.
- [x] T008 [US2] Record combined gate evidence and release note in `specs/046-dependabot-refresh/evidence.md` and `CHANGELOG.md`.

## Phase 5: User Story 3 - Reviewed release (P2)

- [ ] T009 [US3] Commit, push, and open one S046 PR linking #250 and #242-#249.
- [ ] T010 [US3] Address every actionable review comment and at most one additional Codex request; wait for all required checks green.
- [ ] T011 [US3] Ask the owner for final merge; after merge, close superseded bot PRs and publish and verify `v2.0.1` from the exact main commit.

## Phase 6: Polish

- [x] T012 Audit UTF-8 without BOM, LF endings, mojibake, ignored generated files, and spec/plan/task consistency.

## Dependencies and Execution Order

T003 must fail before T004. T004 and T005 precede combined tests. T007 and T008 precede the PR. T011 is gated on owner merge and cannot be completed beforehand.
