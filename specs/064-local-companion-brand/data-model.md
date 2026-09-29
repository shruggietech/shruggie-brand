# Data Model: Local Companion Brand Publication

## Governed brand source

`brands/local-companion/brand.json` declares the product identity, affiliation, graphite and indigo roles, accessible light roles, typography, Full and Reduced logo paths, derivative settings, guidance, and public copy. `build/mk_paths.py` constructs the exact approved paths from `glyphkit` primitives. `identity-continuity.json` binds the approved identity snapshot, source inventory, renderer, palette qualification, and 32 proof hashes. The source may add derivative guidance or social copy after Gate 1 only when the governed snapshot and canonical source binding stay unchanged and the record's brand-file hash is updated.

## Approval states

| State | Required evidence | Permitted next work |
| --- | --- | --- |
| Direction selected | Owner's lower-right calm-orbit choice | Construct exact Full and Reduced masters |
| Canonical candidate | Source bytes, palette qualification, renderer, geometry, 32 proofs | Ask for Gate 1 approval |
| Canonical approved | Owner wording, date, scope, packet hash, source snapshot | Atomic source promotion |
| Promoted | Validated `brands/local-companion/` source and continuity record | Private derivative generation |
| Derivative candidate | Lockups, icons, palette, interface cues, type, application example, social image and exact copy, manifest | Ask for Gate 2 approval |
| Derivative approved | Owner decision bound to derivative manifest and social image bytes | Final kit compilation |
| Publication eligible | Zero glyph failures, zero `verify.py` problems, release and site audits | Tag-built release and Pages deployment |

Governed identity drift after canonical approval returns the lifecycle to a new candidate. Derivative drift after Gate 2 requires renewed derivative approval. Silence never advances a state.

## Derivative manifest

The private Gate 2 packet records each reviewed output's role, relative path, and SHA-256, plus the Gate 1 canonical source binding and exact social copy with line breaks. The validator checks visual file formats and PNG integrity from those paths. It contains only synthetic application material and approved public product language. The generated kit's public manifest is produced by the repository pipeline after Gate 2.

## Verified kit and publication record

`dist/local-companion/` is rebuilt from committed source. Its manifest, registry, interface bindings, platform icons, guidance, and ZIP archive are generated output and never committed. The release record binds the builder version, Local Companion version, source revision, asset inventory, SHA256SUMS, and Pages artifact. The public site's catalog and per-brand pages are projected from that verified kit.
