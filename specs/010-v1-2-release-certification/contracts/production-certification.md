# Contract: v1.2.0 Production Certification

Production certification begins only after owner merge and successful Pages deployment.

## Required evidence

- Successful Pages workflow URL and deployed merged-main revision.
- Complete public route inventory compared with the generated route graph and sitemap.
- HTTPS success, expected content type, and non-empty valid payload for the skill download, all five brand download pages, representative registry JSON, and representative native icon files.
- Strict canonical, page title, description, Open Graph, Twitter, structured data, breadcrumb, sitemap, and robots parity across the route inventory.
- Browser checks at 360 and 1280 CSS pixels for representative portfolio and documentation routes in light and dark themes.
- Zero WCAG 2.1 AA violations and no material visual regression in the representative matrix.

## Failure policy

A delayed workflow remains pending. A failed workflow, stale deployed revision, missing route, invalid resource, discovery mismatch, accessibility violation, or material visual regression keeps #119 open and requires a reviewed correction when source changes are needed.

