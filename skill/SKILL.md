---
name: shruggie-brandbuilder
description: Build a complete, conforming brand kit for a new ShruggieTech sub-brand, or audit an existing one. Generates design tokens, a Tailwind v4 and shadcn binding layer with an installable registry, parametric logo geometry with a measured correctness gate, an enforcement layer that actually fails a build, and a verification report whose numbers are measured rather than typed. Use when creating a new product identity, refreshing an existing kit, or checking whether a project is on-brand.
license: Apache-2.0. The code, templates and reference documentation are licensed under the Apache License 2.0. Apache-2.0 section 6 grants no trademark rights, and the ShruggieTech and sub-brand names, wordmarks and logo geometry are additionally reserved: see LICENSE-BRAND.md. Bundled fonts keep their own SIL Open Font License 1.1.
compatibility: Python 3.8 or newer. `coloraide` is the only hard dependency and without it no colour work can proceed. Everything else degrades to a recorded skip: an SVG rasteriser plus Pillow adds PNGs and favicons, headless Chromium adds the brand guide PDF and the QC sheets. Run `templates/probe.py` first and route off what it reports. The mark geometry and its gate use the standard library only, so they run everywhere.
metadata:
  version: 1.1.2
  canon: 1.1.2
  parent: ShruggieTech
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
  - Edit
---

# shruggie-brandbuilder

Builds brand kits for ShruggieTech sub-brands. The kits are consistent because
almost nothing is left to decide, and correct because almost nothing is left to
judgement.

## Start here

    python3 templates/probe.py <kit-dir>

That tells you what this machine can do before you plan around it. Then ask two
questions and nothing else up front:

1. What is the brand or product called?
2. What does it do, in one sentence?

Then follow `references/03-interview.md`. Every gate after those two arrives
with a computed default, so an operator who approves everything still gets a
complete kit. **Propose before asking.** A gate that presents an empty question
has failed.

Offer two optional extras in the same breath, both defaulting to no: an existing
logo concept to consider, and any existing material at all.

## Routing

| The operator wants | Read, in order |
| --- | --- |
| A new sub-brand kit | `03-interview.md`, `00-variance-contract.md`, `02-kit-anatomy.md`, then generate |
| To pick a colour | `01-canon.json` `color.constrained_rules`, then propose candidates with measured numbers |
| A logo | `08-glyph-construction.md` first, then `06-logo-protocol.md`. Do not draw before reading it |
| Next.js or shadcn wiring | `05-shadcn-binding.md`, then run `templates/gen_nextjs.py` |
| To write copy | `07-voice.md` |
| To know what may change | `00-variance-contract.md` |
| To run somewhere unusual | `09-portability.md` |
| To check a kit | `templates/verify.py` |
| To fix an existing kit | Run verify first, then work the problems list |

## The rules that matter most

**One colour decision and one logo decision.** Under the variance contract
everything else is inherited or derived. If you find yourself deciding a radius,
a font, a spacing step, or an icon set, you have gone wrong. Read
`00-variance-contract.md`.

**Never type path data.** The mark is composed in `<kit>/build/mk_paths.py` from
`templates/glyphkit.py` primitives, in absolute M/L/C/Z only, and proved by
`templates/validate_glyph.py` before anything is exported. This is the step that
fails, and it fails the same way every time: an agent writes coordinates and
then has no mechanical way to tell whether they describe the shape it meant.
`glyphkit` cannot emit malformed geometry, and the gate answers in numbers with
no renderer and no vision. Start at `08-glyph-construction.md`.

**Accessibility is never exemptable.** WCAG AA at rendered size is a floor, and
no conformance level, legacy grandfather or operator override waives it. A kit
that cannot meet AA is not shippable and the value changes instead. Note that
`contrast-rederived` asks whether a stated number is honest while `aa-floor`
asks whether the value is legal: a token accurately declaring 3.2:1 passes the
first and fails the second. Only the first existed until canon 1.1.1, which is
how the parent brand shipped a 1.98:1 link colour on its own live site.

