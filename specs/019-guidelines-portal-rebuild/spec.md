# Feature Specification: Hosted Guidelines Portal Rebuild

**Feature Branch**: `codex/019-guidelines-portal-rebuild`

**Created**: 2026-09-07

**Status**: In Review

**Input**: Resolve GitHub issues #157, #158, #159, #160, and #161 as one corrective hosted-guidelines slice.

## User Scenarios & Testing

### User Story 1 - Move through focused brand topics (Priority: P1)

As a visitor, I can move among focused guideline topics while retaining the current brand and section context, without returning to the top of a single oversized document.

**Why this priority**: The single-page hosted experience adopted in S017 is the root usability failure shared by the navigation, color, asset, instruction, and footer regressions.

**Independent Test**: Open every topic for each production brand at supported desktop and mobile widths, traverse the persistent or disclosed hierarchy with keyboard and touch, follow direct topic and fragment URLs, and repeat the core traversal with scripting disabled.

**Acceptance Scenarios**:

1. **Given** a desktop guideline topic, **When** the visitor scrolls and changes topics, **Then** persistent navigation exposes the full topic hierarchy and identifies the current topic and active section.
2. **Given** a narrow viewport, **When** the visitor opens the navigation control, **Then** the equivalent hierarchy is operable and dismissible by keyboard and touch with accurate expanded state.
3. **Given** a direct topic or fragment URL, **When** it loads at 200 percent zoom, **Then** the intended heading remains visible and no sticky region obscures content or focus.
4. **Given** scripting is unavailable, **When** the visitor traverses topic links and downloads, **Then** all core content and files remain reachable.

---

### User Story 2 - Scan and copy trustworthy color values (Priority: P1)

As a designer or developer, I can scan compact color rows, copy the canonical HEX value immediately, and reveal secondary representations without destabilizing neighboring content.

**Why this priority**: Color is a frequent reference task, and the current expanding card grid turns routine lookup into a visually unstable interaction.

**Independent Test**: Review both palettes for all five brands, including the longest alias sets, and open several detail controls at 360 and 1280 pixels and 200 percent zoom while measuring unrelated row movement, focus, overflow, and copy announcements.

**Acceptance Scenarios**:

1. **Given** a collapsed color entry, **When** it is viewed, **Then** its swatch, human-readable role, canonical token, HEX value, and copy action are immediately available.
2. **Given** a color entry with aliases and multiple representations, **When** details are revealed, **Then** RGB, HSL, OKLCH, Lab D50, aliases, and profile-dependent print guidance appear without resizing unrelated entries.
3. **Given** a copy action succeeds or fails, **When** it is invoked, **Then** the result is announced honestly while selectable fallback text remains available.

---

### User Story 3 - Find the right asset by purpose (Priority: P1)

As a visitor, I can locate the correct logo, platform asset, or integration resource by purpose without interpreting storage paths or scanning a wall of repeated files.

**Why this priority**: The current complete catalog exposes manifest storage structure instead of providing a usable asset library.

**Independent Test**: For every production brand, complete representative logo, web, Android, iOS, macOS, Windows, and integration-resource tasks using collections, filters, search, and detail inventories, then prove exact manifest coverage and no duplicate or dead downloads.

**Acceptance Scenarios**:

1. **Given** a large asset inventory, **When** the visitor browses it, **Then** assets are grouped by task-oriented family and every genuinely distinct visual design has one bounded representative preview.
2. **Given** size copies, aliases, and multiple delivery paths, **When** the visitor opens the representative asset detail, **Then** every authoritative delivery, format, dimension, destination, appearance, alias, and useful hash is available without inflating the summary tile.
3. **Given** a nonvisual XML, JSON, Markdown, or container resource, **When** it appears in the library, **Then** it uses a meaningful document or code treatment and never an empty image well.
4. **Given** a platform instruction document, **When** the visitor opens its topic, **Then** headings, lists, links, and code are rendered in context and the raw source download is secondary.
5. **Given** search or filters are enhanced with scripting, **When** scripting is unavailable, **Then** complete task-oriented collections remain browsable.

---

### User Story 4 - Read balanced landing pages and footer utilities (Priority: P1)

As a visitor, I can read every production brand name and use clearly separated guideline footer controls without clipping, collision, concatenation, or horizontal scrolling.

**Why this priority**: The worst-case brand name currently collides with its logo panel, and the footer controls visually merge at the end of already difficult pages.

