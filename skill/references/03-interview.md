# The Interview

**Design goal: two mandatory inputs. Everything else is a proposal the operator
can accept by saying nothing useful.**

Assume the operator arrives with almost nothing. No palette, no logo, no
positioning doc, possibly not even a firm idea of the audience. That is the
normal case and the flow is built for it.

## The required inputs

1. The brand or product name.
2. One sentence on what it does.
3. Explicit affiliation: ownership, showcase permission, parentage, inheritance, endorsement, and service credit.

These are the mandatory facts. Affiliation and showcase permission cannot be inferred or accepted through silence. If the operator supplies them and then approves each creative gate without edits, the output is a complete, conforming, shippable kit.

## The standing rule

**Propose before asking.** Never present an empty question. Every gate arrives
with a computed recommendation, the reasoning behind it, and the option to
override. A gate that asks "what colour would you like?" has failed.

The operator may accept computed positioning and palette proposals tersely, but canonical identity approval and final derivative approval remain explicit decisions over the actual evidence shown at their gates.

## Gate 0: Affiliation and authoritative inputs

Record the six affiliation decisions before any creative proposal. A third-party brand has no ShruggieTech parent or owned-project endorsement. Ask separately whether the brand explicitly adopts the shared house orange pair or selects independent emphasis and action colors, whether it may appear in the public showcase, and whether the fixed neutral service credit is approved. Owned children may select independent colors. Ownership, palette, typography, and endorsement are separate decisions.

Classify every supplied logo item as either a concept or an authoritative master, then record `logo.source_mode` explicitly. A concept informs a new `constructed` identity. An authoritative master requires `authoritative` mode, separate Full and Reduced bindings to approved role-correct PNG or passive SVG inputs, and no construction helper. Declare role, path, format, hash, color-profile status, usage basis, and only the transformations needed by generation; original bytes remain unchanged. For PNG, explicitly approve `alpha` or `luminance` against the current source hash and record the approver and date. Any later binding, hash, source-art, mask, or visible-geometry change requires fresh owner approval. Palette extraction creates evidence only and requires a human approval tied to the current source hash before a candidate becomes canonical.

Record typography mode as `house` or `fixed`. Fixed mode requires approved local faces, measured metadata, hashes, license evidence, and provenance. Use controlled ingestion before generation if a required approved face is not present. Ordinary builds never fetch fonts.

## Gate 1: Name and descriptor

The only input the agent cannot compute.

Ask for both at once. Accept a rough sentence; the agent will tighten it.
Also ask, in the same breath and as optional extras:

- Is there an existing logo concept, sketch, or reference to consider?
- Is there any existing material at all (a repo, a landing page, a deck)?

Both default to "no" and the flow proceeds unchanged.

## Gate 2: Positioning and voice

The agent proposes, in one block:

- The product principle: verb plus object, three or four words, literal
- The descriptor: the technical definition of what the system is, one line

- Governing principle (one sentence, the thing the brand is actually about)
- Category, role, audience, functional descriptor
- Personality table with an Avoid column
- Voice register selected from canon's three lanes
- Whether the shruggie flourish applies

**How the default is computed.** Infer the audience and technical floor from
the descriptor. Pick the register that fits: a security-adjacent or data tool
gets precise-and-dry, an operations tool gets operator-runbook, a
customer-facing product gets direct-and-witty. Default the flourish to off for
anything security-adjacent, financial, or safety-relevant, and to on otherwise.

Both lines are covered in `07-voice.md`. The principle names what a reader can
do or see, so "View your files." and "See what is known." are the shape. The
descriptor names the artifacts the system is made of, not the audience and not a
feature list.

**What the operator does.** Approve, or edit any line. Editing the governing
principle is common and cheap; everything downstream re-derives.

## Gate 3: Formal colors and interface cues

The agent proposes an identity palette and a separate interface cue map. The operator can choose any accessible identity hue, including one used by another owned brand. Record every formal color intended for approved artwork with its source and use; do not assume a UI cue is a logo color.

The agent presents two or three candidate accents, each with:

- Hex, OKLCH, and hue in degrees
- Intended formal identity colors, their source references, and use in marks or brand applications
- Approved formal-color combinations and the exact artwork or application each permits
- Measured contrast on the dark base
- The derived light-surface variant with its measured contrast
- The measured legal foreground for the accent used as a fill
- The derived five-entry chart palette
- The proposed action, warning, error, success, information, focus, selection, and disabled cues in both themes, with foreground pairings and non-color labels, icons, outlines, or attributes

**How the default is computed.** Take the semantic field of the descriptor (time, network, money, security, data) and propose hues that fit the brand. Measure actual contrast and foreground pairing against both surfaces. Compare neighboring brands only as optional creative context. Do not reject a hue because it resembles a sibling or the parent. The cue map must retain accessible and distinguishable state communication through labels, icons, outlines, or attributes.

