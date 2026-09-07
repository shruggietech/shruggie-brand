# Contract: Square Identity Containment

## Inputs

- A rasterized identity source with at least one non-transparent pixel.
- A positive square output side.
- A role-specific occupancy ratio greater than zero and no greater than one.

## Behavior

1. Determine the source's non-transparent visible bounds.
2. Crop only transparent pixels surrounding those bounds.
3. Uniformly scale the visible content so its long edge is no larger than the rounded output-side occupancy.
4. Center the scaled visible content on both axes using integer offsets.
5. Preserve aspect ratio and pixel color values subject only to the selected resampling operation.

## Invariants

- Output width equals output height.
- No visible pixel lies outside the output.
- Opposite visible margins differ by at most one pixel.
- Canonical SVG path data is never rewritten.
- Platform callers retain their existing occupancy ratios and plate behavior.

## Failure behavior

- Empty visible content raises an explicit error.
- Invalid side or occupancy values raise an explicit error.
- Missing raster capability remains an explicit build-tier skip.
