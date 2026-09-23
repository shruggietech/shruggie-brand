# Tasks: Published Documentation and Guideline Integrity

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [contracts/publication.md](contracts/publication.md), [quickstart.md](quickstart.md)

**Tests**: Required by S047 and the project constitution. Create failing focused checks before each correction.

**Organization**: Setup, foundational inventory, the three independently testable user stories, then full integration and delivery.

## Phase 1: Setup

- [x] T001 Confirm clean `codex/047-published-docs-integrity` baseline, three open issues, feature state, constitution, and CI commands in `specs/047-published-docs-integrity/evidence.md`
- [x] T002 Record the fifteen-page manual inventory, production brand guidance paths, prepared outputs, and exact source-to-publication boundaries in `specs/047-published-docs-integrity/evidence.md`

## Phase 2: Foundational

- [x] T003 Add failing 2.0.2 version, migration, and archive expectations in `scripts/test_release_contract.py` and `scripts/test_package_release.py`, preserving historical 2.0.1 coverage
- [x] T004 Establish 2.0.2 patch-candidate version and migration classification in `skill/SKILL.md`, `site/package.json`, `skill/references/release-impact.json`, `scripts/release_contract.py`, `CHANGELOG.md`, and `skill/CHANGELOG.md`

## Phase 3: User Story 1 - Present-version guidance

**Goal**: Reader-facing manual and kit instructions are direct, current, and free of planning leaks.

**Independent test**: Audit source and prepared manual/kit output, then inspect representative compatibility and recovery guidance.

- [x] T005 [US1] Add failing positive and negative fixtures for slice codes, unjustified Spec Kit mentions, stale prose, compatibility exceptions, unsafe paths, and cross-brand publication isolation in `scripts/test_public_documentation.py`
- [x] T006 [US1] Implement the bounded source/output prose audit using the governed manual and production inventories in `scripts/audit_public_documentation.py`
- [x] T007 [US1] Rewrite public manual sources, including toolchain, operating-mode, logo, and voice references, in `skill/references/*.md` while preserving active contract terms
- [x] T008 [US1] Rewrite reader-facing Cueson and ESO Weave history in `brands/cueson/README.md`, `brands/cueson/NOTES.md`, and `brands/eso-weave/NOTES.md`; reconcile any additional published guidance flagged by the audit
- [x] T009 [US1] Patch changed guidance versions in `brands/cueson/brand.json`, `brands/eso-weave/brand.json`, and `brands/fragcap/brand.json`, and update exact kit expectations in `scripts/test_release_contract.py`
- [x] T010 [US1] Add a failing transformation assertion, then prevent `Brand Canon` and `Interface Canon` corruption in `scripts/test_prepare_site.py` and `scripts/prepare_site.py`
- [x] T011 [US1] Run source and prepared-output prose checks against every manual page and production kit, documenting reviewed exceptions in `specs/047-published-docs-integrity/evidence.md`

## Phase 4: User Story 2 - Readable integration cards

**Goal**: Visual icon previews and nonvisual resource cards are clear and pass local-surface contrast.

**Independent test**: Generated portable guide fixtures and the I Heart PR Tours file pass contrast without altering source assets.

- [x] T012 [US2] Add failing visual/nonvisual delivery and contrast fixtures, including black, white, transparent, full-color, XML, metadata, and container cases, in `skill/templates/test_pipeline.py`
- [x] T013 [US2] Implement explicit well foreground roles, appearance-aware visual selection, and nonvisual-resource labels in `skill/templates/gen_guidelines.py` without changing embedded asset bytes
- [x] T014 [US2] Add rendered portable-file assertions at desktop, narrow, and 200 percent zoom in `site/scripts/verify-site.mjs`
- [x] T015 [US2] Inspect all affected I Heart PR Tours integration cards and record measured contrast and unchanged source hashes in `specs/047-published-docs-integrity/evidence.md`

## Phase 5: User Story 3 - Correct page transitions

**Goal**: Bottom documentation pagination lands at the new heading and focus while preserving fragments and history.

**Independent test**: Actual click and Enter transitions from scrolled sources pass at desktop/mobile widths and reduced motion.

- [x] T016 [US3] Add failing scrolled-source pagination, focus, fragment, direct-load, and history regression cases in `site/scripts/verify-site.mjs`
- [x] T017 [US3] Add the Next smooth-scroll route opt-in in `site/app/layout.tsx` and a scoped pagination focus handoff in `site/components/documentation-pagination-focus.tsx` and `site/app/docs/[[...slug]]/page.tsx`
- [x] T018 [US3] Run rendered browser cases for pointer, keyboard, reduced motion, and representative previous/next routes; record geometry in `specs/047-published-docs-integrity/evidence.md`

## Phase 6: Integration and delivery

- [x] T019 Integrate source and prepared-output prose audit into `.github/workflows/build.yml` without weakening existing kit, security, accessibility, or publication gates
- [x] T020 Run all focused Python tests, generator/native contracts, minimum-version compatibility checks, and Markdown checks listed in `.github/workflows/build.yml`; record results in `specs/047-published-docs-integrity/evidence.md`
- [x] T021 Run capability probe, `scripts/build_all.py`, 2.0.2 release-candidate certification, generated-agent consistency, site lint/build/test, and publication-content audit in the foreground; record zero kit/glyph failures in `specs/047-published-docs-integrity/evidence.md`
- [x] T022 Audit UTF-8 without BOM, LF, mojibake, generated-artifact exclusion, preserved logo/source hashes, and `git diff --check` in `specs/047-published-docs-integrity/evidence.md`
- [x] T023 Re-run Spec Kit cross-artifact analysis and reconcile `spec.md`, `plan.md`, `tasks.md`, contracts, and implementation before commit
- [x] T024 Commit the candidate with a Conventional Commit subject, push `codex/047-published-docs-integrity`, and open a PR closing #236, #237, and #202 with scope and verification evidence
- [x] T025 Process every actionable Codex/security review comment, request at most one additional Codex round if needed, and wait for all required CI checks to pass before requesting the owner's final review and merge in `specs/047-published-docs-integrity/evidence.md`

## Phase 7: Post-merge CI correction (2026-09-23)

- [x] T026 Reproduce the failed `main` Gate 2 path from run 35819083608 and add tests for one mismatch, repeated mismatch, unrelated export failure, and destination confinement in `scripts/test_export_approved_identity_proofs.py`
- [x] T027 Keep the exact approved hash gate while adding one clean mismatch retry and failed-proof artifact capture in `scripts/export_approved_identity_proofs.py` and `.github/workflows/build.yml`
- [ ] T028 Run focused tests, Spec Kit cross-artifact analysis, and the complete CI gate on the follow-up PR; record final results in `specs/047-published-docs-integrity/evidence.md`

## Dependencies

- T001-T004 establish inventory and candidate identity before generated output changes.
- US1, US2, and US3 are independently testable after foundational tasks. Their test tasks precede their correction tasks.
- T019-T025 require the three stories to pass. The final PR may need a follow-up commit for review findings; no release tag is part of S047.

## Parallel opportunities

Read-only research for each user story can be parallel. Implementation is serialized where tasks touch shared generated output or site browser tests. No task may overwrite in-flight brand updates.

## Implementation strategy

Deliver US1's current guidance and audit first, then US2's preview fix, then US3's navigation correction. Validate each independently before the full 2.0.2 candidate gate. The slice is complete only when all three issues, the full build, and PR review/CI are satisfied.
