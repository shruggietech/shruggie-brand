# The Interview

Build an adaptive brief before constructing a brand. Accept substantial source material at the outset or develop the brief conversationally. There is no question ceiling and no minimum-input shortcut. Reuse answers already present in supplied files, links, or prior discussion. Ask a follow-up only when its answer changes a named design decision; say which decision it informs. Invite additional context throughout. An unanswered question stays unresolved, never approved by silence.

## Working brief

Keep a private, reusable record with four separate columns for every topic: **facts** (operator statements and cited source), **constraints** (what the operator explicitly fixes), **proposals** (the agent's recommendation with rationale), and **unresolved** (choices still awaiting an answer). Do not replace a fact with a proposal or turn an unanswered proposal into an approved constraint. Record source, date, and exact operator wording for approvals. The working brief is review evidence, not a public brand contract or an extra approval gate.

For machine-checkable private evidence, store `schema_version`, the thirteen named `topics` below, and `social_copy` in a JSON brief under ignored private output. Each topic has string arrays named `facts`, `constraints`, `proposals`, and `unresolved`. `social_copy` stays `{"status":"unresolved"}` until the exact text, layout, line breaks, approval source, approver, and date are explicitly decided. Run `python templates/authoring_brief.py <private-brief.json>` before preparing Gate 2. The validator checks structure and explicit status; it does not invent missing answers.

| Topic | Decision it informs | Useful discovery questions |
| --- | --- | --- |
| Purpose and success | What the identity must explain and achieve | What does the offering do? What should a customer understand, feel, or do? What would make the kit successful? |
| Audience and setting | Reading context and language needs | Who will encounter it, in which markets, languages, and settings? What do they already understand? |
| Positioning | Distinctive, supportable claims | What distinguishes it from alternatives? Which claims can be substantiated? |
| Personality and voice | Copy register and examples | Which traits, tone examples, and words fit? Which attitudes or styles must be avoided? |
| References and dislikes | Direction to explore or avoid | Which visual examples appeal or repel, and why? References are not artwork to copy. |
| Existing identity and constraints | Preservation versus new construction | Is this a new identity, refresh, or preservation job? Which names, marks, colors, faces, licenses, and files are fixed? |
| Logo and lockups | Source roles and deliverables | Which Full/Reduced marks, standalone wordmarks, wide/stacked lockups, sizes, backgrounds, and tagline combinations are needed? |
| Social share copy | Exact image text and composition | What exact approved slogan appears beside the full-color wordmark or approved supplied wordmark lockup? Is the image slogan-only or slogan-and-description on a separate line? What exact description and line breaks are approved? |
| Formal brand palette | Identity artwork colors | Which colors express the identity or appear in approved artwork? Which combinations and applications are approved? |
| Interface cue palette | Functional state communication | Which action, warning, error, success, information, focus, selection, and disabled roles are needed on dark and light surfaces? What labels, icons, or outlines accompany them? |
| Typography | Tone and script coverage | Which scripts, weights, local-font constraints, readability contexts, and fixed faces matter? |
| Deliverables and uses | Relevant outputs and Gate 2 examples | Which web, app, print, social, packaging, or merchandising uses are actually required? Which examples must be reviewed? |
| Relationship and attribution | Truthful affiliation and publication | Who owns the brand? What parentage, inheritance, endorsement, public showcase permission, source rights, and service credit are explicitly authorized? |

For a richly specified job, fill the brief from supplied material first and ask only about gaps or conflicts. For a sparse job, explore the topics progressively and label proposals as proposals. "Undecided" is a valid working state; offer a concrete option for review without treating it as approval. Distinguish an operator's formal brand colors from functional interface cue colors even when one swatch is deliberately used in both roles. Every brand, including an owned sub-brand, may choose an independent accessible palette; shared colors are opt-in.

## Social-copy decision record

Record the exact approved slogan, its source and approver, the explicit `slogan-only` or `slogan-and-description` choice, and any exact approved description and line breaks. Leave missing fields unresolved. Neither `descriptor` nor `brand_idea` is automatically a slogan. A social share image is its own composition, not a wide or stacked logo lockup. Show the chosen composition in the Gate 2 packet before final kit compilation. Existing generated social images require a separate governed source migration; do not claim that historical copy has been approved merely because it exists in a brand file.

## Work before creative approval

First establish affiliation and usage facts: ownership, parentage, inheritance, endorsement, public showcase permission, source rights, and service credit. These are explicit operating facts, not a numbered creative approval gate. Classify supplied logo material as a concept or authoritative master. An authoritative Full and Reduced source needs role-correct immutable input bindings, hashes, usage basis, approved transformations, and mask approval where applicable. Fixed typography needs approved local faces, metadata, hashes, and license evidence. Missing rights or publication permission stop the affected work.

Explore positioning, voice, mark direction, formal colors, interface cues, typography, and applications with the operator. Present reasoned options and measured accessibility evidence. Direction selection is not canonical approval. A selected sketch, image-generation result, or traced reference cannot authorize permanent source or derivatives. A supplied authoritative master remains byte-identical. Follow `06-logo-protocol.md`, `08-glyph-construction.md`, and `identity-continuity.md` for the applicable source mode.

## Gate 1: Logo source approval

This is the first mandatory creative approval stop. Present the real proposed production Full and Reduced masters, source bindings or construction helper, framing, formal palette qualification, renderer settings, source hashes, topology, and the complete 32-proof production matrix at 256, 64, 32, and 16 pixels on dark, light, black, and white. Explain exactly what will be shipped. The operator explicitly approves that exact source-bound packet or sends it back for revision. Store the decision in the canonical continuity record and `approval_ledger.gate_1`; promotion copies approved bytes without reconstruction. Concept selection alone cannot satisfy this gate. Source, helper, palette, renderer, or proof drift invalidates approval and returns here. Silence is never approval.

## Assemble provisional fundamentals

After Gate 1, render private, provisional derivatives from the promoted source using the production path. Review wide and stacked lockups, standalone wordmark where applicable, formal brand palette with approved artwork combinations, separate interface cue palette, typography, usage rules, and representative applications. Show the exact chosen social share image with its approved slogan, optional description, and line breaks as a separate preview from the wide and stacked lockups. If an approved supplied lockup contains the wordmark, use it; do not invent a standalone wordmark. The packet must identify the generated source and derivative manifest being reviewed.

Provisional review material may live in ignored private output such as `dist/`; it is not a final publishable kit. Do not publish a pending-Gate-2 kit or expose its files through the site, registry, or release. Run the applicable geometry, contrast, and provenance checks on provisional material and fix failures before requesting approval. Automated checks are verification steps, not extra creative approval gates.

Build a `gate-2-packet.json` beside the private review files, with `schema_version: 1`, the approved Gate 1 `source_sha256`, `gate_2.status: pending`, `public_projection_enabled: false`, a verbatim copy of the approved `social_copy` record, and an `assets` map. The source digest must equal the current approved canonical binding in the brand's continuity record and approval ledger. Supply checksummed Full and Reduced marks, wide and stacked lockups, a separate `social-share-image`, formal palette, interface cues, typography, representative application, and derivative manifest. Each asset uses a contained relative `path` and `sha256`. Run `python templates/authoring_brief.py <private-brief.json> --gate-2 <private-gate-2-packet.json> --brand-root <approved-brand-source-dir>`; the validator checks current source approval, rejects missing, stale, invalid, or escaping files, and requires separate paths and content for wide, stacked, and social compositions. The operator still inspects the actual preview and approves or rejects it. This private packet does not replace the production ledger or the separately governed final image-role migration.

## Gate 2: Brand fundamentals approval

This is the second and final mandatory creative approval stop. Present one concrete packet containing the provisional derivatives above, including the distinct social share image, plus measured accessibility results and the exact source/manifest references. The operator explicitly approves the assembled fundamentals before final kit compilation, or rejects the affected decisions for revision. Record approved derivative evidence in `approval_ledger.gate_2`. A changed social slogan, description, layout, lockup, palette application, or other reviewed derivative returns to Gate 2; a changed production master returns to Gate 1 and then requires a fresh Gate 2 review. Silence is never approval.

Only after both gates are approved may the final kit be compiled, verified, and packaged. Every production kit still needs zero `verify.py` problems and zero `validate_glyph.py` failures. Publication remains a separate authorization and release process, not a third creative approval stop. A missing operator response leaves the affected gate pending; no unattended default or timeout bypasses it.

## Scenario checks

- **New identity**: Explore directions, then present actual production sources at Gate 1 and assembled fundamentals at Gate 2.
- **Supplied authoritative artwork**: Preserve source bytes and role bindings; review the exact bound sources at Gate 1 and only permitted derivatives at Gate 2.
- **Sparse input**: Ask decision-relevant follow-ups; unresolved claims and social copy remain pending.
- **Rich input**: Reuse supplied facts and constraints; ask only about gaps, conflicts, and approvals.
- **Revision**: Return to the affected gate, and to Gate 1 whenever governed source changes.
- **Nonresponsive operator**: Retain pending state; do not infer either approval or permission to publish.
