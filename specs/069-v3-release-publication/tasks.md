# Tasks: BrandBuilder 3.0.0 Release Publication

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [release contract](contracts/release-publication.md)
**Prerequisites**: S067 and S068 merged; `v3.0.0` untagged

## Phase 1: Candidate metadata

- [x] T001 [US1] Confirm current tag, release, issue, branch, and candidate state; record the source revision in `specs/069-v3-release-publication/verification.md`.
- [x] T002 [US2] Move S068 release changes from Unreleased into the 3.0.0 section of `CHANGELOG.md`, preserving chronological decisions.
- [x] T003 [US2] Update the 3.0.0 migration text in `scripts/release_contract.py` and `skill/references/release-impact.json` for Brand essentials, Usage limits, and exact navigation behavior.
- [x] T004 [US2] Update `specs/068-brand-essentials-docs-navigation/verification.md` with the actual merge, review, and PR-gate outcome.

## Phase 2: Candidate verification

- [x] T005 [US1] Run focused release notes, release contract, publication workflow, documentation, and packaging tests; correct any contract drift in existing source or tests.
- [x] T006 [US1] Rebuild all eleven production kits and require zero verifier and glyph failures, PDF QC success, exact guide projection, and complete authorized archive inventory.
- [x] T007 [US2] Build and test the site, AA checks, prepared documentation, registry delivery, and semantic publication audit.
- [x] T008 [US1] Check UTF-8 without BOM, LF, mojibake, `git diff --check`, source-only Git hygiene, and generated release notes.
- [x] T009 [US3] Confirm mismatch coverage for tag, revision, candidate checksums, and publication records; add a no-clobber publisher contract assertion and document partial release inventory recovery.

## Phase 3: Reviewed publication

- [x] T010 [US1] Commit S069 source and Spec Kit evidence, push branch, and open the official PR with release scope, evidence, identity, accessibility, and documentation impact.
- [ ] T011 [US1] Resolve all first-round Codex and security findings and pass exact-head CI.
- [ ] T012 [US1] Trigger exactly one additional Codex round, resolve every resulting comment, require green checks for the final head, and do not trigger a third round.
- [ ] T013 [US1] Merge the reviewed PR and confirm the exact release commit is on `main`.
- [ ] T014 [US1] Create and push `v3.0.0` at the verified commit only after main candidate verification.
- [ ] T015 [US1] Require tag preflight and release publishing success; compare exact uploaded files and checksums to the candidate.
- [ ] T016 [US2] Require Pages deployment success and check the live release link, Brand essentials, and all eleven brand guides.
- [ ] T017 [US3] If publication fails or is partial, compare tag and release inventory and resume only with the same revision and bytes; document final disposition.

## Dependencies & Execution Order

T001 precedes metadata changes. T002-T004 precede T005-T009. All local gates precede T010. T011 and T012 precede merge. Merge and main candidate verification precede tag creation. Tag preflight precedes release upload and Pages deployment. Recovery T017 applies only when a publish step fails or requires retry.

## Done When

The exact 3.0.0 source is reviewed, green, tagged, published with eleven expected release assets including checksums, and deployed with eleven verified brand guides. Every applicable task is checked with evidence; T017 may be marked not applicable if no recovery was needed.
