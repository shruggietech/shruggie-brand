# Quickstart: S046 Verification

1. Confirm #242-#249 and issue #250 are traceable in the candidate PR.
2. Run `python scripts/test_publication_workflow.py`, then the documented full validation in `AGENTS.md` and `.github/workflows/build.yml`.
3. Confirm all eight production kits and the site pass, including accessibility, archive, and checksum checks.
4. Watch the candidate PR's required Build checks and external reviews; resolve comments, then ask the owner for final merge.
5. Only after merge, close redundant bot PRs, tag the exact merged main commit `v2.0.1`, and verify release assets and Pages deployment.
