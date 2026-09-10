# Tasks: Approved Identity Construction Continuity

**Input**: Design documents from `specs/027-approved-identity-construction-continuity/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: S027 requires test-first coverage for approval states, source continuity, promotion, perceptual evidence, migration, security boundaries, and the known Cueson regression.

**Organization**: Tasks are chronological and grouped by independently testable user story. Each implementation phase begins with failing focused tests.

## Phase 1: Setup and specification baseline

**Purpose**: Bind S027 to current main, issue #185, constitutional gates, and a complete reviewed work order.

- [X] T001 Record the clean merged-S026 baseline, issue #185 state, branch, Spec Kit selector, and artifact boundaries in `specs/027-approved-identity-construction-continuity/evidence.md`
- [X] T002 [P] Validate `specs/027-approved-identity-construction-continuity/spec.md` against `specs/027-approved-identity-construction-continuity/checklists/requirements.md`
- [X] T003 [P] Review every requirements-quality item in `specs/027-approved-identity-construction-continuity/checklists/continuity.md` and resolve any specification gap before implementation
- [X] T004 Confirm the Phase 0 and Phase 1 decisions pass constitution P1 through P6 in `specs/027-approved-identity-construction-continuity/plan.md`
- [X] T005 Capture pre-migration hashes for all production identity paths, palette values, framing configuration, source mode, and showcase state in ignored `dist/identity-continuity-preflight.json`

---

## Phase 2: Foundational continuity model

**Purpose**: Establish shared schemas, deterministic snapshots, safe path handling, and test fixtures that block every story.

**Critical**: No user-story implementation begins until this phase is complete.

- [X] T006 [P] Add failing canonical serialization, identity snapshot, record-shape, malformed-hash, duplicate-key, and safe-path tests in `skill/templates/test_identity_continuity.py`
- [X] T007 [P] Add failing schema-reference and brand-contract integration tests in `skill/templates/test_brand_contract.py`
- [X] T008 Define the brand-level continuity reference and complete continuity record definitions in `skill/references/canon.schema.json`
- [X] T009 Implement canonical serialization, digest helpers, safe contained-path resolution, source inventories, framing snapshots, palette snapshots, geometry snapshots, and record validation in `skill/templates/identity_continuity.py`
- [X] T010 Integrate the continuity reference and record validator into `skill/templates/brand_contract.py`
- [X] T011 Add source-record copying and measured report setup to the pre-derivative stages in `skill/templates/build_kit.py`
- [X] T012 Add independent generated-record verification scaffolding to `skill/templates/verify.py`
- [X] T013 Run the focused foundation tests and record the red-to-green sequence in `specs/027-approved-identity-construction-continuity/evidence.md`

**Checkpoint**: The repository can represent and validate continuity records without changing identity output.

---

## Phase 3: User Story 1 - Approve the exact production identity (Priority: P1)

**Goal**: Distinguish nonbinding direction selection from source-bound canonical approval and reject incomplete or contradictory approval bundles.

**Independent Test**: A synthetic identity can select a direction without gaining derivative authority, while canonical approval succeeds only with complete production source, full and reduced master, palette, framing, topology, renderer, proof, owner, and revision bindings.

### Tests for User Story 1

- [X] T014 [P] [US1] Add failing lifecycle-transition tests for exploratory, direction-selected, canonical-candidate, canonical-approved, promoted, invalidated, derivative-approved, and publication-eligible states in `skill/templates/test_identity_continuity.py`
- [X] T015 [P] [US1] Add failing completeness and staleness tests for canonical approval evidence in `skill/templates/test_identity_continuity.py`
- [X] T016 [P] [US1] Add failing same-renderer proof-matrix and exact-hash tests in `skill/templates/test_identity_continuity.py`

### Implementation for User Story 1

- [X] T017 [US1] Implement lifecycle transition validation and nonbinding direction-selection semantics in `skill/templates/identity_continuity.py`
- [X] T018 [US1] Implement approved-canonical bundle validation for owner wording, scope, revisions, source snapshot, renderer, topology, palette qualification, and proof matrix in `skill/templates/identity_continuity.py`
- [X] T019 [US1] Extend approval-ledger validation so Gate 1 canonical authority and Gate 2 derivative authority cannot be conflated in `skill/templates/brand_contract.py`
- [X] T020 [US1] Define the operator-facing canonical approval packet and invalidation rules in `skill/references/identity-continuity.md`
- [X] T021 [US1] Run User Story 1 tests and record independent results in `specs/027-approved-identity-construction-continuity/evidence.md`

**Checkpoint**: Direction selection cannot authorize source promotion or derivative work, and canonical approval binds exact production evidence.

---

## Phase 4: User Story 2 - Promote and verify without reconstruction (Priority: P1)

**Goal**: Copy approved source bytes atomically, enforce prospective glyphkit provenance, and fail generation on every governed drift class.

**Independent Test**: A valid provisional source promotes with byte equality; traversal, symlink, external destination, executable declaration, reconstruction, literal paths, custom serializers, and post-approval drift all fail before derivative generation.

### Tests for User Story 2

- [X] T022 [P] [US2] Add failing glyphkit-helper syntax and allowed-primitive tests, including Cueson and a custom-serializer rejection fixture, in `skill/templates/test_identity_continuity.py`
- [X] T023 [P] [US2] Add failing promotion tests for path traversal, symlink escape, duplicate destinations, undeclared files, generated proof files, arbitrary targets, partial-copy rollback, and stale hashes in `skill/templates/test_identity_continuity.py`
- [X] T024 [P] [US2] Add failing build-pipeline tests for source, method, geometry, topology, framing, palette, renderer, and proof drift before derivative generation in `skill/templates/test_pipeline.py`

### Implementation for User Story 2

- [X] T025 [US2] Implement syntax-only glyphkit construction provenance validation and legacy/source-mode exclusions in `skill/templates/identity_continuity.py`
- [X] T026 [US2] Implement bounded staging, byte-copy promotion, rollback, replacement safeguards, and post-install equality in `skill/templates/promote_identity.py`
- [X] T027 [US2] Make `skill/templates/build_kit.py` stop before logo generation whenever the source continuity contract fails
- [X] T028 [US2] Make `skill/templates/verify.py` independently reject stale generated continuity evidence
- [X] T029 [US2] Run User Story 2 tests and record independent security and drift results in `specs/027-approved-identity-construction-continuity/evidence.md`

**Checkpoint**: Approved source enters production unchanged, and every governed post-approval drift class fails closed.

---

## Phase 5: User Story 3 - Judge visual and color continuity before approval (Priority: P2)

**Goal**: Produce complete multi-size, multi-surface comparisons and pre-approval palette evidence that distinguish harmless renderer edges from identity drift.

**Independent Test**: The unchanged Cueson coordinate contract passes calibrated cross-renderer checks at all required sizes and surfaces, while the rejected reconstruction, occupancy shift, hole, component, framing, and color mutations fail and emit all four review evidence families.

### Tests for User Story 3

- [X] T030 [P] [US3] Add failing proof-matrix, hard-mask topology, component, hole, bounds, centroid, edge-band, IoU-evidence, and evidence-family tests in `skill/templates/test_identity_continuity.py`
- [X] T031 [P] [US3] Add failing interior Delta E, intended-color, qualification completeness, contrast, sibling-separation, color-vision, semantic-role, surface, and single-ink tests in `skill/templates/test_identity_continuity.py`
- [X] T032 [P] [US3] Add known-equivalent and known-divergent Cueson regression fixtures generated only in temporary test storage in `skill/templates/test_identity_continuity.py`

### Implementation for User Story 3

- [X] T033 [US3] Implement PNG proof loading, hard masks, connected components, enclosed holes, edge-band dilation, bounds, centroids, IoU, changed-pixel, and interior-color measurement in `skill/templates/identity_continuity.py`
- [X] T034 [US3] Implement same-renderer exact comparison and calibrated cross-renderer disposition rules in `skill/templates/identity_continuity.py`
- [X] T035 [US3] Implement deterministic side-by-side, alpha-overlay, silhouette-XOR, color-difference images, and comparison manifests in `skill/templates/identity_continuity.py`
- [X] T036 [US3] Implement complete pre-approval palette qualification validation and exact sRGB/OKLCH bindings in `skill/templates/identity_continuity.py`
- [X] T037 [US3] Add proof comparison and palette-qualification evidence to the approval workflow guidance in `skill/references/identity-continuity.md`
- [X] T038 [US3] Run User Story 3 tests, visually inspect generated regression evidence, and record calibration results in `specs/027-approved-identity-construction-continuity/evidence.md`

**Checkpoint**: Approval packets reveal production geometry and color at every required size and surface, with equivalent and divergent cases classified correctly.

---

## Phase 6: User Story 4 - Protect existing identities during migration (Priority: P2)

**Goal**: Give every current production brand a truthful continuity baseline without changing geometry, palette, framing, generated output, or showcase state.

**Independent Test**: All seven brands classify and validate; before-and-after authoritative values are identical; Cueson remains the corrected regression; Covarity is documented as legacy; no historical record fabricates owner approval.

### Tests for User Story 4

- [X] T039 [P] [US4] Add failing inventory completeness, classification, baseline revision, historical-evidence, and preservation tests in `scripts/test_identity_continuity_audit.py`
- [X] T040 [P] [US4] Add failing tests that prevent historical baselines from serving as new canonical approval or changing public eligibility in `skill/templates/test_identity_continuity.py`

### Implementation for User Story 4

- [X] T041 [US4] Implement deterministic inventory, record generation, check mode, preservation comparison, and ignored report output in `scripts/audit_identity_continuity.py`
- [X] T042 [US4] Add continuity references without changing governed identity values in all seven `brands/*/brand.json` files
- [X] T043 [US4] Generate and review truthful historical baseline records in all seven `brands/*/identity-continuity.json` files
- [X] T044 [US4] Correct only Covarity’s inaccurate provenance label to legacy construction and assert unchanged helper and path bytes in `brands/covarity/brand.json`
- [X] T045 [US4] Run the migration audit against the preflight snapshot and record exact preservation evidence in `specs/027-approved-identity-construction-continuity/evidence.md`
- [X] T046 [US4] Build and verify every migrated production kit, confirming zero identity drift, zero verification problems, and zero glyph failures in `specs/027-approved-identity-construction-continuity/evidence.md`

**Checkpoint**: Every current brand has a continuity record and no established identity changed.

---

## Phase 7: User Story 5 - Apply the safer workflow consistently (Priority: P3)

**Goal**: Align human instructions, schema, generated agent guidance, validation, and future Spec Kit intake around the corrected lifecycle.

**Independent Test**: A future constructed-brand work order cannot call a sketch final approval, prohibit production construction before final approval, or reveal production geometry first at Gate 2 without contradicting an explicit enforceable rule.

### Tests for User Story 5

- [X] T047 [P] [US5] Add documentation-contract assertions for lifecycle terminology, production-master timing, palette timing, Gate 2 boundaries, and invalidation in `skill/templates/test_pipeline.py`
- [X] T048 [P] [US5] Add schema regression assertions for continuity references, record statuses, source classes, and historical-baseline restrictions in `skill/templates/test_brand_contract.py`

### Implementation for User Story 5

- [X] T049 [US5] Rewrite the brandbuilder gate summary and finishing rules around direction selection and canonical approval in `skill/SKILL.md`
- [X] T050 [US5] Correct interview sequencing and owner-decision terminology in `skill/references/03-interview.md`
- [X] T051 [US5] Require production-rendered canonical evidence before logo approval and forbid Gate 2 reconstruction in `skill/references/06-logo-protocol.md`
- [X] T052 [US5] Require pre-approval primitive conversion, helper provenance, framing, and topology evidence in `skill/references/08-glyph-construction.md`
- [X] T053 [US5] Synchronize generated agent instructions from `skill/SKILL.md` into `skill/AGENTS.md`
- [X] T054 [US5] Run User Story 5 documentation and schema tests and record independent results in `specs/027-approved-identity-construction-continuity/evidence.md`

**Checkpoint**: Human and machine contracts use one lifecycle with no contradictory approval boundary.

---

## Phase 8: Polish, complete verification, publication, and bounded review

**Purpose**: Prove the integrated repository, publish the authorized PR, process every review, and halt before merge.

- [X] T055 Update root and skill unreleased history with the S027 feature and dated architecture decision in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [X] T056 Run the complete focused Python test matrix from `specs/027-approved-identity-construction-continuity/quickstart.md` and record results in `specs/027-approved-identity-construction-continuity/evidence.md`
- [X] T057 Run full capability probing, all seven production-kit builds, release certification, and generated-agent synchronization from `specs/027-approved-identity-construction-continuity/quickstart.md`
- [X] T058 Run site lint, static export, browser route tests, and WCAG checks from `specs/027-approved-identity-construction-continuity/quickstart.md`
- [X] T059 Audit the plan’s validation runtimes, UTF-8 without BOM, LF endings, mojibake, private paths, ignored generated output, tracked artifact boundaries, and `git diff --check` in `specs/027-approved-identity-construction-continuity/evidence.md`
- [X] T060 Re-run cross-artifact analysis and resolve every specification, plan, task, contract, checklist, and implementation inconsistency in `specs/027-approved-identity-construction-continuity/`
- [X] T061 Commit S027 with Conventional Commit traceability and confirm the feature branch is clean
- [X] T062 Push `codex/027-approved-identity-construction-continuity` and open the official pull request closing #185 under the owner’s explicit authorization
- [X] T063 Record hosted CI, review comments, reactions, security findings, responses, fixes, thread resolutions, and the first Codex round in `specs/027-approved-identity-construction-continuity/evidence.md`
- [X] T064 Request at most one second Codex review when useful, process every resulting finding, and never request a third round
- [ ] T065 Confirm the exact final head has green required checks, no unresolved review threads, a clean merge state, and a complete PR readiness ledger
- [ ] T066 Halt without merging and ask the owner to perform the final review and merge ritual

---

## Dependencies and execution order

### Phase dependencies

- Phase 1 establishes the reviewed work order and pre-migration baseline.
- Phase 2 depends on Phase 1 and blocks every user story.
- User Story 1 depends on Phase 2 and establishes canonical approval semantics.
- User Story 2 depends on User Story 1 because promotion consumes approved bundles.
- User Story 3 depends on User Story 1 but its proof algorithms can be developed independently of promotion.
- User Story 4 depends on Phase 2 and the historical-record model; its audit can proceed independently of visual proof generation.
- User Story 5 depends on the settled contracts from User Stories 1 through 4.
- Phase 8 depends on all user stories.

### Parallel opportunities

- T002 and T003 review separate checklists.
- T006 and T007 establish separate module and integration tests.
- Within each story, test files marked `[P]` can be authored together before implementation.
- User Story 3 proof comparison and User Story 4 migration-audit tests affect different files after the shared model stabilizes.
- Documentation files T049 through T052 can be revised independently once lifecycle terms are final.

## Implementation strategy

### MVP first

1. Complete Phases 1 and 2.
2. Complete User Story 1 to make final approval truthful.
3. Complete User Story 2 to make promotion and drift rejection mechanical.
4. Validate the canonical approval and promotion contracts independently before adding perceptual evidence or migration.

### Incremental delivery

1. Land the deterministic source and lifecycle contract.
2. Add safe promotion and fail-closed build integration.
3. Add calibrated visual and palette evidence.
4. Migrate all existing brands without identity changes.
5. Align documentation and run full validation.
6. Publish once, process no more than two Codex rounds, and halt at owner merge.

## Notes

- Tests are written first and must demonstrate a meaningful failure before implementation.
- Generated records used for design review remain ignored; committed per-brand continuity files are source contracts, not generated kits.
- `historical-baseline` describes current authoritative facts and cannot be used to fabricate approval.
- Cueson is regression evidence only. S027 cannot alter its approved identity.
- T066 is completed only by the final halt response after hosted readiness is proven.
