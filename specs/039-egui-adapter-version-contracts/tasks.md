# Tasks: Native egui Adapter and Versioned Contracts

**Input**: Design documents from `specs/039-egui-adapter-version-contracts/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and reviewer-owned checklist

**Tests**: Required by the specification. Test tasks precede implementation and must demonstrate the intended red state.

## Phase 1: Setup and primary-source evidence

- [x] T001 Record exact egui and egui_kittest versions, MSRV, APIs, and primary-source evidence in `specs/039-egui-adapter-version-contracts/research.md`
- [x] T002 Confirm `.specify/feature.json`, branch naming, source/output boundaries, and the S039 baseline in `specs/039-egui-adapter-version-contracts/plan.md`
- [x] T003 Complete the native and version-contract reviewer checklist in `specs/039-egui-adapter-version-contracts/checklists/native-version-contract.md`

---

## Phase 2: Foundational failing contracts

- [x] T004 [P] Add failing independent-domain, bump-rule, compatibility, lifecycle, pinning, and recovery tests in `skill/templates/test_interface_contract.py`
- [x] T005 [P] Add failing deterministic crate, recipe coverage, native-source, support-state, and tamper tests in `skill/templates/test_egui_adapter.py`
- [x] T006 [P] Add failing native manifest and all-brand pipeline requirements in `skill/templates/test_pipeline.py`
- [x] T007 [P] Add failing archive authority, version, compatibility, and provenance requirements in `scripts/test_package_release.py` and `scripts/test_release_contract.py`

**Checkpoint**: New tests fail for absent native and version-policy contracts, not for harness errors.

---

## Phase 3: User Story 1 - Consume a native egui adapter (Priority: P1)

**Goal**: Generate an idiomatic Rust crate with semantic tokens, units, density, runtime capabilities, and bounded egui helpers.

**Independent Test**: Generate one temporary production-brand kit twice, compare bytes, inspect the complete support matrix, compile the crate, and run its generated tests.

- [x] T008 [US1] Author the independent domain and compatibility policy in `skill/references/version-policy.json`
- [x] T009 [US1] Implement policy validation and exact combination checks in `skill/templates/interface_contract.py`
- [x] T010 [US1] Implement deterministic Rust crate and manifest generation in `skill/templates/gen_egui.py`
- [x] T011 [US1] Generate typed theme tokens, logical-unit conversion, density transforms, and observed runtime capability types in `skill/templates/gen_egui.py`
- [x] T012 [US1] Generate idiomatic egui helpers and explicit support records for all shared recipes in `skill/templates/gen_egui.py`
- [x] T013 [US1] Add native generation to `skill/templates/build_kit.py` before enforcement and document the entry point in `skill/SKILL.md`

**Checkpoint**: The generated crate is deterministic, egui-native, complete for every recipe record, and contains no React or CSS runtime model.

---

## Phase 4: User Story 2 - Verify native interaction and rendered state (Priority: P1)

**Goal**: Prove input, focus, selection, error, density, scaling, and unsupported-state behavior using real egui frames.

**Independent Test**: Run `cargo test --locked` against a generated temporary crate and verify all required evidence identifiers.

- [x] T014 [US2] Generate `egui_kittest` integration tests for button input, focusable controls, selected controls, invalid fields, densities, and pixels-per-point scaling in `skill/templates/gen_egui.py`
- [x] T015 [US2] Add Python orchestration that generates a temporary crate, creates its lockfile, and runs Cargo headlessly in `skill/templates/test_egui_adapter.py`
- [x] T016 [US2] Add native adapter validation and support-matrix verification to `skill/templates/verify.py`
- [x] T017 [US2] Run generated Rust evidence in CI and the full-kit build without committing Cargo or target output in `.github/workflows/build.yml`

**Checkpoint**: Native claims are backed by compiled, rendered egui evidence and unsupported behavior remains explicit.

---

## Phase 5: User Story 3 - Pin and recover independent contracts (Priority: P2)

**Goal**: Make every consumer handoff and release archive self-describe exact independent versions, compatibility, provenance, and recovery.

**Independent Test**: Build, verify, archive, and re-verify one kit, then mutate each native or policy version/path/checksum and observe actionable failure.

- [x] T018 [US3] Upgrade `skill/references/consumer-contract.schema.json` and `skill/templates/interface_contract.py` to schema v3 with egui version, policy, native authority, and compatibility records
- [x] T019 [US3] Copy version policy through enforcement and add native/policy files to checksummed provenance and deterministic recovery in `skill/templates/interface_contract.py`
- [x] T020 [US3] Extend manifest and release certification in `skill/templates/build_kit.py`, `scripts/release_contract.py`, `scripts/test_package_release.py`, and `scripts/test_release_contract.py`
- [x] T021 [US3] Add exact pin, compatibility, publication, adoption, and recovery guidance to generated implementation instructions and `skill/SKILL.md`
- [x] T022 [US3] Synchronize `skill/AGENTS.md`, root and skill changelogs, and all S039 Spec Kit artifacts

**Checkpoint**: Brand and deployment cadence are independent, every version is exact, and an old handoff remains recoverable after later releases.

---

## Phase 6: Full verification and pull request

- [x] T023 Run Python compile, focused adapter/interface/pipeline/release suites, generated Cargo tests, and Markdown validation
- [x] T024 Run the full all-brand build and confirm zero `verify.py` and glyph failures without committing `dist/`
- [x] T025 Run site lint/build/test, publication audit, instruction synchronization, mojibake scan, LF/BOM scan, `git diff --check`, and tracked-generated-artifact checks
- [x] T026 Run Spec Kit analysis, review the complete diff for identity isolation, security, accessibility, version integrity, and scope alignment, then resolve every finding
- [ ] T027 Commit with a Conventional Commit subject including S039, push `codex/039-egui-adapter-version-contracts`, and open an official PR closing #216 and #218
- [ ] T028 Wait for CI and every external review, address each comment, and trigger at most one authorized `@Codex` second review round
- [ ] T029 Confirm all checks and both review rounds are satisfied, then request the user's final review and merge ritual without merging

## Dependencies and execution order

- Phase 2 tests establish the red baseline before implementation.
- Version policy validation precedes native generation because the adapter manifest records compatibility.
- User Story 1 generates the crate before User Story 2 compiles and exercises it.
- User Story 3 integrates stable native paths into consumer and release contracts.
- Full verification follows all implementation and documentation work.

## Notes

- The custom checklist is reviewer-owned and has been evaluated independently from implementation.
- Real cross-host golden fixtures remain in #217. S039 uses the official egui harness but does not claim Tauri, Wails, or mobile host certification.
- Downstream pilot issues remain outside this repository and require separate authorization.
- Generated `dist/`, Cargo locks, Cargo targets, release archives, site exports, and native render output are verification artifacts and must remain untracked.
