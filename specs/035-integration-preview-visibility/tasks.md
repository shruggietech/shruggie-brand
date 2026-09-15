# Tasks: Integration Preview Visibility

**Input**: Design documents from `/specs/035-integration-preview-visibility/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/integration-preview-contract.md, quickstart.md

**Tests**: Required by issue #202, the feature specification, and the autopilot TDD discipline. Every story begins with a failing regression before implementation.

**Organization**: Tasks are grouped by independently testable user story, followed by cross-cutting production verification and local commit.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it affects a different file or read-only evidence.
- **[Story]**: Maps the task to a user story from `spec.md`.
- Every task includes an exact repository path.

## Phase 1: Setup and Baseline

**Purpose**: Bind the issue, branch, source boundary, existing behavior, and local validation environment before tests change.

- [x] T001 Record issue #202, branch `codex/035-integration-preview-visibility`, clean-worktree baseline, and generator boundary in `specs/035-integration-preview-visibility/evidence.md`
- [x] T002 Verify `.gitignore` and existing tool configuration exclude `dist/`, `site/out/`, release artifacts, temporary fixtures, test results, dependency trees, and `.specify/feature.json`; record the result in `specs/035-integration-preview-visibility/evidence.md`
- [x] T003 Run the pre-change I Heart PR Tours focused build with the pinned proof renderer, capture zero-gate results and the failing preview contrast semantics in `specs/035-integration-preview-visibility/evidence.md`

---

## Phase 2: Foundational Regression Harness

**Purpose**: Establish reusable temporary fixture and browser measurement coverage before either user-facing correction.

- [x] T004 Add isolated PNG, metadata, XML, ICO, ICNS, mixed-group, byte-hash, deterministic-output, and escaping fixture helpers in `skill/templates/test_pipeline.py`
- [x] T005 [P] Add reusable portable preview image, text-contrast, containment, exclusivity, overflow, zoom, and direct-file audit helpers in `site/scripts/verify-site.mjs`
- [x] T006 Run the focused pre-implementation unit and generated browser checks, confirm the expected wrong-well, missing semantic metadata, generic fallback, and dark-text failures, and record them in `specs/035-integration-preview-visibility/evidence.md`

**Checkpoint**: The shared harness proves the existing implementation cannot satisfy the visual or nonvisual contract.

---

## Phase 3: User Story 1 - Recognize every visual integration asset (Priority: P1) MVP

**Goal**: Select an accessible well from proven appearance or meaningful visible output and embed the exact measured preview bytes.

**Independent Test**: Transparent dark, declared black, declared white, and full-color visual fixtures choose a light or dark well whose recorded significant-pixel contrast is at least 3:1; fully transparent visuals fail clearly; SVG-only visuals are measured without changing their embedded bytes; source hashes do not change.

### Tests for User Story 1

- [x] T007 [US1] Add failing visual surface-selection, exact-preview-byte, 3:1, fully-transparent failure, deterministic-output, and no-filter assertions in `skill/templates/test_pipeline.py`

### Implementation for User Story 1

- [x] T008 [US1] Implement bounded read-only meaningful-pixel sampling for PNG and SVG, WCAG contrast scoring, strongest-well selection, and fail-closed empty-visual handling in `skill/templates/gen_guidelines.py`
- [x] T009 [US1] Use the shared presentation resolver for hosted portal projection and portable catalog generation with visual data attributes in `skill/templates/gen_guidelines.py`
- [x] T010 [US1] Run focused visual tests and record selected wells, scores, deterministic output, and byte preservation in `specs/035-integration-preview-visibility/evidence.md`

**Checkpoint**: Every previewable group has a justified and testable light or dark surface without asset mutation.

---

## Phase 4: User Story 2 - Understand nonvisual integration resources (Priority: P1)

**Goal**: Replace false or invisible image placeholders with explicit format-aware nonvisual resource presentations.

**Independent Test**: JSON, XML, ICO, and ICNS fixtures render no image, identify themselves as nonvisual resources with format and role, use a 4.5:1 text pair, preserve embedded-size and delivery metadata, and remain represented exactly once in mixed groups.

### Tests for User Story 2

- [x] T011 [US2] Add failing metadata/container semantics, mixed-group inventory, accessible foreground, escaped-label, and destination-integrity assertions in `skill/templates/test_pipeline.py`

### Implementation for User Story 2

- [x] T012 [US2] Implement format-aware nonvisual labels and dedicated nonvisual portable markup in `skill/templates/gen_guidelines.py`
- [x] T013 [US2] Pin explicit AA foreground/background pairs for dark, light, and nonvisual wells and style readable resource content in `skill/templates/gen_guidelines.py`
- [x] T014 [US2] Run focused nonvisual and safety regressions and record exact format, inventory, and contrast results in `specs/035-integration-preview-visibility/evidence.md`

**Checkpoint**: Every resource card communicates whether it is visual or nonvisual, with readable text and complete delivery metadata.

---

## Phase 5: User Story 3 - Trust regenerated portable guidance (Priority: P2)

**Goal**: Prove the systemic repair in the generated I Heart PR Tours portable file across viewport, zoom, surface, accessibility, portability, and preservation boundaries.

**Independent Test**: The served and direct-file portable guide pass audits at 1280 and 360 CSS pixels plus 200 percent zoom, exercise light, dark, and nonvisual wells, retain every delivery byte, and complete with zero `verify.py` or `validate_glyph.py` failures.

### Tests for User Story 3

- [x] T015 [P] [US3] Add failing all-card portable browser assertions and screenshot coverage for desktop, narrow, 200 percent zoom, both visual wells, nonvisual wells, axe, containment, and reflow in `site/scripts/verify-site.mjs`
- [x] T016 [P] [US3] Add source and generated-delivery hash preservation assertions for I Heart PR Tours in `skill/templates/test_pipeline.py`

### Implementation and Verification for User Story 3

- [x] T017 [US3] Regenerate I Heart PR Tours with `scripts/build_all.py`, require zero verifier problems and zero glyph failures, and record the generated presentation inventory in `specs/035-integration-preview-visibility/evidence.md`
- [x] T018 [US3] Build the site, run the served and direct-file browser matrix, visually inspect the generated screenshots, and record measurements in `specs/035-integration-preview-visibility/evidence.md`

**Checkpoint**: The corrected portable output is accessible, responsive, portable, and identity-preserving.

---

## Phase 6: Polish and Cross-Cutting Verification

**Purpose**: Reconcile all artifacts, run every authoritative gate, and prepare the local pre-push halt.

- [x] T019 [P] Add the S035 issue #202 correction to the Unreleased Fixed section of `CHANGELOG.md`
- [x] T020 Re-run cross-artifact analysis and reconcile `specs/035-integration-preview-visibility/spec.md`, `plan.md`, `tasks.md`, contract, data model, quickstart, evidence, and implementation
- [x] T021 Run Python compile, discovery, publication, package, release-contract, preparation, identity, brand, icon, glyph, pipeline, Markdown, and probe suites and record exact results in `specs/035-integration-preview-visibility/evidence.md`
- [x] T022 Run the all-production-kit build with the approved proof root and exact renderer, require zero `verify.py` problems and zero `validate_glyph.py` failures for all eight kits, and record results in `specs/035-integration-preview-visibility/evidence.md`
- [x] T023 Run release certification, generated-agent diff, site lint/build/test, publication audit, and direct portable browser verification and record results in `specs/035-integration-preview-visibility/evidence.md`
- [x] T024 Run `git diff --check`, Markdown line policy, UTF-8 BOM/CR and mojibake scans, generated-artifact exclusion, asset-byte preservation review, and task completion review; update `specs/035-integration-preview-visibility/evidence.md` and mark every completed task `[x]` in `specs/035-integration-preview-visibility/tasks.md`
- [x] T025 Commit governed source, tests, changelog, evidence, and Spec Kit artifacts locally with subject `fix(S035): restore integration preview visibility`, then halt before `git push`

---

## Dependencies and Execution Order

### Phase Dependencies

- Setup and Baseline starts immediately.
- Foundational Regression Harness depends on the baseline and blocks implementation.
- User Story 1 depends on the unit fixture harness.
- User Story 2 depends on the same grouping fixture harness and follows User Story 1 because both modify `gen_guidelines.py` and `test_pipeline.py`.
- User Story 3 depends on both presentation behaviors and the browser harness.
- Polish depends on all user stories.

### User Story Dependencies

- **US1**: Independently testable measured visual-surface increment.
- **US2**: Independently testable nonvisual semantic increment, sharing the presentation resolver but not requiring browser acceptance.
- **US3**: End-to-end generated-output increment that depends on US1 and US2 behavior.

### Within Each User Story

- Add the story's test and observe the expected failure.
- Implement the smallest governed-template correction.
- Run the independent story gate and record evidence before continuing.
- Preserve all input and delivery bytes throughout.

### Parallel Opportunities

- T004 and T005 affect different test files and can proceed in parallel.
- T015 and T016 affect different files and can proceed in parallel.
- T019 can proceed after behavior is stable while verification artifacts are reconciled.

---

## Parallel Example: Foundational Harness

```text
Task: "Add temporary generator regression fixtures in skill/templates/test_pipeline.py"
Task: "Add portable browser measurement helpers in site/scripts/verify-site.mjs"
```

## Parallel Example: User Story 3

```text
Task: "Add generated browser matrix assertions in site/scripts/verify-site.mjs"
Task: "Add asset hash preservation assertions in skill/templates/test_pipeline.py"
```

---

## Implementation Strategy

### MVP First

1. Capture the current broken output and hashes.
2. Add failing visual selection fixtures.
3. Implement the shared read-only resolver and exact preview binding.
4. Run the visual contract independently before adding nonvisual semantics.

### Incremental Delivery

1. US1 restores visual icon visibility.
2. US2 restores readable metadata and container semantics.
3. US3 proves the combined fix in real generated portable output.
4. Full repository verification certifies the slice without generated or identity changes.

## Notes

- Custom checklist markers remain reviewer-owned and are intentionally not changed by implementation.
- The generator has no authentication, private data, runtime user input, or tenant boundary. Applicable security coverage is escaping, path and destination integrity, fail-closed malformed input, cross-kit isolation, and synthetic-fixture exclusion.
- Never commit generated `dist/`, `site/out/`, screenshots, PDFs, archives, registries, release files, dependencies, caches, or `.specify/feature.json`.
