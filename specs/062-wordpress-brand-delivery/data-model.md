# Data model: S062

## WordPress adapter

- `adapter_version`: independent semantic version.
- `versions`: exact brand, canon, interface, recipes, compiler, and adapter versions.
- `wordpress`: exact tested core/PHP pairs, `theme_json_version`, native editor baseline.
- `entries`: relative theme settings, supplement, support matrix, source theme, ZIP, and inventory paths.
- `scope`: stable brand namespace and content selectors.

## Theme settings and assets

- `theme.json`: format 3; formal and cue palettes with separate namespaced slugs; typography/font faces; spacing, content widths, colors, elements, and supported core block styles.
- `assets`: referenced local fonts and raster logo alternatives with source path, license, size, and checksum.
- `support-matrix.json`: per recipe/block status and reason; fixture evidence gates supported claims.

## Installable theme

- Root folder is stable `stbb-<full-brand-slug>` and contains `style.css`, `theme.json`, `functions.php`, `templates/`, `parts/`, `patterns/`, and `assets/`.
- `theme-inventory.json` maps every archive path to byte length and SHA-256. It is outside the ZIP to avoid self-checksum recursion.
- ZIP uses sorted safe paths, fixed timestamps and permissions, and no source tree escape.

## Customization state

- Generated defaults are file-owned. Pages/posts/navigation and saved Global Styles or template overrides are site-owned database records.
- Drift report compares effective saved settings/template records with the pinned generated defaults without deleting or rewriting user changes.