**What the operator does.** Approve or revise the formal palette and cue map as separate parts of the same creative gate. If a chosen pairing fails AA, show the measured failure and offer an accessible variant. Never turn a sibling-hue preference into a hidden rejection.

**Use example.** A red heart in an approved logo remains an identity color even when the same red is deliberately chosen for an action button. The button needs its action label and measured foreground. Using that logo swatch alone to signal a warning is a misuse; the warning needs its own declared cue plus text or an icon. Include one correct and one misuse example in the Gate 3 approval packet.

## Gate 4A: Logo direction selection

Three ways in. One way out.

**Path A, the operator supplies a concept.** Any format. Describe back in words
what is load-bearing about it before touching anything; if the operator
disagrees with the description, the redraw would have been wrong and one
sentence just saved the step. Extract its palette for reference only, then
rebuild the geometry from primitives. If the operator declares the file an authoritative master instead, preserve it and follow `06-logo-protocol.md` without reconstruction.

**Path B, the agent ideates.** Generate several directions with image generation
to explore the concept space together. This is encouraged and it is the right
use of the tool. It produces conversation, never artwork.

**Path C, the agent proposes directly.** Propose a geometric or monogram mark
derived from the governing principle when that form can express the identity
without exploratory imagery.

**What this decision means.** The operator selects a direction, not production source. The decision is nonbinding and cannot authorize permanent source, derivatives, publication, or consumer integration. Record the selected visual idea and the operator wording, then construct the production candidate.

**The way out for a constructed direction.** Before canonical approval, compose the real shipped Full and Reduced marks in `<kit>/build/mk_paths.py` from `glyphkit` primitives on a declared grid, with named parameters. Never trace a generated image, type path data, switch construction methods after approval, or use a downscaled full mark as the reduced one.

**The way out for approved artwork.** Set `logo.source_mode` to `authoritative`; bind Full and Reduced to their exact approved input IDs and hashes; retain one bound image placement per variant; and prohibit `build/mk_paths.py`, tracing, simplification, reconstruction, and replacement. Generation may only recolor, resize, embed, or place the mark in a lockup when that source explicitly approves the operation. Review `logos/provenance.json` with the rendered sheet.

Then run the geometry gate:

    python3 templates/validate_glyph.py <kit>/build/mk_paths.py

**Zero failures is the stopping condition**, and it is the whole point of the
gate. An agent that can view images should also open `qc/logo-sheet.png`,
because taste is not measurable. An agent that cannot is finished at zero
failures and must not pretend otherwise.

If the same check fails twice, the shape is wrong rather than the numbers.
Change one parameter, or go back and pick a simpler shape. Do not generate a
third and fourth variant hoping one passes: that is how a run burns out with
nothing shippable.

## Gate 4B: Canonical identity approval

Build the complete source-bound packet described in `identity-continuity.md`. It uses the exact production source and renderer and shows Full and Reduced at 256, 64, 32, and 16 pixels on dark, light, black, and white. Include topology, framing, palette qualification, the approved formal combinations and interface cue map from Gate 3, source hashes, renderer settings, and visual difference evidence.

**What the operator sees.** The measured report and the complete production proof matrix. The operator approves the exact candidate or sends it back with a note. Approval records the owner wording, approver, date, scope, source revision, snapshot hash, and packet hash. Any later governed drift invalidates it.

Full procedure and the failure catalogue: `08-glyph-construction.md`.

## Gate 5: Derivative review

The agent generates the full kit and presents:

- The rendered guidelines page
- Screenshots of the UI kit demo at desktop and mobile
- The type specimen
- `VERIFY.md` with every measured number and a problems count

**What the operator does.** Approve, or point at whatever looks wrong. A
problems count above zero blocks the gate.

Gate 5 reviews only derivatives made from the promoted canonical source. It cannot introduce or reconstruct production geometry. A master change returns to Gate 4B rather than being accepted here.

## After gate 5

Nothing further is asked. The kit generates completely: tokens, the Next.js
binding layer and registry, the enforcement layer, favicons at every size, the
brand guide PDF, the manifest with checksums.

## Handling the unattended case

If the operator is not responding, creative recommendations may use computed defaults after the required affiliation, publication permission, authoritative-input status, palette approval, and typography mode are already explicit. Never infer ownership, permission to publish, source usage rights, approval, or credit language. Stop when any of those decisions is missing.

## What this is really doing

A sub-brand under this variance contract has, in the normal case, exactly two
decisions: one colour and one mark. The interview exists to make those two
decisions well and to keep the operator from being asked about the forty things
that were never theirs to decide.
