# Covarity brand system

Covarity is two products under one identity. `covarity-knowledge` stores sources, evidence spans, entities, claims, and relationships with their provenance intact. `covarity-context` compiles task-scoped instructions and working memory for agents. Each one starts, tests, backs up, and fails on its own, and they meet only through public versioned interfaces.

## The name

Fixed on 18 March 2026, before there was a specification to attach it to.

**co** carries two systems and two parties. A knowledge system and a context system that run apart and meet at a single contract, and a person and a machine working the same material. Cooperation and collaboration start in the same place.

**varity** is covariance folded into verity. Covariance measures how two quantities move together. Verity is the older word for something true that can be shown to be true. Put side by side they describe the work: watch two things move against each other, and keep a record honest enough that somebody else can check it.

Written form: `Covarity` in title case in prose, `covarity` in lowercase for technical identifiers, repositories and package names, `covarity.ai` in a URL and anywhere an unrelated company of the same name could be confused with this one. Never set `Covarity.ai` in a wordmark or a headline, because a top-level domain is an address and it dates a mark.

## Build assumptions

- The wordmark is Covarity. `covarity.ai` is the domain and the disambiguator in any context where unrelated companies named Covarity could be confused with this one.
- Covariance Purple carries product identity. The inherited ShruggieTech orange stays reserved for emphasis, warning, and the split terminal of the mark.
- The register is precise-dry and the shruggie flourish is declined. A product whose entire claim is provenance should not wink.
- Both products ship under one accent. Neither `covarity-knowledge` nor `covarity-context` gets a colour of its own.
- The mark is drawn on a 1000-unit square grid with the artwork optically centred inside it. Standalone mark PNGs export on transparent 1024 canvases; lockups and wordmarks keep their natural aspect ratios.

## Positioning

| Axis | Decision |
| --- | --- |
| Category | Knowledge and agent infrastructure |
| Role | Hold evidence with provenance, decide identity before publication, compile context for agents |
| Audience | Developers, researchers, and technical operators who need every answer traceable to a span |
| Register | Precise and dry |
| Shruggie flourish | Declined |
| Product principle | See what is known. |

## Identity color

| Token | Hex | Use |
| --- | --- | --- |
| Covariance Purple | `#C659FF` | Identity, links, focus, selection, the long arc of the mark |
| Covariance Deep | `#BF36FF` | Hover and active states on dark surfaces |
| Covariance Accessible | `#A000EC` | Links and identity text on light surfaces |
| Dim | `#A79CB8` | Secondary marks and non-identity ink |
| ShruggieTech Orange | `#FF5300` | Shared emphasis and warning hue, the terminal segment of the mark |
| CTA Orange | `#C24000` | Fill with white foreground |
| Fault | `#E9505F` | Failure state on dark surfaces |
| Fault Deep | `#C0293A` | Failure state on light surfaces |

The accent clears every check in the canon's `identity_accent` rule: 58.5 degrees from go-schedule Anchor Blue, 86.5 from the inherited orange, and further still from ShruggieTech green, fragcap cyan and Glitchpad sulfur. Measured contrast values and legal foreground pairings live in `brand.json` and `VERIFY.md`. Regenerate those numbers through the build scripts rather than editing them.

Surfaces run a purple-tinted near-black rather than a neutral one, so the accent sits on a related ground. Every surface stays inside the canon's dark-temperature rule (OKLCH lightness 0.10 to 0.22, chroma at or below 0.030).

## Logo construction

The mark is an aperture C broken once. The long arc is durable knowledge. The short orange terminal is agent context. The radial slot between them is the adjudication boundary, where a reference waits for a verdict instead of being published as a fact.

| Measurement | Value |
| --- | ---: |
| Grid | 1000 units square |
| Centre | 554, 500 |
| Outer radius | 420 units |
| Ring thickness | 168 units |
| Aperture | 84 degrees, from 318 to 42 |
| Orange terminal | 36 degrees, from 42 to 78 |
| Adjudication slot | 10 degrees, from 78 to 88 |
| Clear-space unit | 100 units, 10% of the grid |
| Reduced-master threshold | 32 px |

