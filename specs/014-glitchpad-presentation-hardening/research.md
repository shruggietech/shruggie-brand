# Research: Glitchpad Pre-release Presentation Hardening

## Decision: Resolve a named showcase role from existing surfaces

**Rationale**: Glitchpad already governs `surfaces.card` as `#121416`. A `showcase_surface` role reference keeps the choice in the brand source, avoids a site-owned literal, and allows generated metadata to carry the resolved value. Making it optional preserves sibling-brand output.

**Alternatives considered**: Apply every brand's card surface globally, which would redesign siblings; hard-code Glitchpad or `#121416` in the site, which would violate generated-source authority; continue mixing accent into the panel, which preserves the reported defect.

## Decision: Center visible ink, not only the source canvas

**Rationale**: Transparent source canvases can be asymmetric. Cropping to non-transparent bounds before uniform scaling and centering produces measurable opposite margins for portrait, landscape, and offset source cases without modifying vector geometry.

**Alternatives considered**: Constrain only CSS, which would leave standalone export risks; center the original canvas, which fails asymmetric whitespace; normalize SVG view boxes or paths, which violates the identity-geometry rule.

## Decision: Keep role-specific occupancy

**Rationale**: Website slots, standalone masters, Android adaptive layers, legacy launchers, and store artwork have distinct purposes. The existing generator already assigns platform ratios. S014 reuses those values and derives the standalone master ratio from declared artwork and clear-space dimensions.

**Alternatives considered**: Apply one universal padding ratio, which would conflate website and platform safety; change already-correct native outputs, which would create speculative churn.

## Decision: Use CSS custom-property presence as the opt-in boundary

**Rationale**: Generated records can omit `showcaseSurface` for brands without an explicit role. Components set `--brand-showcase-surface` only when present, and CSS uses a fallback for all other brands. This keeps the behavior static, inspectable, and free of slug checks.

**Alternatives considered**: Add brand-specific CSS classes or slug conditions, which encode identity policy in the site; emit the value for every brand, which changes sibling presentation.

## Decision: Derive the showcase foreground at the generated-data boundary

**Rationale**: A governed surface may be light or dark. Site preparation compares WCAG contrast for black and white and emits the higher-contrast foreground beside the resolved surface, so configured cards remain readable without hard-coded dark-surface assumptions.

**Alternatives considered**: Restrict `showcase_surface` to dark colors, which needlessly narrows the reusable contract; force white in CSS, which fails on valid light surfaces; blend a muted foreground toward the surface, which can reduce contrast below the AA floor.

## Decision: Preserve current Glitchpad identity colors

**Rationale**: #146 is an explicit owner decision about color allocation. #144 and #145 can be completed by correcting containment and surfaces while retaining the existing role maps and protected paths.

**Alternatives considered**: Select the recommended #146 direction during S014, which would make an identity-defining decision outside this slice and prevent a clean unattended review boundary.
