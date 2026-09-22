# Tasks: Compact egui Desktop Density

**Input**: Design documents from `specs/044-compact-egui-density/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/native-density.md`, `quickstart.md`

**Tests**: Required by the feature specification and autopilot TDD discipline. Add each regression before its implementation and record the expected initial failure.

**Organization**: Tasks are grouped by user story so compact desktop controls, dense log rows, and preserved conservative targets remain independently traceable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches a different file and has no incomplete dependency.
- **[Story]**: Maps a task to the user story in `spec.md`.
- Every task includes an exact repository path.

## Phase 1: Setup

**Purpose**: Establish the regression baseline and exact contract identity.

- [x] T001 Confirm branch, clean baseline, issue #239, active feature directory, current 44-point style assignment, and existing test results; record them in `specs/044-compact-egui-density/evidence.md`
- [x] T002 [P] Confirm the version-policy classification and exact adapter/compiler compatibility boundary in `skill/references/version-policy.json` and record the decision in `specs/044-compact-egui-density/evidence.md`
- [x] T003 [P] Validate specification, plan, contract, quickstart, checklist, and Markdown format with `scripts/check_markdown.py`; record results in `specs/044-compact-egui-density/evidence.md`

---

## Phase 2: Foundational Regression Harness

**Purpose**: Add failing tests that expose the unconditional 44-point desktop target before production code changes.

- [x] T004 Add failing Python assertions for adapter 1.0.1 identity and capability-aware generated source in `skill/templates/test_egui_adapter.py`
- [x] T005 Add failing generated Cargo tests for comfortable and compact fine-pointer height, conservative input profiles, text-scale growth, coherent padding, and compact row spacing in `skill/templates/gen_egui.py`
- [x] T006 Run `skill/templates/test_egui_adapter.py`, confirm the new assertions fail for the expected oversized-control and version reasons, and record the failure in `specs/044-compact-egui-density/evidence.md`

**Checkpoint**: The regression is reproducible in deterministic generator and rendered native evidence.

---

## Phase 3: User Story 1 - Use compact desktop controls (Priority: P1) MVP

**Goal**: Make ordinary fine-pointer desktop controls compact and consistently padded without changing public adapter signatures.

**Independent Test**: Generated comfortable and compact fine-pointer styles satisfy the 28-point and 24-point caps, share one padding model, and grow only when scaled text requires it.

- [x] T007 [US1] Implement derived fine-pointer control height, restrained item spacing and button padding, and text-scale-aware minimum height in `skill/templates/gen_egui.py`
- [x] T008 [US1] Make `apply_style` use the fine-pointer default while preserving theme, focus, naming, and invalid-transform behavior in `skill/templates/gen_egui.py`
- [x] T009 [US1] Run the focused Python and generated Cargo evidence for fine-pointer controls and record exact measurements in `specs/044-compact-egui-density/evidence.md`

**Checkpoint**: User Story 1 independently restores compact desktop controls.

---

## Phase 4: User Story 2 - Read dense live logs (Priority: P1)

**Goal**: Keep repeated one-line rows visually contiguous instead of double-spaced.

**Independent Test**: The generated compact default exposes at most 2 points of vertical item spacing and does not force non-interactive labels to control height.

- [x] T010 [US2] Verify generated compact row spacing and consecutive label geometry through the Cargo regression in `skill/templates/gen_egui.py`
- [x] T011 [US2] Record the dense-row measurements and preserved resource-meter scope boundary in `specs/044-compact-egui-density/evidence.md`

**Checkpoint**: User Story 2 independently provides dense operational log rhythm.

---

## Phase 5: User Story 3 - Retain touch accessibility (Priority: P2)

**Goal**: Preserve 44-point interaction targets for every runtime that cannot prove fine-pointer-only input.

**Independent Test**: Coarse, mixed, unknown, and touch-capable profiles use at least 44 points in both densities while fine-pointer-only profiles use compact height.

- [x] T012 [US3] Implement capability-aware conservative target selection in `skill/templates/gen_egui.py`
- [x] T013 [US3] Exercise coarse, mixed, unknown, touch, and fine-pointer profiles plus invalid capability rejection in the generated Cargo suite in `skill/templates/gen_egui.py`
- [x] T014 [US3] Run the focused target-retention evidence and record every profile result in `specs/044-compact-egui-density/evidence.md`

**Checkpoint**: User Story 3 independently preserves conservative interaction accessibility.

---

## Phase 6: Versioning, Migration, and Full Verification

**Purpose**: Publish the corrected adapter identity, verify production kits, and prepare the PR.

- [x] T015 Bump the generated egui adapter to 1.0.1 and BrandBuilder to 2.0.1 in `skill/templates/gen_egui.py`, `skill/templates/egui-Cargo.lock`, `skill/SKILL.md`, and release metadata, update compiler-major-2 compatibility in `skill/references/version-policy.json`, and align exact expectations in focused and release-contract tests
- [x] T016 [P] Add the S044 correction and consumer regeneration note to `CHANGELOG.md` and `skill/CHANGELOG.md`
- [x] T017 Re-run cross-artifact analysis and reconcile `specs/044-compact-egui-density/spec.md`, `plan.md`, `tasks.md`, contract, data model, quickstart, and implementation
- [x] T018 Run focused generator/native tests, Python 3.8 compatibility tests, the full Python contract suite, Markdown audit, capability probe, all-kit build, release certification, generated-agent diff, site lint/build/test, and publication audit; record exact results in `specs/044-compact-egui-density/evidence.md`
- [x] T019 Run repository hygiene, generated-artifact exclusion, UTF-8 without BOM, LF, mojibake, and `git diff --check` audits; record results in `specs/044-compact-egui-density/evidence.md`
- [ ] T020 Mark completed tasks, commit with `fix(S044): restore compact egui density`, push `codex/044-compact-egui-density`, open a PR linked to #239, process exactly one Codex review round, and update `specs/044-compact-egui-density/evidence.md` with final CI status

---

## Dependencies and Execution Order

- Setup starts immediately.
- The failing regression harness depends on Setup and blocks implementation.
- US1 establishes the shared style metrics consumed by US2 and US3.
- US2 validates row density after US1 style metrics exist.
- US3 adds conservative capability selection after the fine-pointer path is stable.
- Versioning and full verification depend on all three stories.

## Parallel Opportunities

- T002 and T003 can run in parallel after T001.
- T016 can run while focused implementation verification completes.
- No production-code tasks are marked parallel because they edit the same generator file.

## Implementation Strategy

1. Reproduce the version and oversized-control failures with T004-T006.
2. Deliver the compact fine-pointer MVP through T007-T009.
3. Prove dense log rhythm through T010-T011.
4. Restore the conservative capability boundary through T012-T014.
5. Publish the patch identity and run the complete repository gate through T015-T020.

## Notes

- The correction deliberately replaces S039's unconditional visible 44-point desktop sizing because that logic conflated coarse-input accessibility with presentation density.
- Security and tenancy surfaces are absent: the generator processes local public brand contracts and creates no authentication, private data, tenant state, or network endpoint. Fail-closed input validation and exact artifact provenance are the applicable safety gates.
- Never commit generated `dist/`, native crates, site exports, release archives, PDFs, raster exports, or registries.
