# Tasks: Guidelines Reference Experience

**Input**: Design documents from `specs/017-guidelines-reference-experience/`

**Tests**: Test-first coverage is mandatory for inventory, conversion, publication, interaction, accessibility, and regression behavior.

## Phase 1: Baseline and Contracts

- [x] T001 Record issues #147, #148, and #149 plus identity and publication boundaries in `spec.md`
- [x] T002 Define catalog, color, navigation, and publication entities in `data-model.md` and `contracts/`
- [x] T003 Complete specification and experience quality checklists

## Phase 2: Tests First

- [x] T004 [US1] Add manifest-derived grouping, largest-preview, complete-delivery, missing-file, and skipped-capability tests to `skill/templates/test_pipeline.py`
- [x] T005 [US2] Add deterministic color-conversion, scoped-theme, copy-control, and graceful-failure tests to `skill/templates/test_pipeline.py`
- [x] T006 [US3] Add section navigation, no-script fallback, progressive back-to-top, and brand-neutral output tests to `skill/templates/test_pipeline.py`
- [x] T007 [US1] [US3] Add hosted asset rewrite, traversal rejection, missing-target rejection, and exactly-one-exit tests to `scripts/test_prepare_site.py`

## Phase 3: Generated Reference Experience

- [x] T008 [US1] Implement manifest loading, normalized delivery records, semantic grouping, and representative selection in `skill/templates/gen_guidelines.py`
- [x] T009 [US1] Render the complete logo and platform catalog with embedded previews, delivery tables, use guidance, and portable asset links in `skill/templates/gen_guidelines.py`
- [x] T010 [US2] Implement deterministic governed color-space representations and copy controls in `skill/templates/gen_guidelines.py`
- [x] T011 [US2] Render complete dark and light comparison wells for palette, charts, typography, and components in `skill/templates/gen_guidelines.py`
- [x] T012 [US3] Add stable sections, compact contents, no-script top fallback, aria-live status, and progressive reduced-motion-aware back-to-top in `skill/templates/gen_guidelines.py`

## Phase 4: Hosted Publication

- [x] T013 [US1] [US3] Rewrite only validated `data-kit-asset` links and inject one hosted `All brands` exit in `scripts/prepare_site.py`
- [x] T014 [US1] [US2] [US3] Extend browser assertions for catalog completeness, conversions, local themes, copy states, navigation, zoom, mobile, and reduced motion in `site/scripts/verify-site.mjs`

## Phase 5: Documentation and Verification

- [x] T015 Update `skill/SKILL.md`, synchronized `skill/AGENTS.md`, `CHANGELOG.md`, and `skill/CHANGELOG.md`
- [x] T016 Run Spec Kit analyze and resolve every material consistency or coverage finding
- [x] T017 Run focused Python suites and the complete five-kit aggregate build
- [x] T018 Run release, site lint/build/browser, accessibility, encoding, mojibake, and Git hygiene gates
- [x] T019 Inspect all five responsive guideline outputs and record evidence in `evidence.md`
- [ ] T020 Push the branch, publish an issue-closing PR, resolve at most two Codex review rounds, and record final green CI

## Dependencies

- T001-T003 establish the contract.
- T004-T007 must fail before T008-T014 implementation.
- T008 blocks T009-T012; T013 consumes T009 links; T014 covers the integrated result.
- T015-T020 follow implementation and preserve chronological closeout.

## Implementation Strategy

Build the shared manifest model once, then render assets, colors, and navigation from it. Apply hosted context only after generated output is verified. Finish with focused gates, aggregate builds, browser evidence, publication, and review closure.
