# Tasks: Immutable Kit Publication

**Input**: Design documents from `/specs/043-immutable-kit-publication/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: Contract and regression tests are required and are written to fail before implementation.

**Organization**: Tasks are grouped by user story so each outcome can be tested independently.

## Phase 1: Setup (Shared Release Boundary)

**Purpose**: Align the unpublished release boundary and source authorities before changing generated contracts.

- [x] T001 Reconcile the unpublished 1.3.0 notes into a complete 2.0.0 boundary in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [x] T002 Update BrandBuilder release metadata and version history for 2.0.0 in `skill/SKILL.md`, `site/package.json`, and `scripts/release_contract.py`
- [x] T003 [P] Add the governed release-impact schema and 2.0.0 source record in `skill/references/release-impact.schema.json` and `skill/references/release-impact.json`

---

## Phase 2: Foundational (Shared Bundle Authority)

**Purpose**: Define the bundle and migration data consumed by all three stories.

**CRITICAL**: No publication, package, or guidance work begins until these contract foundations pass.

- [x] T004 [P] Add failing release-impact schema and prohibited-field tests in `skill/templates/test_interface_contract.py`
- [x] T005 [P] Add failing bundle-record generation and drift tests in `skill/templates/test_interface_contract.py`
- [x] T006 Extend consumer and documentation schemas for bundle and migration facts in `skill/references/consumer-contract.schema.json`, `skill/references/documentation-contract.json`, and `skill/references/documentation-contract.schema.json`
- [x] T007 Implement shared release-impact loading and validation in `skill/templates/interface_contract.py`
- [x] T008 Generate and verify `enforcement/bundle.json` plus consumer provenance in `skill/templates/interface_contract.py`
- [x] T009 Run the focused foundational contract suites in `skill/templates/test_interface_contract.py`

**Checkpoint**: One validated bundle authority and one validated impact authority are available to every story.

---

## Phase 3: User Story 1 - Download One Coherent Released System (Priority: P1) MVP

**Goal**: Make the production site, skill action, release assets, checksums, notes, and source revision represent one exact formal release.

**Independent Test**: Simulate main and exact-tag workflows; main retains candidate artifacts without deploying Pages, while the tag publishes a release before deploying a site whose generated record and actions point to that exact tag.

### Tests for User Story 1

- [x] T010 [P] [US1] Add failing tag-only deployment and release-before-Pages assertions in `scripts/test_publication_workflow.py`
- [x] T011 [P] [US1] Add failing exact release-record and no-moving-link tests in `scripts/test_prepare_site.py`, `site/tests/site.test.mjs`, and `site/scripts/verify-site.mjs`
- [x] T012 [P] [US1] Add failing release preflight tests for tag, notes, revision, and asset agreement in `scripts/test_release_contract.py`

### Implementation for User Story 1

- [x] T013 [US1] Emit an exact generated publication record from verified release metadata in `scripts/prepare_site.py`
- [x] T014 [US1] Replace the moving skill destination with the exact generated release action in `site/lib/layout.shared.tsx`
- [x] T015 [US1] Strengthen tagged release preflight and publication-record validation in `scripts/release_contract.py`
- [x] T016 [US1] Make production Pages tag-only and dependent on successful release publication in `.github/workflows/build.yml`
- [x] T017 [US1] Run the focused publication workflow, release contract, site preparation, and site tests

**Checkpoint**: The release-backed publication path is independently verifiable and untagged main cannot replace production.

---

## Phase 4: User Story 2 - Pin an Immutable Generated Kit (Priority: P1)

**Goal**: Give every generated kit a canonical package identity that changes with BrandBuilder while preserving the governed brand version.

**Independent Test**: Package the same brand version under two compiler identities; canonical IDs and filenames differ, and tampering with the filename, bundle record, revision, recovery metadata, or checksum authority fails verification.

### Tests for User Story 2

- [x] T018 [P] [US2] Add failing canonical package-name and unchanged-brand-version tests in `scripts/test_package_release.py` and `scripts/test_prepare_site.py`
- [x] T019 [P] [US2] Add failing archive bundle, manifest, recovery, revision, and checksum drift tests in `scripts/test_release_contract.py`
- [x] T020 [P] [US2] Add failing generated-kit package identity assertions in `skill/templates/test_pipeline.py`

### Implementation for User Story 2

- [x] T021 [US2] Centralize canonical package ID and filename construction in `scripts/package_release.py`
- [x] T022 [US2] Use canonical immutable package filenames in site staging and registries in `scripts/prepare_site.py`
- [x] T023 [US2] Validate bundle identity and cross-record agreement inside release archives in `scripts/release_contract.py`
- [x] T024 [US2] Document legacy brand-only names as non-canonical in `skill/references/12-verification-versioning.md`
- [x] T025 [US2] Run focused packaging, site staging, pipeline, and archive verification tests

**Checkpoint**: Two compiler releases cannot publish different kit bytes under the same canonical package identity.

---

## Phase 5: User Story 3 - Understand Migration Impact Without Identity Confusion (Priority: P2)

**Goal**: Generate consistent migration guidance that separates unchanged identity from required, optional, and unaffected implementation surfaces.

**Independent Test**: Generate hosted, bundled, portable, and release guidance from the same bundle and impact records; all classifications match, identity remains unchanged, and prohibited downstream evidence is absent.

### Tests for User Story 3

- [x] T026 [P] [US3] Add failing generated migration summary and cross-surface drift tests in `skill/templates/test_documentation_contract.py`
- [x] T027 [P] [US3] Add failing site and release guidance parity tests in `scripts/test_prepare_site.py` and `scripts/test_release_contract.py`
- [x] T028 [P] [US3] Add failing tests that reject downstream adoption and utility fields in `skill/templates/test_interface_contract.py`

### Implementation for User Story 3

- [x] T029 [US3] Generate migration summaries from bundle and impact records in `skill/templates/documentation_contract.py`
- [x] T030 [US3] Add generated migration guidance to kit, hosted, portable, and release surfaces in `skill/templates/gen_enforcement.py`, `scripts/prepare_site.py`, and `scripts/package_release.py`
- [x] T031 [US3] Verify guidance parity and prohibited evidence across all surfaces in `skill/templates/documentation_contract.py` and `scripts/release_contract.py`
- [x] T032 [US3] Run focused documentation, site, and release guidance tests

**Checkpoint**: Consumers receive bounded compatibility facts without any adoption or outcome tracking.

---

## Phase 6: Polish and Cross-Cutting Verification

**Purpose**: Complete traceability, repository-wide verification, and review preparation.

- [x] T033 [P] Update implementation and release documentation in `README.md`, `skill/references/02-kit-anatomy.md`, and `skill/references/12-verification-versioning.md`
- [x] T034 [P] Update all versioned examples and regression expectations from unpublished 1.3.0 to 2.0.0 in `scripts/`, `skill/templates/`, and `site/`
- [x] T035 Run the full validation documented in `specs/043-immutable-kit-publication/quickstart.md` and record results in `specs/043-immutable-kit-publication/verification.md`
- [x] T036 Verify zero logo-geometry changes, zero committed generated artifacts, UTF-8 without BOM, LF endings, and no mojibake; record evidence in `specs/043-immutable-kit-publication/verification.md`
- [x] T037 Update `specs/043-immutable-kit-publication/spec.md`, `plan.md`, and `tasks.md` to reflect implementation status and final evidence
- [x] T038 Prepare commit and pull-request traceability for #233, #234, #235, #222, and #209 without claiming the formal release has been published
- [x] T039 Stop after the local commit and request owner authorization before any push, pull request, tag, or release action as required by `.agents/skills/shruggie-speckit/assets/autopilot-protocol.md`
- [ ] T040 After authorization, push the feature branch and open a traceable pull request using the prepared body in `specs/043-immutable-kit-publication/pull-request.md`
- [ ] T041 After authorization, verify hosted CI is green and complete bounded pull-request review, recording resolved findings in `specs/043-immutable-kit-publication/verification.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- Phase 1 aligns the unpublished release boundary.
- Phase 2 depends on Phase 1 and blocks all user stories.
- US1 and US2 can begin after Phase 2 and are independently testable; the integrated publication path requires both before final verification.
- US3 depends on the shared bundle authority from Phase 2 but can otherwise proceed independently.
- Phase 6 depends on all selected stories.

