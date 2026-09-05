# Voice

Voice is a **constrained** axis. A sub-brand picks a register; the prohibitions
apply to all of them and are enforced by `verify`.

## The three registers

| Register | Exemplar | Sounds like |
| --- | --- | --- |
| direct-witty | ShruggieTech | confidently scrappy, "we" to "you", sparing humour, punchy two-beat sentences |
| precise-dry | fragcap | technically literate, states prerequisites and limits before convenience |
| operator-runbook | go-schedule | exact nouns, explicit policy, the tone of someone handing over a procedure |

**How the interview picks one.** Security-adjacent, financial, or
safety-relevant products get precise-dry. Infrastructure and scheduling tools
get operator-runbook. Customer-facing products get direct-witty. The operator
overrides in one line.

## Universal prohibitions

These apply in every register and `verify` fails the build on them.

### The contrasting device

Do not build sentences out of `X, not Y`.

> evidence, not theatre
> an instrument, not a weapon

It is the most recognisable tell of machine-written copy, it reads as borrowed
confidence, and it usually substitutes a shape for an argument. Its relatives
go too: `X over Y`, `rather than merely Z`, and the coda tacked onto a sentence
that had already finished (`... never decorate`).

State the thing you mean. If the contrast genuinely carries information, give
it its own sentence.

This is a ShruggieTech house rule with real history: fragcap 1.0.0 led with
"instrument, not weapon" as its governing principle, and 1.1.0 replaced it and
added a build check.

### Em-dashes

House style. Prefer parentheses, commas, or standard hyphens. `verify` counts
them and reports the count.

### Corporate filler

`synergy`, `leverage` as a verb, `best-in-class`, `revolutionary`,
`effortless`, `seamless`, `unlock`, `supercharge`, `game-changing`.

### Structural tells

- Testimonials and invented quotes
- Feature grids standing in for an explanation
- Manufactured urgency
- Generalised calls to action with no object
- Emoji in product copy

## Preferred language

| Prefer | Avoid |
| --- | --- |
| you, your project, your machine | the operator, the end user |
| requires, emits, records, filters | unlocks, dominates, supercharges |
| supported, experimental, unknown | flawless, revolutionary, effortless |
| capture, observe, inspect, decode | intercept, attack, exploit |

## Rules that hold everywhere

- **Sentence case** for body. Title Case for nav and buttons. Uppercase
  reserved for compact labels, eyebrows, and table metadata.
- **State prerequisites before instructions.**
- **Label unknowns as unknowns.** Distinguish supported behaviour, inferred
  behaviour, and behaviour nobody has checked.
- **Name the sharp edges.** Where a capability has an obvious misuse, say so
  and say where the project's line falls. Readers technical enough to use the
  thing will work it out anyway, and hedging in front of that audience only
  costs credibility. fragcap's dual-use section is the reference implementation.
- **Product name casing is a decision, and it is binding.** fragcap is always
  lowercase, including at the start of a sentence. Record the rule in the kit
  and let `verify` check it.

## The two lines every kit has to get right

**The product principle** is the line on the cover, on the guidelines page and
in the specimen. Verb plus object, three or four words, literal, and something a
person could say out loud without wincing.

> View your files.  ·  See what is known.

It names what the reader can do or see. It does not describe a benefit, reach
for a metaphor, or explain the architecture. If it needs a second clause it is
not the principle yet.

**The descriptor** is the sentence underneath. It is the technical definition of
what the system is, at roughly the length of the principle plus a line.

> Text, source code, images, PDFs, and office documents.
> An evidence-backed knowledge graph and a policy-enforcing context compiler.

Name the artifacts, not the audience and not the feature list. A descriptor that
says who it is for, or strings together five nouns from the domain model, reads
as word salad and goes stale the moment the specification moves. If the product
has two halves, name both halves.

## The guide describes the brand, never the product

A brand guide that opens with a product summary, an in-scope list and a roadmap
is a specification with the wrong cover on it. It goes stale the first time the
spec moves, and it answers a question nobody opened a brand book to ask.

What belongs: the name and where it came from, how to write it, the register, the personality and the promises, the mark, the palette, the type, the declared affiliation line when one exists, and the one place the brand could mislead somebody.

What does not: what the product does today, what is in scope this quarter, the
architecture, and anything with a version number attached to it.

## The shruggie flourish

The emoticon and "We'll figure it out." Opt-in per sub-brand, at most one
moment per view, always in the identity accent.

Default it **off** for anything security-adjacent, financial, or
safety-relevant. fragcap declines it and is right to: a tool that reads game
network traffic should not wink at you.

## The endorsement

An owned child may explicitly select "A ShruggieTech project", set in its declared mono family, uppercase, positive tracking, visually subordinate, and outside the product logo's clear space. A third-party identity cannot use that phrase. It may explicitly select "Brand system by ShruggieTech" as a neutral service credit or select no credit. Generated copy must never invent an affiliation line.

## Landing-page register

The default structure for a technical sub-brand, drawn from fragcap:

1. State what the tool is, in one sentence, using the functional descriptor
2. Show one worked invocation with representative output
3. Name the prerequisite plainly
4. Link to documentation

No testimonials, no feature grid, no urgency. `ui_kits/fragcap-web/`
demonstrates it.

## What verify scans

`verify.py` runs the banned patterns across every brand-copy file in the kit
(README, SKILL.md, guidelines, UI kit copy) and fails on a hit. The em-dash
count is reported rather than failed, because a legitimate use exists and the
number is what matters.

A pattern that produces false positives gets narrowed, never disabled. The
check earns its place by being annoying in the right way.
