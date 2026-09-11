# Contract: Source Preservation and Transformations

## Source rules

Approved identity files are committed byte for byte. Passive SVG bytes remain unchanged. Portable PNGs remain unchanged and bind an owner-approved alpha or luminance mask only when masking is explicitly permitted. PDF, JPEG, WebP, website images, screenshots, and extracted document objects remain reference-only unless a new owner decision changes their role.

Logo lettering is artwork. Font discovery does not authorize rebuilding, respacing, outlining, or substituting it.

## Proposed allowed operations

Each source receives a separate closed list selected from:

- exact byte copy;
- proportional resize;
- passive-SVG rasterization without geometry changes;
- exact-alpha placement on an approved solid surface;
- non-cropping placement inside approved bounds;
- lossless platform packaging with pixel-equivalent visible content;
- palette analysis that produces evidence only.
- owner-approved single-ink derivation from an unchanged approved light-background master by suppressing the supplied soft shadow, turning near-white artwork into transparent knockouts, preserving narrow antialias transitions, and recoloring remaining visible pixels to exact black or white.
- exact byte copy of supplied colored-heart favicon and platform targets at their declared sizes;
- derivation of missing modern colored app-icon sizes from unchanged `heart.svg` by suppressing its soft source shadow and fitting the mark to the safe-area framing measured from supplied 192 and 310 pixel platform masters.

The following are denied by default: tracing, simplification, path normalization, live-type reconstruction, unapproved re-keying, unapproved recoloring, unapproved masking, crop changes, view-box changes, outline generation, invented monochrome, invented reduced variants, effects, texture removal outside the approved single-ink shadow suppression, and gradient flattening.

## Derivative evidence

Every permitted derivative records source hash, operation list, renderer and settings, dimensions, framing, output hash, and comparison evidence. Production validation runs at the standalone logo boundary, aggregate build boundary, and final verifier boundary.

## Missing deliverables

A deliverable without an approved non-creative source path is `blocked`, not silently omitted or fabricated. Gate 1 decides whether the operator will supply a source, approve a narrowly defined transformation, or accept the omission.
