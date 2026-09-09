# Evidence: Site Shell and Homepage Stabilization

## Scope and traceability

S023 implements GitHub issues #170, #171, #172, #176, #177, and #178. It changes the homepage hero and portfolio presentation, removes the obsolete system callout, adds Company and Download Skill to shared site/docs navigation, simplifies the shared footer, and stabilizes cross-route horizontal layout.

## Test-first evidence

After adding the S023 source contract but before production changes, `node --test site/tests/site.test.mjs` failed because the footer still contained Brands and the old `Download the skill` label. The contract also covered the pending homepage, shared-navigation, removed-content, and scrollbar requirements. After implementation, the same source test passed.

During rendered-test development, the first geometry run identified that the site intentionally passes `id="content"` to Fumadocs' page container for skip-link behavior. The measurement selector was corrected from the library default `#nd-page` to the actual `.docs-page` class. No production offset or selector workaround was introduced.

## Implementation evidence

- `site/app/(site)/page.tsx` renders Documentation, Download Skill, and Explore Our Portfolio in approved order, uses the unchanged `#portfolio` anchor, renders the exact Our Portfolio wording, and no longer emits the system callout.
- `site/lib/layout.shared.tsx` is the authoritative site/docs navigation source for Company and Download Skill. Both links appear in desktop and mobile variants with canonical targets and Fumadocs' `target="_blank"` plus `rel="noreferrer noopener"` behavior.
- `site/components/footer.tsx` removes Brands, uses exact Download Skill wording, retains new-tab isolation for Download Skill, Source, and License, and retains S022's same-tab Company behavior.
- `site/app/globals.css` reserves `scrollbar-gutter: stable` on the document root. Browser measurements confirmed Fumadocs already reserves a 268px desktop TOC track on pages with and without TOC items, so no redundant grid override was added.
- The shared docs target-size rule excludes `.guideline-layout`, preserving the neutral per-brand guidelines contract.

## Validation results

| Command | Result |
|---|---|
| `node --test site/tests/site.test.mjs` | Passed |
| `pnpm --dir site lint` | Passed after generated content preparation |
| `pnpm --dir site exec next build --webpack` | Passed, 76 static pages generated |
| `pnpm --dir site test` | Passed, 71 HTML routes verified at desktop and mobile widths with zero WCAG 2.1 AA violations |
| S023 geometry matrix | Passed for all six download routes, docs index, two representative docs articles, light/dark themes, device scale factors 1/2, 1280/640/360 widths, short/tall pages, and TOC/no-TOC states; drift stayed within one CSS pixel and horizontal overflow was zero |
| `python scripts/build_all.py` | Passed, 6 production kits built with zero reported problems and zero glyph failures |
| Python geometry, release, site-preparation, contract, icon, pipeline, and Markdown suites | Passed: 34 glyph checks, 2 package tests, 13 release tests, 26 site-preparation tests, 35 brand-contract tests, 14 icon tests, 46 pipeline tests, and Markdown prose policy |
| Release packaging and verification for v1.2.1 | Passed, 7 release assets and generated notes verified |
| `python skill/templates/sync_agents_md.py skill` and agent diff check | Passed, generated agent contract unchanged |

## Impact assessment

- **Accessibility**: Positive. Exact link semantics, safe external behavior, keyboard focus, 44px targets, responsive menus, reduced motion, and WCAG 2.1 AA are covered. No waivers were introduced.
- **Identity**: None. No brand source, logo geometry, palette, typography, or generated kit identity data changed.
- **Documentation**: Shared docs navigation/footer and docs layout behavior changed. Documentation content and neutral brand guidelines content did not.
- **Generated artifacts**: None committed. `dist/`, `release/`, `site/out/`, `site/generated/`, `site/public/generated/`, and screenshots remain ignored build products.
- **Changelog**: No update. S023 is a corrective website UX slice tracked by the six linked issues and does not alter the released skill, generator, canon, or kit contract.

## Review ledger

Pending pull request publication, CI, initial third-party Codex review, and the single authorized second review round.
