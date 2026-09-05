# S007 Verification Evidence

## Contract and focused regressions

- `test_brand_contract.py`: 13 tests passed, including fail-closed affiliation, independent semantic colors, third-party output scanning, deterministic raster evidence, stale approvals, passive-SVG restrictions, path and role collisions, imported-image transformation approval, complete fixed-font metadata failures, variable and corrupt font rejection, and atomic ingestion boundaries.
- `test_pipeline.py`: 21 tests passed, including the isolated third-party fixed-font full pipeline, no false ownership, no inherited house orange, no font-network access, supplied SVG wordmark preservation, optional pagination dependency handling, renderer failure handling, and hidden Windows processes.
- `test_prepare_site.py`: 9 tests passed, including explicit public/private showcase behavior, stale-public cleanup, and fail-closed missing output.
- `test_release_contract.py`: 9 tests passed.
- `check_markdown.py`: passed.
- Python compilation passed and production discovery returned exactly `covarity`, `fragcap`, `glitchpad`, `go-schedule`, and `shruggietech`.

## Full production, release, and site gates

- The full Chromium-enabled build completed for all five production brands. Each contract preflight, glyph validation, kit verification, affiliation scan, image QC, PDF QC, and pagination gate reported zero failures.
- Manual review covered all five logo sheets, all five seven-page PDF contact sheets, all five guideline pages at desktop and mobile widths, and the four self-contained product UI kits. No S007 visual regression was found.
- `package_release.py --version 1.1.2` produced seven expected assets. Release notes generation and `release_contract.py verify` passed for all seven assets.
- The static site typecheck and Next.js production build passed. Browser verification covered 26 routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- `sync_agents_md.py skill` reported the generated `skill/AGENTS.md` unchanged.

## Identity, encoding, and scope integrity

- The four recorded ShruggieTech source hashes remain `d500c3eadf049d36ce094bf7e35e37902a4ab49a66bcd6a9b40696961208a5c8`, `dc84170f164277ee4289240405aec1b35170937da0d4afe8f096ecd6d893c324`, `969687b1ceafcb0cef296d1f68bc8767748752c21ab4394bcee6a541f529a18a`, and `514b911167c364fe40535f6cae8866e60c793bee3af46447787e5f273a3f6973`.
- The production brand-definition diff adds explicit affiliation, typography mode, authoritative-input evidence, and palette approvals without changing existing logo path data. The two Space Grotesk WOFF2 files were intentionally regenerated from the repository TTF sources because their prior internal family metadata incorrectly identified them as `Space Grotesk Light`.
- Changed text files pass UTF-8 without BOM, LF-only, mojibake, Markdown, and `git diff --check` inspections. Generated `dist/`, `release/`, site output, local virtual environments, and browser caches remain ignored.
- S007 contains no Android, Apple, macOS, Windows, store-listing, adaptive-icon, or application-icon generation. Issue #106 remains reserved for S008.

## Analysis findings and explicit boundary

- The Spec Kit consistency pass found and corrected two material omissions before completion: independent inheritance now requires brand-specific emphasis and action colors, and negative tests now cover every supplied-SVG and fixed-font failure named by the tasks.
- The site verifier previously rejected the valid owned-child endorsement on every guideline page. It now rejects self-endorsement on the ShruggieTech parent while the third-party pipeline scan enforces the broader client-safety contract.
- The legacy ShruggieTech marketing UI fixture remains dependent on executable React, ReactDOM, Babel, and Lucide CDN resources and therefore produces a blank offline QC sheet. The fixture is byte-for-byte unchanged from `main`, is not consumed by the public site, and was not executed against local project files during this audit. Converting that unrelated fixture to a self-contained implementation is outside issues #104 and #105 and was not folded into S007.
