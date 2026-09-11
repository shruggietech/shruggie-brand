# Data Model: Identity-Locked I Heart PR Tours Brand Guide

## IntakeFile

| Field | Type | Rules |
| --- | --- | --- |
| `private_id` | string | Stable packet-local identifier with no workstation path |
| `original_name` | string | Exact supplied filename; retained only in private gate evidence when sensitive |
| `media_type` | enum | `pdf`, `png`, `svg`, `font`, `jpeg`, `webp`, or `other-reference` |
| `byte_length` | integer | Exact nonnegative byte count |
| `sha256` | digest | Lowercase 64-character SHA-256 |
| `dimensions` | object or null | Pixel dimensions, SVG view box, or PDF page size/count |
| `metadata` | object | Format-specific creator, profile, font, and embedded-object facts |
| `candidate_role` | enum | `brand-guide`, `mark`, `reduced-mark`, `lockup`, `wordmark`, `favicon`, `font`, `imagery`, `reference-art` |
| `disposition` | enum | `candidate`, `reference-only`, `excluded`, `approved`, `rejected`, or `missing-required` |

Private origin paths never enter committed source, public issues, or pull-request prose.

## SourceAuthorityDecision

| Field | Type | Rules |
| --- | --- | --- |
| `role` | string | One exact output authority role |
| `primary_private_id` | string | References one approved intake file |
| `lower_authority_ids` | array | Accounts for every overlapping candidate |
| `reason` | string | Explains why the primary source governs |
| `source_format` | enum | Production marks require passive SVG or portable PNG |
| `usage_status` | enum | `approved` or `reference-only` |
| `owner_disposition` | enum | `pending`, `approved`, `rejected`, or `superseded` |

Each production role has exactly one primary authority. No file becomes primary through format preference alone.

## FontEvidenceRecord

| Field | Type | Rules |
| --- | --- | --- |
| `role` | enum | `display`, `body`, `mono`, or `logo-reference-only` |
| `claimed_family` | string | Exact guide wording |
| `internal_family` | string | Measured font name when a binary exists |
| `subfamily` | string | Measured style and weight |
| `version` | string | Measured binary version |
| `format` | string | Exact font container |
| `sha256` | digest | Required before ingestion |
| `source` | string | Official provenance URL or supplied-source identifier |
| `license` | string | Exact license and reserved-name terms |
| `redistributable` | boolean | Must be true before shared inclusion |
| `offline_delivery` | enum | `approved`, `reference-only`, or `blocked` |

Gate 1 resolved the Source Sans 3/Pro ambiguity in favor of the supplied Source Sans 3 Regular and Semibold files for body and interface roles.

## TransformationContract

| Field | Type | Rules |
| --- | --- | --- |
| `source_private_id` | string | Exact approved source |
| `source_sha256` | digest | Must match the intake source |
| `output_role` | string | One derivative family |
| `operations` | array | Closed list approved per source |
| `renderer` | object | Identity, version, and settings digest |
| `dimensions` | object | Exact dimensions or proportional rule |
| `framing` | object | View box, placement, crop prohibition, and clear-space rule |
| `comparison_manifest` | digest | Binds review evidence |
| `status` | enum | `proposed`, `approved`, `invalidated`, or `blocked` |

Any unlisted operation is denied. A source or recipe change invalidates the contract.

## Gate1Approval

| Field | Type | Rules |
| --- | --- | --- |
| `candidate_id` | string | Unique revision identifier |
| `inventory_sha256` | digest | Binds the complete private intake inventory |
| `authority_sha256` | digest | Binds all role decisions |
| `font_sha256` | digest | Binds exact font evidence |
| `transformation_sha256` | digest | Binds every proposed operation |
| `classification_sha256` | digest | Binds affiliation, privacy, credit, and publication |
| `evidence_sha256` | digest | Binds displayed Gate 1 packet |
| `approved_by` | string | Human operator only |
| `approved_on` | date | Explicit approval date |
| `owner_words` | string | Exact approval wording |
| `status` | enum | `pending`, `approved`, `rejected`, or `invalidated` |

Gate 1 cannot approve while any required logo role is `missing-required` or any font role is ambiguous.

## CanonicalIdentityRecord

The S027 record is created only from an approved Gate1Approval. It binds source class `authoritative`, exact source inventory, identity snapshot, source authority, renderer contract, palette qualification, 32-coordinate proof matrix, four comparison artifacts per coordinate, approval revision, and normalized canonical-source digest.

## DerivedAssetRecord

| Field | Type | Rules |
| --- | --- | --- |
| `path` | string | Generated path under ignored kit output |
| `role` | string | Declared current-kit role |
| `source_id` | string | Approved authoritative input |
| `source_sha256` | digest | Exact approved source hash |
| `transformation_sha256` | digest | Approved recipe binding |
| `renderer_sha256` | digest | Exact renderer and settings binding |
| `output_sha256` | digest | Generated file hash |
| `proofs` | array | Representative visual evidence |

Every identity derivative has exactly one complete lineage record.

## Gate2Approval

| Field | Type | Rules |
| --- | --- | --- |
| `kit_manifest_sha256` | digest | Complete generated kit |
| `guide_sha256` | digest | Rendered guide |
| `asset_catalog_sha256` | digest | Generated asset and lineage catalog |
| `verification_sha256` | digest | Complete validation record |
| `publication_scope` | object | Exact registry, hosted guide, showcase, release, and deployment decisions |
| `approved_by` | string | Human operator only |
| `approved_on` | date | Explicit approval date |
| `owner_words` | string | Exact approval wording |
| `status` | enum | `pending`, `approved`, `rejected`, or `invalidated` |

Gate 2 cannot change Gate 1 source or transformation facts. An affected change invalidates both the relevant canonical record and Gate 2.
