# Logo Protocol

**Image generation is for ideation. Hand-authored vector is what ships.**

This is the single rule that separates a kit from a mess. Everything below
follows from it.

## The boundary

| Phase | Tool | Output |
| --- | --- | --- |
| Explore the concept space | frontier image generation, encouraged | conversation, mood, direction |
| Understand a supplied concept | `potrace`, Inkscape trace, palette extraction | reference geometry, never shipped |
| Construct the mark | the agent composes glyphkit primitives in `build/mk_paths.py` | the deliverable |
| Prove the mark | `templates/validate_glyph.py` | a pass or a numbered failure |
| Export | `rsvg-convert`, `resvg`, Inkscape, Node resvg, `oxipng`; ImageMagick only for ICO assembly | rasters derived from the vector master |

Generated images are how the operator and the agent agree on what the thing
should feel like. They are input to a conversation. The moment a shape is
agreed, the agent rebuilds it as clean geometry with stated coordinates.

Never trace a diffusion output into shipped artwork. Never rasterise a large
logo down at runtime to produce a favicon.

## Construction

**The procedure lives in `08-glyph-construction.md`, and it is not optional.**
This file says what a mark must BE. That one says how to produce one without the
result being wrong, and it is where the runs that fail, fail. The short version:
the agent never types path data. It writes a parametric `build/mk_paths.py`
against `templates/glyphkit.py`, then proves the result with
`templates/validate_glyph.py`, which measures the geometry with no renderer and
no vision. Zero failures is the stopping condition.

Every mark is built on a **declared square grid**, stated in the kit README.
fragcap uses 512 units. Pick one and write it down; a grid that lives only in
the agent's head is not a grid.

Declare, in the README, as numbers:

- The grid size
- The clear-space unit, expressed as a grid measurement and as a percentage of
  artwork width (fragcap: one terminal, 34 of 512 units, roughly 9 percent)
- Minimum size per lockup, in pixels
- The threshold below which the reduced mark takes over

### Geometry rules

- **Filled paths, never strokes.** Stroked lettering resolves differently
  across engines, breaks `currentColor` fills, and does not survive
  expand-to-outlines in print, vinyl, or font tooling. fragcap converted its
  wordmark from 22px strokes to filled outlines in 1.1.0 for exactly this
  reason, and verified the silhouette pixel-identical afterwards.
- **No live text.** A shipped SVG must never depend on an installed font. Run
  `inkscape --export-text-to-path` before anything ships, then assert it.
- **Geometry inside the viewBox.** fragcap 1.0.0 shipped a wordmark whose `f`
  crossbar extended to x = -1 in a viewBox starting at 0, so it was clipped by
  its own canvas with 0px padding on the left against 60px on the right.
- **`currentColor` where the mark is single-ink**, so it inherits whatever
  semantic token its container sets.

## Lockups

Four, minimum:

| Lockup | Use |
| --- | --- |
| Horizontal | headers, repository artwork, wide surfaces |
| Stacked | square compositions, title pages |
| Mark alone | app icons, favicons, avatars, compact controls |
| Wordmark alone | only where something nearby already establishes identity |

Plus single-ink black and white variants for reproduction that supports one
ink, and a **reduced mark** for small sizes.

**Optical alignment.** In every lockup the wordmark's ascender and baseline
should bracket the mark's principal form, so the two share an optical top and
bottom. fragcap had to re-align its lockups in 1.1.0 because they did not.

## The reduced mark

At and below roughly 32px, fine detail collapses into noise. Ship a genuinely
separate simplified master with its own file, and use it for the small favicon
entries. Do not downscale the full mark and hope.

fragcap's reduced mark drops the four reticle corners and keeps the F with its
terminals. That is the right shape of decision: remove whole elements rather
than thinning everything.

## Favicons

The pipeline, in order:

1. SVG favicon from the full mark
2. PNGs at 16, 32, 48, 256 via `rsvg-convert` from the appropriate master
   (reduced at and below 32, full above)
3. Apple touch icon at 180
4. Android icons at 192 and 512
5. A **genuine multi-resolution `.ico`** carrying 16, 24, 32, 48, 64, 128, 256
6. `site.webmanifest`

Then assert the ICO entry count. fragcap 1.0.0 shipped an ICO with one entry
where seven were declared, and nothing caught it until a verify pass existed.

Keep an opaque brand background in the small icons. It protects fine detail
across light and dark browser chrome.

## Prohibited treatments

Universal, inherited by every sub-brand:

- No rotation, skew, stretch, outline, bevel, or glow
- No recolouring individual elements of the mark
- Never set a wordmark in live text or a substitute typeface
- Never place the logo over busy imagery
- Never combine the parent ShruggieTech mark and a product mark into one
  lockup

Domain-specific prohibitions are a sub-brand's own and belong in its README.
fragcap's rule against skulls, weapons, controllers, shields, and crosshairs is
the model, and note how it is written: with the actual argument (moderators
triage on appearance long before they read a manifest) rather than a slogan.

## Handling a supplied concept

When the operator brings a logo idea:

1. Look at it and describe back what is load-bearing about it in words. If the
   operator disagrees with the description, the redraw would have been wrong.
2. Extract its palette for reference. It informs the accent proposal and it
   does not override any canon check.
3. Rebuild the geometry on the declared grid. Trace output is a measuring
   tool.
4. Show the rebuild next to the original at three sizes and ask whether the
   character survived.

## What verify asserts

| Check | Fails when |
| --- | --- |
| `svg-no-live-text` | any shipped SVG contains a `<text>` element or a font dependency |
| `glyph-geometry` | commands outside absolute M/L/C/Z, ink outside the grid, bad centring, thin strokes, or a piece or counter that changes at 16 px |
| `svg-viewbox` | any path geometry falls outside its own viewBox |
| `logo-filled-paths` | a wordmark ships as strokes rather than filled outlines |
| `ico-entries` | the ICO carries fewer entries than declared |
| `raster-dimensions` | an exported PNG is not the size its filename claims |
| `reduced-mark-present` | small favicon entries were made from the full mark |

## The 1.1.0 checklist

fragcap's changelog is the best available list of what goes wrong. Every item
became a verify check:

- Wordmark shipped as strokes rather than filled outlines
- Wordmark clipped by its own viewBox
- Social preview built with live text, so the shipped PNG rendered its tagline
  in Arial instead of Geist, with subpixel colour fringing baked in
- Type specimen declaring bare font families with no fallback and no embedded
  font, rendering in the default serif on any machine without the fonts
- Brand guide PDF referencing a non-embedded Helvetica and embedding only one
  Space Grotesk weight
- ICO carrying one real entry instead of seven
- Lockups not optically aligned

Read that list before authoring a mark. It is cheaper than rediscovering it.
