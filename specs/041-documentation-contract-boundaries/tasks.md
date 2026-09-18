# Tasks: Documentation Contract Boundaries

**Input**: Design documents from `specs/041-documentation-contract-boundaries/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`

**Tests**: S041 uses test-driven implementation. Contract, projection, route, drift, accessibility, and all-brand verification tasks are mandatory.

**Organization**: Tasks are grouped by user story so each surface can be validated independently before the full three-surface agreement gate.

## Phase 1: Setup and baseline

**Purpose**: Record the exact current documentation and route surfaces before adding the governed contract.

- [X] T001 Inventory top-level manual references, generated guidance, hosted portal fields, and documentation-related route kinds in `specs/041-documentation-contract-boundaries/evidence.md`
- [X] T002 Record baseline focused test results for documentation staging, consumer contracts, pipeline generation, and site contracts in `specs/041-documentation-contract-boundaries/evidence.md`
- [X] T003 [P] Verify `.gitignore` and site ignore/config entries cover generated kit, site export, test results, and dependency output without editing unrelated patterns

---

## Phase 2: Foundational documentation contract

**Purpose**: Establish the policy, schema, and reusable validation layer that blocks all projections.

- [X] T004 Add failing schema, inventory, topic coverage, navigation, disposition, and unsafe-path tests in `skill/templates/test_documentation_contract.py`
- [X] T005 Add the versioned documentation policy in `skill/references/documentation-contract.json`
- [X] T006 Add the policy schema in `skill/references/documentation-contract.schema.json`
- [X] T007 Implement Python 3.8-compatible loading, schema validation, source inventory, navigation, topic, and disposition checks in `skill/templates/documentation_contract.py`
- [X] T008 Add documentation contract validation to the minimum-runtime and verified-build jobs in `.github/workflows/build.yml`
- [X] T009 Run `python skill/templates/test_documentation_contract.py` and record the foundational checkpoint in `specs/041-documentation-contract-boundaries/evidence.md`

**Checkpoint**: The documentation contract is deterministic, validates every current manual source, covers all required topics, and rejects missing or unsafe dispositions.

---

## Phase 3: User Story 1 - Learn and extend BrandBuilder from one manual (Priority: P1) MVP

**Goal**: Publish a complete system manual whose navigation and metadata derive from the governed documentation contract.

**Independent Test**: Stage manual sources and build `/docs/`; every required system topic, source owner, validation entry point, hierarchy, and no-script link is reachable without a child-brand guide.

### Tests for User Story 1

- [X] T010 [US1] Add failing contract-derived metadata, navigation, topic coverage, and unlisted-page tests in `scripts/test_prepare_site.py`
- [X] T011 [P] [US1] Add failing expected hierarchy and manual-coverage assertions in `site/tests/site.test.mjs`

### Implementation for User Story 1

- [X] T012 [US1] Replace hard-coded documentation descriptions and navigation with contract-derived records in `scripts/prepare_site.py`
- [X] T013 [P] [US1] Author architecture and documentation ownership guidance in `skill/references/10-system-architecture.md`
- [X] T014 [P] [US1] Author Interface Canon, recipe, Web/React, AppFrame, and egui implementation guidance in `skill/references/11-interface-implementation.md`
- [X] T015 [P] [US1] Author verification, conformance, versioning, and release guidance in `skill/references/12-verification-versioning.md`
- [X] T016 [P] [US1] Author installation, recovery, agent integration, capability-gap, and extension guidance in `skill/references/13-agent-integration.md`
- [X] T017 [US1] Update documentation hierarchy expectations and source-driven route records in `site/tests/site.test.mjs`
- [X] T018 [US1] Run `python scripts/test_prepare_site.py` and the Node site contract test, then record the US1 checkpoint in `specs/041-documentation-contract-boundaries/evidence.md`

**Checkpoint**: The main manual independently covers every required system topic from governed source and retains accessible navigation.

---

## Phase 4: User Story 2 - Inspect one brand without reading the compiler manual (Priority: P2)

**Goal**: Expose exact generated versions, bindings, affiliation, and manual destinations in every hosted child-brand reference.

