# Tasks: Native Host Icon and State Conformance

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [native-role contract](contracts/native-role-contract.md)

## Phase 1: Setup

- [x] T001 Record clean branch, issue scope, and constitution constraints in `specs/048-native-host-conformance/spec.md` and `plan.md`.
- [x] T002 [P] Research official host roles and consumer source paths in `specs/048-native-host-conformance/research.md`.

## Phase 2: Foundation

- [x] T003 Record exact ESO ICO and Glitchpad APK resource/hash attribution in `specs/048-native-host-conformance/evidence.md`.
- [x] T004 Define the role matrix and approved composition policies in `skill/references/04-toolchain.md` and `specs/048-native-host-conformance/contracts/native-role-contract.md`.

## Phase 3: User Story 1 - Read native status and controls (P1)

**Goal**: Status and native interaction states have explicit, measurable colors.

**Independent test**: Generated egui state fixture passes light/dark enabled, disabled, hover, focus, and status checks; consumer call-site attribution is recorded.

- [x] T005 [US1] Add failing generated egui state and contrast regressions in `skill/templates/test_interface_contract.py`.
- [x] T006 [US1] Correct generated state styling and guidance in `skill/templates/gen_egui.py` and `skill/references/` without changing public adapter symbols.
- [x] T007 [US1] Record ESO consumer-local `ui.strong` finding and required repin/call-site action in `specs/048-native-host-conformance/evidence.md`.

## Phase 4: User Story 2 - Recognize applications on native hosts (P1)

**Goal**: Correct Windows and Android role composition without changing source geometry.

**Independent test**: Decode ICO and adaptive resources, composite small frames under target themes/masks, and assert no unintended square or wedge.

- [x] T008 [US2] Add failing Windows and Android role/negative fixtures in `skill/templates/test_pipeline.py`.
- [x] T009 [US2] Validate role-specific profiles in `skill/templates/brand_contract.py`, deriving Glitchpad's mask background from its approved frame role and Win32 transparency from the absence of an approved enclosure without modifying ESO's Gate 1 binding.
- [x] T010 [US2] Generate taskbar and launcher/listing compositions in `skill/templates/iconkit.py`.
- [x] T011 [US2] Add alpha, boundary, safe-zone, three-mask, and small-size assertions in `skill/templates/verify.py`.
- [x] T012 [US2] Update generated Windows and Android integration guidance in `skill/templates/iconkit.py`.

## Phase 5: User Story 3 - Trust role qualification across kits (P1)

**Goal**: All generated icon roles have source-linked qualification.

**Independent test**: Every platform role appears in the matrix and manifest; `any` and `maskable` are separate, representative host composites and negative fixtures pass.

- [x] T013 [US3] Add failing PWA purpose/mask and cross-platform role inventory tests in `skill/templates/test_pipeline.py`.
- [x] T014 [US3] Generate distinct PWA role assets and manifest entries in `skill/templates/iconkit.py`.
- [x] T015 [US3] Extend platform-role verification for PWA, Android, and Windows while retaining Apple checks in `skill/templates/verify.py`.
- [x] T016 [US3] Document source-linked role policies and host evidence limits in `skill/references/04-toolchain.md`.

## Phase 6: Cross-Cutting Completion

- [x] T017 Advance compiler, adapter, and changed brand candidate versions and migration impact in `skill/SKILL.md`, `skill/references/`, `brands/glitchpad/brand.json`, `scripts/release_contract.py`, `site/package.json`, and `CHANGELOG.md`.
- [x] T018 Run focused tests and full documented production, glyph, site, release, encoding, and hygiene gates; record outcomes in `specs/048-native-host-conformance/evidence.md`.
- [ ] T019 Commit, push, open official issue-linked PR, process no more than two Codex review rounds, resolve comments, and wait for green CI; record review ledger in `specs/048-native-host-conformance/evidence.md`.

## Dependencies and Execution Order

T003-T004 establish attribution and role policy. US1 can proceed independently after T004. US2 and US3 both touch icon generation and verification, so implement them sequentially even though their tests can be drafted separately. Version and complete validation follow all three stories. PR review follows local gates.

## Parallel Opportunity

Read-only official platform research and read-only consumer resource attribution may run alongside planning. Generator and verifier edits should remain serialized to avoid conflicting changes.

## Implementation Strategy

Deliver a complete US1 check first, then Windows/Android US2, then cross-platform US3. Do not call a BrandBuilder source change an installed consumer fix. The final owner checkpoint is the PR, not an automatic merge.

## Phase 7: Convergence

- [x] T020 Add a negative Win32 taskbar plate fixture that proves the verifier rejects an opaque frame per FR-009 (partial).
- [x] T021 Name the Apple touch icon's iOS home-screen role, alpha policy, and host check explicitly in the native role matrix per FR-008 (partial).
