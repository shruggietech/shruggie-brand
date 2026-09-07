# Implementation Plan: Guidelines Reference Experience

**Branch**: `codex/017-guidelines-reference-experience` | **Date**: 2026-09-07 | **Spec**: [spec.md](spec.md)

## Summary

Replace the fixed three-image guideline page with a manifest-derived reference experience. Generate semantic asset groups from logo provenance and icon manifests, deterministic multi-space color references from canonical tokens, scoped dark/light specimens, progressive internal navigation, and portable links that the site publisher rewrites into hosted download URLs. Extend generator, publication, and browser verification together.

## Technical Context

**Language/Version**: Python 3.8 minimum; generated HTML, CSS, and JavaScript; Node.js 20 minimum for browser verification

**Primary Dependencies**: Python standard library, ColorAide, Pillow for measured raster inventory, existing Playwright site verification

**Storage**: Committed generator and site source; generated guides and catalogs remain under ignored `dist/`

**Testing**: Python unittest pipeline and publication tests, five-kit aggregate build, Playwright site verification, Markdown and encoding checks

**Target Platform**: Portable offline guideline HTML and statically hosted `brand.shruggie.tech` routes

**Project Type**: Source-first generator plus static site publisher

**Performance Goals**: One self-contained guide per brand, no runtime network dependency, and no preview duplication proportional to raster-size count

**Constraints**: WCAG 2.1 AA, 360px and 200 percent zoom support, Python 3.8, no committed generated output, no identity or palette changes

**Scale/Scope**: Five production brands, 21 logo SVG/PNG families per full build, five platform icon suites per brand

## Constitution Check

| Principle | Treatment | Result |
| --- | --- | --- |
| P1 Sources only | Generator, tests, and publication rules are committed; guide output remains ignored. | PASS |
| P2 Identity preserved | Catalog consumes generated masters and does not modify geometry or pixels. | PASS |
| P3 Accessibility | Local theme contexts, focus, announcements, touch targets, zoom, and reduced motion are measured. | PASS |
| P4 Verification first | Focused tests, five-kit builds, browser checks, and hosted CI block completion. | PASS |
| P5 Site consumes kits | Portable HTML remains authoritative; publication performs a narrow deterministic link/context rewrite. | PASS |
| P6 Spec Kit | Specification, design, tasks, analysis, evidence, and changelogs move together. | PASS |

Post-design recheck: PASS. No constitution exception is required.

## Project Structure

```text
specs/017-guidelines-reference-experience/
|-- spec.md
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- evidence.md
|-- checklists/
|   |-- requirements.md
|   `-- experience.md
|-- contracts/
|   |-- guide-catalog.md
|   `-- publication-context.md
`-- tasks.md

skill/templates/gen_guidelines.py
skill/templates/test_pipeline.py
scripts/prepare_site.py
scripts/test_prepare_site.py
site/scripts/verify-site.mjs
skill/SKILL.md
skill/AGENTS.md
CHANGELOG.md
skill/CHANGELOG.md
```

**Structure Decision**: Keep the guide as one self-contained generated document. Read provenance and icon manifests after logo generation, embed representative previews, and mark portable asset links with an explicit attribute so publication can rewrite only those links and inject the single hosted exit.

## Implementation Phases

1. Pin baseline invariants and write failing generator and publication tests.
2. Add deterministic color conversion and catalog grouping helpers.
3. Replace fixed guide markup with semantic sections, comparison wells, copy controls, and progressive navigation.
4. Add narrow hosted-context rewriting and assertions.
5. Rebuild all kits, inspect responsive evidence, run site and repository gates, publish, and resolve review.

## Complexity Tracking

No violations require justification.
