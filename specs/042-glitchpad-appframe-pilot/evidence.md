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
| Candidate Glitchpad kit | `.venv\\Scripts\\python.exe scripts/build_all.py glitchpad` | Clean with zero verification problems and zero glyph failures; all five generated QC sheets were inspected with no new clipping or identity drift observed. |
| All production kits | `.venv\\Scripts\\python.exe scripts/build_all.py` | Covarity, Cueson, ESO Weave, Fragcap, Glitchpad, Go Schedule, and ShruggieTech were clean. I Heart PR Tours stopped before derivatives because local Node `v26.5.0` differs from its approved proof renderer `v24.11.0`; the authoritative CI Windows proof export and pinned Node workflow remain the required completion evidence. |

## Implemented Contract

- Component recipes: `1.1.0`, adding bounded `contained` and `full-bleed` AppFrame variants.
- Web/React adapter: `1.1.0`, adding `web/react/environment.tsx` without Radix or ReactDOM dependencies while preserving client-entry re-exports.
- BrandBuilder compiler: still `1.2.1`, the current released distribution. S042 does not perform a release; the candidate commit and manifest checksums identify exact unreleased bytes.
- Full-bleed AppFrame locks the generated root scroller, gives the child application shell the complete content track, and preserves generated safe-area and IME ownership.

## Ordered Merge Rule

Merge the upstream S042 contract first, then merge the downstream Glitchpad adoption. Neither repository is merged by this session; both wait for the owner's final review and merge ritual.
