# Verification: Local Companion Brand Kit

## 2026-09-28, creative approvals and source binding

- The owner approved the exact calm-orbit Full and Reduced production masters and 32 proofs at Gate 1, then approved the corrected Node v24.11.0 production binding without changes to the approved paths or proof PNGs.
- The owner approved the revised social text and layout, selected app parity for amber, pink, green, and blue functional cues, and approved the complete private Gate 2 packet with SHA-256 `2ab78758ea45a23d466207beb6536ad01e99af88324de2d4b54c513fda8e3470`.

## 2026-09-28, local validation

- The private `authoring_brief.py` Gate 2 validator accepted the complete packet and every required reviewed asset hash.
- `scripts/export_approved_identity_proofs.py` regenerated all 32 exact approved proofs with the CI-pinned Node v24.11.0 renderer.
- `scripts/build_all.py local-companion` completed with zero `verify.py` problems, zero glyph failures (one documented Full 16-pixel warning; Reduced is used at and below 32 pixels), zero image QC problems, and zero PDF pagination splits.
- All 13 Local Companion QC images were visually inspected, including the contact sheet, logo sheet, desktop and 390-pixel guidelines, browser specimen, and generated component/template pages.
- `python -m unittest test_brand_contract test_color_roles test_pipeline` passed 182 generator tests. Focused release, identity continuity, publication workflow, proof export, package, site-preparation, and documentation tests passed after correcting production-brand fixture counts from eight to nine.
- `scripts/audit_identity_continuity.py --check` reports zero problems. `scripts/audit_public_documentation.py --sources` reports zero problems. `scripts/check_markdown.py` passes.

## 2026-09-29, corrected binding and production validation

- The owner approved the corrected Gate 2 binding packet SHA-256 `4f668c3e328fb84593812374791f7659156cd851785b62e3c02cd6e8409bf71c` (review ZIP SHA-256 `ba263fa36856dc29d80eab790d26c91fe327a4631ab3c991dd649aee95cd26c2`). Only generated Web forced-colors badge and toast CSS changed. `authoring_brief.py` accepted the corrected private packet and current source binding.
- The pinned Node v24.11.0 `scripts/build_all.py` run built all nine kits with zero reported problems. Local Companion has zero glyph failures, zero image QC problems, and zero PDF pagination splits. Final generated hashes match the reviewed `web/components.css` (`e35f980c85fe49298bfac26811f80f09acb064f708ccc2a0f1da1b2c0c07526d`), social SVG (`c2ea7dd5ac51f303e336318efc665ec3b331400a60848130b0ee10d71850514c`), social PNG (`7c6fe6af35e16f9faaf1c1ccaa0c3cbea567358840412012ccfd9735b746a06a`), and `logos/approval.json` (`016aa3ec4eaf1ac96d16534f55683d53cb54bca4ca89956992f9f9ac0ecf490d`).
- Site lint and static build passed. `pnpm --dir site test` verified 103 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations; the Local Companion forced-colors specimen was visually inspected. Registry delivery installed 24 UI items in a clean consumer. Public documentation, README links, and publication artifact audits passed; the artifact audit counted nine brands, nine kit markers, nine site markers, nine packages, and 2,161 public files.
- The 2.8.0 release contract verified ten assets. The Local Companion site download and release archive share SHA-256 `12d3dcdd936e18f2badf0145ed46165ae1a901bc9e573e8d74a2d289a695f5ea`. The final eight changed source files, 182 kit text files, and 183 archive text entries passed UTF-8, LF, and mojibake checks.
- Codex review found that a rewritten historical continuity record could conceal palette or geometry drift during a read-only audit. The audit now compares historical brands with a pinned migration identity snapshot; Go Schedule uses its separately owner-approved S057 snapshot. Six focused audit tests pass, including forged Cueson palette and geometry records, and `audit_identity_continuity.py --check` reports zero problems.
- After S063 merged to main, the Local Companion build again reported zero problems. Its Web CSS, approval manifest, and social SVG and PNG retained the exact Gate 2 hashes above, and the canonical-host export regenerated all 32 exact approved proof PNGs. The read-only audit now also pins S063's owner-approved ShruggieTech snapshot. Seven focused audit tests pass, including later ShruggieTech framing drift. CI audit jobs fetch the pinned history, and the synthetic record test uses Python 3.8-compatible file writes.

## Remaining publication gates

- Confirm required CI on the reviewed source commit, merge the change, tag `v2.8.0` from the merged main commit, and verify the tag-built release and live `brand.shruggie.tech` route against published checksums.
