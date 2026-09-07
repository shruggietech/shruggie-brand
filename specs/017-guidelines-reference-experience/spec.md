# Feature Specification: Guidelines Reference Experience

**Feature Branch**: `codex/017-guidelines-reference-experience`

**Created**: 2026-09-07

**Status**: In Review

**Input**: GitHub issues #147, #148, and #149.

## Clarifications

### Session 2026-09-07

- Q: What inventory should drive the asset catalog? -> A: Generated logo provenance and platform icon manifests are authoritative; visually identical size-only outputs collapse into one preview while every delivered path, format, size, and destination remains listed.
- Q: How should links work in portable and hosted guides? -> A: Generate portable relative links, then rewrite only declared kit-asset links during site publication and add one hosted-only `All brands` exit.
- Q: How should print color be represented without an output profile? -> A: Show HEX, RGB, HSL, OKLCH, and Lab D50; state that CMYK requires an output profile and never invent spot or universal CMYK values.

## User Scenarios & Testing

### User Story 1 - Find and use every distinct asset (Priority: P1)

As a designer or agent, I can browse one representative preview per distinct logo and application-icon design, then see every actual delivery size, format, destination, and usable source link.

**Why this priority**: A brand guide that hides most shipped assets cannot function as the kit's reference surface.

**Independent Test**: Build each production guide from its generated manifests and confirm all unique design groups are present once, all delivery records resolve, and missing optional capabilities are stated rather than advertised.

**Acceptance Scenarios**:

1. **Given** multiple size-only copies of one visual design, **When** the catalog renders, **Then** one representative preview lists all delivered sizes and paths.
2. **Given** Full, Reduced, light, dark, monochrome, plated, and unplated assets, **When** their designs differ semantically, **Then** each is named and previewed separately.
3. **Given** a hosted or portable guide, **When** a user follows an asset link, **Then** it resolves within that publication context.

---

### User Story 2 - Copy governed colors and compare themes (Priority: P1)

As a designer or developer, I can copy accurate multi-format color references and inspect bounded dark and light examples of palette, type, charts, and components without changing the guide's overall dark presentation.

**Why this priority**: Reuse errors and dark-only examples make the current guide incomplete for normal product and print-reference work.

**Independent Test**: For every production color, compare displayed conversions with the canonical value, exercise copy success and failure paths, and measure both themed wells at mobile and desktop widths.

**Acceptance Scenarios**:

1. **Given** a governed color, **When** its details are opened, **Then** HEX, RGB, HSL, OKLCH, and Lab D50 describe the same color within documented rounding tolerance.
2. **Given** clipboard access succeeds or fails, **When** copy is activated, **Then** status is announced honestly and the displayed value remains selectable.
3. **Given** a light comparison well inside the dark guide, **When** it renders, **Then** its complete local token context, text, controls, charts, and focus states meet WCAG 2.1 AA.

---

### User Story 3 - Navigate a long guide without host branding (Priority: P1)

As a keyboard, touch, or direct-link visitor, I can use a compact contents menu, stable section anchors, a progressive back-to-top control, and one neutral hosted exit without receiving a marketing shell or broken offline link.

**Why this priority**: The expanded reference becomes difficult to use without restrained internal navigation, especially on narrow screens.

**Independent Test**: Navigate all sections with and without script at 360 and 1280 pixels, activate back-to-top with reduced motion, and verify the hosted exit exists only after publication context is applied.

**Acceptance Scenarios**:

1. **Given** script is unavailable, **When** the guide loads, **Then** contents and a usable top anchor still work.
2. **Given** the opening area has left view, **When** script is available, **Then** a focus-safe back-to-top control becomes available without covering content.
3. **Given** a hosted guide, **When** the footer renders, **Then** it has one understated `All brands` link; the portable guide omits it.

### Edge Cases

- Core-tier kits with skipped raster suites expose only generated assets and name unavailable suites.
- Long titles, paths, color values, and platform records wrap without horizontal overflow at 360 pixels and 200 percent zoom.
- Clipboard denial, missing APIs, and local-file use never report false success.
- Deep links account for the compact contents region and retain visible headings.
- Byte-identical aliases retain integration paths without duplicate previews.
- Existing affiliation and social metadata remain unchanged and do not become license to add ShruggieTech identity chrome.

## Requirements

### Functional Requirements

