# Implementation Plan: Immutable Kit Publication

**Branch**: `codex/043-immutable-kit-publication` | **Date**: 2026-09-20 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/043-immutable-kit-publication/spec.md`

## Summary

Publish one coherent, immutable BrandBuilder release by making production Pages tag-backed, deriving every public download from the exact release identity, and assigning each generated kit a canonical package identity that includes both brand and compiler versions. Extend the existing consumer and documentation contracts with a generated bundle record and release-impact record so migration guidance distinguishes identity changes from implementation changes without collecting downstream adoption or utility evidence. Because the archive layout and consumer contract change incompatibly, supersede the unpublished `1.3.0` line with `2.0.0`.

## Technical Context

**Language/Version**: Python 3.8 minimum for generated kit tooling, Python 3.12 for the hosted build, TypeScript/React on Node.js 24.11.0 with pnpm 10.28.2 for CI

**Primary Dependencies**: Python standard library contracts and generators, Next.js App Router static export, GitHub Actions, GitHub Pages, GitHub Releases

**Storage**: Versioned JSON and Markdown source contracts; generated `dist/` and site staging remain ephemeral CI artifacts

**Testing**: Python `unittest` contract, generator, packaging, release, and workflow suites; TypeScript checks; Next.js static build; Node site tests; Playwright accessibility checks; aggregate repository verification

**Target Platform**: GitHub-hosted Linux CI, static GitHub Pages, portable generated kits on Python 3.8+, and local Windows development

**Project Type**: Brand-system compiler, release pipeline, and static documentation site

**Performance Goals**: Preserve one verified aggregate build per event, reuse that output for candidate, release, and Pages artifacts, and add no second production-kit rebuild

**Constraints**: WCAG 2.1 AA; zero `verify.py` problems; zero `validate_glyph.py` failures; source-only Git history; no logo geometry changes; UTF-8 without BOM and LF; exact-tag release assets built by CI

**Scale/Scope**: All production brands, the BrandBuilder skill release, two generated adapters, the release workflow, the static site, and four generated guidance surfaces

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **P1, source boundary**: PASS. Only generator, schema, workflow, site source, tests, and Spec Kit artifacts are committed. Generated kits and archives remain in `dist/` or temporary build output.
- **P2, identity geometry**: PASS. No logo path, ownership, affiliation, or inheritance data changes. Brand versions remain unchanged unless source identity changes independently.
- **P3, accessibility**: PASS. Existing AA gates remain mandatory; the site action and generated guidance remain subject to the aggregate accessibility audit.
- **P4, verification**: PASS. Bundle identity, archive filename, checksums, provenance, release identity, and workflow ordering gain fail-closed validation before publication.
- **P5, generated site inputs**: PASS. Site metadata and links are generated from verified release and kit records rather than independently restated.
- **P6, Spec Kit and releases**: PASS. S043 maintains specification, plan, tasks, and evidence. Production deployment and release assets originate from one exact tag; this slice does not create a tag or release.

**Post-design re-check**: PASS. The Phase 1 contracts preserve all six principles and introduce no exception. Publication records carry an explicit candidate or release state, and the version policy requires a BrandBuilder advance for every governed output-contract change.

## Project Structure

### Documentation (this feature)

```text
specs/043-immutable-kit-publication/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
.github/workflows/build.yml          # candidate, release, and Pages orchestration
brands/*/brand.json                  # unchanged brand identity sources
scripts/
├── package_release.py               # canonical kit archive writer
├── prepare_site.py                  # generated publication metadata and staged kits
├── release_contract.py              # exact-release and archive validation
└── test_*.py                         # workflow, release, packaging, and site regression tests
skill/
├── SKILL.md                          # BrandBuilder release metadata
├── references/
│   ├── consumer-contract.schema.json
│   ├── documentation-contract.json
│   ├── documentation-contract.schema.json
│   ├── release-impact.json
│   └── release-impact.schema.json
└── templates/
    ├── interface_contract.py         # bundle record and consumer validation
    └── documentation_contract.py     # generated migration guidance
site/
├── generated/                        # ignored, prepared from verified build output
├── lib/layout.shared.tsx             # exact release action
├── scripts/verify-site.mjs
└── tests/site.test.mjs
```

**Structure Decision**: Extend the existing compiler, release verifier, and site preparation boundaries. The release-impact record is source authority under `skill/references/`; each kit's bundle record and all public guidance are generated artifacts. No new service or persistent store is introduced.

## Complexity Tracking

No constitution violations or additional architectural layers are required.
