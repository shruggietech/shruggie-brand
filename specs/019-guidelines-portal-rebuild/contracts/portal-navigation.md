# Portal Navigation Contract

## Routes

- Overview: `/{brand}/guidelines/`
- Topic: `/{brand}/guidelines/{topic}/`
- Portable guide: `/{brand}/downloads/files/{brand}-portable-guidelines.html`
- Asset delivery: `/{brand}/downloads/files/{validated-kit-path}`

Every hosted topic has canonical metadata, breadcrumbs, social metadata, sitemap coverage, and one page-tree entry. Unknown brands or topics return the static not-found result.

## Desktop

- Persistent sidebar lists the current brand and ordered topics.
- Current topic uses semantic current-page state.
- Long topics expose a compact heading outline with active-section feedback.
- Sticky regions account for their own height in fragment positioning.

## Mobile

- One labelled control opens and closes the same topic hierarchy.
- Expanded state, focus order, dismissal, and touch targets are exposed semantically.
- The desktop sidebar is not squeezed into the narrow layout.

## Footer

- `Back to top` targets the visible page heading.
- `All brands` targets `/` and remains neutral white in all states.
- Controls are separate anchors, each at least 44 pixels high, with visible focus and bottom spacing.

## No-script behavior

All topic links, section anchors, rendered instructions, asset-family sections, detail disclosures, and downloads are present in server-rendered markup. Search, filters, copy shortcuts, URL query synchronization, and active-section enhancement may be unavailable, but no content or delivery becomes unreachable.
