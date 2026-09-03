<!-- verify:allow-rhetoric reason="Preserved parent skill contains deliberate brand slogans and voice examples." -->

---
name: shruggietech-design
description: Use this skill to generate well-branded interfaces and assets for ShruggieTech, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `readme.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Quick reference
- **Mode:** dark-first. Base `#000`; section surfaces are subtly-tinted near-blacks. Light mode (`#F8F8F6`) is a reading-mode alternative.
- **Signature color:** bright green `#2BCC73` (accent) · deep green `#00AB21` (hover) · orange `#FF5300` / CTA `#C24000` (rare emphasis).
- **Type:** Space Grotesk (display, 500/700, tight tracking) · Geist (body, 400/500) · Geist Mono (labels/code/product names).
- **Voice:** direct, helpful, slightly witty; "we"→"you"; no corporate fluff. Signature `¯\_(ツ)_/¯` "We'll figure it out." on the primary CTA, in green, one moment per view.
- **Icons:** lucide (thin stroke). **Logo:** use the PNGs in `assets/` — never redraw the shruggie mark.
- **Load the system:** link `styles.css`; use components from `window.ShruggieTechDesignSystem_1f6967` after loading `_ds_bundle.js`.
