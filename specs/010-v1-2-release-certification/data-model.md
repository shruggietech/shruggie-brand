# Data Model: v1.2.0 Release and Production Certification

## ReleaseCandidate

| Field | Rule |
| --- | --- |
| version | Exactly `1.2.0` for S010 |
| source_revision | Committed reviewed pull-request head before merge; actual merged main after merge |
| skill_version | Must equal `version` |
| canon_version | Must equal `version` |
| release_date | One ISO date shared by root and bundled changelog sections |
| migration_required | `true`, implemented by rebuilding existing kits |
| assets | Exactly seven entries from the release asset contract |
| validation_state | `draft`, `locally-certified`, `hosted-certified`, `merged-main-certified`, `published-certified` |

State transitions are monotonic. `published-certified` requires an owner-merged main revision and successful fresh-download verification.

## ProductionBrandReference

| Field | Rule |
| --- | --- |
| slug | One of the five production slugs |
| brand_version | Preserved from the existing source |
| canon_version | Must equal `1.2.0` |
| archive_name | `<slug>-brand-<brand_version>.zip` |

## ReleaseAsset

| Field | Rule |
| --- | --- |
| filename | Exact expected name derived from release or brand version |
| kind | `skill`, `portable`, or `brand` |
| required_entries | Type-specific plus universal license files |
| safety_state | No duplicate, absolute, parent-traversal, drive-qualified, or backslash path |
| integrity_state | Required metadata, PDF signature, manifest coverage, byte counts, and SHA-256 agree |

## ReviewRound

| Field | Rule |
| --- | --- |
| ordinal | `1` or `2` only |
| trigger | Automatic publication for round 1; one explicit `@Codex review` for round 2 |
| signal_url | Immutable pull-request comment, review, reaction, or check link |
| findings | Zero or more linked review-finding issues |
| state | `pending`, `received`, `addressed`, or `complete` |

No transition creates ordinal 3. A correction push does not create a new round.

## PublicationEvidence

| Field | Rule |
| --- | --- |
| merged_revision | Current verified main after owner merge |
| tag | Annotated `v1.2.0` pointing to `merged_revision` |
| workflow_url | Successful Release workflow for the tag |
| release_url | Public, non-draft, non-prerelease release |
| downloaded_assets | Exact seven-file set from a fresh empty directory |
| verification_result | Zero release-contract failures |

## ProductionEvidence

| Field | Rule |
| --- | --- |
| pages_workflow_url | Successful deployment for `merged_revision` |
| route_inventory | Complete generated public route set |
| resource_samples | Skill, brand, registry, and native-icon responses with expected non-empty content |
| discovery_result | Canonical, metadata, social, structured-data, sitemap, and robots parity |
| accessibility_result | Zero WCAG 2.1 AA violations on representative routes and viewports |
| visual_result | No material regression in light or dark theme at desktop or mobile width |

## ClosureSet

Issues #117 through #119 are not strict implementation dependencies, but each has its own evidence gate. Parent #116 and milestone 22 may close only when all three children are closed.

