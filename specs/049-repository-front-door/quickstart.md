# Quickstart Validation: S049

1. Run `python scripts/test_check_readme_links.py`. The isolated temporary fixtures must pass valid targets and reject missing local paths, traversal, wrong site routes, lookalike hosts, and omitted brand routes.
2. Run `python scripts/build_all.py`, then `pnpm --dir site lint`, `pnpm --dir site build`, and `python scripts/check_readme_links.py`. The generated route contract must cover all eight README brand links.
3. Run the documented production, site, release contract, and artifact audits in `.github/workflows/build.yml`, including `python scripts/package_release.py --version 2.0.3`, release notes generation, and `python scripts/release_contract.py verify --version 2.0.3 --release-dir release --notes release/release-notes.md`.
4. Inspect the GitHub README in light and dark themes; open badge destinations and the current latest-release page. Keep release asset publication pending until owner merge and exact `v2.0.3` tag.
