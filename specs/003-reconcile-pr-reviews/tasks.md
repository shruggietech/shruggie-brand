# Tasks: Review Reconciliation and Foundation Certification

**Input**: Design documents from `/specs/003-reconcile-pr-reviews/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/`

**Tests**: Regression-first verification is mandatory for every reproduced review finding. Existing focused tests may be reused when they already fail against the reviewed defect and pass against current main.

**Organization**: Tasks are sequenced chronologically. `T001` through `T019` intentionally preserve the one-to-one task codes already published in GitHub issues #17 through #25 and #27 through #36.

## Phase 1: Baseline and Evidence Foundation

**Purpose**: Pin the authoritative base, inventory every public relationship, and establish the evidence ledger before any disposition.

- [X] T020 [US1] Record the verified `origin/main` SHA, 19 issue-to-thread mappings, initial thread states, and focused-test mapping in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T021 [US2] Record candidate child sets, parent relationships, explicit exclusions, and initial GitHub states in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T022 [US1] Add a dated S003 supersession note to `specs/002-publication-completion/tasks.md` without rewriting its historical checkboxes

**Checkpoint**: The baseline and closure rules are observable before any GitHub state changes.

---

## Phase 2: Inherited Review Findings (Priority: P1)

**Goal**: Revalidate, correct when needed, document, reply to, and resolve every finding from pull requests #16 and #26.

**Independent Test**: All 19 focused dispositions pass against the S003 branch, each linked issue has current evidence, and all 19 inherited source threads contain a substantive reply and are resolved.

- [X] T001 [US1] Revalidate issue #17 with Python 3.8 build discovery and minimum-version CI evidence in `scripts/build_all.py`, `.github/workflows/build.yml`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T002 [US1] Revalidate issue #18 with offline local-font binding evidence in `skill/templates/gen_nextjs.py`, `skill/templates/test_pipeline.py`, `skill/references/09-portability.md`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T003 [US1] Revalidate issue #19 with lower-tier skip and full-tier fatal PDF evidence in `skill/templates/gen_guide_pdf.py`, `scripts/package_release.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T004 [US1] Revalidate issue #20 with named lower-tier skip and full-tier fatal page-QC evidence in `skill/templates/qc_images.py`, `skill/templates/build_kit.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T005 [US1] Revalidate issue #21 with consistent `fonts` registry routes and installation evidence in `skill/templates/gen_nextjs.py`, `scripts/prepare_site.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T006 [US1] Revalidate issue #22 with single-interactive-control CTA evidence in `brands/shruggietech/ui_kits/shruggie-web/runtime.js`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T007 [US1] Revalidate issue #23 with native required-state forwarding evidence in `skill/templates/gen_vanilla.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T008 [US1] Revalidate issue #24 with hidden non-interactive Windows launcher evidence in `scripts/build_all.py`, `skill/templates/process_utils.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T009 [US1] Revalidate issue #25 with retained vectors and explicit raster-skip evidence in `skill/templates/gen_logo.py`, `skill/templates/verify.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T010 [US1] Revalidate issue #27 with stale PDF removal evidence in `skill/templates/gen_guide_pdf.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T011 [US1] Revalidate issue #28 with stale raster and favicon removal evidence in `skill/templates/gen_logo.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T012 [US1] Revalidate issue #29 with independently measured ICO capability evidence in `skill/templates/probe.py`, `skill/templates/gen_logo.py`, `skill/templates/verify.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T013 [US1] Revalidate issue #30 with governed single-physical-line prose evidence in `scripts/check_markdown.py`, `docs/decisions.md`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T014 [US1] Revalidate issue #31 with runtime Python 3.8 regression execution evidence in `.github/workflows/build.yml`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T015 [US1] Revalidate issue #32 with Pillow-inclusive raster capability evidence in `skill/templates/probe.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T016 [US1] Revalidate issue #33 with stale page-QC sheet removal evidence in `skill/templates/qc_images.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T017 [US1] Revalidate issue #34 with Pillow-independent image-backed core generation evidence in `skill/templates/gen_logo.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T018 [US1] Revalidate issue #35 with stale PDF contact-sheet and extracted-page removal evidence in `skill/templates/gen_guide_pdf.py`, `skill/templates/qc_render.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T019 [US1] Revalidate issue #36 with deferred Pillow import and named core-tier QC skip evidence in `skill/templates/qc_images.py`, `skill/templates/test_pipeline.py`, and `specs/003-reconcile-pr-reviews/evidence.md`; fix regression-first if needed, then reply to and resolve its source thread
- [X] T023 [US1] Post acceptance-specific evidence to issues #17 through #25 and #27 through #36, close only current-main-satisfied issues, and record every issue comment URL in `specs/003-reconcile-pr-reviews/evidence.md`

**Checkpoint**: Nineteen of nineteen inherited review threads are answered and resolved, with no issue closed on branch-only evidence.

---

## Phase 3: Complete Verification Run (Priority: P1)

**Goal**: Produce one reproducible evidence set for the whole repository and its generated outputs.

**Independent Test**: The quickstart completes on the S003 worktree and a separate clean checkout with zero verification problems, zero glyph failures, successful site export, and exactly seven valid dry-run release archives.

