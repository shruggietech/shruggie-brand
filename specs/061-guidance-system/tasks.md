# Tasks: Durable Guidance System

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [guidance-publication contract](contracts/guidance-publication.md)

## Phase 1: Setup and source inventory

- [x] T001 Review issues #270, #271, #272, prior repo issue/PR/spec/manual source history, and write a bounded provenance audit in `specs/061-guidance-system/verification.md`.
- [x] T002 Record all 16 current manual and relevant skill/generated instruction surfaces with disposition and all eight brand/topic combinations in `specs/061-guidance-system/verification.md`.
- [x] T003 Inspect current publication contracts, generator outputs, and site browser gates; record original defects and invariant fields in `specs/061-guidance-system/verification.md`.

## Phase 2: Shared foundation

- [x] T004 [P] Add stable local reference-ID and citation validation in `scripts/` with mutation tests in `scripts/test_public_documentation.py` or a focused new test.
- [x] T005 [P] Add exact-byte public documentation-facts projection in `scripts/prepare_site.py` and verify it in `scripts/audit_publication_artifacts.py` plus focused tests.

## Phase 3: User Story 1 - Curated references (P1, #271)

**Goal**: A reader or offline agent finds a classified, annotated, stable source and its actual local use.

**Independent test**: References is in the manual catalog, site search, and packaged skill; all IDs/citations resolve and duplicate/missing IDs fail.

- [x] T006 [US1] Author the owner-named primary and advisory bibliography, historical-source dispositions, edition caveats, and application notes in `skill/references/references.md`.
- [x] T007 [US1] Register the new page and disposition in `skill/references/documentation-contract.json` and update pagination/source contract tests.
- [x] T008 [US1] Convert relative offline citations to hosted MDX routes in `scripts/documentation_render.py`, preserving exact raw skill sources and testing both outputs.
- [x] T009 [US1] Validate links, IDs, offline package membership, nav, and search in documentation and site tests.

## Phase 4: User Story 2 - Usable generated guidelines (P1, #270)

**Goal**: Every brand topic conveys meaning, action, and exact authority without filler or raw metadata.

**Independent test**: Hosted/portable/PDF/bundled reader tasks succeed across eight brands and conditional states; facts JSON equals certified kit bytes.

- [x] T010 [US2] Refactor `site/components/guidelines/topic-content.tsx` and `site/lib/guidelines.ts` with specific affiliation, inheritance, override, version, binding, registry, and empty-state explanations.
- [x] T011 [US2] Update `site/app/globals.css` for semantic definition-row alignment, narrow reflow, and 200% zoom; keep keyboard focus and heading containment intact.
- [x] T012 [US2] Improve generated offline and portable guidance in `skill/templates/documentation_contract.py` and `gen_guidelines.py`; review the shared facts in `gen_guide_pdf.py` and edit that template only if a required PDF explanation is absent.
- [x] T013 [US2] Extend site/browser and Python tests for fact links, reader tasks, conditional expressions, responsive headings, and exact authority.

## Phase 5: User Story 3 - Applied source-aware guidance (P1, #272)

**Goal**: Concrete tasks in each relevant manual/skill surface carry a valid citation and honest support boundary.

**Independent test**: Manual disposition matrix complete; discovery, identity, palette, components, docs, web, Android, WordPress, and egui examples are locally actionable with resolved citations.

- [x] T014 [US3] Apply discovery, distinctiveness, logo, color, and component guidance in relevant `skill/references/*.md` files, distinguishing project rules from advice.
- [x] T015 [US3] Apply web, Android, WordPress, egui, accessibility, documentation, and verification guidance in relevant `skill/references/*.md` files without implying unshipped adapters.
- [x] T016 [US3] Update canonical `skill/SKILL.md` task routing and fix the obsolete gate count; regenerate `skill/AGENTS.md` via `sync_agents_md.py`.
- [x] T017 [US3] Verify manual and generated/packaged citations, owner approval flow, version identity, and support claims with focused tests and reader-task evidence.

## Phase 6: Full validation and PR handoff

- [x] T018 Run Spec Kit cross-artifact analysis, resolve findings, and keep spec/plan/tasks/verification aligned.
- [x] T019 Run complete documented validation: Python tests, eight zero-problem kits and glyph checks, site lint/build/browser verification, public documentation audit, publication-artifact audit, and source hygiene/mojibake check.
- [x] T020 Update issue/project disposition, commit S061 sources, push `codex/061-guidance-system`, and create the official PR with issue traceability and verification evidence.
- [ ] T021 Wait for required CI and every third-party review; fix and reply to each actionable comment, allow no more than one manual `@codex review` re-request, and hand off only after green CI and satisfied reviews.

## Dependencies and order

T001-T003 establish evidence. T004 and T005 are independent. T006-T009 precede source-aware applications T014-T017. T005 precedes the public-fact UI in T010-T013. The three stories remain independently testable but are delivered together. T018-T021 follow implementation.

## Parallel opportunities

T004 and T005 touch separate validation/publication paths. Source inventory of distinct manual pages can be read in parallel. The single-author work order is reference library, guideline projection, then applied manual guidance to avoid dangling citations.

## Implementation strategy

Keep each story independently verifiable, then run the complete integrated gate. The requested delivery is the complete three-issue slice; no partial MVP is a handoff point.
