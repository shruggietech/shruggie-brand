# S050 Verification Evidence

## Session 1: Contract and baseline

- Issue #193 remains the authoritative scope. The source declaration is optional `guide.surface_mode`, with `dark` as the compatibility default and a validated `light` path.
- Fail-first coverage was added for invalid modes, incomplete or low-contrast light palettes, selected portal presentation, and the PDF ground gate. The built-in Spec Kit requirements checklist passed 16 of 16 items before implementation.
- The approved I Heart PR Tours identity, Glitchpad dark guide, existing per-asset well declarations, and site route boundaries were inspected before generator and hosted changes. No logo geometry was edited.

## Session 2: Implementation and representative proof

- The generator now resolves one declared guide mode early, emits the selected presentation plus both complete semantic palettes, uses the mode for PDF and portable guide output, and passes it to PDF QC. Site preparation projects the selected guide and showcase modes from generated output.
- Hosted brand routes use local semantic/Fumadocs token scopes independent of the host theme. Portfolio cards and native mobile disclosures honor a governed light showcase surface, including accessible action and focus colors. The existing dark fallback remains unchanged.
- The initial representative build exposed a local Node 26.5.0 versus approved Node 24.11.0 identity-proof mismatch. Rerunning with the installed pinned Node 24.11.0 (`GP_NODE`) passed. This is a local toolchain selection, not a source exception or skipped gate.
- The I Heart PR Tours PDF contact sheet, portable guide 390px sheet, and logo sheet were opened and inspected. The light outer ground and source-preserved artwork are coherent. The Glitchpad dark PDF contact sheet was also inspected for regression.

## Session 3: Full validation

- `scripts/build_all.py` with the pinned Node executable built all eight kits with zero reported problems. Each kit passed generator verification, glyph, image, PDF ground/contrast, and pagination gates. The light guide used `--expect-ground light`; default-dark guides used `--expect-ground dark`.
- Python gates passed: glyphkit 34 checks, interface contract 19 tests, documentation contract 4 tests, component contract 5 tests, web React adapter 5 tests, brand contract 58 tests, full pipeline 72 tests, and site preparation 37 tests. `scripts/check_markdown.py` passed and `probe.py` reported the full tier.
- The site production build, TypeScript lint, static site contract, and the 12 payload/origin tests passed using the repository-pinned pnpm 10.28.2 through installed Node 24.11.0. The Codex fallback `pnpm` shim attempted a non-interactive dependency purge, so the equivalent pinned Corepack entry point was used directly. No dependency files or generated site exports were committed.
- The first browser pass found an inherited host-theme color on `.vendor-boundary` (3.54:1 on the ESO Weave dark surface and 2.81:1 on I Heart PR Tours white). It also found that the test compared host `body` text color instead of the brand-owned guide scope. The notice now uses the generated local `muted-foreground`, and the invariance assertion samples the guide container. This corrects a real contrast defect and a test measurement defect without changing the host theme.
- The final `pnpm --dir site test` passed its 12 payload/origin tests and verified 90 exported HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The browser matrix covered host light/dark themes, 360px and 390px widths, desktop, 200 percent zoom, no-script navigation, reduced motion, print presentation, white-well assets, portfolio keyboard actions, and portable CTA states. Rendered portfolio screenshots in both host themes and I Heart PR Tours guideline screenshots at desktop and 390px were opened and inspected.
- `git diff --check` passed. All 31 changed or new source files passed strict UTF-8 decoding, no BOM, LF-only line endings, and a mojibake scan. Git status lists source, tests, documentation, and `specs/050-light-brand-systems/` only; generated `dist/` kits, site output, and `.specify/feature.json` remain outside the commit.
