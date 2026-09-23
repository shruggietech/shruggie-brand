# Verification Evidence: Published Documentation and Guideline Integrity

**Branch**: `codex/047-published-docs-integrity`

## Baseline and intake (2026-09-22)

- Started from clean `main` at merge commit `801ed912aaa8bbc66c12d8a97b5487fcddb0d9da`, matching `origin/main`, then created the S047 branch.
- Issues #236, #237, and #202 were open at intake. No pull request was open.
- `.specify/` and the hyphenated Spec Kit skills are installed; constitution 2.0.0 applies. The built-in specification-quality checklist passed 15/15 items. No custom reviewer-owned checklist is required for unattended execution.
- The full CI gate is `.github/workflows/build.yml`; `CONTRIBUTING.md` also documents focused Python, probe, all-kit, and site checks.

## Publication inventory

- `skill/references/documentation-contract.json` declares fifteen public manual pages. `scripts/prepare_site.py` transforms their governed Markdown into generated MDX for `/docs`.
- `skill/templates/gen_guidelines.py` produces portable guide HTML and related portal facts; `scripts/prepare_site.py` copies the generated portable file to the site.
- `scripts/build_all.py` copies each production brand's source guidance into its generated kit; `scripts/package_release.py` archives the verified kit. Reader-facing README and NOTES files are therefore publication inputs.
- The existing publication audit checks structural safety, but no current gate rejects work-slice codes or stale prose in public guidance.
- The I Heart PR Tours preview defect originates in generator well selection and dark-well foreground styling. The documentation pagination defect originates at the site's Fumadocs footer transition and smooth-scroll behavior.

## Cross-artifact analysis

- Thirteen functional requirements and five measurable success criteria map to twenty-five tasks across three independently testable stories.
- Initial analysis found two task-order/version gaps: version assertions needed to precede metadata changes, and changed delivered brand guidance needed brand patch versions. Both were resolved in `tasks.md` and `plan.md` before implementation. No critical constitutional conflict remains.

## Focused red baseline

- The 2.0.2 release-contract assertions failed before metadata changes because no 2.0.2 changelog section existed. The failure is expected and proves the version contract test precedes implementation.
- The new public-guidance tests initially failed because the audit module did not exist. Source audit then found 19 publication-language violations across the manual and delivered brand guidance.
- The new named-Canon transformation test failed with `Brand Brand system` and `Interface Brand system` before the transformation correction.

## Source guidance correction

- Rewrote manual instructions in interview, logo, voice, toolchain, glyph construction, portability, and operating modes. Active compatibility names and production safety rules remain.
- Rewrote delivered Cueson and ESO Weave guidance to state current approvals, source handling, and consumer installation without internal planning history. Removed a stale claim that ESO Weave Gate 1 was pending; `brand.json` records both gates approved. Corrected the Fragcap voice rule's vague wording.
- Patched Cueson and ESO Weave from 1.0.0 to 1.0.1 and Fragcap from 1.1.0 to 1.1.1 because their delivered guidance changed. No logo source, path, or asset bytes were edited.
- `scripts/audit_public_documentation.py --sources`: 0 problems across the governed manual and all discovered production-brand reader guidance. Six focused audit tests, 37 site-preparation tests, and 27 release-contract tests pass.

## Generator and navigation correction

- The portable generator now samples visible PNG colors or declared SVG paint and chooses the higher-contrast light or dark preview well; transparent regions do not decide the well. The embedded asset bytes are unchanged. Both well classes declare local foreground colors; ICO, ICNS, JSON, and XML deliveries receive explicit nonvisual labels.
- A focused fixture covers black, white, transparent white, full-color, SVG, and nonvisual formats. The full generator pipeline passed 69 tests with the exact approved Node 24.11.0 renderer and 32 exported I Heart PR Tours proof images.
- Pagination retains native links and records only unmodified fragment-free footer activation. On the resulting route it focuses the destination heading and places it at the top. Direct loads, fragments, and browser history are covered by rendered regression cases. TypeScript compilation passes.
- The local Codex `pnpm` fallback rejected three same-day locked dependencies under its minimum-release-age check. Direct invocation of the repository-pinned pnpm 10.28.2 installed the existing frozen lockfile without changing it. This does not alter the repository CI policy; the CI site gate remains required.
- Focused publication-workflow, release-package, release-contract, site preparation, documentation-contract, component-contract, brand-contract, interface-contract, web React, native egui, conformance, identity-continuity, glyph, and icon tests pass. `git diff --check` and Markdown prose policy pass.

## Prepared-output audit and candidate regeneration

