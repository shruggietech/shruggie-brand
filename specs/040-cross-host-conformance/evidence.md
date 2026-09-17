# Verification Evidence: Cross-Host Conformance Fixtures

## Result

S040 implements issue #217 as a generated cross-host conformance system for all eight production brands. The system publishes seven browser capability profiles, executes distinct Tauri Android, Wails Windows, and egui reference tracks, rejects cross-track evidence substitution, reproduces the known-bad duplicate-inset trace, verifies the corrected ownership trace, and emits screenshot candidates that remain pending explicit human review.

## Toolchain

- Python 3.12.9
- Node.js 24.11.0 for the governed identity and site runs
- Cargo 1.96.0
- Go 1.24.2 windows/amd64
- Next.js 16.3.4 with Playwright 1.62.1

## Automated Verification

- `python -m compileall -q scripts skill/templates`: passed.
- `python skill/templates/test_conformance.py`: 11 tests passed, including deterministic generation, known-bad and corrected traces, evidence boundaries, diagnostics, baseline decisions, and executable generated Rust and Go fixtures.
- `python skill/templates/test_web_react_adapter.py`: 4 tests passed.
- `python skill/templates/test_egui_adapter.py`: 3 tests passed, including generated rendered-state execution.
- `python scripts/test_prepare_site.py`: 35 tests passed.
- `python skill/templates/test_pipeline.py` with the approved Node 24.11 renderer: 68 tests passed.
- `python scripts/test_publication_workflow.py`: 17 tests passed.
- `python scripts/test_package_release.py`: 7 tests passed.
- `python scripts/test_release_contract.py`: 20 tests passed.
- `python scripts/check_markdown.py`: passed.
- `python scripts/build_all.py`: all eight production kits reported `BUILD CLEAN`, zero `verify.py` problems, and zero glyph failures.
- Generated Tauri Android fixture: 2 tests passed, including rejection of the known-bad trace.
- Generated Wails Windows fixture: Go tests passed.
- Generated egui fixture: 6 rendered-state and contract tests passed.
- TypeScript lint path and Next.js production build: passed, with 91 static pages generated.
- Node payload and production-origin tests: 12 tests passed.
- `node scripts/verify-site.mjs`: verified 86 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- `python scripts/audit_publication_artifacts.py --kits dist --site site/out`: found exactly 8 governed kit markers and 8 governed site markers.

## Profile and Evidence Counts

- Production brands: 8.
- Component recipes per brand: 15.
- Capability profiles per brand: 7.
- Host tracks per brand: 4, each published with supported reference status plus exact host, renderer, target, and tool policy versions.
- Browser brand-profile combinations: 56.
- Screenshot candidates and checksummed candidate manifests: 56, all `pending-human-review`.
- Public conformance routes: 9 total, one index and one route per production brand.

## Accessibility and Interaction Impact

The browser track checks WCAG 2.1 A and AA rules, keyboard-visible controls, 44 by 44 CSS pixel visible targets, horizontal clipping, responsive portrait and landscape viewports, reduced motion, forced colors, and 200 percent text scaling. The generated Android trace additionally covers orientation changes, IME appearance, resize, usable safe geometry, and duplicate inset ownership. Wails evidence keeps window-chrome overlap diagnostics separate from visual and accessibility diagnostics.

## Identity and Source Impact

No brand source, approved logo geometry, palette, typography, or identity-continuity record changed. Generated conformance manifests bind brand, interface, compiler, adapter, and conformance contract versions plus the exact source revision supplied by CI. Generated kits, static exports, screenshots, candidate manifests, and native build targets remain ignored and are not committed.

## Visual Review

Representative Glitchpad phone portrait, I Heart PR Tours forced-colors, and ShruggieTech 200 percent text-scale captures were visually inspected for profile controls, generated specimen visibility, host evidence boundaries, responsive flow, and vendor disclosure. The stylesheet bundle was corrected and rebuilt after visual inspection exposed a stale incremental bundle. Final automated captures reset scroll position before full-page screenshots.

No candidate has been promoted to an accepted baseline. Promotion requires a separate human decision that matches the candidate identity, source revision, versions, viewport, fonts, renderer, and image digest. Browser-reference evidence does not claim actual-host execution or downstream consumer adoption.

## CI and Review Boundary

The pull request workflow reruns the minimum Python 3.8 contract suite, authoritative Node 24.11 identity proof, full verified build, site build, Playwright and axe verification, publication audit, and ephemeral conformance-candidate upload. CI results and external review responses are recorded on the pull request rather than in this repository file.