**Independent Test**: Generate and stage one brand portal from a valid synthetic documentation-fact fixture; its overview displays the complete generated version set and implementation bindings while shared architecture resolves to the system manual.

### Tests for User Story 2

- [X] T019 [US2] Add failing portal exact-version, binding, manual-link, affiliation, altered-fact, and missing-fact tests using a valid synthetic fact record in `skill/templates/test_pipeline.py`
- [X] T020 [P] [US2] Add failing hosted projection validation tests in `scripts/test_prepare_site.py`
- [X] T021 [P] [US2] Add failing hosted summary rendering and type assertions in `site/tests/site.test.mjs`

### Implementation for User Story 2

- [X] T022 [US2] Embed the exact generated documentation fact record into the portal payload in `skill/templates/gen_guidelines.py`
- [X] T023 [US2] Validate and stage hosted documentation facts without mutation in `scripts/prepare_site.py`
- [X] T024 [US2] Extend hosted portal types for the generated fact record in `site/lib/guidelines.ts`
- [X] T025 [US2] Render exact current contract versions, supported bindings, affiliation, and system-manual links in `site/components/guidelines/topic-content.tsx`
- [X] T026 [US2] Add responsive hosted contract-summary styles in `site/app/globals.css`
- [X] T027 [US2] Run synthetic-fact portal generation, staging, and site contract tests and record the US2 surface checkpoint in `specs/041-documentation-contract-boundaries/evidence.md`

**Checkpoint**: Hosted brand references identify their exact current generated contract without copying the compiler manual or changing identity presentation.

---

## Phase 5: User Story 3 - Implement exact delivered bytes offline (Priority: P3)

**Goal**: Generate complete offline implementation guidance and prove its shared facts agree with the hosted portal.

**Independent Test**: Generate one isolated kit, remove network assumptions, and verify all fact paths, versions, commands, recovery bytes, checksum, and gap rules from local files.

### Tests for User Story 3

- [X] T028 [US3] Add failing shared-fact generation, deterministic Markdown, missing-path, tamper, checksum, latest-version, and portal-drift tests in `skill/templates/test_documentation_contract.py`
- [X] T029 [US3] Add failing consumer authority, provenance, schema, and offline guidance tests in `skill/templates/test_interface_contract.py`

### Implementation for User Story 3

- [X] T030 [US3] Implement shared fact generation, fact verification, and offline `IMPLEMENTATION.md` rendering in `skill/templates/documentation_contract.py`
- [X] T031 [US3] Extend consumer contract schema authority fields in `skill/references/consumer-contract.schema.json`
- [X] T032 [US3] Copy documentation policy files, emit facts and Markdown, and record provenance in `skill/templates/interface_contract.py`
- [X] T033 [US3] Refactor enforcement generation to supply brand-specific governed rules without maintaining an independent implementation authority in `skill/templates/gen_enforcement.py`
- [X] T034 [US3] Add documentation fact and bundled guidance verification to `skill/templates/verify.py`
- [X] T035 [US3] Run documentation, interface-contract, and pipeline tests and record the US3 checkpoint in `specs/041-documentation-contract-boundaries/evidence.md`

**Checkpoint**: A generated kit is complete offline, exact-versioned, checksum-bound, and mechanically consistent with its hosted projection.

---

## Phase 6: User Story 4 - Review ownership and migration evidence (Priority: P4)

**Goal**: Prove complete content and route disposition and explain the three-surface system through accessible semantic graphics.

**Independent Test**: Expand the disposition contract against all current sources and generated routes, then inspect all three graphics at accessible display modes and without script.

### Tests for User Story 4

- [X] T036 [US4] Add failing route-kind coverage, missing disposition, redirect requirement, and stale-source tests in `scripts/test_prepare_site.py`
- [X] T037 [P] [US4] Add failing semantic structure, text-equivalent, no-script, and accessible-label assertions in `site/tests/site.test.mjs`
- [X] T038 [P] [US4] Add browser assertions for overview graphics, hosted summaries, links, narrow width, 200 percent zoom, forced colors, reduced motion, and no-script in `site/scripts/verify-site.mjs`

### Implementation for User Story 4

