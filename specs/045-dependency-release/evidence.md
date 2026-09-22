# S045 Verification Evidence

## Intake and compatibility

- Kickoff open Dependabot inventory: #225 at `3400a23c44e494be27424be2a30a417625f591f4` and #226 at `72f90bd274c4fe65f8da4eda3d4fc0dcd00d15e1`.
- #226's original hosted failure omitted `brand-guide.pdf` after installing only the Node Playwright browser revision. The existing Python verifier remained pinned to Playwright 1.62.0.
- Initial combined site build failed because Fumadocs MDX 15.4.1 imported `fumadocs-core/server`, absent from Core 16.14.3. Pairing Core and UI at 16.15.11 restored the build.
- The repository's `area: site` label was applied to both bot PRs. The previously configured `site` and `skill` labels were changed to existing area labels in `.github/dependabot.yml`.

## Local test-first evidence

- Added `test_verified_build_installs_both_playwright_browser_revisions` to `scripts/test_publication_workflow.py`; it failed against the old workflow, then passed after the browser-install correction (18 tests total).
- `pnpm@10.28.2 --dir site install --frozen-lockfile`: PASS.
- `pnpm@10.28.2 --dir site lint`: PASS.
- `pnpm@10.28.2 --dir site build`: PASS, 95 static pages generated.
- `pnpm@10.28.2 --dir site test`: PASS, 12 contract tests and 90 HTML routes at desktop/mobile widths, zero WCAG 2.1 AA violations.
- `python scripts/test_release_contract.py`: PASS, 27 tests.
- `python scripts/test_package_release.py`: PASS, 8 tests.
- `python scripts/check_markdown.py`: PASS.
- `python scripts/release_contract.py current`: `2.0.1`.
- `python skill/templates/probe.py`: full capability tier, Chromium launches.
- First local `build_all.py` run passed seven kits but rejected I Heart PR Tours proof renderer identity: local default Node 26.5.0 did not match its approved Node 24.11.0. This was an environment mismatch, not a source change. Regenerated the ignored local proof using installed Node 24.11.0 and reran with `GP_NODE` and `GP_APPROVED_PROOF_ROOT` matching the CI proof path.
- CI-matched `python scripts/build_all.py`: PASS, 8 production kits, zero reported problems, required PDFs and PDF QC present.
- `python scripts/package_release.py --version 2.0.1`: PASS, eight brand archives plus the skill and portable bundle.
- `python scripts/release_contract.py notes --version 2.0.1 --output release/release-notes.md`: PASS.
- `python scripts/release_contract.py verify --version 2.0.1 --release-dir release --notes release/release-notes.md`: PASS, 9 release assets and generated notes.
- `python scripts/audit_publication_artifacts.py --kits dist --site site/out`: PASS, 8 kit markers and 8 site markers.
- Remaining CI-parity Python tests: `test_glyphkit.py`, `test_prepare_site.py`, `test_identity_continuity_audit.py`, `test_brand_contract.py`, `test_interface_contract.py`, `test_documentation_contract.py`, `test_component_contract.py`, `test_web_react_adapter.py`, `test_egui_adapter.py`, `test_conformance.py`, `test_identity_continuity.py`, and `test_iconkit.py` all PASS. The pipeline suite initially failed without the approved proof environment; with the CI-matched proof root and Node 24.11.0 it passed all 68 tests.
- Changed tracked files and S045 text passed `git diff --check`, UTF-8 no-BOM/LF byte inspection, and a common-mojibake scan. No generated `dist/`, release archive, site export, or registry file is staged.
- Security and tenancy behavior are not changed by this slice: dependency provenance and release fail-closed tests remain mandatory, while no tenant-owned data or authorization boundary is introduced.

## Pending publication gates

- Official S045 PR: [#241](https://github.com/shruggietech/shruggie-brand/pull/241). The automatic Codex code review completed without findings and left a thumbs-up reaction on the PR body. One additional `@codex security review` was requested; no further review rounds are authorized or planned.
- Both intake PRs have the existing `area: site` label and a response to Dependabot's missing-label comment linking #241. Their final close-as-superseded disposition waits for #241 to merge.
- Confirm all required GitHub PR checks and external reviews are satisfied.
- Owner performs final review and merge. Only then push the exact merged `v2.0.1` tag and observe official release publication, checksums, and Pages.
