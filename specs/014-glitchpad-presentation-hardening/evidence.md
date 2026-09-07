# Evidence: S014 Glitchpad Pre-release Presentation Hardening

## Baseline

- Branch: `codex/014-glitchpad-presentation-hardening`
- Issues: #144 and #145
- Base revision: `b8de9680973461c0916dd10a50533bcbac4ada22`
- Protected Glitchpad `logo.paths` SHA-256: `b7fb71af8414d2af4926fba85d661ec71eefb4eb86b7fa1b33bc3acf0f247373`
- Worktree state: clean before S014 artifacts were created; local `main` and `origin/main` had divergence `0 / 0`.
- Ignore boundary: `dist/`, `release/`, `site/out/`, generated site trees, browser results, caches, local dependencies, and machine-local Spec Kit state are excluded.

## Initial disposition inventory

| Surface or asset family | Baseline | Intended disposition |
| --- | --- | --- |
| Landing portfolio icon | Portrait image box expands below the intended square content area | Correct layout and verify all five cards |
| Landing Glitchpad card | Accent-derived yellow wash and glow | Correct through governed charcoal binding |
| Glitchpad portfolio hero | Accent-derived yellow wash | Correct through governed charcoal binding |
| Standalone square PNG masters | Height-only composition can crop future landscape sources and does not center asymmetric visible bounds | Correct through shared visible containment |
| Web and legacy icon suites | Existing shared visible-containment logic | Verify unchanged behavior |
| Android adaptive and monochrome layers | Existing 66/108 safe-area composition | Verify unchanged behavior |
| Android Play artwork | Existing 0.75 plated composition | Verify unchanged behavior |
| Apple and Windows suites | Existing role-specific shared composition | Verify unchanged behavior |

The source inventory confirms `brands/glitchpad/brand.json` declares charcoal `base`, `card`, `secondary`, and `hover` surfaces, while the site currently creates large backgrounds by mixing the bright accent. Generated application icons already default to the neutral base surface. S014 therefore changes only the demonstrated faulty presentations and the standalone containment path, then records native outputs as unchanged when their measurements pass.

## Implementation evidence

- Added optional `showcase_surface` role validation. Glitchpad selects `card`, resolving to `#121416`; generated site metadata emits `showcaseSurface` only for Glitchpad.
- Added one shared visible-alpha containment primitive. Synthetic portrait, landscape, and asymmetric-canvas inputs center to opposite margins within one pixel, while empty and invalid inputs fail explicitly.
- Standalone 1024px Glitchpad mark masters now derive occupancy from the 900-unit artwork long edge plus two 70-unit clear spaces. The color master visible bounds are `(158, 69, 866, 955)`, producing exactly 158px horizontal and 69px vertical opposite margins.
- The 68 CSS-pixel portfolio slot now retains a square wrapper and square image box at desktop, mobile, and 200 percent zoom. All five production brand cards remain contained and balanced.
- Glitchpad's landing card and portfolio hero compute to `rgb(18, 20, 22)` with no background image; the landing icon has no accent shadow. Other brand cards retain their prior accent-derived fallback.
- Dark and light screenshots at 360px and 1280px were inspected for the landing portfolio and Glitchpad hero. The charcoal well remains visually quiet and bounded, text remains readable, and no sibling treatment changed unexpectedly.

## Generated Glitchpad export inventory

All five manifest suites report `generated`; the aggregate icon manifest records 120 artifacts.

| Asset family | Representative measurement | Disposition |
| --- | --- | --- |
| Full and reduced SVG masters | Canonical `logo.paths` hash remains `b7fb71af8414d2af4926fba85d661ec71eefb4eb86b7fa1b33bc3acf0f247373` | Verified unchanged |
| Standalone PNG masters | 1024px color visible bounds `(158, 69, 866, 955)` | Corrected |
| Web PNG and ICO suite | 192px content bounds `(41, 27, 151, 165)` on `#0B0C0D`; complete ICO gate passed | Verified unchanged |
| Android legacy | 192px content bounds `(41, 27, 151, 165)` on `#0B0C0D` | Verified unchanged |
| Android adaptive and monochrome | 432px visible bounds `(110, 84, 321, 348)`, with separate transparent layers | Verified unchanged |
| Android Play | 512px content bounds `(102, 64, 409, 448)` on `#0B0C0D` | Verified unchanged |
| iOS and macOS | 1024px content bounds `(217, 143, 806, 880)` on `#0B0C0D` | Verified unchanged |
| Windows plated and unplated | 256px content or visible bounds `(54, 36, 201, 220)` | Verified unchanged |

Desktop and Android release preparation should consume assets rebuilt from the S014 source revision. Platform-specific safe areas and plates remain authoritative; consumers must not substitute the website slot's padding.

## Verification evidence

- Focused brand-contract tests: 20 passed.
- Focused site-preparation tests: 20 passed.
- Focused icon tests: 13 passed.
- Focused pipeline tests: 25 passed.
- Five-kit production build: 5 built, zero reported problems; every kit reported zero `verify.py` problems and zero glyph failures.
- Static type check: passed.
- Static export through the Windows webpack fallback: 26 routes generated.
- Browser contract: 26 routes at desktop and mobile widths, zero WCAG 2.1 AA violations.
- Visual inspection: Glitchpad logo sheet, guideline page sheet, product specimen, landing route, and Glitchpad portfolio route reviewed.
- Local environment deviation: the direct Windows Turbopack build failed twice while spawning its pooled Node child process with operating-system error 5 (`Access is denied`). The referenced generated file existed, the same source passed TypeScript and webpack static export locally, and normal Turbopack remains required in Linux CI.
- Release contract: exactly seven v1.2.1 candidate assets and generated notes verified.
- Generated agent contract: `skill/AGENTS.md` remained unchanged at 15,018 bytes with body SHA `4f2c84a64095`.
- Encoding and hygiene: 28 changed text files passed strict UTF-8 without BOM and LF checks; `git diff --check`, mojibake scan, and ignored-artifact review passed.
- Python 3.8 is not installed on the Windows host. Minimum-version execution remains a required hosted CI gate.

## Pull request and review ledger

- Implementation commit: `cd8b16b` (`fix(S014): harden Glitchpad presentation and icon containment`).
- Pull request: [#150](https://github.com/shruggietech/shruggie-brand/pull/150)
- First review round: pending.
- Authorized second review round: not triggered.
