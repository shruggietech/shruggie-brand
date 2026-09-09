# Tasks: Unified Site Navigation and Route Consolidation

**Input**: Design documents from `/specs/025-unified-navigation/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: S025 explicitly requires automated generator, route, source-contract, rendered-navigation, accessibility, registry, and repository validation. Test tasks precede their implementations.

**Organization**: Tasks are grouped by user story so root removal, brand hierarchy, and documentation hierarchy remain independently testable on the shared generated-navigation foundation.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Lock the slice records, issue traceability, and review gates.

- [x] T001 Confirm the S025 scope, route decisions, and #175/#179/#180 traceability in specs/025-unified-navigation/spec.md
- [x] T002 [P] Complete the reviewer-owned navigation and route requirements review in specs/025-unified-navigation/checklists/navigation-contract.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish authoritative navigation metadata and fail-closed validation before changing presentation routes.

- [x] T003 Add failing portal hierarchy metadata and shared-topic tests in skill/templates/test_pipeline.py
- [x] T004 Add failing documentation mapping, route absence, destination resolution, and registry catalog-to-item tests in scripts/test_prepare_site.py
- [x] T005 Extend generated brand topics with exact label, section, order, and path metadata in skill/templates/gen_guidelines.py
- [x] T006 Add the authoritative documentation navigation mapping and emitted metadata in scripts/prepare_site.py
- [x] T007 Implement navigation, content-mapping, route-target, and full registry item validation in scripts/prepare_site.py
- [x] T008 Run focused generator and site-preparation tests in skill/templates/test_pipeline.py and scripts/test_prepare_site.py

**Checkpoint**: Generated inventories express and validate both exact hierarchies before any page consumes them.

---

## Phase 3: User Story 1 - Reach useful brand guidance directly (Priority: P1) MVP

**Goal**: Remove every redundant brand-root content route while preserving all useful brand and machine endpoints.

**Independent Test**: Export all brands and prove root route absence, intentional not-found behavior, direct homepage destinations, valid retained routes, and complete registry resolution.

- [x] T009 [US1] Add failing source and route assertions for brand-root removal and retained endpoints in site/tests/site.test.mjs and site/scripts/verify-site.mjs
- [x] T010 [US1] Remove brand route records and point homepage structured data and brand breadcrumbs to guidelines in scripts/prepare_site.py
- [x] T011 [US1] Remove the root dynamic brand page in site/app/(site)/[slug]/page.tsx and eliminate stale root links from site source
- [x] T012 [US1] Update route kinds and consumers for the retired brand kind in site/lib/routes.ts and site tests
- [x] T013 [US1] Run focused source, route, sitemap, structured-data, and retained-endpoint checks in site/tests/site.test.mjs and scripts/test_prepare_site.py

**Checkpoint**: Brand roots are absent and every nested human or machine endpoint remains valid.

---

## Phase 4: User Story 2 - Scan one consistent brand-guidelines hierarchy (Priority: P1)

**Goal**: Render the exact shared brand hierarchy and consolidate Assets at the stable downloads route.

**Independent Test**: Inspect every brand tree and operate representative destinations across desktop, narrow, touch-only, no-script, and zoom modes while checking one-time content placement and active ancestry.

- [x] T014 [US2] Add failing exact-tree, Assets-route, active-parent, no-script, input-mode, zoom, and content-uniqueness assertions in site/tests/site.test.mjs and site/scripts/verify-site.mjs
- [x] T015 [US2] Build typed brand navigation sections and special Assets path resolution from generated metadata in site/lib/guidelines.ts
- [x] T016 [US2] Lift the shared brand DocsLayout to site/app/(guidelines)/[slug]/layout.tsx and remove the narrower guidelines layout
- [x] T017 [US2] Move the downloads route into the guideline route group and combine direct download resources with AssetLibrary in site/app/(guidelines)/[slug]/downloads/page.tsx and site/components/guidelines/downloads-content.tsx
- [x] T018 [US2] Exclude the obsolete guidelines Assets route and render explicit Integration empty state support in site/app/(guidelines)/[slug]/guidelines/[[...topic]]/page.tsx and site/components/guidelines/topic-content.tsx
- [x] T019 [US2] Add nested hierarchy, active ancestry, no-script, narrow-width, touch, and zoom presentation rules in site/app/globals.css
- [x] T020 [US2] Run focused brand navigation source and rendered checks in site/tests/site.test.mjs and site/scripts/verify-site.mjs

**Checkpoint**: All brands use one exact hierarchy and one complete Assets destination.

---

## Phase 5: User Story 3 - Scan grouped project documentation (Priority: P2)

**Goal**: Render the approved documentation hierarchy while preserving every page title, body, and URL.

**Independent Test**: Compare the generated documentation inventory with its tree and verify exact groups, labels, ordering, one-time page placement, stable routes, active ancestry, and access modes.

- [x] T021 [US3] Add failing documentation tree, one-to-one mapping, title/URL stability, and rendered active-state assertions in scripts/test_prepare_site.py, site/tests/site.test.mjs, and site/scripts/verify-site.mjs
- [x] T022 [US3] Add a typed authoritative documentation tree builder in site/lib/documentation.ts
- [x] T023 [US3] Render the generated grouped tree in site/app/docs/layout.tsx without changing source page titles or routes
- [x] T024 [US3] Extend shared nested-navigation presentation and no-script behavior for documentation in site/app/globals.css
- [x] T025 [US3] Run focused documentation generation, source, and rendered navigation checks in scripts/test_prepare_site.py, site/tests/site.test.mjs, and site/scripts/verify-site.mjs

**Checkpoint**: Every documentation page appears once beneath the exact approved group and retains its existing identity.

---

## Phase 6: Polish and Cross-Cutting Concerns

**Purpose**: Synchronize records, certify all generated output, and prepare review evidence.

- [x] T026 [P] Record the S025 navigation and route-contract decision in CHANGELOG.md
- [x] T027 Run all focused Python, Node source-contract, TypeScript, static-export, Playwright, and axe checks documented in specs/025-unified-navigation/quickstart.md
- [x] T028 Run full production build, verify.py, validate_glyph.py, release archive certification, registry resolution, and repository hygiene gates
- [x] T029 Record commands and zero-problem outcomes in specs/025-unified-navigation/evidence.md and mark completed tasks in specs/025-unified-navigation/tasks.md
- [x] T030 Validate UTF-8 without BOM, LF endings, mojibake absence, ignored generated output, git diff hygiene, and final spec/plan/task synchronization

---

## Dependencies and Execution Order

- Setup has no dependencies.
- Foundational generated metadata and validation depend on Setup and block all user stories.
- US1 depends on the foundation and removes obsolete routes before hierarchy consumers are changed.
- US2 depends on US1 because the Assets route becomes part of the brand shell after root cleanup.
- US3 depends only on the foundation but follows US2 to keep shared layout and verification edits sequential.
- Polish depends on all three user stories.

## Parallel Opportunities

- T001 and T002 touch separate specification records.
- Generator topic tests and route-preparation tests can be drafted independently before shared implementation.
- Documentation hierarchy work is logically independent after the generated navigation foundation, although shared CSS and browser verification remain sequential.
- T026 can proceed independently from final validation execution.

## Parallel Example: Generated Navigation Contracts

```text
Task: Add brand portal hierarchy assertions in skill/templates/test_pipeline.py
Task: Add documentation mapping and route assertions in scripts/test_prepare_site.py
```

## Implementation Strategy

1. Lock and validate generated hierarchy records.
2. Deliver US1 as the minimum useful increment by removing obsolete brand roots safely.
3. Deliver US2 by consolidating and nesting brand guidance around the stable Assets route.
4. Deliver US3 from the same navigation-contract pattern without changing documentation identity.
5. Run the complete production, release, static-site, accessibility, and hygiene gate before publication.

## Format Validation

All 30 tasks use the required checkbox, sequential task ID, optional parallel marker, required user-story label in story phases, and explicit file paths.
