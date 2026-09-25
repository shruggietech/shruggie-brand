# Tasks: Color Roles and Independent Palettes

**Input**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, and `contracts/color-roles.md`

## Phase 1: Setup and baseline

- [x] T001 Capture source hex/path and generated-token baselines for eight brands in temporary output; inspect all color enforcement and publication paths.
- [x] T002 Record Spec Kit requirement review and cross-artifact analysis in `specs/053-color-roles-independent-palettes/` before implementation.

## Phase 2: Shared contract foundation

- [x] T003 Write fail-first role and palette-policy tests, including unsafe/unresolved reference rejection, in `skill/templates/test_brand_contract.py`, `test_interface_contract.py`, and `test_pipeline.py`.
- [x] T004 Define reference-based identity and cue source contracts in `skill/references/01-canon.json` and `canon.schema.json`; implement one resolver in `skill/templates/color_roles.py`.

## Phase 3: User Story 1 - Independent owned palette (Priority: P0)

**Independent Test**: Temporary owned-child and third-party fixtures validate independent/shared choices while contrast remains enforced.

- [x] T005 [US1] Remove owned-child house-palette enforcement in `skill/templates/brand_contract.py` and schema affiliation alternatives.
- [x] T006 [US1] Remove cross-brand hue rejection and mandatory parent-orange assumptions from `skill/templates/enrich_brand.py`, `verify.py`, and `interface_contract.py`.
- [x] T007 [US1] Update `skill/references/01-canon.json`, variance contract, interview, and approval guidance to make palette choice independent of ownership and typography.

## Phase 4: User Story 2 - Formal colors and interface cues (Priority: P0)

**Independent Test**: All production role records resolve and agree across JSON, web, portable, and PDF outputs.

- [x] T008 [US2] Add authoritative formal-color references to `brands/*/brand.json`, preserving all existing hex and logo path values; update continuity bindings.
- [x] T009 [US2] Generate `color-roles.json`, connect token/adapter/registry metadata without changing existing hex values, and project the same records through `skill/templates/gen_guidelines.py` and `gen_guide_pdf.py`.
- [x] T010 [US2] Render labeled role groups and measured pairings in `site/components/guidelines/color-reference.tsx` and type them in `site/lib/guidelines.ts`.
- [x] T011 [US2] Add parity and accessibility tests for generated tokens, adapters, registries, source role data, portable HTML, PDF, and hosted JSON in `skill/templates/test_pipeline.py` and site tests.

## Phase 5: User Story 3 - Migration parity (Priority: P1)

**Independent Test**: Eight production source values, approved geometry, and legacy token names remain stable after build.

- [x] T012 [US3] Bump compatible canon metadata and update version/compatibility records without changing approved brand hex or logo paths.
- [x] T013 [US3] Add migration parity tests and human-readable compatibility notes in `skill/references/` and release/changelog sources.

## Phase 6: Verification and publication handoff

- [x] T014 Run full Python, production-kit, glyph, PDF, site, registry, publication, Markdown, UTF-8/LF/mojibake, and `git diff --check` gates; record precise evidence in `evidence.md`.
- [ ] T015 Complete Spec Kit analysis, mark tasks, commit, push, open official PR, answer every review comment, and wait for green required CI before owner merge handoff.

## Dependencies

T001-T002 precede implementation. T003 fails before T004-T011. T004 supplies the shared resolver for US1-US2. T008 precedes T009-T011. T012-T013 follow the resolved model. T014-T015 follow all source and documentation work. Different generator and site files can be changed independently, but shared source-contract files are edited sequentially.
