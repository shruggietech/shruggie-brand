# Tasks: Cross-Host Conformance Fixtures

**Input**: Design documents from `specs/040-cross-host-conformance/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Required by the specification and autopilot protocol. Contract and integration tests precede implementation.

**Organization**: Tasks are grouped by independently testable user story after shared contract foundations.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it changes different files and has no dependency on another incomplete task.
- **[Story]**: Maps to a user story in `spec.md`.
- Every task names the exact repository path it changes or validates.

## Phase 1: Setup and Test-First Contract

**Purpose**: Establish failing tests and the governed source locations before implementation.

- [x] T001 Add failing policy, profile, evidence-substitution, diagnostic, trace, and baseline-decision tests in `skill/templates/test_conformance.py`
- [x] T002 [P] Add failing deterministic per-kit generation and artifact-boundary tests in `skill/templates/test_pipeline.py`
- [x] T003 [P] Add failing site-staging tests for verified conformance inputs in `scripts/test_prepare_site.py`

---

## Phase 2: Foundational Conformance Contract

**Purpose**: Implement the shared contract, validation, trace evaluation, and generator required by every user story.

**Critical**: No user-story implementation begins until this phase passes its focused tests.

- [x] T004 Create the canonical profile, host, trace, diagnostic, and baseline policy in `skill/references/conformance-contract.json`
- [x] T005 [P] Create the human-only source decision ledger in `skill/references/conformance-baseline-decisions.json`
- [x] T006 Implement fail-closed contract loading, evidence validation, trace evaluation, diagnostic validation, and baseline-decision validation in `skill/templates/conformance_contract.py`
- [x] T007 Implement deterministic per-brand manifest, fixture source, evidence, and browser-harness generation in `skill/templates/gen_conformance.py`
- [x] T008 Integrate conformance generation into `skill/templates/build_kit.py` and synthetic pipeline setup in `skill/templates/test_pipeline.py`

**Checkpoint**: Canonical contract tests pass, the known-bad trace fails for the intended reasons, the corrected trace passes, and identical inputs generate identical bytes.

---

## Phase 3: User Story 1 - Public Browser Reference (Priority: P1)

**Goal**: Publish and verify one generated conformance route for every production brand across the required browser profiles.

**Independent Test**: Build the site and exercise `/conformance/` plus every `/conformance/{slug}/` route with Playwright and axe.

### Tests for User Story 1

- [x] T009 [US1] Complete failing browser staging and production-brand inventory assertions in `scripts/test_prepare_site.py`
- [x] T010 [P] [US1] Add failing route, profile, accessibility, interaction, and screenshot-candidate assertions in `site/tests/site.test.mjs` and `site/scripts/verify-site.mjs`

### Implementation for User Story 1

- [x] T011 [US1] Stage verified per-kit conformance records and browser specimens in `scripts/prepare_site.py`
- [x] T012 [P] [US1] Add typed generated conformance loading in `site/lib/conformance.ts`
- [x] T013 [P] [US1] Add the browser profile control and evidence presentation in `site/components/conformance-reference.tsx`
- [x] T014 [US1] Add the public index and per-brand routes in `site/app/(site)/conformance/page.tsx` and `site/app/(site)/conformance/[slug]/page.tsx`
- [x] T015 [US1] Add governed conformance presentation styles in `site/app/globals.css`
- [x] T016 [US1] Complete browser profile, WCAG 2.1 AA, keyboard, focus, target, scaling, motion, orientation, resize, IME, and candidate capture checks in `site/scripts/verify-site.mjs`

**Checkpoint**: Every production brand is reachable from the public conformance index and passes every supported browser profile with distinct diagnostics.

---

## Phase 4: User Story 2 - Executable Host Boundaries (Priority: P2)

**Goal**: Produce independently executable Tauri, Wails, and egui reference-fixture evidence that cannot be replaced by browser proof.

**Independent Test**: Run the generated Rust, Go, and egui commands and validate their exact evidence classes and support records.

### Tests for User Story 2

- [x] T017 [US2] Complete failing Rust, Go, egui mapping, tool-version, and browser-substitution tests in `skill/templates/test_conformance.py`

### Implementation for User Story 2

- [x] T018 [US2] Generate the locked dependency-free Tauri Android Rust ownership fixture in `skill/templates/gen_conformance.py`
- [x] T019 [US2] Generate the dependency-free Wails Windows Go window-chrome fixture in `skill/templates/gen_conformance.py`
- [x] T020 [US2] Bind existing native egui rendered-state evidence into the conformance manifest in `skill/templates/gen_conformance.py`
- [x] T021 [US2] Execute available generated host fixtures through hidden non-interactive child processes and validate results in `skill/templates/test_conformance.py`

**Checkpoint**: Each native reference track runs through its own entry point, reports exact tool versions, and rejects evidence from any other track.

---

## Phase 5: User Story 3 - Safe-Area Regression (Priority: P3)

**Goal**: Make the generic Glitchpad-style Android display-cutout failure reproducible and prove the corrected AppFrame ownership through every required transition.

**Independent Test**: Evaluate the canonical known-bad and corrected traces in Python and generated Rust, then compare diagnostic codes and usable geometry.

### Tests for User Story 3

- [x] T022 [US3] Complete failing duplicate-inset, obstruction, orientation, IME, resize, and mixed-input trace assertions in `skill/templates/test_conformance.py`

### Implementation for User Story 3

- [x] T023 [US3] Implement trace-state ownership and usable-geometry evaluation in `skill/templates/conformance_contract.py`
- [x] T024 [US3] Emit known-bad and corrected trace evidence plus distinct host-boundary diagnostics in `skill/templates/gen_conformance.py`

**Checkpoint**: The known-bad trace deterministically fails for duplicate ownership and obstruction, while the corrected trace passes all transitions with reachable controls.

---

## Phase 6: User Story 4 - Human-Only Baseline Review (Priority: P4)

**Goal**: Produce reviewable visual candidates and reject automatic, incomplete, stale, or mismatched acceptance.

**Independent Test**: Generate candidate metadata and exercise every acceptance rejection path plus one valid human decision fixture.

### Tests for User Story 4

- [x] T025 [US4] Complete failing candidate identity and human-only decision tests in `skill/templates/test_conformance.py`

### Implementation for User Story 4

- [x] T026 [US4] Implement normalized visual candidate identity and decision-ledger validation in `skill/templates/conformance_contract.py`
- [x] T027 [US4] Emit browser candidate manifests beside ignored screenshots in `site/scripts/verify-site.mjs`
- [x] T028 [US4] Upload ephemeral candidate screenshots and manifests without promotion in `.github/workflows/build.yml`

**Checkpoint**: Candidate evidence is reviewable and checksummed, while no automated code path can create an accepted decision.

---

## Phase 7: Verification, Evidence, and Handoff

**Purpose**: Connect all stories to production gates and record complete evidence.

- [x] T029 Integrate distinct conformance verification checks into `skill/templates/verify.py` and manifest coverage into `skill/templates/test_pipeline.py`
- [x] T030 Add `test_conformance.py` to Python 3.8 and authoritative build jobs in `.github/workflows/build.yml`
- [x] T031 Update `CHANGELOG.md` with the S040 feature and dated architecture decisions
- [x] T032 Run Python compile, focused conformance, Web adapter, egui adapter, site-staging, pipeline, release, and Markdown suites
- [x] T033 Run generated Tauri Rust, Wails Go, and egui Cargo fixture tests using ignored kit output
- [x] T034 Run the full all-brand build and confirm zero `verify.py` problems and zero glyph failures without committing `dist/`
- [x] T035 Run site lint, static export, Node contract tests, Playwright profile checks, axe scans, and publication audit
- [x] T036 Check UTF-8 without BOM, LF endings, mojibake, generated-artifact exclusion, clean staged scope, and synchronized agent instructions
- [x] T037 Record commands, versions, counts, accessibility impact, identity impact, visual-review status, and open evidence boundaries in `specs/040-cross-host-conformance/evidence.md`

---

## Dependencies and Execution Order

### Phase Dependencies

- Phase 1 starts immediately and must produce failing tests.
- Phase 2 depends on Phase 1 and blocks every user story.
- User Story 1 depends on deterministic generated browser conformance data.
- User Story 2 depends on the host and evidence contract but can otherwise proceed independently of site presentation.
- User Story 3 depends on trace evaluation and the generated Tauri fixture.
- User Story 4 depends on the candidate and baseline policy but can proceed independently of native fixture source.
- Phase 7 depends on all four stories.

### User Story Dependencies

- **US1**: Independent public browser reference after Phase 2.
- **US2**: Independent native reference fixtures after Phase 2.
- **US3**: Uses the Tauri fixture from US2 but remains independently testable through canonical trace inputs.
- **US4**: Independent candidate and decision governance after Phase 2.

### Parallel Opportunities

- T002 and T003 can proceed after T001 establishes the shared vocabulary.
- T005 can proceed independently of contract code.
- T012 and T013 can proceed in parallel after staging shape is fixed.
- Rust, Go, and egui generation changes are isolated sections of `gen_conformance.py` but are executed sequentially by one implementer to avoid file conflicts.
- Site candidate capture and native fixture execution can proceed independently after their tests exist.

---

## Parallel Example: Browser and Native Tracks

```text
Task: "Implement staged conformance loading and public routes in site source"
Task: "Implement executable Rust and Go host-envelope fixture generation"
```

---

## Implementation Strategy

### MVP First

1. Finish the contract and deterministic generator.
2. Deliver the browser reference for all production brands.
3. Validate its routes, profiles, accessibility, and interaction checks independently.

### Incremental Delivery

1. Add executable native host tracks and lock evidence classes.
2. Prove the Android known-bad and corrected traces.
3. Add human-only visual candidate governance.
4. Run complete production verification and capture review evidence.

## Notes

- Generated kits, screenshots, site exports, Rust targets, and synthetic inputs remain ignored.
- `[P]` tasks touch different files and have no unresolved dependency.
- Test tasks must fail for the intended missing behavior before implementation.
- A reference fixture never claims downstream consumer adoption.
