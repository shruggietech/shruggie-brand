# Verification Evidence: S059 Canonical Brand Guideline Routes

## Route and publication contract

- Generated topic records for all eight production brands use the visible menu label as their final guideline URL segment. The optional Expressions topic follows the same rule. Duplicate or malformed paths are rejected by generator, preparation, and site checks.
- Exported Overview, Logo, and Assets pages use `/guidelines/overview/`, `/guidelines/logo/`, and `/guidelines/assets/`. The former guideline root, `/guidelines/logos/`, and `/downloads/` page URLs export small compatibility pages with a canonical reference, `noindex`, immediate client navigation, timed refresh, and a visible link. Static hosting serves those pages with HTTP 200 rather than an HTTP 301 or 308 redirect.
- Legacy bridge paths are absent from canonical route records and the sitemap. Direct `/downloads/files/**` and kit archive URL patterns remain unchanged; the registry inventory check compared published registry files with generated kits.
- The 2.6.0 release contract verified nine candidate release assets and notes locally. This evidence does not publish a formal release.

## Local checks

| Check | Result |
| --- | --- |
| `python -m unittest discover -s scripts -p 'test_*.py'` | 140 tests passed. |
| `python skill/templates/test_pipeline.py` | 88 tests passed. |
| `python skill/templates/test_glyphkit.py` | 34 checks, zero failures. |
| Interface, documentation, component, Web/React adapter, and registry contract scripts | 19, 4, 5, 5, and 10 tests passed respectively. |
| `python scripts/build_all.py` with the required Node 24.11.0 runtime for the approved I Heart PR Tours build | Eight production kits completed with zero verification problems and zero glyph failures, including PDF and contact-sheet QC. |
| `python scripts/test_registry_delivery.py` | Eight production registry catalogs and local font bundles validated; pinned shadcn CLI installed 24 UI items and a representative consumer build passed. |
| `python scripts/test_registry_delivery.py --site site/out --inventory-only` | Eight published registry inventories matched generated kits. |
| Site MDX generation, TypeScript `tsc --noEmit`, Next static build, and `node tests/site.test.mjs` | Passed; 121 static pages exported. |
| `node --test tests/production-origin.test.mjs tests/payload-contract.test.mjs` | 12 tests passed. |
| `node scripts/verify-site.mjs` | First complete sweep passed: 92 HTML routes at desktop and mobile widths, zero WCAG 2.1 AA violations. Final sweep with added legacy URL normalization and query/fragment assertions is in progress. |
| Documentation publication, Markdown, README link, release-contract, and public-documentation checks | Passed. |

## Visual review and environment

Generated guidelines contact sheets for Covarity, Cueson, ESO Weave, fragcap, Glitchpad, go-schedule, I Heart PR Tours, and ShruggieTech were visually reviewed at desktop and mobile widths; no clipped or unreadable content was observed. The default shell's Node 26 and Python without Pillow were unsuitable for the approved I Heart PR Tours reproducibility contract, so the eight-kit validation used repository-local Node 24.11.0 and the project `.venv`. The standalone toolchain probe, when run without the configured Playwright browser path, reported the raster tier; the successful full build and browser sweeps used the installed headless Chromium in ignored `dist/playwright-browsers`.

## Pending PR gates

The official PR, hosted CI, external Codex/security review, and owner merge handoff follow the authorized push. Their outcomes will be added when known.
