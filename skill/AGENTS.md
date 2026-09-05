<!-- GENERATED from SKILL.md by templates/sync_agents_md.py. Do not edit. -->

# Agent instructions: shruggie-brandbuilder

You are working inside the `shruggie-brandbuilder` skill, or in a project that
vendored it. This file is the entry point for hosts that do not read skill
frontmatter; `SKILL.md` carries the same content plus that metadata.

Read this file, then follow the routing table below into `references/`. Paths
are relative to this directory. Everything is invoked as a shell command, so
nothing here depends on a particular host's tool names.

Before anything else:

    python3 templates/probe.py <kit-dir>

If `python3` is not on PATH, try `python`. If `coloraide` will not import, stop
and say so: contrast numbers are measured rather than typed, so no colour work
can proceed without it.

---

Builds brand kits for ShruggieTech-owned and third-party identities. Every kit declares ownership, public showcase permission, parentage, inheritance, endorsement, service credit, typography mode, and any authoritative supplied inputs explicitly before generation.

## Start here

    python3 templates/probe.py <kit-dir>

That tells you what this machine can do before you plan around it. Then ask two
questions and nothing else up front:

1. What is the brand or product called?
2. What does it do, in one sentence?

Then follow `references/03-interview.md`. Ownership, showcase permission, inheritance, usage rights, and palette approval have no inferred default. Every creative gate after the required contract arrives with a computed proposal, so an operator who approves everything still gets a complete kit. **Propose before asking.** A gate that presents an empty creative question has failed.

Offer two optional extras in the same breath, both defaulting to no: an existing
logo concept to consider, and any existing material at all.

## Routing

| The operator wants | Read, in order |
| --- | --- |
| A new sub-brand kit | `03-interview.md`, `00-variance-contract.md`, `02-kit-anatomy.md`, then generate |
| A third-party or client brand | `03-interview.md` affiliation gate, `00-variance-contract.md`, `07-voice.md`, then generate |
| A supplied mark or wordmark | `06-logo-protocol.md` authoritative-input path, then `03-interview.md` palette approval gate |
| A fixed font requirement | `03-interview.md` typography gate, `09-portability.md`, then run `templates/ingest_font.py` explicitly |
| To pick a colour | `01-canon.json` `color.constrained_rules`, then propose candidates with measured numbers |
| A logo | `08-glyph-construction.md` first, then `06-logo-protocol.md`. Do not draw before reading it |
| Next.js or shadcn wiring | `05-shadcn-binding.md`, then run `templates/gen_nextjs.py` |
| To write copy | `07-voice.md` |
| To know what may change | `00-variance-contract.md` |
| To run somewhere unusual | `09-portability.md` |
| To check a kit | `templates/verify.py` |
| To fix an existing kit | Run verify first, then work the problems list |

## The rules that matter most

**Declare affiliation before creative work.** Ownership, showcase permission, parentage, inheritance, endorsement, and neutral service credit are separate fields. Missing state stops generation. A third-party brand has no ShruggieTech parent or owned-project endorsement. Neutral credit is optional and fixed. House inheritance explicitly adopts ShruggieTech semantic orange. Independent inheritance requires brand-specific emphasis and action colors.

**One colour decision and one logo decision in house mode.** Under the ordinary owned-brand variance contract, everything else is inherited or derived. Authoritative supplied marks and fixed font requirements are explicit exceptions. They require hashes, provenance, usage or license evidence, and approval before generated use.

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

**Bundle fonts. Never fetch them at build time.** House mode uses the approved local faces. Fixed mode uses only declared local faces whose hash, family, weight, style, format, license, provenance, and usage status pass validation. Network retrieval happens only through the explicitly invoked `templates/ingest_font.py` command and completes atomically before a build begins.

**Preserve authoritative supplied identity files.** A supplied master stays byte-identical. Declare its role, path, format, SHA-256, color-profile status, usage basis, and approved transformations. Palette analysis produces evidence only. A human approval must bind a selected candidate to the current source hash before that color can be canonical.

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

