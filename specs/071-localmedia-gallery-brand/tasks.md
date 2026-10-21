# Tasks: Local Media Gallery Brand and Official Showcase

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md) and [delivery contract](contracts/delivery.md).

## Phase 1: Setup

- [x] T001 Record the owner brief, exact copy, official relationship and D selection in dist/private/localmedia-gallery/brief.json and specs/071-localmedia-gallery-brand/spec.md (FR-001, FR-002).
- [x] T002 Probe the hidden local toolchain and complete design artifacts in specs/071-localmedia-gallery-brand/plan.md and research.md (FR-011, FR-012).

## Phase 2: Foundation

- [x] T003 Add compound-cutout, invalid/open input and provenance regression coverage in skill/templates/test_glyphkit.py and test_identity_continuity.py (FR-013).
- [x] T004 Add byte-preserving compound composition in skill/templates/glyphkit.py, whitelist it in identity_continuity.py and document the vocabulary in skill/references/08-glyph-construction.md (FR-013).
- [x] T005 Run geometry and provenance regression suites and record results in specs/071-localmedia-gallery-brand/verification.md before canonical proof work (FR-005, FR-011, FR-013).

## Phase 3: US1 - Choose and approve logo

**Independent test**: Inspect selected Full/Reduced source, qualified palette, all 32 proofs and exact Gate 1 decision.

- [x] T006 [US1] Preserve the four explored directions and selected D evidence in dist/private/localmedia-gallery/directions/ and brief.json (FR-003, SC-001).
- [x] T007 [US1] Construct Full and simplified Reduced with approved primitives in dist/private/localmedia-gallery/gate-1/build/mk_paths.py; assert Full equals selected D (FR-004, FR-005).
- [x] T008 [US1] Prepare proposed identity/palette and exact current renderer settings in dist/private/localmedia-gallery/gate-1/brand.json and qc/renderer-settings.json (FR-002, FR-004, FR-008).
- [x] T009 [US1] Generate and independently verify 32 production proofs, comparison artifacts, palette qualification and pending source-bound gate-1-packet.json under dist/private/localmedia-gallery/gate-1/ (FR-004, FR-005, FR-008).
- [x] T010 [US1] Present review sheets and record the owner's actual source approval in the Gate 1 packet, then promote exact bytes into brands/localmedia-gallery/ with a valid identity-continuity.json (FR-004, FR-005).

## Phase 4: US2 - Brand fundamentals and kit

**Independent test**: Inspect exact approved fundamentals and social image; final kit must report zero mandatory problems and zero glyph failures.

- [x] T011 [US2] Record independent slogan/description intended uses, additional message dispositions and exact social-copy composition in brands/localmedia-gallery/brand.json and private brief.json (FR-002, FR-007).
- [x] T012 [US2] Assemble source-derived lockups, icons, formal palette, interface cues, typography and gallery example under dist/private/localmedia-gallery/gate-2/ (FR-006, FR-008).
- [x] T013 [US2] Generate the distinct social SVG/PNG, validate gate-2-packet.json and record actual assembled-fundamentals/image approval in brands/localmedia-gallery/brand.json (FR-006, FR-007, FR-009).
- [x] T014 [US2] Compile dist/localmedia-gallery/ through the shared compiler and pass verify.py, validate_glyph.py, render/pagination and provenance checks (FR-009).

## Phase 5: US3 - Official publication

**Independent test**: Official catalog/guidelines/assets/downloads resolve to the approved version with matching release checksums.

- [x] T015 [US3] Add approved identity to current release, proof-export, audit and CI inventories in scripts/ and .github/workflows/build.yml without altering sibling geometry (FR-010, FR-011).
- [x] T016 [US3] Integrate generated catalog and release metadata using site/, CHANGELOG.md and skill/references/version-policy.json (FR-010).
- [x] T017 [US3] Run CONTRIBUTING.md/current CI aggregate validation and site/publication audits, recording exact evidence in specs/071-localmedia-gallery-brand/verification.md (FR-009, FR-010, FR-011).
- [ ] T018 [US3] Complete reviewed publication workflow and verify live official routes/download checksums in specs/071-localmedia-gallery-brand/verification.md (FR-010, SC-005).

## Phase 6: Cross-cutting validation

- [x] T019 Check authored source and delivered artifacts for UTF-8 BOM, LF and mojibake and inspect all produced review/contact sheets, recording evidence in specs/071-localmedia-gallery-brand/verification.md (FR-012).
- [x] T020 Verify only approved sources/specifications/toolkit changes are staged and update chronological decisions and task status in specs/071-localmedia-gallery-brand/plan.md and tasks.md (FR-011).

## Additional US2 correction found during review

- [x] T021 [US2] Correct long-name fitting, wordmark segment colors and compound path fill-rule preservation in skill/templates/build_specimen.py, with regressions in skill/templates/test_brand_essentials.py, before reviewing the final type specimen (FR-014).

## Dependencies and Execution Order

