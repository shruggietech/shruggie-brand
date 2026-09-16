# Tasks: Embed Specimen Logo

**Input**: Design documents from `specs/034-embed-specimen-logo/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/specimen-portability.md, quickstart.md

**Tests**: Required by issue #204 and the feature specification. Add regressions first and observe the expected failure before implementation.

**Organization**: Tasks are grouped by user story so portability, identity preservation, and future regression detection remain independently traceable.

## Phase 1: Setup and Baseline

**Purpose**: Capture the authoritative issue, identity, branch, environment, and pre-fix failure without modifying governed artwork.

- [x] T001 Record issue #204 acceptance criteria, branch state, toolchain paths, and initial generated-specimen failure in `specs/034-embed-specimen-logo/evidence.md`
- [x] T002 [P] Record authoritative I Heart PR Tours source hashes and governed specimen placement values in `specs/034-embed-specimen-logo/evidence.md`
- [x] T003 [P] Confirm generated-output exclusions and existing archive/site provenance gates in `.gitignore`, `scripts/package_release.py`, and `scripts/prepare_site.py`

---

## Phase 2: Foundational Test Harness

**Purpose**: Establish shared structural, source-identity, raster, and browser measurement paths before changing specimen generation.

- [x] T004 Add failing isolated image-component specimen tests for exact payload bytes, dual self-contained references, traversal rejection, unresolved-reference rejection, and invisible mark pixels in `skill/templates/test_pipeline.py`
- [x] T005 [P] Add failing hosted-copy byte-equivalence coverage for specimen publication in `scripts/test_prepare_site.py`
- [x] T006 [P] Add failing exact-route, direct-navigation, offline-opening, self-contained-reference, and mark-region pixel assertions in `site/scripts/verify-site.mjs`
- [x] T007 Run the focused pre-implementation tests and record the expected failures in `specs/034-embed-specimen-logo/evidence.md`

**Checkpoint**: The test harness reproduces the broken relative dependency and distinguishes syntactic success from visible artwork.

---

## Phase 3: User Story 1 - Open a complete portable specimen (Priority: P1) MVP

**Goal**: Make every generated image-backed specimen self-contained so direct hosted and offline local opening show the approved mark.

**Independent Test**: Build I Heart PR Tours, enumerate every specimen reference, then open the exact output through the browser server and `file:` paths without its source directory.

### Tests for User Story 1

- [x] T008 [US1] Confirm T004 and T006 fail on the current `../assets/source/vertical_darkbg.svg` dependency before generator changes in `skill/templates/test_pipeline.py` and `site/scripts/verify-site.mjs`

### Implementation for User Story 1

- [x] T009 [US1] Add contained source resolution, explicit media-type mapping, and exact-byte base64 data-URI construction in `skill/templates/build_specimen.py`
- [x] T010 [US1] Emit the identical embedded value in `href` and `xlink:href` while retaining existing component attributes and a stable specimen-mark identifier in `skill/templates/build_specimen.py`
- [x] T011 [US1] Build I Heart PR Tours and record zero unresolved references plus successful hosted and offline rendering in `specs/034-embed-specimen-logo/evidence.md`

**Checkpoint**: The exact I Heart PR Tours specimen is portable and visibly complete in both user opening paths.

---

## Phase 4: User Story 2 - Preserve the approved identity during embedding (Priority: P1)

**Goal**: Prove the portability repair changes transport only, not authoritative artwork or placement.

**Independent Test**: Decode the specimen payload, compare it byte-for-byte to the governed source, compare the image and group geometry contract, and run identity continuity validation.

### Tests for User Story 2

- [x] T012 [P] [US2] Add exact decoded-source and unchanged component-geometry assertions for the synthetic and I Heart PR Tours specimens in `skill/templates/test_pipeline.py`
- [x] T013 [P] [US2] Preserve and compare before/after authoritative source hashes and governed placement values in `specs/034-embed-specimen-logo/evidence.md`

### Implementation for User Story 2

- [x] T014 [US2] Add production specimen verification for reference allowlisting, matching dual attributes, decoded governed-source bytes, media type, and component geometry in `skill/templates/verify.py`
- [x] T015 [US2] Run I Heart PR Tours identity, glyph, and verifier gates and record exact zero-failure evidence in `specs/034-embed-specimen-logo/evidence.md`

**Checkpoint**: Exact source bytes, geometry, placement, colors, and transparency remain authoritative and unchanged.

---

## Phase 5: User Story 3 - Detect future specimen artwork regressions (Priority: P2)

**Goal**: Make unresolved dependencies, invisible mark regions, and publication-copy drift fail automated validation.

**Independent Test**: Mutate isolated output to a relative reference and to invisible artwork, confirm named failures, then verify the repaired production kit, archive provenance, hosted copy, and browser paths.

### Tests for User Story 3

- [x] T016 [P] [US3] Complete mutation regressions for unresolved dependency and invisible rendered mark failures in `skill/templates/test_pipeline.py`
- [x] T017 [P] [US3] Complete exact hosted-copy and deterministic archive specimen equivalence assertions in `scripts/test_prepare_site.py`
- [x] T018 [P] [US3] Complete hosted direct-navigation and offline rendered-pixel coverage for the exact published SVG in `site/scripts/verify-site.mjs`

### Implementation for User Story 3

- [x] T019 [US3] Add capability-aware whole-specimen rasterization and mark-region non-background pixel measurement with explicit skip semantics in `skill/templates/verify.py`
- [x] T020 [US3] Integrate specimen portability and rendered-mark checks into the production verifier report in `skill/templates/verify.py`
- [x] T021 [US3] Enforce byte-identical source-to-hosted specimen copying on the existing verified publication path in `scripts/prepare_site.py`
- [x] T022 [US3] Run focused mutations, publication tests, and browser paths and record their pass/fail behavior in `specs/034-embed-specimen-logo/evidence.md`

**Checkpoint**: Structural, identity, renderer, browser, offline, archive, and hosted-copy regressions all fail closed.

---

## Phase 6: Polish and Cross-Cutting Verification

**Purpose**: Synchronize governance artifacts, run every authoritative gate, and prepare the local pre-push commit.

- [x] T023 [P] Add the S034 issue #204 correction and dated non-architectural decision entry to `CHANGELOG.md`
- [x] T024 Re-run cross-artifact analysis and reconcile `specs/034-embed-specimen-logo/spec.md`, `plan.md`, `tasks.md`, contract, data model, quickstart, implementation, and evidence
- [x] T025 Run Python 3.8 compatibility compilation and the complete Python publication, release, identity, icon, pipeline, and Markdown suites; record results in `specs/034-embed-specimen-logo/evidence.md`
- [x] T026 Run capability probing, all-production-kit generation, per-kit `verify.py`, per-kit `validate_glyph.py`, release packaging/certification, and generated-agent diff; record results in `specs/034-embed-specimen-logo/evidence.md`
- [x] T027 Run `pnpm --dir site lint`, `pnpm --dir site build`, `pnpm --dir site test`, publication audit, and exact hosted/offline specimen checks; record results in `specs/034-embed-specimen-logo/evidence.md`
- [x] T028 Run repository hygiene, generated-artifact exclusion, source-hash, mojibake, LF/UTF-8, diff, and task-completion checks; record results in `specs/034-embed-specimen-logo/evidence.md`
- [x] T029 Commit source, tests, changelog, evidence, and Spec Kit artifacts locally with an S034 Conventional Commit subject, then halt before `git push`

---

## Phase 7: Owner Correction - Wider Stacked Lockup

**Purpose**: Apply the owner's post-review request to replace the canonical vertical full mark with the existing approved wider stacked lockup in the specimen header.

- [x] T030 Record the owner's correction and reconcile the selection requirement across `spec.md`, `plan.md`, `research.md`, `data-model.md`, the portability contract, quickstart, changelog, and evidence
- [x] T031 Add failing generic and production regressions proving approved horizontal-lockup preference, exact payload bytes, centered native proportions, and unchanged canonical fallback behavior in `skill/templates/test_pipeline.py`
- [x] T032 Implement shared approved-lockup resolution in `skill/templates/brand_contract.py` and consume it from `skill/templates/build_specimen.py` and `skill/templates/verify.py`
- [x] T033 Prove `brand.json`, `vertical_darkbg.svg`, and `horizontal_darkbg.svg` remain byte-for-byte authoritative while the generated specimen payload equals `horizontal_darkbg.svg`
- [x] T034 Re-run Python 3.12, Python 3.8, all-kit, `verify.py`, `validate_glyph.py`, release, site, browser, accessibility, publication, and hygiene validation
- [x] T035 Re-run cross-artifact analysis and update final evidence with the wider lockup geometry, payload hash, rendered pixel count, and kit-to-site specimen hash
- [x] T036 Amend the unpublished local S034 Conventional Commit and halt before `git push`

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup and Baseline**: Starts immediately.
- **Foundational Test Harness**: Depends on the baseline and blocks implementation.
- **User Story 1**: Depends on failing portability coverage.
- **User Story 2**: Depends on embedded output from User Story 1 and adds the identity gate.
- **User Story 3**: Depends on the structural and identity verifier foundation, then adds rendered and publication enforcement.
- **Polish**: Depends on all user stories.
- **Owner correction**: Depends on the completed S034 implementation and owner review, then repeats the complete release gate before the local commit is amended.

### User Story Dependencies

- **US1**: Independently delivers portable hosted and offline opening.
- **US2**: Independently proves that transport changes preserve identity bytes and placement; consumes US1 output.
- **US3**: Independently makes recurrence a release failure; consumes US1 output and US2 verifier parsing.

### Within Each User Story

- Add or complete the test first and observe the expected failure.
- Make the smallest governed template or verifier change that satisfies the test.
- Run the story's independent test before advancing.
- Never edit or regenerate authoritative source artwork.

### Parallel Opportunities

- T002 and T003 can run in parallel.
- T005 and T006 can be prepared in parallel after T004 defines the shared contract.
- T012 and T013 can run in parallel.
- T016, T017, and T018 touch separate test surfaces and can run in parallel.
- T023 can proceed after behavior stabilizes while final evidence is assembled.

---

## Parallel Example: User Story 3

```text
Task: "Complete mutation regressions in skill/templates/test_pipeline.py"
Task: "Complete publication equivalence tests in scripts/test_prepare_site.py"
Task: "Complete hosted and offline browser checks in site/scripts/verify-site.mjs"
```

---

## Implementation Strategy

### MVP First

1. Capture baseline and exact source hashes.
2. Add failing structural and browser regression coverage.
3. Embed exact governed source bytes in the specimen generator.
4. Validate hosted and offline I Heart PR Tours rendering.

### Incremental Delivery

1. US1 repairs the visible artifact and removes external dependencies.
2. US2 proves the repair preserves the authoritative identity.
3. US3 converts the defect class into production verifier and browser release gates.
4. Full validation proves all eight brands, release artifacts, and site publication remain healthy.

## Notes

- `[P]` tasks touch different files and can proceed concurrently when prerequisites are satisfied.
- Custom checklist markers remain reviewer-owned and do not track implementation completion.
- The static generator has no authentication, private data, storage, user input, or tenant boundary. Path containment and URI/publication integrity are the applicable security controls.
- Never commit generated `dist/`, `site/out/`, PDFs, raster exports, registries, release archives, or synthetic fixtures.