**Never type a contrast number.** Measure it with `coloraide` and let the
generators write it. This is not pedantry: a hand-written guide once claimed an
accent measured 1.55:1 on the light surface when it actually measures 3.06:1.
The generated guide got it right because it read the value out of `brand.json`.
If you are transcribing, stop.

**No gate may depend on having eyes.** Every quality question has a measured
form, because on some providers nobody can see the render. An agent that *can*
see images should still open the contact sheets, since taste is not measurable.
An agent that cannot is finished when the numbers are clean and must not pretend
otherwise. See `09-portability.md`.

**Probe before building, and record every skip.** `04-toolchain.md` has the
matrix and the fallback chain. A missing tool gets named in `VERIFY.md` with the
tool that was missing; it never gets silently substituted, and a skip must never
read as "not applicable".

**Bundle fonts. Never fetch them at build time.** `fonts.gstatic.com` is blocked
by the egress proxy in sandboxed environments while `fonts.googleapis.com`
resolves, so the fetch appears to succeed and dies at the binary step. Copy the
five faces and their OFL licences from a sibling kit.

**The brand guide is full-bleed dark on every sheet, and it describes the brand.**
House standard, set by fragcap 1.1.0 and enforced by `qc_render.py
--expect-ground dark`. The light reading surface appears only as specimen chips
inside dark pages. And the guide carries the name, the register, the mark, the
palette and the type. It does not carry a product summary, a scope list or an
architecture: that is a specification with the wrong cover on it, and it goes
stale the first time the spec moves.

**A patch to a generator belongs upstream.** If a kit has to edit
`templates/gen_*.py` to build, that is a defect in this skill, not a quirk of
that brand. Land the fix in `templates/` and note it in the kit's
`build/README.md`. Four kits deep, this skill still shipped a `gen_logo.py` half
the size of the one the newest kit was actually using, and every new kit started
from the older, more broken copy.

## Generating

One command runs the whole pipeline and reports every gate:

    python3 templates/build_kit.py <kit-dir>

