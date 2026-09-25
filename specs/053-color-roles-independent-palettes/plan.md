# Implementation Plan: Color Roles and Independent Palettes

**Branch**: `codex/053-color-roles-independent-palettes` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

## Summary

Implement #267 and #268 as one source-to-publication color contract. Remove ownership-coupled house-orange and cross-brand hue gates. Introduce reference-based formal identity colors and a shared per-theme interface cue model, then project measured role records into all generated and hosted guide formats without changing approved source colors or logo geometry.

## Technical Context

**Language/Version**: Python 3.8+ generator and validators, TypeScript/Next.js site, pinned Node 24.11.0 CI proof renderer

**Dependencies**: Existing coloraide WCAG 2.1 measurements, JSON Schema, Brand Canon and Interface Canon, kit/site generators

**Storage**: Source JSON and templates only; generated kits, PDF, and site export stay outside Git

**Testing**: Fail-first contract and fixture tests, production kit/glyph checks, generator parity, site lint/build/test, publication audit

**Target Platform**: Offline kit consumers, generated web/native adapters, static public brand site

**Constraints**: AA floor, approved path bytes, no silent recoloring, Python 3.8 compatibility, hidden Windows child processes

**Scale/Scope**: Eight production brands; one shared role resolver; two coordinated P1 issues

## Constitution Check

- **P1 source boundary**: PASS. Only source, tests, and Spec Kit artifacts are committed.
- **P2 geometry**: PASS. No logo path changes; source hash and path parity are checked.
- **P3 accessibility**: PASS. Hue restrictions are removed while measured AA pairing remains a gate.
- **P4 verification**: PASS. Production kit, glyph, regression fixture, PDF, and site checks are planned.
- **P5 site projection**: PASS. Hosted guidance reads generated kit role data.
- **P6 specification/release**: PASS. S053 artifacts accompany the PR; release publication is a later owner-directed action.

## Project Structure

```text
specs/053-color-roles-independent-palettes/{spec,plan,research,data-model,quickstart,tasks,evidence}.md
specs/053-color-roles-independent-palettes/contracts/color-roles.md
skill/references/{01-canon,canon.schema,03-interview,00-variance-contract}.json-or-md
brands/*/brand.json
skill/templates/{brand_contract,color_roles,interface_contract,enrich_brand,verify,gen_guidelines,gen_guide_pdf}.py
site/{lib/guidelines.ts,components/guidelines/color-reference.tsx}
skill/templates/test_*.py
```

**Structure Decision**: One resolver owns role references and measurements. Existing token names remain compatibility outputs. Brand source declares formal colors by reference; shared cue defaults live in canon data with optional explicit brand overrides.

## Design Sequence

1. Add fail-first tests for owned independent affiliation, third-party shared-color choice, sibling-hue acceptance, invalid role references, AA failures, and production parity.
2. Change affiliation, semantic color, schema, enrichment, verifier, and interface resolution together. Remove all mandatory sibling/orange hue limits and misleading legacy copy.
3. Add the reference-based role model and one resolver. Author role references in all eight brand sources without changing approved values or path data; update continuity hashes and canon compatibility as required.
4. Emit machine-readable role data and render the same model in hosted, portable, and PDF guidelines. Preserve existing web/native/registry color values while exposing role metadata.
5. Align the interview and approval packet with separate identity and interface roles, retaining #266's broader adaptive-brief redesign as later work.
6. Run full documented validation, record evidence, commit, push, open PR, and resolve CI and review comments under the authorized two-round limit. Stop for owner review and merge once every required check is green.

## Decision Log

2026-09-25: Keep `shruggietech-house` as an explicit historical shared-palette choice because renaming it would change shipped source semantics more broadly. Remove ownership and font coupling instead. The role model adds references, approved artwork combinations, and derived metadata, so no approved artwork or hex is rewritten. Brand Canon 1.5.0 and BrandBuilder 2.2.0 identify the compatible candidate; formal publication follows merge.

## Post-Design Constitution Check

All six gates remain PASS. The new role resolver fails on unresolved values or weak pairings before publication, and existing production identity values remain source authority.
