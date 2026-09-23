# Guide Presentation Contract

## Source declaration

`guide.surface_mode` is optional. Only `dark` and `light` are valid. Omission is backward-compatible `dark`. An explicit light declaration requires a complete governed light palette and WCAG 2.1 AA pairings at rendered roles.

## Generator contract

PDF outer ground, portable document outer ground, and the `brand.surface_mode` in `guidelines/portal.json` equal the resolved source declaration. The PDF may show opposite-mode comparison wells, but no outer page changes ground. Per-asset `surface` values remain independent. The generated portal includes `presentation` for the selected guide mode and complete `presentations.dark` and `presentations.light` semantic token blocks for independently governed showcase surfaces, so a host does not infer presentation from visitor settings.

## Hosted-site contract

The brand guideline and downloads route set `data-guide-mode` from `brand.surface_mode`, declare the selected semantic variables and corresponding Fumadocs aliases locally, and keep that scope stable in SSR/no-script output. A host theme toggle does not change the brand route's governed mode. The public portfolio shell may stay dark; a card with `light.*` showcase surface uses its governed background, foreground, icon well, action, border, hover, and focus colors in desktop and mobile forms.

## Verification contract

An invalid source mode fails before kit generation. PDF QC checks all page outer grounds against resolved mode. Browser checks cover the route, its nav/sidebar/panels and controls, and a representative white-well asset in host light and dark themes. Foreground, meaningful border, interactive state, and focus pairings meet WCAG 2.1 AA on actual local surfaces. Generated PDFs and screenshots are evidence only, never committed source.
