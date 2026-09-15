# Verification Evidence: Integration Preview Visibility

## Baseline

- Branch: `codex/035-integration-preview-visibility`, created from merge commit `71ef159`.
- GitHub issue #202 was open at kickoff and its current body supplied the acceptance matrix used by the specification.
- The worktree was clean before the S035 Spec Kit artifacts were created.
- The failure path is in the shared portable guideline generator. Generated `dist/` and `site/out/` remain ignored and are not implementation targets.
- A focused I Heart PR Tours baseline build completed with `4 checks, 4 warnings, 0 failures`, `verify 0 problems`, zero image/PDF QC problems, and a clean final release manifest after using the exact pinned Node 24.11.0 renderer and shared installed dependencies.
- Pre-change portable CSS sets `.dark-well` to `#090909` without a foreground. In the light-first I Heart PR Tours guide, inherited `#111111` text measures about 1.05:1.
- Pre-change default-appearance I Heart PR Tours blue icon content measures about 2.05:1 on `#090909` and about 8.91:1 on `#F5F5F5`.

## TDD Evidence

- The focused pre-implementation preview run executed 6 tests and produced 10 expected failures: two wrong-well cases, four missing visual metadata/contrast cases, four generic nonvisual fallback cases, one mixed-delivery semantic failure, and one missing fully-transparent failure. Some tests carried more than one assertion failure.
- The first generated browser run produced 12 expected failures for the two transparent Windows target-size groups across served and direct-file desktop, narrow, and 200 percent zoom conditions because declared target metadata selected a weaker well. The resolver was tightened so measured qualifying-pixel coverage is authoritative whenever visual output is available.
- The finished focused preview suite executes 7 tests and passes all transparent, black, white, full-color, SVG-only, JSON, XML, ICO, ICNS, mixed-delivery, deterministic-output, exact-byte, escaping, and fully-transparent cases.

## Cross-Artifact Analysis

- The pre-implementation read-only analysis found zero critical and zero high issues with 16 of 16 functional requirements and 7 of 7 success criteria mapped to tasks.
- Two medium wording mismatches were reconciled before implementation: asset-byte preservation now allows intentional generated guideline and presentation-metadata changes, and the markup contract now distinguishes measured generic visuals from recognized declared black/white surface semantics.
- The final read-only reconciliation found no critical or high inconsistency. The specification, plan, data model, contract, tasks, and implementation agree that measured output selects the strongest well, SVG rasterization is measurement-only, fully transparent visuals fail clearly, and intrinsically low-contrast approved assets remain unmodified with an honest score outside the affected release gate.

## Focused Verification

- The generated I Heart PR Tours guide contains 46 asset cards: 30 visual and 16 nonvisual. Visual cards select 18 light wells and 12 dark wells. All 30 expose measured scores, with a minimum of 4.91:1, median 19.21:1, and maximum 19.91:1.
- The guide contains 19 nonvisual delivery rows and zero legacy `no-preview` placeholders. Every nonvisual card uses a visible `Nonvisual resource` treatment naming its format and role.
- The focused production build completed with `4 checks, 4 warnings, 0 failures`, `verify 0 problems`, zero image/PDF/pagination problems, and a clean 434-file final release manifest.
- `git diff -- brands assets` is empty. Temporary-fixture before/after SHA-256 maps are identical, displayed data URIs equal exact source bytes, and existing I Heart PR Tours generation tests confirm exact approved source derivations.

## Browser Verification

- Final browser verification passed 76 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- The portable asset catalog was audited at 1280 CSS pixels, 360 CSS pixels, and 200 percent zoom against both staged HTTP and the direct `file://` output. All cards passed image decoding, containment, no-transform, no-filter, visual/nonvisual exclusivity, text contrast, meaningful-pixel contrast, stronger-well selection, reflow, horizontal overflow, and axe checks.
- Six full-page screenshots were emitted. Human review of desktop, narrow, and zoom crops found legible labels and resource copy, visible light and dark artwork, intentional metadata/container treatments, contained images, intact links, and no clipping or overlap. The final I Heart PR Tours PDF contact sheet, logo sheet, favicon page sheet, and guidelines page sheet were also opened and found visually intact.

## Full CI-Parity Verification

- Python compile and brand discovery passed for all eight production slugs.
- Unit and contract suites passed: glyphkit 34, publication workflow 17 with one Windows privilege skip, package release 5, release contract 15, site preparation 30, continuity audit 4, brand contract 53, identity continuity 22, iconkit 17, and pipeline 69.
- Markdown prose line policy passed and capability probing reported the full tier with Pillow, Playwright, pikepdf, and launchable Chromium. The exact pinned Node 24.11.0 renderer was used for proof-bound builds and tests.
- The final `scripts/build_all.py` run built all eight production kits with zero reported problems. Every kit reported `verify 0 problems` and its glyph gate reported 0 failures.
- Release v1.2.1 certification generated and verified all 9 expected release assets and validated release notes. `sync_agents_md.py` reported the generated `skill/AGENTS.md` unchanged.
- Fresh site preparation copied 8 kits and 10 reference documents. MDX generation, TypeScript, the 81-page Next.js static build, 12 site contract tests, the 76-route browser verifier, and publication audit all passed. Publication audit reported 8 kit markers and 8 site markers.

## Preservation and Repository Hygiene

- Generated `dist/`, `site/out/`, `release/`, `site/test-results/`, dependency trees, and `.specify/feature.json` remain ignored and are not staged.
- No file under `brands/` or `assets/` changed. No logo path, raster, container, metadata, declaration, icon manifest, or approved proof source was edited.
- The governed diff is limited to the shared generator template, generator regression tests, browser verification harness, changelog, and synchronized S035 specification artifacts.
- `git diff --check`, Markdown policy, UTF-8/BOM/CR checks, mojibake scan, generated-artifact exclusion, and final task review pass before the local commit.
