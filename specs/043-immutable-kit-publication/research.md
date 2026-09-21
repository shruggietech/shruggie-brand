# Research: Immutable Kit Publication

## Decision 1: Supersede unpublished BrandBuilder 1.3.0 with 2.0.0

**Decision**: Publish the incompatible archive and consumer-contract changes as BrandBuilder `2.0.0`. Fold all work currently staged under the unpublished `1.3.0` changelog heading into the complete `2.0.0` boundary.

**Rationale**: Canonical archive names and generated consumer records are public integration contracts. Changing both is an incompatible output-layout change under the repository's version policy. Because no `v1.3.0` tag or release exists, correcting the version before publication creates no released-version rewrite.

**Alternatives considered**:

- Keep `1.3.0`: rejected because it would label an incompatible package-layout change as minor.
- Publish `1.3.0`, then fix identity in `2.0.0`: rejected because it would knowingly publish ambiguous archive identities.

## Decision 2: Deploy production Pages only from an exact release tag

**Decision**: Keep `main` and pull-request builds as downloadable CI candidates, but permit the production Pages deployment only after the exact version tag has passed release preflight and its GitHub release has been published from the same verified build.

**Rationale**: The production site currently advances on `main` while its skill action resolves through a moving `releases/latest` destination. Tag-backed publication makes the site, skill archive, kits, checksums, source revision, notes, and release record one atomic delivery.

**Alternatives considered**:

- Continue deploying `main` and label it preview: rejected because the existing public URL is the production channel.
- Query the latest GitHub release at runtime: rejected because the site is a static export and a moving lookup weakens reproducibility.

## Decision 3: Generate exact release destinations from one publication record

**Decision**: Site preparation emits an exact release record containing the release version, tag, source revision, skill archive, and canonical kit packages. The UI and site verifier consume that generated record. Production validation rejects `latest` links and any mismatch.

**Rationale**: This keeps the static site within the constitution's generated-input boundary and removes independently authored version facts.

**Alternatives considered**:

- Hardcode a versioned URL in the React component: rejected because each release would require duplicate manual edits.
- Retain `/releases/latest`: rejected because it can change without rebuilding the production site.

## Decision 4: Use brand version plus BrandBuilder version as the human-readable package identity

**Decision**: The canonical kit package ID is `<brand-slug>-brand-<brand-version>-bb<brandbuilder-version>`, and the archive is `<package-id>.zip`. The complete bundle record also includes the independent canon, recipe, adapter, source revision, and checksum facts.

**Rationale**: A compiler release changes whenever governed output contracts change, so the pair distinguishes public package generations while keeping filenames readable. The richer tuple remains available for validation and migration decisions.

**Alternatives considered**:

- Hash-only names: rejected because they hide the useful brand and compiler identity and complicate release navigation.
- Full component tuple in the filename: rejected because it creates long, unstable filenames and duplicates the bundle record.
- A mutable brand-only compatibility alias: rejected because the same URL could resolve to different bytes.

## Decision 5: Add one generated bundle record and one governed release-impact record

**Decision**: Every generated kit contains `enforcement/bundle.json`, which is validated through the consumer contract. A source `release-impact.json` classifies identity, palette, typography, platform assets, Web/React, egui, documentation, and recovery impact for the current compiler release. Documentation generation renders migration guidance from those two records.

**Rationale**: The bundle is per-kit evidence; impact classification is per-compiler-release policy. Separating them avoids repeating authored prose across brands while still producing kit-specific guidance.

**Alternatives considered**:

- Put prose directly in every generated document: rejected because drift cannot be detected reliably.
- Infer impact from file diffs: rejected because a diff cannot reliably distinguish compatibility work from optional capability adoption.

## Decision 6: Publish impact facts, not downstream outcomes

**Decision**: Records classify supplied changes as `required`, `optional`, or `unaffected`. They contain no consumer names, adoption state, productivity, elapsed time, correction rounds, escaped defects, utility scoring, or handover evidence.

**Rationale**: BrandBuilder owns the compatibility facts of what it publishes. Whether a downstream product adopts or benefits from a kit is outside this repository's authority and was explicitly rejected by the owner.

**Alternatives considered**:

- Add adoption telemetry or evidence fields: rejected as scope and governance overreach.
- Omit migration guidance entirely: rejected because consumers still need accurate, bounded release-impact facts.
