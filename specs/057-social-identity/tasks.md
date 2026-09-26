# Tasks: Current Go Schedule Identity and Brand Social Images

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [social-image.md](contracts/social-image.md)

## Phase 1: Shared contract

- [x] T001 Add exact `social_copy` schema and semantic failure tests in `skill/references/canon.schema.json` and `skill/templates/test_brand_contract.py`.
- [x] T002 Implement social-copy validation and approval binding in `skill/templates/brand_contract.py`.

## Phase 2: User Story 1 - Current go-schedule mark (P1)

- [x] T003 [US1] Add exact prior-reduced versus new-full comparison test in `skill/templates/test_pipeline.py`.
- [x] T004 [US1] Copy unchanged reduced elements to Full in `brands/go-schedule/brand.json`; update current usage language in brand docs.
- [x] T005 [US1] Refresh governed current snapshot in `brands/go-schedule/identity-continuity.json`, recording owner decision and preserving historical status.
- [x] T006 [US1] Record geometry-role equivalence in `skill/templates/gen_logo.py` provenance and render Gate 1 proofs.

## Phase 3: User Story 2 - Approved social copy (P1)

- [x] T007 [US2] Add exact approved slogan and layout tests for all eight brands in `skill/templates/test_brand_contract.py`.
- [x] T008 [US2] Add governed `social_copy` records to eight `brands/*/brand.json` sources with exact approval attribution.
- [x] T009 [US2] Update canon and BrandBuilder version contract and authoring guidance in `skill/references/`, `skill/SKILL.md`, and release metadata.

## Phase 4: User Story 3 - Dedicated social deliveries (P1)

- [x] T010 [US3] Add generator and provenance regression tests for all eight identities and compatibility aliases in `skill/templates/test_pipeline.py`.
- [x] T011 [US3] Generate canonical social SVG/PNG, aliases, and I Heart PR Tours supplied-lockup composition in `skill/templates/gen_logo.py`.
- [x] T012 [US3] Classify social images separately in `skill/templates/gen_guidelines.py` and enforce dimensions, size, and metadata in `skill/templates/verify.py`.
- [x] T013 [US3] Add brand-page kit-byte test in `scripts/test_prepare_site.py`, then bind `scripts/prepare_site.py` output and portable guide compatibility.
- [x] T014 [US3] Render Gate 2 contact sheets, obtain owner creative approval, record evidence and approval digests, and update `specs/057-social-identity/`.

## Phase 5: Publication and quality

- [x] T015 Update usage, release notes, migration contract, and repository Social Preview upload inventory in docs and `scripts/release_contract.py`.
- [x] T016 Run full documented Python, kit, glyph, site, accessibility, source continuity, release, and publication gates; record results in `specs/057-social-identity/verification.md`.
- [ ] T017 Run read-only Spec Kit cross-artifact analysis, resolve findings, verify UTF-8/LF and mojibake, commit without `dist/`, push and open an official issue-linked PR.
- [ ] T018 Resolve every CI and reviewer finding; request at most one additional review round, then hand off the green PR for owner merge.
