# Validation Quickstart: Local Companion

## Prerequisites

Use the repository's supported Python and Node runtimes, local licensed fonts, Node resvg renderer, and all full-tier dependencies reported by `skill/templates/probe.py`. Work from the `codex/064-local-companion-brand` checkout. The two owner creative decisions and current source-bound approval records are required before the full build.

## Identity checks

1. Run `python skill/templates/validate_glyph.py brands/local-companion/brand.json`. Expect zero failures; the Full mark may retain the documented 16-pixel warning because the Reduced master is used at and below 32 pixels.
2. Validate `identity-continuity.json` against the current source and regenerate the 32 proofs through the production renderer. Expect exact hashes and no source or renderer drift.
3. Inspect the Full and Reduced colorways at 256, 64, 32, and 16 pixels on dark, light, black, and white. The source-bound Gate 1 record must match the owner's approved packet.

## Kit and site checks

1. Run the repository's documented generator tests and `scripts/build_all.py`, then inspect `dist/local-companion/qc/`. Every production kit must report zero `verify.py` problems and zero glyph failures.
2. Run `scripts/test_registry_delivery.py`, release-contract tests, site lint/build/tests, and publication artifact audits. Confirm Local Companion appears in release-authorized and hosted inventories without changing existing brand results.
3. Inspect the generated social image against the exact Gate 2 copy and the owner-approved SVG and PNG hashes. Inspect the public site export for private chats, companion imagery, local paths, model contents, and unapproved screenshots.

## Release checks

After review and merge, tag the documented new builder version from a commit reachable from `main`. Confirm CI-built release assets, SHA256SUMS, the Local Companion archive, and the exact Pages artifact. Verify the live official route and download against published hashes. Do not infer live publication from a local site build or an untagged branch.