It probes first, runs the glyph gate second and stops there if the mark is
wrong, then builds. Individually:

    python3 templates/probe.py          <kit>                 # capability tier
    python3 templates/validate_glyph.py <brand.json>          # the mark, measured
    python3 templates/enrich_brand.py   <brand.json>          # measured values written back
    python3 templates/build_specimen.py <brand.json>          # outlined type specimen
    python3 templates/gen_vanilla.py    <brand.json> <kit>    # tokens, styles.css, components
    python3 templates/gen_nextjs.py     <brand.json> <kit>    # globals.css, registry, fonts, provider
    python3 templates/gen_enforcement.py <brand.json> <kit>   # AGENTS.md, oxlint, stylelint
    python3 templates/gen_logo.py       <brand.json> <kit>    # colourways, lockups, favicons, ICO
    python3 templates/gen_guidelines.py <brand.json> <kit>    # the guidelines page
    python3 templates/gen_guide_pdf.py  <brand.json> <kit>    # the brand guide, full-bleed dark
    python3 templates/verify.py         <kit>                 # measured VERIFY.md
    python3 templates/qc_images.py      <kit>                 # logo and page contact sheets
    python3 templates/qc_render.py      <kit>/brand-guide.pdf --expect-ground dark
    python3 templates/qc_paginate.py    <kit>/build/*.print.html

`gen_logo.py` does not invent geometry. Copy `templates/mk_paths.example.py` to
`<kit>/build/mk_paths.py`, edit the parameter block, run the gate, write the
paths into `brand.json`, and the generator produces every colourway, the
outlined wordmark, the lockups, all rasters, the favicon set and a real
multi-entry ICO.

`examples/shruggietech/` is a real generated instance. Read it when unsure what
correct output looks like.

## Finishing

A kit is done when `verify.py` reports zero problems, `validate_glyph.py`
reports zero failures, `qc_render.py` reports zero problems where the tier
allowed it to run, and every skip names the tool that was missing. Present the
guidelines page, the UI kit screenshots, the type specimen, and the verification
table. A non-zero problem count blocks the final gate.

If you can see images, open `qc/logo-sheet.png` and `qc/contact-sheet.png`
before you say it is finished. The numbers narrow where to look; they do not
replace looking.

## If the operator is not responding

Do not stall on a gate. Take the computed default, state the assumption
prominently at the top of the output, and continue. A complete kit with three
stated assumptions beats a half kit waiting on a question nobody is reading.

## Files

| Path | What it is |
| --- | --- |
| `AGENTS.md` | The same routing, with no frontmatter, for hosts that do not read skill metadata |
| `LICENSE` | Apache License 2.0, the licence for everything except the brand assets |
| `LICENSE-BRAND.md` | What is reserved: names, wordmarks, logo files and logo path data |
| `NOTICE` | Apache attribution notice, plus the bundled font licences |
| `references/00-variance-contract.md` | immutable, constrained, free. Start here for any scope question |
| `references/01-canon.json` | machine-readable inheritance root. Generators read this |
| `references/02-kit-anatomy.md` | what a complete kit contains, file by file |
| `references/03-interview.md` | the five gates and how each default is computed |
| `references/04-toolchain.md` | probe script and the asset-to-tool matrix |
| `references/05-shadcn-binding.md` | token to slot map, registry authoring, the radius deviation |
| `references/06-logo-protocol.md` | what a mark must be: grid, lockups, favicons, prohibitions |
| `references/07-voice.md` | registers, the principle and descriptor shapes, banned rhetoric |
| `references/08-glyph-construction.md` | how to produce a mark that is not wrong |
| `references/09-portability.md` | capability tiers and the cross-provider rules |
| `templates/probe.py` | what this machine can do, as JSON the pipeline reads |
| `templates/glyphkit.py` | mark primitives, exact bbox, optical centring. Standard library only |
| `templates/validate_glyph.py` | the measured geometry gate. No renderer, no vision |
| `templates/mk_paths.example.py` | copy to `<kit>/build/mk_paths.py` and edit the parameters |
| `templates/gen_vanilla.py` | tokens, styles.css and components, generated rather than hand-written |
| `templates/gen_nextjs.py` | the whole `nextjs/` layer |
| `templates/gen_enforcement.py` | `AGENTS.md`, oxlint and stylelint configs |
| `templates/gen_logo.py` | colourways, outlined wordmark, lockups, rasters, favicons, ICO |
| `templates/gen_guidelines.py` | the guidelines page, rendered from the tokens the product ships |
| `templates/gen_guide_pdf.py` | the brand guide PDF, full-bleed dark to the house standard |
| `templates/build_specimen.py` | the outlined type specimen, driven by brand.json |
| `templates/_guidekit.py` | shared token, font and copy helpers for the document generators |
| `templates/enrich_brand.py` | writes measured contrast and hue separation back into brand.json |
| `templates/verify.py` | the check list, measured at run time |
| `templates/qc_render.py` | rasterises a PDF, measures what only pixels show, writes a contact sheet |
| `templates/qc_images.py` | contact sheets for the logo and every HTML page, desktop and mobile |
| `templates/qc_paginate.py` | exact DOM-level check for elements split by a page break |
| `templates/build_kit.py` | runs the whole pipeline in order and reports every gate |
| `templates/rsvg-convert.js` | Node fallback rasteriser via `@resvg/resvg-js` |
| `templates/sync_agents_md.py` | regenerates `AGENTS.md` from this file. Run it after editing `SKILL.md` |
| `templates/test_glyphkit.py` | self-test for the geometry layer. Every case is a bug that actually happened |
| `examples/shruggietech/` | a real generated instance |
