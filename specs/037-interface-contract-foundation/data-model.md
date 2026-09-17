# Data Model: Interface Contract Foundation

## InterfaceCanon

| Field | Type | Rules |
| --- | --- | --- |
| `id` | string | Fixed stable identifier. |
| `version` | semantic version string | Independent Interface Canon version. |
| `brand_canon_compatibility` | array of semantic version strings | Includes the Brand Canon used by a resolved kit. |
| `units` | object | Declares the logical unit and renderer transform expectations. |
| `primitives` | nested object | Contains reusable renderer-neutral values only. |
| `role_catalog` | array of dotted role identifiers | Complete allowed semantic role vocabulary. |
| `required_roles` | array of dotted role identifiers | Every listed role must resolve. |
| `aliases` | object keyed by role | Values are bounded references into primitives, aliases, brand data, Brand Canon, or derived accessible values. |
| `runtime` | object | Required normalized capability keys, enums, numeric constraints, and mixed-profile examples. |
| `invariants` | object | Accessibility and behavioral values that brand overrides cannot weaken. |
| `permitted_overrides` | object | Exact semantic roles and allowed reference roots. |
| `state_pairs` | array | Foreground and background role pairs with minimum measured contrast. |

Validation states: source, structurally valid, graph-valid, brand-resolved, accessibility-valid. Any failure stops generation.

## RuntimeEnvironmentProfile

| Field | Type | Rules |
| --- | --- | --- |
| `viewport` | object | Positive usable width and height in logical units. |
| `safe_area` | object | Non-negative logical top, right, bottom, and left insets. |
| `window_class` | enum | `compact`, `medium`, `expanded`, or `unbounded`. |
| `pointer_precision` | enum | `none`, `coarse`, `fine`, or `mixed`. |
| `hover` | boolean | Observed hover availability. |
| `hardware_keyboard` | boolean | Observed keyboard availability. |
| `touch` | boolean | Observed touch availability. |
| `text_scale` | number | Positive scale factor. |
| `reduced_motion` | boolean | User accessibility preference. |
| `forced_colors` | boolean | Forced-colors or equivalent high-contrast mode. |
| `theme` | enum | `light`, `dark`, or `system`. |
| `ime_obstruction` | object or null | Bounded obstructed rectangle in logical units. |
| `titlebar_regions` | array | Bounded draggable or control regions in logical units. |

No operating-system field is permitted. Profiles may combine capabilities freely when individual values remain valid.

## OperatingModeDecision

| Field | Type | Rules |
| --- | --- | --- |
| `mode` | enum or null | `author`, `implementation`, `audit`, or null when clarification is required. |
| `evidence` | array of strings | Names the normalized request and repository facts supporting the result. |
| `requires_clarification` | boolean | True only for genuinely conflicting mutation intent. |
| `clarification` | string or null | One narrow question, never a broad permission request. |
| `authority_preserved` | boolean | Always true for a valid decision. Mode selection grants no new permission. |

Precedence: governed-source mutation selects Author when already authorized; consumer mutation selects Implementation when already authorized; read-only assessment selects Audit; conflicting or absent mutation authority requests clarification.

## ConsumerContract

| Field | Type | Rules |
| --- | --- | --- |
| `schema_version` | integer | Starts at 1. |
| `brand` | object | Exact slug, title, affiliation, and `brand_version`. |
| `versions` | object | Exact `canon_version`, `interface_canon_version`, `compiler_version`, and `brand_version`. |
| `environment` | object | Declares renderer, host, supported targets, viewport profiles, and adapter versions without OS inference. |
| `authority` | object | Names brand source, Interface Canon, instructions, permitted exceptions, and precedence. |
| `verification` | object | Declares runnable entry point and expected zero-problem result. |
| `recovery` | object | Exact distribution filename, contained path, SHA-256, install guidance, and ordered offline-first sources. |
| `provenance` | array | Relative governed input or output path, byte count, and SHA-256. |
| `capability_gap` | object | Template path and authorization boundary. |

The consumer contract does not checksum itself. The final kit manifest checksums the complete consumer-contract file.

## GovernedInstructionBlock

| Field | Type | Rules |
| --- | --- | --- |
| `begin_marker` | literal string | Appears exactly once. |
| `content` | UTF-8 Markdown | Concise authority, exact version, deeper guidance, verification, recovery, and conflict precedence. |
| `end_marker` | literal string | Appears exactly once after the begin marker. |

Merge states: absent markers append one block; one ordered pair replaces only that block; duplicate, orphaned, or reversed markers fail without writing.

## CapabilityGapRecord

| Field | Type | Rules |
| --- | --- | --- |
| `consumer` | object | Brand slug and version. |
| `environment` | object | Renderer and host. |
| `requirement` | string | Reproduction or required behavior. |
| `shared_concept` | string | Existing or missing shared semantic concept. |
| `evidence` | array | Local paths, checks, or observations. |
| `classification` | enum | `reusable-capability` or `product-composition`. |
| `upstream_resolution` | object | Issue or change reference, initially null. |
| `adopted_version` | string or null | Exact consumer-adopted contract version after resolution. |
| `submission_authorized` | boolean | Defaults false and cannot be inferred from record creation. |

State transition: local draft, authorized submission, upstream resolved, consumer adopted. Only the local draft is generated by this slice.
