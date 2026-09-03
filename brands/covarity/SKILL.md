---
name: covarity-brand
description: Apply the Covarity brand system to product interfaces, documentation, repositories, and generated assets.
license: Proprietary. Internal ShruggieTech use.
compatibility: Requires a filesystem for bundled fonts and assets. The optional verification scripts require Python 3.
metadata:
  version: 1.0.0
  canon: 1.0.0
  parent: ShruggieTech
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Covarity brand

Read `README.md`, `brand.json`, and `enforcement/AGENTS.md` before producing Covarity material.

The product principle is **See what is known.** Covarity is two products under one identity:
`covarity-knowledge` holds sources, evidence spans, entities, claims, and relationships with
their provenance intact, and `covarity-context` compiles task-scoped instructions and working
memory for agents. The voice is precise, plain, and unhurried. Lead with the evidence, the current state, or the
boundary between the two systems. Name the source and the span. Say unknown when support
is missing, and give an unsupported question the same visual weight as an answered one.

Do not write about memory, minds, understanding, or knowing a person. The product records
what a source says and where it says it, and it stops there.

Use the supplied logo masters without recomposition. The mark is an aperture C on a
1000-unit grid: one 168-unit ring from 88 to 318 degrees in Covariance Purple, a 36-degree
terminal segment from 42 to 78 degrees in the inherited orange, and a 10-degree radial slot
between them. Never close the aperture or the slot, never swap the two inks, and never set
the C in a typeface. Below 32 px use the reduced master, which drops the slot and the
orange segment.

Write the name as `Covarity` in prose, `covarity` in identifiers, and `covarity.ai` only in a
URL or where an unrelated company of the same name could be confused with this one. Never set
`Covarity.ai` in a wordmark or a headline.

Use the semantic tokens and the bundled components. Covariance Purple is the identity
accent and carries links, focus, and selection. The inherited orange keeps its emphasis and
warning role and never stands in as a second accent.

Run `build/verify.py` after any kit change. A nonzero problem count blocks delivery.
