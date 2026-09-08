# Contract: Shared Site Interaction Affordances

## Footer Destination Policy

| Label | Navigation | Target | Relationship |
| --- | --- | --- | --- |
| Brands | Same tab | Omitted | Omitted |
| Documentation | Same tab | Omitted | Omitted |
| Download the skill | Separate context | `_blank` | `noopener noreferrer` |
| Company | Same tab | Omitted | Omitted |
| Source | Separate context | `_blank` | `noopener noreferrer` |
| License | Separate context | `_blank` | `noopener noreferrer` |

The contract is label-specific and must not be inferred from absolute URL or hostname. Labels, destinations, ordering, accessible focus, and responsive footer geometry remain unchanged.

## Documentation Pagination Geometry

- The cue row containing the chevron and primary label is an inline alignment container.
- The chevron has stable width and height and cannot shrink.
- The chevron center and complete cue-row center differ by no more than one rendered pixel.
- Previous and next directions, wrapped and unwrapped labels, one-card and two-card layouts, and 360 and 1280 CSS pixel viewports satisfy the same contract.
- The secondary description retains its existing wrapping and hierarchy.

## Theme-Control Interaction

- Every enabled button represented by the shared theme-switch surface reports `cursor: pointer` under pointer input.
- Every disabled theme button reports the established disabled cursor and retains native disabled semantics.
- The current live light/dark toggle remains an enabled semantic button with an accessible name, visible focus, at least a 44 by 44 CSS pixel target, and keyboard activation.
- Theme state remains visible without relying on cursor shape.

## Verification Contract

- Source verification rejects any footer policy record that differs from the six-row table.
- Source verification rejects missing enabled or disabled cursor selectors and missing pagination alignment or non-shrinking icon rules.
- Rendered verification checks metadata and focus for all footer destinations on representative footer routes.
- Rendered verification checks pagination geometry on index, interior, and endpoint documentation pages at both required widths and themes.
- Rendered verification checks theme-control semantics, target size, focus, pointer cursor, and keyboard-driven theme transition.
- The existing full static-export, route, payload, responsive, and WCAG 2.1 AA gates remain mandatory.
