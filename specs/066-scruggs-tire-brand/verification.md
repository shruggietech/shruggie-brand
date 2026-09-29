# Verification: S066 Planning and Gate 1 Candidate

**Date**: 2026-09-28

## Performed

- Confirmed the isolated worktree is based on `origin/main` and branch `codex/066-scruggs-tire-brand`; existing 063, 064, and 065 worktrees were left untouched.
- Ran the repository Spec Kit prerequisite check with `-RequireSpec -RequireTasks -IncludeTasks`; it identified this feature and its research, data model, contract, quickstart, and tasks artifacts.
- Compared the live website logo URL with the base ZIP image by byte count and SHA-256. Both are 25,908 bytes and hash to `b556a49f5c04f3afbe69114a4a7dbef4ef10ad01e2f3161849b652bca410621a`.
- Inspected PNG IHDR format fields for the Full logo, favicon, and 1200x630 image. The live-identical Full logo is non-interlaced RGBA8; the other two are indexed-color PNGs.
- Measured reference color ratios against white and recorded failures for ordinary text use in `research.md`.
- Ran `python scripts/check_markdown.py` through a redirected `CREATE_NO_WINDOW` process: passed.
- Checked all new Markdown files for UTF-8 BOM, CR line endings, replacement characters, and common mojibake markers: none found.
- Completed the cross-artifact and constitution review in `analysis.md`: no critical planning conflict.

## Not yet verified

No approved production mark, approval ledger, complete kit, generated PDF/raster set, `verify.py`, `validate_glyph.py`, aggregate build, site build, or hosted website result exists for Scruggs. Gate 1 and Gate 2 decisions remain pending. No public publication or pull request has been performed.

## 2026-09-29 candidate evidence

- Refreshed the [current client site](https://scruggstires.com/) and confirmed the family-owned Greer and Greenville positioning, since-1989 claim, services, and site-management credit remain present.
- Created passive authoritative Full and Reduced candidate SVG sources under ignored `dist/scruggs-gate1-candidate/`, embedding the two supplied PNG byte streams unchanged. Source SHA-256 values and native mask bounds/topology are recorded in [gate1-review.md](gate1-review.md) and the private packet.
- Validated the thirteen-topic private authoring brief with `skill/templates/authoring_brief.py`'s `validate_brief` function. Social copy and both creative gates remain unresolved.
- Ran `identity_continuity.generate_current_proofs` with the actual production `gen_logo.py` staging and `node-resvg` renderer. It produced all 32 expected Full/Reduced, size, and surface combinations.
- Repeated the production staging in a separate private root and required byte-identical SHA-256 for all 32 proof PNGs. `compare_proofs` reported 32 exact matches and emitted side-by-side, alpha-overlay, silhouette-XOR, and color-difference evidence for every coordinate.
- Recomputed sRGB role map, OKLCH triplets, and candidate contrast pairings. `validate_palette_qualification` accepted the role-bound evidence. Bright red fails ordinary text on white at 4.3904:1 and is explicitly excluded from that use; this is not a waiver.
- Candidate packet canonical content digest: `3c5771a96bb391db46b315ddccd292bfdaf0c2b53026a73dd4df1b0e79025faf`. Identity snapshot SHA-256: `5adfd4f346f8fe6092b4755408e9c3d957f088d938253cb89103479956c32979`. Both belong to a private, unapproved candidate.

## 2026-09-29 r2 correction and evidence

- The owner requested that the tire-only marks remain and the Full wording/background variants change. The r1 packet is superseded. The source PNG was confirmed to be RGBA8 with transparent pixels and original black wording; the r1 white plate was a wrapper addition.
- Tested a generative white-wording edit and rejected it after visual inspection showed changed tire and lettering geometry. The r2 passive SVG sources embed the exact original PNG bytes and use a source-alpha color filter for white wording on black, without redrawing contours.
- Rendered the clear, true-white, and true-black 512-pixel square previews with the production rasterizer. Read-only pixel checks found 25,858 retained red pixels and 5,440 black-wording pixels mapped to white, with zero opaque class errors. Transparent, white, and black corner pixels matched their expected values exactly.
- Rendered all 32 r2 production proofs and independently regenerated them in a separate root. Every proof hash matched, with comparison images for each coordinate. The Reduced source and all 16 Reduced proof hashes are identical to r1.
- Recomputed and validated the r2 palette qualification, including 21:1 wording contrast on the exact white and black square backgrounds. The new candidate packet canonical content digest is `cff80cc50c777cbe2335358f3c4d95e877c525a4414e05b7eb2710ff30c04ad0`; the governed identity snapshot is `7681816322f1f38a5b9f15fb3542a3b78481a3f6992d3e7dbf2b78c8b08d95c3`. Gate 1 approval remains pending.
