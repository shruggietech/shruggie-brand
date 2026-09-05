# Feature Specification: Brand Platform Refresh

**Feature Branch**: `codex/006-brand-platform-refresh`

**Created**: 2026-09-05

**Status**: Approved for planning

**Input**: Deliver GitHub issues #100, #101, #102, and #103 as one coherent public-brand-platform slice: reframe the homepage as ShruggieTech's brand-building portfolio, complete metadata and icon discovery, replace the documentation experience with the proven sister-project pattern, remove the synthetic example brand, publish an official pull request, process every authorized Codex review, and stop for the owner merge ritual.

## Clarifications

### Session 2026-09-05

- Q: What exact homepage headline, subhead, and action labels should S006 implement? -> A: Headline "We build comprehensive brands"; subhead "We shape distinct identities with a repeatable process, then ship the standards, assets, and tools that keep them coherent."; primary action "Explore the portfolio"; secondary action "Download the skill"; documentation link "See how we build brands."

## User Scenarios & Testing

### User Story 1 - Understand ShruggieTech's brand-building work (Priority: P1)

As a prospective client or collaborator, I can immediately understand that ShruggieTech builds strong brands through a disciplined process, inspect the published portfolio, and reach the process documentation or skill download without confusing project labels or stale counts.

**Why this priority**: The current homepage misnames the property, uses count-dependent and internally focused language, hides the practical skill entry point, and visually diverges from the company site.

**Independent Test**: Open the homepage on mobile and desktop, identify the company, service, portfolio, process, and skill-download paths without prior context, then add one publishable production brand and confirm the next build includes it without editing page source or a fixed count.

**Acceptance Scenarios**:

1. **Given** a first-time visitor, **When** the homepage loads, **Then** the approved headline and supporting copy identify ShruggieTech as a systematic brand builder without using a fixed brand count or the word "canon" as marketing language.
2. **Given** a visitor seeking examples, **When** they inspect Identity Spectrum, **Then** every publishable production brand appears in a responsive card with a square app-icon-style mark, a useful summary, and a deliberate destination.
3. **Given** a team member seeking the operating method, **When** they inspect the first screen and nearby content, **Then** the skill download and documentation paths are immediately discoverable and clearly named.
4. **Given** any public page, **When** the shared header and footer render, **Then** they present this property as ShruggieTech, use canonical company artwork, provide useful destinations, and expose neither "A ShruggieTech project" nor skill or canon version numbers.

---

### User Story 2 - Read and navigate useful brand documentation (Priority: P1)

As a designer, developer, or operator, I can search and navigate the brand-system documentation through a responsive ShruggieTech experience whose tables, code, headings, and links render correctly.

**Why this priority**: The present documentation is a flat index, several linked pages expose unrendered Markdown tables, and internal terminology weakens the public explanation.

**Independent Test**: Navigate from the documentation index through every published document using keyboard and mobile layouts, search for a known term, inspect every known table-bearing page, and confirm all authoritative content remains available and semantically rendered.

**Acceptance Scenarios**:

1. **Given** a reader on `/docs`, **When** they browse or search, **Then** they can locate every published source document through a consistent navigation hierarchy.
2. **Given** a table-bearing source document, **When** its public page renders, **Then** the table is semantic and readable rather than exposed as pipe-delimited source text.
3. **Given** a reader using a keyboard or narrow viewport, **When** they use navigation, search, headings, code blocks, tables, and previous or next controls, **Then** all content remains operable, visible, and understandable.
4. **Given** public-facing prose, **When** documentation is generated, **Then** "canon" is replaced with clearer contextual language except where a technical compatibility identifier must be named and explained.

---

### User Story 3 - Discover and share every public route correctly (Priority: P1)

As a visitor arriving from search, a browser bookmark, or a social share, I receive an accurate page title, description, canonical address, preview image, and recognizable ShruggieTech icon for the route I opened.

**Why this priority**: The live property lacks a favicon, canonical addresses, social preview metadata, a manifest, and route-specific titles despite representing a company that offers branding and search services.

**Independent Test**: Inspect the emitted static HTML and discovery files for the homepage, documentation index, representative documentation page, and representative brand page, then validate absolute URLs, route-specific text, preview images, icons, robots policy, and complete sitemap coverage.

