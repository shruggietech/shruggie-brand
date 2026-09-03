<!-- verify:allow-rhetoric reason="Preserved parent guide contains deliberate brand slogans and source examples." -->

# ShruggieTech Design System

A design system for **ShruggieTech** — a modern technical studio in Knoxville, Tennessee building digital systems, software, and AI-driven experiences. This system captures the brand's dark-first visual language, its signature bright green, its voice, and the reusable components + screens that make up the marketing site.

> **Brand vibe:** smart, practical, confidently scrappy. Clean modern design, high contrast, signature bright green with occasional orange emphasis. Approachable expertise — capable people solving real business problems without over-complicating the tech.

---

## Sources

Built by reading the real product code. Explore these to build more faithfully:

- **GitHub — website:** [`shruggietech/shruggie-web`](https://github.com/shruggietech/shruggie-web) (Next.js 15, Tailwind CSS 4, self-hosted fonts). Tokens lifted from `styles/globals.css`; components from `components/ui/*`; copy from `app/*/page.tsx`.
- **Brand asset index:** `uploads/ShruggieTech-CDN-Brand-Assets.json` — authoritative CDN lookup (`https://cdn.shruggie.tech`) for logos, favicons, fonts, avatars, entity icons, and vendored libs. **Look assets up here by URL; never construct CDN URLs from memory.**
- **Fonts & logos:** provided as uploads, copied into `assets/`.
- **Colors** are not in the CDN index — they were read from the website source (`styles/globals.css`, spec §2.1) and are documented below.
- More ShruggieTech repos worth exploring: [`shruggietech/shruggie-indexer`](https://github.com/shruggietech/shruggie-indexer), [`metadexer`](https://github.com/shruggietech/metadexer), [`shruggie-feedtools`](https://github.com/shruggietech/shruggie-feedtools), [`dev-handbook`](https://github.com/shruggietech/dev-handbook).

---

## Content Fundamentals

How ShruggieTech writes. Match this voice in any deliverable.

- **Voice:** direct, helpful, slightly witty. Confidently scrappy, never corporate. No forced hype, no generic tech jargon, no "synergy/leverage/best-in-class" filler.
- **Person:** speaks as **"we"** to the reader as **"you."** "You have a business to run. We handle the technology that makes it grow."
- **Casing:** Title Case for nav and buttons; sentence case for body. **Uppercase, wide-tracked eyebrow labels** ("OUR PROCESS", "THE TEAM") set in the display font above section titles.
- **Headlines:** short, declarative, confident. "We advance your vision." · "The code is open. Jump in." · "Let's scope your project." · "AI is not magic. It is infrastructure."
- **The shruggie flourish:** the emoticon `¯\_(ツ)_/¯` is the brand's personality signature, paired with **"We'll figure it out."** It appears on the primary CTA (fades in on hover) and as a quiet accent. Use it sparingly — one moment per view — always in brand green.
- **Punchy two-beat sentences:** state a myth, then correct it. "Visibility means nothing without conversion." "We earn revenue by building things that work, not by holding things hostage."
- **Emoji:** essentially none in product copy. The only recurring glyphs are the shruggie `¯\_(ツ)_/¯` and a small 🇺🇸 flag in the "Made in the USA" footer line. Do not sprinkle emoji.
- **Values language:** ownership ("Ownership, not rentership."), specification-driven, ship-and-iterate.

---

## Visual Foundations

- **Mode:** **dark-first.** Every marketing route forces dark mode (pure black `#000` base). Light mode (`#F8F8F6` warm off-white) exists as a reading-mode alternative for docs/blog. Both ship as token sets (`.dark` scope = dark).
- **Color:** high-contrast near-monochrome (black / white / gray) with **bright green `#2BCC73`** as the single signature accent — used for links, eyebrow labels, icons, focus rings, hover borders, and the shruggie face. **Deep green `#00AB21`** is the hover/active green. **Orange `#FF5300`** is rare emphasis; its CTA-safe darkened form `#C24000` powers primary buttons and required-field marks. Max 1–2 background colors per view.
- **Backgrounds:** subtly-tinted near-black section surfaces (`surface-dark-warm #0D0F12`, `-rich #0A0E18`, `-slate #111318`, `-deep #060608`) create quiet depth as you scroll — never obvious. The hero uses a low-opacity **green radial mesh** plus a masked **dot grid** (interactive on the live site). No photography-heavy backgrounds, no loud gradients (avoid the bluish-purple gradient trope), no textures.
- **Type:** **Space Grotesk** (500/700) for display + headings with tight negative tracking (−0.02 to −0.03em); **Geist** (400/500) for body with generous 1.6–1.7 line-height; **Geist Mono** (400) for eyebrow labels, product names, code, and metadata. Geist Pixel exists for rare decorative accents (not shipped here — available via the brand typography CDN).
- **Corner radii:** buttons & inputs `8px` (rounded-lg), cards `12px` (rounded-xl), badges fully rounded (pill). Small chips `6px`.
- **Cards:** thin 1px border + soft shadow. In **dark mode** they become *glassmorphism-lite* — 3% white fill + 20px backdrop blur, faint white border. On hover: border turns green, a **green-tinted shadow blooms**, and the card lifts 2px.
- **Shadows:** minimal and green-tinted on interaction (`0 4px 20px rgba(43,204,115,.08)`); static "value" cards carry a soft green glow. No heavy drop shadows.
- **Borders:** hairline. `#262626` on dark, `#E5E5E5` on light; translucent white (`rgba(255,255,255,.06)`) inside glass cards.
- **Hover states:** links/nav lighten toward `text-primary` with an animated green underline that scales in from the left. Buttons: primary brightens (`brightness(1.1)`); secondary shifts border + text to green. Cards lift + glow.
- **Press states:** primary button darkens (`brightness(0.95)`). No aggressive shrink.
- **Focus:** always a visible **2px bright-green ring** with 2px offset (accessibility-first, spec §3.2).
- **Animation:** restrained and purposeful — scroll-reveal fades with slight upward drift + tiny scale (0.97→1), 200–300ms ease-out. The hero mesh drifts on a slow 30s loop. Everything respects `prefers-reduced-motion`.
- **Transparency/blur:** used deliberately — the sticky header gains background opacity + backdrop blur as you scroll; dark cards and form fields use translucent glass fills.
- **Layout:** `1200px` max content width, `720px` narrow; responsive gutters (24 → 48 → 80px); large vertical section rhythm (120 → 200px). Eyebrow → title → description is the standard section-header stack.
- **Imagery vibe:** when illustration appears it's line-art / animated SVG in brand green on dark, not photography. Team uses cartoon ("toon") avatars.

---

## Iconography

- **Icon set:** [**lucide**](https://lucide.dev) (`lucide-react` on the site) — thin 1.5–2px stroke, rounded joints. This is the brand's icon language; the UI kit loads lucide via CDN. Use lucide for any new work.
- **Rendering:** inline SVG (stroke, `currentColor`) so icons inherit text color — typically green on dark, or muted gray. Common glyphs: `package`, `database`, `file-text`, `cpu`, `code-xml`, `palette`, `trending-up`, `external-link`, `check`, `arrow-right`, plus social (`github`, `facebook`, `instagram`, `twitter`) and `menu`, `sun`, `moon`.
- **Entity icons:** square-cropped PNG logos of third-party brands available on the CDN (`https://cdn.shruggie.tech/entity-icons/{slug}.png`, ~60 known). Use these when referencing external services rather than drawing them.
- **The shruggie mark:** the logo is a custom-designed stylized `\(ツ)/` face in bright green (arms, eyes, smile) — **not** the Unicode emoji. Three lockups shipped: `logo-darkbg.png` (dark surfaces), `logo-lightbg.png` (light surfaces), `logo-icon-only-green.png` (standalone mark). Never redraw or approximate the mark — use the PNGs.
- **Emoji / unicode:** avoid, except the textual `¯\_(ツ)_/¯` emoticon (brand signature) and the small 🇺🇸 flag in the footer.

---

## Index / Manifest

**Root**
- `styles.css` — global entry point (link this one file). `@import`s all tokens + base.
- `thumbnail.html` — homepage tile.
- `readme.md` — this file. · `SKILL.md` — Agent-Skills-compatible entry.

**Tokens** (`tokens/`) — `fonts.css` (@font-face), `colors.css` (brand + light/dark semantic), `typography.css` (families + type scale), `spacing.css` (layout, spacing, radii, shadows), `base.css` (element resets, links, focus).

**Components** (`window.ShruggieTechDesignSystem_1f6967.*`)
- `components/core/` — **Button**, **Badge**, **Card**, **SectionHeading**, **ShruggieCTA**, **Divider**.
- `components/forms/` — **Input**, **Textarea**, **Select**.

**UI Kits**
- `ui_kits/shruggie-web/` — interactive marketing-site recreation (Home, Services, Products, Contact + nav/footer).

**Guidelines / specimen cards** (`guidelines/`) — Colors (brand, dark surfaces, light surfaces, semantic), Type (display, body, mono), Spacing (scale, radii & shadows), Brand (logos, voice).

**Assets** (`assets/`) — logos (`logo-darkbg`, `logo-lightbg`, `logo-icon-only-green`, `socialmedia_logo`) and self-hosted WOFF2 fonts (`fonts/`).

### Intentional additions
- **Input / Textarea / Select** — the website defines these as inline field styles inside `ContactForm.tsx` rather than exported primitives. They're promoted to components here (styling lifted verbatim) so the contact UI kit and future forms can compose them. Everything else mirrors an exported `components/ui/*` primitive.

### Notes / substitutions
- Fonts are the real self-hosted WOFF2 files from the repo — **no substitutions**. Geist Pixel (decorative) is not included; pull it from the brand typography CDN if needed.
- Brand **color** values came from the website source, not the CDN asset index (which defers colors to a private MCP server). If canonical values ever change, the site's `styles/globals.css` is the source of truth.
