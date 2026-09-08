# Tasks: ESO Weave Provenance and Current-Spec Kit

**Input**: Design documents from `/specs/020-eso-weave-provenance-kit/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: S020 requires test-first contract, integration, identity-fidelity, accessibility, and publication-gate coverage.

**Organization**: Tasks follow the four user stories and stop at the two explicit owner gates.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run independently in a separate file after its dependencies are satisfied
- **[Story]**: Maps implementation work to a specification user story

## Phase 1: Setup and Specification

**Purpose**: Freeze scope, current source state, and governance before implementation.

- [x] T001 Synchronize Shruggie Brand `main`, create `codex/020-eso-weave-provenance-kit`, and preserve unrelated checkout state
- [x] T002 Synchronize ESO Weave remote objects, resolve its default branch, and record the current commit in `specs/020-eso-weave-provenance-kit/research.md`
- [x] T003 [P] Complete the S020 specification and requirements checklist in `specs/020-eso-weave-provenance-kit/spec.md` and `specs/020-eso-weave-provenance-kit/checklists/requirements.md`
- [x] T004 [P] Complete S020 research, data model, contracts, plan, and validation quickstart under `specs/020-eso-weave-provenance-kit/`

---

## Phase 2: Foundational Fail-Closed Contracts

**Purpose**: Add negative coverage before any new production brand becomes buildable or publishable.

- [x] T005 Add failing tests for approval-ledger structure, hash binding, missing Gate 1, and stale Gate 1 in `skill/templates/test_brand_contract.py`
- [x] T006 [P] Add failing tests for ESO Weave vendor-boundary requirements and prohibited third-party combinations in `skill/templates/test_brand_contract.py`
- [x] T007 [P] Add failing publication tests proving a buildable-but-unapproved ESO Weave source stays absent in `scripts/test_prepare_site.py`
- [x] T008 Implement the minimum generic approval and legal-boundary contract needed by the failing tests in `skill/templates/brand_contract.py` and `skill/references/canon.schema.json`
- [x] T009 Integrate approval and vendor-boundary validation into generation and site projection in `skill/templates/build_kit.py`, `skill/templates/gen_guidelines.py`, and `scripts/prepare_site.py`

**Checkpoint**: Missing, rejected, or stale approvals and missing legal boundaries fail closed before derivative generation or publication.

---

## Phase 3: User Story 1 - Establish Trustworthy Provenance (Priority: P1)

**Goal**: Acquire and account for all current upstream evidence without changing authoritative artwork.

**Independent Test**: Recompute the inventory and byte-compare both contained SVGs to the synchronized upstream snapshot.

- [x] T010 [P] [US1] Copy authoritative SVG masters byte for byte into `brands/eso-weave/assets/source/`
- [x] T011 [P] [US1] Copy Inter Regular, Medium, SemiBold, and OFL evidence into `brands/eso-weave/fonts/`
- [x] T012 [P] [US1] Copy required rendered reference assets into `brands/eso-weave/assets/reference/`
- [x] T013 [P] [US1] Copy current brand, product-voice, legal, reproduction, and full S012 historical evidence into `brands/eso-weave/provenance/`
- [x] T014 [US1] Record every acquired file, path mapping, hash, media fact, role, usage basis, and provenance class in `specs/020-eso-weave-provenance-kit/source-inventory.json`
- [x] T015 [US1] Add deterministic source-inventory and byte-preservation validation in `skill/templates/brand_contract.py` and `skill/templates/test_brand_contract.py`
- [x] T016 [US1] Document the operator-supplied origin statement and public-history boundary in `brands/eso-weave/NOTES.md` and `specs/020-eso-weave-provenance-kit/evidence.md`

**Checkpoint**: One complete auditable inventory exists, authoritative SVG hashes match intake and current upstream, and no derivative production geometry exists.

---

## Phase 4: User Story 2 - Approve Faithful Derivatives (Priority: P1)

**Goal**: Present a complete hash-bound derivative, palette, and missing-typography proposal before production construction.

**Independent Test**: Inspect the Gate 1 packet for exact source hashes, all required derivatives, eight proof contexts per proposal, measurements, transformation boundaries, and recommendations.

- [x] T017 [P] [US2] Measure authoritative mark and glyph bounds, strokes, color roles, silhouette, and small-size behavior into `specs/020-eso-weave-provenance-kit/gate-1-proposal.json`
- [x] T018 [P] [US2] Measure upstream Inter metadata and the locally available Geist Mono candidate with license and hashes in `specs/020-eso-weave-provenance-kit/gate-1-proposal.json`
- [x] T019 [US2] Define proposed reduced, horizontal, stacked, wordmark-only, single-ink, and platform-icon transformation boundaries in `specs/020-eso-weave-provenance-kit/gate-1-proposal.json`
- [x] T020 [US2] Generate ignored source-only light and dark size proofs under `dist/eso-weave-approval/gate-1/`
- [x] T021 [US2] Add the Gate 1 narrative, measurements, recommendations, palette candidates, and typography recommendation to `specs/020-eso-weave-provenance-kit/evidence.md`
- [x] T022 [US2] Re-fetch ESO Weave and prove the proposal hashes remain current in `specs/020-eso-weave-provenance-kit/evidence.md`
- [x] T023 [US2] Present the exact Gate 1 packet to the owner and halt before creating any production derivative geometry
- [x] T024 [US2] Record the owner's hash-bound Gate 1 decision in `specs/020-eso-weave-provenance-kit/gate-1-proposal.json` and `specs/020-eso-weave-provenance-kit/evidence.md`, ready for T025 to project into the production source contract

**Checkpoint**: Gate 1 is explicitly approved against current source hashes, or the slice remains halted.

---

## Phase 5: User Story 3 - Build a Complete Ownership-Safe Kit (Priority: P2)

**Goal**: Generate the complete private current-spec kit from approved sources and transformations.

**Independent Test**: Build only ESO Weave offline and confirm complete deliverables, zero prohibited claims, required legal boundaries, zero verifier problems, zero glyph failures, and no public projection.

- [x] T025 [US3] Add the approved strategy, affiliation, legal boundary, semantic colors, palette approvals, fixed typography, authoritative inputs, and approval ledger to `brands/eso-weave/brand.json`
- [x] T026 [P] [US3] Author human and agent entry points in `brands/eso-weave/README.md` and `brands/eso-weave/SKILL.md`
- [x] T027 [P] [US3] Author the representative desktop UI specimen in `brands/eso-weave/ui_kits/eso-weave-desktop/index.html` and `brands/eso-weave/ui_kits/eso-weave-desktop/README.md`
- [x] T028 [US3] Extend authoritative SVG composition support for the approved source-preserving derivative set in `skill/templates/gen_logo.py`
- [x] T029 [US3] Add Gate 1 enforcement and derivative provenance to generated manifests and verification in `skill/templates/gen_logo.py` and `skill/templates/verify.py`
- [x] T030 [P] [US3] Add vendor-boundary projection to guideline, PDF, enforcement, and portable outputs in `skill/templates/gen_guidelines.py`, `skill/templates/gen_guide_pdf.py`, and `skill/templates/gen_enforcement.py`
- [x] T031 [P] [US3] Add fixed Inter and approved mono font coverage to generated CSS, framework bindings, specimens, and manifests in the existing generator templates
- [x] T032 [US3] Register ESO Weave as a production build source while keeping publication disabled in `scripts/build_all.py`
- [x] T033 [US3] Add complete ESO Weave pipeline regressions in `skill/templates/test_pipeline.py` and source-contract tests in `skill/templates/test_brand_contract.py`
- [x] T034 [US3] Build the private ESO Weave kit and record complete artifact, glyph, verifier, affiliation, disclaimer, image, PDF, pagination, and mojibake evidence in `specs/020-eso-weave-provenance-kit/evidence.md`
- [x] T035 [US3] Verify public site and registry output still excludes ESO Weave before Gate 2 using `scripts/test_prepare_site.py`

**Checkpoint**: The complete verified private kit exists under `dist/`, but no ESO Weave public surface exists.

---

## Phase 6: User Story 4 - Publish Only the Approved Representation (Priority: P3)

**Goal**: Present the complete private kit and exact public surface set, then publish only after owner approval.

**Independent Test**: Compare final source and derivative hashes with Gate 1, inspect the finished guide and UI specimen, review all verification evidence, and prove site projection changes only after Gate 2 approval.

- [x] T036 [US4] Re-fetch ESO Weave and compare all bound hashes immediately before Gate 2 in `specs/020-eso-weave-provenance-kit/evidence.md`
- [x] T037 [US4] Generate the ignored Gate 2 guide, PDF, UI specimen, derivative sheet, manifests, verification report, and exact surface list under `dist/eso-weave-approval/gate-2/`
- [x] T038 [US4] Present the exact Gate 2 packet to the owner and halt before publication
- [x] T039 [US4] Record the owner's Gate 2 decision and exact approved surfaces in `specs/020-eso-weave-provenance-kit/evidence.md` and `brands/eso-weave/brand.json`
- [x] T040 [US4] Enable only the approved generated site, registry, metadata, social, guideline, and download projections in `scripts/prepare_site.py` and derived site data
- [x] T041 [US4] Add publication and stale-approval regression coverage in `scripts/test_prepare_site.py` and `site/tests/site.test.mjs`
- [x] T042 [US4] Build all six production kits and the complete site, then record final public-surface evidence in `specs/020-eso-weave-provenance-kit/evidence.md`

**Checkpoint**: ESO Weave is public only through the approved generated surface set and all boundaries remain intact.

---

## Phase 7: Polish and Delivery

**Purpose**: Close cross-cutting documentation, validation, and hosted review.

- [x] T043 Update the unreleased feature and dated architectural decision in `CHANGELOG.md`
- [x] T044 [P] Update the production brand inventory and contributor entry points in `README.md` and relevant skill documentation
- [x] T045 Run the complete command sequence in `specs/020-eso-weave-provenance-kit/quickstart.md` and resolve every failure
- [x] T046 Audit committed files for generated artifacts, authoritative-source drift, UTF-8 BOM, CRLF, mojibake, and accidental user-state changes
- [x] T047 Re-run Spec Kit cross-artifact analysis and resolve all CRITICAL or HIGH findings across `specs/020-eso-weave-provenance-kit/`
- [x] T048 Mark completed implementation tasks in `specs/020-eso-weave-provenance-kit/tasks.md` and finalize `specs/020-eso-weave-provenance-kit/evidence.md`
- [ ] T049 Commit S020 with Conventional Commit subjects, push `codex/020-eso-weave-provenance-kit`, and publish the official issue-closing pull request
- [ ] T050 Reconcile every CI result and first-round Codex review comment, applying and replying to necessary changes
- [ ] T051 Request at most one authorized second Codex review round, reconcile every response, and return only when CI and reviews are satisfied

## Dependencies and Execution Order

- Phase 1 precedes all implementation.
- Phase 2 test-first contracts precede production source registration.
- User Story 1 provides the hashes and evidence required by User Story 2.
- T023 is a mandatory owner halt. T024 through T051 cannot proceed without Gate 1 approval.
- User Story 3 creates a complete private kit and must prove that publication remains disabled.
- T038 is a mandatory owner halt. T039 through T051 cannot proceed without Gate 2 approval.
- Final delivery depends on the complete local validation gate.

## Parallel Opportunities

- T003 and T004 can proceed independently after branch setup.
- T006 and T007 can be written alongside T005 before shared contract implementation.
- T010 through T013 acquire independent source classes.
- T017 and T018 measure different evidence classes.
- T026 and T027 author independent source documents after Gate 1.
- T030 and T031 affect separate generator concerns after core derivative support exists.

## Implementation Strategy

The source inventory is the first independently verifiable increment. Gate 1 deliberately separates evidence and proposal from production derivative construction. Gate 2 deliberately separates a complete private kit from public projection. No MVP shortcut may bypass either boundary.

## Notes

- The custom checklist remains reviewer-owned. The autopilot kickoff authorizes implementation to proceed despite unchecked requirements-review items, but does not authorize marking them complete.
- Task completion markers track implementation only and never stand in for owner approval.
