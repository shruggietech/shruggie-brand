# Quickstart: Validate Guidelines Reference Experience

1. Run focused tests: `python skill/templates/test_pipeline.py` and `python scripts/test_prepare_site.py`.
2. Run geometry, contract, icon, release, package, and Markdown tests from `.github/workflows/build.yml`.
3. Run `python scripts/build_all.py`; all five kits must be clean.
4. Run release packaging and verification without publishing.
5. Run `pnpm --dir site lint`, `pnpm --dir site build`, and `pnpm --dir site test`.
6. Inspect every generated guideline sheet at 360 and 1280 pixels, including dark/light wells, long catalog rows, keyboard focus, copy failure, reduced motion, deep links, and back-to-top.
7. Confirm UTF-8 without BOM, LF line endings, no mojibake, no tracked generated artifacts, and a clean diff check.
