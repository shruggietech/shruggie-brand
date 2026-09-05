# Tasks: Branded Documentation and Discovery Completion

**Input**: Design documents from `specs/009-branded-docs-discovery/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: S009 requires test-driven source, emitted-site, browser, accessibility, and corruption coverage.

**Organization**: Tasks are chronological and grouped by independently testable user story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes different files without an incomplete dependency.
- **[Story]**: Maps the task to a user story in `spec.md`.

## Phase 1: Setup and Spec Kit Gates

**Purpose**: Establish the governed S009 record and confirm the source baseline.

- [x] T001 Confirm clean current-main baseline, create `codex/009-docs-discovery-completion`, bind `.specify/feature.json` to `specs/009-branded-docs-discovery/`, and ensure `.gitignore` covers the planned generated social and screenshot paths
- [x] T002 Create and validate `specs/009-branded-docs-discovery/spec.md` and `specs/009-branded-docs-discovery/checklists/requirements.md` against issues #108, #109, and #111
- [x] T003 [P] Record primary-source decisions in `specs/009-branded-docs-discovery/research.md`
- [x] T004 [P] Define `specs/009-branded-docs-discovery/data-model.md`, `specs/009-branded-docs-discovery/contracts/documentation-rendering.md`, `specs/009-branded-docs-discovery/contracts/documentation-theme.md`, and `specs/009-branded-docs-discovery/contracts/route-metadata.md`
- [x] T005 Complete `specs/009-branded-docs-discovery/plan.md`, `specs/009-branded-docs-discovery/quickstart.md`, and this chronological `specs/009-branded-docs-discovery/tasks.md`
- [x] T006 Run the read-only Spec Kit cross-artifact analysis and resolve every CRITICAL or HIGH finding in `specs/009-branded-docs-discovery/`

**Checkpoint**: The specification, research, design, contracts, and task coverage are complete and constitution-aligned.

---

## Phase 2: Foundational Route and Content Tests

**Purpose**: Write failing source tests for shared content and discovery contracts before implementation.

- [x] T007 [P] Add failing alert transformation, ordinary-blockquote, fenced-literal, and multiline-notice tests in `scripts/test_prepare_site.py`
- [x] T008 [P] Add failing canonical route, duplicate rejection, breadcrumb, social descriptor, and safe guideline metadata tests in `scripts/test_prepare_site.py`
- [x] T009 [P] Extend expected route, metadata, screenshot, and social-asset inventories in `site/tests/site.test.mjs`
- [x] T010 Run the focused tests and record the expected pre-implementation failures in `specs/009-branded-docs-discovery/evidence.md`

**Checkpoint**: Each shared S009 contract has a demonstrated failing regression test.

---

## Phase 3: User Story 1 - Read Technical Documentation Without Friction (Priority: P1) 🎯 MVP

**Goal**: Restore cohesive code panels, accessible copy behavior, semantic notices, and unique documentation navigation.

**Independent Test**: The docs index and toolchain page render correct code, notices, navigation, keyboard behavior, and mobile containment without requiring the theme or metadata stories.

### Tests for User Story 1

- [x] T011 [US1] Add failing emitted-DOM and keyboard assertions for code figures, copy behavior, syntax distinction, inline code, notices, unique navigation, and overflow in `site/scripts/verify-site.mjs`

### Implementation for User Story 1

- [x] T012 [US1] Implement explicit NOTE, WARNING, and CAUTION blockquote conversion while preserving ordinary prose and fences in `scripts/prepare_site.py`
- [x] T013 [US1] Author representative portable notices in `skill/references/04-toolchain.md`
- [x] T014 [P] [US1] Restore default fenced-code and callout bindings while preserving table behavior in `site/mdx-components.tsx`
- [x] T015 [P] [US1] Remove the duplicate documentation-root link through a documented layout option in `site/lib/layout.shared.tsx` and `site/app/docs/layout.tsx`
- [x] T016 [US1] Run the focused Python and browser tests for documentation rendering and record results in `specs/009-branded-docs-discovery/evidence.md`

**Checkpoint**: #108 behavior is complete and independently verified.

---

## Phase 4: User Story 2 - Recognize ShruggieTech Documentation (Priority: P1)

**Goal**: Apply compact typography, canonical semantic tokens, accessible orientation states, and a recognizable theme-aware ShruggieTech sidebar identity.

**Independent Test**: The docs index and toolchain page pass computed style, geometry, light and dark theme, focus, responsive, screenshot, and WCAG checks.

### Tests for User Story 2

- [x] T017 [US2] Add failing heading-size, first-viewport, canonical-token, active-state, focus, theme, logo, and screenshot assertions in `site/scripts/verify-site.mjs`

### Implementation for User Story 2

- [x] T018 [P] [US2] Publish theme-appropriate generated ShruggieTech lockups in `scripts/prepare_site.py` and cover them in `scripts/test_prepare_site.py`
- [x] T019 [P] [US2] Add the owned documentation page hook in `site/app/docs/[[...slug]]/page.tsx` and render the theme-aware sidebar identity from `site/lib/layout.shared.tsx`
- [x] T020 [US2] Scope marketing typography, map Fumadocs semantic variables to canonical roles, and style code, notice, navigation, focus, footer, responsive, and reduced-motion states in `site/app/globals.css`
- [x] T021 [US2] Run desktop and mobile light and dark documentation verification, inspect the ignored screenshots, and record results in `specs/009-branded-docs-discovery/evidence.md`

**Checkpoint**: #109 behavior is complete and independently verified with zero WCAG 2.1 AA violations.

---

## Phase 5: User Story 3 - Share and Discover the Correct Page (Priority: P1)

**Goal**: Make every route use exact page-aware metadata, structured data, social previews, breadcrumbs, and sitemap URLs from one descriptor graph.

**Independent Test**: Every route record, emitted page, copied guideline, social PNG, and sitemap entry agrees exactly and resolves directly.

### Tests for User Story 3

- [x] T022 [US3] Add failing exact metadata, JSON-LD graph, breadcrumb, social asset, sitemap-set, and direct-resolution assertions in `site/scripts/verify-site.mjs`

### Implementation for User Story 3

- [x] T023 [US3] Generate validated route descriptors and deterministic local social previews, then drive copied guideline metadata from the same records in `scripts/prepare_site.py`
- [x] T024 [P] [US3] Add exact route loading, metadata conversion, and safe structured-data graph helpers in `site/lib/routes.ts`, `site/lib/metadata.ts`, and `site/components/structured-data.tsx`
- [x] T025 [US3] Convert homepage, brand, downloads, and documentation pages to descriptor-driven metadata and structured data in `site/app/(site)/page.tsx`, `site/app/(site)/[slug]/page.tsx`, `site/app/(site)/[slug]/downloads/page.tsx`, and `site/app/docs/[[...slug]]/page.tsx`
- [x] T026 [US3] Generate `site/app/sitemap.ts` and `site/tests/site.test.mjs` inventories exclusively from the shared route descriptor graph
- [x] T027 [US3] Run route generation, TypeScript, static export, metadata, JSON-LD, social image, and sitemap verification and record results in `specs/009-branded-docs-discovery/evidence.md`

**Checkpoint**: #111 behavior is complete and independently verified for every public route.

---

## Phase 6: User Story 4 - Reject Documentation and Discovery Regressions (Priority: P2)

**Goal**: Make invalid rendering, theme, accessibility, metadata, graph, image, and URL relationships block publication deterministically.

**Independent Test**: Focused corruption fixtures and the complete emitted site reject every representative invalid state, while valid output passes.

- [x] T028 [US4] Complete Python corruption coverage for unsupported alerts, unsafe routes, duplicate descriptors, malformed preview inputs, and unsafe guideline content in `scripts/test_prepare_site.py`
- [x] T029 [US4] Make the static verifier enforce strict slash behavior, exact route relations, safe graph semantics, preview decoding, keyboard operation, computed geometry, both themes, screenshot capture, overflow, and axe auditing in `site/scripts/verify-site.mjs`
- [x] T030 [US4] Run focused regression suites and confirm every positive and corruption scenario in `specs/009-branded-docs-discovery/evidence.md`

**Checkpoint**: All S009 regression contracts fail closed and all valid scenarios pass.

---

## Phase 7: Polish, Aggregate Verification, and Publication

**Purpose**: Complete documentation, repository-wide gates, pull-request publication, and bounded reviews.

- [x] T031 [P] Add S009 Added, Changed, and Fixed entries to `CHANGELOG.md` and the dated route-graph and ignored-screenshot decision to `docs/decisions.md`
- [x] T032 Run the complete chronological CI-parity command sequence from `specs/009-branded-docs-discovery/quickstart.md` and record exact counts and outcomes in `specs/009-branded-docs-discovery/evidence.md`
- [x] T033 Verify no generated kits, routes, social PNGs, screenshots, static exports, archives, or machine-local Spec Kit state are tracked; then run UTF-8 without BOM, LF, mojibake, sensitive-data, Markdown, and `git diff --check` hygiene gates
- [x] T034 Re-run Spec Kit cross-artifact analysis, mark all completed tasks in `specs/009-branded-docs-discovery/tasks.md`, and ensure specification, plan, contracts, evidence, and implementation remain synchronized
- [ ] T035 Commit S009 with a Conventional Commit subject, push `codex/009-docs-discovery-completion`, and publish a pull request that closes only #108, #109, and #111
- [ ] T036 Process every automatic Codex review signal and thread, file warranted out-of-scope findings as issues, implement and verify in-scope corrections, reply substantively, and resolve completed threads
- [ ] T037 Request exactly one explicit `@Codex review` second round if round one completed, then process every second-round signal and thread without requesting a third round
- [ ] T038 Verify every latest-head hosted CI check is green, the review-request ceiling is recorded, every review thread is resolved, and the pull request remains open for the owner merge ritual

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 has no dependencies and establishes the blocking Spec Kit gate.
- Phase 2 depends on Phase 1 and writes shared failing tests before implementation.
- User Story 1 depends on Phase 2 and restores the documentation component contract.
- User Story 2 depends on User Story 1 because theme rules target the restored components and owned docs hook.
- User Story 3 depends on Phase 2 but follows User Story 2 to keep route-page edits sequential.
- User Story 4 depends on all three P1 stories and closes their negative-path coverage.
- Phase 7 depends on every implementation and focused verification task.

### Parallel Opportunities

- T003 and T004 can run in parallel after specification validation.
- T007, T008, and T009 describe separate test seams but edits to `scripts/test_prepare_site.py` must be serialized in one working tree.
- T014 and T015 affect separate site modules after T012 and T013 establish generated content.
- T018 and T019 affect separate preparation and layout files before shared CSS integration.
- T024 can begin after route descriptor shape is established, but must integrate with T023 before page conversion.
- T031 can run independently after implementation decisions stabilize.

## Implementation Strategy

1. Complete Spec Kit artifacts and analysis before source changes.
2. Demonstrate focused failures for content derivation and route discovery.
3. Deliver #108 as the first independently testable increment.
4. Deliver #109 on the restored documentation components.
5. Deliver #111 through the shared descriptor graph.
6. Harden all negative paths, run aggregate gates, and publish once.
7. Process no more than two Codex review rounds, then halt for owner merge.

## Notes

- Test tasks must fail for the intended missing behavior before their implementation task begins.
- Generated images and screenshots are evidence artifacts, not committed baselines.
- GitHub issue closure occurs only after owner merge supplies current-main evidence.
- The automatic PR review is round one. Only one explicit second request is authorized.
