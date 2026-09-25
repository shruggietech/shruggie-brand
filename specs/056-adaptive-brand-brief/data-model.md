# Data Model

## Working brief (private authoring evidence)

Each topic records `facts` (operator-supplied or cited source), `constraints` (explicit fixed choices), `proposals` (agent suggestions and rationale), and `unresolved` (questions without approval). Topics cover purpose, audience, positioning, voice, references, identity, lockups, social copy, formal palette, interface cues, typography, deliverables, and affiliation. Rich input fills fields before follow-up questions; sparse input retains unresolved fields.

## Social-copy decision

Fields: exact `slogan`, optional exact `description`, `layout` (`slogan-only` or `slogan-and-description`), approved line breaks, source/approver evidence, and status. A descriptor or brand idea never silently populates these fields. Final publication migration belongs to #281.

## Creative approval state

Gate 1 binds exact production source and proof evidence. Gate 2 binds reviewed provisional derivatives and authorizes final fundamentals. Source change returns to Gate 1 and invalidates affected Gate 2 evidence; derivative or social-copy change returns to Gate 2. Pending or rejected state carries no approval evidence and cannot publish.
