# Implementation Plan: Portfolio Card Consistency

**Branch**: `codex/033-portfolio-card-consistency` | **Date**: 2026-09-13 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/033-portfolio-card-consistency/spec.md`

## Summary

Resolve #199 and #200 as one homepage portfolio slice. Keep approved governed dark showcase surfaces, but prevent light brand surfaces from entering the homepage by falling back to the existing accent-derived dark card treatment whenever the generated legal foreground is not white. Make all visible card copy and actions white, give the action layer enough fixed space and safe hidden-state semantics, preserve pointer, keyboard, Escape, reduced-motion, and mobile disclosure behavior, and replace the vendor-boundary aggregation with one exact generic notice controlled only by third-party applicability. Extend source and Playwright coverage for visual consistency, computed contrast, focusability, spacing, geometry, zoom, reduced motion, notice cardinality, and detailed-metadata preservation.

## Technical Context

**Language/Version**: Node.js 20 minimum; TypeScript, React 19, CSS, JavaScript, JSON, and Markdown

**Primary Dependencies**: Next.js 16 App Router with static export, generated brand registry, Playwright 1.62.1, and axe-core

**Storage**: Site source under `site/`, generated registry inputs and static output under ignored paths, and Spec Kit artifacts under `specs/033-portfolio-card-consistency/`

**Testing**: Source-level Node assertions, TypeScript type-check, Next.js static export, Playwright rendered layout and interaction checks, axe-core WCAG 2.1 AA audit, Python publication suites, all-kit generation, and release-contract verification

**Target Platform**: Statically exported public homepage across desktop and mobile widths, 200 percent zoom, pointer and keyboard input, and reduced-motion preferences

**Project Type**: Statically exported brand-registry and documentation web application

**Performance Goals**: Preserve the existing 81-page static export and 76-route browser-verification envelope; add only bounded homepage measurements and no network or runtime dependency

**Constraints**: WCAG 2.1 AA without waiver; 4.5:1 action text contrast; 3:1 focus-indicator contrast; 44-by-44 CSS pixel targets; at least 16 CSS pixels lower clearance; no hidden focus targets; no geometry delta above 0.5 CSS pixels; no identity-source or brand-route surface changes; generated output remains ignored; UTF-8 without BOM and LF

**Scale/Scope**: Two GitHub issues, eight current production portfolio entries, one shared React component, one shared stylesheet, source tests, targeted homepage browser checks, zero/one/multiple third-party states, and the full publication pipeline

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan evidence | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Commit only site source, tests, changelog, and Spec Kit artifacts. Keep `dist/`, `site/out/`, PDFs, archives, and registries ignored. | PASS |
| P2. Identity geometry is preserved | Keep all brand records, logos, paths, colors, proportions, and source bytes unchanged. Apply only a homepage presentation rule. | PASS |
| P3. Accessibility has no exemption | Require white visible copy, measured action contrast, visible focus, hidden-focus safety, 44-pixel targets, keyboard/Escape operation, zoom, reduced motion, and the complete WCAG sweep. | PASS |
| P4. Verification precedes publication | Add failing source and rendered regressions before implementation, then run the full CI-parity repository and site gates. | PASS |
| P5. The site consumes generated kits | Continue consuming generated registry content and detailed vendor metadata. The generic homepage notice is site-owned summary copy and does not restate brand-specific identity values. | PASS |
| P6. Specifications and releases move together | S033 specification, design, tasks, implementation, evidence, PR traceability, and issue closure move together. No release is cut. | PASS |

### Post-Design Re-check

The design changes only the site-owned homepage presentation and its verification. It preserves generated content bindings, brand-specific guideline surfaces, detailed vendor metadata, identity assets, and every constitution gate. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/033-portfolio-card-consistency/
├── checklists/
│   ├── requirements.md
│   └── ux-accessibility.md
├── contracts/
│   └── portfolio-presentation-contract.md
├── data-model.md
├── evidence.md
├── plan.md
├── quickstart.md
├── research.md
├── spec.md
└── tasks.md
```

### Source Code (repository root)

```text
site/
├── app/globals.css                 # dark card family, white copy, spacing, actions, focus, reduced motion
├── components/brand-portfolio.tsx # surface eligibility, hidden-action state, and generic notice
├── scripts/verify-site.mjs         # computed style, geometry, focus, zoom, notice, and metadata checks
└── tests/site.test.mjs             # source contracts and negative regression assertions

CHANGELOG.md                         # unreleased S033 correction
```

**Structure Decision**: Keep the change inside the existing site-owned portfolio component, global styles, and test harness. Do not alter brand JSON, generated registries, guideline routes, or dependency components. A local surface-eligibility helper may use the generated legal foreground to retain approved dark surfaces while routing light surfaces to the shared dark fallback.

## Delivery Sequence

1. Capture current failures for mixed copy colors, I Heart PR Tours light-surface leakage, action-layer height, hidden focus semantics, and repeated detailed notice copy.
2. Add source-level assertions for dark-surface eligibility, exact generic copy, one-paragraph conditional notice behavior, explicit action destinations, and the absence of per-brand notice aggregation.
3. Add browser assertions for all visible text colors, dark surface family, action contrast and focus, hidden-state visibility/focusability, 44-pixel targets, bottom spacing, zero layout shift, Escape dismissal, mobile disclosures, 200 percent zoom, and reduced motion.
4. Implement homepage surface eligibility and exact generic notice semantics in `brand-portfolio.tsx`.
5. Implement the shared dark-card typography, bounded action stage, hidden/revealed semantics, white action treatments, focus indicator, responsive padding, and reduced-motion behavior in `globals.css`.
6. Run focused source and browser verification, then the full Python compatibility, all-kit, release, site lint/build/test, publication, Markdown, and hygiene gates.
7. Record measured evidence, commit locally with an S033 conventional subject, and halt before push.

## Decision Log

### 2026-09-13 - Preserve governed dark surfaces only

Use a generated white legal foreground as the eligibility signal for retaining a brand's governed homepage surface. If the generated foreground is not white, the homepage uses the existing accent-derived dark fallback. This preserves approved dark surfaces for Cueson, ESO Weave, and Glitchpad while preventing the white I Heart PR Tours guideline surface from breaking the dark portfolio system.

### 2026-09-13 - Make the card itself the keyboard reveal entry

Keep pointer hover as the pointer reveal path, make the card a labeled keyboard focus stop, and hide action anchors with both visibility and pointer semantics until the card is hovered or focused. This ensures no hidden action is focusable while allowing a keyboard user to reveal actions before tabbing into them. Escape returns focus to the card and dismisses the action layer.

### 2026-09-13 - Keep homepage disclosure generic

Drive notice presence from whether any entry has a vendor boundary, but render one fixed sentence rather than collecting boundary strings. Detailed generated wording remains on brand routes and metadata, while adding brands cannot lengthen the homepage notice.

### 2026-09-13 - Checklist sequencing follows installed prerequisites

The installed checklist prerequisite requires `plan.md`, so the UX/accessibility requirements checklist is generated immediately after planning and before task generation. This is the earliest executable point and preserves the checklist's role as a requirements-quality gate.

## Complexity Tracking

No constitution violation requires justification. Bundling the issues is proportional because both defects share the same component, styles, ownership boundary, source tests, homepage browser checks, and publication gate.
