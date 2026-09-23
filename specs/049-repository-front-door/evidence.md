# S049 Evidence and Release Handoff

## Baseline (2026-09-23)

- Branch: `codex/049-repository-front-door`, created from clean `main` at `e2751e7`.
- Tracking issue: [#259](https://github.com/shruggietech/shruggie-brand/issues/259).
- Published latest release: [v2.0.1](https://github.com/shruggietech/shruggie-brand/releases/tag/v2.0.1). Current source and site package: 2.0.3.
- Root README named 2.0.0 skill archives, had eight `/{slug}/` brand links absent from `prepare_site.build_routes`, and had no approved brand lockup or status badges.
- Scope excludes consumer repins/usage verification, light-first generator work (#193), and custom imagery work (#194).

## Verification

- Spec Kit requirements checklist: 16/16 passing. Cross-artifact analysis found no blocking conflict; post-merge publication is explicitly deferred to owner merge.
- Test-first README audit: 23 isolated tests pass, including invalid local paths, encoded traversal, lookalike site host, noncanonical route, missing brand, bad image candidate, same-document fragment, missing latest release, stale fixed-version skill name, Markdown autolinks, and link-versus-image navigation roles.
- README audit against freshly generated `site/generated/routes.json`: 0 problems. All eight brand destinations and the site root returned HTTP 200 in a one-time manual HEAD check; official release, workflow, Build badge, release badge, and code-license badge destinations also returned HTTP 200. CI remains network-free.
- Aggregate `build_all.py` with the approved Node v24.11.0 renderer: eight production kits clean, zero verifier problems and zero glyph failures. The first local attempt used Node v26.5.0 and correctly failed I Heart PR Tours' renderer fingerprint; switching the process-local `GP_NODE` to the installed approved version resolved it without source changes.
- Release candidate: `package_release.py --version 2.0.3`, generated notes, and `release_contract.py verify` passed for nine contract-declared assets (seven brand archives and two BrandBuilder distributions). The site showcases eight brands; the README now directs readers to the release's actual asset list instead of implying every showcase has an archive. No tag or release was published.
- Site: lint and content preparation passed; production export generated 95 pages; 12 Node contract tests and 90 desktop/mobile HTML route checks passed with zero WCAG 2.1 AA violations.
- Python CI-parity suite: 18 focused script suites passed, and `test_pipeline.py` passed 70 tests. The identity-continuity suite initially received a portable-proof environment variable that CI does not supply to that suite; its CI-equivalent rerun passed 23 tests. Existing generator ResourceWarnings did not fail tests.
- Source and prepared public-documentation audits: 0 problems each. Publication artifact audit: eight expected kit markers and eight expected site markers. The audit temporarily moved the ignored local `dist/tooling` cache out of the publication tree, then restored it; no audit rule or generated kit was altered.
- `check_markdown.py`, generated-agent-contract sync, Python compile, `git diff --check`, and a 14-file UTF-8/no-BOM/LF/mojibake scan passed. Approved logo source bytes were not edited.
- Python 3.8 execution and Linux CI remain to be confirmed by the official PR checks; this local machine has Python 3.12 only.

## Review and CI ledger

- PR [#260](https://github.com/shruggietech/shruggie-brand/pull/260) opened from commit `58f14de`. The automatic Codex review is round one; no second review has been requested yet. Codex review requests are capped at two rounds total.
- Round-one Codex review identified two P2 findings: Markdown autolinks escaped route checking, and non-navigable image targets could satisfy required brand/release links. Added failing tests for both, implemented role-aware extraction for inline links, reference links, HTML anchors/images, and autolinks, then passed all 23 focused tests and the live README audit. Thread replies and CI recheck are pending the correction push.

## Post-merge release ritual

After the owner merges this PR, confirm the merge commit is the validated main revision, create the exact `v2.0.3` tag, and let the existing tag-triggered workflow certify and publish the release and Pages update. Inspect the official release for all contract-declared assets and `SHA256SUMS`. This step is not complete at pre-merge PR handoff.