**Acceptance Scenarios**:

1. **Given** any indexable public route, **When** a crawler or social client reads it, **Then** it receives a route-appropriate title and description, absolute canonical address, and complete Open Graph and Twitter preview data.
2. **Given** a browser or supported device surface, **When** it requests site icons or the application manifest, **Then** it receives canonical ShruggieTech artwork in a valid declared format.
3. **Given** the published route inventory, **When** discovery files are generated, **Then** the sitemap contains every public brand and documentation route exactly once while robots policy excludes non-public or generated-internal surfaces.

---

### User Story 4 - Keep synthetic test material out of the public brand catalog (Priority: P1)

As the repository owner, I can build and validate the complete system without maintaining or publishing a synthetic fixture as though it were real work.

**Why this priority**: The synthetic fixture currently affects expected counts, build paths, release paths, documentation, and homepage content, creating public confusion and unnecessary maintenance.

**Independent Test**: Search the current tree and a clean full build for the retired synthetic slug, inspect registries, routes, downloads, and archives, then run the complete regression suite using only temporary test-generated data for synthetic coverage.

**Acceptance Scenarios**:

1. **Given** the current repository tree, **When** fixture cleanup completes, **Then** the retired fixture directory and every active reference to its slug are absent.
2. **Given** a clean full build, **When** registries, routes, downloads, archives, and sitemap entries are inspected, **Then** no synthetic public brand or worked-example section exists.
3. **Given** the regression suite, **When** synthetic input is required, **Then** temporary test-only data provides the coverage and cannot enter public or release output.

---

### User Story 5 - Deliver a review-complete pull request (Priority: P2)

As the repository owner, I receive one official S006 pull request whose issue traceability, checks, and authorized Codex reviews are complete, while merge authority remains with me.

**Why this priority**: The implementation is not ready for owner review until every automated check and review thread has an evidence-backed disposition and the review loop is bounded.

**Independent Test**: Inspect the pull request, linked issues, check runs, review threads, responses, correction commits, and review-request comments, then confirm all required checks are green, every review is resolved, no more than one explicit `@Codex` request occurred, and the pull request remains open.

**Acceptance Scenarios**:

1. **Given** the completed local slice, **When** it is pushed and the official pull request opens, **Then** its description links #100, #101, #102, and #103 and reports accessibility, identity, documentation, and validation impact.
2. **Given** an actionable Codex review finding, **When** it is evaluated, **Then** the necessary correction and tests are pushed, the comment receives a substantive response, and the thread is resolved only after evidence exists.
3. **Given** the automatic review is satisfied, **When** a second review is useful, **Then** exactly one explicit `@Codex` request may be posted and no third round is triggered.
4. **Given** all authorized reviews and checks are satisfied, **When** readiness is reported, **Then** the pull request remains open for the owner merge ritual.

### Edge Cases

- A brand record may be malformed, incomplete, or marked non-production. It must fail preparation or remain unpublished without causing a false portfolio count.
- A brand app icon may be unavailable. The build must fail with a clear source error rather than substituting redrawn geometry or an unrelated decorative swatch.
- A documentation title or body may contain "canon" as a technical file or compatibility identifier. The public explanation may retain it only when renaming would break an interface and the term is explained in plain language.
- A documentation source may contain tables, raw HTML, code fences, unusual Unicode, or internal links. Conversion must preserve meaning, escaping, and navigation.
- A crawler may request a trailing-slash or alternate route form. Canonical metadata must identify one public address without duplicate sitemap entries.
- A social image or icon source may be missing or malformed. The build must fail before publication rather than emit broken or relative metadata.
- The temporary regression fixture may leave files after a failed test. Test setup and cleanup must isolate it from production discovery and release packaging.
- A review bot may provide only a positive reaction, arrive late, duplicate a finding, or fail to respond. The review ledger must distinguish satisfied, duplicate, unavailable, and actionable outcomes without requesting a third round.

## Requirements

### Functional Requirements

