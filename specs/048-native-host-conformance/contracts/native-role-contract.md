# Native Role Contract

| Platform role | Intended source | Required host behavior | Verification |
| --- | --- | --- | --- |
| PWA `any` | Ordinary web PNG | Natural unmasked icon, transparent when declared | Manifest points to ordinary asset; alpha matches declaration |
| PWA `maskable` | Dedicated web PNG | Opaque edge and essential mark inside central 80%-diameter circle | Manifest points to dedicated asset; circle crops no essential content |
| Android adaptive foreground | Transparent mark layer | Essential art inside 66/108 region | Alpha and bounds pass under circle, rounded-square, squircle |
| Android background | Full field | All host masks covered | No transparent or contrasting unintended wedges |
| Android monochrome | Transparent single-ink layer | Host tint preserves approved silhouette | XML mapping and alpha/bounds checks |
| Android legacy / Play | Separate opaque square roles | Host scales or applies listing mask | Density and 512px mappings, no unapproved outer mask |
| iOS/iPadOS and macOS | Flat catalog/icon container | Host applies own mask and appearance | Catalog/container size, appearance, alpha, host preview |
| Win32 ICO | Transparent by default without an approved square enclosure | Taskbar/title/Alt+Tab show mark without an accidental square | Decoded frames and light/dark small-size composites |
| MSIX target-size/unplated | Theme-specific taskbar assets, transparent by default without an approved enclosure | No unintended plate or dark square | Declared variants and decoded pixels |
| MSIX tile / Store | Plated square | Intentional host tile or listing surface | Opacity, plate boundary, manifest mapping |

The integration guide must instruct consumers to embed or declare the exact asset for their package type. A structural kit pass is not evidence that an application selected that asset.
