# Tasks: Hosted Guidelines Portal Rebuild

**Input**: Design documents from `specs/019-guidelines-portal-rebuild/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are required by the specification and autopilot protocol. Each story begins with failing contract coverage.

**Organization**: Tasks are grouped by independently testable user story, with the shared generated-content boundary established first.

## Phase 1: Setup and Baseline

**Purpose**: Lock the scope, source boundaries, and current regression behavior.

- [x] T001 Record the S017 architectural supersession and S019 issue traceability in `CHANGELOG.md`, `skill/CHANGELOG.md`, and `specs/019-guidelines-portal-rebuild/evidence.md`
- [x] T002 Inventory existing guideline generation, publication, routes, site layout, and verification selectors in `skill/templates/gen_guidelines.py`, `scripts/prepare_site.py`, `site/app/`, and `site/scripts/verify-site.mjs`
- [x] T003 Verify existing ignore rules cover `dist/`, `site/generated/`, site exports, browser evidence, caches, and local Spec Kit state in `.gitignore` and `.specify/.gitignore`

---

## Phase 2: Foundational Portal Contract

**Purpose**: Establish the verified payload and site projection required by every story.

- [x] T004 Add failing portal payload, inventory integrity, portable-guide, and Python 3.8 compatibility tests in `skill/templates/test_pipeline.py`
- [x] T005 Add failing publication, generated-registry, route, unsafe-path, duplicate-delivery, and Markdown instruction tests in `scripts/test_prepare_site.py`
- [x] T006 Implement deterministic portal records, semantic asset grouping, nonvisual resources, instruction extraction, color references, and concise portable HTML in `skill/templates/gen_guidelines.py`
- [x] T007 Implement strict portal validation, portable-guide downloads, generated guideline registry, constrained instruction blocks, and canonical topic routes in `scripts/prepare_site.py`
- [x] T008 Add typed portal loaders and page-tree construction in `site/lib/guidelines.ts` and `site/lib/routes.ts`
- [x] T009 Validate the foundation with `skill/templates/test_pipeline.py`, `scripts/test_prepare_site.py`, and `pnpm --dir site lint`

**Checkpoint**: Every verified kit publishes a complete structured portal, portable guide download, static topic tree, and canonical route inventory.

---

## Phase 3: User Story 1 - Move through focused brand topics (Priority: P1) MVP

**Goal**: Replace the hosted one-page guide with accessible direct topic routes and persistent brand-neutral navigation.

**Independent Test**: Traverse all topics, current states, headings, fragment links, and downloads for every brand on desktop, mobile, zoomed, keyboard, touch, reduced-motion, and no-script paths.

- [x] T010 [US1] Add failing page-tree, navigation, current-topic, fragment, mobile disclosure, footer, and no-script browser contracts in `site/scripts/verify-site.mjs` and `site/tests/site.test.mjs`
- [x] T011 [US1] Implement the per-brand Fumadocs layout and static catch-all topic route in `site/app/(guidelines)/[slug]/guidelines/layout.tsx` and `site/app/(guidelines)/[slug]/guidelines/[[...topic]]/page.tsx`
- [x] T012 [US1] Implement brand-neutral topic content, in-page outline, and separated footer utilities in `site/components/guidelines/topic-content.tsx` and `site/components/guidelines/guide-footer.tsx`
- [x] T013 [US1] Add persistent, mobile, fragment-offset, topic, and footer styles in `site/app/globals.css`
- [x] T014 [US1] Extend generated metadata, breadcrumbs, sitemap, structured data, and social preview records for every guideline topic in `scripts/prepare_site.py` and `site/lib/routes.ts`
- [x] T015 [US1] Validate all topic routes and no-script navigation with `pnpm --dir site lint`, `pnpm --dir site build`, and focused Playwright checks

**Checkpoint**: The single hosted document is retired and every production brand has a usable multi-page portal.

---

## Phase 4: User Story 2 - Scan and copy trustworthy color values (Priority: P1)

**Goal**: Provide compact stable HEX-first color rows with accessible secondary details and copy outcomes.

**Independent Test**: Exercise both palettes, longest aliases, multiple disclosures, successful and failed copy paths, zoom, and overflow for all brands.

- [x] T016 [US2] Add failing color-row data, canonical derivation, and alias tests in `skill/templates/test_pipeline.py` and `scripts/test_prepare_site.py`
- [x] T017 [US2] Add failing color layout-stability, copy fallback, announcement, focus, target-size, and responsive checks in `site/scripts/verify-site.mjs`
- [x] T018 [US2] Implement semantic color list and progressive copy behavior in `site/components/guidelines/color-reference.tsx` and `site/components/guidelines/copy-value.tsx`
- [x] T019 [US2] Add compact row, isolated disclosure, swatch, value, alias, and mobile styles in `site/app/globals.css`
- [x] T020 [US2] Validate color data and browser behavior across both palettes for all five brands

**Checkpoint**: Canonical HEX values are immediately scannable and secondary formats never destabilize unrelated entries.

---

## Phase 5: User Story 3 - Find the right asset by purpose (Priority: P1)

**Goal**: Replace the exhaustive card wall with purpose-led collections, bounded representatives, complete details, document treatments, rendered instructions, and progressive search and filters.

**Independent Test**: Complete logo, web, Android, iOS, macOS, Windows, and instruction tasks for all brands while proving exact manifest coverage and no duplicate or dead downloads.

- [x] T021 [US3] Add failing representative grouping, family taxonomy, nonvisual resource, alias, hash, and complete-delivery tests in `skill/templates/test_pipeline.py`
- [x] T022 [US3] Add failing hosted asset registry, rendered Markdown, safe download, exact coverage, and duplicate rejection tests in `scripts/test_prepare_site.py`
- [x] T023 [US3] Add failing bounded-preview, card-height, search, facet, query-state, live-count, empty-state, detail, document-row, no-script, and task-flow browser checks in `site/scripts/verify-site.mjs`
- [x] T024 [US3] Implement server-rendered asset families and representative detail inventory in `site/components/guidelines/asset-library.tsx`
- [x] T025 [US3] Implement progressive search, filters, query synchronization, live results, and reset behavior in `site/components/guidelines/asset-library-client.tsx`
- [x] T026 [US3] Implement nonvisual resource rows and rendered instruction topic integration in `site/components/guidelines/resource-list.tsx` and constrained block output from `scripts/prepare_site.py`
- [x] T027 [US3] Add bounded preview, family, filter, result, detail, delivery, resource, and responsive styles in `site/app/globals.css`
- [x] T028 [US3] Validate task flows and exact inventories across all five brands with Python, site build, and focused Playwright checks

**Checkpoint**: Visitors can find and download the right asset without reading storage paths, while every authoritative delivery remains available.

---

## Phase 6: User Story 4 - Read balanced landing pages and footer utilities (Priority: P1)

**Goal**: Keep every brand name legible and every footer utility distinct across supported layouts.

**Independent Test**: Measure all five brand headings and topic footers at 360, 768, 1024, and 1280 pixels and 200 percent zoom.

- [x] T029 [US4] Add failing heading containment, hero collision, action visibility, footer separation, and target-size checks in `site/scripts/verify-site.mjs`
- [x] T030 [US4] Implement the brand-specific heading scale, width, wrapping, and responsive hero transition in `site/app/globals.css`
- [x] T031 [US4] Validate all production brand landing pages and guideline topic footers across the required viewport and zoom matrix

**Checkpoint**: `ShruggieTech` and every other production name fit without clipping, and footer controls remain separate and usable.

---

## Phase 7: Polish and Cross-Cutting Verification

**Purpose**: Reconcile documentation and prove the complete correction before publication.

- [x] T032 Update the generator and site behavior documentation in `skill/SKILL.md`, `skill/AGENTS.md`, `README.md`, and `specs/019-guidelines-portal-rebuild/evidence.md`
- [x] T033 Run `speckit-analyze` coverage remediation against `spec.md`, `plan.md`, and `tasks.md`
- [x] T034 Run Python 3.8 compatibility, all unit tests, Markdown, probe, five-kit build, zero-problem verify, and zero-failure glyph gates
- [x] T035 Run site lint, static build, full Playwright and axe matrix, no-script paths, required task journeys, and encoding and mojibake checks
- [x] T036 Review generated desktop and mobile evidence for all five brands and record exact results in `specs/019-guidelines-portal-rebuild/evidence.md`
- [x] T037 Mark all completed tasks, set the spec status to In Review, and verify no generated or local-state files are staged

---

## Dependencies and Execution Order

- Setup tasks T001 to T003 precede the shared portal foundation.
- T004 and T005 are written before T006 to T008. T009 gates all user stories.
- US1 establishes the hosted shell and must complete before US2 and US3 integrate their topic components.
- US2 and US3 use the same generated registry but are independently testable after US1.
- US4 can be implemented after the browser harness understands the new guideline routes.
- T032 to T037 require all user stories to be complete.

## Parallel Opportunities

- The Python generator contract and site publication contract tests target separate files but converge before implementation.
- Color and asset component implementation target separate modules after the portal foundation.
- Documentation updates and final evidence scaffolding can proceed while focused checks run, but full gates remain sequential.

## Implementation Strategy

The MVP is US1 plus the foundational portal contract because it removes the unusable single-page hosted architecture. US2 and US3 then replace the two densest regressions without changing the source contract. US4 closes the independent landing typography failure. The slice ships only as the full five-issue correction, with no partial PR.
