# Implementation Plan: Current Go Schedule Identity and Brand Social Images

**Branch**: `codex/057-social-identity` | **Date**: 2026-09-25 | **Spec**: [spec.md](spec.md)

## Summary

Promote the exact existing go-schedule reduced path list to the primary mark role, and give every production brand an explicitly approved social copy record and dedicated social image delivery. The generator composes from current approved mark and wordmark assets, including I Heart PR Tours' unchanged supplied lockup. Brand landing pages publish kit image bytes for Open Graph and Twitter.

## Technical Context

**Language/Version**: Python 3.8 minimum; TypeScript/Next.js on Node 20 minimum.
**Primary Dependencies**: fontTools, Pillow, resvg, JSON Schema, Next.js.
**Storage**: Source JSON under `brands/`; ignored generated kits and site exports.
**Testing**: Python contracts and pipeline, complete `scripts/build_all.py`, site lint/build/test, release and publication audits.
**Target Platform**: Portable kits and static web export.
**Project Type**: Brand-kit compiler and static site.
**Performance Goals**: Eight 1280 by 640 social PNGs, each below 1 MB.
**Constraints**: Preserve shipped path bytes; zero verifier and glyph failures; WCAG 2.1 AA; no generated artifacts committed; two creative gates.
**Scale/Scope**: Eight production brands, go-schedule primary mark migration, old filename compatibility.

## Constitution Check

- **P1**: Commit sources only; keep build output ignored.
- **P2**: Deep-copy preexisting reduced path elements to current primary and record source-bound proof; never redraw.
- **P3**: Check rendered text and declared color AA at use size, plus crop readability.
- **P4**: Complete kit, glyph, continuity, site, and publication gates before PR readiness; owner reviews creative proofs.
- **P5**: Brand-page social PNGs come from verified kit bytes; other route cards remain site generated.
- **P6**: Keep Spec Kit artifacts, evidence, versions, implementation, and changelog synchronized.

The design meets all six principles. Recheck after implementation and creative gates.

## Design Decisions

1. A governed `social_copy` field contains exact slogan, layout, optional description lines, and approval evidence. `brand_idea` and descriptor remain separate editorial fields.
2. Canonical outputs use `social-image` names and kind. Legacy `social-preview` direct files remain compatibility aliases with explicit provenance. Downloads place the canonical image in a Social images family.
3. I Heart PR Tours uses its unchanged approved supplied horizontal color lockup, since its Gate 1 scope excludes a wordmark-only derivative.
4. Brand landing pages retain stable `/social/guidelines-<slug>.png` URLs, populated from verified kit PNG bytes. Other routes retain generated cards.
5. Source or rendered composition changes invalidate historical Gate 2 digests. Capture new owner review evidence before rebinding approval.
6. Go-schedule continuity remains a historical constructed baseline with a new current snapshot and explicit owner decision; it does not claim retrospective canonical approval.

## Project Structure

```text
brands/<slug>/brand.json                     # governed identity and social copy
brands/go-schedule/identity-continuity.json  # current path-role snapshot
skill/references/canon.schema.json           # source contract
skill/templates/brand_contract.py            # semantic validation and binding
skill/templates/gen_logo.py                  # social image and provenance
skill/templates/gen_guidelines.py            # download classification
skill/templates/verify.py                    # artifact verification
scripts/prepare_site.py                      # verified kit to site image
skill/templates/test_*.py                    # contract and pipeline tests
scripts/test_prepare_site.py                 # site byte binding
specs/057-social-identity/                   # decisions and evidence
```

## Delivery Sequence

Write contract tests, promote go-schedule source roles and continuity, add social source records, implement generated social family and compatibility aliases, bind site metadata bytes, update usage and versions, render Gate 1 and Gate 2 proofs, obtain owner approvals, run full local validation, commit, push, open PR, resolve CI and two review rounds at most, then hand off for merge.

## Complexity Tracking

No constitution exception is needed.
