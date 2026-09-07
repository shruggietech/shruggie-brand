# Tasks: Glitchpad Pre-release Presentation Hardening

**Input**: Design documents from `specs/014-glitchpad-presentation-hardening/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, and quickstart.md

**Tests**: S014 requires test-first regression coverage and the complete production gate.

**Organization**: Tasks are grouped by user story and executed in dependency order.

## Phase 1: Setup and Baseline

**Purpose**: Establish traceability and preserve the pre-change identity baseline.

- [x] T001 Record #144 and #145 scope, current branch state, and protected Glitchpad path hashes in `specs/014-glitchpad-presentation-hardening/evidence.md`
- [x] T002 [P] Confirm generated-output, temporary-fixture, and browser-evidence paths remain excluded in `.gitignore`
- [x] T003 [P] Record current Glitchpad site and generated-asset presentation dispositions in `specs/014-glitchpad-presentation-hardening/evidence.md`

---

## Phase 2: Foundational Contracts

**Purpose**: Establish the governed surface reference and shared containment contracts used by all stories.

- [x] T004 Add failing showcase-role validation tests in `skill/templates/test_brand_contract.py`
- [x] T005 Add failing generated site-binding tests in `scripts/test_prepare_site.py`
- [x] T006 Implement the optional showcase-surface role resolver in `skill/templates/brand_contract.py` and schema documentation in `skill/references/canon.schema.json`
- [x] T007 Configure Glitchpad's `card` role in `brands/glitchpad/brand.json` and emit the resolved optional binding from `scripts/prepare_site.py`

**Checkpoint**: Invalid surface references fail closed, Glitchpad emits its governed card value, and unconfigured brands retain an absent override.

---

## Phase 3: User Story 1 - Balanced identity presentations (Priority: P1)

**Goal**: Keep portrait, landscape, and offset-canvas marks centered and contained in square presentations.

**Independent Test**: Measure the landing image box and visible ink at 360px, 1280px, and 200 percent zoom, and run isolated synthetic containment cases.

- [x] T008 [US1] Add failing portrait, landscape, asymmetric-canvas, invalid-input, and margin-symmetry tests in `skill/templates/test_iconkit.py`
- [x] T009 [US1] Promote reusable visible-bound square composition in `skill/templates/iconkit.py`
- [x] T010 [US1] Add a failing standalone square-master regression in `skill/templates/test_pipeline.py`
- [x] T011 [US1] Replace the height-only standalone raster path with declared-clear-space visible containment in `skill/templates/gen_logo.py`
- [x] T012 [US1] Add failing browser assertions for a square image content box, containment, and balanced production cards in `site/scripts/verify-site.mjs`
- [x] T013 [US1] Constrain the portfolio icon grid and image box in `site/app/globals.css`

**Checkpoint**: User Story 1 passes focused generator and browser checks without canonical geometry changes.

---

## Phase 4: User Story 2 - Governed neutral showcase surfaces (Priority: P1)

**Goal**: Present Glitchpad on its declared charcoal card surface without yellow wash or glow while preserving sibling brands.

**Independent Test**: Inspect generated metadata and computed landing-card and portfolio-hero styles for Glitchpad and every sibling in dark and light themes.

- [x] T014 [US2] Add failing browser assertions for governed Glitchpad surfaces, absent glow, and sibling fallback behavior in `site/scripts/verify-site.mjs`
- [x] T015 [US2] Bind optional showcase CSS properties in `site/app/(site)/page.tsx` and `site/app/(site)/[slug]/page.tsx`
- [x] T016 [US2] Apply the optional neutral landing-card and hero treatment with sibling fallbacks in `site/app/globals.css`

**Checkpoint**: User Story 2 passes site preparation, static type, browser, theme, focus, and accessibility checks independently.

---

## Phase 5: User Story 3 - Release-bound export confidence (Priority: P2)

**Goal**: Classify every declared Glitchpad square export and preserve platform-specific composition rules.

**Independent Test**: Rebuild Glitchpad and inspect master, web, Android, Apple, macOS, and Windows manifest paths, dimensions, visible bounds, occupancy, transparency, and backgrounds.

- [x] T017 [US3] Extend generated icon tests to assert existing role-specific occupancy and plate behavior in `skill/templates/test_iconkit.py`
- [x] T018 [US3] Rebuild and record every Glitchpad square-export disposition in `specs/014-glitchpad-presentation-hardening/evidence.md`
- [x] T019 [US3] Record protected-path comparison and desktop and Android handoff guidance in `specs/014-glitchpad-presentation-hardening/evidence.md`

**Checkpoint**: Every required export is corrected, verified unchanged, or explicitly skipped with no speculative platform rewrite.

---

## Phase 6: Polish, Verification, and Review

**Purpose**: Complete repository gates, documentation, publication, CI, and authorized review rounds.

- [x] T020 Update the Unreleased change and architecture-decision records in `CHANGELOG.md`
- [x] T021 Run focused Python and site checks from `specs/014-glitchpad-presentation-hardening/quickstart.md`
- [x] T022 Run the complete five-kit, glyph, release, site, browser, accessibility, Markdown, encoding, and repository-hygiene gate from `specs/014-glitchpad-presentation-hardening/quickstart.md`
- [x] T023 Complete final outcomes and command evidence in `specs/014-glitchpad-presentation-hardening/evidence.md`
- [x] T024 Commit and push `codex/014-glitchpad-presentation-hardening`, then open a pull request with `Fixes #144` and `Fixes #145`
- [x] T025 Process every CI result and first-round review disposition, applying and verifying warranted corrections
- [x] T026 Trigger at most one authorized `@Codex` second review round and process every resulting disposition
- [ ] T027 Confirm all required checks are green and all review threads are resolved, update S014 evidence and task state, push the final documentation commit, and halt before merge

---

## Dependencies and Execution Order

- Phase 1 establishes the immutable baseline.
- Phase 2 blocks both visual user stories because generated surface data must be authoritative before site styling changes.
- User Story 1 and User Story 2 are independently testable after Phase 2, but shared CSS changes execute sequentially.
- User Story 3 depends on User Story 1's composition contract.
- Phase 6 depends on all user stories.
- Tests in each phase are written and observed failing before their corresponding implementation.

## Parallel Opportunities

- T002 and T003 inspect separate concerns after T001.
- T004 and T005 target separate test modules before T006 and T007.
- Generator-focused T008 through T011 and initial site test design in T012 can be prepared independently, then integrated sequentially.
- Documentation evidence can be updated while foreground validation commands are between suites, but test processes themselves remain foreground and are watched to completion.

## Implementation Strategy

1. Preserve and record the baseline.
2. Implement the generated showcase-surface contract.
3. Complete visible-bound square containment under TDD.
4. Apply the site layout and governed neutral presentation.
5. Rebuild and classify release-bound exports.
6. Pass the full gate, publish the pull request, complete no more than two review rounds, and stop before merge.

## Notes

- All task lines use the required checkbox, task ID, optional parallel marker, story label where applicable, action, and file path format.
- The custom checklist remains reviewer-owned. Its unchecked state does not describe implementation incompleteness.
