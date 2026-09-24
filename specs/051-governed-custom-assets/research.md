# Research

## Existing paths

- `brand_contract.py` already provides contained-path, SHA-256, passive SVG, and authoritative-input validation. Extend these helpers instead of duplicating weaker checks.
- The I Heart PR Tours sand SVGs are committed and hash-bound in `authoritative_inputs`. They are not canonical logo bindings. Leave their source bytes and approval-ledger relationships untouched.
- `gen_guidelines.py` and `gen_guide_pdf.py` currently read `guide.expressions` directly. The generated portal copies that list but has no corresponding hosted topic. Replace these reads with a validated eligible selector.
- `scripts/prepare_site.py` has a fixed eight-topic contract and rewrites only existing asset-family paths. Its optional expressions topic and delivery records must be projected and checked together.
- The site route generator derives topic routes from generated portal topics; a content renderer and inventory section are needed, not a new hard-coded route tree.

## Decisions

- Supported public media for S051: static passive SVG and fully decodable raster PNG/JPEG/WebP. SVG animation is rejected because embedded image-document motion cannot be stopped by page-level reduced-motion CSS. Motion/WebGL metadata is modelable but such files do not become publishable until supported preview and reduced-motion verification exists.
- Distinguish approval status from publication eligibility. Only both approved and public records enter outputs.
- Treat asset-source paths as brand-relative, contained committed files. Existing `authoritative_inputs` can record the same supplied source, but `custom_assets` is the public expression authority.
- Require declared preview well and containment. No crop, recolor, or source conversion in generated previews.

## Alternatives rejected

- Keeping `guide.expressions` beside the new collection would create divergent inventories and a publication bypass.
- Copying source assets directly from the site repository would create a second, unverified brand source.
- Renaming or normalizing supplied SVG paths would violate source fidelity.
