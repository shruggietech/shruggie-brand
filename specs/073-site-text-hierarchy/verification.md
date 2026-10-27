# Verification: Site text hierarchy and containment

**Slice**: S073 | **Date**: 2026-10-27 | **Issues**: #310, #311, #335

## Source and analysis gates

- Synced `origin/main` before research and created `codex/073-site-text-hierarchy` from `92525759541a51b7a5b07328c6bc711807945c2c` in an isolated worktree. The existing S072 checkout was left untouched.
- Spec Kit prerequisites and read-only analysis passed for the numbered specification, plan, contract, checklist, and tasks. The requirements checklist has no unchecked items.
- All 68 reference entries have unique IDs and exactly four ordered labeled fields. Reversing only the new Markdown list syntax reproduces the committed reference source exactly, including all wording, IDs, and link targets.
- The first full browser run reported no failures in the new References structure, inbound-anchor, 320px/390px/200% containment, portfolio copy and anchor, or unaffected Conformance heading assertions. Its sole failure was the first title threshold described below.
- `python scripts/check_documentation_references.py`: passed, all IDs and local citations resolve.
- `python scripts/check_markdown.py`: passed, Markdown prose line policy.
- The CI source test matrix passed locally, including package/release, documentation, identity, messaging, color, interface, web, WordPress adapter, conformance, iconkit, registry, and pipeline suites. `python -m compileall -q scripts skill/templates` passed. The separate glyphkit suite passed 43 checks with zero failures.
- `git diff --check`: passed after final validation. A byte scan of all 19 changed text files found UTF-8 without BOM, LF-only endings, and no mojibake markers. `.specify/feature.json`, `dist/`, `site/out/`, and `site/node_modules/` are ignored.

## Validation-gate dependency repair

- The existing WordPress fixture lockfile failed the current moderate-or-higher audit gate (six findings, including a high-severity `body-parser` advisory). Pinned verified patched releases of `qs` 6.16.1, `body-parser` 1.20.9, and `fast-uri` 3.1.9, then regenerated only the fixture lockfile.
- `npm ci --prefix scripts/wordpress-runtime --ignore-scripts`: passed with zero reported vulnerabilities.
- `npm audit --prefix scripts/wordpress-runtime --audit-level=moderate`: passed with zero vulnerabilities.
- `npm test --prefix scripts/wordpress-runtime`: 11/11 passed after clearing the command runner's `GIT_PAGER` and `PAGER` variables, which the fixture's simple-git security parser rejects. The first environment-influenced runs were 10/11; no test or security check was weakened.

## Production and site gates

- `python skill/templates/probe.py`: full capability tier, including a working Chromium browser.
- `python scripts/build_all.py`: all 13 production kits built with zero reported problems. Each completed kit reported a clean build, zero PDF QC problems, zero pagination splits, and zero glyph failures. Generated contact sheets for all 13 kits were visually reviewed; no new clipping or identity defects were observed.
- `python scripts/test_brand_essentials_delivery.py` and `python scripts/test_registry_delivery.py`: passed.
- `pnpm --dir site lint`: passed, with 13 kits and 18 reference documents prepared.
- `pnpm --dir site build`: passed, with 196 static pages generated.
- `python scripts/check_readme_links.py`: passed with zero problems.
- `python scripts/test_wordpress_runtime.py --pair 6.9.9` and `--pair 7.1.2`: passed native install, update/rollback, non-root URL, and live asset checks. The command runner's pager variables were cleared as for the fixture test.
- The first full `pnpm --dir site test` run failed one new S073 assertion: at 1168px, DanceWithMe865 remained at 24px with 19.26px of inner-edge clearance. The original 8px reserve did not cause the requested reduction. All other browser assertions completed without a reported failure. The implementation reserve and specification were raised to 24px.
- A focused local browser measurement on the corrected export found the 1170px five-column transition produces a 210.20px Dance card with an 18px title and 41.84px clearance. At 1280px, the title is one line at 18.2px with 25.23px clearance. Covarity stays at 24px at both widths. A temporary synthetic longer name wrapped at the 18px lower bound with zero horizontal overflow and kept its marker in the card. The temporary test script was removed.
- The corrected `pnpm --dir site test` passed all 12 Node contract tests, completed 278 route and viewport checks, completed 99 visual route and viewport checks across both themes, and verified 139 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The home and References screenshots were inspected at desktop and narrow widths; the portfolio introduction remains grouped beneath its heading, titles remain inside cards, and all References fields remain distinct and readable. The 320px, 390px, and 200% reflow checks passed without horizontal overflow. Keyboard-focus and contrast checks passed within the full site verifier.
- PR #336 received a Codex P1 review finding that fixed-pixel title fitting could cancel a visitor's enlarged browser default font size. The title now keeps its rem-based size and wraps when the root font exceeds the standard default. A new rendered assertion checks 125% and 200% default font sizes, distinct from CSS zoom. Its first full run exposed 200% card overflow from the pre-existing fixed rem icon width and an unbreakable description word, while confirming the title was 48px and retained 48.55px of marker clearance. The icon now stays square within the card and the description wraps. A second focused measurement found the old absolute description overlay clipped vertically at 200%; the stage now sizes to its description and action layers. On the final export at 200%, the card scroll width equals client width (208px), card scroll height equals client height (1127px), and description scroll height equals client height (494px). The temporary diagnostic scripts were removed.
- On the review fix, `pnpm --dir site lint` passed and a clean `pnpm --dir site build` generated 196 static pages. The final `pnpm --dir site test` passed 12 Node tests, 278 route and viewport checks, 99 visual route and viewport checks across two themes, and 139 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The first two incremental rebuild attempts failed because a local Turbopack CSS worker exited before connecting; removing only the ignored `site/.next/` cache restored the documented build, which then passed on each clean rerun. A sandboxed test attempt could not find its isolated Playwright browser; the final suite ran headlessly in the installed browser environment.

## Review boundaries

No generated `dist/` kit, site export, raster image, PDF, local dependency directory, or `.specify/feature.json` belongs in the commit. No brand message or logo geometry changed.
