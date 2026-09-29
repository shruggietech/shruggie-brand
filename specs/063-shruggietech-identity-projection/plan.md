# Implementation Plan: ShruggieTech Identity Projection

**Branch**: `codex/063-shruggietech-identity-projection` | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

**Input**: One end-to-end source correction for #294, #293, and #295, with existing creative reviews preserved.

## Summary

Use the reduced face as the only ShruggieTech standalone square source, make its SVG and raster projections square and vividly green on black, and retain the full arms mark for paired and approved contextual uses. Correct the canonical slogan and project it through the social image and site without changing introductory copy. Audit every generated role, test source and rendered output, obtain applicable approvals, then run the full eight-kit and site validation.

## Technical Context

**Language/Version**: Python 3.8 minimum for BrandBuilder, TypeScript/Next.js with Node.js 20 minimum for the site

**Primary Dependencies**: Pillow, SVG rasterizer, Poppler, ImageMagick, bundled fonts, existing brand contract and iconkit

**Storage**: Governed JSON and Markdown source; generated kit, site, PDF, PNG, and review proofs in ignored `dist/`

**Testing**: Python unittest contract, icon, pipeline and site-preparation tests; full `scripts/build_all.py`; site lint/build/test; rendered proof inspection

**Target Platform**: Browser, PWA, Android, iOS, macOS, Windows, PDF, portable guide, and hosted site

**Project Type**: Brand kit generator and static site

**Performance Goals**: No added runtime service or network dependency

**Constraints**: Source artwork digests unchanged; WCAG 2.1 AA; no generated output in Git; exact existing Gate 1 and Gate 2 decisions; source-bound provenance

**Scale/Scope**: One production brand, three linked issues, eight production-kit regression gate, plus an exact-proof continuity compatibility correction for the shared generator

## Constitution Check

- **P1**: Only source, code, tests, and Spec Kit evidence enter Git. Proofs stay in ignored output.
- **P2**: Paid source bytes remain unchanged. Any changed mask derivation needs existing source approval.
- **P3**: Contrast, rendered sizes, responsive layout, text alternatives, and focus behavior meet AA without waiver.
- **P4**: All eight kits rebuild with zero `verify.py` problems and zero `validate_glyph.py` failures. Exact social-image approval matches final bytes.
- **P5**: The homepage consumes verified kit output, not a site-authored substitute.
- **P6**: S063 follows Spec Kit; no tag or release is part of this slice.
- **P7**: Approved i-heart-pr-tours identity proofs remain byte-exact when the shared generator changes. Renderer-family drift is rejected; settings drift is accepted only with the complete exact approved matrix and comparison evidence.

**Post-design check**: Both contracts below retain every principle. Gate 1 and Gate 2 may require owner decisions after concrete candidate proofs; neither is inferred from kickoff.

**Decision outcome**: The owner approved the revised Gate 1 candidate and the exact assembled Gate 2 social image on 2026-09-28. The first Gate 1 proof was rejected for insufficient side padding; the accepted square window is `[238.5, 30, 440, 440]`. Exact hashes and proof paths are in [verification.md](verification.md).

## Project Structure

```text
specs/063-shruggietech-identity-projection/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  verification.md
  contracts/square-mark-roles.md  contracts/message-and-approval.md
  checklists/requirements.md  checklists/identity-projection.md
brands/shruggietech/brand.json  brands/shruggietech/README.md
skill/templates/gen_logo.py  skill/templates/iconkit.py  skill/templates/brand_contract.py
skill/templates/verify.py  skill/templates/identity_continuity.py  skill/templates/test_*.py
scripts/prepare_site.py  scripts/test_prepare_site.py
site/components/brand-portfolio.tsx  site/app/globals.css
```

**Structure Decision**: Keep the existing generator and kit contract. Make role choices in `brand.json`, reusable transformations in generator templates, and site projection from the generated reduced mark. No second asset store or site-only mark.

## Execution Order and Decisions

1. Inventory square, paired, social, guide, site, and metadata consumers. Map all three issues to generated evidence.
2. Add failing role and exact-copy regression tests before generator changes.
3. Make the reduced face output square-proportioned, qualify a vivid source-bound mask derivation, select it for every standalone square delivery, and correct manifest labels. Preserve full arms compositions.
4. Correct slogan source and approval history, preserve the introductory phrase's role, and generate a provisional assembled social image.
5. Present exact changed derivation proof for the existing Gate 1 decision if required, and the assembled social image for Gate 2. Record only actual owner decisions; pending blocks final compilation and PR publication.
6. Run full documented validation and inspect generated proofs, record acceptance evidence, commit, push, and open the PR. Monitor required CI and external reviews, address actionable comments, and request at most one additional Codex review round.
