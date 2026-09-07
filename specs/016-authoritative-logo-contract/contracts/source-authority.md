# Contract: Logo Source Authority

## Mode declaration

Every logo declares exactly one source mode. `constructed` means the Full and Reduced native elements in `logo.paths` are the approved geometry. `authoritative` means the Full and Reduced identities originate only from bound immutable input files.

No mode is inferred. Missing, unknown, or contradictory declarations block the build.

## Constructed mode

1. Full and Reduced contain non-empty native logo elements and continue through the glyph geometry gate.
2. `authoritative_input_ids` is absent.
3. No approved authoritative input claims the protected `mark` or `reduced-mark` role.
4. Existing path strings remain unchanged during S016 migration.

## Authoritative mode

1. `authoritative_input_ids` contains exactly `full` and `reduced`.
2. Full resolves to one approved `mark` input; Reduced resolves to one approved `reduced-mark` input.
3. Each variant contains exactly one image element whose source equals the bound input path.
4. No path, rectangle, or other independently constructed logo element may coexist with the bound image.
5. Bound input format is passive SVG or portable PNG, its SHA-256 matches measured bytes, and its approved operations cover every requested derivative transformation. JPEG and WebP may remain reference inputs but cannot bind a logo variant.
6. Raster placement preserves source aspect ratio. Passive SVG sources embed unchanged bytes.
7. `build/mk_paths.py` beneath the staged brand source is a contract error and is never executed.
8. Any later change to a binding, source hash, source artwork, mask method, or visible identity geometry requires a new explicit owner approval before generation.
9. A bound PNG uses non-interlaced 8-bit RGBA encoding so Core generation and verification can process it without Pillow. Its `approved_mask`, `mask_source_sha256`, `mask_approved_by`, and `mask_approved_on` fields are all required, the approval hash equals the current source hash, and the image element uses that approved mask.
10. The Full input always approves `place-in-lockup` because generated typography supplies a wordmark when no explicit wordmark path exists.

## Failure timing

All authority checks run in the brand-contract preflight before generated logo, guideline, icon, package, or site output is written. Errors name the brand, affected variant, source ID when available, and violated rule.
