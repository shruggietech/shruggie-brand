# Data Model: Glitchpad Pre-release Presentation Hardening

## Showcase surface reference

- **Source field**: Optional `showcase_surface` string on a production brand.
- **Reference target**: One existing key in the same brand's `surfaces` mapping.
- **Resolved value**: A six-digit hexadecimal color emitted as optional `showcaseSurface` generated site metadata.
- **Absent state**: No generated override. Existing site presentation remains active.
- **Validation**: The field must be a non-empty role name, the role must exist, and the resolved value must be a six-digit hexadecimal color.

## Visible bounds

- **Source**: The alpha-channel bounding box of a rasterized identity asset.
- **Fields**: left, top, right, bottom, width, and height in integer pixels.
- **Validation**: Bounds must be non-empty and contained by the source image.

## Square composition

- **Fields**: output side, occupancy ratio, maximum visible long edge, scaled visible dimensions, and integer placement offset.
- **Validation**: Output side is positive, occupancy is greater than zero and no greater than one, both scaled dimensions are positive, and the placed bounds remain within the square.
- **Invariant**: Opposite margins differ by at most one pixel after integer rounding.

## Verification disposition

- **Identity**: Generated asset path or public presentation name.
- **State**: `corrected`, `verified-unchanged`, or `skipped`.
- **Evidence**: Dimensions, visible or content bounds where applicable, occupancy, transparency or background expectation, and applicable platform role.
- **Lifecycle**: Discovered, measured, classified, then recorded in S014 evidence.
