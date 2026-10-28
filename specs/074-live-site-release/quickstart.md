# S074 Verification Quickstart

1. Verify clean source baseline, current main SHA, v3.1.0 latest release and absent v3.1.1 tag.
2. Run focused metadata tests and the documented full kit, site, accessibility, packaging and release gates. Check LF, UTF-8, mojibake and source-only Git hygiene.
3. Open a release PR, resolve all findings and require green exact-head CI. Merge and confirm the release commit on main.
4. Annotate and push v3.1.1 on verified main. Require tag build, preflight, release publication and Pages deployment success.
5. Compare release assets and SHA256SUMS, then inspect public home, References, release link, guides and downloads. Record exact evidence in `verification.md`.
