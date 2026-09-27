# Tasks: Canonical Brand Guideline Routes

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [route contract](contracts/routes.md)

## Phase 1: Contract and failing tests

- [x] T001 [US1] Add generated topic label/path and duplicate-slug regressions in `skill/templates/test_pipeline.py` and `scripts/test_prepare_site.py`.
- [x] T002 [US2] Add legacy bridge and preserved direct-download assertions in `site/tests/site.test.mjs` and `site/scripts/verify-site.mjs`.
- [x] T003 [US3] Add canonical-only route, metadata, sitemap, and navigation assertions in site and Python tests.

## Phase 2: Canonical topic generation

- [x] T004 [US1] Derive every topic path from its visible label in `skill/templates/gen_guidelines.py`; preserve semantic keys and optional-topic behavior.
- [x] T005 [US1] Validate generated label/path grammar and build canonical topic route records in `scripts/prepare_site.py`.
- [x] T006 [US1] Consume generated topic paths in `site/lib/guidelines.ts` and canonical topic rendering in `site/app/(guidelines)/[slug]/guidelines/[[...topic]]/page.tsx`.

## Phase 3: Compatibility and publication

- [x] T007 [US2] Export static bridges for guidelines root, legacy Logo, and legacy Assets, with accessible fallback, canonical, and `noindex`.
- [x] T008 [US2] Keep `/downloads/files/**` and archive URLs unchanged; add direct file inventory checks.
- [x] T009 [US3] Migrate layout, homepage, README checker, breadcrumbs, vendor links, and documentation route dispositions to canonical paths.
- [x] T010 [US3] Verify canonical-only search, metadata, structured data, robots/sitemap, and export inventory.

## Phase 4: Validation and handoff

- [x] T011 Update version and changelog for 2.6.0 route contract, retaining Brand Canon and identity versions.
- [ ] T012 Run focused and full Python, eight-kit/glyph, site lint/build/browser, release-contract, accessibility, and publication gates; save evidence in `verification.md`.
- [ ] T013 Audit UTF-8/LF, mojibake, ignored generated output, and spec/plan/task consistency; commit and push.
- [ ] T014 Open official PR, attach it to this chat, resolve CI and every review comment, trigger at most one second review round, then request owner merge review.

## Dependencies and execution order

T001-T003 establish expected failures. T004-T006 implement the single route grammar. T007-T010 migrate compatibility and publishing consumers. T011-T013 verify the completed slice. T014 follows the authorized push. Site and generator tests are necessary because route records are a public contract and GitHub Pages cannot supply server redirects.
