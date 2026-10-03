# S070 Validation Guide

Prerequisites: repository Python environment and bundled fonts; measured renderer and full-tier probe; hidden non-interactive launch for non-Git console tools on Windows. Follow current CONTRIBUTING.md and .github/workflows/build.yml for the complete release gate.

1. Validate the private brief with `skill/templates/authoring_brief.py dist/private/insonic/brief.json`. Current records carry explicit owner decisions for both creative gates. Historical review-stage assets remain immutable.
2. Run `skill/templates/validate_glyph.py` on the candidate construction helper. Expect zero failures; explain any permitted warnings and inspect the render.
3. Generate the production 32-proof matrix and full Gate 1 source/palette/renderer evidence, inspect it, and record exact owner approval before promotion.
4. Validate the private Gate 2 packet using `authoring_brief.py BRIEF --gate-2 PACKET --brand-root brands/insonic`. Expect current Gate 1 binding and distinct complete checksummed derivatives. Record owner Gate 2 and social image approval before final build.
5. Build the final kit with `scripts/build_all.py insonic`; expect zero verify problems and zero glyph failures. Inspect logo/contact sheets, guide, application and social outputs; run applicable render/pagination checks.
6. Run the documented aggregate contract tests and renderer-grouped production builds, source audits, registry delivery checks, site lint/build/test, publication audits, encoding/mojibake scan, and `git diff --check`.
   Run the WordPress fixture's frozen install, `npm test --prefix scripts/wordpress-runtime`, unchanged moderate-threshold npm audit and both pinned runtime pairs. The owner-authorized uncached transport replaces the affected test-only HTTP-cache chain.
7. After the reviewed tagged release and site deployment, check official routes, archive inventory, and live SHA-256 agreement. Pending CI or routes do not satisfy completion.
