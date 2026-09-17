# Implementation Plan: Component Recipes and Web AppFrame

**Branch**: `codex/038-component-recipes-web-appframe` | **Date**: 2026-09-17 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/038-component-recipes-web-appframe/spec.md`

## Summary

Add a renderer-neutral component recipe catalog beside Interface Canon, validate its fixed 15-recipe vocabulary and invariants before generation, and compile the resolved contract into framework-neutral web custom properties plus a typed React adapter. Introduce a single-owner AppFrame contract for safe areas, titlebar regions, root scrolling, fixed chrome, IME obstruction, and global focus. Use a pinned accessible headless layer for behavior-heavy controls while BrandBuilder retains semantic styling, packaging, and verification authority. Generate a browser specimen and conservative support records; extend consumer manifests, kit verification, release certification, and all-brand regression coverage without committing `dist/`.

## Technical Context

**Language/Version**: Python 3.8-compatible compiler and validation code; JSON Schema draft 2020-12; TypeScript/TSX targeting React 19 with React 18 compatibility; CSS custom properties

**Primary Dependencies**: Python standard library, existing `coloraide`; React peer dependency; exact pinned Radix aggregate package for behavior-heavy components; existing Playwright Chromium and axe-core site verification

**Storage**: Versioned JSON reference contracts and generated static kit files; no database or network persistence

**Testing**: Python `unittest`, JSON Schema validation, deterministic-byte comparisons, generated TypeScript checks, Playwright Chromium interaction tests, axe accessibility scans, all-brand builds, existing site and release suites

**Target Platform**: Modern browsers, server-aware Next.js, Vite browser applications, and Vite-based Tauri or Wails webviews; conservative support records for Chrome, Windows 11 desktop-web profiles, and Android Chrome profiles

**Project Type**: Static design-system compiler and generated cross-framework UI adapter

**Performance Goals**: Deterministic generation for every production brand; zero generator-time network fetches; one pinned behavior dependency; one style and source pass per kit

**Constraints**: WCAG 2.1 AA; no generated `dist/` committed; no logo or identity-source changes; no OS-based behavior routing; server-safe imports cannot read browser globals; every AppFrame boundary has one owner; UTF-8 without BOM and LF

**Scale/Scope**: 15 bounded recipes spanning the 14 named component families, three web host profiles, all production brands, one shared recipe contract, one Web/React adapter version

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Gate | Result |
| --- | --- | --- |
| I. Source-Only Repository | Generated kits, specimens, and browser evidence remain under ignored `dist/` or temporary directories; only compiler sources, references, tests, dependency locks, and Spec Kit artifacts are committed. | PASS |
| II. Preserve Identity Geometry | No brand source, approved artwork, logo path, affiliation, or provenance change is planned. Adapter values resolve through existing governed contracts. | PASS |
| III. Measured Accessibility | Recipe validation encodes accessible names, focus, keyboard behavior, 44-unit targets, reduced motion, forced colors, and state semantics; browser specimens receive axe and interaction tests. | PASS |
| IV. Full-Kit Verification | `build_all.py`, `verify.py`, glyph validation, release certification, and deterministic rebuild checks cover every production brand. | PASS |
| V. Site Consumes Verified Kits | Browser evidence reads generated output only after all-brand build; no parallel hand-authored public kit is introduced. | PASS |
| VI. Spec-Driven Releases | S038 spec, plan, research, model, contracts, tasks, and verification evidence stay synchronized. Component recipe and adapter versions are reported without publishing a release. | PASS |

Post-design re-check: the dedicated contract and adapter generator preserve the source/output boundary; the exact dependency record makes the accessible behavior layer reviewable and recoverable; generated specimens remain evidence only. No constitutional exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/038-component-recipes-web-appframe/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   ├── component-recipes.md
│   └── web-adapter.md
├── checklists/
│   ├── requirements.md
│   └── recipe-adapter-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
skill/
├── SKILL.md
├── references/
│   ├── component-recipes.json
│   ├── component-recipes.schema.json
│   ├── consumer-contract.schema.json
│   └── web-support-matrix.json
└── templates/
    ├── component_contract.py
    ├── gen_web_react.py
    ├── build_kit.py
    ├── gen_enforcement.py
    ├── interface_contract.py
    ├── verify.py
    ├── test_component_contract.py
    ├── test_interface_contract.py
    └── test_pipeline.py
scripts/
├── package_release.py
├── prepare_site.py
├── test_package_release.py
├── test_prepare_site.py
└── test_release_contract.py
site/
├── scripts/verify-site.mjs
├── package.json
└── pnpm-lock.yaml
```

Generated and never committed:

```text
dist/<brand>/
├── tokens/interface.css
├── web/
│   ├── components.css
│   ├── component-recipes.json
│   ├── app-frame-hosts.json
│   ├── support-matrix.json
│   ├── adapter.json
│   ├── react/
│   │   ├── server.tsx
│   │   ├── client.tsx
│   │   └── index.ts
│   ├── specimen.html
│   └── README.md
└── enforcement/
    ├── component-recipes.json
    ├── component-recipes.schema.json
    └── consumer-contract.json
```

**Structure Decision**: Keep renderer-neutral authoring data in `skill/references/`, reusable validation and compilation in `skill/templates/`, and generated adapter artifacts under one `web/` kit boundary. Existing vanilla and Next.js generators remain compatibility surfaces; the new generator consumes the same resolved brand and Interface Canon inputs. Site preparation may copy generated TSX into ignored `site/generated/` solely for type-checking.

## Complexity Tracking

No constitution violations require justification.
