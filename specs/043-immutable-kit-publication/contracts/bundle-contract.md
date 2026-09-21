# Bundle Contract

Each production kit MUST contain exactly one `enforcement/bundle.json` record.

## Canonical identity

- `package.id`: `<brand-slug>-brand-<brand-version>-bb<brandbuilder-version>`
- `package.filename`: `<package.id>.zip`
- `package.brand_version`: the governed identity version from `brand.json`
- `package.brandbuilder_version`: the compiler release from `skill/SKILL.md`

Changing BrandBuilder while holding brand identity constant MUST change the package ID and filename. It MUST NOT change the brand version by itself.

Every governed source change that can alter generated kit bytes, bundle fields, or compatibility semantics MUST advance BrandBuilder. A released BrandBuilder version cannot be reused for a different governed bundle.

## Required agreement

The bundle record, archive filename, manifest, consumer recovery record, hosted registry, release asset list, and checksum authority MUST agree on package ID, filename, source revision, release version, and tag. Verification fails closed on any disagreement.

## Legacy names

`<brand-slug>-brand-<brand-version>.zip` is a legacy, non-canonical form. Publication MUST NOT create or update that name as an alias to current bytes.
