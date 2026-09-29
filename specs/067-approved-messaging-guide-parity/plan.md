# Implementation Plan: Approved Messaging and Guide Parity

**Branch**: `codex/067-approved-messaging-guide-parity` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

## Summary

Introduce a source-bound messaging record with independent approval and intended-use states. Audit all eleven brands, keep unapproved legacy wording visible in the migration record, and project only approved values into the PDF, portable guide, hosted guide, social data, and consumer contract. Remove guide-only message overrides and generated brand claims. Verify exact roles, values, and asset bindings across the outputs.

## Technical Context

**Language/Version**: Python 3.8-compatible generator and validator, TypeScript/React site, Node 24.11.0 and approved Node 26.5.0 identity proof routes.

**Primary Dependencies**: Existing `brand_contract.py`, `authoring_brief.py`, JSON Schema, Chromium PDF export, existing generated portal and Next site.

**Storage**: `brands/*/brand.json` source and `specs/067-approved-messaging-guide-parity/` migration evidence; generated kits stay under ignored `dist/`.

**Testing**: Focused Python contract and projection tests, extracted PDF text checks, all production `verify.py` and `validate_glyph.py` gates, site and publication checks from current CI.

**Target Platform**: Portable kit and hosted brand portal.

**Project Type**: Brand source compiler and static site.

**Performance Goals**: Preserve current CI coverage and the S066 split-job improvement; avoid adding a serial eleven-kit rebuild inside an existing verification job.

**Constraints**: Source-only commits, unchanged approved logo geometry and social-image bytes, WCAG 2.1 AA, UTF-8 LF, no new creative gate.

**Scale/Scope**: Eleven production brands, two linked issues, all guide and consumer projections. #298 redesign and #299 navigation are follow-on work.

## Constitution Check

- Source and artifact boundary: pass by editing `brands/`, `skill/`, `site/`, `specs/`, and documentation only; `dist/` remains ignored.
- Identity continuity: pass by leaving logo source paths and approved social images unchanged.
- Accessibility: retain WCAG 2.1 AA in PDF, portable, and hosted output.
- Quality: require zero kit and glyph failures, full rebuild after shared generator changes, content and layout assertions instead of PDF byte equality.
- Site authority: hosted pages consume generated kit portal and source-bound metadata.
- Workflow: this spec, plan, tasks, analysis, evidence, and code remain synchronized.

## Design Decisions

1. Use `messaging` in each `brand.json` for independent role decisions. An approved decision has an exact `text`, `uses`, `source`, `approved_by`, and `approved_on`; an absent role has no text; an unresolved role cannot publish its candidate. Keep `social_copy` as the already-approved social composition and require exact equality if a reusable approved slogan is also permitted for social use.
2. Migrate only owner-supported reusable messages. #295 authorizes ShruggieTech's exact slogan. Six Gate 2 ledgers also approve exact descriptors for showcase-card and public-metadata surfaces; preserve those as `short_description` with site-metadata use only. Other descriptors and visual-guide use remain unresolved. An existing social slogan stays in its original role until its reuse is approved.
3. Existing `guide` is a legacy store with some approved visual instructions and some guide-only claims. Move reusable, source-bound visual instructions into canonical `guidance` and put unsubstantiated or conflicting claims in the migration inventory. Keep `guidance.surface_mode` as presentation configuration. A generator must never treat legacy `guide.idea` or `guide.descriptor` as authoritative copy.
4. A common helper returns only approved text for a named role and surface; all guide generators and site portal use it. Omit absent or unresolved roles cleanly. Shared explanatory instructions have one maintained source in the shipped reference or template instead of per-guide defaults.
5. Verify actual HTML/PDF text and labels and kit asset paths/digests. Avoid PDF byte comparison. Use focused regression fixtures for Fragcap, Go Schedule, Glitchpad, and ShruggieTech plus sparse/rich/conflicting synthetic briefs in temporary test directories.
6. Four approved-canonical continuity records include `brand.json` in their source-file inventory. Refresh only that file's byte count and SHA-256 plus the record checksum after the copy migration, assert the identity snapshot and canonical source binding are unchanged, and leave the original Gate 1/Gate 2 approval facts and proof hashes untouched. Historical records have no `brand.json` source-file entry and need no record edit.
7. Version the required `guide` to `guidance` source change as Brand Canon 2.0.0 and the compiler/portable output change as BrandBuilder 3.0.0. Increment each unchanged-identity brand by a patch version, update compatibility edges, and regenerate exact approved portable proofs for continuity-bound brands. Python 3.8/3.9 verification reports a named PDF messaging skip when PyMuPDF is unavailable while retaining all HTML and portal checks; supported Python versions still check extracted PDF text.

## Project Structure

```text
specs/067-approved-messaging-guide-parity/  # Spec Kit artifacts, inventory, parity map, verification
brands/*/brand.json                          # Canonical approved message decisions and source guidance
skill/references/                             # Schema, interview, anatomy, shared guide guidance
skill/templates/                              # Brief validation, generators, verifier, tests
site/components/guidelines/                   # Hosted projection without copy fallback
site/lib/guidelines.ts                        # Generated portal types
dist/                                         # Ignored generated verification output
```

## Verification and Handoff

Write failing focused contract/projection tests before generator changes. Run local contract and site checks, rebuild and verify all eleven kits using each brand's approved renderer, run all documented site/publication checks, and record exact evidence in `verification.md`. Commit only sources and evidence, push, open the official PR, handle first and at most one requested second Codex review round plus security review, wait for green required CI, then hand off for owner merge.
