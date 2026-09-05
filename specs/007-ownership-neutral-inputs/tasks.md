# Tasks: Ownership-Neutral Authoritative Inputs

**Input**: Design documents from `specs/007-ownership-neutral-inputs/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, and built-in requirements checklist complete. The custom integrity checklist remains reviewer-owned and does not represent implementation state.

## Phase 1: Contract Foundation

**Purpose**: Establish the shared fail-closed contract before modifying generated surfaces.

- [x] T001 Add failing affiliation, supplied-input, palette-approval, fixed-font, and ingestion-boundary tests in `skill/templates/test_brand_contract.py`.
- [x] T002 Add the missing Draft 2020-12 authoring schema with affiliation, inheritance, typography, authoritative-input, and approval structures in `skill/references/canon.schema.json`.
- [x] T003 Implement Python 3.8-compatible normalized affiliation, typography, path, digest, font-metadata, SVG-safety, palette-analysis, and output-scan helpers in `skill/templates/brand_contract.py`.
- [x] T004 Add the fail-fast CLI preflight in `skill/templates/validate_brand.py` and run T001 to green.
- [x] T005 Add deterministic generated evidence output in `skill/templates/analyze_inputs.py` and verify source files remain byte-identical.
- [x] T006 Add controlled bounded local-or-HTTPS atomic font ingestion in `skill/templates/ingest_font.py` and run ingestion failure tests to green.

**Checkpoint**: Invalid or incomplete contracts fail before rendering; valid temporary examples normalize deterministically.

---

## Phase 2: User Story 1 - Generate Ownership-Safe Brands (Priority: P1)

**Goal**: Make affiliation and public eligibility explicit and consistent across every generated surface.

**Independent Test**: Generate a temporary third-party kit, scan every text and metadata output, and prepare a mixed public/private site set. No false owned-project claim may appear and no private brand may publish.

### Tests

- [x] T007 [US1] Extend `skill/templates/test_pipeline.py` with a third-party full-output scan that starts red against current hard-coded claims.
- [x] T008 [US1] Extend `scripts/test_prepare_site.py` with explicit public and private records, stale-public cleanup, and missing-showcase failure cases.

### Implementation

- [x] T009 [US1] Run `validate_brand.py` and `analyze_inputs.py` before existing build work in `skill/templates/build_kit.py`; derive manifest affiliation from the shared contract.
- [x] T010 [US1] Derive parent, affiliation, and conditional semantic-color inheritance in `skill/templates/gen_vanilla.py` and `skill/templates/gen_nextjs.py`.
- [x] T011 [US1] Derive optional affiliation text and owned-parent guidance in `skill/templates/_guidekit.py`, `skill/templates/gen_guidelines.py`, and `skill/templates/gen_guide_pdf.py`.
- [x] T012 [US1] Derive ownership-neutral rules and allowed claims in `skill/templates/gen_enforcement.py`.
- [x] T013 [US1] Filter public site output and generated portfolio metadata by explicit showcase state in `scripts/prepare_site.py`.
- [x] T014 [US1] Run T007 and T008 to green and verify the fixed owned endorsement, fixed neutral service credit, and no-credit cases independently.

**Checkpoint**: User Story 1 is independently complete and issue #104 behavior is demonstrable.

---

## Phase 3: User Story 2 - Preserve Supplied Identity and Approve Palette Evidence (Priority: P2)

**Goal**: Make supplied masters immutable and auditable while keeping extracted color candidates advisory until human approval.

**Independent Test**: Build temporary raster and passive-vector supplied inputs, compare source bytes and SVG path data, reproduce ranked candidates, and prove stale or absent approval blocks canonical linkage.

### Tests

- [x] T015 [US2] Add raster transparency, deterministic ranking, source-hash drift, and stale-approval regression cases to `skill/templates/test_brand_contract.py`.
- [x] T016 [US2] Add passive SVG, active-content, external-reference, live-text, role-collision, path-escape, and undeclared-transformation cases to `skill/templates/test_brand_contract.py`.

### Implementation

- [x] T017 [US2] Connect authoritative-input validation to existing imported image use in `skill/templates/gen_logo.py` without rewriting source bytes or vector path data.
- [x] T018 [US2] Emit authoritative-input and palette evidence into ignored kit QC output through `skill/templates/analyze_inputs.py`.
- [x] T019 [US2] Enforce current approval linkage before canonical palette use in `skill/templates/validate_brand.py`.
- [x] T020 [US2] Run T015 and T016 to green and verify repeat runs produce byte-equivalent JSON evidence for unchanged inputs.

**Checkpoint**: Supplied identity preservation and palette approval are independently complete.

---

## Phase 4: User Story 3 - Build with Approved Fixed Fonts Offline (Priority: P3)

**Goal**: Validate and use fixed family requirements across generated kits without any build-time networking or silent substitution.

**Independent Test**: Declare repository-licensed test faces as fixed in temporary storage, disconnect network-capable code paths, generate all typography surfaces, and prove measured names, weights, styles, formats, and hashes match.

### Tests

- [x] T021 [US3] Add complete fixed-face, missing-face, wrong-family, wrong-weight, bad-style, variable-font, corrupt-binary, and hash-drift cases to `skill/templates/test_brand_contract.py`.
- [x] T022 [US3] Add a temporary fixed-font generator integration to `skill/templates/test_pipeline.py` and assert every emitted surface uses declared role names and local paths.

### Implementation

- [x] T023 [US3] Resolve house and fixed role faces through shared helpers in `skill/templates/brand_contract.py` and embed the selected files in `skill/templates/_guidekit.py`.
- [x] T024 [US3] Generate dynamic CSS tokens, Next.js local-font bindings, and registry metadata in `skill/templates/gen_vanilla.py` and `skill/templates/gen_nextjs.py`.
- [x] T025 [US3] Use selected outline-capable roles for wordmarks and SVG specimens in `skill/templates/gen_logo.py` and `skill/templates/build_specimen.py`.
- [x] T026 [US3] Generate dynamic typography prose, CSS, and enforcement allowlists in `skill/templates/gen_guidelines.py`, `skill/templates/gen_guide_pdf.py`, and `skill/templates/gen_enforcement.py`.
- [x] T027 [US3] Run T021 and T022 to green and audit routine generator imports and execution for zero network access.

**Checkpoint**: Fixed-font mode is independently complete and ordinary house mode remains supported.

---

## Phase 5: User Story 4 - Migrate and Audit the Complete System (Priority: P4)

**Goal**: Put all production brands, documentation, release checks, and CI on the same explicit contract without identity changes.

**Independent Test**: Rebuild all five production kits and the public site, confirm zero validation or glyph failures, and compare current source identity bytes and logo path data to the pre-change baseline.

- [x] T028 [US4] Add explicit owned/public affiliation, house inheritance, and house typography mode to all five `brands/*/brand.json` files.
- [x] T029 [US4] Add authoritative supplied raster records and current human palette approval linkage to `brands/shruggietech/brand.json` using measured hashes without changing source assets.
- [x] T030 [US4] Update `skill/SKILL.md` and the interview, variance, anatomy, toolchain, shadcn, logo, voice, and portability references under `skill/references/` for ownership-neutral, authoritative-input, approval, and fixed-font operation.
- [x] T031 [US4] Update repository and skill changelogs plus release-contract expectations for the unreleased S007 behavior.
- [x] T032 [US4] Add focused contract tests to `.github/workflows/build.yml` before full production rendering.
- [x] T033 [US4] Run the Spec Kit analysis pass and resolve all material consistency, coverage, constitution, and traceability findings.
- [x] T034 [US4] Run every command in `quickstart.md`, record outcomes in `specs/007-ownership-neutral-inputs/evidence.md`, and confirm #106 behavior is absent.
- [x] T035 [US4] Check UTF-8 without BOM, LF, mojibake, ignored generated artifacts, unchanged authoritative input bytes, unchanged existing logo path data, and an intentional-only Git diff.

**Checkpoint**: All four user stories are complete, independently evidenced, and ready for pull-request review.

---

## Phase 6: Pull Request and Bounded Review Ritual

- [ ] T036 Commit S007 with a Conventional Commit subject, push `codex/007-ownership-neutral-inputs`, and open an official PR that closes #104 and #105 only.
- [ ] T037 Wait for the automatic Codex review round and CI, investigate every negative finding, make and verify warranted changes, reply to every comment, and resolve every completed thread.
- [ ] T038 Request exactly one second round with `@Codex review`, then investigate, correct, reply to, and resolve every resulting negative finding without requesting a third round.
- [ ] T039 Wait for final hosted CI to become green, confirm all review threads are resolved and #104, #105, and #106 remain open before merge, then halt and ask the owner for the final review and merge ritual.

## Dependencies and Execution Order

- Phase 1 blocks every story because no generator may consume implicit or unvalidated state.
- User Story 1 establishes shared affiliation output used by the later system audit.
- User Story 2 and User Story 3 both depend on the Phase 1 contract but remain independently testable.
- User Story 4 depends on all behavioral stories and performs the production migration and complete regression.
- Pull-request work starts only after local evidence is complete.

## Scope Guard

- S007 closes only #104 and #105 after the owner merges the PR and post-merge evidence confirms fulfillment.
- #106 remains open for S008. Do not add Android, Apple, macOS, Windows, store-listing, or adaptive icon generation here.
- The automatic review at PR publication is round one. T038 is the only authorized explicit `@Codex` request and is round two. Never request a third round.
