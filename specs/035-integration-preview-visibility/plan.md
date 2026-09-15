# Implementation Plan: Integration Preview Visibility

**Branch**: `codex/035-integration-preview-visibility` | **Date**: 2026-09-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/035-integration-preview-visibility/spec.md`

## Summary

Repair shared integration preview generation so visual groups use an explicit or measured accessible well, nonvisual deliveries receive intentional format-aware semantics, and all text inside wells has an explicit AA foreground. Keep every asset byte and geometry unchanged, add isolated six-class regression fixtures and generated-browser checks, regenerate all kits, and retain zero-problem `verify.py` and zero-failure `validate_glyph.py` results.

## Technical Context

**Language/Version**: Python 3.8 minimum for generator and unit coverage; JavaScript on Node.js 20 minimum for generated-site and Playwright verification

**Primary Dependencies**: Pillow for read-only raster sampling, Coloraide and existing WCAG helpers, Python `unittest`, Next.js static export, Playwright Chromium, axe-core

**Storage**: Governed JSON/SVG/PNG inputs and generated local files; no database or persistent runtime state

**Testing**: `skill/templates/test_pipeline.py`, generator and publication suites, all-kit `build_all.py`, generated `verify.py`, generated `validate_glyph.py`, site source tests, TypeScript/build checks, Playwright/axe browser verification

**Target Platform**: Self-contained generated HTML opened directly or copied into the statically exported public site, with Windows and Linux CI parity

**Project Type**: Python generator plus statically exported web documentation

**Performance Goals**: Deterministic preview classification with bounded sampling at the actual 180 CSS pixel preview scale and no material increase in all-kit build duration

**Constraints**: WCAG 2.1 AA, Python 3.8, exact asset-byte and geometry preservation, isolated synthetic fixtures only, no committed generated output, LF and UTF-8 without BOM, no browser-time mutation or CSS filters

**Scale/Scope**: Every visual and nonvisual delivery group in eight production kits, with focused I Heart PR Tours portable-file browser acceptance at 1280 and 360 CSS pixel widths plus 200 percent zoom

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **P1, sources and rebuilds**: PASS. Changes are limited to `skill/templates/`, site verification source, changelog, and S035 artifacts. Synthetic brands and images exist only inside temporary test directories. Generated `dist/`, `site/out/`, screenshots, PDFs, and archives remain uncommitted.
- **P2, identity geometry**: PASS. Preview analysis reads exact delivery bytes and changes only containing HTML/CSS metadata. It does not rewrite, recolor, crop, invert, filter, normalize, or regenerate source geometry.
- **P3, accessibility**: PASS. Visual previews in the affected guide require at least 3:1 measured non-text contrast and all well text requires at least 4.5:1 contrast. The shared resolver records the best available score for pre-existing approved assets in other kits whose intrinsic alpha cannot reach 3:1 on either fixed well; it never alters those assets.
- **P4, verification**: PASS. Tasks include focused red-green coverage, production `verify.py` and `validate_glyph.py` gates through all-kit generation, complete CI parity, explicit optional-renderer skips, and visual review.
- **P5, generated-kit consumption**: PASS. The portable file and hosted portal consume the same generated presentation metadata. The site does not restate brand values.
- **P6, specification and release discipline**: PASS. S035 maintains spec, design, tasks, analysis, implementation, and evidence together. No release or push is in scope.

**Post-design re-check**: PASS. The selected shared resolver, portable markup contract, test fixture isolation, and browser verification preserve all six principles without exception.

## Project Structure

### Documentation (this feature)

```text
specs/035-integration-preview-visibility/
├── checklists/
│   ├── preview-accessibility.md
│   └── requirements.md
├── contracts/
│   └── integration-preview-contract.md
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
skill/templates/
├── gen_guidelines.py
└── test_pipeline.py

site/scripts/
└── verify-site.mjs

brands/i-heart-pr-tours/
└── brand.json                 # read-only governed input