**Independent Test**: Measure all production brand headings and guideline footer controls at 360, 768, 1024, and 1280 pixels and at 200 percent zoom, including `ShruggieTech` as the longest current name.

**Acceptance Scenarios**:

1. **Given** any production brand landing page, **When** it is viewed at a supported width or 200 percent zoom, **Then** the full brand name remains visible within its text column and does not collide with the logo, descriptor, or actions.
2. **Given** the end of a guideline topic, **When** the visitor reaches its utilities, **Then** `Back to top` and `All brands` are distinct, well-spaced controls with visible focus and adequate bottom breathing room.
3. **Given** the host exit control, **When** it rests or interacts, **Then** it remains neutral white and does not adopt a brand or ShruggieTech accent.

### Edge Cases

- Long brand names, canonical tokens, semantic aliases, filenames, storage paths, and instruction headings must wrap without clipping or horizontal overflow.
- A brand with no entries for an optional asset family must omit that family or show a meaningful local empty state without hiding other collections.
- A representative asset whose preview cannot be decoded must retain its human-readable metadata and direct downloads without a blank visual frame.
- Search text or filters that produce no matches must announce zero results and provide a direct reset while the no-script collection remains complete.
- Multiple open color details must not move unrelated entries or lose keyboard focus.
- Sticky navigation must account for safe areas and fragment offsets at every supported width.
- A missing or malformed manifest delivery must fail publication rather than silently disappear from the hosted inventory.
- Content with Markdown links, nested lists, inline code, or fenced code must remain semantically intact when published into a platform topic.

## Requirements

### Functional Requirements

- **FR-001**: Hosted guidelines MUST use separate meaningful topic URLs for overview and foundations, voice and messaging, logo usage, color, typography, components and examples, asset downloads, and platform integration wherever corresponding authoritative content exists.
- **FR-002**: S019 MUST explicitly supersede S017's decision that one self-contained generated guide is the primary hosted experience, while retaining a concise portable offline guide as a generated artifact.
- **FR-003**: The site MUST own hosted navigation, topic composition, and shell chrome while consuming brand facts, rules, colors, instructions, and asset inventory from verified generated-kit output.
- **FR-004**: Hosted brand topics MUST remain visually neutral to the host, keep the current brand visually primary, and MUST NOT inject ShruggieTech marketing identity or calls to action.
- **FR-005**: Desktop topics MUST provide persistent hierarchical navigation with visible current-topic and active-section states; mobile topics MUST provide an accessible disclosure or drawer exposing the same hierarchy.
- **FR-006**: Navigation MUST preserve meaningful direct URLs, visible fragment targets, keyboard and touch operation, accurate expanded state, reduced-motion behavior, and complete no-script topic traversal.
- **FR-007**: Sticky regions MUST remain shallow and MUST NOT cover headings, focused elements, content, or safe-area controls at supported widths or 200 percent zoom.
- **FR-008**: The topic footer MUST render `Back to top` and `All brands` as separate controls with clear spacing, visible focus, at least 44-pixel discrete targets, generous bottom padding, and a neutral-white host exit.
- **FR-009**: Each resting color entry MUST expose a small swatch, human-readable role, canonical token, canonical HEX value, selectable fallback text, and an accessible copy action.
- **FR-010**: Secondary color detail MUST expose RGB, HSL, OKLCH, Lab D50, semantic aliases, and profile-dependent print guidance in compact readable text derived from the same canonical value.
- **FR-011**: Revealing or hiding color details MUST NOT resize or reposition unrelated color entries, produce horizontal overflow, or lose focus.
- **FR-012**: Copy actions MUST retain accessible names, visible focus, 44-pixel hit targets, and honest success or failure announcements without making clipboard support the only way to retrieve a value.
- **FR-013**: The asset library MUST group deliveries first by user purpose and meaningful family, including logos and lockups, marks, social or composite artwork, web icons, Android, iOS, macOS, Windows, and integration resources where present.
- **FR-014**: Each genuinely distinct visual design MUST have exactly one representative summary with bounded preview geometry, a human-readable title, a short usage summary, and a concise format and variant summary.
- **FR-015**: Size-only copies, aliases, hashes, destinations, measured sizes, appearances, formats, and complete paths MUST be available in an accessible detail view without producing duplicate showcase summaries.
- **FR-016**: Nonvisual XML, JSON, Markdown, README, manifest, and container resources MUST use meaningful document or code presentation and MUST NOT use empty visual preview wells.
- **FR-017**: Markdown integration instructions MUST be rendered in their relevant platform or topic context with headings, links, lists, and code preserved; raw-source download MAY remain only as a secondary action.
- **FR-018**: The asset library MUST provide keyboard-accessible search and useful filters for family, platform, appearance or surface, role, and format when applicable, with announced result counts, resettable empty states, and deep-linkable query state where enhancement is active.
- **FR-019**: Search and filtering MUST progressively enhance complete server-rendered collections and MUST NOT make any authoritative delivery unreachable without scripting.
- **FR-020**: Publication MUST preserve exact manifest-derived coverage, reject missing or duplicate deliveries and dead links, and MUST NOT invent files or expose raw storage paths as primary labels.
- **FR-021**: Individual brand landing headings MUST use a page-specific responsive size and width contract that keeps every production brand name fully legible without clipping, collision, or horizontal scrolling at 360, 768, 1024, and 1280 pixels and 200 percent zoom.
- **FR-022**: When a two-column hero cannot support the brand name, the layout MUST use balanced wrapping or transition to one column while keeping the logo panel and primary actions visible.
- **FR-023**: Automated browser coverage MUST measure navigation persistence, active states, fragment visibility, color layout stability, copy outcomes, representative preview bounds, nonvisual treatments, search and filter results, empty states, heading containment, footer separation, overflow, and accessibility.
- **FR-024**: Task-based review MUST prove that visitors can locate a logo, copy a HEX value, find platform guidance, download a required rendition, and move between topics for all five production brands.
- **FR-025**: All affected routes MUST pass WCAG 2.1 AA, semantic HTML, keyboard, touch, reduced-motion, 360-pixel layout, 200 percent zoom, encoding, and mojibake gates.
- **FR-026**: All production kits MUST retain zero `verify.py` problems and zero `validate_glyph.py` failures after the publishing change.
- **FR-027**: Identity names, shipped logo geometry and path data, canonical palette values, generated kit contents, and files under `dist/` MUST remain unchanged by committed source edits.

