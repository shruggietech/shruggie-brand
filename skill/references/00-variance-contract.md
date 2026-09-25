# Variance Contract

This document answers one question: when we build a ShruggieTech-owned or third-party brand, what may that identity decide and what may it inherit?

The machine-readable form of everything here lives in `01-canon.json`, and
`verify` reads that file to check a kit. This document explains the reasoning.
When the two disagree, the JSON wins and this document is stale.

## Why a contract exists at all

The contract separates brand decisions from shared implementation rules. A consumer needs values expressed in its target ecosystem, and verification must catch a substituted value at the point of use. Guidance explains the intended choice; generated tokens and checks make that choice executable.

## The three tiers

| Tier | Meaning |
| --- | --- |
| **Immutable** | Inherited verbatim. A sub-brand that changes one of these is not a ShruggieTech sub-brand. |
| **Constrained** | Chosen per sub-brand, subject to a stated rule that `verify` can check. |
| **Free** | Entirely the sub-brand's own. |

The default answer to "can we change this?" is no. Constrained axes are
deliberately few.

## Required affiliation gate

Every brand explicitly declares ownership, showcase permission, parentage, inheritance, endorsement, and service credit before creative work. These facts are independent. Third-party ownership does not imply public showcase permission, ShruggieTech parentage, house inheritance, or a service credit.

`shruggietech-house` is an explicit selection of the historical house orange emphasis/action pair. `independent` requires brand-specific emphasis and action colors. Either choice is available to an owned brand; a third-party brand may deliberately share a color without acquiring ownership or endorsement. Typography uses its separate `house` or `fixed` mode and never selects colors. Missing or contradictory declarations stop generation.

## Immutable

### Typography

House mode uses Space Grotesk (display, 500/700), Geist (body, 400/500), Geist Mono (400). Fixed mode uses only the explicitly approved local families, faces, weights, and styles declared in the brand contract. Both modes retain the scale, tracking, and casing rules.

Geist ships 400 and 500 only. Geist Mono ships 400 only. Asking for a weight
that does not exist makes the renderer synthesise a faux bold, which prints
badly and forces outlined glyphs into PDFs. In mono contexts, emphasis is
carried by color.

### Geometry

Radii 6 (chips) / 8 (buttons, inputs) / 12 (cards) / pill (badges). The 4px
spacing base and its ten steps. Gutters 24 → 48 → 80. Section rhythm
120 → 160 → 200. Content width 1200, narrow 720.

These are not aesthetic preferences that happen to be written down. They are
measured off the live shruggie.tech token set, and they are the thing that
makes two products look related when a client sees them in the same deck.

### Density

Every kit ships **both** the default and the compact setting. A product
switches per screen. A sub-brand does not pick one as its baseline.

This is a deliberate tightening. A packet table wants tight rows and a
marketing page wants roomy ones, and both of those are true inside a single
product. Letting each sub-brand set its own baseline solves the wrong problem
and costs sibling coherence.

### Icon language

lucide. Grid 24, stroke 1.5 to 2, `currentColor`, inline SVG.

A sub-brand **may** draw domain icons lucide lacks, drawn to the same grid and
stroke spec and shipped in the kit's `icons/` directory. fragcap did exactly
this with six capture-domain icons. Swapping to a different icon library is not
permitted.

Icon set is the single largest source of agent drift and standardising it costs
nothing. Two ShruggieTech products must not read as two companies.

### The optional shared orange

`#FF5300` and its CTA-safe form `#C24000` are carried by brands that explicitly select `shruggietech-house` inheritance. An independent palette declares its own emphasis and action colors regardless of ownership. A color match does not imply the same palette contract or parentage.

`#C24000` is fill-only. As text on the dark base it measures 4.03:1 and fails
AA for normal text. With white text on top of it, 5.21:1.

### The failure colors

Fault `#E9505F` on dark, Fault Deep `#C0293A` on light. Promoted into canon
from fragcap 1.1.0, because the parent system had no failure state at all and
fragcap had to invent one. Now nobody invents one again.

### Accessibility floor

WCAG 2.1 AA at rendered size. A visible 2px focus ring at 2px offset on every
interactive element. Status never carried by color alone. `prefers-reduced-motion`
honored everywhere. Contrast claims re-derived from hex on every build.

**This one is never exemptable.** Not by a conformance level, not by legacy
grandfathering, not by an operator override, and not by a deadline. A kit that
cannot meet AA is not shippable, and the resolution is always to change the
value. `aa-floor`, `accent-rule`, `globals-slots` and `contrast-rederived` sit
outside every exception mechanism the kit has or will have.

Note the distinction between the two colour checks, because it is the one that
let a defect through. `contrast-rederived` asks whether a stated number is
honest. `aa-floor` asks whether the value is legal. A token that accurately
declares 3.2:1 passes the first and fails the second, and until `aa-floor`
existed only the first was enforced.

