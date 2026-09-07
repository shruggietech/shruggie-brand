# Quickstart: Validate Semantic Links and Pagination

1. Run `python skill/templates/test_pipeline.py` and confirm the generated consumer anchor defaults have no global hover underline.
2. Run `python scripts/build_all.py` and confirm all five kits are clean with zero verifier problems and glyph failures.
3. Run `pnpm --dir site lint` followed by a production site build.
4. Serve the static export and run `pnpm --dir site test`.
5. Confirm representative routes pass the taxonomy, pagination, both-theme, 360 and 1280 pixel, reduced-motion, keyboard, and 200 percent zoom assertions.
6. Inspect desktop and mobile captures for the landing action, navigation, prose links, footer, cards, and first, middle, and last pagination cases.
