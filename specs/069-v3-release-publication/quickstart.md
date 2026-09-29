# S069 Release Verification Quickstart

1. Confirm `git status` is clean, `v3.0.0` does not exist, and the source metadata resolves to BrandBuilder 3.0.0 and Brand Canon 2.0.0.
2. Run the focused release contract and publication tests, then the full documented eleven-kit, site, documentation, and archive validation. Record exact checks and any capability skips.
3. Check that the generated candidate contains the skill, portable ZIP, eight authorized brand ZIPs, notes, documentation and publication records, source commit, and checksums. No `dist/`, `release/`, `site/out/`, or `.specify/feature.json` file belongs in Git.
4. After PR review and green CI, merge the reviewed head. Verify the merge commit and its exact candidate before tagging.
5. Push `v3.0.0` at the verified `main` commit. Require tag `release-preflight`, `publish-release`, and `deploy-pages` success.
6. Compare uploaded release assets to the candidate's names and checksums. Confirm the live manual shows BrandBuilder 3.0.0 with the official release URL and all eleven brand guides remain available.
7. If any stage fails, inspect the existing tag, release, and asset inventory before retrying. Never substitute artifacts from another source revision.
