# Verification: S062 WordPress Brand Delivery

## Issue disposition

| Issue | Delivered behavior | Evidence |
| --- | --- | --- |
| #273 | Source-derived native `theme.json` presets, independent identity and interface colors, local licensed fonts, brand-scoped content CSS, core-block mappings, dark Site Editor variation, adapter/support/version contracts, and effective override precedence. | `test_wordpress.py` synthetic mapping and tamper cases, eight clean kit builds, live editor/front-end probes on both pinned WordPress/PHP pairs, and `verify_wordpress.py` inventory validation. |
| #274 | Installable brand-specific block theme with templates, parts, native Home navigation, four editable patterns, approved media, direct public ZIP downloads, client update/rollback guidance, and CI runtime fixtures. | Both live fixture pairs installed the ZIP, edited/saved/reopened a page, rendered search/archive/404, checked local fonts and assets, retained saved Global Styles and footer overrides through update/rollback, and emitted drift records. |

## Completed local gates

- The final `scripts/build_all.py` run generated all eight production kits with `BUILD CLEAN`; each includes zero `verify.py` problems and zero `validate_glyph.py` failures. The existing approved identity geometry in `brands/` was unchanged.
- The full `skill/templates/test_pipeline.py` suite passed 91 tests with the approved proof and headless renderer environment. `skill/templates/test_wordpress.py` passed 10 synthetic cases, including optional social-preview fallback, same-prefix namespace separation, independent colors, missing assets/fonts, unsupported theme format, dark variation drift, ZIP tampering, and traversal rejection.
- The pinned WordPress 6.9.9/PHP 8.2 and WordPress 7.1.2/PHP 8.3 fixtures passed with the final go-schedule ZIP. Each exercised native pattern registration, editor save/reopen without block recovery, published output, Home navigation, local font and media loading, non-root asset URL composition, long-word reflow at 390px, keyboard focus, search/archive/404 templates, and axe WCAG 2.1 AA at 390px and 1440px with zero violations.
- Each runtime fixture installed an updated ZIP, observed the changed theme file, restored the pinned prior ZIP, and confirmed the page, saved Global Styles color pair, and saved footer template part remained effective. `dist/wordpress-runtime/drift-<version>.json` records the generated background default, saved value, effective value, and resolution for baseline, update, and rollback.
- `scripts/test_publication_workflow.py` passed 25 tests. The hosted publication audit, using an isolated eight-kit staging tree because local `dist/` also contains development tool caches, passed with 8 brands, 8 governed kit markers, 8 site markers, 8 packages, and 1,922 public files. The direct WordPress ZIP copy is included in the byte inventory and tamper tests.
- Site lint and static export passed. `scripts/test_registry_delivery.py` installed 24 UI items and local fonts in a clean pinned shadcn consumer. `scripts/audit_public_documentation.py --sources` and `--prepared` each reported zero problems. The v2.7.0 release contract verified nine candidate assets and generated notes. The pinned WordPress fixture dependency audit reported zero vulnerabilities.

## Remaining gate

- The exported site's headless browser verifier is running. Record its final result here, then repeat the static export after the final WordPress manual wording adjustment and rerun the publication audit before PR creation.

## Scope limits

The support matrix claims only the two WordPress/PHP pairs exercised above. Classic themes, builders, forms, commerce, multilingual systems, caching plugins, and a client-specific production site have not been tested. This slice prepares release candidates in CI; public release publication is separate from the PR.
