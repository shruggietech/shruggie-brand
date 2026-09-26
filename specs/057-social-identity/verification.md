# S057 Verification Evidence

## Creative gates

- Gate 1, go-schedule current mark and paired lockups: the repository owner first requested changes, then explicitly clarified on 2026-09-26 to approve the current proof unchanged and push it. The proof uses the previous Reduced path data byte-for-byte as the current Full mark.
- Gate 2, eight social images: the repository owner approved all assembled images on 2026-09-26. Every brand now has a source-bound `social_image_approval` for its assembled SVG and PNG. Cueson, ESO Weave, and I Heart PR Tours additionally retain their full Gate 2 derivative manifest SHA-256 values `b68a1d19e1e5033c353b23807b02fbcc9486d9dd74660d5d93be42d919297451`, `21dc36d5580ddbfa93164c28d8d2c9a16cc234be84066ff850eb540f0348e8bd`, and `02dba1d8bebc4e0b404e5c534d6d8dc5d0fbf91bbfb84f3e540506dd18d04b9b` respectively. Approved copy and image approvals are separate decisions.

## Source and continuity evidence

- The go-schedule Full source elements were copied from its existing Reduced path list without normalization. The source comparison test pins the prior Reduced path fingerprint and rejects divergence of the two current roles.
- I Heart PR Tours' supplied heart and lockup sources were unchanged. The current Node 24.11.0 proof renderer reproduced all 32 previously approved identity proof PNG SHA-256 values exactly after both review corrections. The second correction binds the same approved proof set to generator settings digest `e4116cff4a8eb177248b7533ac2f13935111de1506cff0e2c7d2425b95938a36` and source record digest `8db6682819514194b35241379181f1b2f6b0fd670a1da798dbed59e82b381f7d`.
- The go-schedule `current_mark_approval` binds the owner's Gate 1 decision to identity snapshot SHA-256 `a93ab69568c9b2b1b592af37501a4d0c9341d2b6a0ae218b302cd04a9c7106ee`. The historical baseline still records the earlier migration without retrospective canonical approval.
- Core-tier vector generation for all eight brands passed. Each canonical social SVG embeds the exact generated horizontal color lockup, carries the approved slogan in its title, and has an identical legacy `social-preview` SVG alias with a provenance pointer.

## Build evidence to date

- All eight 1280 by 640 PNGs were generated in ignored `dist/`, each between 27 KB and 56 KB, below the 1 MB repository preview limit.
- The full eight-brand rebuild completed with zero verifier problems and zero glyph failures per kit, including I Heart PR Tours under its pinned Node 24.11.0 renderer. Its 32 historical proof digests also matched. The Cueson, ESO Weave, and I Heart PR Tours rebuilt `logos/approval.json` SHA-256 digests matched their exact Gate 2 source bindings.
- After the review correction, `skill/templates/test_pipeline.py` passed all 84 tests with the pinned renderer (two expected capability skips). The corrected approval contract passed 76 tests and site preparation passed 39. Release contract passed 27, release packaging passed 11, and glyphkit passed 34 checks. The final eight-kit production rebuild reported zero problems and zero glyph failures.
- Site preparation consumed all eight verified kits and 15 reference documents. The direct MDX generation, TypeScript check, and Next.js static export passed (96 pages); 12 Node contract tests passed. The browser verifier checked 91 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The exported registry inventory validated all eight catalogs and local font bundles, and the README link audit found zero problems. The clean registry consumer test installed 24 pinned UI items, theme tokens, and local fonts, then built successfully.
- `scripts/package_release.py --version 2.4.0` and `scripts/release_contract.py verify` passed again for the nine contractually distributed assets and validated notes. The final site type-check and static export passed for 96 pages; 12 Node contract tests passed. The publication-artifact audit passed against a clean eight-kit copy because the local ignored `dist/` also contains earlier tools and test artifacts. The source documentation audit, Markdown policy check, Python compilation, and `git diff --check` passed. The initial 49 changed text files and 27 review-correction files were scanned as UTF-8 without BOM, with LF line endings and no replacement glyphs; a mojibake pattern search found none. A local pnpm dependency repair was needed after its fallback wrapper could not complete an initial install; direct locally installed commands succeeded afterward.

## Spec Kit analysis

Read-only cross-artifact analysis found no CRITICAL, HIGH, MEDIUM, or LOW inconsistency. All nine functional requirements and four buildable success criteria map to one or more of T001-T021; no task is unmapped, no unresolved placeholder remains, and all six constitution principles are represented in the plan and completion gates. The three core artifacts and required workflow files are present.

## Pull request review

- PR #287 first Codex code review on `0457014` raised three findings: missing per-brand assembled-image binding, missing source-bound record for the new go-schedule current approval, and potential clipping of four description lines. T019-T021 address these findings. The exact social approval check permits an explicit raster skip only in the core tier.
- The initial Python 3.8 CI job failed because its core-tier vector test attempted to rasterize an I Heart PR Tours supplied SVG without the optional renderer. That subtest now records an explicit skip when the renderer is absent; the full verified-build job still exercises the supplied source with pinned resvg.
- The single authorized second Codex review on `9825d95` raised three new findings: a semantic waiver could accept changed PNG bytes, a provisional generator mode could skip continuity while emitting publishable assets, and unsupported font glyphs could silently disappear from approved copy. T022-T024 remove the waiver and provisional mode, pin social PNG rendering, and reject absent glyphs. The second correction passed all 85 pipeline tests, 76 brand-contract tests, and the full eight-kit rebuild with zero reported problems. No further review request will be made.

## Remaining gates

Push the reviewed corrections, request one additional Codex code and security review round, then record final CI and reviewer results before owner merge handoff.
