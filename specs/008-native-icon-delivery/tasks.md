# Tasks: Native Icon Delivery and Favicon Integrity

**Input**: Design documents from `specs/008-native-icon-delivery/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

**Tests**: Required by the feature specification, constitution P4, and autopilot TDD discipline.

**Organization**: Tasks are grouped by independently testable user story and remain traceable to #106 and #110.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it targets different files and has no incomplete dependency
- **[Story]**: Maps the task to the corresponding user story in `spec.md`
- Every task names its implementation or evidence path

## Phase 1: Setup and Specification

**Purpose**: Establish the S008 branch, active feature state, specification, decisions, contracts, and reviewer gates.

- [x] T001 Create and activate `codex/008-native-icon-delivery` and set `.specify/feature.json` to `specs/008-native-icon-delivery`
- [x] T002 [P] Complete the validated feature specification and built-in quality checklist in `specs/008-native-icon-delivery/spec.md` and `specs/008-native-icon-delivery/checklists/requirements.md`
- [x] T003 [P] Record platform research and decisions in `specs/008-native-icon-delivery/research.md`
- [x] T004 [P] Define entities and state transitions in `specs/008-native-icon-delivery/data-model.md`
- [x] T005 [P] Define manifest, platform, and site contracts in `specs/008-native-icon-delivery/contracts/`
- [x] T006 [P] Complete the requirements integrity review in `specs/008-native-icon-delivery/checklists/integrity.md`
- [x] T007 Complete the technical plan and runnable validation guide in `specs/008-native-icon-delivery/plan.md` and `specs/008-native-icon-delivery/quickstart.md`

**Checkpoint**: Specification, clarification decisions, checklist, plan, and contracts are ready for cross-artifact analysis.

---

## Phase 2: Foundational Contract and Test Harness

**Purpose**: Add failing tests and shared contract primitives before generating any platform suite.

**Critical**: No user-story implementation begins until these tests fail for the missing S008 behavior and the common profile contract is defined.

- [x] T008 Add failing application-icon profile schema and validation cases to `skill/templates/test_brand_contract.py`
- [x] T009 Add failing safe-path, image-composition, PNG-metadata, native-container, and manifest helper tests to `skill/templates/test_iconkit.py`
- [x] T010 Add failing generation, platform-matrix, compatibility-alias, stale-output, and corruption cases to `skill/templates/test_pipeline.py`
- [x] T011 [P] Add failing generated-suite publication and no-fallback cases to `scripts/test_prepare_site.py`
- [x] T012 [P] Add failing emitted-site icon contract fixtures to `site/tests/site.test.mjs`
- [x] T013 Run the focused test files and record the expected pre-implementation failures in `specs/008-native-icon-delivery/evidence.md`
- [x] T014 Extend the optional `logo.application_icon` source contract in `skill/references/canon.schema.json`
- [x] T015 Implement effective icon-profile validation and fallback behavior in `skill/templates/brand_contract.py`
- [x] T016 Set the approved ShruggieTech icon background in `brands/shruggietech/brand.json`
- [x] T017 Create shared platform matrices, safe output clearing, source-owned domain-symbol preservation, image inspection, composition, native metadata, and manifest primitives in `skill/templates/iconkit.py`
- [x] T018 Run `skill/templates/test_brand_contract.py` and `skill/templates/test_iconkit.py` to validate the foundation

**Checkpoint**: Canonical profile resolution and platform-independent icon helpers are tested and ready.

---

## Phase 3: User Story 1 - Find the Right Icon Immediately (Priority: P1)

**Goal**: Produce one authoritative, human-navigable icon tree with exact manifests and safe compatibility aliases.

**Independent Test**: Build a raster-capable temporary kit, follow its root and platform README files, compare the complete manifest inventory to disk, and prove every `favicons/` alias matches its authoritative web target.

### Tests for User Story 1

- [x] T019 [US1] Complete failing manifest inventory, README presence, path normalization, collision, extra-file, and alias-byte tests in `skill/templates/test_iconkit.py`

### Implementation for User Story 1

- [x] T020 [US1] Implement the top-level `icons/README.md` and versioned `icons/manifest.json` writer in `skill/templates/iconkit.py`
- [x] T021 [US1] Implement per-platform README and platform-manifest writers in `skill/templates/iconkit.py`
- [x] T022 [US1] Implement the authoritative `icons/web/` suite and byte-copied `favicons/` compatibility mirror in `skill/templates/iconkit.py`
- [x] T023 [US1] Integrate authoritative icon generation after canonical SVG rendering in `skill/templates/gen_logo.py`
- [x] T024 [US1] Update generated kit anatomy and toolchain guidance in `skill/references/02-kit-anatomy.md` and `skill/references/04-toolchain.md`
- [x] T025 [US1] Run focused generator tests and inspect one temporary kit's navigation and manifest contract

**Checkpoint**: A user can locate every category from the kit root and legacy web paths remain deterministic aliases.

---

## Phase 4: User Story 2 - Integrate Native Application Icons (Priority: P1)

**Goal**: Deliver complete Android, Apple mobile, macOS, and Windows integration suites from canonical artwork.

**Independent Test**: Build one production kit and validate exact platform paths, image dimensions, appearances, safe areas, JSON/XML metadata, ICO entries, ICNS representations, and distinct store artwork.

### Tests for User Story 2

- [x] T026 [US2] Complete failing Android matrix, adaptive safe-zone, resource XML, and Play listing tests in `skill/templates/test_iconkit.py`
- [x] T027 [US2] Complete failing Apple mobile appearance, macOS catalog, iconset, and ICNS representation tests in `skill/templates/test_iconkit.py`
- [x] T028 [US2] Complete failing Windows classic ICO, MSIX scale, target-size appearance, store-logo, and manifest-reference tests in `skill/templates/test_iconkit.py`

### Implementation for User Story 2

- [x] T029 [US2] Implement Android legacy density, adaptive layer, resource XML, Play listing, README, and manifest output in `skill/templates/iconkit.py`
- [x] T030 [US2] Implement iOS and iPadOS default, dark, tinted, asset-catalog, README, and manifest output in `skill/templates/iconkit.py`
- [x] T031 [US2] Implement macOS all-sizes catalog, iconset, ICNS, README, and manifest output in `skill/templates/iconkit.py`
- [x] T032 [US2] Implement Windows classic ICO, MSIX scale, target-size appearance, store-logo, manifest fragment, README, and manifest output in `skill/templates/iconkit.py`
- [x] T033 [US2] Update the generator pipeline label and platform-delivery guidance in `skill/templates/build_kit.py` and `skill/SKILL.md`
- [x] T034 [US2] Update guide-facing platform asset descriptions in `skill/templates/gen_guide_pdf.py` and `skill/templates/gen_guidelines.py`
- [x] T035 [US2] Run all icon helper and pipeline tests, then inspect generated Android, Apple, macOS, and Windows metadata

**Checkpoint**: Native developers receive complete, distinctly labeled suites without manual resizing or path guessing.

---

## Phase 5: User Story 3 - Receive a Working Brand-Site Favicon (Priority: P1)

**Goal**: Publish the verified ShruggieTech web suite and enforce one shared icon contract on every public route.

**Independent Test**: Materialize and export the site, load the homepage, docs index, and nested docs page, then fetch and decode every icon and manifest relationship.

### Tests for User Story 3

- [x] T036 [US3] Complete generated-source, exact-copy, ICO, manifest, opaque-touch, and missing-source tests in `scripts/test_prepare_site.py`
- [x] T037 [US3] Complete route metadata, SVG dependency, PNG decode, dimensions, alpha, ICO entry, and manifest relationship fixtures in `site/tests/site.test.mjs`

### Implementation for User Story 3

- [x] T038 [US3] Publish the generated ShruggieTech `icons/web/` suite with no raw identity fallback in `scripts/prepare_site.py`
- [x] T039 [US3] Declare SVG, ICO, PNG, Apple touch, and manifest relationships in `site/app/layout.tsx`
- [x] T040 [US3] Replace the generic application-icon download with categorized icon-suite access in `site/app/(site)/[slug]/downloads/page.tsx`
- [x] T041 [US3] Add emitted PNG, ICO, SVG dependency, manifest, visible-bounds, and alpha validation in `site/scripts/verify-site.mjs`
- [x] T042 [US3] Run site materialization tests plus `pnpm --dir site lint`, `pnpm --dir site build`, and `pnpm --dir site test`

**Checkpoint**: Every route presents a valid ShruggieTech icon and broken artwork fails the emitted-site gate.

---

## Phase 6: User Story 4 - Reject Broken or Mispackaged Icons (Priority: P2)

**Goal**: Make kit verification reject every declared structural, metadata, image, container, alias, and stale-output defect.

**Independent Test**: Mutate isolated generated fixtures and prove each required defect produces a path-specific verification problem while clean production kits report zero problems.

### Tests for User Story 4

- [x] T043 [US4] Complete malformed manifest, undeclared file, unsafe path, wrong dimensions, wrong alpha, empty pixels, malformed XML/JSON, bad ICO, bad ICNS, and stale alias tests in `skill/templates/test_pipeline.py`

### Implementation for User Story 4

- [x] T044 [US4] Implement exact icon manifest inventory and alias verification in `skill/templates/verify.py`
- [x] T045 [US4] Implement image dimension, color mode, visible bounds, safe area, alpha policy, and file-size verification in `skill/templates/verify.py`
- [x] T046 [US4] Implement native JSON/XML metadata, platform filename, ICO entry, and ICNS representation verification in `skill/templates/verify.py`
- [x] T047 [US4] Extend capability artifact rules so raster-capable builds require all suites and lower tiers record explicit clean skips in `skill/templates/verify.py`
- [x] T048 [US4] Run all corruption tests and build `shruggietech` with zero `verify.py` problems and zero `validate_glyph.py` failures

**Checkpoint**: Existence-only false positives are eliminated for kits and the public site.

---

## Phase 7: Polish, Aggregate Verification, and Publication Readiness

**Purpose**: Synchronize documentation, evidence, changelogs, task state, and hosted merge-gate requirements.

- [x] T049 [P] Update feature and architecture decisions in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [x] T050 [P] Update the generated agent contract if template inventory changes require it in `skill/AGENTS.md`
- [x] T051 Run Python 3.8-compatible compile, focused tests, release-contract tests, and Markdown validation and record results in `specs/008-native-icon-delivery/evidence.md`
- [x] T052 Run `python scripts/build_all.py` for every production brand and record zero-problem evidence in `specs/008-native-icon-delivery/evidence.md`
- [x] T053 Run release packaging and release-contract certification with the current unreleased version and record results in `specs/008-native-icon-delivery/evidence.md`
- [x] T054 Run generated-agent synchronization, site lint, site build, site test, and WCAG validation and record results in `specs/008-native-icon-delivery/evidence.md`
- [x] T055 Audit UTF-8 without BOM, LF endings, mojibake, generated-artifact hygiene, `git diff --check`, and the complete source diff
- [x] T056 Re-run Spec Kit cross-artifact analysis, reconcile task and evidence traceability, and mark every completed task in `specs/008-native-icon-delivery/tasks.md`
- [x] T057 Commit S008 with a Conventional Commit subject, push `codex/008-native-icon-delivery`, and open a PR closing only #106 and #110
- [ ] T058 Monitor hosted CI and the initial Codex review, respond to and resolve every finding, and make required corrective commits
- [ ] T059 Request at most one explicit second Codex review only when the initial review requires changes, then resolve every second-round finding without requesting a third review
- [ ] T060 Confirm all hosted checks are green, all review threads are resolved, #106 and #110 remain open until merge, and halt for the owner's final review and merge ritual

---

## Dependencies and Execution Order

### Phase dependencies

- Phase 1 has no dependencies.
- Phase 2 depends on Phase 1 and blocks every user story.
- User Story 1 depends on Phase 2 and establishes the authoritative taxonomy consumed by the remaining stories.
- User Story 2 depends on User Story 1's manifest and composition primitives.
- User Story 3 depends on User Story 1's web suite and can proceed independently of the native platform implementations once that suite exists.
- User Story 4 depends on the complete generated output contract from User Stories 1 through 3.
- Phase 7 depends on all desired stories and all focused tests.

### User story dependencies

- **US1**: Starts after the shared profile and helper foundation; establishes the navigable delivery contract.
- **US2**: Uses US1 manifest and image primitives but is independently validated by native metadata and matrices.
- **US3**: Uses US1 web outputs but is independently validated through the static site export.
- **US4**: Validates every prior output and is the final shippability gate.

### Parallel opportunities

- T002 through T006 target separate Spec Kit artifacts.
- T011 and T012 target independent Python and site fixtures.
- Android, Apple, and Windows test design in T026 through T028 targets independent platform matrices.
- T049 and T050 target separate documentation contracts.

## Implementation Strategy

1. Lock the source profile and pure helper behavior with failing tests.
2. Deliver the human-navigable web suite and compatibility aliases as the smallest independently useful increment.
3. Add Android, Apple, macOS, and Windows outputs on the same manifest and composition core.
4. Publish the web suite to the site and validate actual rendered/deployed semantics.
5. Add adversarial verification, rebuild every production kit, and complete hosted review convergence.

## Notes

- No generated file under `dist/`, `site/out/`, `site/generated/`, or materialized `site/public/` belongs in the commit.
- Tests are written and observed failing before their corresponding implementation.
- Every child process remains non-interactive and hidden on Windows.
- S008 closes only #106 and #110. Issues #108, #109, and #111 remain open.
- Exactly one explicit second Codex review is permitted, and only if corrective changes make it useful. A third request is prohibited.
