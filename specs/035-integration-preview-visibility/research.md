# Research: Integration Preview Visibility

## Decision: Resolve preview surfaces from explicit semantics or visible output

**Rationale**: Most generated icon records use `appearance: default`, which describes platform delivery but does not prove preview contrast. I Heart PR Tours' blue heart content measures about 2.05:1 on the current `#090909` default well and about 8.91:1 on `#F5F5F5`. The red content measures about 3.70:1 and 4.94:1 respectively, so a light well exposes both meaningful colors. Generator-time measurement produces deterministic portable and hosted metadata without changing asset bytes.

**Alternatives considered**: Retaining metadata-only selection, always using one well, adding brand-specific CSS, changing icon manifest semantics, browser-time canvas selection, and filtering or inverting imagery were rejected because they are incomplete, nondeterministic, nonportable, or identity-altering.

## Decision: Measure the exact embedded preview candidate at rendered scale

**Rationale**: A group can contain an SVG representative and related PNG deliveries. When appearance does not prove a surface, selecting the largest PNG in the same group for both measurement and display binds the recorded contrast to the exact base64 payload. Sampling at the 180 CSS pixel bound makes the result relevant to the rendered preview. Relative alpha thresholding ignores antialias fringe while supporting intentionally translucent art. Significant-pixel coverage and median contrast avoid the impossible rule that every antialiased or multicolor pixel must contrast with one well.

**Alternatives considered**: Average source metadata cannot see actual colors. Requiring every pixel to pass rejects valid antialiasing and multicolor icons. Measuring a sibling while displaying a different SVG weakens evidence. SVG-only output is rasterized solely for deterministic measurement while its original bytes remain the displayed payload. Fully transparent visuals still fail clearly; an intrinsically low-contrast approved asset receives its strongest supported well and recorded score so unrelated production kits remain buildable, while the affected guide's release gate still requires 3:1.

## Decision: Give nonvisual records format-aware resource semantics

**Rationale**: JSON, XML, ICO, and ICNS records are not failed images. A dedicated `Nonvisual resource` treatment with format and role communicates intent, retains grouped downloads, and can use an explicit 17:1 light text pair.

**Alternatives considered**: The current generic `Container asset` string conflates metadata and containers. Moving all resources into a new portable navigation section is broader than issue #202 requires.

## Decision: Extend existing generator and browser suites

**Rationale**: `test_pipeline.py` already governs delivery grouping, portal resource separation, catalog integrity, and portable HTML/CSS. `verify-site.mjs` already opens the copied portable guide and owns desktop, narrow, zoom, contrast, axe, and screenshot helpers. Extending these keeps regression ownership with existing interfaces.

**Alternatives considered**: A committed synthetic brand would violate Constitution P1. A separate browser package would duplicate infrastructure and expand maintenance.

## Baseline Findings

- `_asset_catalog()` places every non-Markdown delivery in an asset card, including JSON, XML, ICO, and ICNS groups.
- `_preview()` returns the same `Container asset` text for every non-PNG/SVG record.
- Surface selection recognizes only a small allowlist and sends `default` or absent appearance to `dark-well` without inspecting artwork.
- `.dark-well` sets `#090909` background but no foreground, so the I Heart PR Tours light-first guide inherits near-black `#111111` text at roughly 1.05:1.
- The hosted portal already separates nonvisual resources, but its visual surface metadata repeats the unchecked selection rule.
- A clean focused I Heart PR Tours baseline build completed with zero verifier problems and zero glyph failures after using the exact pinned Node renderer and the repository's shared dependency installation.
