# Data Model: Approved Identity Construction Continuity

## Approval State

| State | Meaning | May transition to |
| --- | --- | --- |
| `exploratory` | A concept or reference with no production authority | `direction-selected`, `discarded` |
| `direction-selected` | Owner selected a concept for production refinement | `canonical-candidate`, `discarded` |
| `canonical-candidate` | All conversions are complete and production proofs exist | `canonical-approved`, `direction-selected` |
| `canonical-approved` | Owner approved the exact source-bound master and palette | `promoted`, `invalidated` |
| `promoted` | Approved bytes and configuration occupy permanent brand source | `derivative-approved`, `invalidated` |
| `derivative-approved` | Gate 2 approved derived families and publication surfaces | `publication-eligible`, `invalidated` |
| `publication-eligible` | All approvals and validation are current | `invalidated` |
| `historical-baseline` | Current authoritative facts are recorded without retrospective approval | `invalidated` |
| `invalidated` | A governed value changed or required evidence failed | `canonical-candidate` after explicit remediation |

Direction selection cannot skip to canonical approval. Canonical approval cannot skip byte-preserving promotion. Any governed drift transitions the affected state to `invalidated`; no automatic repair or implicit reapproval is allowed.

## Identity Continuity Reference

Stored in `brand.json`.

| Field | Type | Rules |
| --- | --- | --- |
| `record` | relative path | Fixed to a contained UTF-8 JSON source file; no absolute path, backslash, traversal, or symlink |
| `status` | enum | `approved-canonical` or `historical-baseline`; must equal the record status |

## Identity Continuity Record

Stored beside permanent brand source and validated before derivatives.

| Field | Type | Rules |
| --- | --- | --- |
| `schema_version` | integer | Exactly 1 |
| `brand` | identifier | Equals `brand.json.slug` |
| `status` | enum | `approved-canonical` or `historical-baseline` |
| `source_class` | enum | `glyphkit-constructed`, `legacy-constructed`, or `authoritative` |
| `recorded_on` | date | ISO calendar date |
| `source_revision` | string | Immutable repository revision or explicit baseline identifier |
| `source_files` | array | Unique contained paths with purpose, byte count, and SHA-256 |
| `identity_snapshot` | object | Exact governed values and their canonical digest |
| `topology` | object | Per-variant role counts, path/subpath/closure/fill signature, plus reference proof components and holes when approved |
| `framing` | object | Grid, view box, artwork bounds, clear space, variant padding, crop, and canonical digest |
| `palette` | object | Exact role values, sRGB/OKLCH evidence digest, qualification status, and canonical digest |
| `renderer` | object or null | Approved renderer identity, version, and deterministic settings digest |
| `proofs` | array | Unique variant, size, surface, path, SHA-256, and four-artifact comparison-evidence records; each exact PNG digest binds its rendered topology, color, and bounds |
| `approval` | object or null | Required only for approved canonical records |
| `historical_evidence` | object or null | Required only for historical baselines |
| `record_sha256` | SHA-256 | Digest of the record excluding this field |

The identity snapshot contains the complete `logo` configuration outside the already-bound path arrays as `derivative_settings`, so enclosure, contextual variant, lockup, reduction threshold, role, and future output-affecting settings cannot change silently.

### Record invariants

- Every configured source file resolves within its approved brand or provisional root and cannot traverse a symlink.
- Source-file paths and proof coordinates are unique.
- `glyphkit-constructed` requires a valid construction helper and a full proof matrix for approved canonical status.
- `legacy-constructed` is valid only as a historical baseline and must state why reconstruction is prohibited.
- `authoritative` binds full and reduced authoritative inputs and forbids a construction helper.
- Approved records require the complete 32-proof matrix across the mandatory full and reduced masters.
- Every approved proof binds unique side-by-side, overlay, silhouette-XOR, and color-difference PNG paths and SHA-256 values.
- Historical baselines do not claim an owner decision and may omit proofs whose history does not exist.

## Identity Snapshot

| Field | Contents |
| --- | --- |
| `source_mode` | Constructed or authoritative |
| `construction_provenance` | Declared source class, helper path, engine, and allowed primitive vocabulary |
| `masters` | Exact canonical hashes for full and reduced path arrays or authoritative source bindings |
| `roles` | Ordered roles and role-color mappings used by master geometry |
| `framing_sha256` | Digest of all view-box, bounds, crop, clear-space, and per-variant padding fields |
| `palette_sha256` | Digest of accent, semantic, surface, chart, legacy, and logo role colors |
| `typography_sha256` | Digest of wordmark text and typography fields that affect lockups |
| `derivative_config_sha256` | Existing derivative configuration digest for Gate 2 continuity |
| `sha256` | Canonical digest of the complete snapshot excluding itself |

## Canonical Approval

| Field | Type | Rules |
| --- | --- | --- |
| `bundle_id` | identifier | Stable candidate revision |
| `approved_by` | non-empty string | Human identity owner |
| `approved_on` | date | ISO calendar date |
| `owner_wording` | non-empty string | Exact approval statement |
| `scope` | unique array | Full master, reduced master if present, palette, framing, topology, renderer, and proof matrix |
| `proposal_sha256` | SHA-256 | Exact approval-packet manifest |
| `source_snapshot_sha256` | SHA-256 | Equals current identity snapshot digest |

`approval_ledger.gate_1.canonical_source_sha256` is the canonical digest of the record excluding `record_sha256` and the `brand.json` source-file entry that stores the binding. This removes the fixed-point cycle while preserving exact `brand.json` byte validation through `record_sha256` and `source_files`.

## Historical Evidence

| Field | Type | Rules |
| --- | --- | --- |
| `basis` | enum | `current-authoritative-source` |
| `baseline_revision` | revision | Actual merged revision from which the snapshot was taken |
| `approval_completeness` | enum | `complete`, `partial`, or `unknown` |
| `limitation` | string | Explicitly states that the record is not retrospective approval |
| `migration_issue` | integer | GitHub issue #185 |

## Continuity Comparison

| Field | Type | Rules |
| --- | --- | --- |
| `variant` | enum | `full` or `reduced` |
| `size_px` | enum | 256, 64, 32, or 16 |
| `surface` | enum | `dark`, `light`, `black`, or `white` |
| `same_renderer` | boolean | Selects exact or bounded comparison policy |
| `approved_sha256` | SHA-256 | Exact approval proof |
| `production_sha256` | SHA-256 | Exact current proof |
| `components` / `holes` | integer pair | Must be unchanged |
| `silhouette_iou` | ratio | Evidence only |
| `changed_outside_edge_fraction` | ratio | At most 0.005 across documented cross-renderer output |
| `bbox_delta_max_px` | integer | At most 1 for cross-renderer output |
| `centroid_delta_px` | number | At most 1.0 for cross-renderer output |
| `interior_delta_e_2000` | number | At most 1.0 |
| `evidence_paths` | object | Side-by-side, overlay, XOR, and color-difference images |
| `status` | enum | `pass` or `fail`, derived from policy |

## Promotion Transaction

| Field | Type | Rules |
| --- | --- | --- |
| `approval_bundle` | contained file | Complete approved-canonical record under ignored review root |
| `source_root` | contained directory | Contains exactly declared source files |
| `destination_root` | contained brand path | No arbitrary root or external destination |
| `staging_root` | temporary sibling directory | Must be new and removed on success or failure |
| `copied_files` | array | Each item records source hash, staged hash, and installed hash |
| `result` | enum | `promoted` or `rolled-back` |

Promotion never executes source files and never promotes generated proofs, external destinations, or undeclared files.
