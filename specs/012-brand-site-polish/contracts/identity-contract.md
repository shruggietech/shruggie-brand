# Identity Contract: S012

## Canonical inputs

- The ShruggieTech application-icon background is the exact canonical void value declared in `brands/shruggietech/brand.json`.
- Mark and wordmark geometry, authoritative raster sources, source hashes, and generated path data remain unchanged.
- The site copies identity files only from the verified generated ShruggieTech kit.

## Public destinations

| Destination | Generated source | Required treatment |
| --- | --- | --- |
| `/favicon.svg` | `icons/web/favicon.svg` | Reduced mark on opaque canonical black |
| `/favicon-16x16.png` | `icons/web/favicon-16x16.png` | Reduced mark on opaque canonical black |
| `/favicon-32x32.png` | `icons/web/favicon-32x32.png` | Reduced mark on opaque canonical black |
| `/favicon.ico` | `icons/web/favicon.ico` | Every 16, 24, 32, 48, 64, 128, and 256 frame uses canonical black |
| `/apple-touch-icon.png` | `icons/web/apple-touch-icon.png` | Approved opaque black plate and safe area |
| `/android-chrome-192x192.png` | `icons/web/android-chrome-192x192.png` | Approved opaque black plate and safe area |
| `/android-chrome-512x512.png` | `icons/web/android-chrome-512x512.png` | Approved opaque black plate and safe area |
| `/shruggietech-logo-dark.svg` | `logos/svg/shruggietech-horizontal-color.svg` | Colored dark-surface lockup |
| `/shruggietech-logo-light.svg` | `logos/svg/shruggietech-horizontal-light.svg` | Colored light-surface lockup |

## Fail-closed verification

- PNG and embedded ICO frames require declared dimensions, sRGB, opacity, visible foreground, and exact black corner pixels.
- SVG favicon output requires a canonical black background declaration, embedded self-contained artwork, and no unresolved dependency.
- Header and footer browser checks require the visible lockup source to match the expected theme-specific colored destination and retain meaningful alternative text.
- White, transparent, empty, malformed, off-token, missing, or monochrome substitutions fail.
