# Data Model: Compact egui Desktop Density

## Control Metrics

| Field | Source | Rule |
| --- | --- | --- |
| `target_minimum` | `interaction.target.minimum` | Governed 44-point conservative target; density invariant |
| `pointer_hit_slop` | `interaction.pointer.hit_slop` | Governed 8-point margin used on both sides of a fine-pointer visual control |
| `fine_control_height` | Derived | `(target_minimum - 2 * pointer_hit_slop) * density multiplier` |
| `button_padding_inline` | Derived | Bounded fraction of density-scaled control spacing |
| `button_padding_block` | Derived | Bounded fraction of density-scaled control spacing |
| `item_spacing_inline` | Derived | Bounded fraction of density-scaled control spacing |
| `item_spacing_block` | Derived | Compact repeated-row gap, at most 2 points under normal compact density |
| `minimum_control_height` | Derived at application | Maximum of profile target and scaled body text plus twice block padding |

## Runtime Input Profile

| Field | Values | Effect |
| --- | --- | --- |
| `pointer_precision` | `fine`, `coarse`, `mixed`, `none` | Fine is eligible for compact controls; every other value is conservative |
| `touch` | Boolean | Any true value forces the conservative target |
| `density` | `comfortable`, `compact` | Scales fine control height and spacing only; never reduces conservative targets |
| `text_scale` | Positive finite number | Grows text and the resulting minimum control height when necessary |

## State Selection

1. Validate every runtime capability and unit transform.
2. Resolve theme and density tokens.
3. Select conservative target unless pointer precision is exactly fine and touch is false.
4. Scale body text from the renderer's stable default style.
5. Set the final minimum height to the larger of the selected profile height and scaled body text plus padding.
6. Apply coherent item spacing and button padding.

## Invariants

- Conservative targets never fall below 44 points.
- Fine-pointer compact controls remain at or below 24 points at normal text scale.
- Text scaling may increase, but never decrease, control height.
- Invalid transforms and runtime inputs fail before style application.
- Theme, color, focus, naming, and identity values are independent of density selection.
