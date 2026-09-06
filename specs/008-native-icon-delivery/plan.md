# Implementation Plan: Native Icon Delivery and Favicon Integrity

**Branch**: `codex/008-native-icon-delivery` | **Date**: 2026-09-05 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/008-native-icon-delivery/spec.md`

## Summary

Deliver issues #106 and #110 through one manifest-driven icon pipeline. Extend the brand contract with an explicit application-icon background, compose all web and native derivatives from canonical full or reduced mark sources, package them under an authoritative `icons/` taxonomy, retain `favicons/` as verified compatibility aliases, preserve source-owned product symbols byte for byte under `icons/domain/`, add native metadata and platform instructions, strengthen kit validation, and publish the verified ShruggieTech web suite to every brand-site route.

## Technical Context

**Language/Version**: Python 3.8 minimum for generator and validation code; TypeScript on Node.js 20 minimum for the static site

**Primary Dependencies**: Pillow 10.4 minimum, svgelements 1.9.6, existing SVG renderer capability chain, Next.js 16.3.4, Playwright 1.62.1, Node standard `zlib`

**Storage**: Source JSON and image assets in `brands/`; generated filesystem trees in ignored `dist/` and `site/out/`

**Testing**: Python `unittest`, generator behavioral tests, full production kit builds, `verify.py`, `validate_glyph.py`, TypeScript type checking, static export, Playwright and axe-core site validation

**Target Platform**: Cross-platform brand-kit generation; Android application resources; iOS and iPadOS asset catalogs; macOS asset catalogs and ICNS; Windows classic and MSIX assets; static web deployment

**Project Type**: Generator CLI plus statically exported documentation and download site

**Performance Goals**: Generate and validate all five icon suites for each production brand within the existing aggregate CI build without network access or per-artifact subprocess launches

**Constraints**: Preserve source geometry byte for byte; never commit generated artifacts; use hidden non-interactive child processes on Windows; enforce WCAG 2.1 AA; do not byte-compare rendered PNG or PDF correctness; retain Python 3.8 syntax compatibility

**Scale/Scope**: Five production brands, five platform suites per raster-capable kit, roughly 80 image and metadata artifacts per kit, one public site icon contract, two closing issues

## Constitution Check

*GATE: Passed before research and re-checked after design.*

| Principle | Design response | Gate |
|---|---|---|
| P1. Sources are committed and artifacts are rebuilt | Commit only generator, validator, source contract, site source, tests, and Spec Kit documents. All PNG, ICO, ICNS, archive, and site export output remains generated in ignored directories. | PASS |
| P2. Identity geometry is preserved | Reuse the existing full and reduced mark renderers. Platform composition changes canvas, scale, background, color role, and encoding only. No path data is edited. | PASS |
| P3. Accessibility has no exemption | Preserve existing site AA validation. Icon metadata uses empty alternative text only where icons are decorative; no text-bearing contrast waiver is introduced. | PASS |
| P4. Verification precedes publication | Extend `verify.py`, generation tests, site materialization tests, and emitted-site checks. Raster-capable production suites cannot skip required artifacts. | PASS |
| P5. The site consumes generated kits | Remove raw source fallbacks for the public icon suite and copy only verified `dist/shruggietech/icons/web` outputs. | PASS |
| P6. Specifications and releases move together | S008 includes synchronized spec, plan, contracts, tasks, evidence, implementation, tests, and changelog decision. No release or tag is cut. | PASS |

### Post-design re-check

The platform matrix, manifest, compatibility mirror, and site publication contract preserve every constitutional boundary. Pillow container writing is a measured raster-tier dependency already present in CI, not an optional unverified artifact path. No complexity exception is required.

## Architecture Decisions

1. **Separate composition from logo generation**: add `skill/templates/iconkit.py` for pure manifest, image composition, native metadata, and validation helpers. `gen_logo.py` remains the orchestrator because it already owns canonical mark rendering and measured raster capability.
2. **Authoritative tree plus aliases**: `icons/` owns delivery; `favicons/` is populated only by byte-copying `icons/web/` after successful generation.
3. **Domain-symbol collision handling**: Legacy source-owned product symbols are captured before generated-output replacement, restored byte for byte below `icons/domain/`, and included in exact manifest validation.
3. **Declarative brand background**: `logo.application_icon.background` is optional in the schema and defaults through `brand_contract.py` to `surfaces.base`.
4. **One high-resolution foreground raster per source variant**: rasterize canonical SVG sources once, then use high-quality in-process resizing and composition for platform matrices. This avoids one subprocess per icon.
5. **Manifest-driven verification**: `verify.py` validates the manifest, exact file inventory, native JSON/XML, image pixels, aliases, ICO, and ICNS containers.
6. **Static export integrity**: the Node verifier parses PNG and ICO structures, decodes PNG scanlines, resolves SVG references, checks manifest relationships, and confirms route-level shared declarations.

## Project Structure

### Documentation (this feature)

```text
specs/008-native-icon-delivery/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evidence.md
├── contracts/
│   ├── icon-manifest.md
│   ├── platform-suites.md
│   └── site-icon-contract.md
├── checklists/
│   ├── requirements.md
│   └── integrity.md
└── tasks.md
```

### Source code (repository root)

```text
brands/shruggietech/brand.json          # Approved site icon background
skill/references/canon.schema.json      # Optional application-icon contract
skill/references/02-kit-anatomy.md      # Human archive map
skill/references/04-toolchain.md        # Capability and validation behavior
skill/templates/brand_contract.py       # Effective icon profile validation
skill/templates/iconkit.py              # Platform matrices, composition, metadata
skill/templates/gen_logo.py             # Canonical SVG orchestration and suite call
skill/templates/verify.py               # Manifest and artifact verification
skill/templates/test_brand_contract.py  # Contract tests
skill/templates/test_pipeline.py        # Generator and corruption tests
scripts/prepare_site.py                 # Generated web-suite publication
scripts/test_prepare_site.py            # Publication contract tests
site/app/layout.tsx                     # Shared root icon metadata
site/app/(site)/[slug]/downloads/page.tsx # Categorized download entry
site/scripts/verify-site.mjs            # Emitted icon decoding and route validation
site/tests/site.test.mjs                # Required URL and route fixtures
skill/SKILL.md                          # Generated-kit delivery guidance
skill/CHANGELOG.md                      # Skill-facing release notes
CHANGELOG.md                            # Repository decision and feature record
```

**Structure Decision**: Add one cohesive generator module beside existing templates and extend current validation and site publication seams. Do not create a separate application or commit platform projects.

## Implementation Phases

### Phase 1: Contract and failing tests

Add schema/profile tests, icon-manifest expectations, platform matrix tests, corruption tests, stale-output tests, site publication tests, and emitted-site icon assertions before production implementation.

### Phase 2: Composition and packaging

Implement safe path clearing, canonical raster preparation, platform composition, native metadata, container generation, README output, top-level manifest creation, and compatibility aliases.

### Phase 3: Verification and publication

Extend kit verification, update documentation and download surfaces, publish the ShruggieTech web suite, and enforce static-export decoding and route inheritance.

### Phase 4: Aggregate evidence

Run Python 3.8-compatible tests, all production kit builds, release-contract checks, generated-agent synchronization, site lint/build/test, repository hygiene, encoding, mojibake, and diff review. Record results in `evidence.md`.

## Scope Control

- S008 closes only #106 and #110 after merge evidence.
- S008 does not alter documentation typography, code-block rendering, callout transformation, navigation duplication, structured data, social-preview routing, sitemap URLs, or page-aware metadata tracked by #108, #109, and #111.
- S008 does not cut a release or tag.
- S008 does not modify approved mark path data.

## Complexity Tracking

No constitutional violations require justification.
