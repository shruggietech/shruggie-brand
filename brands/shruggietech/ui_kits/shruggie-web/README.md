<!-- verify:allow-rhetoric reason="Preserved source UI guide documents deliberate brand copy and comparisons." -->

# ShruggieTech Website — UI Kit

Interactive recreation of the ShruggieTech marketing site (`shruggietech/shruggie-web`, Next.js + Tailwind 4). Dark-mode-first, matching the live brand surfaces.

## Screens
- **Home** — dark hero (`We advance your vision.`) with dot-grid + green mesh, services preview (4 cards), products preview, closing CTA.
- **Services** — page hero, four service pillars (Strategy & Brand, Development, Revenue & Marketing Ops, AI & Data), Discuss/Create/Deliver process, CTA.
- **Products** — four product cards with status badges, "How We Build Software" spec-to-ship philosophy, CTA.
- **Contact** — live contact form (Input / Textarea / Select) with success state, plus expectations sidebar.
- Work / Research / About render lightweight page-hero stand-ins (full versions live on the real site).

## Interaction
Header nav switches screens; `Get in Touch` and CTAs route to Contact. The contact form submits to an inline success state. Scroll is contained to the kit viewport so the sticky header gains its blur on scroll.

## Composition
Screens compose the design-system components from `window.ShruggieTechDesignSystem_1f6967` (Button, Card, Badge, SectionHeading, ShruggieCTA, Input, Textarea, Select). Icons use [lucide](https://lucide.dev) via CDN — the same icon set the site ships. Layout, copy, colors, and type are lifted from the real repo, not reinvented.

## Files
`index.html` (shell + script order) · `Icon.jsx` · `Header.jsx` · `Footer.jsx` · `HomeScreen.jsx` · `ServicesScreen.jsx` · `ProductsScreen.jsx` · `ContactScreen.jsx` · `App.jsx` (router).
