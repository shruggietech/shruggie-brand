# Research: Dark Portfolio Cards

The IHPRT source selects `light.card` for its brand showcase, while its separate approved `surfaces.card` is `#101F2C`. Site preparation carries the light showcase to the homepage, and portfolio CSS applies white background and dark foreground. This is the regression shown in the owner's screenshot.

All current brands define a dark `surfaces.card`. Every published kit contains `{slug}-mark-reduced-color.svg`; IHPRT's approved reduced mark is its large heart. The current homepage instead loads `{slug}-mark-color.svg`, which for IHPRT is the full stacked lockup. The homepage is the sole consumer of the generated `icon` field.

Decision: publish an explicit, validated dark `portfolioSurface` from `surfaces.card` and the approved reduced icon for every brand. Keep `showcaseSurface`, `showcaseMode`, and light semantic tokens for brand pages and guides. Reject bad portfolio surfaces at the preparation boundary.
