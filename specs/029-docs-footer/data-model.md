# Data Model: Documentation Footer Removal

S029 introduces no persistent data entity or schema. It clarifies the existing presentation-surface policy used by the static site.

## Presentation Surface Policy

| Field | Documentation | Marketing site | Brand guidelines |
|-------|---------------|----------------|------------------|
| Route scope | `/docs/` and descendants | Main `(site)` routes | `/<slug>/guidelines/` and downloads |
| Global `.site-footer` count | 0 | 1 on the homepage | 0 |
| Contextual end navigation | Fumadocs `.docs-pagination` | Global footer links | Dedicated `.guide-footer` |
| Authoritative owner | Documentation page composition | Marketing route-group layout | Guideline page composition |

## Validation Rules

- A documentation route is invalid if it renders any `.site-footer` element.
- A documentation route is invalid if it loses an applicable previous or next pagination destination.
- The homepage is invalid if it renders other than one `.site-footer` or changes the approved ordered destination policy.
- A guideline route is invalid if it gains `.site-footer` or loses its dedicated guide navigation.
