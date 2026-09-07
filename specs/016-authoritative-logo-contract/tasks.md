# Tasks: Authoritative Logo Source Contract

**Input**: Design documents from `specs/016-authoritative-logo-contract/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, and quickstart.md

**Tests**: S016 explicitly requires test-first coverage for the complete issue #151 regression matrix, generated provenance, and production migration invariants.

**Organization**: Tasks are chronological and grouped by independently testable user story.

## Phase 1: Setup and Baseline

**Purpose**: Establish traceability and immutable identity baselines before contract changes.

- [x] T001 Record issue #151 scope, source-mode decisions, and no-redesign boundary in `specs/016-authoritative-logo-contract/spec.md`
- [x] T002 Capture all production logo path fingerprints and authoritative input SHA-256 values in `specs/016-authoritative-logo-contract/evidence.md`
- [x] T003 [P] Verify Spec Kit selection, ignore boundaries, CI commands, and clean feature-branch state in `specs/016-authoritative-logo-contract/evidence.md`

---

## Phase 2: Foundational Contract Design

**Purpose**: Synchronize the schema, model, and operator contract that block both implementation stories.

**Critical**: No source enforcement or provenance work begins until the common vocabulary and closed transformations are stable.

- [x] T004 Define constructed and authoritative mode invariants in `specs/016-authoritative-logo-contract/contracts/source-authority.md`
- [x] T005 Define deterministic derivative inventory and validation rules in `specs/016-authoritative-logo-contract/contracts/derivative-provenance.md`
- [x] T006 Add required logo source mode, authoritative bindings, and closed transformation values to `skill/references/canon.schema.json`
- [x] T007 Add reusable source-mode, variant-binding, and authoritative-record helpers to `skill/templates/brand_contract.py`

**Checkpoint**: One contract vocabulary governs authoring, generation, and verification.

---

## Phase 3: User Story 1 - Bind Approved Marks to Immutable Sources (Priority: P1) MVP

**Goal**: Reject every ambiguous or substituted source before publishable output exists.

**Independent Test**: A valid temporary authoritative brand passes; unrelated geometry, stale sources, bad roles, reference-only sources, omitted bindings, constructed-mode conflicts, and `build/mk_paths.py` each fail contract preflight.

### Tests for User Story 1

- [x] T008 [US1] Add failing positive and negative source-mode cases to `skill/templates/test_brand_contract.py`
- [x] T009 [US1] Add failing issue #151 path-substitution, reduced-redraw, and construction-helper cases to `skill/templates/test_brand_contract.py`
- [x] T010 [P] [US1] Add failing schema-shape and five-brand migration assertions to `scripts/test_release_contract.py`

### Implementation for User Story 1

- [x] T011 [US1] Enforce explicit source mode and mode-specific field exclusivity in `skill/templates/brand_contract.py`
- [x] T012 [US1] Resolve Full and Reduced IDs to approved role-correct current inputs in `skill/templates/brand_contract.py`
- [x] T013 [US1] Reject mixed authoritative geometry, source mismatch, aspect distortion, and staged construction helpers in `skill/templates/brand_contract.py`
- [x] T014 [US1] Make contract-preflight failures actionable and authority-specific in `skill/templates/validate_brand.py` and `skill/templates/build_kit.py`
- [x] T015 [US1] Run and record the focused source-authority tests in `specs/016-authoritative-logo-contract/evidence.md`

**Checkpoint**: Authoritative source substitution is impossible through the normal preflight path.

---

## Phase 4: User Story 2 - Preserve Provenance Through Every Derivative (Priority: P1)

**Goal**: Make every generated mark and lockup traceable to its bound source and reject altered or stale lineage.

**Independent Test**: ShruggieTech generation emits a complete deterministic logo index and matching SVG metadata; valid recolors and lockups pass, while tampered metadata, unknown operations, missing records, and changed raster masks fail verification.

### Tests for User Story 2

- [x] T016 [US2] Add failing SVG metadata, provenance inventory, valid recolor, and lockup lineage cases to `skill/templates/test_pipeline.py`
- [x] T017 [US2] Add failing missing, extra, duplicate, stale, undeclared-operation, and silhouette-tamper verification cases to `skill/templates/test_pipeline.py`
- [x] T018 [P] [US2] Add failing verified-master handoff assertions to `skill/templates/test_iconkit.py`

### Implementation for User Story 2

- [x] T019 [US2] Attach authoritative source metadata to generated mark and lockup SVG roots in `skill/templates/gen_logo.py`
- [x] T020 [US2] Emit deterministic SVG and PNG derivative records to `logos/provenance.json` in `skill/templates/gen_logo.py`
- [x] T021 [US2] Validate authoritative derivative inventory, hashes, operations, and SVG metadata in `skill/templates/verify.py`
- [x] T022 [US2] Validate raster source aspect ratio and normalized alpha or luminance mask topology in `skill/templates/verify.py`
- [x] T023 [US2] Bind platform icon manifests to provenance-verified logo masters in `skill/templates/iconkit.py`
- [x] T024 [US2] Prove guidelines and downstream icon generation reuse indexed masters in `skill/templates/test_pipeline.py` and `skill/templates/test_iconkit.py`
- [x] T025 [US2] Run and record focused provenance, glyph, and platform tests in `specs/016-authoritative-logo-contract/evidence.md`

**Checkpoint**: Every authoritative logo derivative has independently verifiable lineage.

---

## Phase 5: User Story 3 - Keep Constructed Identities Explicit and Compatible (Priority: P2)

**Goal**: Migrate production brands and operator guidance without changing approved identity content.

**Independent Test**: All five production brands validate with explicit source modes, constructed path fingerprints and authoritative source hashes match baseline, and every kit builds with zero verifier and glyph failures.

### Tests for User Story 3

- [x] T026 [US3] Add production migration and unchanged-identity assertions to `scripts/test_release_contract.py`

### Implementation for User Story 3

- [x] T027 [US3] Declare constructed mode for Covarity, Fragcap, Glitchpad, and Go Schedule in `brands/covarity/brand.json`, `brands/fragcap/brand.json`, `brands/glitchpad/brand.json`, and `brands/go-schedule/brand.json`
- [x] T028 [US3] Declare authoritative mode, Full and Reduced bindings, and required operations in `brands/shruggietech/brand.json`
- [x] T029 [US3] Update approval interview, fresh reapproval requirements, and identity-construction rules in `skill/SKILL.md`, `skill/references/03-interview.md`, and `skill/references/08-glyph-construction.md`
- [x] T030 [US3] Update portability and generated-output provenance guidance in `skill/references/09-portability.md` and `brands/shruggietech/README.md`
- [x] T031 [US3] Reconfirm path fingerprints, authoritative source hashes, colors, and public presentation invariants in `specs/016-authoritative-logo-contract/evidence.md`

**Checkpoint**: Production is fully migrated with zero identity drift.

---

## Phase 6: Polish, Verification, and Publication

**Purpose**: Close documentation, complete repository gates, publish, and resolve automated review.

- [x] T032 Update S016 feature and dated contract-decision entries in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [x] T033 Run Spec Kit cross-artifact analysis and resolve every material finding across `specs/016-authoritative-logo-contract/spec.md`, `specs/016-authoritative-logo-contract/plan.md`, and `specs/016-authoritative-logo-contract/tasks.md`
- [x] T034 Run the focused contract, pipeline, icon, glyph, release-contract, prepare-site, and Markdown checks from `specs/016-authoritative-logo-contract/quickstart.md`
- [x] T035 Run the complete five-kit, release, site, browser, accessibility, encoding, mojibake, and repository-hygiene gate and record results in `specs/016-authoritative-logo-contract/evidence.md`
- [x] T036 Push `codex/016-authoritative-logo-contract`, publish the official issue-closing PR, and record the URL in `specs/016-authoritative-logo-contract/evidence.md`
- [ ] T037 Wait for the automatic Codex review, answer and resolve every finding, optionally request exactly one second round, and record final green CI and review state in `specs/016-authoritative-logo-contract/evidence.md`

---

## Dependencies and Execution Order

- Phase 1 establishes immutable evidence for SC-005.
- Phase 2 blocks both P1 stories because the generator and verifier must derive from the same source contract.
- User Story 1 blocks User Story 2 because generation must receive validated bindings.
- User Story 3 depends on both P1 stories so production migration cannot temporarily weaken existing builds.
- Phase 6 follows all user stories and contains the mandatory analyze gate before implementation completion is claimed.

## Parallel Opportunities

- T003 can run while baseline identity fingerprints are collected.
- T010 can be authored separately from the core brand-contract tests.
- T018 can be authored separately from generator provenance tests.
- Documentation files in T029 and T030 can be updated independently once the contract terminology is final.

## Implementation Strategy

1. Make the contract fail for every unsafe state before production migration.
2. Generate and independently verify authoritative derivative lineage.
3. Migrate each production definition with byte- and path-preservation evidence.
4. Run focused tests, then the full build and publication loop.

## Notes

- Tests precede implementation within each story.
- Custom checklist markers represent reviewer approval of requirements quality, not implementation completion.
- Do not commit generated kits, provenance indexes, release archives, PDFs, PNGs, or site exports.
- Do not trigger more than one manual second Codex review round.
