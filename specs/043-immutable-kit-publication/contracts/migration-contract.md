# Migration Contract

Migration guidance is generated from the governed release-impact record plus the kit's bundle record.

## Required classifications

Every release classifies these surfaces: identity, palette semantics, typography, platform assets, Web/React contracts, egui contracts, documentation, and recovery.

- `required`: an existing consumer of the affected surface must make a compatibility change.
- `optional`: the release supplies a new or improved capability that a consumer may elect to adopt.
- `unaffected`: the surface requires no migration for this release.

## Required statements

Guidance states whether approved identity changed and reports the brand version separately from the kit package identity. Hosted, bundled, portable, and release presentations MUST derive identical classifications from the same source record.

## Prohibited evidence

The record and generated guidance MUST NOT request or store consumer identity, adoption state, productivity, elapsed time, correction rounds, escaped defects, utility scoring, or handover evidence.
