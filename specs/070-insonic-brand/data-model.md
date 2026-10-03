# S070 Data Model

Use existing versioned schemas and runtime validators. No new schema is introduced.

| Entity | Authority and fields | Validation |
| --- | --- | --- |
| Private brief | Thirteen topics, each with facts/constraints/proposals/unresolved arrays; independent messaging statuses; exact social-copy record. | authoring_brief validator; no candidate text in approved fields. |
| Brand source | Name/domain, owned affiliation, independent inheritance, house typography, explicit colors and messaging, logo source mode and approval ledger. | brand_contract and canon schema. |
| Geometry helper | Named grid/construction parameters and Full/Reduced paths produced through glyphkit. | helper AST/provenance validation and validate_glyph. |
| Canonical identity | Source inventory/hash, source class, framing, topology, palette qualification, renderer, 32 proofs and comparison artifacts, exact owner approval. | identity_continuity; record and normalized source digests. |
| Fundamentals packet | Current Gate 1 binding, pending Gate 2, private projection flag, exact messages, checksummed distinct required assets. | authoring_brief Gate 2 validator with approved brand root. |
| Final kit | Generated asset families, local fonts, tokens, platform contracts, guides, manifest and measured evidence. | verify and render/host checks. |
| Public projection | Generated catalog/routes/metadata/registry/assets/downloads from the verified kit. | publication/site/registry checks and live release checksum. |

State order: exploratory, direction-selected, canonical-candidate, canonical-approved, promoted, derivative-approved, publication-eligible. Missing decisions retain pending state. Governed source drift invalidates Gate 1; reviewed derivative drift invalidates Gate 2. Every messaging role independently transitions from unresolved to approved or absent through owner wording and intended-use evidence.
