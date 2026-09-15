# Tasks: Portfolio Card Consistency

**Input**: Design documents from `specs/033-portfolio-card-consistency/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/portfolio-presentation-contract.md`, `quickstart.md`

**Tests**: Required by the feature specification and autopilot TDD discipline. Add each regression before its implementation and record the expected initial failure.

**Organization**: Tasks are grouped by user story so visual consistency, accessible actions, and concise disclosure remain independently traceable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches a different file and has no incomplete dependency.
- **[Story]**: Maps a task to the user story in `spec.md`.
- Every task includes an exact repository path.

## Phase 1: Setup

**Purpose**: Establish the current production baseline and feature traceability.

- [x] T001 Confirm branch, clean worktree, active feature directory, and issue states #199/#200; record the baseline in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T002 [P] Capture existing portfolio component, style, generated-registry, source-test, and browser-test contracts in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T003 [P] Validate specification and plan prose, links, checklist format, and absence of unresolved markers with `scripts/check_markdown.py` and record results in `specs/033-portfolio-card-consistency/evidence.md`

---

## Phase 2: Foundational Test Harness

**Purpose**: Establish shared helpers and baseline checks needed by every story.

**Critical**: No user-story implementation begins until baseline site generation and existing tests are confirmed.

- [x] T004 Run the existing source contract test and capture current behavior for surfaces, actions, and notice aggregation in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T005 Run site preparation/build prerequisites needed by the browser verifier and capture the current generated homepage baseline in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T006 Define reusable computed-color, contrast, geometry, visibility, focusability, and content-clearance measurements in `site/scripts/verify-site.mjs`

**Checkpoint**: The baseline is recorded and the browser verifier can measure every new contract without changing production behavior.

---

## Phase 3: User Story 1 - Scan a coherent portfolio (Priority: P1) MVP

**Goal**: Present all cards and mobile disclosures as one dark portfolio family with exact white visible copy while preserving approved assets and governed dark surfaces.

**Independent Test**: At desktop and mobile widths, all visible titles, descriptions, and actions compute to white; light showcase overrides are absent; approved dark surfaces and icon sources remain intact.

### Tests for User Story 1

- [x] T007 [P] [US1] Add failing source assertions for dark-surface eligibility, absence of light foreground injection, explicit white portfolio copy, and preserved icon policy in `site/tests/site.test.mjs`
- [x] T008 [P] [US1] Add failing rendered checks for every desktop/mobile visible text color, governed-dark eligibility, I Heart PR Tours dark fallback, and unchanged icon source in `site/scripts/verify-site.mjs`

### Implementation for User Story 1

- [x] T009 [US1] Implement generated-foreground-based dark surface eligibility and remove light showcase leakage in `site/components/brand-portfolio.tsx`
- [x] T010 [US1] Apply scoped dark card/accordion surfaces and exact white title, description, panel, and action text in `site/app/globals.css`
- [x] T011 [US1] Run focused source and rendered checks for the coherent portfolio and record pass evidence in `specs/033-portfolio-card-consistency/evidence.md`

**Checkpoint**: User Story 1 independently delivers a coherent dark portfolio with white visible copy and unchanged brand assets.

---

## Phase 4: User Story 2 - Operate accessible card actions (Priority: P1)

**Goal**: Make action reveal, focus, dismissal, sizing, spacing, and reduced-motion behavior fully operable without hidden focus targets or layout shift.

**Independent Test**: Pointer and keyboard users can reveal both actions for every card; at rest no action is visible or focusable; all states meet contrast, focus, target-size, bottom-clearance, geometry, zoom, and reduced-motion requirements.

### Tests for User Story 2

- [x] T012 [P] [US2] Add failing source assertions for a labeled keyboard card entry, visibility-based hidden actions, exact white labels, dual focus treatment, fixed stage clearance, and reduced-motion overrides in `site/tests/site.test.mjs`
- [x] T013 [P] [US2] Add failing browser checks for resting visibility/focusability, card-first keyboard reveal, action destinations, 4.5:1 text contrast, 3:1 focus-indicator contrast, 44-pixel targets, Escape dismissal, 16-pixel bottom clearance, 0.5-pixel geometry tolerance, narrow width, 200 percent zoom, and reduced motion in `site/scripts/verify-site.mjs`

### Implementation for User Story 2

- [x] T014 [US2] Make each desktop card a labeled keyboard reveal entry while preserving pointer, focus-exit, pointer-exit, and Escape state transitions in `site/components/brand-portfolio.tsx`
- [x] T015 [US2] Reserve sufficient desktop stage height and bottom inset for long descriptions and two 44-pixel actions in `site/app/globals.css`
- [x] T016 [US2] Implement hidden/revealed visibility semantics, stable dark action fills, white labels, hover/active cues, dual focus indicator, and reduced-motion overrides in `site/app/globals.css`
- [x] T017 [US2] Verify desktop, narrow, mobile, zoom, keyboard-only, pointer, and reduced-motion action flows and record measurements in `specs/033-portfolio-card-consistency/evidence.md`

**Checkpoint**: User Story 2 independently provides accessible and geometrically stable portfolio actions.

---

## Phase 5: User Story 3 - Read one concise third-party notice (Priority: P2)

**Goal**: Replace the accumulating legal-copy list with one exact generic notice while retaining correct applicability, accessible associations, and detailed metadata elsewhere.

**Independent Test**: Positive applicability yields exactly one paragraph with exact copy; zero applicability yields no notice; additional applicable entries do not change copy/count; markers and detailed route metadata remain correct.

### Tests for User Story 3

