# Evidence: Dark Portfolio Cards

## Baseline

2026-09-25: Owner screenshot shows white IHPRT homepage card and unreadable small full lockup. Source IHPRT `showcase_surface` is `light.card`; the existing homepage applies that light treatment to the portfolio. The independently approved IHPRT dark card surface is `#101F2C` and the published kit has its reduced-color heart.

## Validation

2026-09-25: `python dist/s053_pinned_node.py python dist/s053_validation.py` passed 21 of 22 suites on the first pass; the one failure was a test call-count expectation after two added negative fixtures. Moving surface validation before archive staging resolved it. `python scripts/test_prepare_site.py` then passed all 38 tests, including white, invalid, and missing reduced-mark mutations.

2026-09-25: `python dist/s053_pinned_node.py python scripts/build_all.py` rebuilt all eight kits. Each reported zero verifier problems and zero glyph failures. `python dist/s053_pinned_node.py pnpm --dir site lint` and `... build` passed; static export generated 96 pages.

2026-09-25: Generated `brands.json` contains eight approved dark `portfolioSurface` values and eight reduced-color SVG icon URLs. IHPRT uses `#101F2C` and `/i-heart-pr-tours/downloads/files/logos/svg/i-heart-pr-tours-mark-reduced-color.svg`; its independent `showcaseSurface` remains `#FFFFFF` for brand pages.

2026-09-25: `python scripts/package_release.py --version 2.2.1` produced nine candidate assets. `python scripts/release_contract.py verify --version 2.2.1 --release-dir release --notes release/release-notes.md` and the exact documentation publication gate passed. `python scripts/check_markdown.py`, `python -m compileall -q scripts`, and `python scripts/test_documentation_publication.py` passed.

2026-09-25: Clean registry delivery passed, including pinned shadcn installation and local-font consumer build. The marker audit of a clean eight-kit staging tree and `site/out` found exactly eight governed markers in each. The full `skill/templates/test_pipeline.py` regression passed.

2026-09-25: Inspected generated full-page desktop screenshots in both site themes and a 360px light-theme mobile screenshot. All eight initial cards/disclosures are dark; IHPRT's heart is large and legible on its `#101F2C` card. The brand's own light guide remains a separate surface. Screenshots are ignored under `site/test-results/visual/`.

2026-09-25: `python dist/s053_pinned_node.py pnpm --dir site test` passed all 12 payload/origin tests and verified 91 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. Final Markdown, whitespace, UTF-8 without BOM, LF, and common mojibake checks passed for changed files.

Pending remote CI/reviews and production publication after merge.