- [X] T024 [US2] Run compile, discovery, glyph, pipeline, Markdown, capability, six-kit, agent-sync, site lint/export, and dry-run packaging checks from `specs/003-reconcile-pr-reviews/quickstart.md`, then record exact results in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T025 [US2] Repeat the documented build from a separate clean checkout and record repository-only results for issue #74 in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T026 [US2] Run UTF-8-without-BOM, LF, mojibake, secret, private-path, and provider-identifier scans and record sanitized results in `specs/003-reconcile-pr-reviews/evidence.md`

**Checkpoint**: The evidence set is sufficient to evaluate each candidate without relying on unsupported inference.

---

## Phase 4: Work-Order Certification (Priority: P1)

**Goal**: Reduce the backlog to actual remaining work through criterion-specific evidence.

**Independent Test**: Each candidate issue has a public pass or incomplete comment, every closure is based on current-main evidence, and parent state matches child state.

- [X] T027 [US2] Evaluate and update Phase 1 child issues #39 through #46 against repository, governance, licensing, backup, inventory, layout, and Spec Kit evidence; record decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T028 [US2] Evaluate and update Phase 2 child issues #47 through #49 against skill, entry-point, font, portability, test, and hygiene evidence; record decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T029 [US2] Evaluate and update Phase 3 child issues #50 through #58 against geometry, provenance, migration, registry, accessibility, and six-kit evidence; record decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T030 [US2] Evaluate and update Phase 4 child issue #59 against fixture build, verification, hue-exemption, orchestration, and release-exclusion evidence; record the decision in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T031 [US2] Evaluate and update Phase 5 child issues #60 through #62 while keeping release issue #63 open; record workflow and packaging decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T032 [US2] Evaluate and update Phase 6 child issues #64 through #67 against static export, local fonts, generated-kit consumption, routes, and real registry-install evidence; record decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T033 [US2] Evaluate and update Phase 7 child issues #68 through #70 against public DNS, HTTPS, Pages, route, and scratch-install evidence without exposing operational identifiers; record decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T034 [US2] Evaluate and update Phase 8 child issues #71 and #72 while keeping published-archive issue #73 open; record documentation-history decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T035 [US2] Evaluate and update clean-build issue #74 while keeping issue #75 open unless the deployed revision and every route are independently proven; record decisions in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T036 [US2] Re-query GitHub child states, update parent issues #6 through #15 according to set-complete closure rules, and record why program #37 remains open in `specs/003-reconcile-pr-reviews/evidence.md`

**Checkpoint**: GitHub presents a coherent evidence-backed project profile, with remaining open work explicit.

---

## Phase 5: Publication and Bounded Review (Priority: P2)

**Goal**: Deliver a green, fully reviewed, unmerged pull request without exceeding two Codex rounds.

**Independent Test**: The official PR is open, all checks are green, every comment from both permitted rounds is answered and resolved, exactly one explicit `@Codex` request exists, and no merge has occurred.

- [X] T037 [US3] Update `CHANGELOG.md`, complete `specs/003-reconcile-pr-reviews/evidence.md`, run `git diff --check` and the full quickstart, then create a Conventional Commit for S003
- [X] T038 [US3] Push `codex/003-reconcile-pr-reviews` and open the official pull request with issue links, exclusions, verification results, and the initial ledger from `specs/003-reconcile-pr-reviews/contracts/review-ledger.md`
- [X] T039 [US3] Observe automatic Codex review round 1, respond to every comment, implement regression-first corrections where warranted, rerun verification, push changes, resolve every addressed thread, and update the pull-request ledger
- [X] T040 [US3] Post exactly one `@Codex` pull-request comment for round 2 and record its immutable comment URL in `specs/003-reconcile-pr-reviews/evidence.md`
- [X] T041 [US3] Observe Codex review round 2, respond to every comment, implement regression-first corrections where warranted, rerun verification, push changes, resolve every addressed thread, and update the pull-request ledger without another review request
- [ ] T042 [US3] Wait for every required continuous-integration check to succeed, verify the pull request remains open and review-complete, and hand it to the owner for the final review and merge ritual

---

## Dependencies & Execution Order

- Phase 1 precedes all state changes.
- Phase 2 verifies inherited defects before broad certification.
- Phase 3 provides the reusable technical evidence for Phase 4.
- Phase 4 GitHub updates complete before the pull-request narrative is finalized.
- T038 depends on all local checks in T037.
- T040 cannot run before round 1 is complete.
- T042 cannot run before round 2 is complete and CI is green.
- Merge, tag, release, deployment, and Phase 10 work are not tasks in S003.

## Parallel Opportunities

- Focused test inspection for independent findings can be batched, but GitHub replies remain ordered and individually verified.
- Candidate issue evidence within a phase can share one verified artifact set, while each decision remains criterion-specific.
- CI observation and review observation may proceed concurrently after a push, but round 2 still waits for round 1 completion.

## Implementation Strategy

1. Establish traceability and correct historical ambiguity.
2. Complete the 19 finding dispositions with regression evidence.
3. Build the reusable repository-wide evidence set once.
4. Apply that evidence carefully across candidate issues and parents.
5. Publish once, process two bounded review rounds, and halt at the owner's merge gate.
