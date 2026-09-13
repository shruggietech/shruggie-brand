# Implementation Plan: CTA Role Consistency

**Branch**: `codex/032-cta-role-consistency` | **Date**: 2026-09-13 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/032-cta-role-consistency/spec.md`

## Summary

Project the existing independent-brand `semantic_colors.action` value into explicit CTA fill, filled-control foreground, and surface-aware outline-foreground tokens. Consume that contract in every portable-guidelines primary and secondary button, with the secondary control matching the live-site red-outline role, and document the same roles in the generated PDF palette and semantic guidance. Normalize reader-facing guide copy to American English without renaming established internal schema keys or compatibility APIs. Extend generator, browser, contrast, text-extraction, and PDF-layout regressions so the HTML and PDF cannot drift.

## Technical Context

**Language/Version**: Python 3.8 minimum for generator code; Node.js 20 minimum for the site; CI uses Python 3.8 and 3.12 plus Node.js 24.11.0
**Primary Dependencies**: coloraide, Pillow, fontTools, svgelements, Playwright Chromium, Next.js static export
**Storage**: Source JSON and generator templates under `brands/` and `skill/templates/`; generated artifacts remain ignored under `dist/` and `site/out/`
**Testing**: Python `unittest` suites, generator verification, glyph validation, Markdown audit, Next.js lint/build, Node contract tests, Playwright plus axe-core
**Target Platform**: Static HTML/PDF/kit artifacts and GitHub Pages
**Project Type**: Source-driven brand-system generator plus static publication site
**Performance Goals**: Preserve the existing eight-kit build and 76-route verification envelope without adding a network dependency or persistent browser process
**Constraints**: WCAG 2.1 AA is mandatory; source logo bytes and geometry are immutable; generated artifacts are not committed; text is UTF-8 without BOM and LF; reader-facing prose uses American English
**Scale/Scope**: One brand-specific CTA value projected through shared generator semantics, two generated guide formats, all eight production kits, and the complete site publication pipeline

## Constitution Check

### Before Design

| Principle | Gate | Result |
|-----------|------|--------|
| P1 Sources committed, artifacts rebuilt | Changes stay in `brands/`, `skill/templates/`, `site/`, tests, and `specs/`; `dist/` remains ignored | PASS |
| P2 Identity geometry preserved | No logo source, path, transformation, or approval ledger changes | PASS |
| P3 Accessibility has no exemption | CTA foreground and focus behavior are measured and fail closed below AA | PASS |
| P4 Verification precedes publication | TDD plus all production kit, glyph, PDF, site, and publication gates are required | PASS |
| P5 Site consumes generated kits | The site continues copying the verified portable guide and PDF from generated output | PASS |
| P6 Specifications and releases move together | S032 contains specification, plan, tasks, analysis, evidence, and changelog traceability | PASS |

### After Design

The design remains compliant. The new CTA foreground is derived from the governed action value by the existing legal-foreground measurement, not transcribed. The portable guide consumes generated token output, the PDF consumes the same generated token block, and verification examines the exact rebuilt artifacts. Internal `colourway` compatibility keys remain unchanged because renaming them would be an unrelated schema migration; only reader-facing prose is normalized.

## Project Structure

### Documentation for this feature

```text
specs/032-cta-role-consistency/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── cta-guide-contract.md
├── checklists/
│   └── requirements.md
├── tasks.md
└── evidence.md
```

### Source code

```text
brands/i-heart-pr-tours/
└── brand.json

skill/templates/
├── enrich_brand.py
├── gen_nextjs.py
├── gen_guidelines.py
├── gen_guide_pdf.py
├── verify.py
└── test_pipeline.py

site/
├── scripts/verify-site.mjs
└── tests/
```

**Structure Decision**: Keep the brand-approved CTA value and copy in the I Heart PR Tours source, shared token projection and guide presentation in generator templates, and computed browser checks in the existing site verifier. No generated artifact is edited or committed.

## Design

### Governed CTA token pair

`semantic_colors.action` remains the single source for the fill and outline. `gen_nextjs.py` adds `brand-cta-foreground`, selected by the existing measured `legal_fg` rule, plus `brand-cta-outline-foreground`, which uses CTA red when it clears 4.5:1 on the current surface and otherwise uses that surface's legal foreground. The dark and light token blocks expose the same CTA fill and filled-control foreground, while the outline foreground adapts to the actual surface. `verify.py` treats both generated foreground pairings as AA contracts.

### Portable-guidelines behavior

Every `.btn-primary` consumes `--brand-cta` and `--brand-cta-foreground`. Every `.btn-secondary` has a transparent default fill, `--brand-cta` border, and surface-aware `--brand-cta-outline-foreground` text, then uses the governed filled pair on hover. Hover and active states communicate through border, inset treatment, and movement rather than an unmeasured color mutation. Focus uses a dual light/dark indicator so it remains distinguishable against the control and both light and dark surrounding surfaces. Reduced-motion behavior retains the same visual state without relying on movement.

### PDF palette and semantic guidance

The palette adds a `brand-cta` swatch next to identity, emphasis, and destructive roles. The semantic table gains a CTA row with the exact value and purpose. Compact specimens document primary default, hover, active, and focus-visible treatments plus the secondary red-outline role. Copy explicitly excludes CTA red from identity text, links, focus, destructive states, and chart series.

### American-English boundary

Normalize all reader-facing strings emitted by the portable-guidelines and PDF generators, plus I Heart PR Tours source copy. Preserve established internal names such as `colourway`, `colourways`, and `rasterise` functions because they are schema or code compatibility surfaces rather than reader-facing prose.

### Test strategy

1. Add failing generator regressions for the CTA token pair, cross-brand isolation, all three portable button specimens, PDF palette/semantic/state content, artifact agreement, and reader-facing American English.
2. Implement the shared token and document changes.
3. Add computed-style browser assertions against the generated portable file for default, hover, active, focus, and both theme wells.
4. Rebuild I Heart PR Tours, render and extract the PDF, inspect every page, then run the complete repository CI-parity suite.

## Decision Log

| Decision | Rationale | Alternatives considered |
|----------|-----------|-------------------------|
| Use `semantic_colors.action` as the only CTA fill source | It already contains the owner-approved `#C5342C` and is projected as `brand-cta`; adding another source would create drift | New brand field; hardcoded template value; reuse general `primary` |
| Add measured `brand-cta-foreground` and `brand-cta-outline-foreground` tokens | Filled controls need a legal foreground on red, while outlined controls need a legal foreground on each surface; the verifier can enforce both | Hardcode white; force red text on dark; calculate independently in each guide |
| Keep hover and active fill unchanged | State remains visibly distinct without introducing unmeasured derived colors that could break generic independent brands | Fixed darker reds; runtime color mixing; per-brand state fields |
| Use a dual-tone focus indicator | A light/dark pair remains visible against CTA red and either surrounding theme surface | Existing identity ring; foreground-only outline; brand-specific focus color |
| Normalize emitted prose only | The user-visible dialect becomes consistent without breaking established schema and generator APIs | Rename internal compatibility keys; limit correction to one PDF |
| Skip a custom reviewer checklist | The issue acceptance criteria and built-in 16-item requirements checklist already cover color semantics, accessibility, copy, layout, and publication; a second unchecked reviewer-owned list would duplicate them | Add separate UX or PDF checklist |

## Complexity Tracking

No constitution violations or justified complexity exceptions.
