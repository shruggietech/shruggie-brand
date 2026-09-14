# Verification Evidence: Portfolio Card Consistency

## Baseline

- Branch: `codex/033-portfolio-card-consistency`, created from `origin/main` at merge commit `a27e33b4c3d823383b9d3fbe3af99019c099cea3`.
- GitHub issues #199 and #200 were both open at kickoff.
- The worktree contained only new S033 Spec Kit artifacts before implementation.
- `.gitignore` already excludes generated kits, static exports, generated registries, release artifacts, dependency trees, caches, local environments, and machine-local Spec Kit state. No ignore-file change was required.
- The static public portfolio has no authentication, private storage, user input, or tenant boundary. Applicable safety checks preserve exact generated destinations, explicit downloads, non-navigating articles, and inaccessible-hidden-control prevention.

## Observed pre-change behavior

- `site/components/brand-portfolio.tsx` injected every available `showcaseSurface` and `showcaseForeground`, causing I Heart PR Tours to render as a white card with black copy.
- `site/app/globals.css` used muted description text by default and inherited action-label colors.
- Desktop action anchors were hidden only with opacity and pointer suppression, leaving them in the keyboard tab order before visible reveal.
- The action stage minimum was 5.5 rem while two 44-pixel actions plus their gap require more vertical space.
- The homepage notice deduplicated and rendered every detailed `vendorBoundary` string, so additional third-party projects could add paragraphs.

## Baseline command results

| Command | Result |
| --- | --- |
| `node site/tests/site.test.mjs` | PASS |
| `.venv/Scripts/python.exe scripts/check_markdown.py` | PASS, `Markdown prose line policy: passed` |
| `.venv/Scripts/python.exe scripts/prepare_site.py` | PASS after removing two exact ignored S032 review PNGs from `dist/i-heart-pr-tours/qc/s032-review/`; `prepared 8 kits and 10 reference documents` |
| `site/node_modules/.bin/fumadocs-mdx.CMD` | PASS with repository-scoped dependency access |
| `site/node_modules/.bin/tsc.CMD --noEmit` | PASS |

The global Corepack `pnpm` shim points to a missing cached pnpm 12.3.4 entry. The pinned pnpm 10.28.2 package exists locally; direct project binaries are used for local parity, while CI uses `pnpm/action-setup` with the repository-pinned 10.28.2 version.

## TDD evidence

- The expanded `node site/tests/site.test.mjs` source contract failed before implementation with `portfolio does not limit governed showcase surfaces to generated white-foreground treatments`.
- The first rendered run intentionally exposed the old presentation contract: muted descriptions, opacity-only hidden actions, 18-rem cards, hover translation, the light I Heart PR Tours surface, and detailed notice aggregation all failed the new assertions.
- A stale Turbopack CSS cache was diagnosed by comparing the new exported markup with the linked old stylesheet. Only ignored `site/.next/` and `site/out/` build products were removed, after which a clean export contained the new source CSS.

## Focused verification

- `node site/tests/site.test.mjs`: PASS after implementation. Source assertions cover dark-surface eligibility, explicit white text roles, visibility-hidden actions, card-first keyboard entry, dual focus treatment, reserved lower clearance, reduced motion, boolean notice applicability, exact generic copy, and absence of detailed notice aggregation.
- `site/node_modules/.bin/tsc.CMD --noEmit`: PASS.
- `site/node_modules/.bin/next.CMD build`: PASS, with 81 static pages generated.
- `node site/scripts/verify-site.mjs`: PASS, `verified 76 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations`.
- Rendered checks confirmed exact white portfolio titles, descriptions, and action labels; governed dark surfaces only; the I Heart PR Tours dark fallback and unchanged colored-heart icon; non-focusable hidden actions; card-first keyboard reveal; exact action destinations; Escape dismissal; at least 16 CSS pixels of lower clearance; declared 44-pixel targets within the established half-pixel rendering tolerance; unchanged layout geometry; reduced-motion behavior; narrow desktop behavior; native mobile disclosures; and 200 percent zoom.
- The production registry contains two applicable third-party entries. The homepage rendered two correctly associated markers and exactly one paragraph reading `* Third-party projects are independently owned and operated.`. Source assertions cover the zero-applicability branch and prevent count-dependent aggregation; route verification confirmed detailed vendor-boundary metadata remains unchanged.
- The generated homepage review image is `site/test-results/visual/home-dark-1280.png`; it shows all eight cards in the shared dark family with white copy and the single concise notice.

## Full CI-parity verification

- `.venv/Scripts/python.exe -m compileall -q scripts skill/templates`: PASS.
- `.venv/Scripts/python.exe scripts/build_all.py --list`: PASS, eight production brands discovered.
- Python contract suites: PASS, including 17 publication-workflow tests (one Windows privilege-dependent symlink case skipped), 5 package-release tests, 15 release-contract tests, 30 site-preparation tests, 4 identity-audit tests, 53 brand-contract tests, 22 identity-continuity tests, 17 icon-kit tests, and 34 glyph checks with zero failures.
- `.venv/Scripts/python.exe skill/templates/test_pipeline.py` with the approved proof root and official temporary Node 24.11.0 runtime: PASS, 63 tests. The first local attempt correctly rejected system Node 24.11.1 because the approved renderer and CI are pinned to 24.11.0; rerunning with the exact pinned runtime passed without source or proof changes.
- `.venv/Scripts/python.exe skill/templates/probe.py`: PASS, full tier with Chromium, Playwright, Pillow, pikepdf, and the bundled Node renderer available; ImageMagick remained optional and absent.
- `.venv/Scripts/python.exe scripts/build_all.py` with the approved proof root and exact Node runtime: PASS, `Built 8 kit(s) with zero reported problems.` Every kit reported zero verification problems, zero image-QC problems, zero PDF-QC problems, and zero pagination splits.
- Release certification: PASS. Version `1.2.1` produced the expected archives and notes, then `release_contract.py verify` confirmed nine release assets.
- `.venv/Scripts/python.exe skill/templates/sync_agents_md.py skill`: PASS, `skill/AGENTS.md` unchanged and `git diff --exit-code -- skill/AGENTS.md` clean.
- Site equivalents for the repository-pinned `lint`, `build`, and `test` scripts all passed: content preparation, Fumadocs MDX generation, TypeScript, Next static export, Node unit tests, source contracts, and the 76-route Playwright/axe verifier. The machine's global Corepack shim points to a missing pnpm 12.3.4 cache entry, so direct project binaries were used; CI installs the repository-pinned pnpm 10.28.2.
- `.venv/Scripts/python.exe scripts/audit_publication_artifacts.py --kits dist --site site/out`: PASS, `{"kit_markers": 8, "site_markers": 8}`.
- Post-implementation cross-artifact analysis found no critical, high, or medium consistency issue across the specification, plan, tasks, data model, contract, quickstart, and implementation. The Escape edge case was reconciled so incidental pointer movement cannot reopen actions while focus remains on the card.

## Repository hygiene

- Generated kits, static exports, generated registries, release artifacts, dependency trees, test results, caches, and machine-local Spec Kit state remain ignored and unstaged.
- `git diff --check`: PASS. Markdown policy, UTF-8 BOM/CR scans, and mojibake scans passed with no findings.
- The intended commit set is limited to `CHANGELOG.md`, four site source/test files, and the S033 Spec Kit directory. No generated `dist/`, `site/out/`, PDF, archive, registry, release, dependency, cache, or test-result path is included.
- The requirements checklist remains 16 of 16 complete. The 22-item UX/accessibility checklist remains reviewer-owned and intentionally unmodified, as required by the checklist workflow.
