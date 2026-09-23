# README Link Audit Contract

The command `python scripts/check_readme_links.py` reads the root `README.md` and the generated `site/generated/routes.json`. A nonzero exit means the repository front door has an invalid link or an incomplete brand inventory.

For isolated tests, callers may provide `--readme`, `--routes`, and `--root` paths. Inputs must remain inside the supplied repository root except the temporary test root itself. The command makes no network requests.

Valid local destinations are repository-contained files or directories; an optional fragment does not change the target. Encoded traversal, absolute local filesystem paths, and backslashes are invalid. The exact `https://brand.shruggie.tech` origin must point to a generated canonical route, not a plausible-looking brand prefix. A lookalike host cannot satisfy route completeness. Other HTTPS destinations may be present for GitHub workflow/release/badge links but do not satisfy brand-route coverage.

The checker reports each invalid target and every missing brand overview route. It also requires the official latest-release destination and rejects exact-version BrandBuilder distribution filenames, which become stale before the next publication. Success requires zero errors. Source HTML image references and Markdown image references are checked as local targets when relative.
