# Tasks: Glitchpad Identity Color Approval

**Input**: Design documents from `specs/015-glitchpad-color-system/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, and quickstart.md

**Tests**: S015 requires test-first coverage for decision-study validation and all approved production behavior.

**Organization**: Tasks are chronological across decision evidence, the owner approval gate, approved implementation, verification, and publication.

## Phase 1: Setup and Baseline

**Purpose**: Establish traceability, source boundaries, and protected identity fingerprints.

- [x] T001 Record #146 scope, merged S014 prerequisites, clean base revision, and current Glitchpad role mappings in `specs/015-glitchpad-color-system/evidence.md`
- [x] T002 Create `codex/015-glitchpad-color-system` and bind `.specify/feature.json` to `specs/015-glitchpad-color-system`
- [x] T003 [P] Confirm `dist/.s015-color-study/` and all generated kit, screenshot, PDF, registry, archive, and site-export paths remain ignored in `.gitignore`
- [x] T004 Record stable pre-change path and lockup-geometry fingerprints in `specs/015-glitchpad-color-system/evidence.md`

---

## Phase 2: Foundational Decision Contracts

**Purpose**: Define complete candidate matrices, measurement rules, and fail-closed study behavior before rendering proposals.

- [x] T005 Add failing matrix-completeness, hex-validation, path-fingerprint, contrast, and output-boundary tests in `scripts/test_glitchpad_color_study.py`
- [x] T006 Implement the three complete exploratory matrices and protected geometry fingerprint in `scripts/glitchpad_color_study.py`
- [x] T007 Implement contrast observations and fail-closed required-context validation in `scripts/glitchpad_color_study.py`
- [x] T008 Confirm the study makes zero production-source or production-output mutations in `scripts/test_glitchpad_color_study.py`

**Checkpoint**: The study can only render complete, valid, geometry-preserving exploratory matrices into an ignored destination.

---

## Phase 3: User Story 1 - Compare credible identity directions (Priority: P1)

**Goal**: Produce a controlled visual and numerical comparison of Sulfur Sheet, Signal Slate, and Sulfur Plate.

**Independent Test**: Generate the study once and confirm identical geometry plus complete dark, light, lockup, small-size, launcher, and store contexts for all directions.

- [x] T009 [US1] Add failing required-section and required-sample assertions in `scripts/test_glitchpad_color_study.py`
- [x] T010 [US1] Generate labeled dark and near-white full-mark, horizontal, and stacked comparisons in `scripts/glitchpad_color_study.py`
- [x] T011 [US1] Generate 16, 24, 32, and 48 pixel full/reduced samples plus desktop, Android launcher, and store contexts in `scripts/glitchpad_color_study.py`
- [x] T012 [US1] Emit exact matrix values, measured relationships, thresholds, and dispositions to `dist/.s015-color-study/measurements.json`
- [x] T013 [US1] Render `dist/.s015-color-study/comparison.svg` to the inspection PNG and inspect every candidate at full size
- [x] T014 [US1] Record geometry, measurement, visual tradeoff, and generated-output-boundary evidence in `specs/015-glitchpad-color-system/evidence.md`

**Checkpoint**: The owner has one complete, fair, source-safe comparison and a grounded recommendation.

---

## Phase 4: User Story 2 - Approve one explicit color-role system (Priority: P1)

**Goal**: Obtain an explicit owner disposition before production identity changes.

**Independent Test**: The decision record names approval, bounded adjustment, or rejection and contains every role needed to determine the next action.

- [x] T015 [US2] Present the comparison, recommendation, exact role matrices, measurements, and tradeoffs, then halt for owner input
- [x] T016 [US2] Record the owner disposition and rationale in `specs/015-glitchpad-color-system/evidence.md`
- [x] T017 [US2] If adjusted, regenerate the bounded comparison through `scripts/glitchpad_color_study.py` and return to T015
- [x] T017A [US2] Present Revision 2 with the mandatory safe square composition and halt for owner input
- [x] T017B [US2] Record and render the bounded A-dark plus B-light Revision 3 proposal, then halt for explicit approval

**Checkpoint**: Only an `approved` disposition unlocks production source work.

---

## Phase 5: User Story 3 - Ship the approved identity consistently (Priority: P2)

**Goal**: Promote only the approved matrix through source, shared generation, guidance, and every applicable output family.

**Independent Test**: Rebuild all production kits and compare every Glitchpad identity output with the approved role matrix while protected geometry hashes remain unchanged.

- [x] T018 [US3] Add failing optional source-owned wordmark-role and identity-matrix validation tests in `skill/templates/test_brand_contract.py`
- [x] T019 [US3] Add failing full, light, reduced, wordmark, lockup, monochrome, and platform-output tests in `skill/templates/test_pipeline.py`, retaining the existing platform occupancy suite in `skill/templates/test_iconkit.py`
- [x] T020 [US3] Encode the approved permanent-square composition, role matrix, and revised prohibitions in `brands/glitchpad/brand.json`
- [x] T021 [US3] Add proportional optional shared schema and validation support in `skill/references/canon.schema.json` and `skill/templates/brand_contract.py` if required
- [x] T022 [US3] Generate the approved permanent square, safely inset protected page, wordmark, and lockup roles through shared behavior in `skill/templates/gen_logo.py` without slug conditions
- [x] T023 [US3] Update Glitchpad guide, assumption, palette, measured, and source rationale records in `brands/glitchpad/brand.json`
- [x] T024 [US3] Rebuild and classify all full, light, reduced, monochrome, desktop, Android, web, Apple, Windows, guideline, specimen, registry, and site dispositions in `specs/015-glitchpad-color-system/evidence.md`
- [x] T025 [US3] Reconfirm protected path and lockup-geometry fingerprints in `specs/015-glitchpad-color-system/evidence.md`

**Checkpoint**: The approved identity is consistent, generated from source, and geometry-preserving across all delivery contexts.

---

## Phase 6: Polish, Verification, and Publication

**Purpose**: Complete repository gates, documentation, review, and owner merge handoff.

- [x] T026 Update Unreleased feature and dated identity-decision entries in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [x] T027 Run the focused study, brand-contract, generator, icon, pipeline, and site checks from `specs/015-glitchpad-color-system/quickstart.md`
- [x] T028 Run the complete five-kit, glyph, release, site, browser, accessibility, Markdown, encoding, mojibake, and repository-hygiene gate
- [x] T029 Complete final outcomes, commands, and output dispositions in `specs/015-glitchpad-color-system/evidence.md`
- [x] T030 Commit, push, and open the official pull request with `Fixes #146` after explicit publication authorization
- [x] T031 Process every authorized CI and review disposition, applying and verifying warranted corrections
- [x] T032 Confirm all required checks are green and all review threads are resolved, then halt before merge

---

## Dependencies and Execution Order

### Phase dependencies

- Phase 1 establishes the source boundary and fingerprints.
- Phase 2 depends on Phase 1 and blocks comparison generation.
- User Story 1 depends on Phase 2 and produces the decision evidence.
- User Story 2 depends on User Story 1 and is a mandatory human identity gate.
- User Story 3 depends on an approved User Story 2 disposition.
- Phase 6 depends on the approved implementation and complete output classification.

### Parallel opportunities

- T003 can run while T001 and T002 establish branch-local state.
- After T006, contrast observation work in T007 and mutation-boundary coverage in T008 concern separate assertions.
- Post-approval contract tests can be prepared together, but production implementation remains sequential through source, shared behavior, and generated evidence.

## Implementation Strategy

1. Preserve the baseline and formalize the candidate contract.
2. Build the deterministic comparison under test-first discipline.
3. Inspect and present the complete decision evidence.
4. Halt for owner approval before any production identity mutation.
5. Implement only the approved matrix, rebuild everything, and complete publication gates.

## Notes

- The custom identity checklist remains reviewer-owned; implementation never changes its markers.
- Generated comparison output is exploratory and ignored.
- Approval of a color direction does not authorize geometry, typography, texture, or unrelated-brand changes.
