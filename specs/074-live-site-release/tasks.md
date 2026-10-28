# Tasks: BrandBuilder 3.1.1 Live Site Release

**Input**: [spec.md](spec.md), [plan.md](plan.md), [publication contract](contracts/publication.md)

## Phase 1: Candidate

- [x] T001 [US1] Confirm main, official release, deployment workflow and version policy in `research.md`.
- [x] T002 [US2] Update seven brand versions, BrandBuilder/site versions, release impact, migration guidance and dated histories.
- [x] T003 [US2] Update current-version contract tests and source-bound continuity hashes.
- [x] T004 [US1] Run focused and full documented validation, inspect output and record evidence.
- [x] T005 [US2] Check source-only Git hygiene, UTF-8/LF, mojibake and release notes.

## Phase 2: Publication

- [ ] T006 [US2] Commit source and evidence, push and open the release PR.
- [ ] T007 [US2] Resolve review findings and require green final-head CI.
- [ ] T008 [US2] Merge the reviewed PR and verify main revision and candidate.
- [ ] T009 [US2] Annotate and push v3.1.1 at verified main.
- [ ] T010 [US2] Require tag preflight, official release and Pages jobs to succeed, then compare assets and SHA256SUMS.
- [ ] T011 [US1] Verify the live site and record exact final evidence.

## Done When

The exact reviewed revision is tagged and published as v3.1.1, the release assets pass integrity checks, Pages is green, and the public site shows S072 and S073 changes.
