# Tasks: Site Interaction Affordances

**Input**: Design documents from `/specs/022-site-interaction-affordances/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Test-first source and rendered coverage is required by the specification and autopilot protocol.

**Organization**: Tasks are grouped by user story so each outcome remains independently testable.

## Phase 1: Setup and Baseline

**Purpose**: Freeze the current shared interaction structure and scope before changing behavior.

- [X] T001 Capture the six footer labels, destinations, order, and current target/relationship attributes in `specs/022-site-interaction-affordances/evidence.md`
- [X] T002 Capture the dependency-rendered pagination and theme-switch DOM contracts in `specs/022-site-interaction-affordances/evidence.md`
- [X] T003 Record the explicit Company same-tab decision and rejected hostname-inference alternative in `specs/022-site-interaction-affordances/research.md`
- [X] T004 Verify `.gitignore` and site ignore/configuration boundaries cover generated content, exports, screenshots, caches, and `.specify/feature.json`

---

## Phase 2: Foundational Test Seams

**Purpose**: Establish reusable static and rendered assertions before story implementation.

- [X] T005 Add a source-level footer destination policy parser and exact six-link assertion in `site/tests/site.test.mjs`
- [X] T006 Add source-level pagination alignment and stable-icon selector assertions in `site/tests/site.test.mjs`
- [X] T007 Add source-level enabled and disabled theme-cursor selector assertions in `site/tests/site.test.mjs`
- [X] T008 Add reusable rendered style, focus, geometry, and semantic measurement helpers in `site/scripts/verify-site.mjs`

**Checkpoint**: Shared test seams fail against the current behavior and identify the expected contract gaps.

---

## Phase 3: User Story 1 - Keep the brand site available from selected footer links (Priority: P1) MVP

**Goal**: Apply safe separate-context behavior to exactly Download the skill, Source, and License while keeping Brands, Documentation, and Company same-tab.

**Independent Test**: Inspect every shared footer destination and activate representative links with keyboard input. Exactly three links carry `_blank` plus `noopener noreferrer`, and all other labels, URLs, order, focus, and layout remain unchanged.

### Tests for User Story 1

- [X] T009 [US1] Add isolated negative footer-policy fixtures for missing safety metadata and accidental same-tab-link targeting in `site/tests/site.test.mjs`
- [X] T010 [US1] Add rendered footer metadata, target-size, and keyboard-focus assertions on marketing and documentation routes in `site/scripts/verify-site.mjs`

### Implementation for User Story 1

- [X] T011 [US1] Define the ordered shared footer destination records in `site/components/footer.tsx`
- [X] T012 [US1] Render internal, same-tab external, and safe separate-context records without changing labels or destinations in `site/components/footer.tsx`
- [X] T013 [US1] Run the source-level site contract and confirm all footer policy cases pass

**Checkpoint**: Issue #163 is independently satisfied across every shared-footer instance.

---

## Phase 4: User Story 2 - Recognize and follow documentation controls (Priority: P2)

**Goal**: Center previous/next chevrons with complete labels and expose pointer cursors only on enabled theme controls.

**Independent Test**: Measure index, interior, and endpoint pagination cues plus theme controls at 360 and 1280 pixels in both themes. Center delta remains at most one pixel, icons do not shrink, and cursor state matches actual enabled/disabled semantics.

### Tests for User Story 2

- [X] T014 [US2] Add rendered previous/next label-group center and chevron-size assertions in `site/scripts/verify-site.mjs`
- [X] T015 [US2] Add rendered theme-control cursor, accessible-name, enabled/disabled, focus, target-size, and keyboard-transition assertions in `site/scripts/verify-site.mjs`

### Implementation for User Story 2

- [X] T016 [US2] Add shared pagination cue-row alignment and zero-margin label rules in `site/app/globals.css`
- [X] T017 [US2] Add stable non-shrinking pagination chevron dimensions in `site/app/globals.css`
- [X] T018 [US2] Add enabled pointer and disabled cursor rules for root and nested theme buttons in `site/app/globals.css`
- [X] T019 [US2] Run focused rendered checks for index, interior, and endpoint documentation routes in both themes and widths

**Checkpoint**: Issue #164 is independently satisfied without replacing dependency components.

---

## Phase 5: User Story 3 - Prevent interaction-affordance regressions (Priority: P3)

**Goal**: Make each footer, alignment, and cursor defect fail before publication.

**Independent Test**: Exercise isolated malformed policies and style fixtures plus the production browser matrix. Each known defect class fails with a specific message, while production routes pass.

### Tests and Integration for User Story 3

- [X] T020 [US3] Complete negative source fixtures for footer, pagination, and theme cursor defect classes in `site/tests/site.test.mjs`
- [X] T021 [US3] Validate first-page, interior-page, and last-page pagination shapes in `site/scripts/verify-site.mjs`
- [X] T022 [US3] Validate footer and theme keyboard behavior plus visible focus without weakening existing interaction checks in `site/scripts/verify-site.mjs`
- [X] T023 [US3] Run the complete Playwright route, responsive, theme, payload, interaction, and WCAG 2.1 AA matrix

**Checkpoint**: Every S022 regression class is enforced by an objective publication gate.

---

## Phase 6: Polish, Validation, and Delivery

**Purpose**: Reconcile documentation, run CI parity, publish the authorized PR, and close both permitted review rounds.

- [X] T024 Update the unreleased site correction and dated decision record in `CHANGELOG.md`
- [X] T025 Record focused and full validation outcomes in `specs/022-site-interaction-affordances/evidence.md`
- [X] T026 Run Python compile and all documented Python test suites from `.github/workflows/build.yml`
- [X] T027 Run `python scripts/build_all.py` and confirm all six production kits report zero problems and zero glyph failures
- [X] T028 Run `pnpm --dir site lint`, `pnpm --dir site build`, and `pnpm --dir site test`
- [X] T029 Audit UTF-8 without BOM, LF, mojibake, ignored generated output, and unchanged identity/generated source boundaries
- [X] T030 Re-run cross-artifact requirement/task coverage analysis and resolve every critical or high finding
- [X] T031 Mark every completed implementation and local-validation task in `specs/022-site-interaction-affordances/tasks.md`
- [X] T032 Commit S022 with Conventional Commit traceability on `codex/022-site-interaction-affordances`
- [X] T033 Push the authorized feature branch and open an official PR closing #163 and #164
- [X] T034 Reconcile every CI result and first-round Codex review response with code, tests, replies, and resolved threads
- [X] T035 Request at most one authorized second Codex review round and reconcile every response without requesting a third round
- [X] T036 Confirm the final PR head is green, every review thread is resolved, the branch is synchronized, and the PR is ready for owner merge review

## Dependencies and Execution Order

- Phase 1 precedes all implementation and freezes the shared behavior baseline.
- Phase 2 assertions precede production component and stylesheet changes.
- User Story 1 and User Story 2 are independently implementable after Phase 2 and touch different production files.
- User Story 3 consumes both story contracts and makes them durable publication gates.
- Final validation and delivery depend on all three stories.

## Parallel Opportunities

- T001 and T002 inspect separate interaction surfaces.
- T006 and T007 cover separate stylesheet contracts after T005 establishes the test pattern.
- User Story 1 production work in `site/components/footer.tsx` and User Story 2 production work in `site/app/globals.css` are independent after their tests exist.
- T024 and T025 update separate documentation artifacts after behavior is stable.

## Implementation Strategy

### MVP First

1. Freeze footer policy and shared dependency DOM.
2. Add failing source and rendered footer assertions.
3. Implement explicit destination records and safe metadata.
4. Validate issue #163 independently, then continue directly into issue #164 under autopilot.

### Incremental Delivery

1. User Story 1 preserves browsing context and closes the footer behavior defect.
2. User Story 2 restores documentation alignment and control affordances.
3. User Story 3 prevents both shared regressions from recurring.
4. Full repository validation proves no identity, kit, or unrelated site behavior changed.

## Notes

- The custom checklist remains reviewer-owned and its items stay unchecked unless the reviewer explicitly evaluates them.
- Test completion markers record implementation work, not owner approval.
- No subagent work is used for this slice.
