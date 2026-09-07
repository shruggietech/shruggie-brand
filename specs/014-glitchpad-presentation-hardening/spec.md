# Feature Specification: Glitchpad Pre-release Presentation Hardening

**Feature Branch**: `codex/014-glitchpad-presentation-hardening`

**Created**: 2026-09-07

**Status**: Ready for Planning

**Input**: Resolve GitHub issues #144 and #145 before the first Glitchpad desktop and Android release by centering non-square marks in square presentations and replacing diluted yellow showcase surfaces with governed charcoal surfaces.

## User Scenarios & Testing

### User Story 1 - See balanced Glitchpad identity presentations (Priority: P1)

As a visitor, I see the existing Glitchpad paper-and-G mark centered inside every square portfolio presentation without cropping, stretching, downward drift, or accidental double padding.

**Why this priority**: The current landing presentation visibly mis-centers the release-bound mark and weakens confidence in the supplied identity assets.

**Independent Test**: Inspect all five portfolio cards at mobile and desktop widths and at 200 percent zoom, then measure the Glitchpad image box and visible-ink bounds against the padded square.

**Acceptance Scenarios**:

1. **Given** the portrait Glitchpad mark in the 68 CSS-pixel landing slot, **When** the portfolio loads, **Then** its image box remains square and its visible ink has symmetric opposite margins within one raster pixel.
2. **Given** any of the five production portfolio marks, **When** it is viewed at 360px, 1280px, or 200 percent zoom, **Then** it remains centered, contained, proportional, and free of overflow or double padding.
3. **Given** a portrait, landscape, or asymmetric-canvas mark, **When** it is composed for a square delivery role, **Then** its visible bounds fit the role occupancy and clear-space contract without changing canonical path data.

---

### User Story 2 - See calm, governed Glitchpad showcase surfaces (Priority: P1)

As a visitor or release operator, I see Glitchpad marks presented on the brand's declared neutral surfaces, while sulfur yellow remains concentrated in intentional identity details rather than diluted across large backgrounds or shadows.

**Why this priority**: The current accent mixtures create an owner-rejected olive cast and diverge from the neutral surfaces already declared by the Glitchpad brand source.

**Independent Test**: Inspect the landing card, portfolio hero, relevant guideline examples, and generated application assets in dark and light contexts, comparing each surface with the governed brand values and confirming sibling brands are unchanged.

**Acceptance Scenarios**:

1. **Given** Glitchpad's landing card and portfolio hero, **When** they are rendered in the dark site theme, **Then** large showcase surfaces use declared Glitchpad charcoal values without a yellow or olive wash or decorative yellow glow.
2. **Given** a light presentation context, **When** a Glitchpad asset is shown, **Then** the appropriate declared light surface and compatible asset are used with readable text and focus treatment.
3. **Given** another production brand, **When** the same routes are rendered, **Then** its identity treatment and governed values do not change as a side effect.

---

### User Story 3 - Trust release-bound square exports (Priority: P2)

As a desktop or Android release operator, I can distinguish correct existing platform assets from defects and receive evidence that each required Glitchpad square export preserves visible-bound containment, platform-specific padding, and recognizability.

**Why this priority**: Outer square dimensions alone do not prove that a non-square glyph is centered or has safe visible bounds.

**Independent Test**: Rebuild and inspect full and reduced masters, standalone raster marks, web icons, Android legacy, adaptive, monochrome, and Play assets, recording unchanged passing paths separately from corrected paths.

**Acceptance Scenarios**:

1. **Given** each declared square export role, **When** visible bounds and occupancy are measured, **Then** the mark is uniformly scaled by its limiting edge and centered within the role-specific safe area.
2. **Given** an Android adaptive foreground, **When** it is validated, **Then** its separate foreground, background, and monochrome contracts remain intact and are not replaced by website padding.
3. **Given** an already correct generated asset, **When** S014 completes, **Then** it is recorded as verified without speculative source changes.

### Edge Cases

- Transparent source canvases may contain asymmetric whitespace even when their visible ink is symmetric.
- Portrait and landscape visible bounds must both fit without assuming height is always the limiting edge.
- Platform assets with baked plates must not receive a second plate or a second full padding treatment.
- Very small reduced marks must remain recognizable without changing their canonical geometry.
- Missing optional renderers must produce explicit skips rather than false passes or publication failures.
- A brand without a dedicated showcase-surface override must retain its current governed presentation rather than inherit Glitchpad values.
- Image load failure must not cause the portfolio card to overflow or collapse its accessible link target.

## Requirements

### Functional Requirements

