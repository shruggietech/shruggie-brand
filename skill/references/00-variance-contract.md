# The ShruggieTech Variance Contract

**Version 1.0.0 · 2026-08-22**

This document answers one question: when we build a ShruggieTech-owned or third-party brand, what may that identity decide and what may it inherit?

The machine-readable form of everything here lives in `01-canon.json`, and
`verify` reads that file to check a kit. This document explains the reasoning.
When the two disagree, the JSON wins and this document is stale.

## Why a contract exists at all

Three brand kits already exist (ShruggieTech, fragcap, go-schedule). They are
well written. They still fail in practice, and the failure has a specific
shape: an agent reads the guidelines, agrees with them, and then writes
`bg-slate-900` anyway, because that is what its hands know how to do.

Prose does not constrain agents. Three things do:

1. Fewer decisions available to get wrong.
2. Brand values expressed in the exact vocabulary the target ecosystem uses.
3. A check that fails at the moment of the mistake.

The contract is item one.

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

`shruggietech-house` inheritance adopts the house semantic orange and the house typography option. `independent` inheritance requires brand-specific emphasis and action colors. A fixed-font requirement is selected through the separate typography contract. Missing or contradictory declarations stop generation.

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

### The inherited orange

`#FF5300` and its CTA-safe form `#C24000` are carried by brands that explicitly select `shruggietech-house` inheritance. An independently themed third-party identity declares its own emphasis and action colors and does not receive this pair.

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

Every kit ships the same directory tree and passes the same `verify` checks.
An agent that has seen one kit knows where everything is in all of them.

### Glyph production

Mark geometry is free. How it gets produced is not. The mark is composed in
`build/mk_paths.py` from `glyphkit` primitives, in absolute M/L/C/Z only, as
filled paths, centred on measured ink, with a separate reduced master that
removes whole elements. It is proved by `validate_glyph.py` before anything is
exported. See `08-glyph-construction.md`.

This is immutable because it is the step that fails, and it fails identically
every time: an agent types path data and then has no mechanical way to tell
whether the numbers describe the shape it had in mind.

### Portability

Three capability tiers, and the core tier, Python and its standard library
alone, must always succeed. Probe before building. A missing tool is a recorded
skip naming the tool, never a silent substitution. No quality gate may depend on
an agent being able to view an image. See `09-portability.md`.

### Where a fix lands

A kit that has to patch a generator to build has found a defect in the skill,
not a quirk of that brand. Land the patch in `templates/` and note it in the
kit's `build/README.md`. Four kits deep, `gen_logo.py` in the skill was 9.5 KB
while the newest kit shipped 17.8 KB of it, and every new kit started from the
older, more broken copy.

## Constrained

### Identity accent

The one real decision a sub-brand makes. Five checks, all machine-checkable:

| Check | Rule |
| --- | --- |
| Hue separation | At least 30° in OKLCH from every existing sibling **identity** accent |
| Orange distance | At least 30° from house orange at 38.3° when house inheritance is selected |
| Dark contrast | At least 4.5:1 on the dark base |
| Light variant | A separate accessible variant clearing 4.5:1 on the light base must exist |
| Foreground pairing | The legal text color on the accent fill is measured and recorded |

Current identity accents: ShruggieTech green 153.0°, fragcap cyan 215.7°,
go-schedule Anchor Blue 253.3°. Closest pair is 37.6° apart, so the 30° rule
passes all three approved kits with margin.

Scope note that matters: go-schedule's Interval Mint sits 18.8° from green,
which would fail the rule. Mint is a semantic success color there, and Anchor
Blue is the identity accent. The check applies to identity accents only.

The light variant is not optional bookkeeping. fragcap's Signal Cyan measures
1.89:1 on its light surface, and ShruggieTech's own bright green measures
1.98:1 on `#F8F8F6` while being set as the light-mode link color in the live
stylesheet. That is a real defect on a real site, and it exists because no
accessible green was ever derived. Now one is (`#037B40`, 5.05:1).

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
pairwise separation is at least 50°, and no entry comes within 40° of the
inherited orange or 60° of the fault red. It must remain a formula, stated, not
five hues somebody liked. Covarity's `[0, −57, −113, −170, −226]` is the worked
example: the same arc, swept one direction, evenly spaced.

### Motion

120ms to 300ms on an approved easing. No pulsing glow, glitch, screen shake, or
decorative scan lines.

### Voice register

Pick a lane: direct-and-witty (parent), precise-and-dry (fragcap), or
operator-runbook (go-schedule). The banned-rhetoric list applies to all three
and is enforced by `verify`.

### The shruggie flourish

Opt-in. At most one moment per view, always in the identity accent. fragcap
declines it, correctly. A security-adjacent tool should not wink.

## Free

Logo mark geometry. Governing principle, positioning, and all copy.
Domain-specific components (`CaptureRow`, `ScheduleRow`) and bespoke icons.
Product-specific page structure.

## What this buys us

A sub-brand kit becomes, in the normal case, **one color decision and one logo
decision**. Everything else generates. That is the answer to "keep mandatory
operator inputs to a minimum": most of the inputs were never real choices, they
were opportunities to drift.
