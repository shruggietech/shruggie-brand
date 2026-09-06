# Research: Phase 13 Brand Site Polish

## Decision 1: Correct identity at canonical inputs and generated selection points

**Decision**: Change `logo.application_icon.background` to the existing canonical void value and select `shruggietech-horizontal-color.svg` for dark surfaces plus `shruggietech-horizontal-light.svg` for light surfaces.

**Rationale**: The generator already plates every web and operating-system application icon from the application-icon background field, and it already produces both colored lockup variants from preserved authoritative geometry. This fixes all downstream outputs without redrawing or site-authored copies.

**Alternatives considered**: Recoloring copied site assets was rejected because it would violate the source-driven contract. Using one colored lockup in both themes was rejected because the generated light variant carries the approved light-surface wordmark treatment.

## Decision 2: Use supported Fumadocs viewport filtering

**Decision**: Model `Documentation` as a shared navigation item, while `Download the Skill` and `View on GitHub` are menu-only items. Documentation layouts omit the redundant docs-root link through the existing `includeDocsLink` option.

**Rationale**: Fumadocs exposes `on: nav`, `on: menu`, and `on: all` as its supported item contract. This provides the exact mobile/desktop inventory without replacing accessible menu, focus, escape, search, or theme behavior.

**Alternatives considered**: CSS-only duplicate links were rejected because hidden duplicate anchors complicate accessibility assertions. A custom navigation implementation was rejected as unnecessary framework replacement.

## Decision 3: Normalize terminology at authoritative sources

**Decision**: Generate the documentation root as `Documentation` and change the first source heading to `Variance Contract`, while retaining existing slugs, filenames, route paths, and descriptions.

**Rationale**: Generated frontmatter, search data, page trees, breadcrumbs, structured data, social metadata, and pagination all derive from these source values. Source correction prevents regeneration drift.

**Alternatives considered**: JSX-only display substitutions and post-build text replacement were rejected because metadata and search output would remain inconsistent.

## Decision 4: Bind interaction roles to generated semantic tokens

**Decision**: Use `--brand-cta` for orange primary fills, `--primary` for surface-appropriate green secondary emphasis, and `--sh-motion-normal` for the eligible text-link underline. Scope pagination through an explicit `docs-pagination` class supplied to the Fumadocs footer slot.

**Rationale**: These tokens are already generated from canonical ShruggieTech source. An explicit pagination hook is more stable than selecting minified utility-class fragments and keeps card treatment separate from inline links.

**Alternatives considered**: Literal colors in site CSS were rejected because they duplicate generated brand values. A universal anchor underline was rejected because buttons, cards, logos, and heading anchors require distinct interaction semantics.

## Decision 5: Verify semantics and measured presentation

**Decision**: Extend the complete browser verifier to assert exact navigation labels and visibility, rejected terminology absence, lockup source selection, CTA and link computed styles, reduced-motion behavior, pagination resting and focus states, and black favicon corner pixels including every ICO entry. Expand visual evidence to the landing, documentation index, and Variance Contract routes across two widths and two themes.

**Rationale**: Existence-only tests previously allowed wrong-but-decodable assets and visually incomplete treatments to pass. Source tests prevent generator regression, while computed browser and pixel assertions prove the emitted result.

**Alternatives considered**: Snapshots alone were rejected because they are not fail-closed semantic or color contracts. Byte comparison of PNG or PDF outputs was rejected by repository governance.

## Decision 6: Preserve the existing public and security boundary

**Decision**: Add no runtime service, user input, authentication, storage, or new external origin. Retain the current approved GitHub download and repository destinations and validate exact URLs.

**Rationale**: S012 is a static presentation correction. Keeping the existing static boundary avoids new privacy, tenancy, injection, or availability risks.

**Alternatives considered**: Dynamic navigation configuration and remote asset loading were rejected because they create unnecessary runtime dependencies and weaken deterministic export.
