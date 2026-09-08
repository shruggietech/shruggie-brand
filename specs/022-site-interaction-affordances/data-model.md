# Data Model: Site Interaction Affordances

## Footer Destination Record

| Field | Meaning | Validation |
| --- | --- | --- |
| `label` | Existing user-visible footer text | Unique across the six records and byte-for-byte unchanged |
| `href` | Existing internal path or absolute destination | Byte-for-byte unchanged from the pre-slice footer |
| `newTab` | Explicit browsing-context policy | `true` only for Download the skill, Source, and License |
| `relationship` | Opener and referrer policy | Present exactly when `newTab` is true |
| `internal` | Whether framework-local navigation is appropriate | True only for Brands and Documentation |

### Invariants

- The collection contains exactly six records in the existing order.
- Exactly three records use a separate browsing context.
- Company is an ordinary anchor with same-tab behavior despite its absolute URL.
- Internal records use existing local navigation behavior.
- A separate-context record always carries both opener isolation and referrer suppression.

## Pagination Cue

| Field | Meaning | Validation |
| --- | --- | --- |
| Direction | Previous or next | Both directions covered across representative routes |
| Label group bounds | Bounds of the complete cue label container | Center is compared with the icon center |
| Icon bounds | Rendered chevron box | Stable width and height, no flex shrink |
| Center delta | Absolute difference between vertical centers | No more than one rendered pixel |
| Neighbor count | One or two pagination cards | Index, interior, and endpoint shapes covered |

## Theme Control State

| State | Cursor | Required cues |
| --- | --- | --- |
| Enabled, current light | Pointer | Semantic button, accessible name, current visual state, visible focus |
| Enabled, current dark | Pointer | Semantic button, accessible name, current visual state, visible focus |
| Disabled | Established disabled cursor | Native disabled state and existing disabled treatment |

### State Transitions

1. The enabled theme control begins in either light or dark state.
2. Pointer or keyboard activation changes to the opposite theme.
3. The control remains enabled and its accessible label and visible state remain understandable.
4. Disabled styling is reserved for a genuine disabled state and does not occur merely because a theme is current.