- **FR-001**: The guide MUST derive its logo inventory from generated logo provenance and its application inventory from generated icon manifests.
- **FR-002**: The catalog MUST group size-only or byte-identical deliveries into one preview while retaining every path, format, measured size, destination, and alias.
- **FR-003**: Distinct Full, Reduced, orientation, colorway, appearance, adaptive, plated, unplated, and composite designs MUST remain separately discoverable.
- **FR-004**: Each group MUST provide a largest suitable representative, concise use guidance, background/transparency context, minimum-size or clear-space guidance, and usable asset links.
- **FR-005**: Catalog output MUST state skipped capabilities and MUST NOT advertise absent files.
- **FR-006**: Portable asset links MUST resolve relative to the kit, while hosted publication MUST rewrite only declared asset links to their copied download destinations.
- **FR-007**: Every governed color MUST expose copyable HEX, sRGB RGB, CSS HSL, OKLCH, and CIELAB D50 values derived from the same canonical source.
- **FR-008**: Conversions MUST declare channel units, white point where applicable, and stable rounding precision without altering canonical colors.
- **FR-009**: Without an explicit governed output profile, print guidance MUST state `CMYK: output profile required` and MUST NOT assert spot-color matches.
- **FR-010**: Copy controls MUST be real buttons with accessible names, visible focus, touch-friendly targets, honest success/failure announcements, and selectable text fallback.
- **FR-011**: Bounded dark and light wells MUST demonstrate palette, chart, typography, and component roles using complete generated token contexts.
- **FR-012**: All text, interactive controls, and focus states MUST meet WCAG 2.1 AA on their actual local surfaces, with no color-only status cue.
- **FR-013**: Stable descriptive section IDs and a compact contents navigation MUST cover the complete final guide structure.
- **FR-014**: Back-to-top MUST retain a no-script anchor fallback, appear only when useful with script, leave hidden controls unfocusable, restore useful focus, and honor reduced motion.
- **FR-015**: Hosted guides MUST add exactly one neutral deterministic `All brands` exit; portable guides MUST omit it.
- **FR-016**: New navigation MUST remain brand-neutral and MUST NOT add a shared site shell, ShruggieTech identity marks, cross-brand chooser, redirect, or marketing CTA.
- **FR-017**: All controls and layouts MUST remain usable at 360 and 1280 pixels, touch input, keyboard input, direct deep links, and 200 percent zoom.
- **FR-018**: Verification MUST reject omitted unique groups, nonexistent records or links, smaller-than-available representatives, duplicate size-only previews, inaccurate conversions, inaccessible local states, and hosted/portable contract drift.
- **FR-019**: All five production kits MUST retain zero verifier problems and zero glyph failures without changing logo geometry, approved colors, affiliation text, or release version.
- **FR-020**: S017 MUST close issues #147, #148, and #149 with synchronized specifications, tests, evidence, documentation, and changelog records.

### Key Entities

- **Asset Delivery**: One generated file with source family, semantic role, appearance, format, measured dimensions, destination, and publication-relative path.
- **Asset Group**: Deliveries sharing one visual and semantic design, with one representative preview and complete delivery list.
- **Color Reference**: One canonical color plus deterministic alternate-space representations and role metadata.
- **Comparison Well**: A bounded dark or light token context containing representative palette, type, chart, and component content.
- **Guide Navigation Context**: Stable internal sections plus optional hosted publication values that never contaminate the portable source.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every distinct generated asset design across all five production brands appears exactly once, while 100 percent of delivered logo and icon files remain discoverable through group records.
- **SC-002**: Every displayed color representation round-trips to its canonical color within 0.5 RGB channel units or an equivalent perceptual tolerance.
- **SC-003**: All guide text and controls pass WCAG 2.1 AA, every interactive target is at least 44 by 44 CSS pixels where practical, and no tested layout overflows at 360 pixels or 200 percent zoom.
- **SC-004**: All internal, portable asset, and hosted asset links resolve in their declared context, with exactly one hosted exit and zero portable host exits.
- **SC-005**: Scripted copy and back-to-top behaviors pass success, failure, reduced-motion, and keyboard tests; no-script contents and top anchors remain functional.
- **SC-006**: The aggregate build completes for all five brands with zero verification problems, zero glyph failures, and no identity, palette, affiliation, or release-version drift.

## Assumptions

- Existing generated provenance and icon manifests are complete after S016 and can be extended only if a missing grouping fact cannot be derived safely.
- A dark outer guide with locally scoped light wells matches the approved direction; S017 does not add a global theme toggle.
- Existing brand affiliation copy and hosted metadata remain valid; the new `All brands` exit is navigation context, not endorsement.
- Client-side behavior uses progressive enhancement and requires no network service or stored user data.

## Scope Boundaries

### In Scope

- Generated guideline catalog, color references, themed demonstrations, internal navigation, back-to-top behavior, hosted link rewriting, tests, five-brand evidence, and documentation.

### Out of Scope

- Site-wide link taxonomy, docs pagination cards, global theme switching, new brand assets, identity or palette changes, release publication, analytics, and a marketing shell.

## Done When

- Issues #147, #148, and #149 are closed by one review-clean PR whose final head has green CI; all Spec Kit artifacts and verification evidence agree with the implemented portable and hosted guide contracts.
