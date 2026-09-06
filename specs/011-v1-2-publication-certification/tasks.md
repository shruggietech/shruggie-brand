# Tasks: v1.2.0 Publication and Production Certification

**Input**: Design documents from `specs/011-v1-2-publication-certification/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Regression-first origin selection, full candidate validation, public release verification, complete production browser verification, and repository hygiene are mandatory.

## Phase 1: Setup and Traceability

- [X] T001 Create issue #129 under milestone 22 and link S011 to #116, #118, and #119
- [X] T002 Create the S011 specification, plan, research, data model, contracts, quickstart, checklist, evidence, and task ledger
- [X] T003 Analyze the complete S011 artifact set and resolve every inconsistency before implementation

## Phase 2: Production Verification Foundation

- [X] T004 [P] [US2] Add failing origin-selection tests in `site/tests/production-origin.test.mjs` for local fallback, approved HTTPS production, HTTP rejection, and unexpected-host rejection
- [X] T005 [US2] Implement the narrow origin-selection contract in `site/scripts/verification-origin.mjs`
- [X] T006 [US2] Integrate production-origin mode into `site/scripts/verify-site.mjs` without weakening existing checks or closing a server that was not started
- [X] T007 [US2] Run focused origin tests and the complete local site lint, static build, and browser verifier

## Phase 3: Verified Public Release (User Story 1, Priority: P1)

- [X] T008 [US1] Revalidate the exact merged main revision with the complete S010 candidate command set and record sanitized results in `evidence.md`
- [X] T009 [US1] Prove no conflicting v1.2.0 tag or release exists, create one annotated tag at verified main, push it, and verify the resolved tag target
- [X] T010 [US1] Wait for the tag-triggered Release workflow and prove it succeeded for v1.2.0
- [X] T011 [US1] Inspect public release state and notes, download exactly seven assets into a fresh ignored directory, run the release contract, and attach evidence to #118

## Phase 4: Qualified Production Deployment (User Story 2, Priority: P1)

- [X] T012 [US2] Verify the successful Pages workflow targets the exact merged main revision
- [X] T013 [US2] Run the complete site verifier against `https://brand.shruggie.tech` and record sanitized route, resource, metadata, responsive, theme, and accessibility results
- [X] T014 [US2] Inspect representative production screenshots in both themes and widths, record the result, and attach evidence to #119

## Phase 5: Reviewable Closure Evidence (User Story 3, Priority: P2)

- [X] T015 [US3] Complete `evidence.md`, update the task ledger, and run Markdown, encoding, sensitive-data, generated-artifact, diff, and git-status gates
- [X] T016 [US3] Commit, push, and open the official S011 pull request with closure links for #116, #118, #119, and #129
- [X] T017 [US3] Process automatic Codex round one, file every negative finding, respond to every comment, implement and verify warranted corrections, and resolve addressed threads
- [ ] T018 [US3] Post at most one explicit `@Codex review` request after round one completes and record its URL
- [ ] T019 [US3] Process round two without another trigger, disposition every comment, wait for all required checks to succeed, and update the durable review ledger
- [ ] T020 [US3] Stop with the pull request open and ask the owner for the final review and merge ritual

## Dependencies & Execution Order

- T001 through T003 complete before implementation.
- T004 must fail for the intended missing behavior before T005 and T006.
- T007 completes before remote production use.
- T008 completes before T009. T010 and T011 depend on the pushed tag.
- T012 through T014 depend on the merged-main deployment and production-origin verifier.
- T015 completes before publication of the evidence PR.
- T017 completes before the sole optional second-round request in T018. T019 cannot trigger another review.
- T020 is the owner merge gate. S011 never merges its own pull request.

## Implementation Strategy

1. Converge the specification and fail-closed production verifier.
2. Revalidate and publish the exact merged main revision.
3. Independently verify the public assets and production site.
4. Publish durable evidence and complete no more than two review rounds.
5. Halt for owner merge.