The centre sits at 554 rather than 500 because an 84-degree aperture removes ink from the right side. Offsetting the construction puts the drawn bounding box back on the optical centre of the canvas.

The reduced master drops the slot and the orange segment and runs a single 190-unit ring across the whole 42 to 318 sweep. It removes whole elements rather than thinning everything, which is what survives a 16 px favicon.

Every terminal is a flat radial cut. Every shipped SVG uses filled paths and outlined glyphs, so nothing depends on an installed font.

### Prohibited treatments

- Do not close the aperture or the slot. The opening and the break are the whole idea.
- Do not recolour the long arc to orange or the terminal segment to purple.
- Do not add a node, dot, or glyph inside the aperture.
- Do not set the C in a typeface. The mark is drawn geometry and the wordmark is outlined Space Grotesk.
- Do not alter the 420-unit outer radius, the 168-unit ring, the 84-degree aperture, or the 10-degree slot.
- Do not use the full mark below 24 px. The reduced mark takes over at and below 32 px.
- Do not combine the Covarity and ShruggieTech marks into one lockup.

## Chart palette

The canon derives chart colors from the identity accent by rotating hue 0, -52, +52, -104, +104. That pattern assumes an accent sitting mid-spectrum: from ShruggieTech green at 153 it spans 49 to 257 and behaves. From Covariance Purple at 311.8 the +52 entry wraps onto 3.7, a magenta that reads as a paler accent and sits 15 degrees from the failure red.

Covarity declares `chart_palette.hue_rotations` as `[0, -57, -113, -170, -226]`: the same arc, swept one direction, at an even 57 degrees. The 0.92 chroma relationship and the solve-against-the-real-surface rule are unchanged, and mid-spectrum sub-brands keep the canon default. Minimum pairwise separation is 55.7 degrees, and no entry comes within 47 degrees of the warning orange or 67 of the failure red.

| | Dark | Light |
| --- | --- | --- |
| chart-1 | `#C75FFF` | `#A000EC` |
| chart-2 | `#4499FF` | `#0073CC` |
| chart-3 | `#00ADB3` | `#007F80` |
| chart-4 | `#22B80C` | `#348300` |
| chart-5 | `#BE9000` | `#936A00` |

## Typography

Space Grotesk handles display text at 500 and 700. Geist handles body and interface text at 400 and 500. Geist Mono handles spans, hashes, identifiers, confidence figures, and metadata at 400. The font binaries and OFL licenses are bundled in `fonts/`. Asking for a weight the face does not ship makes the renderer synthesise a faux bold; in mono contexts, carry emphasis with colour.

## Interface behavior

Dark is the default product surface. Light is a reading surface for documentation and the blog. Evidence tables, verdict queues, and context traces use the compact density; explanatory surfaces use the default. Every focusable control carries a visible two-pixel focus ring at a two-pixel offset. Status always carries a label or a shape as well as a colour, which matters here because supported, provisional, and unsupported are the three states the product exists to distinguish.

An unsupported answer is a designed state. It is never dressed up as an error. Give it a container, a heading, and an explanation of what failed the threshold.

## Installation

For a non-React surface, load `styles.css`, then `components/components.css`.

For Next.js, follow `nextjs/README.md`. The kit publishes Tailwind v4 and shadcn bindings through the `@covarity` registry namespace, including the three domain rows declared in `brand.json`.

## Verification

Run the scripts from `build/` with the dependencies described in `build/README.md`. Delivery requires zero problems in `VERIFY.md`, a clean PDF render check, a clean pagination check, and visual inspection of every image in `qc/`.

## Parent endorsement

Set `A ShruggieTech project` in Geist Mono, uppercase, with positive tracking. Keep it visually subordinate and outside the product logo clear space. Never combine the parent mark and the product mark into a single lockup.

Names, wordmarks, logos, endorsement lockups, and logo path geometry remain reserved as described in the repository's [brand asset terms](../../LICENSE-BRAND.md).
