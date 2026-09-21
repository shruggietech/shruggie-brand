# Data Model: Immutable Kit Publication

## FormalRelease

| Field | Type | Rule |
|---|---|---|
| `version` | semantic version | Equals BrandBuilder metadata, changelog boundary, and tag without `v` |
| `tag` | string | Exactly `v<version>` |
| `source_revision` | full Git SHA | Equals the tagged revision and all bundle records |
| `skill_archive` | filename | Versioned release asset built from the tagged revision |
| `kit_packages` | list of KitPackageIdentity | Exactly the production brand set |
| `notes_boundary` | version | Equals `version` and contains all changes since the prior tag |

Validation fails when any field disagrees with source metadata or generated assets.

## KitPackageIdentity

| Field | Type | Rule |
|---|---|---|
| `package_id` | string | `<brand-slug>-brand-<brand-version>-bb<brandbuilder-version>` |
| `filename` | string | `<package_id>.zip` |
| `brand_slug` | slug | Equals source brand slug |
| `brand_version` | semantic version | Retains identity meaning and equals source `brand.json` |
| `brandbuilder_version` | semantic version | Equals the FormalRelease version |

The identity changes if either brand identity or BrandBuilder changes. It does not require a brand-version change when only generated implementation contracts change.

## BundleRecord

| Field | Type | Rule |
|---|---|---|
| `schema_version` | integer | Versioned contract discriminator |
| `package` | KitPackageIdentity | Canonical package identity and filename |
| `versions` | object | Brand, BrandBuilder, canon, interface canon, recipes, Web/React adapter, and egui adapter versions |
| `source_revision` | full Git SHA | Exact build revision |
| `release` | object | Exact formal version and tag |
| `checksum_authority` | object | Algorithm, checksum manifest path, and verification command |

The record is generated into `enforcement/bundle.json`. The manifest, consumer contract, hosted registry, release archive, and recovery fields reference the same package identity.

## ReleaseImpactRecord

| Field | Type | Rule |
|---|---|---|
| `schema_version` | integer | Versioned source contract |
| `brandbuilder_version` | semantic version | Equals current compiler metadata |
| `identity_redesign` | boolean | Owner-controlled identity decision; false for S043 |
| `surfaces` | map | Exactly identity, palette, typography, platform assets, Web/React, egui, documentation, and recovery |
| `surfaces.*.classification` | enum | `required`, `optional`, or `unaffected` |
| `surfaces.*.summary` | string | Bounded statement of supplied change and consumer action |

The record contains publisher-owned impact facts only. Downstream products and outcome metrics are prohibited fields.

## MigrationSummary

Generated Markdown derived from one BundleRecord and the current ReleaseImpactRecord. It states whether identity changed, lists only affected surfaces, and distinguishes required compatibility work from optional capability adoption and unaffected surfaces.

## ProductionPublication

| Field | Type | Rule |
|---|---|---|
| `status` | enum | `candidate` for untagged output or `release` for an exact matching version tag |
| `release` | FormalRelease | One exact tagged release |
| `site_revision` | full Git SHA | Equals `release.source_revision` |
| `skill_destination` | URL | Exact tag or exact release asset, never `latest` |
| `kit_destinations` | URL map | Canonical filenames under the release or generated site path |

For `candidate` status, the target version and expected tag remain version facts but do not claim that the release exists. Production validation accepts only `release` status whose tag and revision match the workflow context.

State transition: `source` -> `verified candidate` -> `tag preflight` -> `release published` -> `Pages deployed`. `main` and pull requests stop at `verified candidate`.

## CandidateArtifact

Ephemeral verified output associated with a branch or commit. It may contain the same structural records as a future release but cannot claim production status, an immutable release tag, or a production Pages destination.

## VersionPolicyInvariant

Any governed change that can alter generated kit bytes, bundle fields, or compatibility semantics requires a BrandBuilder version change. Release verification rejects reuse of a released BrandBuilder version for a different governed contract history. This invariant makes the human-readable package ID sufficient to distinguish governed package generations; checksums continue to distinguish and authenticate exact bytes.
