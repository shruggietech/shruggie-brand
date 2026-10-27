# S073 Research

## Baseline and issue map

Fetched `origin/main` is `92525759541a51b7a5b07328c6bc711807945c2c`. The S073 worktree starts at that commit; the separate uncommitted S072 checkout is not used. [#310](https://github.com/shruggietech/shruggie-brand/issues/310) covers long card titles and the DanceWithMe865 marker, [#335](https://github.com/shruggietech/shruggie-brand/issues/335) covers portfolio heading grouping, and [#311](https://github.com/shruggietech/shruggie-brand/issues/311) covers the References page. The issue text is the owner-approved scope; source inspection below explains the current behavior.

## Findings

- `site/app/(site)/page.tsx` puts the portfolio description beside the eyebrow/heading wrapper. `site/app/globals.css` applies `display: flex` and `justify-content: space-between` to every `.section-heading`. The Conformance page also uses that shared class, so the homepage change must be scoped.
- `site/components/brand-portfolio.tsx` renders the vendor marker as a `sup` after the exact name. `site/app/globals.css` gives every desktop card heading 1.5rem, while the grid can narrow cards to 210px and card padding is 1.35rem per side. `overflow: hidden` clips content that exceeds the card.
- `skill/references/references.md` contains 68 `REF-*` headings. Each entry has Source, Class, Use, and Limit in one physical Markdown paragraph. `scripts/prepare_site.py` validates and copies this source into the MDX site. `scripts/check_documentation_references.py` requires the four labels and stable links but does not require one-line paragraphs.
- `site/scripts/verify-site.mjs` checks the portfolio's wording, marker association, and stable reference anchors. It does not measure title clearance or field separation. Its current `#portfolio .section-heading > p` selector must change with the markup.

## Decisions and alternatives

| Decision | Chosen | Rejected or deferred |
| --- | --- | --- |
| Portfolio description | Move the paragraph into the existing eyebrow/heading wrapper; style only the portfolio section. | CSS-only visual reordering would leave the DOM relationship split and could alter unrelated section headings. |
| Long card titles | Measure rendered text against available width; at standard default font size, reduce when clearance falls below 24px, down to a readable lower bound, then wrap if necessary. At enlarged browser default font sizes, keep the rem-based title scale and wrap. | The first 8px threshold left DanceWithMe865 at 24px with 19px clearance; global reduction wastes hierarchy on short names, and character-count heuristics ignore real font metrics and zoom. Fixed pixel reduction also cancels user font enlargement. |
| Reference fields | Four normal Markdown list items per reference, followed by route-scoped compact CSS. | HTML-only definition lists would reduce portability of the shipped Markdown; tables risk horizontal overflow. |
| Verification | Add rendered geometry/structure checks and preserve existing exact-copy/link checks; use temporary synthetic long-title input. | Source substring checks alone cannot prove clipping, reflow, or layout. |

The 24px reserve is the S073 measurable interpretation of the owner's direction to reduce title size before it reaches the usable card edge. It is measured against the card content box rather than the outer border. The first full browser run demonstrated that an 8px reserve was too small to reduce DanceWithMe865 at the narrowest grid width. No current evidence establishes an existing WCAG failure solely from screenshots. [WCAG 2.1 SC 1.3.1](https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html), [SC 1.4.4](https://www.w3.org/WAI/WCAG21/Understanding/resize-text.html), and [SC 1.4.10](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html) guide verification of relationships, enlargement, and narrow-view behavior.

## Validation implications

The reference reformat changes shipped source documentation, so full source, kit, site, and Markdown validation is required. Rendered checks must cover dark and light site themes where applicable, keyboard navigation, desktop grid widths, 390px and 320px viewports, and enlarged text. Retain all original reference text, links, headings, and citation targets.
