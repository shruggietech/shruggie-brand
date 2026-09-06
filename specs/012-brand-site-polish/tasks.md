# Tasks: Phase 13 Brand Site Polish

**Input**: Design documents from `specs/012-brand-site-polish/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Regression-first source, generator, browser, visual, reduced-motion, and WCAG coverage are mandatory.

## Phase 1: Setup and Traceability

- [X] T001 Create and categorize S012 tracking issue #133 with links to #120 through #126 in `specs/012-brand-site-polish/evidence.md`
- [X] T002 Create the complete S012 specification, plan, research, data model, contracts, quickstart, checklist, evidence, and task ledger under `specs/012-brand-site-polish/`
- [X] T003 Analyze the S012 artifact set against the constitution and resolve every critical, high, and material medium inconsistency in `specs/012-brand-site-polish/`

## Phase 2: User Story 1 - Official ShruggieTech Identity (Priority: P1)

**Goal**: Deliver the approved black-background favicon suite and colored lockups everywhere the public site identifies ShruggieTech.

**Independent Test**: Rebuild the ShruggieTech kit and site, then prove exact black icon backgrounds and theme-specific colored lockups on the landing and documentation surfaces without geometry changes.

- [X] T004 [P] [US1] Add regression-first canonical icon-background and colored-lockup materialization assertions in `scripts/test_prepare_site.py` and `skill/templates/test_brand_contract.py`
- [X] T005 [P] [US1] Add failing emitted favicon pixel, ICO-frame, route inheritance, and visible lockup assertions in `site/scripts/verify-site.mjs`
- [X] T006 [US1] Change only the canonical ShruggieTech application-icon background in `brands/shruggietech/brand.json`
- [X] T007 [US1] Select the existing generated colored dark and light lockup variants in `scripts/prepare_site.py`
- [X] T008 [US1] Complete fail-closed black-background image inspection for PNG, SVG, ICO, Apple touch, and manifest icons in `site/scripts/verify-site.mjs`
- [X] T009 [US1] Run focused identity source and generation tests and record preserved geometry evidence in `specs/012-brand-site-polish/evidence.md`

## Phase 3: User Story 2 - Responsive Canonical Navigation (Priority: P1)

**Goal**: Deliver the exact desktop and mobile landing inventories plus canonical Documentation and Variance Contract naming across every source and generated public surface.

**Independent Test**: Inspect 1280px and 360px landing navigation and scan source plus emitted pages, metadata, breadcrumbs, search, and pagination for exact canonical labels and preserved route paths.

- [X] T010 [P] [US2] Add regression-first route, generated metadata, and banned-terminology assertions in `scripts/test_prepare_site.py`
- [X] T011 [P] [US2] Add failing desktop and mobile navigation inventory, destination, absence, interaction, and terminology assertions in `site/scripts/verify-site.mjs`
- [X] T012 [US2] Canonicalize the documentation root label and generated metadata in `scripts/prepare_site.py`
- [X] T013 [US2] Canonicalize the authoritative first-document title without changing its filename or route in `skill/references/00-variance-contract.md`
- [X] T014 [US2] Implement exact viewport-filtered landing links and preserve documentation-shell behavior in `site/lib/layout.shared.tsx`
- [X] T015 [US2] Replace remaining public legacy labels while preserving destinations in `site/components/footer.tsx` and `site/app/(site)/page.tsx`
- [X] T016 [US2] Run focused materialization and responsive navigation checks and record route stability evidence in `specs/012-brand-site-polish/evidence.md`

## Phase 4: User Story 3 - Branded Action and Link Hierarchy (Priority: P1)

**Goal**: Deliver canonical orange primary actions, green documentation accents, scoped animated underlines, and unmistakable documentation pagination cards.

**Independent Test**: Measure representative CTA, secondary, inline-link, list-marker, code-string, and pagination-card states in both themes, both widths, normal motion, and reduced motion.

- [X] T017 [P] [US3] Add failing computed-style, component-exclusion, reduced-motion, pagination-resting, focus, and touch-target assertions in `site/scripts/verify-site.mjs`
- [X] T018 [US3] Add an explicit stable documentation pagination hook in `site/app/docs/[[...slug]]/page.tsx`
- [X] T019 [US3] Implement canonical CTA, green documentation accent, eligible orange underline, reduced-motion, and pagination-card states in `site/app/globals.css`
- [X] T020 [US3] Expand the visual route matrix to 12 route-width-theme cells in `site/tests/site.test.mjs`
- [X] T021 [US3] Run focused browser verification, inspect all 12 screenshots, and record visual and WCAG evidence in `specs/012-brand-site-polish/evidence.md`

## Phase 5: Polish, CI Parity, and Review

- [X] T022 Update the Unreleased changelog with the S012 feature and dated source-driven presentation decision in `CHANGELOG.md`
- [X] T023 Run the complete Python 3.8-compatible test set, full production build where capabilities permit, site lint, static export, browser verifier, Markdown, encoding, sensitive-data, artifact-boundary, whitespace, and git-status gates and record results in `specs/012-brand-site-polish/evidence.md`
- [X] T024 Commit, push, and open the official S012 pull request with closure links for #120 through #126 and #133
- [X] T025 Process automatic Codex round one, file every negative finding as an issue, respond to every comment, correct warranted findings, resolve addressed threads, and update `specs/012-brand-site-polish/contracts/review-ledger.md`
- [X] T026 Post at most one explicit `@Codex review` request after round one completes, process round two without another trigger, file and disposition every finding, resolve every thread, wait for green final-head checks, and update `specs/012-brand-site-polish/evidence.md`
- [ ] T027 Stop with the pull request open and ask the owner for the final review and merge ritual

## Dependencies and Execution Order

- T001 through T003 complete before implementation.
- T004 and T005 fail for the intended identity gaps before T006 through T008.
- T010 and T011 fail for the intended terminology and navigation gaps before T012 through T015.
- T017 fails for the intended presentation gaps before T018 through T020.
- T009, T016, and T021 are independent user-story gates that complete before the aggregate T023 gate.
- T024 follows all local validation. T025 completes before the sole optional request in T026. T026 cannot post a third review request.
- T027 is the owner merge gate. S012 never merges its own pull request.

## Parallel Opportunities

- T004 and T005 modify separate Python and browser-test surfaces.
- T010 and T011 modify separate Python and browser-test surfaces.
- User stories share generator and browser outputs, so their implementation remains sequential even though regression tests can be authored independently.

## Implementation Strategy

1. Converge the complete specification and analysis before changing product source.
2. Lock each issue cluster with failing tests before its implementation.
3. Correct canonical sources and reuse existing generated asset and framework contracts.
4. Run focused story gates before the complete repository gate.
5. Publish one reviewable pull request, process at most two Codex rounds, and halt for the owner merge ritual.
