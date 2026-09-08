# Tasks: Asset Delivery Fidelity

**Input**: Design documents from `/specs/021-asset-delivery-fidelity/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: S021 requires test-first structural, rendered-output, and browser-layout regression coverage.

**Organization**: Tasks are grouped by user story so each fidelity boundary remains independently testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run independently in a different file after its prerequisites
- **[Story]**: Maps the task to a user story in `spec.md`
- Every task names its exact file or output path

## Phase 1: Setup and Baseline

**Purpose**: Freeze protected data and record reproducible failures before implementation.

- [X] T001 Record S021 issue scope and current branch in `specs/021-asset-delivery-fidelity/spec.md`
- [X] T002 Hash and record the unchanged Glitchpad full and reduced paths in `specs/021-asset-delivery-fidelity/evidence.md`
- [X] T003 Build the current Glitchpad kit and record black/white horizontal and stacked mark-region failures in `specs/021-asset-delivery-fidelity/evidence.md`
- [X] T004 [P] Record the current asset-preview layout and delivery hashes for presentation-only comparison in `specs/021-asset-delivery-fidelity/evidence.md`

---

## Phase 2: Foundational Test Contracts

**Purpose**: Establish failing regressions and shared acceptance helpers before production corrections.

**CRITICAL**: Production implementation begins only after these tests demonstrate the reported failures.

- [X] T005 Add an isolated implicit-mask clipping regression for nested lockups in `skill/templates/test_pipeline.py`
- [X] T006 Add black and white horizontal and stacked mark-height and component-presence assertions in `skill/templates/test_pipeline.py`
- [X] T007 Add verifier rejection cases for incomplete square-knockout mask coverage in `skill/templates/test_pipeline.py`
- [X] T008 [P] Add static exact-delivery and shared-preview-structure expectations in `site/tests/site.test.mjs`
- [X] T009 Add browser helpers for preview, inner media, image, and divider bounds in `site/scripts/verify-site.mjs`
- [X] T010 Run the focused regressions and record their expected pre-fix failures in `specs/021-asset-delivery-fidelity/evidence.md`

**Checkpoint**: Both reported defect classes have reproducible failing tests.

---

## Phase 3: User Story 1 - Download Complete Monochrome Glitchpad Lockups (Priority: P1) MVP

**Goal**: Restore the complete approved square-based paper-and-G mark and wordmark in every black and white full lockup.

**Independent Test**: Generate Glitchpad alone and prove that both horizontal and stacked black/white SVG and PNG outputs retain the complete mark region, wordmark, source paths, proportions, and canvas placement.

### Tests for User Story 1

- [X] T011 [US1] Confirm T005 through T007 fail on the current generator in `skill/templates/test_pipeline.py`
- [X] T012 [US1] Preserve exact Glitchpad source path hashes through the regression fixture in `skill/templates/test_pipeline.py`

### Implementation for User Story 1

- [X] T013 [US1] Declare explicit local square-knockout mask coordinates and extent in `skill/templates/gen_logo.py`
- [X] T014 [US1] Preserve existing full/reduced selection, lockup measurements, and monochrome role behavior in `skill/templates/gen_logo.py`
- [X] T015 [US1] Rebuild Glitchpad and confirm all four affected SVG masters and PNG deliveries are complete under `dist/glitchpad/logos/`
- [X] T016 [US1] Visually inspect corrected black and white horizontal and stacked outputs and record results in `specs/021-asset-delivery-fidelity/evidence.md`

**Checkpoint**: User Story 1 is independently complete and the P0 public identity defect is corrected.

---

## Phase 4: User Story 2 - Trust Every Asset Preview (Priority: P2)

**Goal**: Center and contain exact shipped assets in one shared media region above card metadata.

**Independent Test**: Render every production asset page and guideline logo example with wide, tall, square, transparent, and opaque assets at mobile, tablet, and desktop widths in both themes; all image and presentation bounds remain centered and above the divider.

### Tests for User Story 2

- [X] T017 [US2] Confirm T008 and T009 expose the current missing shared media boundary in `site/tests/site.test.mjs` and `site/scripts/verify-site.mjs`
- [X] T018 [P] [US2] Add exact preview-to-delivery membership assertions in `site/tests/site.test.mjs`
- [X] T019 [US2] Add one-device-pixel centering and containment assertions for asset cards in `site/scripts/verify-site.mjs`
- [X] T020 [US2] Add equivalent containment assertions for guideline logo examples in `site/scripts/verify-site.mjs`
- [X] T021 [US2] Cover mobile, tablet, desktop, both themes, and 200 percent zoom in `site/scripts/verify-site.mjs`

### Implementation for User Story 2

- [X] T022 [P] [US2] Add the shared inner media wrapper to asset cards in `site/components/guidelines/asset-library-client.tsx`
- [X] T023 [P] [US2] Add the same inner media wrapper to logo examples in `site/components/guidelines/topic-content.tsx`
- [X] T024 [US2] Implement one fixed, clipped, centered preview viewport and axis-constrained image contract in `site/app/globals.css`
- [X] T025 [US2] Preserve generated light/dark wells, exact URLs, intrinsic aspect ratios, and metadata layout in `site/app/globals.css`
- [X] T026 [US2] Confirm presentation changes leave generated asset delivery hashes unchanged and record the comparison in `specs/021-asset-delivery-fidelity/evidence.md`

**Checkpoint**: User Story 2 is independently complete across every generated brand asset page.

---

## Phase 5: User Story 3 - Prevent Delivery and Preview Regressions (Priority: P3)

**Goal**: Fail publication when monochrome marks clip or preview content crosses its media boundary.

**Independent Test**: Mutate an isolated mask to reproduce the fold-fragment failure and mutate a preview fixture to cross its divider; each gate identifies and rejects the defect.

### Tests for User Story 3

- [X] T027 [P] [US3] Add malformed, undersized, and missing mask-region fixtures in `skill/templates/test_pipeline.py`
- [X] T028 [P] [US3] Add preview overflow and off-center negative cases in `site/scripts/verify-site.mjs`

### Implementation for User Story 3

- [X] T029 [US3] Validate square-knockout mask units, explicit bounds, target coverage, and references in `skill/templates/verify.py`
- [X] T030 [US3] Validate rendered full monochrome lockup mark height and SVG-to-PNG agreement in `skill/templates/verify.py`
- [X] T031 [US3] Report affected derivative paths and failed boundaries in verifier diagnostics from `skill/templates/verify.py`
- [X] T032 [US3] Run isolated negative regressions and record fail-closed evidence in `specs/021-asset-delivery-fidelity/evidence.md`

**Checkpoint**: Both defect classes fail before publication and all user stories are complete.

---

## Phase 6: Polish and Cross-Cutting Validation

**Purpose**: Complete documentation, full production validation, and delivery automation.

- [X] T033 [P] Add the S021 correction and dated architecture decision to `CHANGELOG.md`
- [X] T034 [P] Document shared generator behavior in `skill/CHANGELOG.md`
- [X] T035 Run Markdown, package, release, prepare-site, brand-contract, glyph-kit, icon-kit, and pipeline tests listed in `specs/021-asset-delivery-fidelity/quickstart.md`
- [X] T036 Build all six production kits with zero verifier problems and zero glyph failures using `scripts/build_all.py`
- [X] T037 Run site preparation, lint, static build, responsive route audit, and WCAG 2.1 AA checks from `specs/021-asset-delivery-fidelity/quickstart.md`
- [X] T038 Inspect representative Glitchpad lockups and all-brand asset pages in both themes and record results in `specs/021-asset-delivery-fidelity/evidence.md`
- [X] T039 Run Spec Kit cross-artifact analysis and resolve every CRITICAL or HIGH finding across `specs/021-asset-delivery-fidelity/`
- [X] T040 Audit UTF-8 without BOM, LF, mojibake, ignored generated output, and clean source hashes in `specs/021-asset-delivery-fidelity/evidence.md`
- [X] T041 Commit S021 with Conventional Commit traceability on `codex/021-asset-delivery-fidelity`
- [X] T042 Push the authorized feature branch and open an official PR closing #166 and #165
- [X] T043 Reconcile every CI result and first-round Codex review comment, replying to and resolving all findings
- [X] T044 Request at most one authorized second Codex review round, reconcile every response, and return only when CI and reviews are satisfied

## Dependencies and Execution Order

- Phase 1 precedes all implementation and freezes the identity and artifact baseline.
- Phase 2 tests precede the production generator and site corrections.
- User Story 1 is the P0 MVP and can be completed without User Story 2.
- User Story 2 depends only on the shared baseline and can be tested independently of generator correctness using other production brands.
- User Story 3 consumes the failure modes established by User Stories 1 and 2 and makes them durable publication gates.
- Final validation depends on all three stories.

## Parallel Opportunities

- T004 can run while T002 and T003 capture generator evidence.
- T008 can be authored independently of T005 through T007.
- T022 and T023 affect separate shared components after the static contract is defined.
- T027 and T028 cover separate generator and browser failure domains.
- T033 and T034 update separate changelogs after behavior is stable.

## Implementation Strategy

### MVP First

1. Freeze source hashes and reproduce the clipped mask.
2. Add failing structural and rendered lockup regressions.
3. Correct explicit mask bounds and verify Glitchpad alone.
4. Continue immediately into shared preview containment under autopilot.

### Incremental Delivery

1. User Story 1 restores release-blocking identity output.
2. User Story 2 restores trustworthy public asset presentation.
3. User Story 3 prevents both failures from recurring.
4. Full validation proves no unrelated identity or delivery changes.

## Notes

- The custom checklist remains reviewer-owned and its items stay unchecked unless the reviewer explicitly evaluates them.
- Test completion markers record implementation work, not owner approval.
- No subagent work is used for this slice.
