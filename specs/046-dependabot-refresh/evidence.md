# Evidence: Post-Merge Dependabot Refresh

## Intake and design

- #241 merged at `1ad9c36ac2867f954ca927fb95610ac1499b8d1f` on 2026-09-22 23:34 UTC.
- S045 bot PRs #225 and #226 are closed. Eight new bot PRs #242-#249 appeared after that merge.
- No `v2.0.1` tag or release existed at S046 kickoff; tagging is deferred until the follow-up candidate merges.
- Five action revisions were checked against upstream release tags, including peeled pnpm annotated tag.

## Analysis gate

The S046 spec, plan, tasks, contract, and intake agree on eight PRs and the owner's merge boundary. No constitution conflict or unresolved clarification remains. The immutable-source regression must be updated in lockstep, not disabled.

## Verification

- Test-first contract: `test_external_actions_are_immutable_and_expected` failed with expected `v7.0.1` versus old checkout comment `v6.0.2`; after coordinated action and allowlist updates, all 18 publication workflow tests pass.
- `python -m pip install --user --disable-pip-version-check --no-input -r requirements.txt`: PASS on Python 3.12.9; installed fontTools 4.65.0, pikepdf 10.13.0.post1, and Playwright 1.63.0. Python 3.8 markers remain unchanged for hosted compatibility.
- `python -m playwright install chromium`: PASS.
- `python scripts/build_all.py` with approved Node 24.11.0 and proof root: PASS, eight production kits, zero reported problems. ESO Weave PDF and desktop/mobile guideline sheets were visually spot-checked with no obvious rendering regression.
- `python scripts/test_release_contract.py` (27 tests), `test_package_release.py` (8 tests), `test_prepare_site.py` (36 tests), `test_identity_continuity_audit.py` (4 tests), `scripts/check_markdown.py`, and the remaining template regression suites including `test_pipeline.py`: PASS. The first broad local test command incorrectly set `GP_APPROVED_PROOF_ROOT` for `test_identity_continuity.py`; rerunning it without that variable, as CI does, passed. No source correction was needed.
- `npx --yes pnpm@10.28.2 --dir site install --frozen-lockfile`: PASS. The globally available pnpm 11 initially rejected the existing lockfile under its newer release-age policy; using the repository-pinned pnpm 10.28.2 reproduced the hosted toolchain and passed.
- `npx --yes pnpm@10.28.2 --dir site lint` and `build`: PASS, 95 static pages.
- `python scripts/package_release.py --version 2.0.1`: PASS, eight brand archives plus skill and portable bundle.
- `python scripts/release_contract.py notes` and `verify`: PASS, nine versioned assets and generated notes.
- `python scripts/audit_publication_artifacts.py --kits dist --site site/out`: PASS, eight kit and eight site markers.
- `npx --yes pnpm@10.28.2 --dir site test`: PASS, 12 contract tests and 90 HTML routes at desktop/mobile widths with zero WCAG 2.1 AA violations.
- All eight PDF contact sheets were visually inspected for obvious clipping or rendering regressions; the ESO Weave desktop/mobile guideline sheet was also inspected. No issue found.
- `git diff --check`, `scripts/check_markdown.py`, strict UTF-8/no-BOM/LF inspection of 14 changed source and specification files, mojibake scan, and generated-file exclusion: PASS. No `dist/`, site export, release archive, or `.specify/feature.json` is staged.
- Hosted PR gates are pending PR creation.

## Release handoff

Pending owner merge, exact merged-main tag, official release assets, checksums, and Pages deployment.