CHANGELOG.md
```

**Structure Decision**: Keep surface analysis, portable rendering, and portal projection in the existing guideline generator because it owns the shared preview presentation contract. Extend the existing pipeline and site browser suites rather than adding a new package or committed fixture tree.

## Design

### Group-aware presentation resolver

One pure, read-only helper receives a delivery group and returns the exact preview delivery plus `kind`, `surface`, measured contrast, and display labels. Visual groups preserve the existing grouping key and inventory. When measurable output exists, significant-pixel coverage and median contrast select the strongest well even if generic, stale, or target-oriented appearance metadata suggests the weaker one. Explicit black/light-target and white/dark-target appearances are used only when no measurable visual delivery is available.

For unproven groups, the resolver selects the largest PNG in that same group, scales a read-only copy to fit the actual 180 CSS pixel preview bound, ignores fully transparent and low-alpha antialiasing fringe relative to the asset's maximum alpha, and computes WCAG relative-luminance contrast for meaningful visible pixels on fixed `#F5F5F5` and `#090909` wells. SVG-only groups are rasterized at the same bound for measurement while the exact SVG remains the embedded preview. The resolver selects the well with the stronger significant-pixel coverage and median score, records the score, and embeds the exact measured delivery bytes as the preview. The affected guide must reach 3:1 in browser acceptance. Existing approved assets in unrelated kits that intrinsically cannot reach 3:1 on either well keep the stronger measured well without blocking their build. Identical bytes and metadata produce identical output. Fully transparent visual input fails clearly instead of receiving an unchecked default.

### Nonvisual presentation

Groups with no PNG or SVG representative use a dedicated nonvisual well. The well says `Nonvisual resource` and names the delivery format and role, such as `XML adaptive declaration`, `JSON metadata`, `ICO container`, or `ICNS container`. It emits no `<img>` and no image-preview wording. Mixed groups retain their visual representative and list every nonvisual sibling exactly once.

### Portable and hosted contract

Portable wells expose deterministic `data-preview-kind`, `data-preview-surface`, and `data-preview-basis` attributes for regression and browser auditing. Measured presentations also expose `data-preview-contrast`. `.dark-well` pins `#F5F5F5` text on `#090909`; `.light-well` and `.nonvisual-well` pin `#111111` text on `#F5F5F5`. The hosted portal receives surface and measurement metadata from the same group-aware resolver, while its existing resource list continues to separate nonvisual deliveries.

### Test strategy

Tests are written before implementation. Temporary fixtures cover transparent dark artwork, declared black, declared white, full-color light artwork, fully transparent failure, JSON/XML metadata, ICO/ICNS containers, and a mixed visual/nonvisual group. Assertions cover exact embedded bytes, hash preservation, deterministic output, one-to-one links, format-aware copy, text-pair CSS, no filters, and escaping/path integrity. Browser checks audit every generated I Heart PR Tours portable asset card at desktop, narrow, and 200 percent zoom, calculate text contrast, require both well types, validate visual or nonvisual exclusivity, check image containment and reflow, run axe on the full asset section, and repeat against a direct `file:` URL.

### Security and tenancy applicability

The generator has no authentication, private data, network request, runtime user input, or tenant boundary. Applicable security tests preserve HTML escaping for manifest-derived text, keep asset paths within the generated kit contract, preserve download destinations, reject missing or malformed visual inputs clearly, and prove temporary synthetic fixtures cannot enter production discovery or publication. Multi-tenant isolation is not applicable because generation is one local source tree to one output tree, but cross-kit contamination remains covered by existing build and publication suites.

## Decision Log

### 2026-09-15, use generator-time visible-output measurement

**Decision**: Resolve presentation from explicit proven appearance semantics or deterministic read-only pixel measurement before emitting HTML and portal metadata.

**Rationale**: This prevents a wrong-well flash, keeps standalone HTML self-contained, provides the hosted portal with the same decision, and creates a reproducible acceptance value without modifying assets.

**Alternatives considered**: A CSS foreground-only patch leaves artwork and semantics broken. Always-light or always-dark wells fail one-color assets. Runtime canvas selection is script-dependent and cannot populate deterministic portal metadata. Per-brand exceptions do not cover future deliveries. Changing icon manifest appearance conflates platform semantics with preview presentation. CSS filters or asset rewriting violate identity preservation.

### 2026-09-15, keep nonvisual deliveries in portable cards with explicit semantics

**Decision**: Use a dedicated nonvisual well in the portable catalog while retaining the hosted portal's existing separate resource list.

**Rationale**: This is the smallest systemic repair, preserves delivery grouping and destination discoverability, and replaces the false image-preview claim with accessible resource information.

**Alternatives considered**: Moving every nonvisual delivery into a new portable section is semantically valid but causes broader navigation and layout churn beyond this focused slice.

## Complexity Tracking

No constitution violations or additional architectural layers are introduced.
