# Feature Specification: Branded Documentation and Discovery Completion

**Feature Branch**: `codex/009-docs-discovery-completion`

**Created**: 2026-09-05

**Status**: Ready for Review

**Input**: Complete Phase 11 by addressing GitHub issues #108, #109, and #111 in one end-to-end slice: repair documentation code blocks, callouts, and navigation; apply the canonical ShruggieTech visual system to documentation; and complete route-aware structured data, social previews, and discovery URL parity.

## Clarifications

### Session 2026-09-05

- Q: Which open issues define S009? → A: S009 covers #108, #109, and #111 together because they share the documentation shell, route contract, generated content, and emitted-site verification surfaces.
- Q: Which identity source governs the documentation visual system? → A: Canonical ShruggieTech brand tokens and shipped logo geometry govern all visual decisions; near-match colors and redrawn marks are prohibited.
- Q: How should documentation notices be authored? → A: Authoritative references use explicit portable NOTE, WARNING, and CAUTION blockquotes that transform deterministically into semantic notices without promoting ordinary prose.
- Q: What URL policy governs discovery metadata? → A: Every public page uses one absolute trailing-slash canonical route, reused exactly by canonical, Open Graph, sitemap, breadcrumb, and structured-data identifiers.
- Q: How many explicit Codex review rounds are permitted? → A: One automatic round and at most one explicit `@Codex` round; no third request is allowed.

## Scope

### In Scope

- Documentation typography, surfaces, navigation states, focus treatment, logo treatment, code panels, callouts, and responsive behavior.
- Deterministic generation of documentation components from authoritative reference sources.
- Shared canonical-route, page-metadata, structured-data, social-preview, sitemap, and breadcrumb contracts for every emitted public route.
- Route-relevant social-preview content and alternative text for the homepage, brand pages, downloads, guidelines, the documentation index, and nested documentation pages.
- Automated source, emitted-file, browser, accessibility, keyboard, metadata, structured-data, image, and URL-parity verification.
- Complete S009 Spec Kit artifacts, verification evidence, issue traceability, and bounded review ledger.

### Out of Scope

- Editing the primary `shruggie.tech` website or its repository.
- Changing production brand identity geometry, source marks, wordmarks, or palette definitions.
- Rewriting authoritative documentation prose into a second site-only content source.
- Changing brandbuilder generation behavior unrelated to documentation preparation.
- Publishing a release tag or merging the S009 pull request.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read Technical Documentation Without Friction (Priority: P1)

A designer, developer, or operator can read long-form guidance, distinguish inline literals from fenced examples, copy complete samples, recognize critical notices, and understand the documentation hierarchy without broken presentation or duplicate navigation.

**Why this priority**: The current code presentation, missing notices, and duplicate navigation directly obstruct the primary documentation journey and undermine confidence in the published system.

**Independent Test**: Open the documentation index and the toolchain reference at desktop and mobile widths, then inspect fenced examples, inline code, notices, navigation, keyboard behavior, and horizontal containment.

**Acceptance Scenarios**:

1. **Given** a reference containing a fenced multiline sample, **When** a reader views and copies it, **Then** the sample appears as one cohesive panel with preserved whitespace, useful syntax distinction, contained overflow, and an accessible copy action.
2. **Given** prose containing a narrowly defined prerequisite, warning, hard gate, or destructive consequence, **When** documentation is generated, **Then** the passage appears as an appropriate semantic notice without duplicating or changing its authoritative meaning.
3. **Given** the documentation navigation at any supported width, **When** the reader opens the index or a nested page, **Then** the documentation root appears once and the reader retains a clear route to the index.

---

### User Story 2 - Recognize ShruggieTech Documentation (Priority: P1)

A reader experiences a compact, legible documentation product whose typography, surfaces, identity, links, orientation states, and focus treatment clearly belong to ShruggieTech in both light and dark themes.

**Why this priority**: The documentation currently inherits marketing-scale headings and framework defaults that obscure content and fail to demonstrate the finalized brand system.

**Independent Test**: Compare the rendered documentation index and a long reference page across light and dark themes at representative desktop and mobile widths, including navigation, heading hierarchy, first-viewport density, links, focus indicators, logo treatment, code panels, and notices.

**Acceptance Scenarios**:

1. **Given** a normal desktop viewport, **When** the documentation index opens, **Then** its title, description, introductory content, and the start of the next meaningful element are visible without scrolling.
2. **Given** any documentation page, **When** a reader changes theme or viewport size, **Then** canonical ShruggieTech semantic colors, compact heading hierarchy, readable surfaces, and responsive navigation remain coherent and WCAG 2.1 AA compliant.
3. **Given** keyboard navigation, **When** focus moves through the documentation shell, **Then** active, current, hover, and focus states are distinct through color and at least one non-color cue.
4. **Given** the documentation sidebar header, **When** it is viewed at supported sizes, **Then** it displays recognizable shipped ShruggieTech geometry at a legible scale without redrawing the mark.

---

### User Story 3 - Share and Discover the Correct Page (Priority: P1)

A visitor, crawler, or social platform receives metadata that accurately describes the exact brand or documentation page, links it to the authoritative ShruggieTech organization, and resolves directly to one canonical URL without avoidable redirects.

**Why this priority**: Generic preview content, absent structured data, and sitemap-to-canonical redirects make the public brand system harder to understand, index, and share accurately.

**Independent Test**: Inspect every emitted public page, the sitemap, and every social-preview asset, then compare canonical, Open Graph, breadcrumb, structured-data, and sitemap identifiers for exact route equality and route-relevant content.

**Acceptance Scenarios**:

1. **Given** the portfolio homepage, **When** metadata is parsed, **Then** it publishes a valid collection or website graph connected to the authoritative ShruggieTech organization without inventing or duplicating company facts.
2. **Given** a documentation or brand route, **When** metadata is parsed, **Then** page-level and breadcrumb data identify that route and its hierarchy using the same canonical identifiers.
3. **Given** any route-specific social preview, **When** its metadata and image are fetched, **Then** the title, description, alternative text, dimensions, format, and URL accurately represent that route.
4. **Given** any sitemap entry, **When** it is requested, **Then** it returns the corresponding exported page directly and exactly equals that page's canonical and Open Graph URL.

---

### User Story 4 - Reject Documentation and Discovery Regressions (Priority: P2)

A maintainer receives a deterministic failure when documentation presentation, accessibility, navigation, route metadata, structured data, social assets, or URL relationships regress.

**Why this priority**: Prior checks asserted tag or file presence but did not prove semantics, relationships, visual containment, or route relevance.

**Independent Test**: Mutate representative generated content, theme states, route values, structured data, or social assets and prove each invalid state is rejected by source-level or emitted-site checks.

**Acceptance Scenarios**:

1. **Given** a broken fenced block, missing copy action, duplicate navigation item, invalid notice, oversized heading, overflow, or inaccessible state, **When** validation runs, **Then** it fails with the affected route and contract.
2. **Given** mismatched canonical, Open Graph, sitemap, breadcrumb, or structured-data URLs, **When** validation runs, **Then** it fails with the exact route relationship.
3. **Given** generic or missing route-preview content, malformed structured data, or an unavailable social asset, **When** validation runs, **Then** publication is blocked.

### Edge Cases