- The first all-kit build completed eight kits with zero verifier problems and zero glyph failures. The 2.0.2 archives and release notes certified, and the site lint and static export passed.
- The first prepared-output prose audit found six generated `VERIFY.md` reports still saying Type3 glyph fonts were "usually a renderer fallback." That report is generated by `skill/templates/verify.py`, so the template wording was made precise and the complete candidate is being regenerated. No generated report was patched directly.
- During regeneration, a new responsive preview `100%` rule exposed the portable template's percent-string interpolation. It was corrected to `100%%` in generator source; the focused guide-generation regression passes. The partial failed build was discarded, and a fresh all-eight-kit build was started from the corrected source.
- The final build completed all eight kits with zero verifier problems and zero glyph failures. The 2.0.2 candidate produced nine certified release assets and validated notes. Site lint, static export of 95 pages, `scripts/audit_public_documentation.py --prepared` (0 problems), and `scripts/audit_publication_artifacts.py` (8 kit markers, 8 site markers) pass. No prose-audit exceptions were needed.
- A read-only scan of all 44 changed text files found UTF-8 without BOM, LF line endings, and no mojibake markers. `git diff --check` passes; `git status` shows no changed identity source assets, provenance files, or shared fonts. Generated kits, site exports, and release archives remain ignored and uncommitted.
- The final generator pipeline rerun passed all 69 tests against the corrected template and exact approved renderer. Other local Python contract suites, including the native egui adapter and publication workflow, passed earlier in this candidate; the Python 3.8 compilation job remains a CI-only check on this host, which has Python 3.12 installed.

## Rendered inspection and final cross-artifact analysis

- The first final-export browser pass reached the I Heart PR Tours portable card matrix without any preview, label, zoom, or card-clipping finding. Desktop and 390px screenshots were inspected: XML cards are visibly labeled, and the heart icon remains distinct on its well. The dark well's declared text pair measures 18.26:1; the light well's pair measures 17.32:1. Both exceed the 4.5:1 AA text floor. Source-preserved icon files and all approved logo bytes remain unchanged.
- Pagination arrival and heading focus passed pointer and keyboard cases at desktop and mobile widths, with and without reduced motion. The first browser pass did find a test timing race in Forward history: Playwright's Back navigation returned before the client route committed, causing an immediate Forward to observe stale source state. A dedicated isolated browser reproduction proved the route works once the source heading has committed. The regression now waits for that commit before testing Forward, and the full rendered pass is being rerun.
- Cross-artifact analysis after implementation found no unmapped requirement or contradictory acceptance rule. FR-001 through FR-004 map to authoritative prose, transformation tests, and both publication audits; FR-005 through FR-008 map to generator surface/fallback tests and rendered cards; FR-009 through FR-011 map to the scoped focus helper and browser transitions; FR-012 and FR-013 map to source-only diffs, identity preservation, and the full build/CI gates. The verifier-template wording correction is a publication-bound generator change within US1, not a new subsystem or scope expansion.
- The completed browser rerun verified 90 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. Pagination arrival, focus, fragments, reduced motion, Back/Forward, and portable card cases all pass. The source-heading commit wait fixed only the regression harness timing, not the product history stack.

## PR and CI (2026-09-22)

- Commit `3d6e1dd` (`fix(S047): restore published docs and guideline integrity`) was pushed to `codex/047-published-docs-integrity`. [PR #252](https://github.com/shruggietech/shruggie-brand/pull/252) closes #236, #237, and #202. No release tag or published archive was created.
- The CI approved-identity-proofs and Python 3.8 compatibility jobs passed. The full verified-build job and the first automatic Codex/security review remain pending at this evidence update.

## First Codex review response (2026-09-22)

- The first automatic Codex review completed with three inline findings. The P1 evidence finding is resolved by the full rendered rerun (90 routes, zero WCAG 2.1 AA violations) and checked T018. The test harness waits for the source heading to commit before checking Forward history, matching the proved client transition.
- The first P2 finding identified that the prose audit rejected every mention of the required Spec Kit workflow. Author-mode guidance now gives one exact reader-required instruction; only that sentence in its authoritative source and two prepared publication paths is excepted. Seven focused audit tests reject the same instruction on another page and reject any extra planning reference on the allowed page.
- The second P2 finding identified a false release-impact claim that brand versions were unchanged. The identity summary now distinguishes unchanged logo/source/affiliation from Cueson 1.0.1, ESO Weave 1.0.1, and Fragcap 1.1.1 package-version advances. The interface-contract test asserts all three versions and rejects the old wording.
- After these changes, the source and prepared-output prose audits each report zero problems, all eight kits rebuild with zero verifier/glyph failures, nine 2.0.2 release assets certify, site lint/build pass, and the publication audit reports eight kit plus eight site markers. The final commit CI and second review remain pending.
