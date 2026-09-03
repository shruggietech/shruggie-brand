<!-- verify:allow-rhetoric reason="Preserved source guide contains examples and deliberate operational contrasts." -->

# go-schedule Brand & Design System

**Status:** Source of truth, version 1.0.0\
**Parent:** ShruggieTech\
**Repository:** `shruggietech/go-schedule`\
**Audience:** Product, engineering, documentation, and communications teams

go-schedule is a cross-platform scheduler in Go. The identity connects familiar
cron-field structure with cross-platform scheduling, desktop visibility, and
service-backed execution. It should feel like a practical system utility: cron
users recognize the lineage immediately, while everyone else understands that the
same scheduling power is available on every OS through a CLI, a desktop app, and a
background service.

## Contents

- [Brand foundation](#brand-foundation)
- [Logo system](#logo-system)
- [Color](#color)
- [Typography](#typography)
- [Visual language](#visual-language)
- [Voice and writing](#voice-and-writing)
- [Parent brand relationship](#parent-brand-relationship)
- [Digital implementation](#digital-implementation)
- [Asset inventory](#asset-inventory)

## Brand foundation

### Governing principle: familiar scheduling, broader reach

go-schedule reads as calm, exact, technical infrastructure. Cron users should
recognize the field structure at a glance. Everyone else should see that a
readable schedule can run anywhere, with policy stated plainly rather than hidden
in a crontab comment.

### Positioning

**Category:** Cross-platform task scheduling.\
**Role:** A readable scheduler for service-managed automation.\
**Audience:** Developers, operators, maintainers, and technical users who want
less cron ambiguity without giving up control.\
**Functional descriptor:** A cross-platform scheduler in Go.

### Brand idea

**Schedules as fields and run points.** Anchor Blue marks exact run times. Interval
Mint marks recurrence and readable schedule intent. Neutral rails keep the mark
quiet and technical. The system privileges explicit policy (timezone, catch-up,
overlap) over convenience claims.

### Personality

| Trait | Expression | Avoid |
| --- | --- | --- |
| Exact | Precise nouns, units, timezones, and flags | Vague claims |
| Operational | Runbook clarity, explicit policy | Hand-waving |
| Calm | Quiet surfaces, steady rhythm | Hype or urgency |
| Competent | Assumes technical ability | Condescending tutorials |
| Fair to cron | Uses cron as a reference frame | Copy that dismisses cron |

### Brand promises

- Schedules are readable and their policy is explicit.
- Timezone, catch-up, and overlap behavior are stated, not implied.
- Terminology stays consistent across CLI, docs, schemas, and interfaces.
- The same schedule store backs the CLI, the desktop app, and the service.

## Logo system

### Mark construction

The mark is a compact terminal and cron-field symbol: a prompt chevron, a command
cursor line, and five schedule cells rendered as asterisks over a dashed rail. It
is technical enough for cron users while remaining legible as a general scheduling
mark. The five cells map to the five cron fields; the Anchor Blue cell marks a
selected field.

The wordmark is Space Grotesk Bold **outlined to vector paths**. It does not depend
on any installed or web-loaded font at render time, so it reproduces identically in
browsers, on GitHub, and in raster exports. Do not re-typeset the wordmark in live
text, and do not substitute another face.

### Approved lockups

Use the horizontal lockup (mark plus wordmark, no tagline) for headers, repository
artwork, and wide surfaces. Use the stacked lockup for square compositions and
title pages. Use the mark alone for application icons, favicons, avatars, and
compact controls. Use the wordmark alone only where another nearby element already
establishes product identity.

### Clear space and minimum size

Maintain clear space equal to the width of one schedule cell around any lockup. No
text, border, icon, or crop may enter that area.

| Asset | Minimum digital size |
| --- | --- |
| Mark | 24 px wide |
| Horizontal lockup | 160 px wide |
| Stacked lockup | 96 px wide |
| Wordmark | 120 px wide |

Below 32 px, use the supplied favicon exports rather than downscaling a full
lockup. The favicon uses a reduced mark (prompt and cursor only) so it stays
legible in a browser tab.

### Backgrounds

The primary presentation is the color mark on Night. The light variant places the
color mark and Ink wordmark on Paper. Use the single-color white or black variants
where reproduction supports only one ink.

### Prohibited treatments

- Do not rotate, skew, stretch, outline, bevel, or add glow.
- Do not recolor individual schedule cells or lanes.
- Do not set the wordmark in live text or a substitute typeface.
- Do not add a tagline inside the horizontal lockup.
- Do not place the logo over busy imagery.
- Do not combine the go-schedule and ShruggieTech marks into one lockup.

## Color

The palette is dark-first and close to monochrome. Neutral rails carry structure;
Interval Mint and Anchor Blue carry meaning; Hold Amber and Stop Red stay scarce so
they retain their signal.

| Token | Hex | Role |
| --- | --- | --- |
| Night | `#071014` | Primary dark background |
| Panel | `#0D171C` | Cards and code surfaces |
| Raised | `#13232A` | Elevated controls, selected rows |
| Line | `#28414B` | Rails, borders, inactive schedule segments |
| Text | `#F3F7F8` | Primary text on dark |
| Muted | `#9BAEB6` | Secondary text on dark |
| Interval Mint | `#62D9B7` | Recurrence, readable schedule intent, success |
| Anchor Blue | `#58A6FF` | Exact run points, links, focus |
| Hold Amber | `#F2B84B` | Catch-up, pause, overlap, pending policy (rare) |
| Stop Red | `#E05F5F` | Failed or missed run (error only) |
| Paper | `#F6F8F7` | Light documentation surface |
| Ink | `#132027` | Primary text on light |
| Muted Ink | `#4A5A62` | Secondary text on light |

### Deep accents for light surfaces

The dark-tuned accents do not meet WCAG AA as text on Paper. Use these deeper
values for accent text, links, or icons on light surfaces:

| Token | Hex | Contrast on Paper |
| --- | --- | --- |
| Interval Deep | `#0E7C63` | 4.8:1 |
| Anchor Deep | `#1160C6` | 5.6:1 |
| Hold Deep | `#9A6600` | 4.6:1 |
| Stop Deep | `#C23B3B` | 4.9:1 |

### Color ratio and semantics

Aim for roughly 80 percent neutral surfaces, 15 percent Mint and Blue combined, and
under 5 percent Amber in a typical view. Anchor Blue identifies selection, the next
run, links, and focus. Interval Mint identifies recurrence and successful runs.
Hold Amber flags catch-up, overlap, or pending policy. Stop Red is reserved for a
failed or missed run and always appears with explicit text, never color alone.

## Typography

Typography is shared with other ShruggieTech product kits, creating lineage through
craft rather than copied color or layout.

| Function | Typeface | Weights |
| --- | --- | --- |
| Display and headings | Space Grotesk | 500, 700 |
| Body and interface | Geist | 400, 500 |
| Commands, schedules, labels | Geist Mono | 400 |
| Product wordmark | Space Grotesk Bold, outlined | Fixed artwork |

### Monospace decision

Geist Mono keeps `0` and `O`, `1`, `l` and `I`, `8` and `B`, `5` and `S`, `2` and
`Z` distinguishable at interface size, which matters for cron fields, timestamps,
and daemon output. Its family relationship to Geist keeps command specimens from
feeling detached from surrounding text. Evaluate any future replacement against the
included specimen (`specimens/`), not a decorative alphabet.

### Type behavior

Display headings use tight tracking near `-0.025em`. Body copy uses a line height
near `1.65`. Labels and eyebrows use Geist Mono, uppercase, with `0.12em` tracking.
Commands and schedules never use ligatures or smart quotes. Sentence case is the
default; uppercase is reserved for compact labels and schedule states.

## Visual language

### Instrumentation

References come from terminals, cron fields, timelines, and run logs. Use exact
alignment and quiet negative space. A graphic should explain a schedule, a state,
or a relationship, not decorate.

### Iconography

Use simple line icons with a `1.75px` stroke, lightly rounded joints, and minimal
fill. Prefer direct symbols: terminal, clock, calendar, service, timezone, retry.
Avoid mascots, decorative circuitry, and anything that reads as spectacle.

### Surfaces and geometry

Panels use `1px` Line borders and radii between `4px` and `8px`. Avoid glass
effects, large shadows, chrome, and decorative gradients. Selected states may use a
subtle Anchor Blue border or a low-opacity Anchor fill.

### Motion

Motion communicates run state, selection, or continuity. Keep interface transitions
between `120ms` and `240ms`. Avoid pulsing glow, glitch effects, and decorative
scan lines. Respect `prefers-reduced-motion`.

## Voice and writing

Write like an operator explaining a runbook: short sentences, exact nouns, explicit
policy. Treat cron as a useful frame of reference rather than a problem to mock.

### Preferred language

| Prefer | Avoid |
| --- | --- |
| schedule, interval, run, daemon, timezone | supercharge, automate everything |
| catch-up, overlap, policy, service, task | never miss a beat, time wizard |
| requires, emits, records, next run | magic cron, copy that dismisses cron |

### Examples

**Product statement:** A cross-platform scheduler in Go.\
**Prerequisite:** The service requires permission to run at startup on the target
OS.\
**Empty state:** No tasks scheduled yet.\
**Error:** Run skipped. The daemon was not running at the scheduled time; catch-up
is off.

### Casing and terminology

The product name is always lowercase: **go-schedule**. Preserve canonical casing for
timezones, flags, and command names. The CLI binary is `gosched`.

## Parent brand relationship

go-schedule is an independent ShruggieTech product identity. It shares Space
Grotesk, Geist, Geist Mono, and dark-first discipline. It does not inherit
ShruggieTech green, the shruggie mark, or marketing layouts.

The approved endorsement is **A ShruggieTech project**. Set it in Geist Mono,
uppercase, with `0.12em` tracking, visually subordinate and outside the logo's clear
space. It may appear in footers, About pages, repository metadata, and the social
preview. Do not create a combined parent-product logo.

## Digital implementation

### CSS

Link `styles.css` to load fonts, tokens, and base element styles in one file. The
default surface is dark; add `class="gs-light"` to a container for reading mode.
Component styles live in `components/components.css`; React wrappers live in
`components/core/` and `components/forms/`.

### Favicons

The `favicons/` directory includes an SVG, an ICO bundle, standard browser PNGs, an
Apple touch icon, Android icons, and a web manifest. The favicon uses the reduced
prompt mark on a Night tile so it protects legibility across browser themes.

### Accessibility

Do not use the dark-tuned Mint, Blue, or Amber as text on Paper; use the Deep
variants. Do not communicate run status through color alone; pair it with text or an
icon. Every interactive element needs a visible `2px` focus ring and a non-color
state change. Interface text should meet WCAG AA contrast at its rendered size.

## Asset inventory

| Directory | Contents |
| --- | --- |
| `logos/svg/` | Vector masters and all approved lockups (font-proof) |
| `logos/png/` | High-resolution raster exports and social preview |
| `favicons/` | Browser, Apple, Android, SVG, ICO, and manifest assets |
| `fonts/` | WOFF2, TTF, CSS declarations, and OFL licenses |
| `tokens/` | CSS and JSON design tokens (colors, type, spacing, base) |
| `components/` | `components.css` plus React core and form components |
| `guidelines/` | Visual system reference (`index.html`) |
| `ui_kits/go-schedule-web/` | Demo product page built from the system |
| `specimens/` | Type and command-readability specimen |
| `styles.css` | Single CSS entry point |
| `brand-guide.pdf` | Printable reference manual |
| `VERIFY.md` | Generated dimensions, ICO entries, and SHA-256 checksums |

Treat the files in `logos/svg/` as the source of truth. Use SVG in product
interfaces and documentation wherever the surface supports it; use PNG for social
platforms and raster-only systems.
