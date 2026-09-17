# Data Model: Component Recipes and Web AppFrame

## ComponentRecipeCatalog

| Field | Type | Rules |
| --- | --- | --- |
| `id` | string | Stable `shruggie-component-recipes` identifier. |
| `kind` | constant | `component-recipe-catalog`. |
| `version` | semantic version | Independent component recipe version. |
| `interface_canon_compatibility` | array | Includes the resolved Interface Canon version. |
| `grammar` | object | Forbids screens, navigation, product layouts, raw values, and renderer properties. |
| `required_dimensions` | array | Exact recipe fields every component declares. |
| `components` | closed object | Exactly 15 recipes spanning the 14 issue families. |
| `coverage` | array | One row per recipe linking consumer need, states, adapters, and checks. |

Validation states: schema-valid, vocabulary-complete, role-resolved, invariant-valid, coverage-complete, brand-override-valid. Any failure stops generation.

## ComponentRecipe

| Field | Type | Rules |
| --- | --- | --- |
| `purpose` | string | Shared consumer need, never a product workflow. |
| `element` | string | Native semantic root or shell role. |
| `variants` | array | Closed presentation choices. |
| `densities` | array | Shared density vocabulary. |
| `states` | array | Relevant governed state subset. |
| `roles` | object | Named `$role.<interface-role>` assignments only. |
| `keyboard` | array | Explicit input-to-outcome rules. |
| `target` | object | Minimum target role and hit-area rules. |
| `icons` | object | Required, optional, prohibited, decorative, or labeled behavior. |
| `accessibility` | object | Role, naming, relationships, announcements, and focus ownership. |
| `motion` | object | Standard and reduced-motion role assignments. |
| `responsive` | object | Capability and window-class adaptations. |
| `overrides` | array | Exact expressive fields a brand may replace. |
| `owner` | enum | `server`, `client`, or `app-frame`. |
| `verification` | array | Stable check identifiers. |

## AppFrameOwnershipMap

| Field | Type | Rules |
| --- | --- | --- |
| `profile` | enum | `browser`, `tauri`, or `wails`. |
| `responsibilities` | object | Exactly `safe_area`, `dynamic_viewport`, `root_scrolling`, `fixed_chrome`, `ime_obstruction`, `titlebar_regions`, and `global_focus`. |
| responsibility value | enum | Exactly one of `app-frame` or `host`. |
| `handoff` | object | Host input for every host-owned responsibility. |
| `capabilities` | array | Observed inputs; excludes OS routing. |

Invalid states: missing owner, duplicate owner, unknown responsibility, host ownership without handoff, or OS-derived branching.

## WebAdapterManifest

| Field | Type | Rules |
| --- | --- | --- |
| `adapter_version` | semantic version | Initially `1.0.0`. |
| `component_recipe_version` | semantic version | Matches copied catalog. |
| `interface_canon_version` | semantic version | Matches resolved contract. |
| `entries` | object | Token, CSS, server, client, specimen, host, and support paths. |
| `dependencies` | object | Exact Radix package version and license record. |
| `peer_dependencies` | object | Supported React range. |
| `server_safe_exports` | array | Exports with no browser-global import evaluation. |
| `client_exports` | array | Behavior-heavy components behind the client boundary. |
| `components` | array | Exactly the catalog recipe keys. |

## RuntimeEnvironmentProps

| Field | Type | Rules |
| --- | --- | --- |
| `windowClass` | enum | `compact`, `medium`, `expanded`, or `unbounded`. |
| `pointerPrecision` | enum | `none`, `coarse`, `fine`, or `mixed`. |
| `hover`, `hardwareKeyboard`, `touch` | boolean | Observed capabilities. |
| `textScale` | positive number | Never counter-scaled. |
| `reducedMotion`, `forcedColors` | boolean | Accessibility capabilities. |
| `safeArea` | inset object | Non-negative logical measures. |
| `imeObstruction` | rectangle or null | Exposed without disabling root scroll. |
| `titlebarRegions` | array | Avoidance rectangles supplied by the host. |

## SupportRecord

| Field | Type | Rules |
| --- | --- | --- |
| `target` | string | Chrome browser, Windows 11 webview-style, or Android Chrome-style. |
| `engine` | object | Actual executed browser name and version. |
| `host` | object | Actual runner plus native or simulated classification. |
| `configuration` | object | Viewport, input, scaling, motion, colors, insets, titlebar, and IME. |
| `checks` | array | Executed keyboard, focus, reachability, ownership, and accessibility checks. |
| `limitations` | array | Explicit untested native-host behavior. |
| `result` | enum | `passed`, `failed`, or `not-run`. |

## ConsumerContractV2 additions

Add `component_recipe_version` and `web_react_adapter_version` to `versions` and `version_semantics`; add `component_recipes`, `web_adapter`, and `support_matrix` authority paths; include copied contracts and adapter metadata in provenance. Existing version and recovery semantics remain unchanged.
