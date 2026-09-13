# Data Model: CTA Role Consistency

## CTA semantic role

| Field | Meaning | Validation |
|-------|---------|------------|
| `action` | Owner-approved primary CTA fill | Six-digit uppercase hex; `#C5342C` for I Heart PR Tours |
| `foreground` | Legal normal-text color on the action fill | Derived, not transcribed; contrast is at least 4.5:1 |
| `default` | Primary CTA resting presentation | Uses the governed action and foreground pair |
| `hover` | Pointer-hover presentation | Retains the governed pair and adds a non-color cue |
| `active` | Pressed presentation | Retains the governed pair and adds a non-color cue |
| `focus-visible` | Keyboard-focus presentation | Dual-tone indicator visible against both the CTA and surrounding surface |

## Related color roles

| Role | I Heart PR Tours value | Relationship to CTA |
|------|------------------------|---------------------|
| Identity primary | Theme-dependent blue | Remains identity, selection, and structural emphasis; never substituted for CTA |
| Links | Accessible identity blue | Remains a text/navigation role |
| Focus token | Theme-dependent identity blue | Remains the general control focus token; CTA uses an explicit dual-tone indicator |
| Emphasis | `#A1CFF4` | Remains a separate attention role |
| Destructive | `#E9505F` dark / `#C0293A` light | Remains failure semantics and must not be labeled CTA |
| Chart series | Five derived values per theme | Excludes CTA red because CTA is an action role, not data series color |

## Generated token projection

| Token | Source | Consumers |
|-------|--------|-----------|
| `brand-cta` | `semantic_colors.action` | Next.js token output, portable guide, PDF guide |
| `brand-cta-foreground` | Measured legal foreground for `semantic_colors.action` | Next.js token output, portable primary buttons, PDF CTA specimens, verifier |
| `brand-cta-outline-foreground` | CTA red when it clears AA on the current background, otherwise the legal surface foreground | Next.js token output, portable secondary buttons, verifier |

The fill and filled-control foreground appear in light and dark blocks with the same hex pair. The outlined-control foreground adapts to the page surface because CTA red measures 5.38:1 on white but only 3.48:1 on the dark I Heart PR Tours background.

## Guide content projection

| Content | Source | Required projection |
|---------|--------|---------------------|
| Sharp-edge guidance | I Heart PR Tours `guide.sharp_edge` | Names `#C5342C` and primary CTA role |
| Palette introduction | I Heart PR Tours `guide.palette` | Explains action red without confusing it with destructive red |
| CTA swatch | Generated token pair | Label, hex, and primary CTA purpose |
| Semantic-use CTA row | Generated token pair | Action role, default fill, legal foreground |
| State specimen | Shared PDF template | Default, hover, active, and focus-visible guidance |
| Secondary specimen | Shared PDF template | CTA-red outline role distinct from the filled primary action |

## Language normalization boundary

Reader-facing guide prose uses American English. Internal code and data compatibility identifiers retain established spellings, including `colourway`, `colourways`, and function names such as `rasterise`, unless a separate migration explicitly changes those contracts.

## State transitions

```text
resting -> hover -> resting
resting -> active -> resting
resting -> focus-visible -> resting
hover -> active -> hover
```

All states retain the same measured fill/foreground pair. State changes are communicated through geometry, border, inset, and focus indicators.