- [x] T018 [P] [US3] Add failing source assertions for boolean applicability, one fixed paragraph, exact copy, zero-state conditional rendering, and absence of vendor-boundary mapping in `site/tests/site.test.mjs`
- [x] T019 [P] [US3] Add failing browser checks for exact notice count/text, one paragraph, marker applicability and association, absent detailed homepage wording, and unchanged guideline metadata in `site/scripts/verify-site.mjs`

### Implementation for User Story 3

- [x] T020 [US3] Replace distinct vendor-boundary aggregation with boolean applicability and one exact generic paragraph in `site/components/brand-portfolio.tsx`
- [x] T021 [US3] Remove obsolete multi-paragraph spacing behavior while preserving concise notice layout in `site/app/globals.css`
- [x] T022 [US3] Run focused notice and metadata checks and record zero/positive/multiple applicability evidence in `specs/033-portfolio-card-consistency/evidence.md`

**Checkpoint**: All three user stories are independently traceable and the combined homepage contract is complete.

---

## Phase 6: Polish and Cross-Cutting Verification

**Purpose**: Reconcile artifacts, run every authoritative gate, and prepare the local commit.

- [x] T023 [P] Update the unreleased correction entry for S033 and issues #199/#200 in `CHANGELOG.md`
- [x] T024 Re-run cross-artifact analysis and reconcile `specs/033-portfolio-card-consistency/spec.md`, `plan.md`, `tasks.md`, contract, data model, quickstart, and implementation
- [x] T025 Run all Python 3.8-compatible suites, Python publication/generator suites, Markdown audit, capability probe, all-kit build, release certification, and generated-agent diff; record exact results in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T026 Run `pnpm --dir site lint`, `pnpm --dir site build`, and `pnpm --dir site test`; record page, route, contract, and WCAG results in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T027 Run publication audit, repository hygiene checks, generated-artifact exclusion, diff checks, mojibake scan, and task completion review; record results in `specs/033-portfolio-card-consistency/evidence.md`
- [x] T028 Commit source, tests, changelog, evidence, and Spec Kit artifacts locally with an S033 Conventional Commit subject, then halt before `git push`

---

## Phase 7: Post-review light-theme correction

**Purpose**: Correct the review-discovered fallback regression without changing the approved white-copy or dark-family contract.

- [x] T029 [US1] Add source and rendered regressions proving desktop cards and mobile disclosures retain the same dark surfaces and white foregrounds in both site themes in `site/tests/site.test.mjs` and `site/scripts/verify-site.mjs`
- [x] T030 [US1] Pin the accent-derived desktop and mobile fallback gradients to a theme-invariant dark base in `site/app/globals.css`
- [x] T031 Rebuild the static site, run the focused site validation, record evidence in `specs/033-portfolio-card-consistency/evidence.md`, and present the corrected light-theme preview before changing the local commit

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup**: Starts immediately.
- **Foundational Test Harness**: Depends on Setup and blocks story implementation.
- **User Story 1**: Depends on the shared measurement harness.
- **User Story 2**: Depends on the shared measurement harness and integrates with the card surface/text contract from User Story 1.
- **User Story 3**: Depends only on Setup and the browser harness, but follows the P1 stories for single-agent execution.
- **Polish**: Depends on all selected stories.

### User Story Dependencies

- **US1**: Independently testable dark-surface and white-copy increment.
- **US2**: Independently testable action-state increment; consumes the stable dark/white visual contract established by US1.
- **US3**: Independently testable notice increment; does not depend on US1 or US2 behavior.

### Within Each User Story

- Add source and browser regressions first and observe the expected failure.
- Implement the smallest component and style changes that satisfy those regressions.
- Run the story's independent checks before advancing.
- Preserve explicit generated destinations, detailed metadata, and approved identity assets throughout.

### Parallel Opportunities

- T002 and T003 can run in parallel.
- T007 and T008 can run in parallel before US1 implementation.
- T012 and T013 can run in parallel before US2 implementation.
- T018 and T019 can run in parallel before US3 implementation.
- T023 can run in parallel with final artifact reconciliation after behavior is stable.

---

## Parallel Example: User Story 1

```text
Task: "Add failing surface and text source assertions in site/tests/site.test.mjs"
Task: "Add failing computed-style browser assertions in site/scripts/verify-site.mjs"
```

## Parallel Example: User Story 2

```text
Task: "Add failing action source assertions in site/tests/site.test.mjs"
Task: "Add failing action interaction and geometry checks in site/scripts/verify-site.mjs"
```

## Parallel Example: User Story 3

```text
Task: "Add failing generic-notice source assertions in site/tests/site.test.mjs"
Task: "Add failing rendered notice and metadata checks in site/scripts/verify-site.mjs"
```

---

## Implementation Strategy

### MVP First

1. Complete Setup and the shared browser measurement harness.
2. Add failing US1 regressions.
3. Implement the dark portfolio family and exact white copy.
4. Validate US1 independently before changing action or notice behavior.

### Incremental Delivery

1. US1 normalizes the visible portfolio.
2. US2 repairs action accessibility and spacing without changing destinations.
3. US3 replaces only the shared notice content strategy.
4. Full verification proves the combined slice without generated or identity changes.

## Notes

- `[P]` tasks touch different files and may proceed concurrently when dependencies are satisfied.
- Custom checklist markers remain reviewer-owned and do not track task completion.
- The static homepage has no authentication, private data, storage, user input, or tenant boundary; destination integrity and hidden-interaction safety are the applicable security checks.
- Never commit generated `dist/`, `site/out/`, PDFs, raster exports, registries, or release archives.
