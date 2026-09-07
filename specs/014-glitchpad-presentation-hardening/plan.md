# Implementation Plan: Glitchpad Pre-release Presentation Hardening

**Branch**: `codex/014-glitchpad-presentation-hardening` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/014-glitchpad-presentation-hardening/spec.md`

## Summary

Resolve #144 and #145 together by making visible-ink containment the shared rule for square raster composition, binding an optional showcase-surface role from a brand source into generated site data, and using that contract to present Glitchpad on calm charcoal surfaces without changing identity colors, canonical paths, sibling brands, or platform-specific icon policies.

## Technical Context

**Language/Version**: Python 3.8 minimum, TypeScript and CSS on Node.js 20 minimum, JSON, and Markdown

**Primary Dependencies**: Python standard library, Pillow, existing SVG raster capability chain, Next.js App Router, Playwright, and axe-core

**Storage**: Committed brand and generator sources plus ignored `dist/`, generated site bindings, static exports, screenshots, and temporary synthetic inputs

**Testing**: Python `unittest`, visible-alpha bounds measurements, five-kit build, `verify.py`, `validate_glyph.py`, TypeScript checks, static export, Playwright browser measurements, WCAG audit, Markdown policy, and repository hygiene

**Target Platform**: Static brand site plus generated web, Windows, macOS, iOS, and Android identity assets

**Project Type**: Source-driven brand generator, portable skill, and statically exported documentation and portfolio site

**Performance Goals**: Preserve the existing static rendering model and add no runtime data request or client-side presentation dependency

**Constraints**: UTF-8 without BOM, LF, generated artifacts excluded from Git, canonical paths unchanged, WCAG 2.1 AA, Python 3.8 compatibility, role-specific platform padding, hidden non-interactive child processes

**Scale/Scope**: Two P0 issues, five production brands, one Glitchpad-specific showcase role selection, all declared Glitchpad square export roles, and two public site routes at three viewport and zoom conditions

## Constitution Check

| Principle | Design response | Gate |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only source, tests, Spec Kit records, and changelog entries; create synthetic raster cases in temporary directories. | PASS |
| P2. Identity geometry is preserved | Treat visible-bounds work as a presentation transform and assert canonical Glitchpad path bytes remain unchanged. | PASS |
| P3. Accessibility has no exemption | Measure corrected dark and light text and focus surfaces with the complete browser accessibility gate. | PASS |
| P4. Verification precedes publication | Rebuild and verify all five production kits and every declared Glitchpad icon suite before push. | PASS |
| P5. The site consumes generated kits | Resolve the showcase surface from committed brand data during site preparation and consume only the generated binding in site components. | PASS |
| P6. Specifications and releases move together | S014 synchronizes requirements, design, tasks, evidence, changelog, issues, pull request, CI, and review records. | PASS |

Post-design re-check: PASS. No constitutional exception or identity change is introduced.

## Technical Approach

1. Add regression tests for visible-bound containment using portrait, landscape, and asymmetric transparent canvases, plus generated-site surface-role validation and browser measurements.
2. Promote the existing visible-alpha crop and uniform contain behavior into a reusable icon composition function. Use it for standalone square PNG masters while retaining each platform's established occupancy ratio.
3. Add an optional `showcase_surface` role reference to the brand contract. Resolve it against the brand's `surfaces` mapping, derive the higher-contrast black or white foreground, and emit both values only when explicitly configured.
4. Set Glitchpad's role reference to `card`, pass the resolved value through generated site metadata, and apply it to the landing card and portfolio hero through one optional CSS custom property. Preserve the existing fallback treatment for all other brands.
5. Constrain the landing icon's grid item and image content box so intrinsic portrait dimensions cannot expand its square track. Remove the optional showcase shadow only where an explicit neutral showcase surface is present.
6. Inventory the rebuilt Glitchpad master and platform outputs using measured visible bounds, dimensions, transparency, backgrounds, and manifest roles. Record already-correct outputs without rewriting them.
7. Run focused and complete validation, publish the pull request with `Fixes #144` and `Fixes #145`, process no more than two Codex review rounds, and stop before merge.

## Architecture Decisions

- Represent a showcase surface as a role name that resolves through the brand's existing `surfaces` object. This avoids a duplicate color literal and lets other brands opt in without changing their current presentation.
- Derive the showcase foreground during site preparation by comparing WCAG contrast for black and white against the resolved surface. This supports valid light and dark governed surfaces without site-owned color assumptions.
- Keep the absence of `showcase_surface` meaningful. The generated record omits the optional override and site CSS retains the existing accent treatment, which prevents an incidental sibling-brand redesign.
- Center visible ink for standalone square raster masters through the shared containment primitive. Do not modify SVG canvas geometry or path strings to compensate for presentation behavior.
- Preserve platform occupancy values of 0.72, 66/108, and 0.75. A website content-box correction and a standalone master clear-space ratio do not replace platform-specific safe areas.
- Derive standalone master occupancy from the declared artwork long edge and clear space: `long_edge / (long_edge + 2 * clear_space)`. This provides declared breathing room on the limiting dimension and naturally leaves more space on the shorter dimension.
- Treat #146 as explicitly out of scope. S014 preserves all current neutral, accent, wordmark, light, and monochrome identity colors.
- Leave the custom visual-identity checklist reviewer-owned and unchecked. The operator's autopilot authorization permits implementation to proceed after the built-in specification checklist passes.

## Project Structure

### Documentation for S014

```text
specs/014-glitchpad-presentation-hardening/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── square-containment.md
│   └── showcase-surface.md
├── checklists/
│   ├── requirements.md
│   └── visual-identity.md
└── tasks.md
```

### Repository surfaces changed or verified

```text
CHANGELOG.md
brands/glitchpad/brand.json
scripts/prepare_site.py
scripts/test_prepare_site.py
site/app/(site)/page.tsx
site/app/(site)/[slug]/page.tsx
site/app/globals.css
site/scripts/verify-site.mjs
skill/references/canon.schema.json
skill/templates/brand_contract.py
skill/templates/gen_logo.py
skill/templates/iconkit.py
skill/templates/test_brand_contract.py
skill/templates/test_iconkit.py
skill/templates/test_pipeline.py
specs/014-glitchpad-presentation-hardening/
```

**Structure Decision**: Extend the existing brand contract, preparation pipeline, composition helper, and browser verifier. Do not add a second metadata file, presentation service, or committed artifact tree.

## Complexity Tracking

No constitutional violation or unjustified complexity is introduced. The optional surface-role reference is a proportional general contract used by one brand in this slice, while the absent state preserves every sibling's current rendering.
