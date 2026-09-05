# Research: Brand Platform Refresh

## Decision 1: Use the Fragcap Fumadocs architecture as the structural reference

**Decision**: Use Fumadocs Core 16.14.3, Fumadocs UI 16.14.3, Fumadocs MDX 15.2.3, zbsearch 3.3.4, and Tailwind CSS 4.2.4 with the repository's existing Next.js 16.3.4 and React 19.2.8 stack.

**Rationale**: The sibling Fragcap site already proves this combination with static export, client-side static search, responsive docs navigation, semantic Markdown tables, route metadata, and local branding. Reusing the proven version family reduces integration uncertainty while keeping this repository's branding and content independent.

**Alternatives considered**: Adding only a GitHub Flavored Markdown plugin would fix tables but not deliver the requested navigation, search, table of contents, metadata, or sister-project experience. Building a custom documentation framework would duplicate solved work.

## Decision 2: Generate MDX from authoritative skill references

**Decision**: Derive `.mdx` pages and navigation metadata under ignored `site/generated/docs/` during `prepare_site.py`, then regenerate the Fumadocs source adapter before type checking or building.

**Rationale**: The constitution requires the public site to consume authoritative generated values and the issue forbids a second maintained documentation tree. The existing site build already runs Python preparation before Next.js.

**Alternatives considered**: Committing copied MDX would drift. Loading Markdown strings at runtime would retain the current flat renderer and bypass Fumadocs compilation. Moving the authoritative references into the site would break the skill package.

## Decision 3: Rewrite public terminology only outside literal code

**Decision**: Replace public prose uses of "canon" with "brand system" during documentation derivation while preserving fenced code, inline code, schema keys, filenames, and compatibility identifiers.

**Rationale**: The user explicitly rejected the term in public marketing and documentation, but changing technical keys such as `canon` would expand S006 into a schema migration and break consumers. A line-aware transform separates public explanation from literal interfaces.

**Alternatives considered**: Global replacement would corrupt commands and JSON. Editing every skill source paragraph would change the underlying operator vocabulary and create a much wider migration. Leaving the term visible would fail issues #100 and #102.

## Decision 4: Discover only production brand sources

**Decision**: Normal builds enumerate `brands/*/brand.json` only. Site preparation accepts verified generated records from those sources and rejects duplicate or non-production identities. Tests create temporary input inside the test runner when synthetic coverage is required.

**Rationale**: This removes the public fixture and the hard-coded expected set while making a new production brand flow automatically through build and site preparation.

**Alternatives considered**: Keeping an ignored fixture source would still create a special operational path. Keeping `fixtures/` in discovery would risk publishing future test data. Hard-coding five slugs would immediately recreate the maintenance problem.

## Decision 5: Reuse generated identity assets without transformation

**Decision**: Use each generated color mark SVG inside a square card treatment, the generated ShruggieTech horizontal white logo in shared navigation, the generated favicon set, and the existing generated 1280 by 640 social-preview PNG.

**Rationale**: The generated kit already supplies correctly governed assets, including a social preview with the target dimensions. Copying them preserves identity geometry and satisfies the site-consumption boundary.

**Alternatives considered**: Drawing new icons or composing new marks would create an unnecessary identity decision. Using color swatches would not meet the card requirement. Linking deep download paths from metadata would make stable site identity depend on route layout.

## Decision 6: Separate the custom site shell from the Fumadocs docs shell

**Decision**: Keep one root provider and metadata layer, place homepage and brand routes in a route group with custom ShruggieTech header and footer, and use Fumadocs `DocsLayout` for `/docs` with shared company navigation options.

**Rationale**: A body-level custom header duplicates the Fumadocs docs navigation. Route grouping preserves public URLs and gives each surface the correct information architecture.

**Alternatives considered**: Forcing the custom header around Fumadocs would create double navigation. Using Fumadocs for the marketing homepage would constrain the required portfolio design. Maintaining unrelated headers would create copy and link drift.

## Decision 7: Verify the static product in a real browser without spawning a console server

**Decision**: Add a Node verification script that starts an HTTP server in-process, launches headless Playwright, runs axe, checks responsive overflow and semantic tables, and closes both resources in one process.

**Rationale**: Static HTML assertions cannot measure rendered layout or accessibility. An in-process server avoids a project-owned console subprocess and remains portable in CI.

**Alternatives considered**: Playwright `webServer.command` would spawn a separate console process locally. A manual-only review would not prevent regression. A server-based runtime would violate static hosting.

## Decision 8: Amend the constitution as a major version

**Decision**: Change constitution 1.0.0 to 2.0.0, removing the mandate to commit and build a persistent fixture while requiring isolated temporary regression data and retaining all production verification gates.

**Rationale**: The previous P1 and P4 requirements are incompatible with issue #103. Removing a mandatory source class is backward-incompatible governance, so the constitution's own version policy requires a major bump.

**Alternatives considered**: A patch or minor bump would understate the semantic change. An exception would preserve a requirement the owner explicitly rejected. Ignoring the conflict would fail analysis.