- Documentation source can contain inline backticks, fenced examples with or without a language, nested lists, tables, quoted warnings, and ordinary uses of words such as "must" that must not all become notices.
- Long unbroken sample lines must scroll within their panel while the page remains horizontally contained at 360 CSS pixels.
- Copy controls must remain usable by keyboard and must expose a meaningful accessible name even when scripting or clipboard access fails.
- Active navigation must remain distinguishable in high contrast, light, dark, reduced-motion, and narrow-screen contexts without relying on color alone.
- A wide wordmark can become illegible at compact sidebar height; the selected existing asset must preserve geometry while providing recognizable mark content.
- Route inputs can contain a root path, nested documentation segments, brand slugs, or action suffixes; normalization must not create double slashes, omit the required trailing slash, or permit an external origin.
- Titles and descriptions can contain quotes or non-ASCII characters; structured data and preview generation must preserve them as valid UTF-8 without unsafe markup.
- Breadcrumbs must omit invalid parent pages and must not publish duplicate canonical entities.
- Social-preview generation must remain deterministic, local, and independent of remote fonts or images.
- The local static test server does not emulate redirects; route verification must still prove that every emitted sitemap URL maps directly to an exported page path.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every published fenced sample MUST appear as one cohesive code panel with preserved multiline whitespace, contained horizontal overflow, readable padding, a clear boundary, and a keyboard-accessible copy action.
- **FR-002**: Fenced samples with a declared language MUST retain useful syntax distinctions, while inline code MUST retain a separate compact inline treatment.
- **FR-003**: Documentation styling MUST NOT flatten all syntax tokens to one color or apply inline-code presentation to fenced samples.
- **FR-004**: The documentation preparation contract MUST support selective `info`, `warn`, and `error` notices for defined prerequisites, critical distinctions, hard gates, destructive behavior, and irreversible consequences.
- **FR-005**: Notice generation MUST preserve authoritative wording and source ownership under `skill/references/`, remain deterministic, and leave ordinary paragraphs unchanged.
- **FR-006**: The documentation root label MUST appear exactly once in navigation at every supported breakpoint while retaining a clear path to the documentation index.
- **FR-007**: Documentation headings MUST use an explicitly scoped, compact hierarchy that cannot inherit the public marketing display scale.
- **FR-008**: At a 1280 by 900 CSS-pixel viewport, the documentation index MUST show its title, description, introductory content, and the start of the next meaningful element without scrolling.
- **FR-009**: Documentation semantic surfaces, borders, text, muted text, links, focus rings, code panels, notices, and navigation states MUST derive from canonical ShruggieTech palette roles or documented semantic derivatives.
- **FR-010**: Active sidebar, table-of-contents progress, links, and focus treatments MUST use canonical ShruggieTech green roles and at least one non-color distinction for current and focus states.
- **FR-011**: The documentation sidebar header MUST use existing shipped ShruggieTech geometry in a compact treatment that keeps the identity recognizable at rendered size.
- **FR-012**: Documentation MUST preserve supported light and dark themes, responsive navigation, reduced-motion behavior, local fonts, and network-independent identity assets.
- **FR-013**: Every documentation route MUST remain readable and operable at widths from 360 through 1280 CSS pixels without page-level horizontal overflow.
- **FR-014**: Every text, control, navigation, notice, syntax, and focus role MUST meet WCAG 2.1 AA at rendered size in both supported themes.
- **FR-015**: One route contract MUST normalize every public page to an absolute `https://brand.shruggie.tech` URL with a trailing slash.
- **FR-016**: Canonical, Open Graph, sitemap, breadcrumb, structured-data, and social-preview identifiers MUST be derived from the same normalized route contract.
- **FR-017**: The portfolio homepage MUST publish a valid website or collection graph linked to the authoritative ShruggieTech organization identity at `https://shruggie.tech`.
- **FR-018**: The documentation index and every nested documentation page MUST publish page-level and breadcrumb structured data using their exact canonical identifiers.
- **FR-019**: Every brand detail, downloads, and guidelines route MUST publish page-level and breadcrumb structured data using its exact canonical identifier and source-derived brand name.
- **FR-020**: Structured data MUST NOT invent facts, duplicate the authoritative organization entity, claim ownership of third-party brands, or contradict public page content.
- **FR-021**: Every public route MUST declare route-relevant Open Graph and Twitter titles, descriptions, URLs, image metadata, and alternative text.
- **FR-022**: Every route-relevant social image MUST be generated deterministically from local assets, resolve successfully, use the declared dimensions and media type, and remain legible at preview scale.
- **FR-023**: Sitemap entries MUST exactly equal emitted canonical and Open Graph URLs, map directly to exported page paths, and require no redirect.
- **FR-024**: Existing valid manifest, robots policy, absolute metadata base, title and description behavior, static export, icon suite, and source-driven documentation generation MUST remain intact.
- **FR-025**: Source-level tests MUST cover notice transformation, fenced-source preservation, navigation deduplication, route normalization, breadcrumb formation, structured-data shape, preview descriptors, and sitemap construction.
- **FR-026**: Emitted-site verification MUST parse metadata values and structured data, fetch and inspect social assets, compare route relationships, exercise copy controls and navigation by keyboard, and test desktop and mobile presentation.
- **FR-027**: Visual regression evidence MUST cover the documentation index and `04-toolchain` at representative desktop and mobile widths in both supported themes.
- **FR-028**: Validation MUST reject missing or malformed metadata, conflicting canonical identities, generic route previews, broken social assets, duplicate navigation, inaccessible controls, page overflow, and WCAG 2.1 AA violations.
- **FR-029**: Every production brand kit MUST continue to report zero `verify.py` problems and zero `validate_glyph.py` failures after S009.
- **FR-030**: All changed text MUST use UTF-8 without BOM and LF line endings and MUST contain zero detected mojibake sequences.
- **FR-031**: S009 MUST close #108, #109, and #111 only after the merged implementation provides current-main evidence for every acceptance criterion.
- **FR-032**: S009 publication MUST use one automatic Codex review round and MAY request exactly one explicit second round; every actionable comment MUST be corrected or dispositioned and every review thread MUST be resolved before the owner merge gate.

