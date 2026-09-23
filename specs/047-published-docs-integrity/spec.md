# Feature Specification: Published Documentation and Guideline Integrity

**Feature Branch**: `codex/047-published-docs-integrity`

**Created**: 2026-09-22

**Status**: Draft

**Input**: Deliver the BrandBuilder-owned documentation and guideline corrections in issues #236, #237, and #202 as one verified work slice. Keep in-flight brand identity work and downstream consumer adoption outside this slice.

**Issues**: [#236](https://github.com/shruggietech/shruggie-brand/issues/236), [#237](https://github.com/shruggietech/shruggie-brand/issues/237), [#202](https://github.com/shruggietech/shruggie-brand/issues/202)

## Clarifications

### Session 2026-09-22

- Q: Which documents are subject to the public-language audit? → A: Publication-bound manual, hosted guide, and delivered-kit instructions, including their authoritative inputs; internal specifications, issue history, changelogs, and approval ledgers remain outside the reader-facing rule.
- Q: How should the audit handle technical compatibility words and legitimate workflow instructions? → A: Use narrow, documented context exceptions rather than banning every occurrence of `may`, a legacy alias, or `Spec Kit` mechanically.

## User Scenarios & Testing

### User Story 1 - Follow present-version instructions (Priority: P1)

As a reader of the public manual or a delivered brand kit, I receive direct instructions for the current product rather than internal planning codes, obsolete history, or vague claims.

**Why this priority**: Published operating guidance must be actionable and accurate across the manual, hosted guides, and downloadable kits.

**Independent Test**: Audit every published manual page and every production kit's reader-facing guidance, then follow representative installation, compatibility, recovery, and asset-use instructions without consulting planning history.

**Acceptance Scenarios**:

1. **Given** a published manual or guide, **when** a reader looks for a current task, **then** the page states what to do and how to verify it without exposing work-slice codes or obsolete implementation history.
2. **Given** an active compatibility term such as `historical-baseline` or `legacy-constructed`, **when** it appears in guidance, **then** its current accepted meaning remains explicit.
3. **Given** a production kit, **when** its instructional files are inspected, **then** they retain all identity, accessibility, provenance, licensing, recovery, and safety constraints while meeting the same editorial rules.

---

### User Story 2 - Understand every integration asset card (Priority: P1)

As a reader of portable guidelines, I can distinguish visual icon artwork from its preview surface and read labels or nonvisual-resource messages without guessing whether a card is empty.

**Why this priority**: The current I Heart PR Tours integration cards include nearly invisible text and ambiguous icon previews, failing the accessibility floor.

**Independent Test**: Inspect generated portable guides for visual and nonvisual delivery fixtures on light and dark surfaces at normal, narrow, and enlarged viewing sizes, measuring text and meaningful graphical contrast.

**Acceptance Scenarios**:

1. **Given** black, white, transparent, or full-color artwork, **when** its card renders, **then** the artwork is visibly distinguishable against an appropriate declared surface without changing the asset bytes.
2. **Given** XML, metadata, declaration, or container delivery, **when** its card renders, **then** it is identified as a nonvisual resource with readable text rather than an empty-looking visual preview.
3. **Given** a dark preview well, **when** it contains a label or fallback, **then** the text meets WCAG 2.1 AA on that exact well.

---

### User Story 3 - Move between documentation pages (Priority: P1)

As a reader using bottom previous/next navigation, I arrive at the new page's beginning with a sensible focus context instead of retaining the prior page's deep scroll offset.

**Why this priority**: The published site can show the destination heading thousands of pixels above the viewport after an otherwise correct navigation.

**Independent Test**: From a scrolled source page, activate representative previous and next links by pointer and keyboard at desktop and mobile widths, then check the destination heading, scroll position, focus, and browser history.

**Acceptance Scenarios**:

1. **Given** a bottom link without a fragment, **when** it opens another page, **then** that page's heading is visible at the beginning of the readable viewport and focus enters the new page.
2. **Given** a link with an explicit heading fragment, **when** it opens, **then** the requested heading remains the destination.
3. **Given** back/forward navigation or a direct page load, **when** it completes, **then** history and expected initial position remain coherent.

### Edge Cases

- A dark or light icon may become invisible on the surface suggested by its file type; appearance, not extension alone, governs preview choice.
- A nonvisual platform delivery may be valid and must not be presented as broken merely because it lacks an image preview.
- A reader may disable motion or scripts; documentation links must remain meaningful and ordinary page navigation must not inherit animated scrolling.
- A navigation target may include a fragment; top-reset behavior must not erase that explicit destination.
- A technical permission word such as `may` or a live compatibility alias must not be removed by a mechanical prose audit.
- In-flight brand updates may change source guidance before S047 merges; integrate their merged source without overwriting approved identity or asset files.

## Requirements

### Functional Requirements

- **FR-001**: Published manual pages, hosted guideline instructions, and documentation delivered in every production kit MUST describe present-version behavior and explicitly labeled future considerations, not superseded state or internal work history.
- **FR-002**: Reader-facing instructional output MUST contain zero internal work-slice identifiers. `Spec Kit` may appear only where a reader must actually invoke that workflow for the documented task.
- **FR-003**: Editorial changes MUST retain all currently valid commands, compatibility aliases, identity restrictions, accessibility requirements, provenance and licensing rules, and recovery instructions.
- **FR-004**: A repeatable audit MUST detect work-slice leakage, unjustified planning references, historical narrative, and defined vague phrasing in authoritative sources and prepared public or kit output; any exception MUST be narrow and documented.
- **FR-005**: Every visual integration-card icon MUST have a preview surface that makes its meaningful artwork discernible without recoloring, inverting, redrawing, cropping, or modifying the delivered file.
- **FR-006**: Preview text MUST meet WCAG 2.1 AA text contrast on its actual local surface, and meaningful icon artwork MUST meet applicable non-text contrast.
- **FR-007**: Nonvisual integration deliveries MUST use a readable nonvisual-resource treatment rather than an apparently empty icon well.
- **FR-008**: The preview correction MUST cover black, white, transparent, full-color, metadata-only, and container deliveries across affected production guides, including I Heart PR Tours.
- **FR-009**: Cross-page bottom documentation pagination without a fragment MUST place the destination at its beginning and move focus to an appropriate new-page context after client navigation.
- **FR-010**: Pagination MUST preserve explicit fragments, governed neighbor order and URLs, direct navigation, browser back/forward history, accessible link semantics, static publication, and reduced-motion behavior.
- **FR-011**: Rendered regression checks MUST exercise actual pointer and keyboard pagination from a scrolled source page at desktop and mobile widths and measure destination URL, heading visibility, position, and focus.
- **FR-012**: Changes MUST be made in authoritative source and generation logic; generated kits, site exports, release archives, and approved logo geometry MUST remain uncommitted and unchanged as source.
- **FR-013**: The complete production-kit, glyph, site, accessibility, publication, encoding, and repository-hygiene gates MUST pass before the slice is offered for merge.

### Key Entities

- **Instructional source**: A governed reader-facing manual or brand guidance input, with an intended publication destination and current task contract.
- **Integration delivery**: A visual asset or nonvisual platform resource, with appearance, source bytes, preview surface, and reader guidance.
- **Documentation transition**: A source page, destination page or fragment, activation mode, viewport, motion preference, resulting position, and focus context.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Zero work-slice codes or unjustified planning references appear in published manual pages, hosted guidelines, or production-kit instructional files.
- **SC-002**: Every production kit retains its current compatibility, identity, provenance, accessibility, licensing, and recovery instructions after the editorial rewrite.
- **SC-003**: Every audited integration-card text sample passes WCAG 2.1 AA text contrast, and every meaningful icon preview passes the applicable non-text contrast threshold on its actual well.
- **SC-004**: All tested fragment-free pagination transitions from a scrolled page show the destination heading in the first readable viewport with focus in the destination, across pointer, keyboard, desktop, mobile, and reduced-motion cases.
- **SC-005**: All production kits report zero verifier problems and zero glyph failures; the public site, accessibility, publication, and encoding checks pass with no gate waiver.

## Scope and Assumptions

- This slice covers BrandBuilder's published documentation, shared generator output, and public site navigation only. It does not modify a downstream consumer repository or ask another team to adopt a kit.
- Brand identity, logo paths, and platform asset bytes are authoritative. Preview treatment may change, but artwork does not.
- The broader light-first theme contract in #193 and the custom-expression asset schema in #194 are separate features. S047 corrects readability of existing cards without introducing those systems.
- Existing active brand updates may merge during S047. Reconcile their latest reader-facing guidance before final verification; do not overwrite unrelated work.
- This slice does not cut a new release tag. Its pull request and merged site/source changes follow the project's normal publication process.
