# S017 Verification Evidence

## Baseline

- Branch: `codex/017-guidelines-reference-experience`, created from merged S016 commit `3d56bab`.
- Issues: #147 asset reference, #148 color references and scoped light examples, #149 neutral navigation.
- Identity boundary: no brand path, authoritative source, canonical palette, affiliation record, or release version may change.
- Artifact boundary: generated kits, screenshots, PDFs, raster exports, registries, and release archives remain ignored.

## Spec Kit Analysis

Specification, clarification, requirements checklist, experience checklist, plan, research, data model, contracts, quickstart, and chronological tasks are present. Final analysis covered 20 functional requirements, 6 measurable success criteria, 3 P1 stories, and 20 chronological tasks. It found zero consistency, ambiguity, duplication, coverage, or constitution issues. The convergence pass checked the implemented generator, publisher, tests, and documentation against the same contract and added no remediation tasks.

## Verification

### Test-first and focused checks

- Manifest grouping, largest-preview selection, skipped capability disclosure, missing-file rejection, alias retention, container-size extraction, deterministic conversion, and conversion round trips were exercised in `test_pipeline.py`.
- Hosted asset rewrite, traversal rejection, missing-target rejection, metadata preservation, and exactly-one-exit behavior were exercised in `test_prepare_site.py`.
- The final focused matrix passed: 39 pipeline tests, 22 prepare-site tests, 28 brand-contract tests, 14 icon-kit tests, 13 release-contract tests, 2 package-release tests, and 31 glyph checks with zero failures.
- Python compilation and the Markdown prose policy passed. Generated `skill/AGENTS.md` remained synchronized.

### Production and publication gates

- `scripts/build_all.py` rebuilt Covarity, Fragcap, Glitchpad, Go Schedule, and ShruggieTech. Every kit reported `BUILD CLEAN`; the aggregate reported five kits with zero problems. Every `verify.py` report had zero problems and every glyph report had zero failures.
- Release packaging created and verified all seven version 1.2.1 assets without publishing them.
- Site preparation and TypeScript lint passed. A production build with Next.js's supported webpack builder compiled, type-checked, generated all 26 static pages, and completed build traces.
- The normal Windows Turbopack launcher failed to spawn its pooled Node child with operating-system error 5 and misleadingly named an existing generated MDX file as missing. This matches the established local host limitation; hosted Linux CI remains the authoritative Turbopack result.
- Browser verification passed 11 payload/origin tests and all 26 HTML routes at 360 and 1280 pixels with zero WCAG 2.1 AA violations. The guideline checks prove exact manifest-derived path coverage, no duplicate delivery links, governed dark/light wells, 44 px copy targets, clipboard success and denial announcements, a no-script top anchor, a progressive focus-safe back-to-top interaction, reduced motion, 200 percent zoom, and exactly one hosted `All brands` exit.

### Visual and integrity review

The five responsive guideline sheets were inspected at 1280 and 390 pixels. The identity colors, header lockups, compact contents, color cards, theme wells, typography, and component samples remained aligned without clipping or overflow. A full-page ShruggieTech capture was also inspected through the complete catalog; semantic cards, light/dark grounds, long delivery lists, Full and Reduced forms, and compatibility alias rows remained readable and visually quiet. No generated kit, screenshot, PDF, raster export, registry, or release archive is included in the source diff.

## Publication

- Pull request: https://github.com/shruggietech/shruggie-brand/pull/155
- Automatic Codex review: completed against `73cd7e0`. Its two findings covered complete dark/light token references and macOS integration-role preview deduplication. Both are implemented with focused regressions and complete local gates.
- Optional second review round: pending exactly one authorized `@Codex review` request after the corrective commit.
- Hosted CI and final review state: pending the corrective head.
