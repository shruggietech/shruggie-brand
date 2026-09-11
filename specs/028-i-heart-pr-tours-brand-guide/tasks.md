# Tasks: Identity-Locked I Heart PR Tours Brand Guide

**Input**: Design documents from `specs/028-i-heart-pr-tours-brand-guide/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Tests**: S028 requires test-first coverage for source authority, exact-byte preservation, transformations, approval staleness, third-party affiliation, private publication, accessibility, unsafe paths, and the complete build.

**Organization**: Tasks are chronological, grouped by independently testable user story, and interrupted only by the two mandatory owner gates and the final owner merge gate.

## Phase 1: Specification and planning baseline

**Purpose**: Bind S028 to issue #188, merged S027, repository law, and a complete reviewable work order.

- [X] T001 Record branch `codex/028-i-heart-pr-tours-brand-guide`, issue #188, baseline `435019dbc37e754fd1f0b16228a576c985e9468a`, and S027/S016 dependencies in `specs/028-i-heart-pr-tours-brand-guide/spec.md`
- [X] T002 Create and validate the stakeholder specification in `specs/028-i-heart-pr-tours-brand-guide/spec.md` and `specs/028-i-heart-pr-tours-brand-guide/checklists/requirements.md`
- [X] T003 Run clarification coverage analysis, record the no-question result and explicit defaults in `specs/028-i-heart-pr-tours-brand-guide/spec.md`
- [X] T004 Generate the reviewer-owned source, privacy, gate, font, transformation, accessibility, and publication checklist in `specs/028-i-heart-pr-tours-brand-guide/checklists/intake.md`
- [X] T005 Complete Phase 0 and Phase 1 planning in `specs/028-i-heart-pr-tours-brand-guide/plan.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

---

## Phase 2: User Story 1 - Approve exact source authority (Priority: P1)

**Goal**: Produce a private, complete, hash-bound Gate 1 packet without committing source or generating production derivatives.

**Independent Test**: The packet accounts for every explicitly in-scope intake file, excludes unrelated neighboring material, identifies every authority decision and unavailable variant, and leaves `brands/i-heart-pr-tours/` absent.

- [X] T006 [US1] Locate only explicitly named intake candidates and record the restricted-discovery rule in `specs/028-i-heart-pr-tours-brand-guide/research.md`
- [X] T007 [US1] Hash and inspect format, page, creator, and dimension metadata for the supplied guide in ignored `dist/i-heart-pr-tours/gate-1/intake.json`
- [X] T008 [US1] Inspect guide text, embedded font names, embedded raster occurrences, and vector-object counts without extracting a production master; record findings in ignored `dist/i-heart-pr-tours/gate-1/intake.json`
- [X] T009 [P] [US1] Measure all eight guide colors in sRGB, OKLCH, and representative black/white contrast pairs in ignored `dist/i-heart-pr-tours/gate-1/palette.json`
- [X] T010 [P] [US1] Research official font identity and licensing sources and record the Source Sans 3/Pro and logo-lettering distinctions in `specs/028-i-heart-pr-tours-brand-guide/research.md`
- [X] T011 [P] [US1] Capture retrieval-dated official-site voice and use-context evidence without downloading media in ignored `dist/i-heart-pr-tours/gate-1/context.json`
- [X] T012 [US1] Generate a review-only guide overview and embedded-heart occurrence sheet in ignored `dist/i-heart-pr-tours/gate-1/contact-sheet.png`
- [X] T013 [US1] Write the proposed per-role authority, transformation, font, affiliation, privacy, credit, and publication decisions in ignored `dist/i-heart-pr-tours/gate-1/gate-1.json`
- [X] T014 [US1] Generate the operator-readable Gate 1 packet with exact digests and blocked deliverables in ignored `dist/i-heart-pr-tours/gate-1/README.md`
- [X] T015 [US1] Confirm `brands/i-heart-pr-tours/` is absent, generated evidence is ignored, unrelated files are excluded, and committed Spec Kit prose contains no private path in `specs/028-i-heart-pr-tours-brand-guide/evidence.md`
- [X] T016 [US1] **OWNER GATE 1** Halt for explicit approval of exact candidate `iheartpr-g1-r2`, including source hashes, role hierarchy, font files, safe embedded-PNG SVG support, transformations, affiliation, privacy, service credit, publication classification, and wordmark-only and monochrome omissions

**Checkpoint**: No production brand source or derivative exists before Gate 1.

---

## Phase 3: Foundational promotion and tests (after Gate 1)

