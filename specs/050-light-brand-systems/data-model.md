# Data Model: Guide Presentation

## Brand source

- `guide.surface_mode`: optional enum `dark | light`; absent means `dark`.
- `light_surfaces`: governed source colors needed when light is explicit, including base, card, popover, secondary, hover, foreground, and muted foreground. Validation rejects malformed values and insufficient local AA pairings.
- `showcase_surface`: existing governed role, such as `light.card`, used for the public brand card. Its actual color and foreground are resolved during site preparation.

## Generated guideline portal

- `brand.surface_mode`: required resolved mode in generated output. Older source without a declaration emits `dark`.
- `presentation`: selected semantic token colors for background, foreground, card, muted, secondary, border, popover, primary, focus ring, action, and state roles. Values derive from the generated light or dark palette, not a handwritten parallel brand stylesheet.
- `presentations`: complete generated `dark` and `light` semantic token blocks, used when a governed showcase surface has a mode different from the guide's selected mode.
- `asset_families[].assets[].surface`: existing independent light/dark preview-well declaration, retained for each asset.

## Generated site record

- `showcaseSurface` and `showcaseForeground`: existing resolved values for a governed brand card.
- `showcaseMode` and `showcaseTokens`: selected local card colors when a brand declares a showcase surface. Absence preserves the existing dark fallback presentation.

## State and validation

- Source missing mode -> resolved `dark` -> dark generated guide and site route.
- Source explicit `light` -> validated governed light values -> light generated guide, site route, and eligible showcase card.
- Invalid enum or incomplete/low-contrast explicit light -> source validation error before publishable output.
- Visitor site-theme changes do not mutate brand presentation; asset wells remain per-asset.