### Key Entities

- **Canonical Route**: The normalized public path, absolute URL, exported file path, hierarchy, and page kind used by every discovery surface.
- **Page Descriptor**: Source-derived title, description, page kind, route, hierarchy, social-preview content, and publishing relationship for one public page.
- **Structured Data Graph**: The page-appropriate website, collection, page, and breadcrumb nodes that reference one authoritative external organization identity.
- **Social Preview**: A route-specific image and metadata record with title, description, alternative text, dimensions, media type, URL, and deterministic source inputs.
- **Documentation Theme Contract**: The mapping from canonical ShruggieTech palette and typography roles to documentation surfaces, navigation, focus, code, and notice states.
- **Documentation Notice**: A selectively promoted authoritative passage with one semantic severity and unchanged source meaning.
- **Verification Finding**: A route, source, or asset contract violation with enough context to block publication and identify the failed relationship.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One hundred percent of published fenced samples render as cohesive panels with preserved whitespace, accessible copy controls, useful syntax distinction where declared, and zero page-level horizontal overflow at 360 and 1280 CSS pixels.
- **SC-002**: Representative `info`, `warn`, and `error` notices are generated from authoritative references, while zero ordinary paragraphs are incorrectly promoted in the tested fixture set.
- **SC-003**: The documentation root label appears exactly once in desktop and mobile navigation on the index and every nested documentation route.
- **SC-004**: At 1280 by 900 CSS pixels, the documentation index exposes the title, description, introductory content, and start of the next meaningful element in its first viewport.
- **SC-005**: Light and dark documentation pages at 360 and 1280 CSS pixels report zero WCAG 2.1 AA violations and zero page-level horizontal overflow.
- **SC-006**: Every active, current, and focus state uses an official ShruggieTech color role plus a detectable non-color cue, and the sidebar identity includes recognizable shipped mark geometry.
- **SC-007**: One hundred percent of emitted public pages contain valid route-appropriate structured data whose canonical identifiers match the page and do not duplicate or contradict the authoritative organization identity.
- **SC-008**: One hundred percent of public routes use route-relevant social-preview titles, descriptions, alternative text, and working images with the declared dimensions and media type.
- **SC-009**: Every sitemap entry exactly matches the corresponding canonical and Open Graph URL and maps directly to an exported page with zero redirect requirement.
- **SC-010**: Corruption tests reject one hundred percent of representative duplicate-navigation, broken-code-panel, invalid-notice, inaccessible-state, malformed-structured-data, generic-preview, broken-image, and route-mismatch fixtures.
- **SC-011**: Every production kit completes with zero verification problems and zero glyph failures, and the complete repository CI-parity validation passes.
- **SC-012**: All changed text passes UTF-8 without BOM, LF, Markdown, sensitive-data, and mojibake checks with zero findings.

## Assumptions

- The repository's existing documentation application, static export, source preparation, icon suite, local fonts, and generated production inventory remain the architecture of record.
- The issue evidence measured on 2026-09-05 remains representative until contradicted by current local or emitted-site inspection.
- The primary company site remains authoritative for organization identity; the brand subdomain describes its own collection and pages without copying unsupported company facts.
- Shipped ShruggieTech full and reduced marks are sufficient for a compact sidebar treatment and route-specific preview composition without changing geometry.
- Route-specific previews may share a branded layout and background as long as their visible text and metadata accurately distinguish the page.
- Static export trailing-slash behavior remains required by the deployment target.
- S009 does not require authentication, personal data, tenancy, or state mutation; security coverage therefore concentrates on safe serialization, local deterministic assets, path normalization, and prevention of markup or URL injection.
- The user's explicit instruction to push and publish the pull request overrides the autopilot skill's normal pre-push halt for this slice; merge remains exclusively reserved for the owner.
