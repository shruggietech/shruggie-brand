# Data model

## Reference entry

An entry is a `### REF-<DOMAIN>-<NAME>` heading in `skill/references/references.md`, followed by a source title/URL, classification, applicable scope or edition, local use, and caveat. ID is unique, stable, and independent of display title. The Markdown file is canonical; no duplicate editorial catalog is maintained. External URL status is review evidence, not local citation validity.

## Local citation

A manual or packaged skill link targets `references.md#ref-...`. The deterministic hosted transform maps it to `/docs/references/#ref-...`. Validation rejects unknown or duplicate IDs and citations to missing files. The source citation remains navigable in the offline package.

## Guideline fact

The generated `enforcement/documentation-facts.json` uses documentation contract 1.1.0 and fields for brand, bundle, versions, bindings, rules, authority, verification, recovery, hosted, and bundled scopes. For each declared override, `rules.default_references` contains the exact dark and light default aliases selected by the pinned interface canon plus that canon's kit path. The hosted portal embeds these facts and the public static JSON resource copies them byte for byte. No separate fact is authored in the site.

## Reader-task audit record

A verification row identifies brand and topic/conditional state, reader question, answer, next action, source authority, observation, and repair disposition. The matrix covers all eight production brands and topic classes and records representative manual and portable/PDF tasks.
