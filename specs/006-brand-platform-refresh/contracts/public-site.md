# Public Site Contract

## Stable routes

- `/` presents the approved ShruggieTech brand-building message and generated portfolio.
- `/docs/` and `/docs/<reference>/` present the searchable documentation tree.
- `/<brand>/` and `/<brand>/downloads/` present one route pair per generated production brand record.
- `/<brand>/guidelines/` and `/<brand>/brand/r/*.json` remain copied generated-kit surfaces.
- `/static.json`, `/robots.txt`, `/sitemap.xml`, `/site.webmanifest`, favicon paths, and the social-preview path are static discovery assets.

## Metadata

Every indexable HTML route emits one absolute canonical URL, route-specific title and description, Open Graph type, URL, title, description, site name, image URL, dimensions, type, and alt text, plus a Twitter summary-large-image card. Root metadata declares the favicon set, Apple touch icon, manifest, application name, and theme color.

## Accessibility and responsive behavior

- Every meaningful foreground and interaction state satisfies WCAG 2.1 AA at rendered size.
- Every interactive target is at least 44 by 44 CSS pixels or has equivalent spacing that prevents adjacent-target interference.
- Skip navigation reaches the page's main content.
- Focus indicators remain visible against every surface.
- Reduced-motion preference removes non-essential animation and smooth scrolling.
- Portfolio and documentation layouts create no horizontal page overflow at 360, 768, 1280, or 1920 CSS pixels and with ten portfolio cards.
- Documentation tables use semantic table markup and remain horizontally reachable within their own container on narrow screens.

## Review boundary

The official pull request closes no issue before merge. It links #100 through #103, permits the automatic Codex review plus at most one explicit `@Codex` request, and remains open after every required check and review is satisfied.
