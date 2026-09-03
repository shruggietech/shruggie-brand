# The Interview

**Design goal: two mandatory inputs. Everything else is a proposal the operator
can accept by saying nothing useful.**

Assume the operator arrives with almost nothing. No palette, no logo, no
positioning doc, possibly not even a firm idea of the audience. That is the
normal case and the flow is built for it.

## The two required inputs

1. The brand or product name.
2. One sentence on what it does.

That is the entire mandatory surface. If the operator supplies only these and
then approves each gate without edits, the output is a complete, conforming,
shippable kit.

## The standing rule

**Propose before asking.** Never present an empty question. Every gate arrives
with a computed recommendation, the reasoning behind it, and the option to
override. A gate that asks "what colour would you like?" has failed.

The operator is allowed to say "yes to all" at gate 1 and skip straight to
gate 5.

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

## Gate 3: The accent

The one real decision, and the agent still proposes it.

The agent presents two or three candidate accents, each with:

- Hex, OKLCH, and hue in degrees
- Measured hue separation from every sibling identity accent and from orange
- Measured contrast on the dark base
- The derived light-surface variant with its measured contrast
- The measured legal foreground for the accent used as a fill
- The derived five-entry chart palette

**How the default is computed.** Take the semantic field of the descriptor
(time, network, money, security, data) and pick a hue that reads for it, then
push it until every check in `canon.color.constrained_rules.identity_accent`
passes. Reject anything within 30° of green 153.0°, cyan 215.7°, blue 253.3°,
or orange 38.3°. Present the survivors ranked by fit.

**What the operator does.** Pick one, or name a hue and let the agent solve
for the nearest legal value. If the operator names a colour that fails a check,
say which check and by how much, then offer the nearest passing value.

## Gate 4: The logo

Three ways in. One way out.

**Path A, the operator supplies a concept.** Any format. Describe back in words
what is load-bearing about it before touching anything; if the operator
disagrees with the description, the redraw would have been wrong and one
sentence just saved the step. Extract its palette for reference only, then
rebuild the geometry from primitives.

**Path B, the agent ideates.** Generate several directions with image generation
to explore the concept space together. This is encouraged and it is the right
use of the tool. It produces conversation, never artwork.

**Path C, the agent proposes directly.** A geometric or monogram mark derived
from the governing principle. Usually the strongest option for a technical
sub-brand and always the fastest.

**The way out, whichever path came in.** The shipped mark is composed in
`<kit>/build/mk_paths.py` from `glyphkit` primitives, on a declared grid, with
its parameters named. Never traced from a generated image. Never typed as path
data. Never a downscaled full mark standing in for a reduced one.

Then run the gate:

    python3 templates/validate_glyph.py <kit>/build/mk_paths.py

**Zero failures is the stopping condition**, and it is the whole point of the
gate. An agent that can view images should also open `qc/logo-sheet.png`,
because taste is not measurable. An agent that cannot is finished at zero
failures and must not pretend otherwise.

If the same check fails twice, the shape is wrong rather than the numbers.
Change one parameter, or go back and pick a simpler shape. Do not generate a
third and fourth variant hoping one passes: that is how a run burns out with
nothing shippable.

**What the operator sees.** The measured report, and, where the tier allows it,
the mark rendered at three sizes on both surfaces with the reduced master shown
at 16 and 32 px. They pick, or send it back with a note.

Full procedure and the failure catalogue: `08-glyph-construction.md`.

## Gate 5: Review

The agent generates the full kit and presents:

- The rendered guidelines page
- Screenshots of the UI kit demo at desktop and mobile
- The type specimen
- `VERIFY.md` with every measured number and a problems count

**What the operator does.** Approve, or point at whatever looks wrong. A
problems count above zero blocks the gate.

## After gate 5

Nothing further is asked. The kit generates completely: tokens, the Next.js
binding layer and registry, the enforcement layer, favicons at every size, the
brand guide PDF, the manifest with checksums.

## Handling the unattended case

If the operator is not responding, do not stall on a gate. Take the computed
default, record the assumption prominently at the top of the output, and
continue. A complete kit with three stated assumptions beats a half kit waiting
on a question nobody is reading.

## What this is really doing

A sub-brand under the variance contract has, in the normal case, exactly two
decisions: one colour and one mark. The interview exists to make those two
decisions well and to keep the operator from being asked about the forty things
that were never theirs to decide.