A rebuild that surfaces an inherited AA failure fixes it. The
identity-invariance gate treats an accessibility correction as pre-authorised
rather than as an identity change requiring sign-off: it is recorded in the
kit's `NOTES.md` and in the changelog, and it proceeds.

**Resolved precedent.** ShruggieTech's own bright green `#2BCC73` measures
1.98:1 on the light surface and was the light-mode link colour on the live site.
Under this rule that is a defect to fix rather than a quirk to preserve. The
accessible variant `#037B40` at 5.05:1 replaces it wherever green is used as
text on a light surface, in the kit and downstream on shruggie.tech.

### The endorsement

An owned child may explicitly select "A ShruggieTech project", set in its declared mono family, uppercase, positive tracking, visually subordinate, and outside the product logo's clear space. A third-party identity cannot use this ownership endorsement. It may explicitly select the fixed neutral service credit "Brand system by ShruggieTech" or no credit.

### Kit shape

Every kit ships the shared core contract and passes its declared `verify` checks. Optional assets and platform capabilities vary by brand; inspect the delivered `manifest.json` for exact files.

### Glyph production

New constructed marks use an approved `build/mk_paths.py` with `glyphkit` primitives and a separate reduced master. Authoritative supplied marks bind exact approved inputs without a construction helper; imported and legacy constructed geometry remain byte-identical. Every source mode passes its applicable `validate_glyph.py` checks before export. See `08-glyph-construction.md` for the source-mode and measurement rules.

### Portability

Three capability tiers, and the core tier, Python and its standard library
alone, must always succeed. Probe before building. A missing tool is a recorded
skip naming the tool, never a silent substitution. No quality gate may depend on
an agent being able to view an image. See `09-portability.md`.

### Where a fix lands

A kit that has to patch a generator to build has found a defect in the skill, not a quirk of that brand. Land the patch in `templates/`, rebuild affected kits, and note the change in the kit's `build/README.md`. Never patch a generated copy as the lasting fix.

## Constrained

### Identity accent

Identity colors are approved separately from interface cues. The accent has three measured checks:

Record each approved combination of formal colors with its intended application and exact artwork reference. A shared interface cue remains separately named and measured.

| Check | Rule |
| --- | --- |
| Dark contrast | At least 4.5:1 on the dark base |
| Light variant | A separate accessible variant clearing 4.5:1 on the light base must exist |
| Foreground pairing | The legal text color on the accent fill is measured and recorded |

Another brand's hue is context for a creative choice, not a qualification rule. A chosen palette may intentionally share a hue while preserving its own source record and measured interface pairings.

The light variant is not optional bookkeeping. Measure the actual foreground and surface pair in each theme, record the result, and change a failing value before publication. Do not infer light-theme legibility from a dark-theme pass.

### Dark surface temperature

One hue family, OKLCH lightness 0.10 to 0.22, chroma at or below 0.030. Parent
`#000`, fragcap `#050708`, go-schedule `#071014` are all legal. A warm
brown-black would not be.

### Chart palette

Derived from the identity accent by formula, never hand-picked: rotate hue by
0, −52, +52, −104, +104; clamp lightness to 0.58–0.82; hold chroma at 0.92× the
accent for entries two through five; fit to sRGB. Every entry clears 4.5:1 on
the dark base.

**The rotation set is a default, and a brand may replace it.** That default is
symmetric about the accent, which assumes the accent sits mid-spectrum. From
green at 153° it spans 49° to 257° and behaves. From an accent near the ends of
the hue circle it wraps: `+52` off Covariance Purple at 311.8° lands on 3.7°, a
magenta that reads as a paler accent and sits 15° from the failure red.

A brand hitting that declares `chart_palette.hue_rotations` in `brand.json` with
its reasoning. Only the offsets may change. Chroma stays at 0.92×, lightness is
still solved against the real surface, every entry still clears 4.5:1, minimum
pairwise separation is at least 50°. Charts use labels or shapes so meaning does not depend on hue alone. The set must remain a formula, stated, not
five hues somebody liked. Covarity's `[0, −57, −113, −170, −226]` is the worked
example: the same arc, swept one direction, evenly spaced.

### Motion

120ms to 300ms on an approved easing. No pulsing glow, glitch, screen shake, or
decorative scan lines.

### Voice register

Choose a voice register in the brand source and use it consistently. The banned-rhetoric list applies to every register and is enforced by `verify`.

### The shruggie flourish

Opt-in. At most one moment per view, always in the identity accent. A brand may decline the flourish when it does not fit its voice.

## Free

Logo mark geometry. Governing principle, positioning, and all copy.
Domain-specific components (`CaptureRow`, `ScheduleRow`) and bespoke icons.
Product-specific page structure.

## What this buys us

A brand author still decides strategy, voice, logo source, palette, and the other choices that define its identity. The contract makes those decisions explicit and lets shared implementation details generate consistently from approved source. The authoring workflow in `03-interview.md` governs discovery and approval before a kit is shipped.
