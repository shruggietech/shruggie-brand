# S049 Evidence and Release Handoff

## Baseline (2026-09-23)

- Branch: `codex/049-repository-front-door`, created from clean `main` at `e2751e7`.
- Tracking issue: [#259](https://github.com/shruggietech/shruggie-brand/issues/259).
- Published latest release: [v2.0.1](https://github.com/shruggietech/shruggie-brand/releases/tag/v2.0.1). Current source and site package: 2.0.3.
- Root README named 2.0.0 skill archives, had eight `/{slug}/` brand links absent from `prepare_site.build_routes`, and had no approved brand lockup or status badges.
- Scope excludes consumer repins/usage verification, light-first generator work (#193), and custom imagery work (#194).

## Verification

- Spec Kit requirements checklist: 16/16 passing. Cross-artifact analysis found no blocking conflict; post-merge publication is explicitly deferred to owner merge.
- Test-first README audit: 26 isolated tests pass, including invalid local paths, encoded traversal, lookalike and percent-encoded site hosts, noncanonical route, missing brand, bad image candidate, same-document fragment, missing latest release, stale fixed-version skill name, angle-bracket and bare GitHub autolinks, and link-versus-image navigation roles.
- README audit against freshly generated `site/generated/routes.json`: 0 problems. All eight brand destinations and the site root returned HTTP 200 in a one-time manual HEAD check; official release, workflow, Build badge, release badge, and code-license badge destinations also returned HTTP 200. CI remains network-free.
- Aggregate `build_all.py` with the approved Node v24.11.0 renderer: eight production kits clean, zero verifier problems and zero glyph failures. The first local attempt used Node v26.5.0 and correctly failed I Heart PR Tours' renderer fingerprint; switching the process-local `GP_NODE` to the installed approved version resolved it without source changes.
- Release candidate: `package_release.py --version 2.0.3`, generated notes, and `release_contract.py verify` passed for nine contract-declared assets (seven brand archives and two BrandBuilder distributions). The site showcases eight brands; the README now directs readers to the release's actual asset list instead of implying every showcase has an archive. No tag or release was published.
- Site: lint and content preparation passed; production export generated 95 pages; 12 Node contract tests and 90 desktop/mobile HTML route checks passed with zero WCAG 2.1 AA violations.
- Python CI-parity suite: 18 focused script suites passed, and `test_pipeline.py` passed 70 tests. The identity-continuity suite initially received a portable-proof environment variable that CI does not supply to that suite; its CI-equivalent rerun passed 23 tests. Existing generator ResourceWarnings did not fail tests.
- Source and prepared public-documentation audits: 0 problems each. Publication artifact audit: eight expected kit markers and eight expected site markers. The audit temporarily moved the ignored local `dist/tooling` cache out of the publication tree, then restored it; no audit rule or generated kit was altered.
- `check_markdown.py`, generated-agent-contract sync, Python compile, `git diff --check`, and a 14-file UTF-8/no-BOM/LF/mojibake scan passed. Approved logo source bytes were not edited.
- Official Linux CI run [35858387753](https://github.com/shruggietech/shruggie-brand/actions/runs/35858387753) on the reviewed implementation commit `c3cdfcf` passed the approved-identity, Python 3.8, verified-build, and aggregate build jobs. Release-preflight, publication, and Pages jobs correctly skipped on this pull request. This local machine has Python 3.12 only.

## Review and CI ledger

- PR [#260](https://github.com/shruggietech/shruggie-brand/pull/260) opened from commit `58f14de`. Codex review requests are capped at two rounds total. The automatic opening review was round one; the manual `@codex review` request on `ac5675a` was round two and the final request.
- Round one identified two P2 findings: Markdown autolinks escaped route checking, and non-navigable image targets could satisfy required brand/release links. Both were corrected in `ac5675a`, replied to, and marked resolved. Its approved-identity, Python 3.8, and full verified-build CI jobs all passed.
- Round two identified two P2 findings: bare GitHub-autolinked URLs escaped route checking, and percent-encoded URL authorities escaped site-host validation. New failing tests reproduced both. The checker now extracts bare URLs outside existing Markdown/HTML target spans, trims terminal prose punctuation, and rejects encoded authorities before host routing. All 26 focused tests, live README audit, Markdown check, and diff check passed locally. The correction was pushed in `c3cdfcf`; both findings were replied to and resolved. All four review threads across the two rounds are resolved, and no third review will be requested.
- No separate security-bot review or PR-body approval reaction arrived by this ledger update. The owner-approved two-round cap takes precedence over requesting another review. The documentation-only ledger sync commit will start a fresh CI run; its final status is checked through the PR rollup at handoff.

## Post-merge release ritual

After the owner merges this PR, confirm the merge commit is the validated main revision, create the exact `v2.0.3` tag, and let the existing tag-triggered workflow certify and publish the release and Pages update. Inspect the official release for all contract-declared assets and `SHA256SUMS`. This step is not complete at pre-merge PR handoff.
