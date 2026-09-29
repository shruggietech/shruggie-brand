# Public Kit and Site Contract

## Brand source inputs

The committed source root is `brands/local-companion/`. It contains `brand.json`, `build/mk_paths.py`, and `identity-continuity.json`. The Full and Reduced logo paths in `brand.json` must match the approved `glyphkit` helper output. The continuity record binds the identity snapshot, renderer, palette qualification, and 32 proofs. Product screenshots, chats, model files, character portraits, and generated exports do not enter this source root.

## Generated consumer outputs

The build emits `dist/local-companion/` with logo SVG and PNG colorways, wide and stacked lockups, wordmark, reduced small icon, favicon and platform icon suites, social share image, guideline documents, color-role binding, interface contracts, verification report, and release manifest. Each output is derived from source and carries its recorded provenance or hash. `verify.py` and `validate_glyph.py` must report zero problems and failures respectively.

## Public routes and archive

`scripts/prepare_site.py` consumes the verified kit and exposes its catalog entry, Local Companion landing page, guidance, registry, metadata, social preview, and versioned downloads at the official `brand.shruggie.tech` subdomain. The per-brand release archive is named according to the existing `<slug>-brand-<brand-version>-bb<builder-version>.zip` contract. Published SHA256SUMS must match that archive. The site source must not restate kit values or include private application data.

## Compatibility boundary

The kit supplies a portable design identity. The current Windows app uses Segoe UI Variable and Cascadia Mono, and retains its own existing UI assets until a separate app integration change. The brand kit does not claim the installed app already uses the new symbol, fonts, or icon assets.
