# Tasks: Dependency Integration and 2.0.1 Release

**Input**: S045 specification, plan, research, data model, release-candidate contract, and quickstart.

**Tests**: Required by the release contract and autopilot TDD gate.

## Phase 1: Setup

- [x] T001 Record the two Dependabot intake heads, current release version, and CI failure in `specs/045-dependency-release/research.md`.
- [x] T002 Validate all requirement-quality checklist markers and branch isolation in `specs/045-dependency-release/checklists/`.

## Phase 2: Foundational

- [x] T003 Add a failing dual-browser provisioning regression in `scripts/test_publication_workflow.py`.

## Phase 3: User Story 1 - Current site dependencies (P1)

**Goal**: Combine both pending dependency groups in one reproducible site candidate.

**Independent Test**: Frozen install and site lint/build/test pass with the combined direct versions.

- [x] T004 [US1] Apply both Dependabot direct-version groups plus compatible Fumadocs Core/UI to `site/package.json` and regenerate `site/pnpm-lock.yaml`.
- [x] T005 [US1] Run frozen installation and site lint/build/test, documenting results in `specs/045-dependency-release/evidence.md`.

## Phase 4: User Story 2 - Verified release build (P1)

**Goal**: Keep full-tier kit PDFs and certified archives available with both browser clients.

**Independent Test**: Workflow regression and full kit/release validation pass; hosted CI confirms both browser launches.

- [x] T006 [US2] Install both pinned browser revisions without cross-client garbage collection in `.github/workflows/build.yml`.
- [x] T007 [US2] Run the Python publication-workflow contract and full repository validation, recording results in `specs/045-dependency-release/evidence.md`.
- [x] T008 [US2] Align automation labels with the existing taxonomy in `.github/dependabot.yml` and acknowledge existing bot PR comments.

## Phase 5: User Story 3 - Reviewed 2.0.1 release (P2)

**Goal**: Deliver a green, review-complete official PR and preserve post-merge tag provenance.

**Independent Test**: PR checks and review threads are satisfied; after owner merge, tag-run release and assets verify.

- [x] T009 [US3] Update the 2.0.1 changelog and dated decision entry in `CHANGELOG.md` and complete release evidence in `specs/045-dependency-release/evidence.md`.
- [x] T010 [US3] Commit, push, and open the official S045 pull request with links to #225 and #226.
- [ ] T011 [US3] Process initial Codex/security review and at most one additional Codex request; resolve every actionable review thread on the S045 PR.
- [ ] T012 [US3] Confirm all required PR checks green, then ask the owner for final review and merge, recording the pending tag handoff in `specs/045-dependency-release/evidence.md`.
- [ ] T013 [US3] After owner merge, tag the exact merged main commit `v2.0.1` and verify the official release, assets, checksums, Pages deployment, and disposition of #225/#226.

## Phase 6: Polish and cross-cutting checks

- [x] T014 Check UTF-8 without BOM, LF endings, mojibake, generated-file exclusion, and spec/plan/task consistency in changed files.

## Dependencies and Execution Order

Setup precedes the failing regression. T003 must fail before T006. T004 precedes T005. T006 precedes T007. T005 and T007 precede the release candidate PR. T010 precedes T011 and T012. T013 is gated on the owner's final merge and cannot be completed during pre-merge review.

## Parallel Opportunities

T004 and T006 edit different files after T003 and can proceed independently; T005 and T007 may share build outputs, so execute them serially. Review and CI observation can proceed concurrently after the PR is open.

## Implementation Strategy

The first independent increment is the combined site dependency install (US1). The second restores release completeness (US2). The final increment prepares, reviews, and publishes the exact release revision (US3). No task authorizes bypassing the owner's final merge or the main-ancestry gate.
