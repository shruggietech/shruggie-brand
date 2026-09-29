# Tasks: Brand Essentials and Docs Navigation

**Input**: spec.md, plan.md, research.md, data-model.md, contracts/essentials-projection.md

**Tests**: Focused failing tests precede each implementation phase.

## Phase 1: Source classification

- [x] T001 Inventory every current overview, foundation, promise, scope, boundary, and related visual sentence for all eleven brands in disposition-inventory.md (FR-001, SC-001).
- [x] T002 Record guide/source field mapping and empty-role behavior in projection-map.md (FR-003, FR-005).

## Phase 2: Brand essentials projection

- [x] T003 [US1] Add failing rich/sparse/strategy and exact-source tests in skill/templates/test_brand_essentials.py (FR-002, FR-003, FR-006, FR-009).
- [x] T004 [US1] Implement shared projection in skill/templates/brand_essentials.py and portal data in skill/templates/gen_guidelines.py (FR-002, FR-003, FR-005).
- [x] T005 [US1] Replace hosted overview content and static TOC in site/components/guidelines/overview-content.tsx and site/lib/guidelines.ts (FR-002, FR-004).

## Phase 3: Portable and PDF parity

- [x] T006 [US2] Add failing portable/PDF heading, role, and omission checks in skill/templates/test_brand_essentials.py and site/tests/site.test.mjs (FR-004, FR-009).
- [x] T007 [US2] Render source-bound essentials and dynamic contents in skill/templates/gen_guidelines.py (FR-004, FR-005).
- [x] T008 [US2] Replace historical name/promises material with essentials in skill/templates/gen_guide_pdf.py, preserving detailed identity sheets (FR-003, FR-004).

## Phase 4: Docs sidebar

- [x] T009 [US3] Add failing release/candidate decision and responsive rendered-footer assertions in site/tests/site.test.mjs and site/scripts/verify-site.mjs (FR-007, FR-008, FR-009).
- [x] T010 [US3] Implement publication-driven theme-switch slot and styling in site/components/documentation-sidebar-theme.tsx, site/app/docs/layout.tsx, and site/app/globals.css (FR-007, FR-008).

## Phase 5: Completion

- [x] T011 Run focused and full documented kit, glyph, PDF, site, accessibility, registry, and publication gates; record exact outcomes in verification.md (FR-010, SC-005).
- [x] T012 Update CHANGELOG.md and source documentation, check UTF-8 LF, BOM, mojibake, and Git diff, then commit (FR-001, FR-010).
- [ ] T013 Push and publish the official PR linked to #298 and #299.
- [ ] T014 Resolve all first-round external reviews and at most one requested second Codex round; wait for final green required CI and hand off the merge.

## Dependencies

T001 and T002 establish what may project. T003 precedes T004 and T005; T006 precedes T007 and T008; T009 precedes T010. T011 follows all implementation work; T012 through T014 follow verification. No subagent parallelism is planned.
