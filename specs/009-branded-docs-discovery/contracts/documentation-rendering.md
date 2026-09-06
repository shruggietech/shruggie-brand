# Documentation Rendering Contract

## Source ownership

- `skill/references/*.md` remains the only authoritative prose source.
- Generated MDX may remove its first-level heading, normalize public terminology outside literal code, convert indented samples into fences, and promote explicitly authored alert blockquotes into semantic notices.
- Supported alert markers are NOTE, WARNING, and CAUTION. Unsupported alert markers fail preparation.

## Code

- Inline code uses a compact inline treatment and never controls fenced samples.
- Fenced samples render through the installed documentation component contract as one panel with preserved whitespace, contained horizontal scrolling, a clear boundary, syntax distinctions when a language is declared, and an accessible copy action.
- The copy action is keyboard reachable, has an accessible name, and copies the complete source sample.
- Page width remains contained at 360 and 1280 CSS pixels.

## Notices

- NOTE maps to `info`, WARNING maps to `warn`, and CAUTION maps to `error`.
- Notice intent is explicit in the authoritative Markdown rather than inferred from vague keywords.
- Notice wording remains equal to the authoritative blockquote body.
- Ordinary blockquotes and alert-looking text inside code fences remain unchanged.

## Navigation

- The documentation root is represented once in the page tree.
- Shared documentation navigation does not add a second identically named root link.
- Portfolio, skill download, and repository links remain accessible without duplicating the page-tree root.
