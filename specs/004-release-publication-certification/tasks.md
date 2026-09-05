# Tasks: v1.1.2 Release and Publication Certification

**Input**: Design documents from `specs/004-release-publication-certification/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: Regression-first unit tests are required for the release contract and manifest-version defect. Existing aggregate tests and builds are reused for unchanged identity, accessibility, site, and packaging surfaces.

**Organization**: Tasks are chronological across the pre-merge readiness stage, owner merge gate, and post-merge publication continuation.

## Phase 1: Baseline and Public Traceability

**Purpose**: Pin the authoritative release state and make S004 visible before implementation changes.

- [X] T001 Record the base SHA, absent v1.1.2 tag/release, open child/parent/milestone states, and discovered release contradictions in `specs/004-release-publication-certification/evidence.md`
- [X] T002 Create the S004 GitHub slice issue with `slice`, `spec-kit`, `area: release`, `area: docs`, `priority: P0`, `effort: M`, and `task` labels; link #63, #72, #73, #10, #13, and #37 in `specs/004-release-publication-certification/evidence.md`

**Checkpoint**: Release baseline and slice scope are publicly traceable without exposing private operational data.

---

## Phase 2: Trustworthy Release Candidate (User Story 1, Priority: P1)

**Goal**: Make v1.1.2 notes, metadata, packaging, and archive validation one reproducible release contract.

**Independent Test**: Freshly generate notes and seven archives, then run `scripts/release_contract.py verify` with zero failures and exact expected filenames.

### Regression tests

- [X] T003 [US1] Add failing metadata, notes, archive-shape, exact-asset, version, unsafe-path, and checksum regression cases in `scripts/test_release_contract.py`
- [X] T004 [US1] Extend the manifest-version regression in `skill/templates/test_pipeline.py` so Fragcap-style non-1.0.0 kit metadata fails before the generator correction

### Implementation

- [X] T005 [US1] Implement Python 3.8-compatible metadata parsing, changelog extraction, notes generation, expected asset enumeration, and archive verification in `scripts/release_contract.py`
- [X] T006 [US1] Generate `manifest.json` version from the kit's declared version in `skill/templates/build_kit.py` and make the manifest regression pass in `skill/templates/test_pipeline.py`
- [X] T007 [US1] Make packaging clean only the validated ignored release directory and reuse the expected release contract in `scripts/package_release.py`
- [X] T008 [US1] Fold merged S003 fixes into 1.1.2, align the actual release date, and preserve complete 1.1.0 through 1.1.2 history in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [X] T009 [US1] Run release-contract tests in Python 3.8 CI and run full notes, package, and archive preflight in `.github/workflows/build.yml`
- [X] T010 [US1] Replace hardcoded release notes and inline license-only checks with generated notes and the shared verifier in `.github/workflows/release.yml`
- [X] T011 [US1] Run steps 1 through 5 of `specs/004-release-publication-certification/quickstart.md`, including isolated clean-checkout verification, and record sanitized results in `specs/004-release-publication-certification/evidence.md`
- [X] T012 [US1] Add acceptance-specific pre-merge evidence to #63, #72, and #73 while explicitly retaining their open publication-dependent state; record comment links in `specs/004-release-publication-certification/evidence.md`

**Checkpoint**: User Story 1 is independently complete. The release candidate is reproducible, but no tag or release exists.

---

## Phase 3: Bounded Reviewed Publication (User Story 2, Priority: P1)

**Goal**: Deliver an open, green, review-complete S004 pull request without exceeding the authorized two-round ceiling.

**Independent Test**: The pull request is open, required checks are green, every review comment is answered and resolved, every negative finding has an issue, exactly one explicit `@Codex` request exists, and no tag or release has been created.

- [X] T013 [US2] Complete `specs/004-release-publication-certification/evidence.md`, mark finished pre-merge tasks, run `git diff --check` and the full quickstart, and create a Conventional Commit for S004
- [X] T014 [US2] Push `codex/004-release-publication-certification` and open the official pull request with issue traceability, release evidence, explicit post-merge work, and the initial ledger from `specs/004-release-publication-certification/contracts/review-ledger.md`
- [X] T015 [US2] Observe automatic Codex round 1, file every negative finding as a GitHub issue, respond to every comment, implement and verify warranted corrections, push them, resolve every addressed thread, and update `specs/004-release-publication-certification/evidence.md` plus the pull-request ledger
- [X] T016 [US2] Post exactly one `@Codex` pull-request comment for round 2 and record its immutable URL in `specs/004-release-publication-certification/evidence.md`
- [X] T017 [US2] Observe Codex round 2, file every new negative finding as a GitHub issue, respond to every comment, implement and verify warranted corrections, push them, resolve every addressed thread, and update `specs/004-release-publication-certification/evidence.md` plus the pull-request ledger without another review request
- [X] T018 [US2] Wait for every required continuous-integration check to succeed, verify the pull request remains open and review-complete with no v1.1.2 tag or release, and hand it to the owner for the final review and merge ritual

**Checkpoint**: User Story 2 is complete and execution halts at the owner merge gate.

---

## Phase 4: Evidence-Backed Public Release (User Story 3, Priority: P2)

**Goal**: Continue only after owner merge, publish v1.1.2 from verified main, inspect downloaded assets, and close the evidence-complete release hierarchy.

**Independent Test**: The public release targets verified main, exactly seven downloaded assets and its notes pass the shared contract, and GitHub child, parent, and milestone states match their acceptance policies.

- [X] T019 [US3] After owner merge, fetch and reconcile actual `origin/main`, prove it contains the reviewed S004 tree, and rerun the complete `specs/004-release-publication-certification/quickstart.md` preflight against that revision
- [X] T020 [US3] Create and push annotated tag v1.1.2 at the verified main revision, wait for the Release workflow to succeed, and record tag target plus workflow URL in `specs/004-release-publication-certification/evidence.md`
- [X] T021 [US3] Download the published release body and all assets into a fresh temporary directory, run `scripts/release_contract.py verify`, and record the release URL, exact seven assets, and zero-failure result in `specs/004-release-publication-certification/evidence.md`
- [X] T022 [US3] Attach published acceptance evidence to and close #63, #72, and #73; then close eligible parents #10 and #13 and milestones 15 and 18 only after re-querying their complete child and open-issue sets
- [X] T023 [US3] Update #37 and the S004 slice issue with the release outcome and next remaining work, complete `specs/004-release-publication-certification/evidence.md`, and synchronize final S004 task state through a documentation pull request if post-merge evidence changes require committed records

**Checkpoint**: User Story 3 and S004 completed after published verification and child-first GitHub housekeeping.

---

## Dependencies & Execution Order

- T001 and T002 establish the evidence and public tracking foundation.
- T003 and T004 must fail for their intended regressions before T005 and T006 implement corrections.
- T005 precedes packaging and workflow integration. T006 through T010 complete before aggregate preflight.
- T011 completes before GitHub issue evidence in T012 and before the publication commit in T013.
- T015 completes before the sole round 2 request in T016.
- T017 completes before the final hosted gate in T018.
- T018 halts for the owner merge ritual. T019 through T023 cannot begin before that merge.
- T020 depends on successful actual-main validation in T019. T021 depends on successful tagged publication. T022 depends on published verification. T023 is last.

## Parallel Opportunities

- Metadata/archive unit tests and the manifest regression touch separate test surfaces, but both intentionally precede their corresponding implementation.
- Root and bundled changelog review can proceed alongside workflow inspection after the release-contract behavior is fixed.
- Hosted CI observation and review observation can overlap after each push, while round ordering remains strict.
- Post-publication issue evidence can share one downloaded verification result, but each issue decision remains criterion-specific and child-first.

## Implementation Strategy

1. Establish public traceability and freeze the baseline.
2. Build the release contract with regression-first corrections.
3. Produce complete local and clean-checkout evidence.
4. Publish once and process exactly two bounded review rounds.
5. Stop at the owner merge gate.
6. Resume from actual merged main, publish, verify, and close the release hierarchy.
