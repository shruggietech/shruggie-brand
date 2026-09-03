# Feature specification: Brand system foundation

## Goal

Create the public source repository, verified build pipeline, installable brand kits, and static reference site for the ShruggieTech brand system.

## User outcomes

- A product team can download one complete, licensed kit or install its shadcn theme from the published registry.
- A maintainer can change source-only inputs and rebuild all production kits plus the fixture with zero reported problems.
- A designer or developer can read the generated guidelines and brandbuilder references without relying on the migration source folder.
- A release consumer can identify the skill version, canon version, and migration requirement from every release.

## Functional requirements

1. The repository contains the Apache-2.0 brandbuilder, reserved-mark notice, canonical fonts, five source-only production brands, and one synthetic fixture.
2. Every kit build performs geometry, contrast, rhetoric, rendering, pagination, and manifest verification.
3. CI rebuilds every kit, verifies the synchronized agent contract, exports the site, and retains built kits as an artifact.
4. The Next.js App Router site uses static export and local canonical fonts.
5. The site copies guidelines, registry JSON, PDFs, masters, favicons, and specimens from verified build output without re-authoring them.
6. GitHub Pages publishes the site at `brand.shruggie.tech` with HTTPS.
7. Tagged releases contain two licensed skill bundles and five licensed production-kit archives.

## Acceptance criteria

- A cold clone can follow `CONTRIBUTING.md` and complete the full build without undocumented steps.
- All six builds report zero problems.
- The five registry theme URLs return valid JSON.
- `npx shadcn@latest add @covarity/theme` succeeds against the deployed registry.
- The repository `build` check is required before merging to `main`.
