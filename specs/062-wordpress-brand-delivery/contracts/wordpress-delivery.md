# WordPress delivery contract

## Output paths

`wordpress/adapter.json`, `wordpress/support-matrix.json`, `wordpress/theme-inventory.json`, `wordpress/theme/`, `wordpress/<slug>-stbb-theme.zip`, and `wordpress/README.md` are required for every production kit. The theme ZIP root contains one `stbb-<full-slug>/` directory. Existing full-kit download retains these files in its authoritative manifest.

## Version and support claims

Adapter version starts at 1.0.0 independent of compiler and brand versions. The adapter record states exact tested pairs: WordPress 6.9.9/PHP 8.2 and WordPress 7.1.2/PHP 8.3. A pair is supported only after its runtime fixture passes. Other versions, classic themes, builders, commerce, forms, multilingual and caching plugins are unverified unless later tested.

## Native mapping

Native `theme.json` owns site-wide colors, type, spacing, content widths, links, buttons, and relevant blocks. `stbb-<brand>-` names prevent collisions. Formal colors and interface cues have separate palette groups. Supplemental CSS is limited to the site content and editor content roots, uses `:where()` for low specificity, and does not target admin chrome. There are no generated HTML IDs in patterns.

## Archive and recovery

Every ZIP member appears exactly once under the single theme root and matches the normalized inventory hash and size. Unsafe paths, missing files, external URLs in local asset references, mismatched versions, or unlicensed included fonts fail verification. An update workflow captures database customizations and pins prior ZIP/checksum for rollback.
