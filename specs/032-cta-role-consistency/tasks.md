# Tasks: CTA Role Consistency

**Input**: Design documents from `specs/032-cta-role-consistency/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/cta-guide-contract.md`, `quickstart.md`

**Tests**: Required by FR-013 and the repository constitution. Every behavior change begins with a failing regression.

**Organization**: Tasks are grouped by independently testable user story after a shared measured-token foundation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes a different file and does not depend on an incomplete task.
- **[Story]**: Maps the task to the corresponding user story in `spec.md`.

## Phase 1: Setup and Baseline

**Purpose**: Record the current failure and protect immutable source boundaries.

- [X] T001 Record the current CTA, PDF text, PDF layout, generated-guide, and source-hash baseline in `specs/032-cta-role-consistency/evidence.md`
- [X] T002 Verify repository ignore coverage for Python, Node, generated `dist/`, `site/out/`, temporary render output, and machine-local `.specify/feature.json` in `.gitignore` and `.specify/.gitignore`

---

## Phase 2: Foundational Governed CTA Pair

**Purpose**: Publish and verify one measured CTA fill/foreground pair before either guide consumes it.

**Critical**: User-story implementation depends on this phase.

- [X] T003 Add failing regression coverage for `brand-cta` and `brand-cta-foreground` projection, source derivation, light/dark parity, cross-brand isolation, role separation, and AA failure behavior in `skill/templates/test_pipeline.py`
- [X] T004 Run the focused token regressions and capture the expected red result in `specs/032-cta-role-consistency/evidence.md`
- [X] T005 Implement measured `brand-cta-foreground` projection from `semantic_colors.action` in `skill/templates/gen_nextjs.py`
- [X] T006 Extend the generated-global pair gate to require WCAG 2.1 AA for `brand-cta-foreground` on `brand-cta` in `skill/templates/verify.py`
- [X] T007 Run the focused token regressions to green and record the result in `specs/032-cta-role-consistency/evidence.md`

**Checkpoint**: The generated token contract distinguishes CTA action from identity primary and fails closed below AA.

---

## Phase 3: User Story 1 - Apply the Approved CTA Color (Priority: P1)

**Goal**: Every portable-guide primary button uses the measured red CTA pair with accessible interaction states.

**Independent Test**: Generate the portable guide, inspect all three primary specimens in a browser, and measure default, hover, active, focus-visible, and reduced-motion behavior in both theme wells.

### Tests for User Story 1

- [X] T008 [US1] Add failing generator regressions for all portable-guide primary specimens and their non-color interaction/focus contract in `skill/templates/test_pipeline.py`
- [X] T009 [P] [US1] Add failing computed-style and accessibility checks for the generated I Heart PR Tours portable guide in `site/scripts/verify-site.mjs`
- [X] T010 [US1] Run the focused portable-guide regressions and record the expected red result in `specs/032-cta-role-consistency/evidence.md`

### Implementation for User Story 1

- [X] T011 [US1] Bind portable-guide primary buttons and their hover, active, focus-visible, and reduced-motion states to the CTA contract in `skill/templates/gen_guidelines.py`
- [X] T012 [US1] Update I Heart PR Tours sharp-edge and palette guidance to name `#C5342C` and its bounded CTA role in `brands/i-heart-pr-tours/brand.json`
- [X] T013 [US1] Run portable-guide generator and browser regressions to green and record computed evidence in `specs/032-cta-role-consistency/evidence.md`
- [X] T029 [US1] Add and run failing regressions for the live-site secondary red-outline contract across all three portable specimens and the PDF in `skill/templates/test_pipeline.py`
- [X] T030 [US1] Add the measured surface-aware outline foreground token and verifier pairing in `skill/templates/gen_nextjs.py` and `skill/templates/verify.py`
- [X] T031 [US1] Apply the red-outline default, filled-red hover, active, focus-visible, and reduced-motion contract to secondary portable buttons in `skill/templates/gen_guidelines.py`
- [X] T032 [US1] Add the labeled secondary red-outline specimen to PDF CTA guidance in `skill/templates/gen_guide_pdf.py`
- [X] T033 [US1] Extend computed browser verification to all secondary specimens, rebuild both guide formats, and present the revised visual review before commit in `site/scripts/verify-site.mjs` and `specs/032-cta-role-consistency/evidence.md`

**Checkpoint**: All portable-guide CTA specimens use the approved red without changing identity, link, focus, chart, emphasis, or destructive semantics.

---

## Phase 4: User Story 2 - Understand CTA Semantics in the PDF Guide (Priority: P1)

**Goal**: The PDF palette, semantic table, and state guidance completely define the CTA role and distinguish it from adjacent roles.

**Independent Test**: Generate the PDF HTML/PDF, extract its text, and inspect page four for the labeled swatch, semantic row, accessible foreground, state specimens, and role exclusions.