- [X] T039 [US4] Validate every documentation-related generated route against the contract disposition in `scripts/prepare_site.py`
- [X] T040 [US4] Implement documentation ownership, operating modes, and improvement-loop graphics with adjacent text equivalents in `site/components/documentation-overviews.tsx`
- [X] T041 [US4] Add the overview graphics to the documentation index in `site/app/docs/[[...slug]]/page.tsx`
- [X] T042 [US4] Add responsive, zoom-safe, reduced-motion, and forced-colors graphic styles in `site/app/globals.css`
- [X] T043 [US4] Run staging and site verification and record the US4 checkpoint in `specs/041-documentation-contract-boundaries/evidence.md`

**Checkpoint**: Every current source and route has an explicit disposition, and all three relationship views remain accessible with and without client script.

---

## Phase 7: Integration and release-quality verification

**Purpose**: Prove all documentation surfaces agree across every production brand and CI path.

- [X] T044 Add documentation contract tests to the documented contributor workflow in `CONTRIBUTING.md`
- [X] T045 Update the unreleased feature and dated architecture decision in `CHANGELOG.md`
- [X] T046 Run Python compile, all focused contract/staging/release/identity tests, and Markdown validation; record exact results in `specs/041-documentation-contract-boundaries/evidence.md`
- [X] T047 Run `python scripts/build_all.py` and record all eight zero-problem and zero-glyph-failure results in `specs/041-documentation-contract-boundaries/evidence.md`
- [X] T048 Run site lint, static build, Node tests, Playwright/axe verification, and publication audit; record exact results in `specs/041-documentation-contract-boundaries/evidence.md`
- [X] T049 Run UTF-8 BOM, mojibake, generated-artifact, synchronized-agent, diff, and worktree hygiene checks; record results in `specs/041-documentation-contract-boundaries/evidence.md`
- [X] T050 Reconcile every spec requirement, success criterion, issue #213 acceptance item, and completed task in `specs/041-documentation-contract-boundaries/evidence.md` and `specs/041-documentation-contract-boundaries/tasks.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- Phase 1 establishes the baseline.
- Phase 2 blocks all user stories.
- US1 depends on Phase 2 and supplies the system-manual destination used by later stories.
- US2 depends on Phase 2 and the shared fact shape finalized with US3; its failing tests may be written before US3 implementation.
- US3 depends on Phase 2 and existing consumer contract generation.
- US4 depends on US1 navigation and route generation but can develop graphic structure independently.
- Integration depends on all four user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after the foundational contract and independently delivers the system manual.
- **US2 (P2)**: Starts after the foundational contract; final projection uses the US3 fact record.
- **US3 (P3)**: Starts after the foundational contract and independently delivers offline correctness.
- **US4 (P4)**: Starts after US1 route/navigation integration; graphics are otherwise independent.

### TDD Order

1. Write contract and negative-path tests before policy validation.
2. Write site staging and hierarchy tests before contract-driven navigation.
3. Write portal tests before adding hosted facts and rendering.
4. Write offline and drift tests before shared-fact generation and verification.
5. Write route and accessibility tests before the disposition gate and graphics.

## Parallel Opportunities

- T003 can run alongside baseline inventory.
- T011 can run alongside T010.
- T013 through T016 are independent manual pages after the policy shape exists.
- T020 and T021 can run alongside T019.
- T036 through T038 cover different layers and can be authored independently.
- Focused validation commands that do not mutate shared output may run independently; full build and site staging remain sequential.

## Implementation Strategy

### MVP First

1. Complete baseline and foundational contract.
2. Deliver US1 system manual and contract-derived navigation.
3. Validate the manual independently before projections.

### Incremental Delivery

1. Add the main manual authority.
2. Add one shared generated fact record and complete offline bundle.
3. Project the same record into hosted brand references.
4. Add migration evidence and semantic relationship graphics.
5. Rebuild and verify all brands and the public site.

## Notes

- `[P]` tasks touch independent files or test layers.
- Custom checklist markers remain reviewer-owned and are not implementation progress.
- Generated outputs under `dist/`, `site/out/`, and `site/test-results/` remain ignored and uncommitted.
- No task changes #193, #194, #202, consumer repositories, approved identity, or release state.
