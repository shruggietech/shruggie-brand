# Tasks: Dark Portfolio Cards

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md)

## Phase 1: Regression coverage

- [x] T001 [US1] Add publication fixtures for dark portfolio surface and rejected white/invalid card sources in `scripts/test_prepare_site.py`.
- [x] T002 [US1] Assert dark initial cards and disclosures, copy contrast, and preserved brand-page light mode in `site/tests/site.test.mjs` and `site/scripts/verify-site.mjs`.
- [x] T003 [US2] Assert reduced SVG paths and loaded assets for every brand on both layouts.

## Phase 2: Homepage fix

- [x] T004 [US1] Generate validated `portfolioSurface` in `scripts/prepare_site.py` and render it in `site/components/brand-portfolio.tsx`.
- [x] T005 [US1] Remove obsolete light portfolio selectors from `site/app/globals.css`.
- [x] T006 [US2] Publish approved reduced-color marks to the homepage without changing SVG sources.

## Phase 3: Delivery

- [x] T007 Cross-check S055 artifacts, record analysis, and prepare patch release metadata.
- [x] T008 Run full documented validation and record evidence.
- [ ] T009 Commit, push, open PR, resolve CI and review findings, and hand off for merge and release.

## Dependencies

T001-T003 precede T004-T006. T007 follows design. T008 follows implementation. T009 follows local verification.
