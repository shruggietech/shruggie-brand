# Data Model: Cross-Host Conformance Fixtures

## Conformance Contract

| Field | Meaning | Validation |
| --- | --- | --- |
| `schema_version` | Shape version for the source contract | Exact supported integer |
| `contract_version` | Independent semantic version of conformance policy | Valid semantic version |
| `profiles` | Canonical capability profiles | Required identifiers exactly once |
| `host_tracks` | Reference and later evidence boundaries | Required host identifiers exactly once |
| `diagnostic_classes` | Allowed primary failure ownership | Exactly visual, accessibility, interaction, host-boundary |
| `traces` | Ordered host envelope regression events | Known-bad and corrected trace required |
| `baseline_policy` | Candidate and decision requirements | Human-only, complete metadata, fail-closed |

## Capability Profile

| Field | Meaning | Validation |
| --- | --- | --- |
| `id` | Stable profile identity | Safe kebab case and unique |
| `viewport` | Logical width, height, and orientation | Positive finite logical units |
| `input` | Keyboard, touch, pointer precision, and hover | Capability values, not OS inference |
| `motion` | Standard or reduced | Closed vocabulary |
| `contrast` | Normal, forced colors, high contrast, or unsupported | Status and behavior explicit |
| `text_scale` | Requested text multiplier | Positive finite value within declared test range |
| `safe_area` | Logical inset edges | Non-negative finite values |
| `ime_block_end` | Logical IME obstruction | Non-negative and smaller than usable block size |
| `window_class` | Compact, narrow, normal, or expanded | Closed capability vocabulary |

## Host Track

| Field | Meaning | Validation |
| --- | --- | --- |
| `id` | Browser, Tauri Android, Wails Windows, or egui native | Required and unique |
| `renderer` | Web/React or egui | Must match existing adapter identity |
| `host` | Reference host boundary | Stable declared value |
| `target` | Browser, Android WebView, Windows WebView2, or native | Stable declared value |
| `entry_point` | Generated fixture path or existing egui crate | Safe relative path under kit |
| `evidence_class` | What the fixture may satisfy | Cannot be broader than the fixture |
| `profiles` | Supported or explicitly unsupported profiles | Every required profile dispositioned |
| `required_tool` | Browser, Rust/Cargo, Go, or egui test command | Exact executed version recorded later |

## Host Envelope Event

| Field | Meaning | Validation |
| --- | --- | --- |
| `sequence` | Ordered transition number | Contiguous non-negative integer |
| `event` | Initial, orientation, resize, IME, input, or titlebar change | Closed vocabulary |
| `viewport` | Current logical geometry | Positive finite dimensions |
| `safe_area` | Host-reported edge insets | Non-negative and not larger than viewport |
| `ime_block_end` | Current bottom obstruction | Non-negative and bounded |
| `titlebar_regions` | Reserved window-control rectangles | Valid non-inverted geometry |
| `ownership` | AppFrame or host owner per boundary | Exactly one owner per responsibility |
| `required_controls` | Logical control rectangles that must remain reachable | Each intersects positive usable content |

## Fixture Result

| Field | Meaning | Validation |
| --- | --- | --- |
| `brand` | Production brand slug and version | Matches generated kit |
| `versions` | Canon, Interface Canon, recipes, adapters, compiler, conformance | Exact generated identities |
| `source_revision` | Source revision that emitted fixture | Matches consumer contract |
| `host_track` | Fixture that executed | Known host identifier |
| `evidence_class` | Evidence boundary satisfied | Exact match to host track |
| `tool` | Executed tool and exact version | Non-empty and parseable |
| `profiles` | Per-profile result records | All track profiles dispositioned |
| `status` | Supported, unsupported, pending-proof, blocked, failed | Closed vocabulary with reason rules |
| `diagnostics` | Classified failures or skips | Valid diagnostic objects |

## Diagnostic

| Field | Meaning | Validation |
| --- | --- | --- |
| `class` | Primary owning category | One of four declared classes |
| `code` | Stable machine-readable identifier | Safe dotted or kebab identifier |
| `brand` | Affected production brand | Matches fixture result |
| `profile` | Affected capability profile | Known profile |
| `host` | Affected host track | Known host |
| `subject` | Element, capability, trace event, or contract | Non-empty |
| `message` | Actionable explanation | Non-empty and free of ambiguous fallback category |

## Visual Candidate

| Field | Meaning | Validation |
| --- | --- | --- |
| `candidate_id` | Digest over image bytes and normalized metadata | Recomputed exactly |
| `image_sha256` | Screenshot checksum | Lowercase SHA-256 |
| `brand` / `brand_version` | Generated brand identity | Matches kit |
| `versions` | Contract identities | Complete and matching |
| `source_revision` | Source identity | Exact fixture source |
| `host` / `profile` | Evidence context | Known pair |
| `viewport` | Logical dimensions and orientation | Matches profile |
| `fonts` | Font family, source identity, and load state | Complete list |
| `rendering` | Browser or renderer version, scale, color scheme, contrast, motion | Complete normalized object |
| `review_state` | Pending human review | Cannot be accepted by candidate generation |

## Baseline Decision

| Field | Meaning | Validation |
| --- | --- | --- |
| `candidate_id` | Exact candidate under review | Must resolve and match metadata |
| `decision` | Accepted or rejected | Closed vocabulary |
| `reviewer` | Human identity | Non-empty and not an automation identity |
| `reason` | Decision rationale | Non-empty |
| `reviewed_at` | UTC decision timestamp | Valid timestamp |
| `source_revision` | Reviewed source | Matches candidate |
| `environment` | Host, profile, viewport, fonts, and rendering settings | Exact candidate equality |

## State Transitions

### Fixture evidence

`declared -> generated -> executed -> supported|unsupported|failed`

`declared -> generated -> pending-proof|blocked`

Browser evidence cannot transition another host track. Reference fixture evidence cannot transition actual-host or consumer-adoption records.

### Visual review

`generated -> pending-human-review -> accepted|rejected`

Only a human-authored matching decision can leave `pending-human-review`. Any content or environment change produces a new candidate identity and returns to pending review.
