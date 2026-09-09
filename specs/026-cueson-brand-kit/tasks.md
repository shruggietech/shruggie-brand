---

description: "Task list for the S026 Cueson brand kit"
---

# Tasks: Cueson Brand Kit

**Input**: Design documents from `/specs/026-cueson-brand-kit/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: S026 requires test-first identity-study, approval, contract, generator, pipeline, site, accessibility, and repository-hygiene coverage. Test tasks precede the source changes they govern.

**Organization**: Tasks are grouped by user story and two explicit owner gates. Autopilot must stop at T017 and T030 until the exact proposal revision receives owner approval.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it owns different files and has no dependency on an incomplete task
- **[Story]**: Maps the task to the user story in `spec.md`
- Every task names an exact file or output path

## Phase 1: Setup and Evidence Freeze

**Purpose**: Establish issue traceability, source revisions, output boundaries, and the complete S026 design ledger.

- [X] T001 Record issue #184, the authorized push and pull-request exception, and the two retained owner halts in `specs/026-cueson-brand-kit/evidence.md`
- [X] T002 Fetch both repositories, record current Shruggie Brand and Cueson `origin/main` revisions, and preserve the untouched Cueson worktree state in `specs/026-cueson-brand-kit/evidence.md`
- [X] T003 [P] Confirm `dist/.s026-cueson-study/`, generated kits, site exports, PDFs, rasters, registries, and archives resolve to ignored paths and record results in `specs/026-cueson-brand-kit/evidence.md`
- [X] T004 [P] Validate the S026 specification and built-in requirements checklist for placeholders, contradictions, UTF-8 without BOM, LF, and mojibake in `specs/026-cueson-brand-kit/spec.md` and `specs/026-cueson-brand-kit/checklists/requirements.md`
- [X] T005 Record the installed checklist preflight ordering deviation and completed design artifacts in `specs/026-cueson-brand-kit/plan.md` and `specs/026-cueson-brand-kit/evidence.md`

**Checkpoint**: S026 has a synchronized, issue-traceable, source-only foundation and no production identity geometry.

---

## Phase 2: Foundational Proposal Contract

**Purpose**: Define deterministic proposal data and fail-closed checks before visual concepts are rendered.

**Critical**: Gate 1 proposal work depends on these tests and contracts. Production `brands/cueson/` source remains prohibited.

- [X] T006 [P] Add failing tests for four unique candidates, one recommendation, complete metadata, exact proof sizes and surfaces, palette thresholds, deterministic manifests, and ignored output in `scripts/test_cueson_identity_study.py`
- [X] T007 [P] Add the Gate 1 proposal schema with evidence snapshot, criteria, candidates, palette, approval state, and public-eligibility fields in `specs/026-cueson-brand-kit/gate-1-proposal.json`
- [X] T008 Implement the deterministic Gate 1 data validation, vector assembly, raster proof, contact-sheet, and manifest pipeline in `scripts/cueson_identity_study.py`
- [X] T009 Run `scripts/test_cueson_identity_study.py` and record the expected red-to-green progression in `specs/026-cueson-brand-kit/evidence.md`

**Checkpoint**: The proposal generator is test-covered, deterministic, non-publishing, and ready to express User Story 1.

---

## Phase 3: User Story 1 - Choose a Meaningful Identity Direction (Priority: P1) MVP

**Goal**: Present four product-grounded glyph concepts and one recommended accessible color system, then stop for iterative owner review.

**Independent Test**: The Gate 1 packet alone contains four materially distinct concepts, complete rationale and risk records, exact 256/64/32/16 pixel dark/light/single-ink proofs, a measured approved palette, deterministic hashes, and no production or public eligibility.

### Tests for User Story 1

- [X] T010 [P] [US1] Extend study tests to prove the screenshot-style exclusion, exact Cueson copy, cliché-risk disclosures, and complete identity-criterion mapping in `scripts/test_cueson_identity_study.py`
- [X] T011 [P] [US1] Add negative tests for missing recommendations, duplicated geometry fingerprints, absent 16-pixel proofs, failed contrast, missing color-vision evidence, active SVG content or external references, path escapes, and premature approval in `scripts/test_cueson_identity_study.py`

### Implementation for User Story 1

- [X] T012 [US1] Implement Cueframe, Parallel Source, Timing Spine, and Interchange Aperture full and reduced proposal geometry in `scripts/cueson_identity_study.py`
- [X] T013 [US1] Implement and validate the selected palette revision, semantic role comparisons, contrast evidence, parent-role separation, and single-ink proofs in `scripts/cueson_identity_study.py`
- [X] T014 [US1] Re-fetch both remotes, confirm the evidence revisions or record material drift, then generate the complete ignored Gate 1 packet and manifest under `dist/.s026-cueson-study/gate-1/`
- [X] T015 [US1] Open and visually inspect the overview, individual concept sheets, 16-pixel proofs, and palette sheet from `dist/.s026-cueson-study/gate-1/`, recording findings in `specs/026-cueson-brand-kit/evidence.md`
- [X] T016 [US1] Record exact proposal and manifest hashes, concept tradeoffs, recommendation, and pending approval in `specs/026-cueson-brand-kit/evidence.md`
- [X] T017 [US1] HALT for iterative Gate 1 owner critique and exact glyph-plus-palette approval, then record the accepted wording and hashes in `specs/026-cueson-brand-kit/evidence.md`

**Checkpoint**: User Story 1 is independently reviewable. No work after T017 begins without explicit Gate 1 approval.

---

## Phase 4: User Story 2 - Approve the Complete Derived Spread (Priority: P1)

**Goal**: Convert only the Gate 1-approved glyph and palette into the complete derived identity family and stop for iterative owner review.

**Independent Test**: The Gate 2 packet contains every current derivative family, exact source relationships and hashes, copy compositions, size/surface/platform proofs, measurements, and disabled public eligibility.

### Tests for User Story 2

- [X] T018 [P] [US2] Add failing contract tests for constructed-brand approval ledgers with honest empty imported-source bindings, configuration drift, pending Gate 2, and stale Gate 2 manifests in `skill/templates/test_brand_contract.py`
- [X] T019 [P] [US2] Add failing pipeline tests for Cueson affiliation, exact copy, house typography, approved geometry, derivative coverage, zero glyph failures, and Gate 2 publication blocking in `skill/templates/test_pipeline.py`
- [X] T020 [P] [US2] Add failing study tests for complete lockup, wordmark, colorway, reduced, platform, copy-composition, manifest, and public-surface coverage in `scripts/test_cueson_identity_study.py`

### Implementation for User Story 2

- [X] T021 [US2] Record the current Gate 1 approval object and approved configuration fingerprint in `specs/026-cueson-brand-kit/gate-1-proposal.json` and `specs/026-cueson-brand-kit/evidence.md`
- [X] T022 [US2] Permit approval-ledger validation for a constructed identity with no imported protected source while preserving strict authoritative-source behavior in `skill/templates/brand_contract.py`
- [X] T023 [US2] Create the Gate 1-approved Cueson source contract, exact constructed master, palette, house typography, voice, components, and pending Gate 2 ledger in `brands/cueson/brand.json`
- [X] T024 [US2] Add human and agent source guidance that marks the identity as Gate 2-pending in `brands/cueson/README.md`, `brands/cueson/NOTES.md`, and `brands/cueson/SKILL.md`
- [X] T025 [US2] Add a self-contained representative Cueson data-interface specimen source in `brands/cueson/ui_kits/cueson-data/index.html` and `brands/cueson/ui_kits/cueson-data/README.md`
- [X] T026 [US2] Generate the private Cueson kit, then implement the Gate 2 derivative, application, copy, and public-surface packet path in `scripts/cueson_identity_study.py`
- [X] T027 [US2] Re-fetch both remotes, confirm Gate 1 evidence remains current or invalidate it on material drift, then generate the complete ignored Gate 2 packet and derivative manifest under `dist/.s026-cueson-study/gate-2/`
- [X] T028 [US2] Open and visually inspect every Gate 2 overview, wordmark, copy, reduced-size, platform-mask, UI, guideline, and public-surface proof from `dist/.s026-cueson-study/gate-2/`, recording findings in `specs/026-cueson-brand-kit/evidence.md`
- [X] T029 [US2] Record exact approved-source, producing-configuration, derivative-manifest, and public-surface hashes with pending status in `specs/026-cueson-brand-kit/gate-2-proposal.json` and `specs/026-cueson-brand-kit/evidence.md`
- [X] T030 [US2] HALT for iterative Gate 2 owner critique and exact derived-spread approval, then record the accepted wording and hashes in `specs/026-cueson-brand-kit/gate-2-proposal.json` and `specs/026-cueson-brand-kit/evidence.md`

**Checkpoint**: User Story 2 is independently reviewable. No public eligibility or final kit work begins without explicit Gate 2 approval.

---

## Phase 5: User Story 3 - Consume a Complete Verified Cueson Kit (Priority: P2)

**Goal**: Finalize the complete current-specification kit and generated public projection from the exact Gate 2-approved spread.

**Independent Test**: A clean offline multi-brand build contains every required Cueson layer, zero glyph or kit problems, passing accessibility and site checks, and no tracked generated output.

### Tests for User Story 3

- [X] T031 [P] [US3] Add release/archive discovery tests for the seventh production kit and exact Cueson deliverables in `scripts/test_package_release.py` and `scripts/test_release_contract.py`
- [X] T032 [P] [US3] Add site preparation and generated-value tests for Cueson routes, registries, metadata, downloads, structured data, and social presentation in `scripts/test_prepare_site.py` and `site/tests/payload-contract.test.mjs`
- [X] T033 [P] [US3] Add source contract tests for exact slogan, description line break, affiliation, palette, typography, and approval hashes in `skill/templates/test_brand_contract.py`

### Implementation for User Story 3

- [X] T034 [US3] Record Gate 2 approval and enable only the exact approved public surface set in `brands/cueson/brand.json`
- [X] T035 [US3] Finalize generated guidance, UI specimen content, minimum-size rules, misuse rules, application notes, and exact verbal identity in `brands/cueson/README.md`, `brands/cueson/NOTES.md`, `brands/cueson/SKILL.md`, and `brands/cueson/ui_kits/cueson-data/index.html`
- [X] T036 [US3] Update only discovered seven-brand assertions and source-driven site integration points required by the new kit in `scripts/`, `site/tests/`, and `site/` without hard-coding Cueson identity values outside `brands/cueson/`
- [X] T037 [US3] Build and verify Cueson, then run the complete multi-kit and site validation from `specs/026-cueson-brand-kit/quickstart.md`
- [X] T038 [US3] Open and visually inspect representative Cueson logos, icons, guide pages, PDF pages, UI specimen, download surface, registry output, and responsive public routes from `dist/` and `site/out/`, recording results in `specs/026-cueson-brand-kit/evidence.md`

**Checkpoint**: User Story 3 supplies a complete, verified, source-driven Cueson kit and public proposal.

---

## Phase 6: User Story 4 - Hand Off an Approved Identity Safely (Priority: P3)

**Goal**: Produce an exact future consumer-import map while leaving the Cueson repository and dormant domain unchanged.

**Independent Test**: The handoff manifest maps each intended consumer asset to an approved hash, license, destination, and follow-up workflow, and independent repository checks show no Cueson or domain mutation.

### Tests for User Story 4

- [X] T039 [P] [US4] Add failing handoff tests for approval references, source and artifact hashes, licenses, destinations, future issue/slice fields, and unchanged-domain declarations in `scripts/test_cueson_identity_study.py`

### Implementation for User Story 4

- [X] T040 [US4] Generate the hash-addressed consumer handoff manifest under `dist/cueson/consumer-handoff.json` from approved source and artifact manifests
- [X] T041 [US4] Record the Cueson worktree status, remote state, absent integration commit, and untouched `cueson.io` boundary in `specs/026-cueson-brand-kit/evidence.md`
- [X] T042 [US4] Document the required later Cueson issue and Spec Kit import workflow in `brands/cueson/NOTES.md` without performing the import

**Checkpoint**: User Story 4 provides a safe, exact handoff with no cross-repository or domain mutation.

---

## Phase 7: Cross-Cutting Verification, Publication, and Review

**Purpose**: Complete local quality gates, publish the authorized branch and pull request, reconcile at most two Codex review rounds and every other received review, then return for owner merge.

- [X] T043 [P] Re-evaluate the reviewer-owned requirements in `specs/026-cueson-brand-kit/checklists/identity-approval.md` without treating checkbox state as implementation completion
- [X] T044 Run every focused Python, Markdown, capability, full-build, site lint, site build, and site test command from `specs/026-cueson-brand-kit/quickstart.md` in the foreground and record exact results in `specs/026-cueson-brand-kit/evidence.md`
- [X] T045 Inspect repository hygiene, tracked generated files, UTF-8 without BOM, LF, mojibake, whitespace, and Cueson/domain scope boundaries, then record results in `specs/026-cueson-brand-kit/evidence.md`
- [X] T046 Update the Unreleased feature and dated approval-architecture decision in `CHANGELOG.md` and any generator-facing entry required in `skill/CHANGELOG.md`
- [X] T047 Complete task states and final local evidence in `specs/026-cueson-brand-kit/tasks.md` and `specs/026-cueson-brand-kit/evidence.md`
- [X] T048 Commit S026 with a Conventional Commit subject that references S026 and verify the committed branch head
- [X] T049 Push `codex/026-cueson-brand-kit` and open the official pull request closing #184 under the explicit kickoff authorization
- [ ] T050 Record the pull request, branch head, automatic review signals, security feedback, and required check runs in `specs/026-cueson-brand-kit/evidence.md`
- [ ] T051 Process every actionable and non-actionable round-1 Codex, security-bot, CI, and human review item with evidence-backed replies, necessary changes, verification, pushes, and thread resolution
- [ ] T052 Post at most one `@Codex review` comment for round 2 after round-1 findings are resolved, then process every resulting item with the same evidence and never request a third round
- [ ] T053 Verify all required checks are green, all received reviews are satisfied, the exact branch head is recorded, and the pull request remains unmerged in `specs/026-cueson-brand-kit/evidence.md`
- [ ] T054 HALT and ask the owner to perform the final review and merge ritual for the verified official pull request

---

## Dependencies and Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational Proposal Contract (Phase 2)**: Depends on Setup and blocks Gate 1 rendering.
- **User Story 1 (Phase 3)**: Depends on the proposal contract and ends at mandatory Gate 1.
- **User Story 2 (Phase 4)**: Depends on explicit Gate 1 approval and ends at mandatory Gate 2.
- **User Story 3 (Phase 5)**: Depends on explicit Gate 2 approval.
- **User Story 4 (Phase 6)**: Depends on the complete approved generated kit.
- **Cross-Cutting Verification and Review (Phase 7)**: Depends on all four stories and both approvals.

### User Story Dependencies

- **User Story 1 (P1)**: Independently delivers the complete initial owner decision packet.
- **User Story 2 (P1)**: Requires the exact User Story 1 approval but remains independently testable as a derivative-spread packet.
- **User Story 3 (P2)**: Requires the exact User Story 2 approval and converts it into the complete kit.
- **User Story 4 (P3)**: Requires the generated kit but does not modify the consumer repository.

### Within Each User Story

- Tests are written and observed failing before the governed implementation.
- Proposal geometry precedes Gate 1 only in ignored, non-production output.
- Gate 1 approval precedes production source and every derivative.
- Gate 2 approval precedes public eligibility and consumer handoff.
- Local verification precedes commit, push, and pull-request creation.
- Review corrections precede the optional second round and final owner halt.

### Parallel Opportunities

- T003 and T004 can run alongside the issue and revision evidence updates.
- T006 and T007 own separate proposal-test and proposal-schema files.
- T010 and T011 split positive and negative study requirements in one file and should be applied sequentially by one editor despite independent reasoning.
- T018, T019, and T020 target distinct contract, pipeline, and study behaviors.
- T031, T032, and T033 cover separate release, site, and source-contract surfaces.
- T039 can be prepared while final kit verification completes because it owns the handoff test contract.

## Implementation Strategy

### MVP First: User Story 1

1. Complete evidence freeze and planning.
2. Build the tested non-publishing study generator.
3. Render and inspect all four Gate 1 directions and the Cue Iris palette.
4. Stop at T017 for owner critique and approval.

### Approval-Gated Increment

1. Gate 1 approval unlocks only production master, palette, typography application, and Gate 2 derivation.
2. Gate 2 approval unlocks only complete kit finalization, public eligibility, and handoff generation.
3. Full validation unlocks the already-authorized push and official pull request.
4. Satisfied CI and bounded reviews unlock only the final owner review request, never merge.

## Notes

- `[P]` marks non-overlapping file ownership, not permission to cross an approval gate.
- The two owner halts override autopilot continuation exactly at T017 and T030.
- The authorized push exception applies only after T044 and T045 pass.
- S026 must not create production `brands/cueson/` content before Gate 1, enable public output before Gate 2, request more than two Codex rounds, or merge its pull request.
