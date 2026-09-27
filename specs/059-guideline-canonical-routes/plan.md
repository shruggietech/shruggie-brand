# Implementation Plan: Canonical Brand Guideline Routes

**Branch**: `codex/059-guideline-canonical-routes` | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

## Summary

Resolve #285 by deriving every dedicated brand guideline page URL from its visible menu label, migrating Overview, Logo, and Assets to `/<brand>/guidelines/<label-slug>/`. Generate static compatibility bridges for the three old page paths per brand, while leaving direct file downloads unchanged. Update navigation, metadata, indexing, and publication verification in one slice.

## Technical Context

**Language/Version**: Python 3.8 minimum; TypeScript/Next.js 16 on Node 20 minimum.
**Primary Dependencies**: Existing BrandBuilder templates and site preparation, Next.js static export, React, GitHub Pages deployment.
**Storage**: Brand source and generator templates; ignored generated kits, `site/generated/`, and `site/out/`.
**Testing**: Python generator/site-preparation tests, eight production kits and glyph validation, site lint/build/browser verifier, README link and release-contract checks.
**Target Platform**: Portable brand kits and the GitHub Pages static brand site.
**Project Type**: Brand-kit compiler and static site.
**Performance Goals**: No new live service; compatibility bridge transfers immediately and is a small static page.
**Constraints**: GitHub Pages serves exported files, so legacy bridges cannot emit HTTP 301/308; WCAG 2.1 AA; no generated files committed; approved identity geometry unchanged.
**Scale/Scope**: Eight brands, nine possible guideline topics (one optional), three changed page paths per brand, direct asset download tree preserved.

## Constitution Check

- **P1**: Commit only source, tests, documentation, and Spec Kit evidence. Generated kits and site export remain ignored.
- **P2**: No logo, social image, or approved identity path data changes.
- **P3**: Canonical pages and accessible redirect fallback satisfy WCAG 2.1 AA.
- **P4**: Run all eight kit and glyph checks, then full site verification.
- **P5**: Generated portal topic records are authoritative; site navigation consumes their paths instead of maintaining a second key-based route table.
- **P6**: Spec, route contract, tests, version and changelog, and evidence move together. Formal release is later.

All six principles pass before design and remain satisfied by the proposed source-level implementation.

## Design Decisions

1. **Label slug rule**: Normalize a visible menu label to a lowercase ASCII slug with hyphens between words. Reject empty or duplicate slugs. Current labels map directly (`Overview` to `overview`, `Logo` to `logo`, `Assets` to `assets`, `Expressions` to `expressions`). Keep semantic topic keys (including `logos`) for content lookup; derive URL from `label`.
2. **One source of topic routes**: Define the route grammar in the generator and publish each `topic.path` in portal JSON. Site code validates the label/path relationship and uses the generated path directly. Site preparation consumes the same topic list for route records, breadcrumbs, canonical/social URLs, structured data, homepage links, and sitemap.
3. **Static compatibility bridges**: Export one page for each legacy path: `/<brand>/guidelines/` to Overview, `/guidelines/logos/` to Logo, and `/downloads/` to Assets. The bridge includes immediate client navigation, canonical and `noindex` metadata, and a visible accessible fallback link. Keep bridges out of route records and sitemap. This preserves browser links on GitHub Pages but HTTP status remains 200; true HTTP redirects require host support unavailable in the current deployment.
4. **Assets page**: Render the existing Assets content at the new canonical guideline topic route. Legacy `/downloads/` becomes a bridge; direct `/downloads/files/` and archive paths stay as published.
5. **Search and documentation**: Brand site search currently indexes the main `/docs/` manual, not dedicated brand pages. Assert no legacy brand routes enter published search data. Keep manual routes unchanged; migrate prose links to canonical brand pages.
6. **Version**: Increment BrandBuilder and site from 2.5.0 to 2.6.0 for the generated route and hosted navigation contract, while retaining Brand Canon and brand identity versions. Document old-to-new page URL map and static bridge behavior.

## Project Structure

```text
skill/templates/gen_guidelines.py       # authoritative topic labels and paths
skill/templates/test_pipeline.py        # generated portal route contract
scripts/prepare_site.py                # site route records and publication inputs
scripts/test_prepare_site.py           # route and legacy-path contract tests
scripts/check_readme_links.py          # linked brand-entry validation
site/app/(guidelines)/[slug]/          # canonical topic pages and legacy bridges
site/lib/guidelines.ts                 # generated topic/path validation and navigation
site/scripts/verify-site.mjs           # published canonical and bridge checks
site/tests/site.test.mjs               # generated route and page assertions
skill/references/                     # documentation disposition and version records
specs/059-guideline-canonical-routes/ # specification and evidence
```

## Delivery Sequence

Write failing route and static bridge tests, update generator topic paths and site route records, migrate canonical topic rendering and legacy bridge pages, update internal links and publication checks, bump versions and documentation, run full validation, commit and push, open the authorized PR, then handle CI and at most two review rounds before owner merge handoff.

## Complexity Tracking

No constitution exception. Static compatibility pages are required because the current GitHub Pages deployment has no server redirect facility.
