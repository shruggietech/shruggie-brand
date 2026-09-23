# Quickstart: Validate Published Documentation and Guideline Integrity

## Prerequisites

Use the repository's documented Python environment, pinned site dependencies, and both Playwright browser revisions used in CI. Keep generated output ignored.

## Focused checks

1. Run the public-documentation source audit. It should reject injected work-slice codes or stale phrases in a temporary fixture while accepting documented current compatibility terms.
2. Run generator tests for black, white, transparent, full-color, metadata, and container preview deliveries. Their exact source bytes must remain unchanged.
3. Build the I Heart PR Tours kit and inspect its generated `guidelines/index.html`: every integration card has a visible icon or an explicit nonvisual-resource label, with passing text and meaningful graphic contrast.
4. Build and test the site. From a scrolled documentation page, follow previous and next links by pointer and keyboard at desktop and narrow widths, with normal and reduced motion. Check URL, destination heading, position, focus, fragments, and history.

## Full candidate gate

Run the commands documented in `CONTRIBUTING.md` and the additional CI jobs in `.github/workflows/build.yml`: focused Python contract and publication tests, `python scripts/build_all.py`, `pnpm --dir site lint`, `pnpm --dir site build`, `pnpm --dir site test`, release-candidate certification, and publication-content audit. Record zero verifier problems, zero glyph failures, the prepared-output prose audit result, and generated-artifact exclusion in `evidence.md`.

Do not tag or publish 2.0.2 from this work slice. Its PR is ready for the owner's final merge ritual only after all required checks and reviews are satisfied.
