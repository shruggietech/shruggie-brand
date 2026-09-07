# Contract: Logo Derivative Provenance

## Index

Each generated kit contains `logos/provenance.json`. It records every generated file under `logos/svg/` and `logos/png/`, including wordmark-only outputs, and contains no records for absent files.

Records are deterministic, unique by output path, sorted lexically, and derived from the validated source contract rather than copied from existing output.

## Authoritative SVG metadata

Every authoritative mark and lockup SVG root carries:

- `data-logo-source-mode="authoritative"`
- `data-logo-variant="full"` or `data-logo-variant="reduced"`
- `data-authoritative-input-id="..."`
- `data-authoritative-source-sha256="..."`

The values equal the provenance index and current source record. Wordmark-only SVGs state constructed typography and do not claim an authoritative mark source.

## Allowed lineage

- Mark colorways use the bound Full or Reduced source and record `recolor-mask` for raster recolors or `embed-unchanged` for passive SVG.
- A differing output placement records `resize` only when the source approves it.
- Horizontal and stacked lockups additionally record `place-in-lockup` against the Full source.
- PNGs inherit the same lineage as the SVG master from which they are rasterized.
- Downstream icon manifests name a verified logo master. They cannot nominate an unindexed or stale master.

## Verification

Verification independently derives the expected inventory and rejects:

1. Missing, extra, duplicate, or unsorted records.
2. Missing or conflicting SVG root metadata.
3. Unknown or undeclared transformations.
4. Source ID, path, role, approval, or hash drift.
5. Aspect-ratio distortion, changed image placement, hidden identity content, unsupported transforms, or later SVG content that obscures opaque identity pixels.
6. Raster-mask topology that differs from the hash-bound owner-approved alpha or luminance source after deterministic nearest-neighbor normalization.
7. Any generated logo PNG whose pixels differ from an independent rendering of its verified SVG master.
8. Any platform PNG, favicon SVG payload, ICO frame, or ICNS frame whose pixels or embedded bytes differ from the declared verified Full, Reduced, or monochrome master.
9. Downstream references to a logo master absent from the validated index.

Generated PDF or PNG byte identity is never used as the correctness gate.
