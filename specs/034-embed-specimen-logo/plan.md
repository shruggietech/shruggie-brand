# Implementation Plan: Embed Specimen Logo

**Branch**: `codex/034-embed-specimen-logo` | **Date**: 2026-09-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/034-embed-specimen-logo/spec.md`

## Summary

Make generated type specimens portable by resolving each governed image component inside its staged kit and embedding the exact source bytes as a media-typed base64 data URI. Select an already approved supplied horizontal color lockup for the specimen when the brand declares one, otherwise retain the canonical full/reduced mark fallback. Add a production `verify.py` specimen gate for self-contained references, source-byte equivalence, and rendered visible pixels in the declared header mark region. Extend the isolated pipeline regression with image-based synthetic brands and exercise the exact I Heart PR Tours SVG through hosted direct navigation and offline local opening. Preserve authoritative logo files and native proportions, prove the site copy and kit archive derive from the identical specimen bytes, and run the full repository validation matrix.

## Technical Context

**Language/Version**: Python 3.8-compatible generator and verification code; Node.js 20-compatible site verification code

**Primary Dependencies**: Python standard library, fontTools, Pillow, existing SVG rasterizer abstraction (`rsvg-convert`, `resvg`, Inkscape, or bundled `@resvg/resvg-js`), Playwright Chromium, existing deterministic ZIP publication code

**Storage**: Governed JSON and logo source files, generated SVG specimens, temporary raster evidence, generated site copies, and deterministic ZIP archives; no database

**Testing**: `unittest` suites in `skill/templates/test_pipeline.py` and `scripts/test_prepare_site.py`, production `verify.py`, `validate_glyph.py`, Playwright browser verification in `site/scripts/verify-site.mjs`, full CI-parity build and release checks

**Target Platform**: Portable SVG consumers, local/offline file viewers, evergreen Chromium, Linux and Windows CI, Python 3.8 minimum runtime

**Project Type**: Static brand-kit generator and statically exported documentation site

**Performance Goals**: Embed each source once with linear byte encoding; keep a single specimen near the source artwork plus outlined-type payload size; add only one 1600-pixel temporary render per production kit during verification

**Constraints**: Preserve authoritative source bytes and geometry; reject path escapes and missing sources; no generated artifacts committed; WCAG 2.1 AA remains non-exemptable; absent optional renderers become explicit skips; no foreground windows; no external image fetches

**Scale/Scope**: Eight production brands, one generated SVG specimen per kit, one or more logo components per mark, one affected production brand with an image-based specimen mark, one isolated synthetic image regression

## Constitution Check

*GATE: Passed before Phase 0 research and re-checked after Phase 1 design.*

| Principle | Plan alignment | Result |
| --- | --- | --- |
| P1. Sources are committed and artifacts are rebuilt | Changes are limited to generator/verifier/site-test sources and S034 documentation. Synthetic brand data is created only in a temporary directory. Generated kits, rasters, exports, and archives remain ignored. | PASS |
| P2. Identity geometry is preserved | The existing governed file is read without rewriting and its exact bytes are encoded. No brand path, dimensions, placement, color, transparency, source file, or approval record changes. | PASS |
| P3. Accessibility has no exemption | No color roles change. The complete existing AA pipeline remains required. | PASS |
| P4. Verification precedes publication | `verify.py` gains structural and rendered specimen gates. Full builds still require zero verifier problems and zero glyph failures, with unavailable renderers reported explicitly. | PASS |
| P5. The site consumes generated kits | Browser coverage targets the specimen copied from verified `dist/` output and compares hosted, offline, and downloadable-kit provenance without reauthoring the artwork. | PASS |
| P6. Specifications and releases move together | S034 maintains spec, plan, tasks, evidence, analysis, changelog, tests, and implementation together, ending at a local pre-push commit. | PASS |

Post-design re-check: PASS. The design adds no constitutional exception, changes no authoritative identity source, and strengthens P4 and P5 enforcement.

## Project Structure

### Documentation (this feature)

```text
specs/034-embed-specimen-logo/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   └── specimen-portability.md
├── checklists/
│   ├── requirements.md
│   └── portability-identity.md
└── tasks.md
```

### Source Code (repository root)

```text
skill/templates/
├── brand_contract.py       # Resolve approved specimen lockup selection and geometry
├── build_specimen.py       # Embed governed image bytes and declare mark region
├── verify.py               # Structural, identity, and rendered-pixel specimen gate
└── test_pipeline.py        # Isolated image-based generator and failure regressions

scripts/
├── prepare_site.py         # Existing verified-kit copy and archive publication path
└── test_prepare_site.py    # Hosted-copy byte-equivalence regression

site/
├── scripts/verify-site.mjs # Exact direct-navigation and offline browser pixel checks
└── tests/site.test.mjs     # Generated specimen route and downloadable-file contract

brands/i-heart-pr-tours/
├── brand.json              # Read-only governed binding and placement authority
└── assets/source/          # Read-only authoritative artwork bytes
```

**Structure Decision**: Extend the existing shared brand-contract helper, generator, production verifier, pipeline regression, publication copy test, and browser verifier. Do not introduce a second specimen implementation, fixture directory, brand-specific generator branch, or generated source artifact.

## Complexity Tracking

No constitution violations or justified complexity exceptions are required.

## Implementation Strategy

1. Write structural and rendered regression expectations against an isolated temporary image-based brand and the current broken production behavior.
2. Add a narrowly scoped source resolver and media-type encoder to the shared specimen generator, preserving both `href` forms and every existing placement value.
3. Add `verify.py` specimen checks that parse all references, compare embedded authoritative image bytes, and render the declared mark region when the capability probe reports a renderer.
4. Add site publication and browser checks for exact-byte copy provenance, direct hosted navigation, offline opening, and visible mark pixels.
5. Rebuild the affected kit first, then run the full eight-kit, release, site, browser, identity, glyph, Markdown, and hygiene matrix.
6. Apply the owner's follow-up correction by resolving the existing approved supplied horizontal color lockup through the shared contract, centering its native dimensions within the mark grid, and proving the fallback remains unchanged.

## Decision Record

- Encode exact source bytes as base64 rather than percent-encoding or inlining child SVG nodes. This is deterministic across text and binary formats, preserves byte authority, and avoids namespace or geometry rewriting.
- Allow only an explicit extension-to-media-type table. This fails closed for unsupported formats and avoids host-dependent MIME guessing.
- Resolve image sources under the staged kit boundary before reading. This prevents an otherwise valid brand-relative path from escaping the governed build root.
- Add the rendered-pixel assertion to `verify.py` and the browser verifier. Generator-only structural tests cannot distinguish a valid but invisible payload from a complete mark.
- Use the existing capability probe and SVG rasterizer abstraction. Core environments record an explicit pixel-check skip; the authoritative CI tier must execute the check.
- Treat publication equivalence as a provenance chain: deterministic archive certification preserves the source specimen bytes, `prepare_site.py` copies those same bytes, and browser verification reads the exact hosted copy.
- Derive specimen lockup choice from `supplied_lockup_input_ids.horizontal.color`. This reuses the existing approval and authoritative-input boundary, avoids a redundant brand field, and selects the wider I Heart PR Tours lockup without modifying `brand.json` or either logo source.
- Preserve the selected lockup's native aspect ratio and scale down only if it exceeds the existing grid. Centering the approved source within the grid changes generated placement intentionally while leaving the outer header transform and authoritative artwork untouched.