### Tests for User Story 2

- [X] T014 [US2] Add failing PDF generator regressions for CTA palette presence, exact value, semantic role, legal foreground, state guidance, role exclusions, and portable/PDF agreement in `skill/templates/test_pipeline.py`
- [X] T015 [US2] Run the focused PDF regressions and record the expected red result in `specs/032-cta-role-consistency/evidence.md`

### Implementation for User Story 2

- [X] T016 [US2] Add the CTA swatch, semantic-use row, state specimens, and explicit role boundaries to `skill/templates/gen_guide_pdf.py`
- [X] T017 [US2] Run focused PDF regressions to green, rebuild I Heart PR Tours, extract PDF text, and record results in `specs/032-cta-role-consistency/evidence.md`
- [X] T018 [US2] Render and inspect every regenerated PDF page for clipping, overlap, readability, corruption, and pagination in `dist/i-heart-pr-tours/qc/`

**Checkpoint**: PDF and portable HTML agree exactly on the CTA value, foreground, purpose, and state behavior.

---

## Phase 5: User Story 3 - Read Consistent American English (Priority: P2)

**Goal**: Reader-facing generated guide prose uses American English while stable internal compatibility identifiers remain unchanged.

**Independent Test**: Strip markup from generated portable/PDF HTML, extract PDF text, and confirm the known British variants are absent as reader-facing standalone words.

### Tests for User Story 3

- [X] T019 [US3] Add failing reader-text regressions for the identified British spellings and explicit compatibility-boundary assertions in `skill/templates/test_pipeline.py`
- [X] T020 [US3] Run the focused language regressions and record the expected red result in `specs/032-cta-role-consistency/evidence.md`

### Implementation for User Story 3

- [X] T021 [P] [US3] Normalize reader-facing portable-guide prose to American English in `skill/templates/gen_guidelines.py`
- [X] T022 [P] [US3] Normalize reader-facing PDF-guide prose to American English in `skill/templates/gen_guide_pdf.py`
- [X] T023 [US3] Run language regressions to green and record the text-extraction evidence in `specs/032-cta-role-consistency/evidence.md`

**Checkpoint**: Generated reader text is consistent while `colourway` schema keys and compatibility function names remain unchanged.

---

## Phase 6: Polish and Cross-Cutting Verification

**Purpose**: Prove all production kits, artifacts, publication output, and documentation remain shippable.

- [X] T024 Update the Unreleased feature and dated decision entries for S032 in `CHANGELOG.md`
- [X] T025 Run the complete Python compatibility, generator, identity, icon, glyph, publication, release, and Markdown suites from `.github/workflows/build.yml` and record results in `specs/032-cta-role-consistency/evidence.md`
- [X] T026 Build all eight production kits with the approved identity proofs, require zero `verify.py` problems and zero `validate_glyph.py` failures, and record results in `specs/032-cta-role-consistency/evidence.md`
- [X] T027 Run release certification, generated-agent diff, site lint/build/test, and publication artifact audit, then record results in `specs/032-cta-role-consistency/evidence.md`
- [X] T028 Audit UTF-8/LF, mojibake, generated-output exclusion, identity source hashes, task completion, and `git diff --check`, then finalize `specs/032-cta-role-consistency/evidence.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- Phase 1 has no dependencies.
- Phase 2 depends on the baseline and blocks all user stories.
- Phase 3 depends on the measured CTA token pair.
- Phase 4 depends on the measured CTA token pair and may consume the source guidance updated in Phase 3.
- Phase 5 depends on the guide generators being functionally complete so language tests inspect final reader text.
- Phase 6 depends on all user stories.

### User Story Dependencies

- **US1**: Depends only on Phase 2 and delivers the portable-guide correction.
- **US2**: Depends only on Phase 2 for token semantics, but follows US1 to validate final cross-artifact agreement.
- **US3**: Can be tested independently, then applies after US1 and US2 to avoid conflicting edits in shared guide files.

### Parallel Opportunities

- T009 can be authored while T008 is prepared because it changes a separate JavaScript verifier.
- T021 and T022 can be applied independently after T019 and T020 because they affect separate generator files.
- Full Python and site checks remain sequential where they share generated output.

## Implementation Strategy

### MVP First

1. Complete Phases 1 and 2.
2. Complete US1 and prove every portable primary CTA is corrected.
3. Complete US2 so the PDF teaches the same role in the same slice.
4. Complete US3 and the full publication gate.

### TDD Discipline

- Add and run failing tests before each implementation group.
- Preserve failure output in `evidence.md`.
- Do not weaken existing assertions, identity checks, accessibility floors, security checks, or publication gates.
- Mark each task `[X]` only after its work and evidence are complete.
