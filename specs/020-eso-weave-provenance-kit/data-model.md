# Data Model: ESO Weave Provenance and Current-Spec Kit

## Upstream Snapshot

| Field | Type | Rule |
| --- | --- | --- |
| `repository` | URL | Exact public ESO Weave repository |
| `default_branch` | string | Resolved from the synchronized remote |
| `commit` | 40-character SHA | Current branch head at acquisition or gate refresh |
| `retrieved_at` | timestamp | UTC evidence collection time |
| `intake_commit` | 40-character SHA | Issue #153 intake baseline |
| `status` | enum | `current`, `advanced-no-authoritative-drift`, or `authoritative-drift` |

The snapshot advances through `fetched -> inventoried -> gate-checked`. Any authoritative input drift moves it to `authoritative-drift` and invalidates dependent approvals.

## Source Evidence Record

| Field | Type | Rule |
| --- | --- | --- |
| `id` | stable string | Unique inside ESO Weave evidence |
| `contained_path` | relative path | Path copied into `brands/eso-weave/` or historical source path for metadata-only records |
| `upstream_path` | relative path | Path at the synchronized commit |
| `intake_path` | relative path or null | Original issue path when it moved |
| `role` | enum | `mark`, `reduced-mark-candidate`, `glyph`, `fixed-font`, `font-license`, `reproduction`, `historical-spec`, `brand-standard`, `product-voice`, `legal-boundary`, or `reference-art` |
| `format` | string | Normalized media or document format |
| `bytes` | integer | Exact source size |
| `sha256` | lowercase hex | Required for every acquired file |
| `color_profile` | enum | `srgb`, `embedded-other`, `none`, `unknown`, or `not-applicable` |
| `license_or_basis` | string | License, ownership, issue-supplied usage basis, or reference-only basis |
| `usage_status` | enum | `authoritative`, `approved-input`, `reference-only`, `historical-evidence`, or `excluded` |
| `provenance_class` | enum | `public-repository-evidence` or `operator-supplied-assertion` |
| `approved_transformations` | string list | Closed transformation set, empty before Gate 1 where applicable |

Authoritative SVG records require exact byte preservation. Reference art may establish intended appearance but can never replace an SVG master.

## Affiliation Contract

| Field | Required value |
| --- | --- |
| `ownership` | `third-party` |
| `showcase` | `public` |
| `parent` | `null` |
| `inheritance` | `independent` |
| `endorsement` | `none` |
| `service_credit` | `brand-system-by-shruggietech` |

The derived service credit is exactly `Brand system by ShruggieTech`. This record cannot derive an owned-project endorsement.

## Legal Boundary

| Field | Description |
| --- | --- |
| `non_affiliation_entities` | ZeniMax Online Studios, ZeniMax Media Inc., Bethesda Softworks, and Microsoft |
| `trademarks` | The Elder Scrolls and The Elder Scrolls Online belong to ZeniMax Media Inc. |
| `risk_statement` | Automation may violate applicable terms; the user remains responsible |
| `required_surfaces` | Standalone guide, PDF, public guideline portal, downloads context, UI specimen context, and machine-readable public metadata where omission could imply official status |

## Derivative Proposal

| Field | Type | Rule |
| --- | --- | --- |
| `id` | stable string | One per derivative family |
| `deliverable_roles` | string list | Current-kit assets satisfied by the proposal |
| `source_input_ids` | string list | Must resolve to current evidence records |
| `source_hashes` | lowercase hash list | Approval binding |
| `construction` | text | Exact composition or conversion proposed |
| `allowed_changes` | string list | Closed set |
| `forbidden_changes` | string list | Includes source path edits and identity normalization |
| `proof_contexts` | object list | 256, 64, 32, and 16 pixels on light and dark surfaces |
| `measurements` | object | Bounds, alignment, spacing, silhouette, and color differences |
| `recommendation` | enum | `approve`, `approve-with-minimum`, or `reject` |

## Approval Ledger Entry

| Field | Type | Rule |
| --- | --- | --- |
| `gate` | enum | `derivatives` or `publication` |
| `status` | enum | `pending`, `approved`, `rejected`, or `stale` |
| `approved_by` | string or null | Owner identity or null while pending |
| `approved_on` | date or null | ISO date |
| `source_hashes` | map | Complete authoritative hash binding |
| `derivative_hashes` | map | Required for publication approval |
| `scope` | string list | Approved derivative ids or exact public surfaces |
| `evidence_path` | relative path | Committed evidence record for decision |

`pending -> approved` requires explicit owner input. Any bound hash drift transitions `approved -> stale`. `rejected` requires a new proposal rather than mutation of the rejected record.

## Typography Contract

Each fixed face records file path, family, weight, style, format, SHA-256, license path, provenance, local-delivery status, and approved use. The planned proportional mappings are Inter Regular 400, Medium 500, and SemiBold 600. Mono remains absent unless separately approved.

## ESO Weave Kit

The production source entity combines strategy, voice, independent semantic colors, affiliation, legal boundary, authoritative inputs, palette approvals, typography, logo construction, domain components, guide content, and approval ledger. It is buildable only after Gate 1 and publicly projectable only after Gate 2.

## Publication Surface Set

The second gate enumerates brand showcase card, landing page, multi-page guideline portal, downloads library, generated registry endpoints, structured metadata, social preview, and generated kit download surfaces. Approval of one surface never implies an unlisted surface.