### User Story Dependencies

- **US1 (P1)**: Depends only on the shared contract foundation.
- **US2 (P1)**: Depends only on the shared contract foundation.
- **US3 (P2)**: Depends on the shared bundle and impact records, not on production deployment behavior.

### Parallel Opportunities

- T003 can proceed independently of the changelog reconciliation.
- T004 and T005 target different test files.
- T010, T011, and T012 are independent failing-test changes.
- T018, T019, and T020 are independent failing-test changes.
- T026, T027, and T028 are independent failing-test changes.
- T033 and T034 can proceed in parallel after story implementation.

## Parallel Examples

### User Story 1

```text
T010: workflow ordering tests
T011: exact site action tests
T012: release preflight tests
```

### User Story 2

```text
T018: package naming tests
T019: archive agreement tests
T020: generated-kit identity tests
```

### User Story 3

```text
T026: documentation generation tests
T027: hosted and release parity tests
T028: prohibited evidence tests
```

## Implementation Strategy

1. Establish and test the shared bundle and impact contracts.
2. Complete US1 as the publication MVP and prove that untagged main cannot deploy production.
3. Complete US2 so every kit action and release asset is immutable.
4. Complete US3 so migration decisions remain accurate and bounded.
5. Run the full repository gate, perform bounded review, and prepare a traceable pull request.

## Format Validation

All 41 tasks use the required checkbox, sequential ID, optional parallel marker, user-story label where applicable, concrete action, and exact file path format.