- **FR-001**: S006 MUST deliver the complete acceptance scope of GitHub issues #100, #101, #102, and #103 in one coherent slice.
- **FR-002**: The public property MUST use an approved company-aligned name and MUST NOT identify itself as "Shruggie Brand" or "A ShruggieTech project."
- **FR-003**: The homepage MUST use the human-approved headline "We build comprehensive brands," the subhead "We shape distinct identities with a repeatable process, then ship the standards, assets, and tools that keep them coherent," the primary action "Explore the portfolio," the secondary action "Download the skill," and the documentation link "See how we build brands."
- **FR-004**: Homepage marketing copy MUST NOT use a fixed count of brands or the word "canon."
- **FR-005**: The homepage MUST state that ShruggieTech builds good brands, uses a systematic process, presents completed work, and makes its underlying method available through documentation and a downloadable skill.
- **FR-006**: The skill download MUST be discoverable from the first screen or its immediately adjacent content and MUST be labeled by the user benefit or action.
- **FR-007**: The shared header MUST display an unmodified canonical ShruggieTech mark suitable for the available space and provide accessible primary navigation.
- **FR-008**: The public visual system MUST use a restrained hierarchy of ShruggieTech-aligned dark surfaces and accents rather than one undifferentiated black background.
- **FR-009**: The footer MUST provide useful company, portfolio, documentation, skill, source, and appropriate legal destinations and MUST NOT expose skill or canon version numbers.
- **FR-010**: Identity Spectrum MUST remain the portfolio concept and MUST render one card for every publishable production brand discovered from verified generated records.
- **FR-011**: Each portfolio card MUST use a square app-icon-style canonical brand image, name, useful summary, and deliberate accessible destination.
- **FR-012**: Adding a valid publishable production brand MUST make it appear in the next normal site build without editing homepage source, a fixed expected-brand list, or a count-specific statement.
- **FR-013**: Portfolio cards MUST reflow without clipping, overlap, horizontal page scrolling, or undersized interactive targets across narrow mobile, tablet, desktop, and growing-card-count scenarios.
- **FR-014**: The documentation experience MUST provide responsive navigation, current-page context, search, a table of contents where useful, previous or next navigation, theme handling, and keyboard-accessible controls.
- **FR-015**: Documentation pages MUST consume the authoritative skill reference sources without creating a separately maintained content tree.
- **FR-016**: Documentation conversion MUST preserve headings, warnings, links, lists, code, tables, and substantive prose.
- **FR-017**: The eight known table-bearing documents named in issue #102 MUST emit semantic tables and MUST NOT expose raw pipe-delimited table source.
- **FR-018**: Public documentation navigation, headings, and explanatory prose MUST replace "canon" with plain terms such as standards, system, method, or inheritance rules according to context.
- **FR-019**: Every indexable public route MUST emit a route-appropriate title, description, absolute canonical address, Open Graph data, Twitter card data, and a valid absolute social-preview image with dimensions, type, and alternative text.
- **FR-020**: The site MUST publish canonical ShruggieTech favicon assets, an Apple touch icon, a valid application manifest, and a supported theme color without redrawing or normalizing logo geometry.
- **FR-021**: The site MUST publish a robots policy and a sitemap derived from the actual public route inventory, with every public brand and documentation route exactly once and no synthetic, internal, or duplicate route.
- **FR-022**: Metadata, navigation, portfolio records, and discovery files MUST be derived from shared authoritative data so additions cannot silently diverge across surfaces.
- **FR-023**: The retired fixture and every active current-tree reference to its slug MUST be removed from source, documentation, specifications, tests, workflows, preparation, release configuration, and public content.
- **FR-024**: Synthetic regression coverage MUST use temporary test-only data that is never eligible for production discovery, public routing, registry inclusion, download, or release packaging.
- **FR-025**: Production discovery MUST NOT rely on a fixed count or manually enumerated expected-brand set.
- **FR-026**: The implementation MUST preserve all shipped logo geometry and MUST consume generated verified kit outputs for public brand values and assets.
- **FR-027**: Every public foreground and interactive state MUST meet WCAG 2.1 AA at rendered size, with visible keyboard focus, usable touch targets, reduced-motion behavior, and semantic landmarks.
- **FR-028**: The static site MUST remain network-independent at runtime, use local fonts and assets, and remain compatible with the repository's static hosting path and trailing-slash contract.
- **FR-029**: Automated validation MUST inspect emitted static HTML, metadata, discovery files, responsive portfolio behavior, semantic documentation tables, accessibility, source-boundary compliance, and absence of the removed fixture.
- **FR-030**: All committed text MUST use UTF-8 without BOM and LF line endings, avoid mojibake, and keep Markdown prose paragraphs on one physical line unless syntax requires a break.
- **FR-031**: S006 MUST update the changelog's Unreleased section with the delivered public experience and any architecture-affecting decisions.
- **FR-032**: The official pull request MUST link #100, #101, #102, and #103, report verification evidence and impact, and remain unmerged for the owner.
- **FR-033**: Every actionable Codex review comment MUST receive a substantive response, warranted correction, regression coverage, and resolution after the correction is available.
- **FR-034**: S006 MAY request exactly one explicit second Codex review using `@Codex` after the automatic round is complete and MUST NOT request or trigger a third review round.
- **FR-035**: All required continuous-integration checks and every authorized review MUST be satisfied before the owner is asked to perform the final review and merge ritual.

