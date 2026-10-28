# S072 Validation Guide

1. Run .venv/Scripts/python.exe skill/templates/test_messaging.py for exact role, independent states, consumer fallback and escaping regressions.
2. Run .venv/Scripts/python.exe skill/templates/test_brand_contract.py and test_identity_continuity.py. Validate all current brand sources and required source-bound records.
3. Review decisions.md and inventory.md against issue #309 and subsequent owner selections. Check exact punctuation and unchanged social_copy values.
4. After copy selection concludes, follow every command in CONTRIBUTING.md and applicable .github/workflows/build.yml checks. Run scripts/build_all.py for all production brands; require zero verify.py problems and validate_glyph.py failures. Review changed PDF/portable/hosted message surfaces without PDF/PNG byte comparison.
5. Check generated WordPress hero patterns and Next.js OG alt text for canonical approved descriptions; absent/unresolved values must omit description markup and use title-only alt.
6. Run site preparation, lint/build/test/accessibility and publication audits, source encoding and Markdown checks, git diff --check, and generated artifact exclusion checks. Store precise results in verification.md. A focused pass is not full slice completion.
