# Evidence: S015 Glitchpad Identity Color Approval

## Baseline

- Branch: `codex/015-glitchpad-color-system`
- Issue: #146
- Base revision: `694cd911c8500648803cbd4a9947e1bce7d0b86b`
- S014 prerequisites: #144 and #145 closed by merged PR #150.
- Current production role mapping: full-color paper `#A8A39D`, fold `#FFD900`, wordmark `#F2F5FA`; light paper `#0A0A0A`, fold `#867100`, wordmark `#0A0A0A`.
- Generated comparison output is exploratory, ignored, and ineligible for production publication.

## Decision ledger

- Owner requested a halt after the proposed coloring is ready and before production promotion.
- Owner rejected all Revision 1 candidates because the study incorrectly treated the square as optional rather than permanent glyph structure.
- Owner established that every Glitchpad glyph must be square-based and must contain the protected rectangular page construction.
- Owner permanently rejected muddy deep gold (`#867100`). It is prohibited from every revised candidate and must be removed from production if a Revision 2 direction is approved.
- The rejected Revision 1 Sulfur Plate samples also exposed a study composition defect: a flush 800 by 800 plate was inserted into the legacy 800 by 1000 page canvas, causing the full, reduced, and actual-size children to clip. Revision 2 replaces that composition rather than patching its symptoms.
- Revision 2 compared `sulfur-square`, `charcoal-square`, and `slate-square` using one identical safe square composition.
- Owner requested a bounded Revision 3 mix: Sulfur Square dark mode paired with Charcoal Square light mode.
- Revision 3 dark roles are surface `#121416`, square and square edge `#FFD900`, page `#0B0C0D`, fold `#667788`, and wordmark `#F2F5FA`.
- Revision 3 light roles are surface `#F8F8F6`, square and square edge `#0B0C0D`, page `#FFD900`, fold `#667788`, and wordmark `#0A0A0A`.
- Owner disposition: Revision 3 explicitly approved on 2026-09-07 with the instruction to continue forward.

## Comparison evidence

- Protected geometry fingerprint over path strings and fill rules: `ec36a47b2b39d00501163fc189b8dfe8d780580496f013771ccc2301548fb843`.
- Protected lockup-layout fingerprint: `8d5ca8d2a54e56831a20735d4f374ffd824e0f2e5f5f79b8c05a8a78f4bfb1ad`.
- The deterministic study emitted `comparison.svg`, `comparison.html`, and `measurements.json` under ignored `dist/.s015-color-study/`; the inspection-only `comparison.png` was rendered there with ImageMagick. `git check-ignore -v` resolves every file to the repository's `dist/` rule.
- Six focused tests pass. They cover revised matrix completeness, uppercase hexadecimal values, explicit rejection of `#867100`, geometry fingerprints, required contrast relationships, non-mutation of `brands/glitchpad/brand.json` and `skill/templates/gen_logo.py`, required samples, and safe square containment for every full and reduced mark.
- Every direction was inspected in dark and light contexts as full, reduced, horizontal, stacked, 16, 24, 32, and 48 pixel full/reduced samples, desktop file-list icons, Android launcher icons, and store artwork.
- Direction A places sulfur on the square. Its square edge measures 13.34:1 on dark and 18.41:1 on light; charcoal page-to-square is 14.15:1 and slate fold-to-square is 3.33:1.
- Direction B places sulfur on the page inside charcoal. Its square edge measures 13.34:1 on dark and 18.41:1 on light; sulfur page-to-square is 14.15:1 and slate fold-to-square is 4.25:1.
- Direction C places sulfur on the fold inside slate. Square-edge contrast is 4.01:1 dark and 4.33:1 light; charcoal page-to-square is 4.25:1 and sulfur fold-to-square is 3.33:1.
- Neutral wordmarks measure 16.90:1 dark and 18.62:1 light in all directions.
- Revision 2 uses a 1000 by 1000 study composition with the square inset 62 units, a 24-unit contained edge, and the unmodified 720 by 900 page paths uniformly scaled to 72 percent and centered. Full, reduced, and all child contexts were visually inspected with no clipping, stretching, double plating, or missing square.
- Revision 3 regenerates that identical composition as one focused proposal. Dark square edge-to-surface is 13.34:1, page-to-square is 14.15:1, and fold-to-square is 3.33:1. Light values are 18.41:1, 14.15:1, and 4.25:1 respectively. Full, reduced, actual-size, lockup, desktop, Android, and store samples were inspected with no clipping or role leakage.
- The study preserves canonical page paths and source lockup data. No production source, generated kit, site export, registry, archive, PDF, or raster deliverable was changed or published.

## Post-approval implementation evidence