Setup -> foundation -> US1 source approval/promotion -> US2 fundamentals approval/final kit -> US3 publication -> final validation. Creative approvals block only dependent production/publication work. T007 starts only after the compound helper passes its regression tests. Candidate preparation and independent validation do not manufacture approval.

## Parallel Opportunities

Within US1, palette comparison can run independently of geometry validation once masters are fixed. Within US2, typography review and the gallery specimen can be assembled independently from the same promoted source. Within US3, read-only inventory inspection and documentation drafting can run independently before final integration. Shared-file edits and mutation/approval steps remain sequential.

## Implementation Strategy

Deliver the actual qualified Gate 1 source/proof packet first. After exact owner approval, promote without reconstruction and deliver Gate 2. After that approval, compile, aggregate-verify and publish through existing workflows. A completed discovery packet is not final package or publication completion. All 31 tasks use checklist IDs and paths; five US1 tasks, fourteen US2 tasks and five US3 tasks include their story label.

## Current review state

Gate 1 square approval, the selected-B source amendment, and the owner's exact final Gate 2 approval are recorded. T011 and T013 are complete with independent message roles, the explicit slogan-only composition, canonical social SVG/PNG hashes and the approved derivative manifest. Final compilation, aggregate validation, encoding checks and publication staging have passed. The source-only publication candidate is prepared for PR review. T018 remains open for a reviewed tagged release and live route/download verification.

## Owner-directed typed-name revision

- [x] T022 [US2] Replace domain-form lettering with Local Media Gallery in a source-bound candidate, regenerate and check the unchanged 32 square proofs, refresh wordmark/pairing and application previews under dist/private/localmedia-gallery/gate-1-name-revision/, and record actual revised-source acceptance before promotion. Preserve the earlier approved snapshot as historical evidence; use the domain only as an address (FR-002, FR-005, FR-006).

- [x] T023 [US2] Prepare smaller-type/larger-icon horizontal studies, including Local Media above larger Gallery, under dist/private/localmedia-gallery/horizontal-pairing-study/; preserve exact square paths and verify outlined bounds, contrast and raster outputs (FR-005, FR-006, FR-008).

T022 is complete: the owner selected B, its production output matches the chosen artwork, and the proper-name source amendment is promoted. T024-T026 provide the shared line renderer, source continuity and refreshed fundamentals. Gate 2 approval and final kit compilation are complete. T018 remains open for live publication.

## Selected B implementation and review refresh

- [x] T024 [US2] Add failing malformed-config, measured-layout, clipping and renderer-binding regressions; implement governed horizontal wordmark lines in skill/templates/brand_contract.py, lockup_typography.py and gen_logo.py; preserve unconfigured production render paths in identity_continuity.py (FR-015).
- [x] T025 [US2] Reproduce the selected B artwork through production, preserve exact square geometry/proofs, record the owner's actual amendment wording and promote matching Local Media Gallery source under brands/localmedia-gallery/ (FR-002, FR-005, FR-015).
- [x] T026 [US2] Regenerate the source-derived fundamentals, social composition, gallery examples, wordmark/pairing and verification evidence under dist/private/localmedia-gallery/gate-2-b/ and present the refreshed assembled review (FR-006, FR-008, FR-015).

Implementation order for this amendment: T024 tests -> shared implementation -> scoped validation -> T025 exact artwork/source checks -> T026 review. T022 closes with T025. T013 records final Gate 2 approval; T014 tracks final compilation.

## Owner-directed social image revision

- [x] T027 [US2] Remove description text from the social composition, center the combined visible logo/slogan group through shared source, preserve default outputs and identity proofs, and refresh the actual production social SVG/PNG and private review evidence (FR-007, FR-016).

## Required validation fixture remediation

- [x] T028 [US2] Resolve the observed WordPress fixture npm audit failures with patched scoped dependency pins in scripts/wordpress-runtime/package.json and package-lock.json; verify transport, affected parser/YAML behavior, required audit and both pinned runtime pairs; record evidence (FR-017).

## Measured review-sheet correction

- [x] T029 [US2] Correct contact-sheet overlap and clipping in skill/templates/qc_images.py using measured alpha bounds, panel height that includes standalone supplied lockups, and bounded square mark samples; add non-overlap, tall-only and non-square regression cases in test_qc_images.py and inspect regenerated sheets (FR-012, FR-015).

## Portable presentation correction

- [x] T030 [US2] Bind bundled local fonts in the standalone Web specimen and inherit readable link color in the portable guide through shared generator source; measure actual font loading and dark/light link contrast and inspect regenerated screenshots (FR-008, FR-009, FR-012).

## Hosted runner compatibility correction

- [x] T031 [US3] Pin the Python 3.8 compatibility job to the supported Ubuntu 24.04 image in .github/workflows/build.yml, retain the minimum-version test requirement, assert the runner contract in scripts/test_publication_workflow.py, use Python 3.8-compatible UTF-8 fixture writes in test_lockup_typography.py, isolate the vector social-composition test from raster proof generation in test_pipeline.py, and rerun hosted validation (FR-010, FR-011).