**Purpose**: Convert the approved packet into fail-closed source and regression contracts before generating a kit.

**Critical**: Update the exact source destination filenames in this task list from the approved Gate 1 authority manifest before T017. No implementation proceeds from provisional filenames.

- [X] T017 Add failing approved-input, exact-byte, format, mask, transformation, private-publication, affiliation, and font-contract fixtures to `skill/templates/test_brand_contract.py`
- [X] T018 [P] Add failing canonical-candidate, source inventory, proof matrix, palette qualification, renderer, staleness, and promotion tests to `skill/templates/test_identity_continuity.py`
- [X] T019 [P] Add failing I Heart PR Tours discovery, build-boundary, site-exclusion, and private-path regressions to `skill/templates/test_pipeline.py` and `scripts/test_prepare_site.py`
- [X] T020 Run T017 through T019 and record the expected red baseline in `specs/028-i-heart-pr-tours-brand-guide/evidence.md`
- [X] T021 Promote approved source bytes through `skill/templates/promote_identity.py` into the exact Gate 1 destinations under `brands/i-heart-pr-tours/assets/`
- [X] T022 Add the approved source contract, independent third-party affiliation, private publication values, palette roles, typography, product voice, and logo bindings in `brands/i-heart-pr-tours/brand.json`
- [X] T023 Add the approved source inventory, renderer contract, palette qualification, comparison evidence, and owner approval in `brands/i-heart-pr-tours/identity-continuity.json`
- [X] T024 Add source authority, prohibited uses, typography, palette, imagery, accessibility, and publication notes in `brands/i-heart-pr-tours/README.md`
- [X] T025 Add only the narrow schema, generator, verifier, or promotion changes demonstrated necessary by approved-source tests in `skill/references/canon.schema.json` and `skill/templates/`
- [X] T026 Run the focused contract, continuity, promotion, pipeline, and site-preparation tests and record the green result in `specs/028-i-heart-pr-tours-brand-guide/evidence.md`

**Checkpoint**: Approved bytes are promoted exactly, every negative contract fails closed, and the brand remains private.

---

## Phase 4: User Story 2 - Preserve and bind the approved identity (Priority: P1)

**Goal**: Prove every identity output comes from one approved source and transformation without reconstruction.

**Independent Test**: A private build preserves exact source bytes, rejects all drift classes before derivatives, and emits complete lineage and comparison evidence.

- [X] T027 [US2] Implement approved authoritative Full, Reduced, lockup, wordmark, and favicon bindings required by Gate 1 in `brands/i-heart-pr-tours/brand.json` and the narrowly affected `skill/templates/` modules
- [X] T028 [US2] Encode only approved per-source transformations and blocked variants in `brands/i-heart-pr-tours/brand.json`
- [X] T029 [US2] Generate and verify all required 256/64/32/16 pixel proof coordinates on approved light and dark surfaces under ignored `dist/i-heart-pr-tours/gate-2/`
- [X] T030 [US2] Validate exact source-to-output lineage, framing, topology, color placement, renderer settings, and comparison artifacts in ignored `dist/i-heart-pr-tours/qc/`
- [X] T031 [US2] Run mutation regressions for source, crop, framing, color, font, transformation, renderer, proof, and report drift in `skill/templates/test_pipeline.py`

**Checkpoint**: No generated identity asset can diverge from Gate 1 silently.

---

## Phase 5: User Story 3 - Review the complete guide and delivery (Priority: P2)

**Goal**: Build a complete applicable private kit and Gate 2 review packet.

**Independent Test**: The rendered guide, catalog, specimens, examples, implementation artifacts, and verification evidence are complete and private, and every omitted family has an approved reason.

- [X] T032 [P] [US3] Add representative tour, itinerary, guide, booking, and testimonial content fields without copied customer or website data in `brands/i-heart-pr-tours/fixtures/product.json`
- [X] T033 [P] [US3] Define accessible semantic roles that preserve all eight identity values and prohibit failing text/surface uses in `brands/i-heart-pr-tours/brand.json`
- [X] T034 [US3] Generate the complete applicable source contract, tokens, styles, components, framework bindings, enforcement files, logo families, icons, specimens, guidelines, UI fixture, and PDF under ignored `dist/i-heart-pr-tours/`
- [X] T035 [US3] Verify the private kit with zero `verify.py` problems and zero applicable `validate_glyph.py` failures under ignored `dist/i-heart-pr-tours/qc/`
- [X] T036 [US3] Visually inspect the logo sheet, guide pages, UI fixture, font specimen, and representative multi-size comparisons; record conclusions in `specs/028-i-heart-pr-tours-brand-guide/evidence.md`
- [X] T037 [US3] Build the operator-readable Gate 2 packet and digest manifest under ignored `dist/i-heart-pr-tours/gate-2/`
- [X] T038 [US3] **OWNER GATE 2** Halt for explicit approval of the complete guide, kit, blocked variants, and exact public-surface classification; owner rejected candidate `iheartpr-g2-r1` and returned the slice to Gate 1

