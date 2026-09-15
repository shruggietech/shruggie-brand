# Feature Specification: Integration Preview Visibility

**Feature Branch**: `codex/035-integration-preview-visibility`

**Created**: 2026-09-15

**Status**: Draft

**Input**: GitHub issue #202, "[I HEART PR TOURS][GUIDELINES] Restore icon and card-text visibility in integration instructions"

## Scope

**In scope**: Shared generation of portable integration asset cards, hosted visual-preview surface metadata derived by the same resolver, explicit light and dark well foregrounds, format-aware nonvisual treatments, isolated regression fixtures, generated I Heart PR Tours portable output, browser acceptance, production-kit verification, and preservation evidence.

**Out of scope**: Recoloring or redrawing assets, changing identity geometry, changing platform icon-generation rules or manifest appearance semantics, redesigning the broader guideline portal, patching `dist/` or `site/out/`, release publication, and unrelated light-theme work tracked by issue #193.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recognize every visual integration asset (Priority: P1)

A reader reviewing portable integration guidance can immediately distinguish every visual icon or mark from the preview well surrounding it, regardless of whether the artwork is transparent, black, white, or full color.

**Why this priority**: Invisible artwork prevents readers from recognizing the asset they are being instructed to install and creates an accessibility failure in the primary integration workflow.

**Independent Test**: Generate the affected portable guide and inspect every visual integration card on desktop, at a narrow viewport, and at 200 percent zoom. Each card exposes meaningful artwork with at least 3:1 non-text contrast against its selected well without altering the delivered asset.

**Acceptance Scenarios**:

1. **Given** a visual delivery whose meaningful artwork is dark, **When** its integration card is presented, **Then** the preview uses a light well on which the artwork reaches at least 3:1 contrast.
2. **Given** a visual delivery whose meaningful artwork is light, **When** its integration card is presented, **Then** the preview uses a dark well on which the artwork reaches at least 3:1 contrast.
3. **Given** transparent or full-color artwork, **When** the declared appearance does not prove a suitable well, **Then** measurable visible output determines a well that reaches the required contrast.

---

### User Story 2 - Understand nonvisual integration resources (Priority: P1)

A reader can distinguish metadata, declarations, XML files, and container deliveries from visual artwork and can read an intentional resource explanation without encountering an empty-looking preview.

**Why this priority**: Presenting nonvisual resources as failed image previews miscommunicates their purpose, while inherited black text on a near-black well makes the only explanation unavailable.

**Independent Test**: Generate cards for metadata-only, declaration, XML, and container deliveries. Every resource receives an explicit nonvisual presentation, a readable resource-kind label, and a readable fallback message rather than an image-preview claim.

**Acceptance Scenarios**:

1. **Given** a delivery with no directly previewable visual representation, **When** its integration card is presented, **Then** it is identified as a nonvisual resource using intentional visible text.
2. **Given** a nonvisual delivery associated with a dark well, **When** its label and fallback are read, **Then** both reach at least 4.5:1 contrast against the well.
3. **Given** a grouped set containing both visual and nonvisual deliveries, **When** the group is presented, **Then** the visual representative remains visible and every nonvisual delivery remains clearly identified in the delivery list.

---

### User Story 3 - Trust regenerated portable guidance (Priority: P2)

A brand maintainer can regenerate the portable guide and know that visibility is determined consistently for all affected cards without changing any approved asset payload.

**Why this priority**: The correction must survive future kit generation, apply beyond the named examples, and preserve the identity and platform artifacts that consumers download.

**Independent Test**: Compare source and generated delivery bytes before and after the generator correction, run the full production-kit validation, and exercise synthetic deliveries for each required visual and nonvisual class in isolated temporary storage.

**Acceptance Scenarios**:

1. **Given** unchanged governed brand sources, **When** the corrected guide is regenerated, **Then** every asset download retains its existing bytes, geometry, colors, proportions, transparency, and platform metadata.
2. **Given** a future delivery from a covered visual or nonvisual class, **When** the portable guide is generated, **Then** the same classification and contrast rules apply without a brand-specific card patch.
3. **Given** the generated standalone portable file, **When** it is opened directly at the required viewport and zoom settings, **Then** the same readable and distinguishable presentation is available without the hosted site shell.

### Edge Cases