- **FR-001**: S014 MUST cover and trace GitHub issues #144 and #145 in one Spec Kit slice.
- **FR-002**: The 68 CSS-pixel portfolio icon slot MUST contain a square image box inside its padding regardless of the source asset's intrinsic aspect ratio.
- **FR-003**: The Glitchpad mark's visible ink MUST be centered with opposite margins differing by no more than one raster pixel at the measured presentation size.
- **FR-004**: Portfolio presentations MUST preserve source aspect ratio and MUST NOT crop, stretch, overflow, or apply duplicate padding to any production brand.
- **FR-005**: Square export composition MUST scale visible bounds uniformly by the limiting edge and center them within the applicable role-specific occupancy and clear-space contract.
- **FR-006**: Regression coverage MUST include portrait, landscape, and asymmetric-source-canvas cases generated only in isolated temporary storage.
- **FR-007**: Full and reduced SVGs, standalone PNGs, web PNG and ICO outputs, Android legacy, adaptive, monochrome, and Play outputs, and other declared square platform assets MUST be inventoried as corrected, unchanged and verified, or explicitly skipped.
- **FR-008**: Platform-specific contracts MUST remain distinct; website presentation padding MUST NOT replace Android adaptive safe areas or other platform rules.
- **FR-009**: Glitchpad landing-card and portfolio-hero showcase surfaces MUST use neutral values governed by the Glitchpad brand source and generated site binding.
- **FR-010**: The site MUST NOT maintain an independent literal copy of the governed Glitchpad showcase surface.
- **FR-011**: Large Glitchpad showcase surfaces MUST contain no diluted yellow or olive wash and no decorative yellow glow.
- **FR-012**: Dark and light showcase contexts MUST use appropriate declared surfaces and compatible asset variants while meeting WCAG 2.1 AA for text and focus indicators.
- **FR-013**: S014 MUST record a cross-surface inventory of corrected and already-correct Glitchpad presentations.
- **FR-014**: Sibling-brand identity, functional status colors, and public-showcase authorization MUST remain unchanged.
- **FR-015**: Every canonical logo path string, the G channel, fold geometry, aspect ratio, and lockup proportion MUST remain byte-for-byte unchanged.
- **FR-016**: Glitchpad color-role reassignment, wordmark recoloring, and final identity selection tracked by #146 MUST remain out of scope.
- **FR-017**: All five production kits MUST finish with zero verification problems and zero glyph-validation failures.
- **FR-018**: Browser evidence MUST cover the landing card and portfolio hero at 360px and 1280px, 200 percent zoom, dark and light themes, and representative focus states.
- **FR-019**: The slice MUST pass the repository's complete Python, generation, site, accessibility, Markdown, encoding, and hygiene gates before publication.
- **FR-020**: Only source, tests, documentation, and Spec Kit evidence MAY be committed; generated kits, exports, screenshots, archives, and synthetic fixtures MUST remain uncommitted.

### Key Entities

- **Visible bounds**: The smallest rectangle containing non-transparent asset pixels or equivalent vector ink.
- **Square presentation**: A website or generated delivery role with equal outer width and height and a declared occupancy or clear-space policy.
- **Showcase surface**: A governed background value supplied by a brand source for large identity presentations.
- **Platform role**: A delivery context such as web, legacy launcher, adaptive foreground, monochrome, or store artwork, each with its own composition rules.
- **Verification disposition**: The recorded state of an inspected surface or export: corrected, unchanged and verified, or explicitly skipped.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The Glitchpad mark is centered in the 68 CSS-pixel landing slot with opposite visible-ink margins within one raster pixel and zero crop, stretch, overflow, or double padding.
- **SC-002**: Five of five production portfolio marks remain visually balanced at 360px, 1280px, and 200 percent zoom.
- **SC-003**: Every declared Glitchpad square-export role has a recorded disposition and every generated production asset passes its applicable visible-bound and occupancy checks.
- **SC-004**: The landing card and portfolio hero derive their Glitchpad showcase surfaces from generated brand data, with zero independently maintained copies of the governed value in site source.
- **SC-005**: Browser inspection finds zero yellow-tinted large Glitchpad backgrounds or decorative yellow showcase shadows across the in-scope routes.
- **SC-006**: Dark and light text and focus treatment on corrected surfaces produce zero WCAG 2.1 AA violations.
- **SC-007**: Canonical Glitchpad path strings and protected geometry have zero byte changes.
- **SC-008**: Five production kits report zero verification problems and zero glyph failures, and all complete repository and site gates pass.
- **SC-009**: Repository hygiene reports zero committed generated artifacts, synthetic fixtures, screenshots, private paths, BOMs, CRLF text files, or mojibake markers.

## Scope

### In scope

- GitHub issues #144 and #145.
- Portfolio icon containment, generated square-export containment evidence, governed showcase-surface binding, Glitchpad landing and portfolio presentation styling, regression tests, browser evidence, and release handoff notes.

### Out of scope

- Glitchpad identity color allocation or wordmark changes from #146.
- Guideline catalog, color-reference, and navigation work from #147 through #149.
- Site-wide link taxonomy and docs pagination from #142 and #143.
- Canonical path, fold, G-channel, lockup, or aspect-ratio changes.
- Release tagging, merging, or official binary publication.

## Assumptions

- Glitchpad's declared `card` surface is the intended dark showcase plate, while existing base and secondary surfaces remain available where hierarchy requires them.
- Existing Android adaptive and Play outputs are likely correct and should change only if objective regression tests prove otherwise.
- Generated brand metadata is the authoritative bridge between committed brand sources and site presentation.
- A pull request can close #144 and #145 after merge, but the issues remain open while the branch is under review.
