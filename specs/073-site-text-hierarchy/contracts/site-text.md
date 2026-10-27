# S073 Site Text Contract

## Portfolio introduction (#335)

- `#portfolio` remains the section target and `#portfolio-heading` remains its heading.
- The visible and DOM order is Selected work, Our Portfolio, approved description, then cards.
- The description is a descendant of the same intro group as the heading and sits below it at desktop, mobile, and enlarged text sizes.
- The exact sentence and hero link remain unchanged. Other `.section-heading` uses keep their previous layout.

## Card titles (#310)

- Every current name and marker is fully rendered inside its content box. DanceWithMe865 has at least 24 CSS pixels between the title/marker right edge and the content box right edge at the narrowest desktop grid width.
- Normal titles retain their standard display size. Only a measured insufficient fit invokes bounded reduction.
- A synthetic longer title remains complete within the card through reduced size or wrapping. The vendor marker remains associated with its title and its `aria-describedby` target remains valid.
- Layout checks cover breakpoint widths, 390px, 320px, and 200% text enlargement. Cards do not overlap or create page-level horizontal overflow.

## References (#311)

- Each of 68 `REF-*` headings has exactly one ordered Source, Class, Use, Limit sequence rendered as separate compact list items in one visual unit.
- Existing `#ref-*` anchors, inbound links, external URLs, and field wording remain valid. Long links and prose wrap inside the viewport.
- The page keeps meaningful heading order, keyboard focus, selection/copy, 200% enlargement, WCAG 2.1 AA contrast, and 320 CSS-pixel reflow.

## Verification and boundaries

Tests must inspect rendered behavior, not only source strings. Source assertions retain exact approved wording. No changes to canonical brand messaging, logo geometry, generated kits, or unrelated documentation pages are in scope.
