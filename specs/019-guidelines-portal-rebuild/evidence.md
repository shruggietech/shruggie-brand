# Verification Evidence: Hosted Guidelines Portal Rebuild

## Scope and traceability

S019 resolves the corrective epic #157 and its child issues #158, #159, #160, and #161. It supersedes only S017's hosted one-page presentation. The generated kit remains the source of truth, logo geometry and source bytes are unchanged, and the standalone HTML guide remains available under each brand's downloads.

## Architecture decision

The implementation deviated from the initial generated-MDX projection after inspecting the installed Fumadocs interfaces. A single validated `site/generated/guidelines.json` registry now feeds direct static Fumadocs route trees. This removes a second generated content representation, preserves one projection boundary, and keeps all 40 brand-topic pages statically enumerable.

## Generated contract

- Each of five production kits emits `guidelines/portal.json` plus `guidelines/index.html`.
- Each portal exposes eight ordered topics, complete dark and light palettes, semantic visual families, nonvisual resources, rendered instruction blocks, and a portable-guide path.
- Portal publication rejects unsafe paths, missing files, digest disagreement, duplicate deliveries, and unsupported Markdown constructs before writing site data.
- Representative visual records retain every verified size, format, variant, alias, and destination in their disclosure details. ICO, ICNS, JSON, XML, and Markdown files render as resources instead of fake image previews.

## Automated verification

- Python compilation: `python -m compileall -q skill/templates scripts` passed.
- Unit suites: 31 glyph checks, 2 package tests, 13 release-contract tests, 25 publication tests, 28 brand-contract tests, 14 icon tests, and 44 pipeline tests passed.
- Markdown policy: `scripts/check_markdown.py` passed.
- Capability probe: full tier with Chromium, Pillow, ImageMagick, pikepdf, Playwright, fontTools, and coloraide available.
- Production build: `scripts/build_all.py` rebuilt all five kits. Every `verify.py` result reported 0 problems and every glyph gate reported 0 failures.
- Site typing and preparation: `pnpm --dir site lint` passed.
- Static export: `pnpm --dir site exec next build --webpack` produced 66 pages, including all 40 guideline topic routes.
- Browser contract: `pnpm --dir site test` verified 61 HTML routes at 360 and 1280 pixels with zero WCAG 2.1 AA violations. It also measured all five landing headings at 360, 768, 1024, and 1280 pixels and 200 percent zoom.

The ordinary local Turbopack build was attempted twice and reached source collection, but the Windows host denied creation of a Turbopack worker process. The source file named in the diagnostic existed and the supported Webpack build completed cleanly. Linux CI remains the authoritative ordinary `pnpm build` check.

## Visual review

The generated portable guideline desktop and 390-pixel sheets were opened for Covarity, Fragcap, Glitchpad, Go Schedule, and ShruggieTech. Hosted overview captures were reviewed in light and dark themes at 360 and 1280 pixels for every brand. The Glitchpad color and asset routes were additionally reviewed as the densest shared-layout cases. No clipping, horizontal overflow, blank preview cards, overlapping footer actions, or illegible heading wraps were observed.

## Completion state

All S019 tasks are complete locally. Generated kits, site exports, browser captures, caches, and `.specify/feature.json` remain ignored and were not staged.

## Publication and review

- Implementation commit: `289e3e5` (`feat(S019): rebuild hosted guideline portals`).
- Pull request: [#162](https://github.com/shruggietech/shruggie-brand/pull/162).
- CI: the current-head Build run `34162563224` passed both `python-38-compatibility` and the full `build` job. The superseded initial run `34162559920` also completed green.
- External review round one: the automatic Codex connector reported that its review quota was exhausted, so it produced no findings.
- External review round two: the single authorized `@Codex review` request received the same quota response and produced no findings. No further review round was requested.
- Review disposition: both connector responses were acknowledged on the pull request, no review threads or inline comments exist, and the pull request reports a clean merge state.
