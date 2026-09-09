# Implementation Plan: Complete Kit Downloads and Explicit Brand Actions

**Branch**: `codex/024-kit-download-actions` | **Date**: 2026-09-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/024-kit-download-actions/spec.md`

## Summary

Deliver issues #173 and #174 as one dependency-complete slice. Extend the existing deterministic release archive contract to every public production brand, reuse that verified archive writer during site materialization, expose one brand-specific archive record to the homepage, and replace full-card links with explicit desktop actions plus native mobile disclosures. Preserve generated-kit authority, third-party attribution, static delivery, keyboard access, reduced motion, and fail-closed publication.

## Technical Context

**Language/Version**: Python 3.8 minimum for archive and site preparation; TypeScript 5.9 and JavaScript ES modules on Node.js 20 minimum for the site

**Primary Dependencies**: Python standard-library `zipfile`, Next.js 16.3 static export, React 19.2, Playwright 1.62.1, axe-core

**Storage**: Source-controlled Python, TSX, CSS, JSON contracts, and Spec Kit records; generated `dist/`, `release/`, `site/public/generated/`, archives, static export, and browser evidence remain uncommitted

**Testing**: Python `unittest`, Node test runner source contracts, Playwright rendered-site checks, axe WCAG audits, TypeScript, aggregate production-kit verification

**Target Platform**: GitHub Pages static export in evergreen desktop and mobile browsers; GitHub release archives use the same writer

**Project Type**: Deterministic build pipeline plus static brand portfolio website

**Performance Goals**: One archive pass per published brand during site preparation; no client JavaScript required for portfolio disclosure or downloads; no desktop card layout shift

**Constraints**: WCAG 2.1 AA floor; byte-preserved logo geometry; archives derived only from verified `dist/`; deterministic ordering, timestamps, permissions, compression, and bytes; no generated artifact committed; static hosting cannot set per-file `Content-Disposition` headers

**Scale/Scope**: Six public production brands, six complete archives, six desktop cards, six mobile disclosure rows, one shared third-party disclaimer, and two linked GitHub issues

## Constitution Check

### Pre-design gate

- **P1 PASS**: Only archive/site generator source, tests, and Spec Kit artifacts are committed. Generated ZIPs and site exports remain ignored.
- **P2 PASS**: No logo source or derivative geometry changes.
- **P3 PASS**: Keyboard, focus, touch target, zoom, contrast, and reduced-motion checks remain blocking.
- **P4 PASS**: Archives are assembled only from verified production output and are independently checked against manifest bytes and hashes before publication.
- **P5 PASS**: The site consumes the generated kit and its authoritative manifest; it does not maintain a second asset inventory.
- **P6 PASS**: S024 uses the complete Spec Kit flow, retains release automation, and records issue, CI, review, and changelog evidence.

### Post-design gate

- **PASS**: The design introduces no committed generated artifacts, geometry mutations, accessibility waivers, or hand-authored duplicate brand inventories.
- **PASS**: One reusable archive writer and one generated portfolio record govern release and site delivery.
- **PASS**: Native disclosure and ordinary anchors keep core actions available without client scripting.

## Project Structure

### Documentation (this feature)

```text
specs/024-kit-download-actions/
├── checklists/
│   ├── archive-ux.md
│   └── requirements.md
├── contracts/
│   └── kit-download-actions.md
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
scripts/
├── package_release.py
├── prepare_site.py
├── release_contract.py
├── test_package_release.py
├── test_prepare_site.py
└── test_release_contract.py

site/
├── app/
│   ├── (site)/page.tsx
│   └── globals.css
├── components/brand-portfolio.tsx
├── scripts/verify-site.mjs
└── tests/site.test.mjs
```

**Structure Decision**: Reuse the existing release and site preparation modules. Add one server-rendered portfolio component to keep the homepage legible while desktop and mobile presentations consume the same generated record.

## Implementation Strategy

### Phase 0: Lock archive and interaction contracts

Add failing unit/source contracts for a six-brand release inventory, atomic deterministic archive output, site archive publication, exact portfolio record fields, explicit actions, native disclosure semantics, and one shared disclaimer.

### Phase 1: Unify and publish complete archives

Make the release contract the sole production-brand archive inventory, including ESO Weave. Extract an atomic reusable brand-archive writer from release packaging, verify every archive before replacing its destination, and invoke it from both release packaging and site materialization. Publish the stable filename and path in each generated brand record.

### Phase 2: Replace ambiguous card navigation

Render non-interactive desktop card containers with a reserved content stage that swaps descriptions for exactly two anchors on hover or focus within. Render mobile cards as native `details` disclosures with semantic `summary` controls and the same actions. Keep each responsive variant unavailable to the accessibility tree outside its breakpoint through layout display rules.

### Phase 3: Consolidate attribution and verify behavior

Derive applicable markers from generated vendor-boundary data and render the full legally meaningful notice once after the portfolio. Exercise pointer, keyboard, disclosure, breakpoint, zoom, reduced-motion, link, download, MIME, ZIP signature, and accessibility behavior in the rendered export.

### Phase 4: Validate and publish

Run focused Python and site tests, full production kit builds, archive certification, static export, rendered accessibility checks, repository hygiene, encoding, and mojibake scans. Commit, push under the operator's explicit authorization, open a PR closing #173 and #174, process every initial review finding, request at most one second `@Codex` round, resolve all threads, and wait for green CI.

## Complexity Tracking

No constitution violation is required. The plan deliberately interprets download disposition through the same-origin anchor `download` contract because GitHub Pages cannot emit custom per-file `Content-Disposition` headers. The generated `.zip` path supplies the archive media type, and rendered verification checks the actual response type and ZIP signature.
