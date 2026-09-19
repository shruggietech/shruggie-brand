# Evidence: Glitchpad AppFrame Adoption Pilot

## Baseline

- Upstream repository: `shruggietech/shruggie-brand`
- Upstream baseline: `ce516dd904d9b97434a93f6f48c09766db46b1ac`
- Downstream repository: `shruggietech/glitchpad`
- Downstream baseline: `3d9a56048d01bbe2e661933e2c6eaebc7526534b`
- Upstream tracker: [#219](https://github.com/shruggietech/shruggie-brand/issues/219)
- Downstream tracker: [#196](https://github.com/shruggietech/glitchpad/issues/196)
- Cross-link: [upstream issue comment](https://github.com/shruggietech/shruggie-brand/issues/219#issuecomment-5742896201)

## Existing Consumer Boundary

- Renderer: React 19 and Vite inside the Tauri 2 application family.
- Android host: generated Tauri Android application with real `ActivityScenario<MainActivity>` WebView instrumentation on API 24 and API 36.
- Windows host: Tauri desktop build/package path plus repository shell and packaging checks.
- Existing web root: `App` returns `main.app-shell`; `html`, `body`, `#root`, and `.app-shell` claim full height, while the application menu bounds itself to the viewport.
- Existing native exception: Tauri owns native titlebar regions. The generated web AppFrame must not consume that geometry a second time.
- Missing upstream capability: AppFrame offers only its centered contained layout, and the environment bridge is coupled to the interactive Radix client entry. Glitchpad needs a bounded full-bleed shell layout and a dependency-free environment entry.

## Measurement Limitations

- No reliable historical elapsed-time, review-round, or prior-adoption baseline was recorded before S042. This slice records a prospective baseline and does not invent missing observations.
- Browser tests remain supporting evidence and cannot satisfy Android WebView or Windows Tauri host claims.
- Final actual-host results, candidate revisions, workflow runs, pull requests, and pilot observations will be appended only after they are observed.

## Verification Log

| Stage | Command or evidence | Result |
|---|---|---|
| Baseline generation | `.venv\\Scripts\\python.exe scripts/build_all.py glitchpad` | Passed at the upstream baseline with zero verification problems and zero glyph failures. |
| Contract red phase | `.venv\\Scripts\\python.exe -m unittest skill.templates.test_component_contract skill.templates.test_web_react_adapter` | Failed on the absent full-bleed recipe, adapter version, environment entry, and generated CSS before implementation. |
| Contract green phase | Focused component, Web/React, consumer-contract, and conformance suites | 33 tests passed after implementation; the broader repository contract batch also passed. |
| API 24 compatibility correction | `python -m unittest skill.templates.test_web_react_adapter` | Four focused adapter tests passed after adding generated fallbacks for selectors, viewport units, and IME measurement. The superseded CI run `35453038633` was cancelled before artifact publication so downstream cannot consume pre-correction bytes. |
| Generated site adapter mirror | CI run `35453987017`, then `python -m unittest discover -s scripts -p test_prepare_site.py` | CI correctly rejected client adapters whose newly referenced environment sibling was not staged. The mirror now copies all four generated entries, and 35 preparation tests pass locally. No verified-kit artifact from the failed run is eligible for downstream use. |
| Generated instruction Markdown | Glitchpad PR #197 `Documentation and public surface`, then interface and release-contract suites | Exact downstream import exposed that the generated consumer marker touched its following heading without a Markdown blank line. The generator now emits a formatter-stable governed block; 13 interface-contract, 20 release-contract, and 7 package-release tests pass locally. A replacement artifact is required before the downstream receipt can be final. |
| Downstream initial Codex review | Glitchpad PR #197 at `2ac0b57118ae0cf50ccc123f7108180c2bee0e44` | Two valid findings were accepted. The generated scroll container now always occupies AppFrame grid row 2 so a headerless shell fills the viewport; the downstream root contract merger will add repository-relative path context without mutating governed kit bytes. Seventeen focused Web/React and interface-contract tests pass after the upstream correction. |
| Candidate Glitchpad kit | `.venv\\Scripts\\python.exe scripts/build_all.py glitchpad` | Clean with zero verification problems and zero glyph failures; all five generated QC sheets were inspected with no new clipping or identity drift observed. |
| All production kits | `.venv\\Scripts\\python.exe scripts/build_all.py` | Covarity, Cueson, ESO Weave, Fragcap, Glitchpad, Go Schedule, and ShruggieTech were clean. I Heart PR Tours stopped before derivatives because local Node `v26.5.0` differs from its approved proof renderer `v24.11.0`; the authoritative CI Windows proof export and pinned Node workflow remain the required completion evidence. |

## Implemented Contract

- Component recipes: `1.1.0`, adding bounded `contained` and `full-bleed` AppFrame variants.
- Web/React adapter: `1.1.0`, adding `web/react/environment.tsx` without Radix or ReactDOM dependencies while preserving client-entry re-exports.
- BrandBuilder compiler: `1.3.0`, so the exact offline recovery distribution contains the new generator behavior. S042 prepares the release candidate but does not tag or publish it.
- Full-bleed AppFrame locks the generated root scroller, gives the child application shell the complete content track, and preserves generated safe-area and IME ownership.
- Modern engines use `:has()`, `100dvh`, and VisualViewport. The generated environment bridge also marks the mounted root, falls back to `100vh`, and derives legacy IME obstruction from per-orientation window-height baselines for the governed API 24 WebView.

## Ordered Merge Rule

Merge the upstream S042 contract first, then merge the downstream Glitchpad adoption. Neither repository is merged by this session; both wait for the owner's final review and merge ritual.
