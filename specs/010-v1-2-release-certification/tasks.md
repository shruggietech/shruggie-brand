# Tasks: v1.2.0 Release and Production Certification

**Input**: Design documents from `specs/010-v1-2-release-certification/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Regression-first release tests, the complete production build, release preflight, site checks, and repository hygiene are mandatory.

**Organization**: Tasks are grouped by independently testable release-owner and consumer outcomes. The owner merge ritual is the boundary between the pre-merge candidate and post-merge public evidence.

## Phase 1: Setup and Traceability

**Purpose**: Establish the public tracking and complete Spec Kit foundation before implementation.

- [X] T001 Create Phase 12 milestone 22 and linked issues #116 through #119 with evidence-based closure policy on GitHub
- [X] T002 Record the synchronized base, v1.1.2 release baseline, current metadata, absent v1.2.0 tag and release, and tracking records in `specs/010-v1-2-release-certification/evidence.md`
- [X] T003 Complete and validate `specs/010-v1-2-release-certification/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, and `checklists/requirements.md`

**Checkpoint**: S010 has complete public and repository-local traceability.

---

## Phase 2: Release Authority Foundation

**Purpose**: Add regression-first coverage and establish one validated path for current release metadata.

- [X] T004 [P] [US1] Add failing current-version, v1.2.0 history, date-agreement, migration, exact-asset, and independent-brand-version regressions in `scripts/test_release_contract.py`
- [X] T005 [P] [US1] Add failing default-version packaging coverage in `scripts/test_package_release.py`
- [X] T006 [US1] Generalize requested-version history validation, update migration language, and add the validated `current` command in `scripts/release_contract.py`
- [X] T007 [US1] Make omitted `--version` use validated current metadata while preserving explicit-version support in `scripts/package_release.py`
- [X] T008 [US1] Make pull-request release preflight discover the validated current version in `.github/workflows/build.yml`

**Checkpoint**: Release commands fail closed on version drift and no workflow or packaging default duplicates the current release literal.

---

## Phase 3: Coherent Release Candidate (User Story 1, Priority: P1)

**Goal**: Produce one locally certified v1.2.0 candidate with complete history, exact assets, and unchanged production brand versions.

**Independent Test**: A clean source build produces five zero-failure production kits and exactly seven release assets whose notes and contents pass the shared contract.

- [X] T009 [P] [US1] Promote current Unreleased history into dated v1.2.0 sections while preserving earlier releases in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [X] T010 [P] [US1] Advance the skill and canon metadata to 1.2.0 in `skill/SKILL.md` and `skill/references/01-canon.json`
- [X] T011 [P] [US1] Advance only the canon reference in `brands/shruggietech/brand.json`, `brands/fragcap/brand.json`, `brands/go-schedule/brand.json`, `brands/glitchpad/brand.json`, and `brands/covarity/brand.json`
- [X] T012 [P] [US1] Advance the private site package version to 1.2.0 in `site/package.json` and synchronize `site/pnpm-lock.yaml` only if package metadata requires it
- [X] T013 [US1] Run the focused regression and Python 3.8-compatible command set from `specs/010-v1-2-release-certification/quickstart.md`
- [X] T014 [US1] Rebuild all five production kits and prove zero `verify.py` problems, zero `validate_glyph.py` failures, and unchanged identity geometry using `scripts/build_all.py`
- [X] T015 [US1] Package exactly seven v1.2.0 candidate assets, generate notes, and pass the complete contract using `scripts/package_release.py` and `scripts/release_contract.py`
- [X] T016 [US1] Synchronize generated agent instructions and pass site lint, static export, browser route tests, responsive checks, both themes, and WCAG audits using `skill/templates/sync_agents_md.py` and `site/`
- [X] T017 [US1] Run Markdown, UTF-8 without BOM, LF, mojibake, sensitive-data, generated-artifact, and diff hygiene gates and record sanitized results in `specs/010-v1-2-release-certification/evidence.md`

**Checkpoint**: Issue #117 has complete candidate evidence and becomes eligible to close only when the reviewed pull request merges.

---

## Phase 4: Bounded Reviewed Handoff (User Story 2, Priority: P1)

**Goal**: Publish an official review-complete pull request without merging or tagging.

**Independent Test**: The pull request has successful required checks, every Codex comment is dispositioned, there are no unresolved actionable threads, and no more than one explicit review request exists.

