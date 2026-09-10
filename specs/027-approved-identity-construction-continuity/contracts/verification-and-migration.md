# Verification and Migration Contract

## Build-time continuity

Every production brand references one committed continuity record. Before derivative generation, source validation recomputes all contained source hashes, the identity snapshot, geometry and framing digests, palette digest, source classification, and construction provenance. Any mismatch stops the build.

`glyphkit-constructed` requires a construction helper whose parsed source imports glyphkit and obtains path-producing values from the approved primitive vocabulary. Literal path strings, custom path serializers, dynamic execution, and unrelated geometry engines fail. `legacy-constructed` is permitted only in a historical baseline and is never a template for new canonical approval. `authoritative` preserves and hashes the bound source inputs and forbids a construction helper.

## Proof comparison

The governed matrix covers each applicable full and reduced variant at 256, 64, 32, and 16 pixels on dark, light, black, and white treatments.

- Same renderer and settings: approval and production proof SHA-256 values must match exactly.
- Different documented renderer: source snapshot, geometry, topology, framing, roles, and intended colors remain exact. Hard-mask components and holes must match. Changed pixels outside a one-pixel antialias edge band may not exceed 0.5 percent of the union. Visible bounds may move by at most one pixel, centroid by at most one pixel, and interior Delta E 2000 may not exceed 1.0. Raw IoU is reported as supporting evidence only.
- Every comparison emits or references side-by-side, alpha-overlay, silhouette-XOR, and color-difference evidence.

## Palette qualification

Canonical approval is unavailable until all declared text and fill roles meet WCAG 2.1 AA, sibling-brand separation and semantic-role distinctions are measured, supported color-vision simulations preserve required distinctions, light and dark roles are valid, single-ink output is declared, and exact sRGB and measured OKLCH values are bound.

## Historical migration

S027 inventories all current production identities at the merged S026 revision. Each receives one source class and `historical-baseline` record derived from unchanged authoritative source. The record states approval completeness and explicitly denies retrospective approval. Migration must not change paths, role colors, palette values, framing, public eligibility, or generated visual output.

The migration audit records before-and-after digests and fails on any identity change. Cueson’s complete S026 approval evidence may be referenced, but S027 does not rewrite its approval or identity. Covarity is classified honestly as legacy constructed because its existing helper uses a custom arc serializer despite prior metadata claiming glyphkit; the source remains unchanged.

## Final verification

The full repository gate includes focused continuity and security tests, all existing generator tests, every production-kit build, zero verifier problems, zero glyph failures, release certification, site lint and export, browser route and WCAG checks, generated-agent synchronization, strict UTF-8/LF and mojibake checks, private-path scanning, and a clean tracked source boundary.
