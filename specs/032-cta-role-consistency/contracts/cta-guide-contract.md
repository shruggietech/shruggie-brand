# Contract: Generated CTA Guidance

## Source contract

- I Heart PR Tours declares `semantic_colors.action` as exactly `#C5342C`.
- The shared generator derives the legal action foreground by measurement.
- The general `primary` identity token remains independent from the CTA token.
- No generated artifact under `dist/` is a source of truth.

## Token contract

Both light and dark generated token blocks expose:

| Token | Required value |
|-------|----------------|
| `--brand-cta` | `#C5342C` |
| `--brand-cta-foreground` | `#FFFFFF` |
| `--brand-cta-outline-foreground` | `#C5342C` on the light surface; the legal surface foreground on the dark surface |

The measured contrast of the foreground on the CTA fill must be at least 4.5:1. The verifier fails if the pair is absent, drifts, cannot round-trip, or falls below the floor.

## Portable-guidelines contract

- Exactly three current primary CTA specimens exist: dark theme reference, light theme reference, and Type and components.
- Every specimen uses `--brand-cta` for its computed default background and `--brand-cta-foreground` for its computed text color.
- Hover and active retain the same measured color pair and add a visible non-color state cue.
- Keyboard focus presents a visible dual-tone indicator at least two CSS pixels wide.
- Reduced-motion mode does not remove any non-motion state cue.
- Exactly three current secondary CTA specimens use a transparent default fill, the `--brand-cta` red outline, and the surface-aware `--brand-cta-outline-foreground` text token.
- Secondary hover uses the same governed red fill and white foreground as the primary action, while active and focus-visible states retain non-color cues.
- Identity, link, general focus, chart, emphasis, and destructive tokens remain semantically distinct.

## PDF guide contract

- Page four presents a `brand-cta` swatch with `#C5342C` and the label `Primary CTA button`.
- The Semantic use table includes a CTA/Action row identifying `#C5342C` as the default fill and white as the legal foreground.
- CTA guidance identifies red as the filled-primary and outlined-secondary treatment, distinct from destructive `#E9505F`, identity blue, links, general focus, and chart colors.
- Default, hover, active, and focus-visible treatments are visually demonstrated and described.
- The secondary action is visibly demonstrated and labeled as the red-outline alternative.
- Page two sharp-edge copy names the approved value and role.
- Portable HTML and PDF values and semantics agree exactly.

## Reader-facing language contract

Generated PDF and portable-guide reader text uses these American forms where applicable:

- `color`
- `color vision`
- `colorway`
- `recolor`
- `rasterize`
- `synthesize`

Known British variants must not appear as standalone words in reader-visible text. Internal schema keys, source metadata, and compatibility function names are excluded.

## Failure contract

Generation or verification fails when any of the following occurs:

- a primary CTA falls back to the general blue `primary` token;
- the action or foreground value drifts from governed source;
- any CTA fill/foreground combination is below 4.5:1;
- any secondary outlined CTA uses red text on a surface where it falls below 4.5:1;
- the focus treatment is absent or relies on the identity-blue ring alone;
- the PDF omits or mislabels CTA red;
- the PDF confuses CTA red with destructive or chart semantics;
- a known British spelling returns to reader-facing guide prose;
- PDF text is clipped, overlapped, corrupted, or paginated outside the declared page structure.
