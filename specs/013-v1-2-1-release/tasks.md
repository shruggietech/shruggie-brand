# Tasks: v1.2.1 Release and Production Certification

**Input**: Design documents from `specs/013-v1-2-1-release/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Release regression tests, the complete five-kit build, exact-asset contract, site checks, and repository hygiene are mandatory.

**Organization**: Tasks are grouped by independently testable release-owner and consumer outcomes.

## Phase 1: Setup and Traceability

**Purpose**: Establish public tracking and a complete Spec Kit foundation.

- [X] T001 Create milestone 24 and issue #140 with evidence-based closure policy on GitHub
- [X] T002 Record the synchronized v1.2.0 baseline and merged S012 and Dependabot revisions in `specs/013-v1-2-1-release/evidence.md`
- [X] T003 Complete `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, and `checklists/requirements.md` under `specs/013-v1-2-1-release/`

**Checkpoint**: S013 has complete public and repository-local traceability.

---

## Phase 2: Release Candidate Foundation

**Purpose**: Establish regression coverage and synchronized patch-release metadata.

- [X] T004 [P] [US1] Add v1.2.1 history, metadata, migration, exact-asset, and independent-brand-version coverage in `scripts/test_release_contract.py`
- [X] T005 [P] [US1] Advance default-version packaging coverage to v1.2.1 in `scripts/test_package_release.py`
- [X] T006 [US1] Make migration notes version-specific and recognize v1.2.1 history in `scripts/release_contract.py`
- [X] T007 [P] [US1] Promote Unreleased history into dated v1.2.1 sections in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [X] T008 [P] [US1] Advance skill and canon metadata to v1.2.1 in `skill/SKILL.md` and `skill/references/01-canon.json`
- [X] T009 [P] [US1] Advance only the canon field to v1.2.1 in all five `brands/*/brand.json` production sources
- [X] T010 [P] [US1] Advance private site package metadata to v1.2.1 in `site/package.json`

**Checkpoint**: Every candidate metadata surface agrees on v1.2.1 while production-brand versions remain unchanged.

---

## Phase 3: Coherent Patch Candidate (User Story 1, Priority: P1)

**Goal**: Produce a complete locally certified v1.2.1 candidate.

**Independent Test**: A full source build produces five zero-failure production kits and exactly seven archives whose generated notes and contents pass the release contract.

- [X] T011 [US1] Run focused release, packaging, brand-contract, icon, pipeline, site-preparation, and Markdown checks from `specs/013-v1-2-1-release/quickstart.md`
- [X] T012 [US1] Rebuild all five production kits with zero verifier problems and zero glyph failures using `scripts/build_all.py`
- [X] T013 [US1] Package exactly seven v1.2.1 candidate assets and verify their generated notes using `scripts/package_release.py` and `scripts/release_contract.py`
- [X] T014 [US1] Synchronize generated agent instructions and pass site lint, static export, browser routes, responsive layouts, themes, and WCAG checks using `skill/templates/sync_agents_md.py` and `site/`
- [X] T015 [US1] Run UTF-8, LF, mojibake, sensitive-data, generated-output, Markdown, diff, and status gates and record sanitized results in `specs/013-v1-2-1-release/evidence.md`

**Checkpoint**: The v1.2.1 source revision is a complete release candidate.

---

## Phase 4: Reviewed Source Publication (User Story 2, Priority: P1)

**Goal**: Publish, review, and merge the source candidate with all automatic feedback resolved.

**Independent Test**: The pull request has successful required checks, substantive dispositions for every review comment, zero unresolved actionable threads, and no manual Codex review request.

- [X] T016 [US2] Complete candidate evidence and task state, commit the S013 revision, and verify the committed branch is clean
- [ ] T017 [US2] Push `codex/013-v1-2-1-release` and open the official S013 pull request tracking #140
- [ ] T018 [US2] Process automatic Codex review, file every negative finding, implement and verify warranted corrections, respond to every comment, resolve addressed threads, and update `specs/013-v1-2-1-release/evidence.md`
- [ ] T019 [US2] Wait for every required check to succeed, verify zero manual review triggers, and merge the pull request
- [ ] T020 [US2] Synchronize actual main and repeat the complete v1.2.1 candidate contract before tagging

**Checkpoint**: Reviewed merged main is qualified for immutable publication.

---

## Phase 5: Official Release Publication (User Story 2, Priority: P1)

**Goal**: Publish and independently certify the official v1.2.1 release.

**Independent Test**: The public release targets verified main and seven freshly downloaded assets plus generated notes pass the shared contract.

- [ ] T021 [US2] Create and push annotated tag v1.2.1 at verified main and wait for the Release workflow
- [ ] T022 [US2] Download the public release body and exactly seven assets into fresh ignored repository-local storage and pass the v1.2.1 release contract
- [ ] T023 [US2] Record immutable tag, workflow, release, inventory, and fresh-download evidence on `specs/013-v1-2-1-release/evidence.md` and issue #140

**Checkpoint**: The public v1.2.1 release is independently certified.

---

## Phase 6: Production Certification (User Story 3, Priority: P2)

**Goal**: Prove the deployed site reflects the release without route, payload, discovery, responsive, theme, or accessibility regression.

**Independent Test**: The production-origin verifier passes every public route at 360px and 1280px with zero failures and zero WCAG 2.1 AA violations.

- [ ] T024 [US3] Verify the Pages workflow targets merged main and run the production contract from `specs/013-v1-2-1-release/contracts/production-contract.md`
- [ ] T025 [US3] Attach sanitized production evidence to #140, close only #140 after all criteria pass, then close milestone 24
- [ ] T026 [US3] Confirm zero open pull requests, zero unintended issue closures, clean synchronized main, and final release status in `specs/013-v1-2-1-release/evidence.md`

**Checkpoint**: S013 and Phase 14 are complete.

## Dependencies & Execution Order

- T001 through T003 establish the foundation before implementation.
- T004 and T005 precede their implementation and metadata counterparts T006 through T010.
- T006 through T010 complete before T011 through T015.
- T011 through T015 complete before commit and publication in T016 and T017.
- T018 and T019 complete before merge. S013 never posts a manual Codex review request.
- T020 completes before T021. T022 depends on successful CI publication.
- T024 depends on the merged-main Pages deployment. T025 and T026 require both public release and production evidence.

## Parallel Opportunities

- T004 and T005 affect separate regression files.
- T007 through T010 update independent source surfaces after release behavior is established.
- Release and Pages workflow observation may overlap after merge, while evidence and closure remain contract-specific.

## Implementation Strategy

1. Establish traceability and converge the specification.
2. Build and certify a synchronized v1.2.1 candidate.
3. Publish the source pull request and resolve automatic review feedback.
4. Merge after green checks, revalidate actual main, and publish from one annotated tag.
5. Verify fresh public assets and the production site.
6. Close only the evidence-complete S013 hierarchy.
