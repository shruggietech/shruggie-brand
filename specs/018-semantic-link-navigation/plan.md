# Implementation Plan: Semantic Link and Documentation Navigation

**Branch**: `codex/018-semantic-link-navigation` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

## Summary

Replace the inherited blanket anchor behavior with a site-owned semantic link taxonomy, then rebuild documentation pagination on the same explicit role contract. Keep generated brand guidelines isolated, preserve native anchor semantics, and prove interaction behavior across themes, widths, keyboard use, reduced motion, and zoom.

## Technical Context

**Language/Version**: TypeScript with Node.js 20 minimum; Python 3.8 for generated consumer regression coverage

**Primary Dependencies**: Next.js App Router, React, Fumadocs UI, Playwright, axe-core

**Storage**: Static source and generated site files only

**Testing**: Node contract tests, Playwright browser verification, Python generator tests, aggregate five-kit build

**Target Platform**: Static web export on modern desktop and mobile browsers

**Project Type**: Static documentation and brand portfolio site plus Python kit generator

**Performance Goals**: No new runtime dependency or client-side state; CSS-only interaction treatment

**Constraints**: WCAG 2.1 AA, 44-pixel discrete targets, 360-pixel layout, 200 percent zoom, reduced motion, no generated artifacts committed

**Scale/Scope**: Every public site anchor family, nine documentation pages, five hosted guidelines, two themes, two viewport widths

## Constitution Check

- P1 passes: only generator, site, tests, and Spec Kit sources are committed.
- P2 passes: no identity geometry or palette changes are permitted.
- P3 passes: automated AA, focus, touch, motion, and zoom gates are mandatory.
- P4 passes: all production kits and the site rebuild before publication.
- P5 passes: site chrome owns taxonomy while copied brand guidelines remain isolated.
- P6 passes: S018 specification, plan, tasks, evidence, changelog, and PR move together.

Post-design re-check: all gates pass with no exception or complexity waiver.

## Project Structure

```text
skill/templates/gen_vanilla.py
skill/templates/test_pipeline.py
site/app/globals.css
site/app/(site)/page.tsx
site/app/(site)/[slug]/page.tsx
site/components/footer.tsx
site/mdx-components.tsx
site/scripts/verify-site.mjs
specs/018-semantic-link-navigation/
```

**Structure Decision**: Keep the global taxonomy in site shell CSS, attach explicit role classes at authored link sites, use stable Fumadocs descendant structure only where runtime markup is framework-owned, and fix the shared generated anchor default at its source template.

## Implementation Phases

1. Record rendered anchor inventory and state contract.
2. Add failing generator and browser assertions for duplicate decoration, semantic families, pagination hierarchy, neighbors, themes, motion, and zoom.
3. Remove the generated global hover underline and implement explicit site roles.
4. Restyle pagination with neutral tokens and stable structural selectors validated against rendered markup.
5. Rebuild all kits and the site, inspect representative screenshots, and publish with review closure.
