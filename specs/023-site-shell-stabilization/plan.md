# Implementation Plan: Site Shell and Homepage Stabilization

**Branch**: `codex/023-site-shell-stabilization` | **Date**: 2026-09-09 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/023-site-shell-stabilization/spec.md`

## Summary

Deliver issues #170, #171, #172, #176, #177, and #178 as one site-shell slice. Update the authoritative homepage, shared navigation, and shared footer records; reserve the browser scrollbar gutter at the document level; preserve Fumadocs' right-rail allocation; and add source plus Playwright measurements that verify route-to-route stability across themes, viewports, content heights, and scale emulation.

## Technical Context

**Language/Version**: TypeScript 5.9, JavaScript ES modules, Node.js 20 minimum, Python 3.8 minimum for repository validation

**Primary Dependencies**: Next.js 16.3 App Router static export, React 19.2, Fumadocs UI 16.14.3, Playwright 1.62.1, axe-core

**Storage**: Source-controlled TSX, CSS, JSON, Markdown, and Spec Kit artifacts; generated site and kit output remains uncommitted

**Testing**: Node test runner source contracts, Playwright rendered-site checks, axe WCAG audits, TypeScript, aggregate Python validation

**Target Platform**: Static web export in evergreen desktop and mobile browsers

**Project Type**: Static documentation and brand portfolio website

**Performance Goals**: No new runtime dependency or client-side layout correction; no visible route-transition drift beyond one CSS pixel

**Constraints**: WCAG 2.1 AA floor; local generated tokens only; stable shell at light/dark, desktop/narrow, short/tall content, and 100%/200% scale; no route-specific transforms or offsets; no changes to neutral guidelines chrome; UTF-8 without BOM and LF

**Scale/Scope**: One homepage, six retained brand download routes, ten documentation routes, shared desktop/mobile header, and shared site/docs footer

## Constitution Check

### Pre-design gate

- **P1 PASS**: Only site source, verification code, and Spec Kit records are committed. Generated `dist/`, `site/out/`, screenshots, and registries remain ignored.
- **P2 PASS**: No logo geometry or identity path data changes.
- **P3 PASS**: WCAG 2.1 AA, keyboard focus, touch targets, contrast, and reduced motion remain blocking gates.
- **P4 PASS**: Full production verification remains required before publication.
- **P5 PASS**: The site continues to consume generated brand registries and assets. This slice changes only owned shell and homepage source.
- **P6 PASS**: S023 uses the complete repository Spec Kit sequence and records issue, CI, review, and changelog evidence.

### Post-design gate

- **PASS**: The design adds no generated artifacts, geometry mutations, accessibility waivers, duplicated brand data, or unpublished release behavior.
- **PASS**: Source and browser contracts directly cover the requested interaction and stability behavior.

## Project Structure

### Documentation (this feature)

```text
specs/023-site-shell-stabilization/
├── checklists/
│   ├── requirements.md
│   └── ux-accessibility.md
├── contracts/
│   └── site-shell-contract.md
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
├── app/
│   ├── (site)/page.tsx
│   └── globals.css
├── components/footer.tsx
├── lib/layout.shared.tsx
├── scripts/verify-site.mjs
└── tests/site.test.mjs
```

**Structure Decision**: Keep changes inside the existing static site and its authoritative source/rendered verification layers. Do not create route-specific wrappers or fork Fumadocs.

## Implementation Strategy

### Phase 0: Establish evidence and contracts

Capture the current layout mechanics from the owned CSS and Fumadocs slot implementation. Add pure source-policy helpers and browser measurement helpers before production changes so failures identify missing labels, target policies, removed content, and drift.

### Phase 1: Update shared chrome and homepage

Update `baseOptions()` once for all main-site/docs navigation. Simplify the single shared footer record list. Rewrite the homepage action hierarchy and portfolio copy, then remove the obsolete callout and its unused styles.

### Phase 2: Stabilize layout

Reserve the vertical scrollbar gutter on the shared document root. Keep a stable Fumadocs table-of-contents track at desktop widths using the framework's existing layout variables and placeholder model, without per-page correction. Reuse the existing site shell width token for homepage and download content.

### Phase 3: Validate and publish

Run source contracts, TypeScript, a webpack static build if the Windows Turbopack launcher is unavailable, rendered route checks, aggregate production-kit validation, hygiene, encoding, and mojibake scans. Push once, open the issue-closing PR, process initial Codex review, request one second `@Codex` review, resolve every thread, and wait for final green CI.

## Complexity Tracking

No constitution violations or architectural exceptions are required.
