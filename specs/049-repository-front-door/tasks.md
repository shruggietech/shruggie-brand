# Tasks: Repository Front Door and v2.0.3 Release Readiness

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [README link contract](contracts/readme-links.md)

**Tests**: Required by FR-005 through FR-007 and the autopilot test-first discipline.

## Phase 1: Setup

- [x] T001 Record issue #259, current README defects, latest published release, branch state, and scope boundaries in `specs/049-repository-front-door/evidence.md`.

## Phase 2: Foundational README Link Contract

- [x] T002 Add failing valid, missing-file, traversal, lookalike-host, invalid-route, omitted-brand, image, and badge fixtures in `scripts/test_check_readme_links.py`.
- [x] T003 Implement deterministic repository-local and generated-route validation in `scripts/check_readme_links.py` until T002 passes.

## Phase 3: User Story 1 - Find the right brand and download (P1)

**Goal**: Visitors recognize the approved brand and reach the current official distribution and eight canonical guideline pages.

**Independent test**: Audit the root README against generated route data and inspect its light/dark image references.

- [x] T004 [US1] Replace stale artifact names and eight invalid brand URLs, add approved theme-aware branding and useful download guidance in `README.md`.
- [x] T005 [US1] Run the focused README audit against generated site routes and correct any remaining destinations in `README.md`.

## Phase 4: User Story 2 - Trust front-page status and links (P2)

**Goal**: Contributors see useful Build, release, and code-license badges, with regression protection for README destinations.

**Independent test**: Verify each badge label/destination and prove an invalid route or local file fails CI's deterministic audit.

- [x] T006 [US2] Add labeled Build, latest-release, and code-only license badges in `README.md`.
- [x] T007 [US2] Run focused link tests in both Python test tiers and the live README audit after site route generation in `.github/workflows/build.yml`.

## Phase 5: User Story 3 - Publish a traceable v2.0.3 release (P3)

**Goal**: Candidate metadata and guidance are consistent and ready for exact-main tagging after owner merge.

**Independent test**: Full release-candidate verification passes and README points only to already published release entry points before tag.

- [x] T008 [US3] Reconcile 2.0.3 release notes, current-source and latest-publication wording, and exact post-merge release sequence in `CHANGELOG.md` and `specs/049-repository-front-door/evidence.md`.
- [x] T009 [US3] Validate all contract-declared candidate packages, notes, and checksums with `scripts/package_release.py` and `scripts/release_contract.py`; record results in `specs/049-repository-front-door/evidence.md`.

## Phase 6: Cross-Cutting Completion

- [x] T010 Run the full documented build, glyph, site, accessibility, identity, publication, encoding, and hygiene gates; record evidence in `specs/049-repository-front-door/evidence.md`.
- [ ] T011 Commit and push `codex/049-repository-front-door`, open an issue-linked PR, resolve all received review comments within at most two Codex review rounds, and wait for green CI; record the PR ledger in `specs/049-repository-front-door/evidence.md`.

## Dependencies and Execution Order

T002 must fail before T003. T003 establishes the checker used by US1 and US2. Complete US1 before US2 so badges land on an otherwise correct front page. US3 certification follows documentation/CI changes, then cross-cutting validation and PR work. The formal tag and publication follow owner merge and therefore are documented as pending rather than falsely marked complete in this pre-merge task list.

## Parallel Opportunity

Read-only release metadata inspection and approved-logo inspection are independent. README edits, checker integration, and CI changes remain serialized to keep the link contract consistent.