**Checkpoint**: Candidate `iheartpr-g2-r1` is rejected. Copy, palette, surface mode, and transformation changes invalidate the affected Gate 1 approval.

---

## Phase 6: Gate 1 revision after rejected Gate 2

**Goal**: Convert the owner's Gate 2 findings into one exact revised Gate 1 contract before changing production implementation.

**Independent Test**: The review-only packet binds the requested copy, light-first surface mode, evidence-based palette, clean single-ink transform, supplied sandy expressions, exact source hashes, and disabled public surfaces.

- [X] T039 [US1] Reinspect the live site and two explicitly supplied brochure masters for exact color, voice, layout, photography, and surface evidence
- [X] T040 [US1] Diagnose repository-wide light-theme and optional custom-asset gaps and file dedicated issues #193 and #194 with root causes and measurable acceptance criteria
- [X] T041 [US1] Test literal recoloring, identify the retained-shadow and lost-knockout failure modes, and define a deterministic shadow-suppressed knockout-aware single-ink transform
- [X] T042 [US1] Generate review-only candidate `iheartpr-g1-r4`, direction board, monochrome proof, sandy-expression preview, live favicon comparison, candidate contract, and digest manifest under ignored `dist/i-heart-pr-tours/gate-1-r4/`
- [X] T043 [US1] Update the S028 specification, plan, research, transformation contract, tasks, quickstart, and evidence with the Gate 2 rejection and revised Gate 1 scope
- [X] T044 [US1] **OWNER GATE 1** Halt for explicit approval of exact candidate `iheartpr-g1-r4` and manifest SHA-256 `6b25b935b9e8420463f4e56c102e16d8da31dcd2ef729602a051db30debd72be`

**Checkpoint**: Production changes remain blocked until the revised copy, palette, surface mode, transformation, and custom-asset scope receive exact approval.

---

## Phase 7: Revised implementation and Gate 2

**Goal**: Replace the rejected private kit with a light-first, source-faithful candidate that satisfies the revised contract.

- [X] T045 Add failing tests for exact copy, light-first guide output, palette roles, single-ink proof binding, and sandy-expression inclusion
- [X] T046 Apply approved revised contract values to `brands/i-heart-pr-tours/`, add the narrow client-specific light-guide path, and implement the approved deterministic single-ink derivation without mutating source bytes
- [X] T047 Regenerate the complete private I Heart PR Tours kit and revised Gate 2 packet
- [X] T048 Run focused and full validation with zero verifier problems, zero applicable glyph failures, WCAG 2.1 AA, deterministic derivatives, and clean source boundaries
- [X] T049 Visually inspect the white-paper guide, desktop and mobile portable guide, colored and single-ink marks, sandy expressions, implementation examples, and small-size proofs
- [X] T050A [US3] Record the owner's Gate 2 typography revision and live-site heading measurements without changing any approved identity asset, palette, copy, or publication value
- [X] T050B [US3] Add and run failing regressions that reserve Courier Prime for code-like values and require supplied brand fonts for section labels and table headings
- [X] T050C [US3] Apply the semantic heading and label typography correction to the PDF and portable guide generators
- [X] T050D [US3] Rebuild candidate `iheartpr-g2-r3` and rerun affected, all-brand, verifier, and glyph validation
- [X] T050E [US3] Visually inspect the revised guide typography and record the exact candidate digest and evidence
- [X] T050F [US3] Record the owner's `iheartpr-g2-r3` footer, cover metadata, abbreviation, code-block exception, and page-3 surface-preview findings
- [X] T050G [US3] Add failing regressions for exact footer wording, body-font metadata, code-block-only mono use, approved `IHPRT` prose shorthand, and correct dark-surface preview wells
- [X] T050H [US3] Correct PDF and portable-guide small-text roles, preserve the literal code block, add shorthand guidance, and repair page-3 surface bindings
- [X] T050I [US3] Rebuild candidate `iheartpr-g2-r4` and rerun affected, all-brand, verifier, and glyph validation
- [X] T050J [US3] Visually inspect the revised cover, page 2, page 3, typography, footer, code block, and portable guide, then record the exact candidate digest
- [X] T050 [US3] **OWNER GATE 2** Halt for explicit approval of the revised complete guide, kit, variants, and exact public-surface classification

