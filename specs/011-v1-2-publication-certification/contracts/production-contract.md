# Contract: v1.2.0 Production Deployment

## Provenance

- The successful Pages workflow must identify merged main revision `39b65b5daf9ea74c317132d26347566a9e4959d5`.
- Production verification must target exactly `https://brand.shruggie.tech` over HTTPS.

## Automated evidence

- Complete public route inventory compared with the generated route graph and sitemap.
- Strict canonical, page title, description, Open Graph, Twitter, structured data, sitemap, and robots parity.
- Expected content type and valid non-empty payload for skill and brand downloads, representative registries, favicon and application icons, manifests, and social previews.
- Browser checks at 360 and 1280 CSS pixels with no horizontal overflow.
- Light and dark theme checks for representative portfolio and documentation routes.
- Zero WCAG 2.1 AA violations.

## Manual evidence

Inspect the representative screenshots produced by the automated verifier for clipped content, overlapping navigation, illegible branding, broken hierarchy, or theme failure. Screenshots remain ignored and are not committed.

## Failure policy

A delayed workflow remains pending. A failed or stale workflow, unexpected origin, missing route, invalid resource, discovery mismatch, accessibility violation, overflow, or material visual regression keeps #119 open and requires a reviewed correction when source changes are needed.
