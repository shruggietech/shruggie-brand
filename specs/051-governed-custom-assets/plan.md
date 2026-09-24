# Implementation Plan: Governed Custom Assets and Expressions

**Branch**: `codex/051-governed-custom-assets` | **Date**: 2026-09-23 | **Spec**: [spec.md](spec.md)

## Summary

Add a single optional `custom_assets` source contract and validation path. Select only approved, publication-eligible records for generator projection. Replace legacy `guide.expressions` with this authoritative set, then project it into PDF, portable and hosted guidelines, site asset library, and kit downloads. Preserve supplied sand SVG bytes and existing logo authority. Verify negative cases and output completeness before publication.

## Technical Context

**Language/Version**: Python 3.8+ generator and validation; TypeScript/Next.js on Node 20+

**Primary Dependencies**: Existing BrandBuilder contract/path/hash/SVG helpers, ReportLab PDF generator, static site projection, site tests and verifier

**Storage**: `brand.json` and committed `assets/source` files; ignored generated kit and site records

**Testing**: Python unit/contract/pipeline, full production kit/glyph validation, site unit/build and accessibility checks

**Target Platform**: Offline generated kits and statically exported public brand site

**Constraints**: WCAG 2.1 AA, source SVG byte invariance, no generated artifacts in Git, dark/default compatibility, no external asset hotlinks

**Scale/Scope**: Two supplied I Heart PR Tours assets initially; all other brands with absent collection remain unchanged

## Constitution Check

- **Source only**: PASS. Edit manifest, generator, site source, documentation and tests; no `dist/` contents.
- **Identity preservation**: PASS. Sand sources stay byte-identical and separate from canonical logo binding.
- **AA floor**: PASS by design. Preview wells have explicit presentation and text overlays require readable pairings; no contrast waiver.
- **Measured validation**: PASS. Contract, output inventory, PDF/HTML/site and full kit gates prove publication behavior.
- **Site projection**: PASS. Site consumes generated portal/kit data, not a second custom brand source.
- **Spec Kit/release**: PASS. Spec/plan/tasks/evidence accompany PR. No release tag or merge.

## Project Structure

```text
specs/051-governed-custom-assets/{spec,plan,research,data-model,quickstart,tasks,evidence}.md
specs/051-governed-custom-assets/contracts/custom-assets.md
specs/051-governed-custom-assets/checklists/requirements.md
brands/i-heart-pr-tours/brand.json
skill/references/canon.schema.json
skill/references/02-kit-anatomy.md
skill/templates/{brand_contract,gen_guidelines,gen_guide_pdf,verify}.py
scripts/{prepare_site,test_prepare_site}.py
site/{lib,components,tests}/...
```

**Structure Decision**: Extend the generator-to-site pipeline; do not introduce a parallel registry or a manually curated website inventory.

## Design Sequence

1. Specify schema and fail-first tests for required metadata, local path containment, hash/magic/SVG safety, uniqueness, and publication state.
2. Add contract validation and one eligible-asset selector, retaining original asset bytes and existing authoritative input records.
3. Replace legacy expression reads with eligible projection in portable/PDF generators. Add optional hosted topic and materialize verified delivery paths for asset library/downloads.
4. Migrate the two sand fixtures, update contributor docs, assert empty-brand behavior and cross-output inventory equivalence.
5. Run full documented validation and record source hashes, result counts, manual preview findings, and CI results.

## Post-Design Constitution Check

All six gates remain PASS. `guide.expressions` is removed as an independent source so publication eligibility cannot be bypassed through legacy display-only metadata.
