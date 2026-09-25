# Implementation Plan: Dark Portfolio Cards

**Branch**: `codex/055-dark-portfolio-cards` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

## Summary

Repair the homepage regression by separating portfolio surfaces from brand-page showcase surfaces and using approved reduced marks at small sizes. Prepare a patch release candidate so the site correction can follow the formal tagged publication path.

## Technical Context

- **Language**: Python site preparation and Next.js/TypeScript static homepage.
- **Sources**: `brands/*/brand.json`, verified kit SVG assets, `scripts/prepare_site.py`, `site/components/brand-portfolio.tsx`, and `site/app/globals.css`.
- **Tests**: Python publication fixtures, static site assertions, browser measurements at desktop/mobile and both site themes, full repository release gates.
- **Constraints**: WCAG 2.1 AA, unchanged SVG geometry, generated exports remain ignored, no new identity approval.

## Constitution Check

- P1: PASS. Source, tests, specs, and release metadata are committed; generated site and kits are ignored.
- P2: PASS. Use exact approved reduced mark assets without editing their geometry.
- P3: PASS. Enforce readable dark card text and preserve focus and target checks.
- P4: PASS. Run documented full kit, glyph, site, and release checks.
- P5: PASS. Site copies from verified kits and does not patch generated kit contents.
- P6: PASS. S055 specification, plan, tasks, analysis, and evidence remain in sync.

## Design Sequence

1. Add a preparation regression for light showcases, dark portfolio surfaces, reduced icon paths, and rejected invalid surfaces.
2. Add static and browser assertions that all homepage cards use dark surfaces and reduced marks in both layouts.
3. Publish `portfolioSurface` from each approved dark card color, replace homepage icon with reduced-color SVG, and remove obsolete light portfolio CSS.
4. Prepare patch release metadata and run the full documented validation.
5. Commit, open a pull request, resolve CI and reviews, then hand off for merge and formal release.

## Post-Design Constitution Check

P1-P6 remain satisfied; the brand's independently light showcase stays governed by its existing source.
