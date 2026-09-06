# Site Icon Contract

## Published root files

- `/favicon.svg`
- `/favicon-16x16.png`
- `/favicon-32x32.png`
- `/favicon.ico`
- `/apple-touch-icon.png`
- `/android-chrome-192x192.png`
- `/android-chrome-512x512.png`
- `/site.webmanifest`

## Metadata

Every Next.js route inherits the shared root metadata contract. It declares the SVG first, then ICO and sized PNG fallbacks, plus the Apple touch icon and web manifest. Generated guideline HTML receives the same preferred SVG relationship.

## Integrity rules

1. Every root file is copied from the verified ShruggieTech `icons/web/` suite.
2. SVG files contain no unresolved local, relative, or remote image dependency.
3. PNG files decode, match exact dimensions, and contain visible approved artwork.
4. Apple touch and manifest application icons are fully opaque.
5. ICO files contain all declared image entries and valid offsets.
6. Manifest icon URLs return the declared MIME type and dimensions.
7. The homepage, documentation index, and nested documentation routes all load the same preferred icon successfully.
8. A missing generated source is fatal; raw source fallbacks do not mask an incomplete production kit.
