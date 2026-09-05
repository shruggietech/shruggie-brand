# Generated Content Contract

## Production brand discovery

- Normal build discovery reads source directories beneath `brands/` only.
- Every discovered directory must contain `brand.json` and must have a unique derived slug.
- Site preparation reads only verified `dist/<slug>/brand.json` records whose slug exists in production source discovery.
- Site preparation fails on missing production output, unexpected generated brand output, duplicate slugs, invalid registry data, or missing logo, icon, specimen, guide, or download assets.
- No fixed brand count or expected-slug set is maintained in site code.

## Published brand record

The generated `site/generated/brands.json` array contains the fields defined in `data-model.md`, is deterministically sorted by slug, and contains exactly one record for each production brand source.

## Documentation derivation

- Each `skill/references/*.md` file produces one `site/generated/docs/<slug>.mdx` page.
- The first H1 becomes frontmatter title and is removed from the body.
- A non-empty frontmatter description is derived deterministically from source prose or an explicit site-owned fallback.
- Public prose rewrites the standalone word "canon" outside inline and fenced code. Literal technical content remains byte-equivalent within its code boundary.
- `site/generated/docs/meta.json` records deterministic navigation order.
- The generated index page explains the method and links to the skill download without duplicating the reference content.

## Identity assets

- Root favicon, touch icon, manifest icons, navigation logo, and social preview are copied from verified ShruggieTech kit output.
- Portfolio icons and brand-page logos point to copied generated kit assets.
- No image is traced, redrawn, optimized, color-normalized, or byte-compared as a correctness gate.