It validates the explicit contract first, then probes, runs the glyph gate, and stops before publishable output on any failure. Individually:

    python3 templates/validate_brand.py <brand.json>          # affiliation, inputs, type
    python3 templates/probe.py          <kit>                 # capability tier
    python3 templates/validate_glyph.py <brand.json>          # the mark, measured
    python3 templates/analyze_inputs.py <brand.json> <kit>    # generated evidence
    python3 templates/enrich_brand.py   <brand.json>          # measured values written back
    python3 templates/build_specimen.py <brand.json>          # outlined type specimen
    python3 templates/gen_vanilla.py    <brand.json> <kit>    # tokens, styles.css, components
    python3 templates/gen_nextjs.py     <brand.json> <kit>    # globals.css, registry, fonts, provider
    python3 templates/gen_enforcement.py <brand.json> <kit>   # AGENTS.md, oxlint, stylelint
    python3 templates/gen_logo.py       <brand.json> <kit>    # colourways, lockups, native icon suites
    python3 templates/gen_guidelines.py <brand.json> <kit>    # the guidelines page
    python3 templates/gen_guide_pdf.py  <brand.json> <kit>    # the brand guide, full-bleed dark
    python3 templates/verify.py         <kit>                 # measured VERIFY.md
    python3 templates/scan_affiliation.py <brand.json> <kit>  # false claims
    python3 templates/qc_images.py      <kit>                 # logo and page contact sheets
    python3 templates/qc_render.py      <kit>/brand-guide.pdf --expect-ground dark
    python3 templates/qc_paginate.py    <kit>/build/*.print.html

`gen_logo.py` does not invent geometry. Copy `templates/mk_paths.example.py` to `<kit>/build/mk_paths.py`, edit the parameter block, run the gate, write the paths into `brand.json`, and the generator produces every colourway, the outlined wordmark, the lockups, all rasters, and categorized application-icon suites for web, Android, iOS and iPadOS, macOS, and Windows. `icons/manifest.json` is authoritative; `favicons/` is a byte-identical web compatibility mirror.

When an approved master already exists, do not route through reconstruction. Declare it under `authoritative_inputs`, preserve its bytes, authorize only the needed transformations, and let validation connect each imported logo image to its source record. Use `templates/ingest_font.py --help` for the separate fixed-font ingestion contract. Ordinary generation must stay offline.

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
| `references/canon.schema.json` | authoring schema for explicit affiliation, inheritance, typography, supplied inputs, and approvals |
| `references/02-kit-anatomy.md` | what a complete kit contains, file by file |
| `references/03-interview.md` | the five gates and how each default is computed |
| `references/04-toolchain.md` | probe script and the asset-to-tool matrix |
| `references/05-shadcn-binding.md` | token to slot map, registry authoring, the radius deviation |
| `references/06-logo-protocol.md` | what a mark must be: grid, lockups, favicons, prohibitions |
| `references/07-voice.md` | registers, the principle and descriptor shapes, banned rhetoric |
| `references/08-glyph-construction.md` | how to produce a mark that is not wrong |
| `references/09-portability.md` | capability tiers and the cross-provider rules |
| `templates/probe.py` | what this machine can do, as JSON the pipeline reads |
| `templates/brand_contract.py` | shared fail-closed affiliation, supplied-input, palette, and typography contract |
| `templates/validate_brand.py` | first-step runtime contract validation |
| `templates/analyze_inputs.py` | deterministic generated audit and palette evidence |
| `templates/ingest_font.py` | explicit bounded and atomic local or HTTPS font ingestion |
| `templates/scan_affiliation.py` | generated-output scan for false third-party ownership claims |
| `templates/glyphkit.py` | mark primitives, exact bbox, optical centring. Standard library only |
| `templates/validate_glyph.py` | the measured geometry gate. No renderer, no vision |
| `templates/mk_paths.example.py` | copy to `<kit>/build/mk_paths.py` and edit the parameters |
| `templates/gen_vanilla.py` | tokens, styles.css and components, generated rather than hand-written |
| `templates/gen_nextjs.py` | the whole `nextjs/` layer |
| `templates/gen_enforcement.py` | `AGENTS.md`, oxlint and stylelint configs |
| `templates/gen_logo.py` | colourways, outlined wordmark, lockups, rasters, categorized application icons |
| `templates/iconkit.py` | platform matrices, composition, native containers, manifests, and compatibility aliases |
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
