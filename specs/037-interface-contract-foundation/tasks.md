# Tasks: Interface Contract Foundation

**Input**: Design documents from `specs/037-interface-contract-foundation/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/interface-canon.md, contracts/routing-policy.md, contracts/consumer-contract.md, quickstart.md

**Tests**: Required by issues #210, #211, and #212 and the feature specification. Add focused regressions first and observe expected failures before implementation.

**Organization**: Tasks are grouped by user story so canon resolution, contextual routing, and consumer recovery remain independently traceable.

## Phase 1: Setup and Baseline

**Purpose**: Lock scope, source authority, versions, branch state, and current generated behavior.

- [x] T001 Record issue #210, #211, and #212 acceptance criteria, baseline commit, branch, versions, and production-brand inventory in `specs/037-interface-contract-foundation/evidence.md`
- [x] T002 [P] Record the existing Brand Canon, skill metadata, manifest, enforcement, synchronization, release archive, and verifier authority paths in `specs/037-interface-contract-foundation/evidence.md`
- [x] T003 [P] Confirm `dist/`, release archives, generated kits, and machine-local `.specify/feature.json` remain excluded from commits using `.gitignore` and `git status`

---

## Phase 2: Foundational Test Harness

**Purpose**: Establish fail-closed test coverage before source canon or generator changes.

- [x] T004 Add failing Interface Canon shape, required-role, unknown-role, invalid-target, cycle, compatibility, unsupported-override, cross-affiliation, and inaccessible-state tests in `skill/templates/test_interface_contract.py`
- [x] T005 [P] Add failing mixed runtime capability and operating-system-key rejection tests in `skill/templates/test_interface_contract.py`
- [x] T006 [P] Add failing contextual Author, Implementation, Audit, ambiguous, conflicting, existing-brand styling, contract-discovery, and missing-skill routing fixtures in `skill/references/routing-fixtures.json` and `skill/templates/test_interface_contract.py`
- [x] T007 Add failing consumer-contract, deterministic bundle, exact recovery, governed-block preservation, malformed-marker, provenance checksum, and capability-gap tests in `skill/templates/test_interface_contract.py` and `skill/templates/test_pipeline.py`
- [x] T008 [P] Add failing release archive requirements for the consumer contract and bundled exact distribution in `scripts/test_package_release.py`
- [x] T009 Run the focused pre-implementation suites and record the expected failures in `specs/037-interface-contract-foundation/evidence.md`

**Checkpoint**: Tests distinguish every named failure class and prove the current pipeline lacks the S037 contract.

---

## Phase 3: User Story 1 - Consume Governed Interface Intent (Priority: P1) MVP

**Goal**: Resolve one renderer-neutral Interface Canon for every production brand while preserving identity and failing closed on invalid structure or accessibility.

**Independent Test**: Validate the canonical contract against all production brands and mutate aliases, roles, state pairs, compatibility, and override boundaries to observe named failures.

### Tests for User Story 1

- [x] T010 [US1] Confirm T004 and T005 fail because Interface Canon source and validation do not exist

### Implementation for User Story 1

- [x] T011 [P] [US1] Author renderer-neutral primitives, semantic roles, logical-unit transforms, runtime capabilities, invariants, overrides, state pairs, and mixed profiles in `skill/references/interface-canon.json`
- [x] T012 [P] [US1] Author the synchronized Interface Canon schema in `skill/references/interface-canon.schema.json`
- [x] T013 [US1] Implement bounded loading, reference resolution, alias graph validation, runtime-profile validation, brand defaults, override boundaries, and accessibility pair measurement in `skill/templates/interface_contract.py`
- [x] T014 [US1] Integrate Interface Canon resolution into the first brand contract gate in `skill/templates/brand_contract.py` and `skill/templates/validate_brand.py`
- [x] T015 [US1] Add production-brand default resolution and identity-boundary assertions to `skill/templates/test_interface_contract.py`
- [x] T016 [US1] Run the focused canon suite and all production source validation, then record results in `specs/037-interface-contract-foundation/evidence.md`

**Checkpoint**: #210 has a source, schema, migration/default behavior, mixed runtime profiles, negative validation, and production-brand proof.

---

## Phase 4: User Story 2 - Route BrandBuilder Work from Context (Priority: P2)

**Goal**: Infer Author, Implementation, or Audit from normalized intent and repository evidence while preserving existing authorization.

**Independent Test**: Evaluate every routing fixture, confirm clear cases select one mode, conflicting cases ask one narrow question, and metadata-aware and ambient instructions remain equivalent.

### Tests for User Story 2

- [x] T017 [US2] Confirm T006 fails because mode policy, fixture evaluation, and distributed guidance are absent

### Implementation for User Story 2

- [x] T018 [P] [US2] Author canonical mode evidence, responsibilities, prohibitions, handoffs, and missing-skill recovery guidance in `skill/references/operating-modes.md`
- [x] T019 [US2] Implement authorization-preserving contextual mode decisions in `skill/templates/interface_contract.py`
- [x] T020 [US2] Update `skill/SKILL.md` with the mode routing table, inference order, conflict rule, consumer contract discovery, and exact recovery path
- [x] T021 [US2] Regenerate `skill/AGENTS.md` with `skill/templates/sync_agents_md.py` and add semantic-equivalence assertions in `skill/templates/test_interface_contract.py`
- [x] T022 [US2] Run all routing fixtures across both host surfaces and record results in `specs/037-interface-contract-foundation/evidence.md`

**Checkpoint**: #211 has canonical modes, contextual selection, missing-skill behavior, behavioral fixtures, and synchronized host instructions.

---

## Phase 5: User Story 3 - Resume Consumer Work from Delivered Bytes (Priority: P3)

**Goal**: Generate a deterministic, checksummed, merge-safe consumer authority surface with exact offline recovery and reusable-gap traceability.

**Independent Test**: Generate twice from identical inputs, preserve unrelated instructions, verify every focused checksum, install from the contained exact distribution without network, and create a complete unauthorized local gap draft.

### Tests for User Story 3

- [x] T023 [US3] Confirm T007 and T008 fail because consumer contract outputs and archive certification are absent

### Implementation for User Story 3

- [x] T024 [P] [US3] Author the consumer contract schema in `skill/references/consumer-contract.schema.json`
- [x] T025 [US3] Implement skill metadata parsing, deterministic exact-version bundle writing, contained provenance hashing, governed-block merge validation, consumer contract construction, and gap template construction in `skill/templates/interface_contract.py`
- [x] T026 [US3] Extend `skill/templates/gen_enforcement.py` to emit the concise governed block, deeper `IMPLEMENTATION.md`, copied canon and schema, consumer contract, gap template, and bundled distribution
- [x] T027 [US3] Extend enforcement documentation and final kit manifest metadata in `skill/templates/gen_enforcement.py` and `skill/templates/build_kit.py`
- [x] T028 [US3] Add production verification for contract shape, versions, host and renderer semantics, provenance checksums, marker integrity, recovery bundle path and hash, and gap authorization in `skill/templates/verify.py`
- [x] T029 [US3] Require and validate the consumer contract and exact distribution in release archives through `scripts/release_contract.py`
- [x] T030 [US3] Complete deterministic, preservation, mutation, offline recovery, and archive tests in `skill/templates/test_interface_contract.py`, `skill/templates/test_pipeline.py`, and `scripts/test_package_release.py`
- [x] T031 [US3] Generate a fresh isolated kit and a production kit, then record fresh-session discovery and offline handover evidence in `specs/037-interface-contract-foundation/evidence.md`

**Checkpoint**: #212 has generated instructions, a machine manifest, exact versions, renderer and host semantics, checksums, recovery, deterministic merge, verification, and a complete local gap record.

---

## Phase 6: Polish and Cross-Cutting Verification

**Purpose**: Synchronize governance, prove all kits, run CI parity, and prepare the authorized pull request.

- [x] T032 [P] Update `skill/references/02-kit-anatomy.md`, `skill/references/09-portability.md`, `CONTRIBUTING.md`, `.github/workflows/build.yml`, and the `skill/SKILL.md` file index for the delivered contract and focused suite
- [x] T033 [P] Add the S037 changes and dated architectural decisions to `CHANGELOG.md` without declaring a release
- [x] T034 Re-run cross-artifact analysis and reconcile `spec.md`, `plan.md`, `tasks.md`, contracts, data model, quickstart, source, tests, and evidence until no CRITICAL or HIGH findings remain
- [x] T035 Run Python compilation and the complete script and template unit suites, then record exact results in `specs/037-interface-contract-foundation/evidence.md`
- [x] T036 Run capability probing, all-production-kit generation, every per-kit `verify.py` and `validate_glyph.py`, deterministic recovery comparisons, release packaging/certification, and generated-agent diff, then record results
- [x] T037 Run Markdown validation, site lint/build/test, publication audit, and repository hygiene checks for generated artifacts, BOMs, mojibake, LF endings, and untracked state, then record results
- [x] T038 Mark completed tasks, run final cross-artifact analysis, create or update the S037 slice issue, and commit with a Conventional Commit subject containing S037

---

## Phase 7: Authorized Publication and Review Autopilot

**Purpose**: Push the verified branch, publish the official pull request, and close every automated review thread before owner merge review.

- [x] T039 Push `codex/037-interface-contract-foundation` to origin and open the official S037 pull request closing #210, #211, and #212 with complete verification evidence
- [x] T040 Wait for first-round CI, Codex, security, and other automated review results; inspect reviews, inline comments, issue comments, and pull-request reactions
- [x] T041 Address every actionable first-round comment with tests and source changes, reply to each comment, resolve satisfied threads, rerun affected and full gates, commit, and push
- [ ] T042 Trigger exactly one second Codex review round with `@Codex review`, then wait for CI and all second-round review results
- [ ] T043 Address every actionable second-round comment, reply and resolve each thread, rerun affected and full gates, commit, push, and do not request a third review round
- [ ] T044 Confirm every required CI check is green, every review is satisfied or explicitly non-actionable, and no unresolved thread remains; update `specs/037-interface-contract-foundation/evidence.md` and ping the owner for the final review and merge ritual

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup** starts immediately.
- **Foundational tests** depend on the baseline and block implementation.
- **US1** establishes the shared canon and resolution used by later consumer outputs.
- **US2** depends only on the shared policy module but is delivered after US1 to preserve chronological implementation.
- **US3** consumes the canon and routing guidance and adds generated delivery, verification, and recovery.
- **Polish** depends on all user stories.
- **Publication and review** depends on every local gate and commit.

### Within Each User Story

- Add the test first and observe the expected failure.
- Make the smallest source change that satisfies the documented contract.
- Run the independent story test before advancing.
- Preserve Brand Canon, identity geometry, and existing authorization boundaries.

### Parallel Opportunities

- T002 and T003 touch separate evidence and hygiene checks.
- T005, T006, and T008 cover independent contract, routing, and archive surfaces after T004 establishes the test module.
- T011 and T012 can be authored together before T013.
- T018 can be authored while T019 is implemented after the routing fixtures exist.
- T032 and T033 touch separate documentation surfaces after behavior stabilizes.

## Implementation Strategy

### MVP First

1. Lock authority and baseline.
2. Add failing Interface Canon and runtime tests.
3. Implement and validate the source canon for every production brand.
4. Stop and independently verify #210 before routing and delivery work.

### Incremental Delivery

1. US1 provides renderer-neutral governed intent and fail-closed validation.
2. US2 provides authorization-preserving contextual operation across host surfaces.
3. US3 makes those authorities discoverable, deterministic, portable, and recoverable from delivered bytes.
4. Full CI and review autopilot validate the integrated slice before owner merge.

## Notes

- Custom checklist markers remain reviewer-owned and do not track implementation completion.
- S037 closes only #210, #211, and #212. Recipes, adapters, conformance hosts, full version policy, consumer adoption, and documentation restructuring remain with their owning issues.
- Do not change approved logo path data or source bytes.
- Do not commit generated `dist/`, `site/out/`, PDFs, raster exports, registries, nested `.skill` distributions, or release archives.
- The user explicitly authorized push and pull-request creation. No more than two Codex review rounds may be requested.
