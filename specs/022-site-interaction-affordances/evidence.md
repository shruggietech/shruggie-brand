# Evidence: Site Interaction Affordances

## Baseline

- Branch: `codex/022-site-interaction-affordances`.
- Scope: GitHub issues #163 and #164 only.
- The shared footer contained six hard-coded links in this order: Brands, Documentation, Download the skill, Company, Source, License. No link declared `target` or `rel` attributes.
- The issue contract explicitly classifies Company as same-tab even though its absolute destination uses another hostname. Hostname inference would therefore violate the named acceptance behavior.
- Dependency pagination emits a previous or next link containing an inline-flex cue row, a 16-pixel non-shrinking Lucide chevron, and a primary label paragraph. Existing site CSS changed label typography but did not own the row alignment or optical position.
- The shared light/dark switcher emits an enabled semantic `button[data-theme-toggle]` containing both theme icons. At desktop width its pre-fix computed cursor was `default` and its target measured 61 by 26 CSS pixels.

## Test-First Record

- The first source contract failed because no ordered footer destination records existed, zero records opted into separate-context behavior, and Company had no explicit same-tab declaration.
- Source contracts also failed before CSS implementation because pagination cue, stable chevron, enabled theme cursor, and disabled theme cursor selectors were absent.
- Isolated negative fixtures reject a missing separate-context classification for Source, accidental separate-context classification for Company, pagination center drift, icon shrink or size drift, missing optical correction, incorrect enabled or disabled cursors, missing button semantics, and undersized theme controls.
- The first rendered integration run exposed three test assumptions: Next canonicalizes the internal Documentation destination to `/docs/`, focusing a footer link scrolls it into view, and the desktop sidebar theme switcher is not visible in the 360-pixel mobile state. Expectations were corrected without changing production behavior.
- The next rendered run correctly found that `.docs-page` was too narrow a theme-selector scope because the switcher lives in the documentation layout sidebar. The selector now binds directly to the stable `data-theme-toggle` boundary.

## Corrected Behavior

- One ordered footer record collection owns all six labels, unchanged destinations, and explicit `internal`, `same-tab`, or `new-tab` behavior.
- Exactly Download the skill, Source, and License receive `target="_blank"` and `rel="noopener noreferrer"`. Brands, Documentation, and Company omit both attributes.
- Keyboard activation of Source opens a separate page while the originating page remains active and available. Every footer link retains a visible focus indicator and a target of at least 44 by 44 CSS pixels.
- Pagination cue rows are explicitly center-aligned, primary-label margins are zero, and chevrons retain 16 by 16 pixel non-shrinking boxes.
- Chevrons use the independent CSS `translate` property for a one-pixel optical lift, preserving the dependency's separate right-to-left rotation transform.
- Root and nested theme buttons use pointer cursors only while enabled, use `not-allowed` while disabled, and retain semantic buttons, accessible names, visible focus, keyboard theme transitions, and minimum 44-pixel targets.

## Focused Validation

- Source-level footer, pagination, theme-style, and negative-fixture contracts pass.
- `pnpm --dir site lint` passes after preparing six kits and nine reference documents.
- The normal local Turbopack build failed twice at the Windows process-launch boundary with `Access is denied` while spawning a pooled Node process. The generated MDX source existed and type-checking was green. Per repository policy, that launcher was stopped.
- `pnpm --dir site prepare:content` followed by `pnpm --dir site exec next build --webpack` produced all 76 static pages successfully. Hosted Linux CI remains responsible for exact Turbopack parity.
- `pnpm --dir site test` passes 11 source/payload tests and verifies 71 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- S022 rendered coverage includes marketing and documentation footer instances, keyboard-opened separate context, first/interior/last pagination shapes, both directions, a forced wrapped-label fixture, 360 and 1280 pixel widths, both themes, enabled and disabled theme cursor states, visible focus, and keyboard theme transitions.

## Full Validation

- Python compilation and the complete documented regression suite pass: 34 glyph-kit tests, 2 packaging tests, 13 release-contract tests, 26 site-preparation tests, 35 brand-contract tests, 14 icon-kit tests, 46 pipeline tests, and the Markdown prose-line policy.
- `python scripts/build_all.py` rebuilt all six production kits. Every kit reported `BUILD CLEAN`, zero verification problems, zero image-QC problems, zero PDF-QC problems, zero pagination splits, and zero glyph failures.
- `python skill/templates/probe.py` confirmed the full local tool tier, and `python scripts/package_release.py --version 1.2.1` produced and contract-verified the exact seven ignored release assets.
- `python skill/templates/sync_agents_md.py skill` reported the generated agent contract unchanged, and `git diff --exit-code -- skill/AGENTS.md` passed.
- Visual inspection of the generated 1280-pixel light documentation capture confirmed the shared footer and next-page cue remain intact after the interaction changes. Rendered measurements provide the corresponding mobile, dark-theme, wrapped-label, endpoint, and interior-page evidence.
- Exact hosted Turbopack parity remains a required pull-request check because the local Windows Turbopack launcher encountered the documented process-creation access boundary. The supported webpack fallback, full static export, browser matrix, and all source checks are green locally.

## Hygiene

- Generated kits, public copies, static exports, screenshots, caches, and local Spec Kit state remain ignored.
- No brand source, identity geometry, generated kit source, dependency version, information architecture, footer destination, documentation order, or theme-selection behavior changed.
- All 15 changed text files decode as strict UTF-8 without BOM, use LF line endings, and contain no detected mojibake. `git diff --check` passes, generated outputs remain untracked, and the brand, font, and generator-source boundaries have no diff.
- Final cross-artifact analysis maps all 18 functional requirements and 8 success criteria to the 36-task ledger, with no critical, high-severity, ambiguity, duplication, constitution, or unmapped-task findings.
