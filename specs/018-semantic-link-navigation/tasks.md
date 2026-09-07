# Tasks: Semantic Link and Documentation Navigation

**Input**: Design documents from `specs/018-semantic-link-navigation/`

**Tests**: Test-first coverage is mandatory for generator cascade behavior and every affected browser interaction family.

## Phase 1: Baseline and Contracts

- [x] T001 Record issues #142 and #143, superseded guidance, scope, identity boundary, and success gates in `spec.md`
- [x] T002 Define anchor-family and pagination contracts in `data-model.md` and `contracts/`
- [x] T003 Complete specification and experience quality checklists in `checklists/`

## Phase 2: Tests First

- [x] T004 [US1] Add a generated-anchor regression to `skill/templates/test_pipeline.py`
- [x] T005 [US1] [US3] Replace ordinary-link browser assertions with role inventory, computed decoration, focus, visited, reduced-motion, theme, and isolation checks in `site/scripts/verify-site.mjs`
- [x] T006 [US2] Add first, middle, and last pagination assertions for neutral states, hierarchy, structure, URLs, wrapping, targets, and zoom in `site/scripts/verify-site.mjs`

## Phase 3: Semantic Link Taxonomy

- [x] T007 [US1] Remove the global generated hover underline in `skill/templates/gen_vanilla.py`
- [x] T008 [US1] Implement explicit site link families and complete state treatments in `site/app/globals.css`
- [x] T009 [US1] Add explicit text-action cues and stable role hooks in `site/app/(site)/page.tsx` and `site/app/(site)/[slug]/page.tsx`
- [x] T010 [US1] [US3] Preserve component-owned footer, navigation, card, button, identity, search, sidebar, breadcrumb, and contents treatments in site source

## Phase 4: Documentation Pagination

- [x] T011 [US2] Implement neutral pagination surfaces, stable title and description hierarchy, restrained green border states, and wrapping in `site/app/globals.css`
- [x] T012 [US2] Validate Fumadocs neighbor structure without replacing its routing in `site/app/docs/[[...slug]]/page.tsx`

## Phase 5: Documentation and Verification

- [x] T013 Update `CHANGELOG.md`, `skill/CHANGELOG.md`, and synchronized generated guidance where required
- [x] T014 Run Spec Kit analysis and resolve every material consistency or coverage finding
- [x] T015 Run focused Python and site contract suites
- [x] T016 Run the complete five-kit build and confirm zero verifier problems and glyph failures
- [x] T017 Run site lint, production build, browser, accessibility, motion, zoom, encoding, mojibake, and Git hygiene gates
- [x] T018 Inspect representative desktop/mobile dark/light outputs and record evidence in `evidence.md`
- [x] T019 Push, publish an issue-closing PR, resolve no more than two Codex review rounds, and record final green CI

## Dependencies

- T001-T003 establish the contract.
- T004-T006 must fail before T007-T012 implementation.
- T007 prevents generated cascade leakage before T008-T012 establish site-owned roles.
- T013-T019 close the slice chronologically after implementation.

## Implementation Strategy

Fix the unsafe shared default first, then define every site role explicitly. Treat pagination as contextual navigation within the same taxonomy, and prove the integrated result through computed browser behavior rather than CSS-source assumptions.
