# S059 Validation Quickstart

1. Run focused Python route-contract tests and site tests. Confirm each active topic label maps to one canonical path, including optional Expressions, and all three former paths map directly to the new pages.
2. Build all eight kits with `python scripts/build_all.py`; require zero `verify.py` problems and zero `validate_glyph.py` failures. Compare direct download paths and approved identity source digests with the pre-S059 inventory.
3. Run `pnpm --dir site lint`, `pnpm --dir site build`, `python scripts/check_readme_links.py`, and `pnpm --dir site test`. Inspect exported canonical pages and static bridges, with and without trailing slashes, and confirm bridge `noindex`/canonical/fallback link.
4. Audit `routes.json`, sitemap, metadata, structured data, menu, breadcrumbs, pagination, and search payload. Require canonical paths only in indexable listings; `/docs/` and direct asset file paths remain unchanged.
5. Run complete CI-parity release and publication checks in `.github/workflows/build.yml`, then inspect UTF-8/BOM, line endings, mojibake, and ignored generated output before commit.