### Key Entities

- **Published Brand Record**: Verified generated data for one production brand, including stable slug, display name, summary, canonical mark or app icon, public destination, and publication eligibility.
- **Documentation Record**: One authoritative skill reference exposed publicly with stable slug, title, description, navigation order, headings, table of contents, and source path.
- **Route Metadata Record**: The title, description, canonical address, social preview, indexing state, and route type for one public route.
- **Site Identity Asset**: An unmodified generated ShruggieTech logo, favicon, touch icon, or preview image with declared role and dimensions.
- **Temporary Regression Brand**: Test-generated synthetic input isolated from production discovery and removed after its test lifecycle.
- **Review Round**: One authorized Codex arrival signal, its findings, responses, correction evidence, thread state, and optional explicit request URL.

## Success Criteria

### Measurable Outcomes

- **SC-001**: First-screen review identifies ShruggieTech, brand-building value, portfolio access, process access, and skill download on both a 360-pixel-wide viewport and a desktop viewport, with zero fixed brand counts and zero public marketing uses of "canon."
- **SC-002**: Five of five current publishable production brands appear exactly once with canonical square icon artwork, and one additional valid test brand appears automatically in an isolated build without editing page source or an expected-brand list.
- **SC-003**: Portfolio layouts show zero clipping, overlap, horizontal page overflow, or interactive targets smaller than 44 by 44 CSS pixels at the declared mobile, tablet, desktop, and expanded-card-count test widths.
- **SC-004**: All published documentation sources are discoverable through navigation and search, and all eight known affected documents emit semantic tables with zero raw pipe-delimited table blocks.
- **SC-005**: Homepage, documentation index, every documentation page, and every production brand route emit one absolute canonical address plus complete route-appropriate title, description, Open Graph, and Twitter metadata.
- **SC-006**: Emitted output contains a valid favicon set, Apple touch icon, manifest, robots policy, and sitemap whose route set matches the public inventory with zero duplicates, fixtures, or internal paths.
- **SC-007**: Current-tree and clean-build searches find zero active retired-fixture references or outputs, while temporary regression coverage completes without publishing or packaging its synthetic input.
- **SC-008**: Automated accessibility checks report zero WCAG 2.1 AA violations on the homepage, documentation index, representative table-bearing documentation, and representative brand page at mobile and desktop widths.
- **SC-009**: Full repository validation reports five of five production kits with zero verification problems and zero glyph failures, all focused tests pass, the static export succeeds, and repository hygiene checks report zero committed generated artifacts, BOMs, CRLF text, or mojibake.
- **SC-010**: The official S006 pull request has zero unresolved actionable review comments, no more than two authorized Codex review rounds, all required checks green, and remains open for the owner merge ritual.

## Assumptions

- The five current production brands are ShruggieTech, Fragcap, Go Schedule, Glitchpad, and Covarity.
- The repository's generated kit output remains the source boundary for brand values and public identity assets.
- A test-generated temporary brand may replace fixture-dependent regression coverage only when it cannot enter normal production discovery or release output.
- The sister Fragcap documentation experience is the functional and structural reference, while all visual identity, copy, and navigation are adapted to ShruggieTech.
- The public site remains a statically exported Next.js application hosted at `https://brand.shruggie.tech/`.
- GitHub issues #104 through #106 remain outside S006 and must not be closed by this slice.
- The owner retains sole merge authority after S006 becomes review-complete.