---

## Phase 8: User Story 4 - Publish only approved work (Priority: P3)

**Goal**: Commit and publish the approved source scope, reconcile bounded review, and stop before merge.

**Independent Test**: The official pull request closes #188, exact-head CI is green, every review thread is resolved, no third Codex round occurs, and no unapproved public surface appears.

- [X] T051 [US4] Apply exactly the revised Gate 2 publication settings to `brands/i-heart-pr-tours/brand.json`, `scripts/prepare_site.py`, and site discovery only where approved
- [X] T052 [US4] Add issue, identity, accessibility, documentation, privacy, and verification evidence to `specs/028-i-heart-pr-tours-brand-guide/evidence.md`
- [X] T053 [US4] Update unreleased history and architecture decisions in `CHANGELOG.md` and `skill/CHANGELOG.md`
- [X] T054 [US4] Run all focused Python suites and Markdown policy from `specs/028-i-heart-pr-tours-brand-guide/quickstart.md`
- [X] T055 [US4] Run capability probing, all production-kit builds, release certification, generated-agent synchronization, repository hygiene, and encoding checks from `specs/028-i-heart-pr-tours-brand-guide/quickstart.md`
- [X] T056 [US4] Run site lint, static build, browser route coverage, and WCAG 2.1 AA checks from `specs/028-i-heart-pr-tours-brand-guide/quickstart.md`
- [X] T057 [US4] Re-run cross-artifact analysis and resolve every specification, plan, task, contract, checklist, and implementation inconsistency in `specs/028-i-heart-pr-tours-brand-guide/`
- [X] T058 [US4] Commit S028 with Conventional Commit traceability and confirm the feature branch is clean
- [X] T059 [US4] Push `codex/028-i-heart-pr-tours-brand-guide` and open the official pull request closing #188 under the owner's explicit authorization
- [ ] T060 [US4] Record hosted CI, Codex and security review activity, reactions, responses, fixes, and thread resolutions in `specs/028-i-heart-pr-tours-brand-guide/evidence.md`
- [ ] T061 [US4] Request at most one second Codex review when useful, process every resulting finding, and never request a third round
- [ ] T062 [US4] Confirm the exact final head has green required checks, no unresolved review threads, a clean merge state, and a complete readiness ledger
- [ ] T063 [US4] Halt without merging and ask the owner to perform the final review and merge ritual

---

## Dependencies and execution order

- Phase 1 is complete and establishes the work order.
- User Story 1 begins immediately and blocks all source promotion.
- Phase 3 depends on explicit Gate 1 approval and exact destination paths derived from it.
- User Story 2 depends on promoted authoritative sources and continuity records.
- User Story 3 depends on the locked identity and ends at Gate 2.
- The rejected first Gate 2 returns S028 to revised Gate 1 before any production changes.
- Revised implementation depends on explicit approval of `iheartpr-g1-r4`.
- User Story 4 depends on explicit revised Gate 2 approval and the exact approved publication scope.
- T059 is pre-authorized by the kickoff but remains impossible before both revised owner gates.
- T063 is the final non-merge halt.

## Parallel opportunities

- T009, T010, and T011 concern separate palette, font, and contextual evidence.
- T017, T018, and T019 affect separate test surfaces after Gate 1.
- T032 and T033 affect fixture content and palette semantics after identity locking.
- Hosted push and pull-request CI jobs run independently after T059.

## Implementation strategy

### MVP first

1. Complete private intake evidence.
2. Obtain Gate 1 approval.
3. Promote exact sources and make the authoritative contract fail closed.
4. Prove one private build before expanding delivery.

### Incremental delivery

1. Source authority and privacy packet.
2. Exact promotion and continuity contract.
3. Complete private guide and kit.
4. Gate 2 approval and only then repository publication.
5. Bounded automated review and owner merge gate.

## Notes

- Tests precede implementation and must demonstrate meaningful failures.
- Reviewer-owned checklist markers are not implementation status.
- Gate 1 approved exact SVG source filenames and roles. T017 onward must use only those names and hashes.
- Generated intake, proof, guide, kit, site, and release artifacts remain ignored.
- No identity source may be committed and no production derivative may be generated before Gate 1.
