# Data Model: Semantic Link and Documentation Navigation

## Anchor Family

| Field | Meaning |
| --- | --- |
| id | Stable semantic name such as editorial, text-action, desktop-nav, footer, card, button, identity, or contextual-nav |
| context | Component or content region that owns the link |
| resting affordance | Color, underline, border, surface, or cue visible without interaction |
| interaction states | Hover, focus-visible, active, current, and visited behavior allowed for the family |
| motion | Transition behavior and reduced-motion fallback |
| exclusions | Decorations that must never leak into the family |

## Pagination Destination

| Field | Meaning |
| --- | --- |
| direction | Previous or next |
| title | Destination document name |
| description | Secondary destination summary |
| href | Valid neighboring document URL |
| availability | Present only when the neighbor exists |

## Relationships and Validation

- Every rendered anchor maps to exactly one family.
- Destination attributes such as external or download do not select the visual family.
- Pagination is a contextual-navigation family with one anchor per available neighbor.
- Dedicated generated guideline documents are outside the site taxonomy.