### Key Entities

- **Guideline Topic**: One meaningful hosted page with a stable URL, title, description, ordered content blocks, topic hierarchy position, and optional heading outline.
- **Guide Navigation Tree**: The ordered topic hierarchy for one brand, including current-topic and active-section state and mobile disclosure behavior.
- **Color Reference Entry**: One canonical color value with role, token, swatch, HEX, derived representations, aliases, copy label, and print guidance.
- **Asset Family**: A task-oriented collection of related representative designs and nonvisual resources, independent of physical storage hierarchy.
- **Representative Asset**: One distinct visual design with a bounded preview, usage summary, formats, appearances, and associated deliveries.
- **Asset Delivery**: One authoritative manifest path with role, platform, format, dimensions, destination, appearance, alias relationships, and optional hash.
- **Integration Instruction**: Authoritative Markdown guidance associated with a platform or task and accompanied by an optional raw-source download.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every production brand exposes all applicable guideline topics through direct URLs, with 100 percent of core topic links and downloads operable without scripting.
- **SC-002**: Task review completes all five target tasks for every production brand without requiring a visitor to interpret a raw storage path.
- **SC-003**: Every distinct visual asset design has exactly one bounded summary, while 100 percent of authoritative deliveries remain accessible in details with zero duplicate or dead downloads.
- **SC-004**: Opening and closing any tested combination of color details produces zero movement in unrelated entries and zero clipped or horizontally overflowing values.
- **SC-005**: Every production brand name remains within its heading column and viewport at 360, 768, 1024, and 1280 pixels and 200 percent zoom.
- **SC-006**: Browser verification reports zero WCAG 2.1 AA violations, hidden fragment targets, undersized discrete controls, unannounced search or copy outcomes, or concatenated footer utilities across the required matrix.
- **SC-007**: All five production kits report zero verification problems and zero glyph failures, and the full repository validation remains green.

## Assumptions

- The newly filed issue cluster is the complete authority for S019 and is sufficiently specific to proceed without operator clarification.
- The existing documentation framework is the preferred navigation foundation, but hosted brand topics require their own brand-neutral shell rather than the ShruggieTech documentation marketing shell.
- The authoritative generated manifest and brand records already contain the information needed for the initial portal model; adding derived presentation metadata is permitted when it does not restate or alter brand values.
- Search and filters may use client-side progressive enhancement because every collection and direct download remains available in server-rendered markup.
- S019 closes #157 through #161 together. ESO Weave provenance and kit work in #153 remains out of scope and moves to the next slice.
