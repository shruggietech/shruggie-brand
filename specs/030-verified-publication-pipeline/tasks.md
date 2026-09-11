# Tasks: Verified Publication Pipeline

**Input**: Design documents from `specs/030-verified-publication-pipeline/`
**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/verified-publication.md`, `quickstart.md`

**Tests**: Required. This slice changes the protected CI boundary and both publication paths, so contract tests and mutation-style artifact-audit tests precede implementation.

**Organization**: Tasks are grouped by user story so each publication outcome can be implemented and verified independently.

## Phase 1: Setup

**Purpose**: Establish traceability and preserve the known failing baseline.

- [X] T001 Record issue #196, failed Pages run 34633145579, passing Build run 34633145470, production deployment 6382937945, and the S030 branch in `specs/030-verified-publication-pipeline/evidence.md`
- [X] T002 Confirm the S030 specification, plan, contracts, and reviewer checklists are internally complete in `specs/030-verified-publication-pipeline/`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add the reusable publication-artifact boundary and its test harness before changing workflow behavior.

**CRITICAL**: No user story work begins until this phase is complete.

- [X] T003 Add failing mutation tests for symlinks, unexpected hidden paths, and missing or extra governed manifests in `scripts/test_publication_workflow.py`
- [X] T004 Add failing source-contract tests for immutable action pins, SHA-qualified artifact names, exact checkout revisions, and job-scoped publisher permissions in `scripts/test_publication_workflow.py`
- [X] T005 Implement the publication artifact auditor in `scripts/audit_publication_artifacts.py`
- [X] T006 Run the focused publication workflow tests and record the red-to-green result in `specs/030-verified-publication-pipeline/evidence.md`

**Checkpoint**: Artifact contents and workflow source can now be verified independently of hosted Actions.

---

## Phase 3: User Story 1 - Publish the verified main revision (Priority: P1) MVP

**Goal**: A successful protected `build` for an exact main commit feeds the Pages publisher from same-run verified artifacts, with no renderer or dependency reconstruction.

**Independent Test**: Exercise the workflow contract tests, build the site locally, audit its staged publication contents, and verify that the deploy job can consume only the SHA-qualified Pages artifact after the aggregate `build` succeeds.

### Tests for User Story 1

- [X] T007 [US1] Add failing regression tests for main-only deployment, stable main concurrency, same-run Pages artifacts, and no publisher checkout in `scripts/test_publication_workflow.py`

### Implementation for User Story 1

- [X] T008 [US1] Consolidate verified build and Pages publication orchestration into `.github/workflows/build.yml`
- [X] T009 [US1] Wire the publication auditor and SHA-qualified Pages artifact upload into `.github/workflows/build.yml`
- [X] T010 [US1] Remove the superseded independent Pages workflow at `.github/workflows/pages.yml`
- [X] T011 [US1] Run the US1 contract tests plus a local site build and publication audit, then record evidence in `specs/030-verified-publication-pipeline/evidence.md`

**Checkpoint**: Main publication reuses the exact verified site artifact and cannot race a newer main deployment.

---

## Phase 4: User Story 2 - Detect publication defects before merge (Priority: P2)

**Goal**: Pull requests exercise the same publication-sensitive build path while the required `build` context remains exact, terminal, and merge-blocking.

**Independent Test**: Verify PR triggers do not publish, the terminal `build` job depends on every required verifier, skipped or failed prerequisites make `build` fail, and branch pushes do not duplicate the PR workload.

### Tests for User Story 2

- [X] T012 [US2] Add failing regression tests for PR-only verification, branch-push deduplication, the exact required `build` context, and aggregate failure semantics in `scripts/test_publication_workflow.py`

### Implementation for User Story 2

- [X] T013 [US2] Restructure `.github/workflows/build.yml` into compatibility, approved-proof, verified-build, and terminal `build` jobs
- [X] T014 [US2] Run publication workflow tests from both Python 3.8 compatibility and verified-build jobs in `.github/workflows/build.yml`
- [X] T015 [US2] Verify the active branch ruleset still requires the exact `build` context and record the result in `specs/030-verified-publication-pipeline/evidence.md`

**Checkpoint**: Pull requests prove the publication-sensitive path without write permissions or duplicate branch-push builds.

---

## Phase 5: User Story 3 - Publish releases through the same verified boundary (Priority: P3)

**Goal**: A version tag on main publishes only SHA-qualified, checksummed release assets produced by the successful verified build.

**Independent Test**: Build an ephemeral release candidate, validate its source marker and SHA256 inventory without repository scripts, reject version or main-ancestry mismatches, and verify that the write-capable release job has no checkout.

### Tests for User Story 3

- [X] T016 [US3] Add failing regression tests for release-candidate provenance, tag/version agreement, main ancestry, checksum verification, and checkout-free publishing in `scripts/test_publication_workflow.py`
- [X] T017 [US3] Update release workflow contract coverage for the consolidated pipeline in `scripts/test_release_contract.py`

### Implementation for User Story 3

- [X] T018 [US3] Add read-only release preflight and ephemeral release-candidate staging to `.github/workflows/build.yml`
- [X] T019 [US3] Add the least-privilege checkout-free GitHub Release publisher to `.github/workflows/build.yml`
- [X] T020 [US3] Remove the superseded independent release workflow at `.github/workflows/release.yml`
- [X] T021 [US3] Run the release dry-run and source/checksum verification from `specs/030-verified-publication-pipeline/quickstart.md`, then record evidence in `specs/030-verified-publication-pipeline/evidence.md`

**Checkpoint**: Both Pages and release publication cross the same verified artifact boundary.

---

## Phase 6: Polish and Cross-Cutting Concerns

**Purpose**: Synchronize documentation, run the full validation matrix, and complete hosted review reconciliation.

- [X] T022 Update the repository change log for S030 in `CHANGELOG.md`
- [X] T023 Complete all reviewer-owned requirement checks in `specs/030-verified-publication-pipeline/checklists/publication.md`
- [X] T024 Run the full S030 quickstart, actionlint, encoding, mojibake, generated-artifact, and diff sanity checks, recording results in `specs/030-verified-publication-pipeline/evidence.md`
- [X] T025 Re-run Spec Kit analysis and synchronize `spec.md`, `plan.md`, `tasks.md`, contracts, quickstart, and evidence under `specs/030-verified-publication-pipeline/`
- [X] T026 Commit S030 with a Conventional Commit subject, push `codex/030-verified-publication-pipeline`, and open the official pull request closing issue #196
- [ ] T027 Monitor hosted CI and the first Codex/security review round, address every actionable comment, reply to each thread, and resolve completed threads
- [ ] T028 Trigger at most one second Codex review round if needed, reconcile every resulting comment, and record the review outcome in `specs/030-verified-publication-pipeline/evidence.md`
- [ ] T029 Confirm the final pull request head has green required checks and no unresolved review threads, then request the owner's final review and merge ritual

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: Starts immediately.
- **Foundational (Phase 2)**: Depends on Setup and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational and supplies the Pages MVP.
- **User Story 2 (Phase 4)**: Depends on User Story 1 because it makes the shared workflow terminal and branch-protection compatible.
- **User Story 3 (Phase 5)**: Depends on User Stories 1 and 2 because it reuses their verified build and terminal gate.
- **Polish (Phase 6)**: Depends on all user stories.

### User Story Dependencies

- **US1**: Uses only the foundational auditor and contract harness.
- **US2**: Extends the US1 workflow while preserving the exact protected `build` context.
- **US3**: Consumes the verified artifacts and terminal gate established by US1 and US2.

### Within Each User Story

- Write contract tests and observe failure before workflow implementation.
- Implement the smallest workflow change that satisfies the tests.
- Run focused local verification before advancing.
- Record evidence as each checkpoint completes.

### Parallel Opportunities

- Documentation review in T002 can occur while T001 evidence is assembled.
- Mutation cases within T003 are independent once the test harness exists.
- Hosted CI and independent external reviews in T027 run concurrently after the pull request opens.

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Setup and Foundational phases.
2. Complete US1 so Pages consumes the exact verified site artifact.
3. Validate the independent US1 checkpoint before restructuring the protected gate.

### Incremental Delivery

1. Establish provenance and content auditing.
2. Put Pages behind the verified same-run artifact boundary.
3. Preserve the exact protected `build` context with terminal aggregation and remove duplicate branch work.
4. Put releases behind the same boundary with read-only preflight and a minimal publisher.
5. Complete local gates, hosted CI, and no more than two Codex review rounds.

---

## Notes

- `[P]` denotes tasks safe to perform concurrently because they touch different files and have no incomplete dependency.
- `[US1]`, `[US2]`, and `[US3]` map tasks to the specification's independently testable user stories.
- No task is marked `[P]` when it edits `.github/workflows/build.yml` or `scripts/test_publication_workflow.py`, avoiding shared-file conflicts.
- Publication never rebuilds, redraws, or normalizes governed identity inputs.
- The owner-authorized autopilot exception permits push and pull-request creation without the normal Spec Kit halt. Merge remains owner-only.
