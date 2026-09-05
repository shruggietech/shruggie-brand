# Tasks: Guarded Staging Disposition and Program Closure

**Input**: Design documents from `specs/005-guarded-staging-disposition/`

**Prerequisites**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, and the checked specification-quality checklist

**Organization**: Tasks are sequenced chronologically because disposition safety requires preservation and destination gates before any filesystem move.

## Phase 1: Spec Kit and Baseline Setup

**Purpose**: Establish the slice, its public/private boundary, and the no-delete review protocol.

- [x] T001 Create the S005 branch and `specs/005-guarded-staging-disposition/spec.md` from the active work order and GitHub issue state.
- [x] T002 Validate specification quality in `specs/005-guarded-staging-disposition/checklists/requirements.md` and record that no high-impact clarification remains.
- [x] T003 Create `specs/005-guarded-staging-disposition/plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and `contracts/` with the sanitized evidence boundary and two-round review ceiling.
- [x] T004 Create the public S005 slice issue, link #39, #41, #42, #76 through #86, parents #6 and #15, and program #37, and assign the Phase 10 milestone and governance labels.

**Checkpoint**: S005 has one complete public specification and one coherent GitHub work package before operational mutation.

---

## Phase 2: Foundational Safety Gates

**Purpose**: Prove prerequisites, archive coverage, and destination safety before any source is moved.

- [x] T005 Record the required and optional toolchain preflight in `specs/005-guarded-staging-disposition/evidence.md`, including an authenticated account-scoped infrastructure read and sanitized optional-tier skips.
- [x] T006 Stream-compare the pre-disposition archive against the live workspace by normalized path, byte count, and SHA-256 and record the two transient-cache exceptions in `specs/005-guarded-staging-disposition/evidence.md`.
- [x] T007 Create the operator-held private recovery record with exact inventory paths, counts, hashes, archive identity, intended destination roots, and recovery instructions.
- [x] T008 Verify current hosted build, live HTTPS site and registries, and published v1.1.2 seven-asset release, then record sanitized prerequisite evidence in `specs/005-guarded-staging-disposition/evidence.md`.
- [x] T009 Resolve and validate exact governed cold-storage and recoverable-deletion roots in the private recovery record, rejecting source escape and existing destination collisions.
- [x] T010 Reconcile S004 post-merge publication state in `specs/004-release-publication-certification/spec.md`, `tasks.md`, and `evidence.md`.

**Checkpoint**: The archive, infrastructure, release, source, and destination prerequisites are proven; no staging item has moved.

---

## Phase 3: User Story 1 - Prove Every Source Recoverable (Priority: P1)

**Goal**: Establish governed preservation proof for every authoritative, historical, provenance, unrelated, and private item.

**Independent Test**: Every execution-time top-level entry has exactly one classification and an external preservation proof before the first move.

- [x] T011 [US1] Compare the private skill tree and transport bundles with governed `skill/` sources and published bundles, preserving any unique source before classifying copies as superseded.
- [x] T012 [US1] Verify canonical shared fonts and all five production source trees in `assets/fonts/` and `brands/`, and verify their generated outputs and published snapshots satisfy the current contracts.
- [x] T013 [US1] Hash and path-compare Fragcap historical construction files against `docs/provenance/fragcap/` without modifying geometry.
- [x] T014 [US1] Compare the staged SVG runtime helper with `skill/templates/rsvg-convert.js`, verify behavior equivalence, and record dependency-based reproducibility.
- [x] T015 [US1] Hash-verify both parent-brand CSS sources against `docs/provenance/shruggietech/` and confirm their canon/accessibility references.
- [x] T016 [US1] Classify historical bulk artifacts, both unrelated research groups, private session output, and the operator directive for governed cold storage.
- [x] T017 [US1] Draft every required row of `docs/disposition.md` with sanitized classifications, preservation proof, destination class, recoverability, and pending final state.

**Checkpoint**: Five of five brands and every non-brand top-level entry have verified external coverage and a planned public disposition row.

---

## Phase 4: User Story 2 - Recoverable Staging Retirement (Priority: P1)

**Goal**: Move every source to its verified recoverable destination and leave the original workspace empty.

**Independent Test**: Destination fingerprints match the pre-move inventory, the original workspace has zero files and no undocumented directories, and nothing was permanently deleted.

- [x] T018 [US2] Revalidate resolved source and destination roots and absence of every target immediately before movement; record the gate in the private recovery record.
- [x] T019 [US2] Move historical bulk artifacts, unrelated research, private session output, and the operator directive to governed cold storage without overwriting any destination.
- [x] T020 [US2] Move superseded skill copies and transport bundles to recoverable deletion staging after their governed coverage gate passes.
- [x] T021 [US2] Move the five legacy brand directories and five snapshot archives to recoverable deletion staging after the five-brand gate passes.
- [x] T022 [US2] Move the regenerable runtime and verified private provenance originals to recoverable deletion staging after their comparison gates pass.
- [x] T023 [US2] Verify every destination fingerprint, confirm every source is absent, and verify the original workspace has zero files and zero undocumented directories.
- [x] T024 [US2] Finalize all rows in `docs/disposition.md` and the private recovery record as verified, including execution-time counts and no-permanent-delete confirmation.

**Checkpoint**: The private staging workspace is safely retired and every item remains recoverable.

---

## Phase 5: User Story 3 - Public Evidence and Owner Gate (Priority: P2)

**Goal**: Publish auditable sanitized evidence, pass all quality gates, and complete exactly the authorized review lifecycle without merging.

**Independent Test**: GitHub and the repository trace all fourteen child issues to reviewed evidence, public scans find no private data, review threads are resolved, required checks are green, and the pull request remains open.

- [x] T025 [US3] Append S005 deviations and disposition decisions to `docs/decisions.md` and complete `specs/005-guarded-staging-disposition/evidence.md` without private operational data.
- [x] T026 [US3] Run focused regressions, Markdown policy, generated-agent sync, full six-target build, glyph validation, image/PDF QC, site lint/export, and repository hygiene from `specs/005-guarded-staging-disposition/quickstart.md`.
- [x] T027 [US3] Run UTF-8 without BOM, LF, mojibake, secret, provider-identifier, raw-session, backup-location, and private-path scans against every changed public text file.
- [x] T028 [US3] Run a clean-checkout repetition and record exact sanitized results in `specs/005-guarded-staging-disposition/evidence.md`.
- [x] T029 [US3] Run the read-only Spec Kit consistency analysis and correct any critical or high-severity cross-artifact defects before publication.
- [x] T030 [US3] Mark completed implementation tasks in `specs/005-guarded-staging-disposition/tasks.md`, commit with the S005 Conventional Commit subject, and push the branch.
- [x] T031 [US3] Open the official S005 pull request with issue traceability, validation evidence, accessibility/identity/documentation/changelog impact, and the bounded Codex review ledger.
- [x] T032 [US3] Process automatic Codex round 1: file every negative finding as a GitHub issue, substantively answer every comment, push warranted corrections, resolve addressed threads, and update the review ledger.
- [x] T033 [US3] Post exactly one `@Codex` request and process round 2 with the same issue, correction, reply, resolution, and evidence rules; never request round 3.
- [x] T034 [US3] Wait for all required hosted checks, verify zero unresolved review threads and zero premature S005-dependent closures, then halt with the pull request open for the owner merge ritual.

**Checkpoint**: The open S005 pull request is green and review-complete, and the owner retains sole merge authority.

---

## Phase 6: Post-Merge Housekeeping

**Purpose**: Execute only after the owner reports that S005 was merged.

- [ ] T035 Verify the actual merged main revision contains the reviewed S005 tree and recheck the public disposition evidence.
- [ ] T036 Attach current-main acceptance evidence and close #39, #41, #42, and #76 through #86 child-first.
- [ ] T037 Close parents #6 and #15 only after all listed children close; close milestones 11 and 20 only when each has zero open issues.
- [ ] T038 Close the S005 slice issue and update or close program #37 according to its definition of done while retaining the separate downstream link.
- [ ] T039 Reconcile final post-merge evidence in the next authorized repository change if needed, without requesting another S005 review round.

## Dependencies & Execution Order

- Phase 1 establishes scope and traceability.
- Phase 2 blocks every filesystem move.
- Phase 3 blocks Phase 4 because preservation proof precedes retirement.
- Phase 4 blocks final evidence and GitHub review publication.
- Phase 5 ends at the owner merge gate.
- Phase 6 begins only after an explicit owner merge report.

## Notes

- No task is marked parallel because preservation, collision checks, moves, and final-state proof form one ordered safety chain.
- Exact private paths, archive names, provider identifiers, and recovery commands belong only in the operator-held recovery record.
- A failed proof or destination collision blocks that entry. It does not authorize deletion or an inferred destination.
- Correction pushes do not trigger review requests. Exactly one explicit second-round comment is authorized.