- A fully transparent image contains no meaningful visible output and must not be treated as proof that either well provides graphical contrast.
- A visual asset can contain both very light and very dark content; selection must use meaningful visible pixels and choose a supported well that meets the non-text contrast floor rather than trusting a filename or unchecked default.
- An asset can have declared appearance metadata that is absent, generic, stale, or insufficient to prove contrast; measured visible output is the fallback authority.
- A group can contain a previewable visual delivery alongside XML, metadata, or container siblings; resource semantics must not displace the visual representative or disappear from the delivery inventory.
- Text inside either light or dark wells must retain its required contrast in the light-first guide, at narrow widths, and at 200 percent zoom without clipping or overlap.
- Unsupported or malformed preview input must fail clearly during generation or receive the nonvisual treatment; it must not silently produce an empty visual well.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every visual asset card in Integration instructions MUST present meaningful graphical content that is visibly distinguishable from its preview well.
- **FR-002**: Preview-well selection MUST use the delivery's declared appearance only when that declaration proves suitability; otherwise it MUST use measurable visible output from the exact delivered artwork.
- **FR-003**: Meaningful graphical content in the affected I Heart PR Tours guide MUST reach at least 3:1 contrast against the selected preview well at rendered size; the shared resolver MUST still record and choose the strongest supported well for an approved asset whose intrinsic transparency prevents either fixed well from reaching that threshold.
- **FR-004**: The preview system MUST support transparent, black, white, and full-color visual deliveries without recoloring, redrawing, inverting, normalizing, or otherwise changing their asset payload.
- **FR-005**: All surface labels, resource-kind labels, fallback messages, and other text inside preview wells MUST reach at least 4.5:1 text contrast against their well.
- **FR-006**: Nonvisual XML, metadata, declaration, and container deliveries MUST use an intentional nonvisual-resource presentation rather than an image-preview claim or empty-looking placeholder.
- **FR-007**: The nonvisual presentation MUST identify the resource as nonvisual and communicate its delivery type or purpose in readable text.
- **FR-008**: The correction MUST apply consistently to every affected integration card and MUST NOT be limited to named examples or to one brand-specific output patch.
- **FR-009**: Grouped delivery behavior MUST retain previewable visual representatives while preserving the identity and discoverability of nonvisual sibling deliveries.
- **FR-010**: Regression coverage MUST include transparent, black, white, full-color, metadata-only, and container delivery fixtures created only in isolated temporary test storage.
- **FR-011**: Browser acceptance MUST cover desktop, narrow viewport, 200 percent zoom, light wells, dark wells, and the generated standalone portable file.
- **FR-012**: Existing asset bytes, approved logo geometry, colors, proportions, transparency, platform metadata, and download destinations MUST remain unchanged.
- **FR-013**: The correction MUST be made in governed brand source or shared generator sources and MUST NOT patch generated output.
- **FR-014**: Every production kit MUST complete with zero verification problems and zero glyph-validation failures, and the complete documented build and site validation MUST pass.
- **FR-015**: The generated guide MUST remain self-contained so its contrast and resource treatments work when the portable file is opened directly.
- **FR-016**: Preview analysis MUST behave deterministically for identical asset bytes and metadata.

### Key Entities

- **Integration delivery**: A generated-kit asset record with path, format, role, appearance metadata, dimensions, destination, and optional embedded sizes.
- **Visual preview candidate**: An SVG or PNG delivery whose exact artwork can be embedded in a preview well and whose meaningful visible output can be measured.
- **Preview well**: The light or dark surface selected to expose visual artwork and carry an accessible surface label.
- **Nonvisual resource treatment**: A visible presentation for metadata, declarations, XML, icon containers, and other resources that do not provide a directly previewable visual image.
- **Delivery group**: Related platform assets collected into one integration card with one representative and a complete delivery inventory.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100 percent of visual integration previews in the affected portable guide achieve at least 3:1 contrast between meaningful graphical content and the selected well.
- **SC-002**: 100 percent of text rendered inside preview wells achieves at least 4.5:1 contrast against its background, with no effectively invisible labels or fallback messages.
- **SC-003**: 100 percent of nonvisual XML, metadata, declaration, and container fixtures receive an explicit readable nonvisual-resource treatment.
- **SC-004**: All six required regression classes, transparent, black, white, full-color, metadata-only, and container, pass deterministic generation checks.
- **SC-005**: Desktop, narrow-viewport, 200-percent-zoom, light-well, dark-well, and direct portable-file browser checks complete with zero accessibility or layout failures.
- **SC-006**: Hash comparison reports zero changes to governed source assets and zero changes to generated icon, logo, metadata, declaration, or container delivery bytes; only generated guideline documents and their presentation metadata may change.
- **SC-007**: Every production kit reports zero verification problems and zero glyph-validation failures, and all documented generator, publication, Markdown, site, and browser suites pass.

## Assumptions

- WCAG 2.1 AA thresholds are 3:1 for meaningful non-text graphics and 4.5:1 for normal text in these preview wells.
- The shared portable-guideline generator is the governing correction point because the defect is systemic across integration cards and generated output must remain uncommitted.
- PNG and SVG deliveries are the directly previewable visual formats currently supported by the guide; metadata, XML, declarations, ICO, ICNS, and other containers require nonvisual semantics unless a governed visual representation is explicitly available.
- Existing I Heart PR Tours source assets and manifest declarations are authoritative and remain byte-for-byte unchanged.
- The static guide contains no authentication, private data, user input, or tenant boundary; applicable safety coverage is fail-closed local asset handling, escaped labels, destination integrity, and exclusion of synthetic fixtures from production discovery and publication.
