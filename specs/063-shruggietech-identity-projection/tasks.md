# Tasks: ShruggieTech Identity Projection

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), and [contracts/](contracts/)

**Tests**: Required by FR-008 and the project constitution. Write focused regressions first and confirm they fail for the old behavior.

## Phase 1: Setup and inventory

- [x] T001 Inventory ShruggieTech square, paired, social, PDF, portable, hosted, and metadata consumers in `specs/063-shruggietech-identity-projection/verification.md` with exact source fields and generated paths.
- [x] T002 Capture unchanged paid-source digests and existing approval bindings from `brands/shruggietech/brand.json` and `brands/shruggietech/identity-continuity.json` in `specs/063-shruggietech-identity-projection/verification.md`.

## Phase 2: Foundational role contract

- [x] T003 Add failing ShruggieTech square-source and vivid-pixel regressions in `skill/templates/test_iconkit.py` and `skill/templates/test_pipeline.py`.
- [x] T004 Add failing exact-slogan, superseded-approval, and retained-introduction regressions in `skill/templates/test_brand_contract.py` and `scripts/test_prepare_site.py`.

## Phase 3: User Story 1, correct square delivery

- [x] T005 [US1] Declare reduced-face standalone roles and source-bound mask method in `brands/shruggietech/brand.json`, preserving paid source bytes and full arms paired roles.
- [x] T006 [US1] Generate square-proportioned reduced SVG/PNG projections and a vivid antialiased face in `skill/templates/gen_logo.py`.
- [x] T007 [US1] Route every web, PWA, Android, Apple, macOS, Windows, and store square role to the reduced face and correct manifest source labels in `skill/templates/iconkit.py`.
- [x] T008 [US1] Validate square source roles, rendered interior color, safe area, and source/approval integrity in `skill/templates/verify.py` and `skill/templates/brand_contract.py`.
- [x] T009 [US1] Update mark-role and download guidance in `brands/shruggietech/README.md` and the source-fed guide fields in `brands/shruggietech/brand.json`.
- [x] T010 [US1] Produce and inspect ignored 16, 32, 48, and larger square proofs; record measured results and applicable existing Gate 1 decision in `specs/063-shruggietech-identity-projection/verification.md`.

## Phase 4: User Story 2, portfolio scale

- [x] T011 [US2] Add a failing portfolio source and responsive-scale regression in `scripts/test_prepare_site.py` and the relevant `site/` tests.
- [x] T012 [US2] Project the verified square reduced source through `scripts/prepare_site.py` and adjust `site/components/brand-portfolio.tsx` or `site/app/globals.css` only as needed for peer-card scale and accessible responsive layout.
- [ ] T013 [US2] Compare desktop and narrow mobile renders across all published cards; record source path, perceived-size evidence, text alternative, contrast, and overflow results in `specs/063-shruggietech-identity-projection/verification.md`.

## Phase 5: User Story 3, exact slogan

- [x] T014 [US3] Record the exact slogan and superseded S057 classification in `brands/shruggietech/brand.json` and its provenance, retaining separate introductory uses.
- [x] T015 [US3] Trace and correct any slogan-labeled generated guide, social, manifest, or site projections in `skill/templates/` and `scripts/prepare_site.py`; keep source-only fixes in templates.
- [x] T016 [US3] Generate the provisional assembled social image, present exact SVG/PNG and source hashes for existing Gate 2 review, and record the actual decision in `brands/shruggietech/brand.json` and `specs/063-shruggietech-identity-projection/verification.md`.

## Phase 6: Cross-cutting verification and PR

- [ ] T017 Run focused regressions, the full `CONTRIBUTING.md` validation, all eight kit gates, the existing i-heart-pr-tours 32-proof continuity gate, site build/tests, and publication audit; record exact results in `specs/063-shruggietech-identity-projection/verification.md`.
- [x] T018 Update the unreleased change log and any architecture-affecting decision entry in `CHANGELOG.md`; check UTF-8/LF, mojibake, generated-output hygiene, and `git diff --check`.
- [ ] T019 Commit S063 on `codex/063-shruggietech-identity-projection`, push the authorized branch, open the official PR, and attach it to this task.
- [ ] T020 Monitor all required CI and external reviews; reply to and resolve every review thread, make needed corrections, and request at most one additional Codex review round. Hand off only with definitive green required checks and satisfied reviews.

## Dependencies and independent tests

T001-T004 establish the inventory and red regressions. US1 then provides the correct square source for US2. US3 can be developed against the current `social_copy` contract, but its final social image may change if US1 changes a paired composition. T010 and T016 retain existing owner approval stops. T017-T020 depend on all three stories and recorded approvals.

- **US1**: Build the icon suites and inspect every square asset and manifest variant against the unchanged reduced source.
- **US2**: Render the portfolio with the corrected square source and compare all brand cards at desktop and narrow mobile widths.
- **US3**: Compare exact slogan bytes and labels across source, generated social artwork, guide, and site while preserving introductory roles.
