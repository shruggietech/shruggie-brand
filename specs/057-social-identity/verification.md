# S057 Verification Evidence

## Creative gates

- Gate 1, go-schedule current mark and paired lockups: the repository owner first requested changes, then explicitly clarified on 2026-09-26 to approve the current proof unchanged and push it. The proof uses the previous Reduced path data byte-for-byte as the current Full mark.
- Gate 2, eight social images: the repository owner approved all assembled images on 2026-09-26. Cueson, ESO Weave, and I Heart PR Tours Gate 2 ledgers bind the new exact derivative manifest SHA-256 values `b68a1d19e1e5033c353b23807b02fbcc9486d9dd74660d5d93be42d919297451`, `21dc36d5580ddbfa93164c28d8d2c9a16cc234be84066ff850eb540f0348e8bd`, and `02dba1d8bebc4e0b404e5c534d6d8dc5d0fbf91bbfb84f3e540506dd18d04b9b` respectively. Approved copy and image approvals are separate decisions.

## Source and continuity evidence

- The go-schedule Full source elements were copied from its existing Reduced path list without normalization. The source comparison test pins the prior Reduced path fingerprint and rejects divergence of the two current roles.
- I Heart PR Tours' supplied heart and lockup sources were unchanged. The current Node 24.11.0 proof renderer reproduced all 32 previously approved identity proof PNG SHA-256 values exactly. Its continuity record binds the current generator settings digest `0bfc34f22064da510b0e0fe8f4544f529595336097705896e18183a20d56f7e5` and source record digest `9ab5e552deba81f0f7725c8898235723f6ac1679ae8c39d2e0956e74fcff7ddb`.
- Core-tier vector generation for all eight brands passed. Each canonical social SVG embeds the exact generated horizontal color lockup, carries the approved slogan in its title, and has an identical legacy `social-preview` SVG alias with a provenance pointer.

## Build evidence to date

- All eight 1280 by 640 PNGs were generated in ignored `dist/`, each between 27 KB and 56 KB, below the 1 MB repository preview limit.
- The full eight-brand rebuild completed with zero verifier problems and zero glyph failures per kit, including I Heart PR Tours under its pinned Node 24.11.0 renderer. Its 32 historical proof digests also matched. The Cueson, ESO Weave, and I Heart PR Tours rebuilt `logos/approval.json` SHA-256 digests matched their exact Gate 2 source bindings.
- `skill/templates/test_pipeline.py` passed all 84 tests with the pinned renderer. `skill/templates/test_brand_contract.py` passed 73 tests, `scripts/test_prepare_site.py` passed 39, `scripts/test_release_contract.py` passed 27, `scripts/test_package_release.py` passed 11, and the glyphkit suite passed 34 checks.
- Site preparation consumed all eight verified kits and 15 reference documents. The direct MDX generation, TypeScript check, and Next.js static export passed (96 pages); 12 Node contract tests passed. The browser verifier checked 91 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The exported registry inventory validated all eight catalogs and local font bundles, and the README link audit found zero problems. The clean registry consumer test installed 24 pinned UI items, theme tokens, and local fonts, then built successfully.
- `scripts/package_release.py --version 2.4.0` and `scripts/release_contract.py verify` passed for the nine contractually distributed assets and validated notes. The source documentation audit, Markdown policy check, Python compilation, and `git diff --check` passed. All 49 changed text files were scanned as UTF-8 without BOM, with LF line endings and no replacement glyphs; a mojibake pattern search found none. A local pnpm dependency repair was needed after its fallback wrapper could not complete an initial install; direct locally installed commands succeeded afterward.

## Spec Kit analysis

Read-only cross-artifact analysis found no CRITICAL, HIGH, MEDIUM, or LOW inconsistency. All nine functional requirements and four buildable success criteria map to one or more of T001-T018; no task is unmapped, no unresolved placeholder remains, and all six constitution principles are represented in the plan and completion gates. The three core artifacts and required workflow files are present.

## Remaining gates

Publish the source-only pull request, then record CI and reviewer results before owner merge handoff.
