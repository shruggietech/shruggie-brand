# Tasks: Complete Kit Downloads and Explicit Brand Actions

**Input**: Design documents from `/specs/024-kit-download-actions/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: S024 explicitly requires automated archive, source-contract, rendered-interaction, accessibility, and repository validation. Test tasks precede their implementations.

**Organization**: Tasks are grouped by user story so each outcome can be implemented and verified independently after the shared archive foundation exists.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Lock the slice records and production inventory boundary.

- [x] T001 Confirm the six homepage brands and S024 issue traceability in specs/024-kit-download-actions/spec.md
- [x] T002 [P] Add reviewer-owned archive and interaction requirements criteria in specs/024-kit-download-actions/checklists/archive-ux.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish one authoritative, reusable archive pipeline before any download action is exposed.

- [x] T003 Add failing six-brand production inventory and atomic archive-writer tests in scripts/test_package_release.py and scripts/test_release_contract.py
- [x] T004 Export the single six-brand production inventory from scripts/release_contract.py and consume it from scripts/package_release.py
- [x] T005 Implement deterministic staged archive assembly, verification, cleanup, and atomic replacement in scripts/package_release.py
- [x] T006 Run the focused release archive tests in scripts/test_package_release.py and scripts/test_release_contract.py

**Checkpoint**: A complete archive can be produced and certified for every public production brand without publishing partial output.

---

## Phase 3: User Story 1 - Download a complete, trustworthy brand kit (Priority: P1) MVP

**Goal**: Publish the verified, version-aware archive for each homepage brand from the same kit revision as its site content.

**Independent Test**: Prepare all six site brands, download each generated archive, and verify identity, version, normalized inventory, checksums, licenses, filename, deterministic bytes, and response signature.

- [x] T007 [US1] Add failing site archive publication and portfolio-record tests in scripts/test_prepare_site.py and site/tests/site.test.mjs
- [x] T008 [US1] Materialize each verified archive and publish its generated path and filename in scripts/prepare_site.py
- [x] T009 [US1] Add archive MIME and ZIP-response verification support in site/scripts/verify-site.mjs
- [x] T010 [US1] Run focused site preparation and archive mapping tests in scripts/test_prepare_site.py and site/tests/site.test.mjs

**Checkpoint**: Every public brand has exactly one complete archive and one generated download destination.

---

## Phase 4: User Story 2 - Choose an explicit brand action on desktop (Priority: P1)

**Goal**: Replace ambiguous full-card links with stable cards that reveal exactly two deliberate actions.

**Independent Test**: Use pointer and keyboard on every desktop card and confirm exact destinations, fixed outer geometry, persistent action availability, visible focus, and reduced-motion behavior.

- [x] T011 [US2] Add failing desktop markup and action contract assertions in site/tests/site.test.mjs and site/scripts/verify-site.mjs
- [x] T012 [US2] Create the shared portfolio renderer with non-interactive desktop articles and exact action anchors in site/components/brand-portfolio.tsx
- [x] T013 [US2] Replace homepage full-card links with the shared renderer in site/app/(site)/page.tsx
- [x] T014 [US2] Implement fixed-height desktop content swaps, focus visibility, pointer continuity, and reduced-motion rules in site/app/globals.css
- [x] T015 [US2] Run desktop source and rendered interaction checks in site/tests/site.test.mjs and site/scripts/verify-site.mjs

**Checkpoint**: Desktop cards expose only Guidelines and Download Kit without layout shift or implicit navigation.

---

## Phase 5: User Story 3 - Browse compact brand actions on mobile (Priority: P1)

**Goal**: Present the same portfolio as compact native disclosures on narrow viewports.

**Independent Test**: Expand and collapse every mobile row with pointer and keyboard, then verify summary contents, panel order, hidden-focus behavior, target size, breakpoint switching, and 200% zoom.

- [x] T016 [US3] Add failing mobile disclosure, focus, breakpoint, and zoom assertions in site/tests/site.test.mjs and site/scripts/verify-site.mjs
- [x] T017 [US3] Render native mobile details and summary disclosures from the shared record in site/components/brand-portfolio.tsx
- [x] T018 [US3] Implement compact mobile layout, disclosure indicator, focus state, touch target, and overflow protection in site/app/globals.css
- [x] T019 [US3] Run mobile source and rendered disclosure checks in site/tests/site.test.mjs and site/scripts/verify-site.mjs

**Checkpoint**: Mobile rows remain compact when closed and expose complete, accessible actions when open.

---

## Phase 6: User Story 4 - Understand third-party attribution once (Priority: P1)

**Goal**: Preserve full generated attribution while removing repeated card-level disclaimer paragraphs.

**Independent Test**: Compare generated vendor-boundary records with both responsive presentations and confirm eligible markers, accessible associations, one post-portfolio notice, unique full wording, and no card-level repetition.

- [x] T020 [US4] Add failing marker eligibility and exactly-one disclaimer assertions in site/tests/site.test.mjs and site/scripts/verify-site.mjs
- [x] T021 [US4] Render generated markers and one unique portfolio-level notice region in site/components/brand-portfolio.tsx
- [x] T022 [US4] Style marker and shared notice presentation for both themes and responsive layouts in site/app/globals.css
- [x] T023 [US4] Remove obsolete repeated vendor-summary output from scripts/prepare_site.py and run attribution checks

**Checkpoint**: Attribution remains complete and accessible while appearing only once after the portfolio.

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Synchronize records, certify all production artifacts, and prepare review evidence.

- [x] T024 [P] Update S024 implementation and verification notes in CHANGELOG.md and skill/CHANGELOG.md where applicable
- [x] T025 Run all focused Python, Node source-contract, TypeScript, static-export, Playwright, and axe checks documented in specs/024-kit-download-actions/quickstart.md
- [x] T026 Run full production build, verify.py, validate_glyph.py, release archive certification, and repository hygiene gates
- [x] T027 Record commands and zero-problem outcomes in specs/024-kit-download-actions/evidence.md and mark completed tasks in specs/024-kit-download-actions/tasks.md
- [x] T028 Validate UTF-8 without BOM, LF endings, mojibake absence, ignored generated output, git diff hygiene, and final spec/plan/task synchronization

---

## Dependencies and Execution Order

- Setup has no dependencies.
- Foundational archive work depends on Setup and blocks all user stories.
- US1 depends on the archive foundation and supplies the destinations consumed by US2 and US3.
- US2 and US3 can proceed independently after US1 publishes the shared record.
- US4 shares the portfolio renderer with US2 and US3 and follows their structural implementation.
- Polish depends on all four user stories.

## Parallel Opportunities

- T001 and T002 touch separate planning records.
- After T010, desktop source assertions and mobile source assertions can be drafted independently, although shared component edits remain sequential.
- T024 can proceed independently from final execution of the validation suites.

## Parallel Example: Responsive Portfolio

```text
Task: Add desktop rendered behavior assertions in site/scripts/verify-site.mjs
Task: Add mobile disclosure source assertions in site/tests/site.test.mjs
```

## Implementation Strategy

1. Complete the deterministic archive foundation.
2. Deliver US1 as the minimum useful increment, proving complete downloads before advertising them.
3. Add desktop and mobile presentations from the same generated record.
4. Consolidate attribution once the shared renderer exists.
5. Run the full gate, synchronize evidence, then publish for CI and review.

## Format Validation

All 28 tasks use the required checkbox, sequential task ID, optional parallel marker, required user-story label in story phases, and explicit file paths.
