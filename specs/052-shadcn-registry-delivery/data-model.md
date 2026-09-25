# Data Model: shadcn Registry Delivery

## Registry item

Fields: `name`, `type`, `title`, `description`, optional `files`, `cssVars`, `css`, `dependencies`, `registryDependencies`, and `docs`. The generator creates one in-memory item object per advertised installable unit. The direct endpoint is that object plus its schema URL. The catalog entry is a projection of the same object, not a second authoring path.

## Public catalog

Fields: schema URL, brand name, homepage, description, and ordered item projections. It is an inventory for discovery. Every item name maps to one sibling `{name}.json` endpoint. The theme may have no files because its CSS variables are the payload. UI items require nonempty source content and safe target paths.

## Local font bundle

Fields: generated `nextjs/fonts.ts`, referenced `fonts/` files, approved face metadata, and setup instructions. This bundle is not a `registry:font` item under the pinned shadcn contract. Local paths resolve inside the downloaded kit and are copied together into the consumer.

## Consumer fixture

A disposable directory contains a declared Next.js/Tailwind/shadcn configuration, a local HTTP view of generated registry endpoints, and installed results. It is created outside production discovery and removed after the test. The test records CLI version, item names, output paths, and local font resolution.