- [X] T018 [US2] Update task state and candidate evidence, commit the S010 source revision, and verify the committed tree remains clean on `codex/010-v1-2-release-certification`
- [X] T019 [US2] Push the feature branch and open the official S010 pull request with `Closes #117`, `Tracks #116`, `Tracks #118`, and `Tracks #119`
- [X] T020 [US2] Process automatic Codex round one, file every negative finding as a linked Phase 12 issue, respond to every comment, implement and verify warranted corrections, resolve addressed threads, and update `specs/010-v1-2-release-certification/evidence.md`
- [X] T021 [US2] Post at most one explicit `@Codex review` comment after round one completes and record its immutable URL in `specs/010-v1-2-release-certification/evidence.md`
- [ ] T022 [US2] Process Codex round two without another review request, filing, correcting, responding, resolving, and recording every finding under the same policy
- [ ] T023 [US2] Wait for every required check to succeed, verify the pull request remains open with no v1.2.0 tag or release, and hand it to the owner for the final review and merge ritual

**Checkpoint**: User Story 2 is complete and execution halts at the owner merge gate.

---

## Phase 5: Evidence-Backed Public Release (User Story 3, Priority: P2)

**Goal**: Continue only after owner merge, publish v1.2.0 from verified main, and independently certify the public release.

**Independent Test**: The public release targets verified main and exactly seven freshly downloaded assets plus its notes pass the shared contract.

- [ ] T024 [US3] After owner merge, synchronize actual `origin/main`, prove it contains the reviewed S010 tree, and repeat the complete candidate validation from `specs/010-v1-2-release-certification/quickstart.md`
- [ ] T025 [US3] Create and push annotated tag v1.2.0 at the verified main revision, wait for the Release workflow, and record tag and workflow evidence in `specs/010-v1-2-release-certification/evidence.md`
- [ ] T026 [US3] Download the public release body and exactly seven assets into a fresh empty directory, pass `scripts/release_contract.py verify`, attach evidence to #118, and close #118 only if every criterion passes

**Checkpoint**: The public v1.2.0 release is independently certified.

---

## Phase 6: Qualified Production Deployment (User Story 4, Priority: P2)

**Goal**: Prove the deployed site and downloadable resources reflect the merged release without accessibility, discovery, or visual regressions.

**Independent Test**: The production contract passes for the Pages revision, full route inventory, representative downloads and registries, both themes, two viewports, and WCAG 2.1 AA.

- [ ] T027 [US4] Verify the Pages workflow and deployed merged-main revision, then record the immutable workflow and deployment evidence in `specs/010-v1-2-release-certification/evidence.md`
- [ ] T028 [US4] Execute `specs/010-v1-2-release-certification/contracts/production-certification.md` against production and attach sanitized route, resource, discovery, accessibility, and visual evidence to #119
- [ ] T029 [US4] Close #119 only after production evidence passes, then close parent #116 and milestone 22 only after re-querying all child and open-issue states
- [ ] T030 [US4] Complete the durable S010 evidence and task ledger through a reviewed follow-up only if post-merge public evidence requires repository changes

**Checkpoint**: S010 and Phase 12 are complete after public release and production proof.

---

## Dependencies & Execution Order

- T001 through T003 establish the tracking and specification foundation.
- T004 and T005 must demonstrate their intended failures before T006 and T007 implement the corresponding behavior.
- T006 and T007 precede T008 and all candidate metadata changes.
- T009 through T012 may proceed in parallel after the foundation but must all complete before T013 through T017.
- T013 through T017 complete before the commit in T018.
- T020 completes before the sole optional second-round request in T021. T022 cannot request another review.
- T023 is the owner merge gate. T024 through T030 cannot begin before the owner merges.
- T025 depends on actual-main revalidation in T024. T026 depends on successful tagged publication. T027 through T029 depend on merged-main Pages deployment.
- T030 is required only when durable post-merge repository evidence changes are warranted.

## Parallel Opportunities

- T004 and T005 touch independent test files.
- T009 through T012 update separate metadata and history surfaces after release behavior is established.
- Hosted CI observation and review observation may overlap after a push, but review round ordering stays strict.
- Release and Pages workflows may run concurrently after owner merge, while their issue closures remain evidence-specific.

## Implementation Strategy

1. Establish tracking and Spec Kit artifacts.
2. Add regression-first release authority changes.
3. Synchronize v1.2.0 metadata and history.
4. Produce complete local candidate evidence.
5. Publish once and process no more than two review rounds.
6. Stop at the owner merge gate.
7. Resume from actual main to publish, verify, qualify production, and close the hierarchy.
