# Data Model: Native egui Adapter and Versioned Contracts

## VersionPolicy

| Field | Type | Rules |
| --- | --- | --- |
| `schema_version` | integer | Version 1 of the closed policy document shape. |
| `id` | string | Stable `shruggie-version-policy` identifier. |
| `kind` | constant | `version-policy`. |
| `version` | semantic version | Version of the policy schema and meanings. |
| `domains` | closed object | Exactly Brand Canon, Interface Canon, component recipes, Web/React adapter, egui adapter, compiler, and brand. |
| `compatibility_rules` | array | Exact dependency edges and accepted versions. |
| `lifecycle_states` | array | Distinguishes compatible candidates from published artifacts and unadopted contracts from named consumer adoption. |
| `recovery` | object | Exact-version and checksum requirements; forbids latest-version substitution. |

## VersionDomain

| Field | Type | Rules |
| --- | --- | --- |
| `meaning` | string | Names the contract surface the version identifies. |
| `patch` | array | Backward-compatible corrections that do not add contract surface. |
| `minor` | array | Backward-compatible additions or expanded support. |
| `major` | array | Breaking removals, renamed meanings, incompatible defaults, or schema shape changes. |
| `compatibility_keys` | array | Other domains whose versions determine validity. |
| `publication` | string | Names the artifact boundary that publishes this domain. |

## EguiAdapterManifest

| Field | Type | Rules |
| --- | --- | --- |
| `adapter_version` | semantic version | Independent egui adapter version. |
| `interface_canon_version` | semantic version | Exact compatible Interface Canon. |
| `component_recipe_version` | semantic version | Exact compatible recipe catalog. |
| `brand_version` | semantic version | Exact source brand resolved into tokens. |
| `crate` | object | Package name, edition, MSRV, and exact dependency versions. |
| `entries` | object | Rust source, tests, policy, support, and guidance paths. |
| `logical_units` | object | Source unit, target unit, transform factor, and density multipliers. |
| `runtime_capabilities` | array | Closed observed input vocabulary. |
| `support` | array | One component support record per shared recipe. |

## NativeSupportRecord

| Field | Type | Rules |
| --- | --- | --- |
| `component` | string | One shared recipe identifier. |
| `status` | enum | `supported`, `adapted`, or `unsupported`. |
| `symbol` | string or null | Generated Rust helper when available. |
| `reason` | string | Explains native mapping or the explicit gap. |
| `states` | array | Recipe states claimed by the adapter. |
| `evidence` | array | Stable generated test or verifier identifiers. |

## RuntimeCapabilities

| Field | Type | Rules |
| --- | --- | --- |
| `viewport_points` | positive pair | Available logical viewport in egui points. |
| `pointer_precision` | enum | `none`, `coarse`, `fine`, or `mixed`. |
| `hover`, `hardware_keyboard`, `touch` | boolean | Observed input capabilities. |
| `text_scale` | positive number | User or host scale, never counter-scaled. |
| `reduced_motion`, `forced_colors` | boolean | Accessibility capabilities. |
| `safe_area`, `ime_obstruction`, `titlebar_regions` | geometry | Host-observed obstructions and ownership inputs. |
| `theme` | enum | `light`, `dark`, or `system`. |
| `density` | enum | `comfortable` or `compact`. |

## ConsumerContractV3 additions

Add `egui_adapter_version` to `versions` and `version_semantics`; add `egui_adapter`, `egui_support_matrix`, and `version_policy` authority paths; add an exact compatibility record; include native manifests, support, policy, and guidance in provenance; retain exact offline compiler recovery and all v2 fields.