- `brands/glitchpad/brand.json` now declares the approved 1000 by 1000 permanent square, 62-unit inset, 142-unit corner radius, 24-unit edge, and 72 percent uniformly scaled inner page. The dark role mapping is sulfur square, charcoal page, slate fold, and `#F2F5FA` wordmark; the light mapping is charcoal square, sulfur page, slate fold, and `#0A0A0A` wordmark.
- The Reduced master retains the complete square and page and removes only the fold. Its source role changed from `accent` to `neutral` so it follows the contextual page role; its protected `d` and `fill_rule` values remain unchanged.
- Shared schema, contract validation, logo generation, source-owned contextual wordmark roles, monochrome knockout generation, guide metrics, and web-guideline metrics support the optional composition without slug-specific generator branches. Unconfigured brands retain their prior behavior.
- Generated full, light, reduced, horizontal, stacked, black, and white masters changed to the permanent-square composition and were classified against the approved roles. Desktop, Android, web, iOS and iPadOS, macOS, Windows, favicon, registry, guideline, PDF, and product-page outputs changed through those masters and retain the square. The type specimen has no glyph treatment, so its logo-color disposition is inapplicable and its typography output was verified unchanged.
- The generated logo sheet was visually inspected across full and Reduced marks at 128, 64, 32, and 16 pixels on dark and light surfaces. The guideline and Glitchpad product-page sheets were inspected at desktop and 390-pixel widths. No clipping, stretching, missing square, lost page, or Full/Reduced hierarchy defect was observed.
- The generated guidelines describe the delivered `1000 × 1000` canvas, 50-unit clear space, and 5.6 percent artwork-width relationship rather than the protected inner page's legacy canvas.
- `python scripts/build_all.py glitchpad` completes with `verify.py` reporting 0 problems, glyph validation reporting 0 failures, image QC reporting 0 problems, PDF QC reporting 0 problems, and pagination reporting 0 split elements.
- The geometry-only fingerprint remains `ec36a47b2b39d00501163fc189b8dfe8d780580496f013771ccc2301548fb843`; the lockup-layout fingerprint remains `8d5ca8d2a54e56831a20735d4f374ffd824e0f2e5f5f79b8c05a8a78f4bfb1ad`. Source diff inspection confirms no protected path string or lockup measurement changed.
- The prohibited `#867100` value is absent from production source. Its remaining committed mentions are historical decision evidence and regression assertions that reject it.
- Focused tests pass: 23 brand-contract tests, 27 pipeline tests, 13 icon-kit tests, 31 glyphkit checks, 6 decision-study tests, 12 release-contract tests, 20 site-preparation tests, and 11 site payload/origin tests. Markdown prose policy, Python compilation, generated-agent synchronization, strict UTF-8 without BOM, LF-only endings, mojibake scanning, and `git diff --check` also pass.
- The complete `python scripts/build_all.py` run builds all five production kits with zero reported problems. Release packaging and certification verify all seven versioned assets, including `glitchpad-brand-1.1.0.zip`.
- The local Windows host denies Turbopack's pooled worker-process spawn with OS error 5 despite the referenced generated MDX file being present. The same prepared site source compiles and statically exports all 26 routes through Next.js webpack, then browser verification passes desktop and mobile widths with zero WCAG 2.1 AA violations. Hosted Linux CI remains the authority for the standard Turbopack command.

## Publication and review

- Implementation commit: `fab16b5` (`feat(S015): approve Glitchpad square identity`).
- Official pull request: #152, `S015: Approve Glitchpad square identity`.
- The pull request body records `Fixes #146`, identity approval, accessibility impact, generated contact-sheet inspection, and the local Windows Turbopack limitation.
- Hosted round-one CI passed both Python 3.8 compatibility and the complete Linux build on the implementation and publication commits.
- Round-one Codex review raised two findings. The P1 platform-monochrome finding was accepted: Android adaptive monochrome and iOS tinted exports now receive the generated knockout master rather than recoloring the opaque full-color silhouette. A new measured topology regression proves transparent/opaque Android regions and white/black iOS tinted regions. The P2 task-state finding was accepted and T028/T029 were synchronized with the completed gate.
- Post-review verification passes 14 icon-kit tests, 27 pipeline tests, and a complete five-kit build with zero reported problems. Generated Android monochrome alpha samples confirm a transparent page center and opaque square/G regions; the iOS tinted image was visually inspected as a black square with white page and black G.
- The single authorized final Codex review round was triggered with `@Codex review` against `3a7c2ba`; no further review round will be requested. Its two P2 findings were accepted. Generated web guidance now distinguishes the 50-unit external clear-space band from the protected 70-unit internal G channel, and square-enclosure validation measures both Full and Reduced source bounds and rejects unsafe fit with a contract error before rendering. Focused contract, pipeline, icon, Markdown, and Glitchpad build gates pass after both corrections, and the regenerated guideline sheet was visually inspected.
