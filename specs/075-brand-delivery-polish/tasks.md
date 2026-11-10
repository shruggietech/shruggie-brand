# Tasks: Brand Messaging and Delivery Polish

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [contract](contracts/messaging-presentation.md).

**Tests**: Autopilot test-driven discipline applies to message integrity and rendered layout changes.

## Phase 1: Setup

- [x] T001 Establish clean main baseline, S075 branch and installed Spec Kit artifacts in `specs/075-brand-delivery-polish/`.
- [x] T002 Investigate Cloudflare authentication and record exact permission failures in `specs/075-brand-delivery-polish/cloudflare.md`.

## Phase 2: Foundation

- [x] T003 Run blocking spec/plan/tasks analysis and record coverage in `specs/075-brand-delivery-polish/verification.md`.
- [x] T004 Probe existing renderer capabilities and preserve Local Media Gallery before evidence under ignored `dist/private/s075/`.

## Phase 3: US1 - Read the Brand Message First

**Goal**: Exact approved messages lead the guide opening at readable sizes.

**Independent Test**: Local Media Gallery before/after, dark/light and synthetic wrapping/rich/sparse covers with measured bounds and negative message-integrity checks.

- [x] T005 [US1] Add failing label-free, duplicate/wrong-role and unauthorized-value regressions in `skill/templates/test_messaging.py`.
- [x] T006 [US1] Add measured rich/wrapping/sparse cover regressions in `skill/templates/test_guide_cover.py`.
- [x] T007 [US1] Implement semantic label-free typography and bounded continuation layout in `skill/templates/gen_guide_pdf.py` and a focused shared helper if needed.
- [x] T008 [US1] Update exact projection/PDF verification in `skill/templates/verify.py`, retaining all negative integrity checks.
- [x] T009 [US1] Reconcile S067 cover-label contract/prose and current assertions in `specs/067-approved-messaging-guide-parity/` and `skill/templates/`.
- [x] T010 [US1] Inventory thirteen production kits across PDF, print HTML, portable and hosted openings and review representative rendered proofs in `specs/075-brand-delivery-polish/verification.md`.

## Phase 4: US2 - Publish Approved DanceWithMe865 Description

**Goal**: Existing short-description surfaces receive exact owner-approved text.

**Independent Test**: Exact source/projection comparisons and desktop/mobile portfolio inspection; live verification remains after authorized publication.

- [x] T011 [US2] Record approved wording, uses and 2026-11-09 provenance in `brands/dancewithme865/brand.json` and refresh only applicable continuity source bindings.
- [x] T012 [US2] Validate exact copy on generated outputs and desktop/mobile site surfaces, including 200% enlargement and 320 CSS-pixel reflow, recording evidence in `specs/075-brand-delivery-polish/verification.md`.

## Phase 5: US3 - Canonical Host Alias

**Goal**: Automated exact-host permanent edge redirect, contingent only on actual management access.

**Independent Test**: HTTP/HTTPS root/nested/query redirects, valid TLS, repeat-run no-op and preserved canonical routes.

- [x] T013 [US3] Record denied DNS/rule inspection, public baseline and required permissions in `specs/075-brand-delivery-polish/cloudflare.md`.
- [ ] T014 [US3] Reconcile alias DNS/Single Redirect, verify TLS/HTTP/idempotence and exercise rollback evidence in `specs/075-brand-delivery-polish/cloudflare.md` (blocked: DNS Edit and Single Redirect Edit access).

## Phase 6: Candidate and Validation

- [x] T015 Coordinate patch versions, release impact, migration/history and continuity hashes in existing release sources including `skill/references/release-impact.json`.
- [x] T016 Reproduce the required WordPress fixture audit failure and add filesystem compatibility coverage in `scripts/wordpress-runtime/dependency-test.cjs`.
- [x] T017 Pin patched transitive fixture dependencies and require zero audit findings in `scripts/wordpress-runtime/package.json` and `package-lock.json`.
- [x] T018 Run full documented contributor/CI-parity validation, rebuild all thirteen kits and verify packages/site, recording results in `specs/075-brand-delivery-polish/verification.md`.
- [x] T019 Audit source-only Git state, UTF-8 without BOM/LF and mojibake; synchronize tasks/evidence in `specs/075-brand-delivery-polish/`.
- [x] T020 Commit verified source locally and present exact pre-push command and remaining deviations, including #352 and pending publication, in `specs/075-brand-delivery-polish/verification.md`.
- [ ] T021 Complete Pages deployment and direct live issue verification per `specs/075-brand-delivery-polish/deployment.md`. Authorization, PR #354 review/CI/merge and the official v3.1.2 release are complete; three Pages attempts timed out, so live acceptance and #328/#353 closure remain blocked.

## Dependencies and Execution Order

Setup precedes foundation; analysis blocks implementation. T005/T006 precede T007/T008. US2 is independently implementable after foundation; its build joins US1 validation. US3 access failure blocks only T014. Candidate validation follows repository changes and precedes local commit. The pre-push checkpoint was explicitly approved on 2026-11-10. T021 now remains blocked by Pages deployment, independently of the Cloudflare blocker.

## Parallel Opportunities

Cloudflare read-only research and local source research can proceed independently. Projection unit checks and source-only audits may run together; do not run delivery checks against kits being replaced by build_all.py. No parallel agent implementation is required.

## Implementation Strategy

Ship US1/US2 together through one rebuild/candidate; preserve the authorized external blocker for US3. This staged result does not claim full three-issue completion or live publication until evidence exists.

## Phase 7: Pages Recovery Continuation

- [x] T022 Investigate current Pages API, upstream action, source workflow and exact uploaded artifact; record findings in `specs/075-brand-delivery-polish/deployment.md`.
- [ ] T023 Refresh the existing Pages configuration, use documented same-domain certificate reprovisioning if required to restore HTTPS enforcement, and compare private snapshots/public identity; record the observed outcome in `specs/075-brand-delivery-polish/deployment.md`.
- [x] T024 Specify the qualified-artifact recovery contract in `specs/075-brand-delivery-polish/plan.md` and `contracts/pages-recovery.md`, then run blocking analysis before implementation.
- [x] T025 Add failing provenance, digest, release-consistency and archive-boundary tests in `scripts/test_pages_recovery.py` and workflow invariants in `scripts/test_publication_workflow.py`.
- [x] T026 Implement qualified source/candidate/TAR validation and hidden noninteractive launches in `scripts/recover_pages.py`.
- [x] T027 Add main-only manual artifact preparation/deployment, isolated concurrency and correct action labels to `.github/workflows/build.yml`; record the decision in `CHANGELOG.md`.
- [ ] T028 Run targeted tests, real original-artifact preflight, required review/CI and merge; record evidence in `specs/075-brand-delivery-polish/verification.md`.
- [ ] T029 Activate the exact v3.1.2 TAR through the fresh controller, restore HTTPS enforcement, run existing live acceptance and close #328/#353 in `specs/075-brand-delivery-polish/verification.md`; keep #352 open.

T023 depends on T022 and the supplemental analysis. T024 depends on the observed T023 result; a further blocking analysis covers any resulting code changes. T025 precedes T026/T027. T028 follows implementation; T029 preserves the original T021 done-gate.
