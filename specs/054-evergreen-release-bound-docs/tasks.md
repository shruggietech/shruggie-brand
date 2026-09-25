# Tasks: Evergreen, Release-Bound Documentation

**Input**: [spec.md](spec.md), [plan.md](plan.md), [contracts/documentation-publication.md](contracts/documentation-publication.md)

## Phase 1: Setup and inventory

- [x] T001 Inventory all cataloged source pages, overview, navigation, search text, and README claims in `specs/054-evergreen-release-bound-docs/evidence.md`.
- [x] T002 Record baseline release candidate state and exact local verification commands in `specs/054-evergreen-release-bound-docs/evidence.md`.

## Phase 2: User Story 1, current manual

**Independent test**: Every declared source/prepared/export page is audited; stale mutations fail and technical quantities pass.

- [x] T003 [US1] Add fail-first count, history, slice-code, and description mutation tests in `scripts/test_public_documentation.py`.
- [x] T004 [US1] Correct stale prose and obsolete version header across `skill/references/*.md`, preserving operative rules.
- [x] T005 [US1] Extend source, prepared, exported, and search-text coverage in `scripts/audit_public_documentation.py`.
- [x] T006 [US1] Complete page-by-page disposition and code/canon cross-check in `specs/054-evergreen-release-bound-docs/evidence.md`.

## Phase 3: User Story 2, exact release identity

**Independent test**: Candidate and release records bind catalog, source references, prepared pages, tag, revision, and packaged skill bytes; mutations fail.

- [x] T007 [US2] Add fail-first record and mismatch tests in `scripts/test_documentation_publication.py`.
- [x] T008 [US2] Generate documentation publication record and candidate/release page identity in `scripts/prepare_site.py` and `scripts/documentation_render.py`.
- [x] T009 [US2] Verify record against local sources, prepared pages, exported copy, and packaged references in `scripts/release_contract.py`.
- [x] T010 [US2] Stage and verify record in `.github/workflows/build.yml` before tagged publication.

## Phase 4: User Story 3, evergreen README

**Independent test**: README audit accepts a growing site inventory without edits and rejects snapshot claims and unsafe links.

- [x] T011 [US3] Add fail-first README content and preserved link/accessibility cases in `scripts/test_check_readme_links.py`.
- [x] T012 [US3] Rewrite `README.md` with stable site/release/policy/help links and semantic build examples.
- [x] T013 [US3] Retire brand enumeration and enforce evergreen content in `scripts/check_readme_links.py`.

## Phase 5: Cross-cutting delivery

- [x] T014 Run Spec Kit cross-artifact analysis and resolve findings in `specs/054-evergreen-release-bound-docs/analysis.md`.
- [x] T015 Run full documented local kit, glyph, archive, site, publication, accessibility, encoding, and hygiene gates; record results in `specs/054-evergreen-release-bound-docs/evidence.md`.
- [x] T016 Update `CHANGELOG.md` with S054 behavior and dated publication-process decision.
- [ ] T017 Commit source and Spec Kit records, push `codex/054-evergreen-release-bound-docs`, and open an official PR with #264/#265/#276 traceability.
- [ ] T018 Follow required CI and external reviews, resolve every actionable comment, optionally run one second Codex review round, and hand off only after checks are green.

## Dependencies

T001-T002 precede content changes. T003 precedes T004-T006. T007 precedes T008-T010. T011 precedes T012-T013. T014 gates implementation consistency and is run before code changes. T015-T018 follow all user stories.

## Implementation strategy

Complete the manual-content corrections, then record binding, then README. Each story has independent assertions. Generated output is rebuilt, never committed. Live production checks remain a post-merge release step.
