# Verification: Local Companion Brand Kit

## 2026-09-28, creative approvals and source binding

- The owner approved the exact calm-orbit Full and Reduced production masters and 32 proofs at Gate 1, then approved the corrected Node v24.11.0 production binding without changes to the approved paths or proof PNGs.
- The owner approved the revised social text and layout, selected app parity for amber, pink, green, and blue functional cues, and approved the complete private Gate 2 packet with SHA-256 `2ab78758ea45a23d466207beb6536ad01e99af88324de2d4b54c513fda8e3470`. On 2026-09-29 the owner approved the corrected Gate 2 binding packet SHA-256 `4f668c3e328fb84593812374791f7659156cd851785b62e3c02cd6e8409bf71c`; only the Web forced-colors badge and toast CSS derivative changed, while all approved visual and social hashes stayed the same.
- Final source regeneration matches the approved social SVG SHA-256 `c2ea7dd5ac51f303e336318efc665ec3b331400a60848130b0ee10d71850514c`, social PNG SHA-256 `7c6fe6af35e16f9faaf1c1ccaa0c3cbea567358840412012ccfd9735b746a06a`, and production `logos/approval.json` SHA-256 `016aa3ec4eaf1ac96d16534f55683d53cb54bca4ca89956992f9f9ac0ecf490d`.

## 2026-09-28, local validation

- The private `authoring_brief.py` Gate 2 validator accepted the complete packet and every required reviewed asset hash.
- `scripts/export_approved_identity_proofs.py` regenerated all 32 exact approved proofs with the CI-pinned Node v24.11.0 renderer.
- `scripts/build_all.py local-companion` completed with zero `verify.py` problems, zero glyph failures (one documented Full 16-pixel warning; Reduced is used at and below 32 pixels), zero image QC problems, and zero PDF pagination splits.
- All 13 Local Companion QC images were visually inspected, including the contact sheet, logo sheet, desktop and 390-pixel guidelines, browser specimen, and generated component/template pages.
- `python -m unittest test_brand_contract test_color_roles test_pipeline` passed 182 generator tests. Focused release, identity continuity, publication workflow, proof export, package, site-preparation, and documentation tests passed after correcting production-brand fixture counts from eight to nine.
- `scripts/audit_identity_continuity.py --check` reports zero problems. `scripts/audit_public_documentation.py --sources` reports zero problems. `scripts/check_markdown.py` passes.

## Remaining publication gates

- Complete the full production build and site/release validation on this branch, then confirm required CI on the reviewed source commit.
- Merge the reviewed change, tag `v2.8.0` from the merged main commit, and verify the exact tag-built release and live `brand.shruggie.tech` route against published checksums.
