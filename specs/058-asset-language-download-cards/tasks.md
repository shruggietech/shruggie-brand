# Tasks: Shared Asset Language and Distinct Download Cards

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), and [asset-language contract](contracts/asset-language.md).
**Prerequisites**: Approved S057 source and v2.4.0 baseline; no new creative approval because derivative bytes and Gate 2 inventory remain unchanged.
**Tests**: Required by FR-011 and autopilot test-first discipline.

## Phase 1: Setup

- [x] T001 Record exact v2.4.0 derivative approval inventory, representative legacy paths, and current version facts in `specs/058-asset-language-download-cards/verification.md`.

## Phase 2: Foundation

- [x] T002 Add failing semantic naming, alias, and collision tests in `skill/templates/test_pipeline.py` or `skill/templates/test_asset_language.py` for wide, stacked, social, monochrome, clear/light/dark, and absent IHPRT wordmark.
- [x] T003 Implement one explicit asset-language classifier and name/alias contract in `skill/templates/asset_language.py`, with source-derived axes and bounded canonical filenames.

## Phase 3: User Story 1 - Understand the right asset (P1)

**Goal**: Shared glossary, names, and first-use explanation across delivered surfaces.
**Independent Test**: Reader chooses a wide, stacked, social, and monochrome asset from glossary and guide labels without interpreting a technical filename.

- [x] T004 [US1] Add the governed glossary and source-documentation catalog route in `skill/references/asset-glossary.md` and `skill/references/documentation-contract.json`.
- [x] T005 [US1] Emit semantic axes and plain-English labels from `skill/templates/gen_guidelines.py` for manifest-driven hosted and portable catalog records.
- [x] T006 [US1] Add first-use glossary explanations or direct anchors to hosted, portable, and PDF guide surfaces in `site/components/guidelines/`, `skill/templates/gen_guidelines.py`, and `skill/templates/gen_guide_pdf.py`.
- [x] T007 [US1] Update shared source examples, main manuals, and generator-facing guidance under `skill/references/` and `skill/SKILL.md` to use one meaning and explain legacy terms. Leave approval-bound brand READMEs byte-identical.

## Phase 4: User Story 2 - Browse one design per card (P1)

**Goal**: One card per actual design with consistent preview, hint, search, and deliveries.
**Independent Test**: All eight portals separate applicable wide, stacked, and social cards; IHPRT has no invented standalone wordmark.

- [x] T008 [US2] Add failing mixed-design, size-stack, bounded-preview, and alias-within-design tests for `group_asset_deliveries` and `portal_assets` in `skill/templates/test_pipeline.py`.
- [x] T009 [US2] Replace the grouping tuple and duplicated technical title construction in `skill/templates/gen_guidelines.py` with shared semantic design identity, human-readable labels, and an optimally sized card face. Correct reused web icon roles without mixing full, reduced, supplied, or maskable artwork.
- [x] T010 [US2] Update hosted card types, search/filter terms, preview and delivery presentation in `site/lib/guidelines.ts` and `site/components/guidelines/asset-library-client.tsx`, preserving the existing keyboard and AA styling in `site/app/globals.css`.
- [x] T011 [US2] Add all-brand catalog checks in `site/tests/site.test.mjs` and run the existing browser accessibility checks in `site/scripts/verify-site.mjs`.

## Phase 5: User Story 3 - Continue using old links (P2)

**Goal**: Publish descriptive names while preserving exact old file paths and owner approval.
**Independent Test**: Every mapped new alias has identical bytes to an approved source, old direct paths remain, and `logos/approval.json` matches the baseline.

- [x] T012 [US3] Add failing alias-map, path confinement, collision, and Gate 2 invariance tests in `skill/templates/test_asset_language.py`, `skill/templates/test_pipeline.py`, and publication contract tests.
- [x] T013 [US3] Generate descriptive file aliases and an old-to-new map after derivative approval from `skill/templates/` without mutating `logos/approval.json` or existing derivative bytes.
- [x] T014 [US3] Validate aliases, complete inventories, path confinement, digest equality, and old direct paths in `skill/templates/verify.py` and the existing `scripts/prepare_site.py` site copy gate.
- [x] T015 [US3] Document exact compatibility behavior and migration in `skill/references/` and `specs/058-asset-language-download-cards/verification.md`.

## Phase 6: Polish and gates

- [x] T016 Update BrandBuilder/site version and migration impact, root/skill changelogs, and any affected release/documentation contracts for 2.5.0 in source files only.
- [x] T017 Recheck Spec Kit cross-artifact analysis after any specification edits, run all focused tests, all eight kit/glyph checks, site build and accessibility/publication audits; record measured results in `specs/058-asset-language-download-cards/verification.md`.
- [ ] T018 Check UTF-8 without BOM, LF, mojibake, ignored output, and final scope diff; commit `feat(S058): ...`, push, publish PR, resolve CI and no more than two review rounds.

## Dependencies & Execution Order

T001 establishes the baseline. T002 must fail before T003. T003 enables T004-T007 and T008-T011. T012 must fail before T013-T015. T016 follows implemented contracts. T017 and T018 close the slice. All three stories are independently demonstrable, while the complete slice ships them together.

## Parallel Opportunities

Documentation source edits in T004 and catalog-focused tests in T008 touch separate files after T003. Site type/UI work in T010 can start after T009 defines the payload. No concurrent edits to `gen_guidelines.py` or `test_pipeline.py` are planned.

## Implementation Strategy

Establish semantic axes and approval invariants first, then expose truthful names, then separate cards, then add verified aliases. Keep the existing production kit and site publishing pipeline as the end-to-end gate rather than checking only isolated examples.
