# Tasks: Documentation Footer Removal

**Input**: Design documents from `/specs/029-docs-footer/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: S029 requires source-contract, rendered-route, responsive pagination, accessibility, static-export, and full repository validation. Test tasks precede the production change.

**Organization**: Tasks are grouped by user story so documentation footer removal and marketing-footer retention remain independently testable.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Lock scope, traceability, and quality gates.

- [x] T001 Confirm S029 scope, issue #191 traceability, route boundaries, and completed specification quality review in specs/029-docs-footer/spec.md and specs/029-docs-footer/checklists/requirements.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the route-surface regression contract before changing production composition.

- [x] T002 Add failing documentation source-composition assertions in site/tests/site.test.mjs
- [x] T003 [P] Add failing rendered documentation footer-absence and retained-pagination assertions in site/scripts/verify-site.mjs

**Checkpoint**: Source and rendered checks fail on the current documentation footer while preserving existing homepage and guideline expectations.

---

## Phase 3: User Story 1 - Continue through documentation without obstruction (Priority: P1) MVP

**Goal**: Remove the global marketing footer from every documentation page while preserving contextual pagination and documentation behavior.

**Independent Test**: Export all documentation routes, prove each contains zero `.site-footer` elements, and verify the index plus a representative article retain reachable pagination at desktop and narrow viewport widths.

- [x] T004 [US1] Remove the shared Footer import and rendered element from site/app/docs/[[...slug]]/page.tsx and obsolete documentation footer spacing from site/app/globals.css without changing DocsPage pagination or page content
- [x] T005 [US1] Run focused source-contract, type, export, rendered pagination, keyboard, narrow viewport, and WCAG checks from specs/029-docs-footer/quickstart.md

**Checkpoint**: Documentation pages contain no marketing footer and retain their complete contextual navigation.

---

## Phase 4: User Story 2 - Retain the marketing footer where intended (Priority: P2)

**Goal**: Preserve the approved shared footer on the marketing homepage and the separate dedicated footer behavior of guideline portals.

**Independent Test**: Verify the homepage contains exactly one `.site-footer` with the approved ordered destinations and guideline routes continue to contain no `.site-footer` while retaining their guide footer.

- [x] T006 [US2] Preserve and exercise homepage footer policy and guideline footer isolation in site/tests/site.test.mjs and site/scripts/verify-site.mjs

**Checkpoint**: The correction remains limited to documentation routes.

---

## Phase 5: Polish and Cross-Cutting Concerns

**Purpose**: Synchronize records, certify all generated output, and prepare review evidence.

- [x] T007 Record the S029 route-composition correction in CHANGELOG.md
- [x] T008 Run the full production build, zero-problem kit verification, zero-failure glyph validation, release-contract, static-site, accessibility, and repository-hygiene gates from specs/029-docs-footer/quickstart.md
- [x] T009 Record commands, TDD failure evidence, and final zero-problem outcomes in specs/029-docs-footer/evidence.md
- [x] T010 Validate UTF-8 without BOM, LF endings, mojibake absence, ignored generated output, git diff hygiene, and final spec, plan, task, and evidence synchronization

---

## Dependencies and Execution Order

- Setup has no dependencies.
- Foundational regression tests depend on Setup and must fail before production changes.
- US1 depends on both foundational tests.
- US2 depends on the US1 route-scope change and verifies unaffected surfaces.
- Polish depends on both user stories.

## Parallel Opportunities

- T002 and T003 touch separate test files and can be drafted independently.
- Changelog wording can be prepared independently from final gate execution after both user stories pass.

## Parallel Example: Route-Surface Regressions

```text
Task: Add documentation source-composition assertions in site/tests/site.test.mjs
Task: Add rendered footer-absence and pagination assertions in site/scripts/verify-site.mjs
```

## Implementation Strategy

1. Lock the route-surface contract with failing source and browser checks.
2. Deliver US1 by removing only the documentation page's footer composition.
3. Prove US2 by retaining the homepage footer policy and guideline isolation.
4. Run the complete repository gate, record evidence, and synchronize all S029 artifacts before publication.

## Format Validation

All 10 tasks use the required checkbox, sequential task ID, optional parallel marker, required user-story label in story phases, and explicit file paths.
