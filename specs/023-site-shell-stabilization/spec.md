# Feature Specification: Site Shell and Homepage Stabilization

**Feature Branch**: `codex/023-site-shell-stabilization`

**Created**: 2026-09-09

**Status**: Approved for implementation

**Input**: Work slice S023 covering GitHub issues #170, #171, #172, #176, #177, and #178.

## User Scenarios & Testing

### User Story 1 - Reach the primary destinations from the homepage (Priority: P1)

A visitor can immediately enter the documentation, download the current skill, or move to the portfolio through a clear and accessible hero hierarchy.

**Why this priority**: These are the homepage's primary calls to action and replace destinations that would otherwise be lost when the lower callout is removed.

**Independent Test**: Render the homepage at desktop and mobile widths, verify the exact action order and labels, follow each link, and confirm its visual, keyboard, touch, and reduced-motion behavior.

**Acceptance Scenarios**:

1. **Given** the homepage hero, **When** a visitor reads the actions in document order, **Then** they encounter the orange primary `Documentation` button, the green outline `Download Skill` button, and the separated green `Explore Our Portfolio` link in that order.
2. **Given** the supporting portfolio link, **When** assistive technology computes its name, **Then** the decorative downward arrow does not add redundant speech and the link targets the unchanged `#portfolio` anchor.
3. **Given** a narrow viewport, **When** the hero actions wrap or stack, **Then** their semantic order, complete labels, touch targets, and visible interaction states remain intact.

---

### User Story 2 - Understand and browse the portfolio without redundant homepage content (Priority: P1)

A visitor sees the portfolio under the exact heading `Our Portfolio`, reads `identity spectrum` naturally in its adjacent description, and is not distracted by the obsolete `The system underneath` panel.

**Why this priority**: The wording and section removal establish the approved homepage information architecture.

**Independent Test**: Inspect the rendered homepage and source assertions for the exact heading and phrase, unchanged anchor and cards, and complete absence of the removed panel and its obsolete content.

**Acceptance Scenarios**:

1. **Given** the portfolio section, **When** the page renders, **Then** its heading is exactly `Our Portfolio` and its adjacent copy reads `Explore our identity spectrum: a portfolio of distinct brands, each built with its own system, voice, and purpose.`
2. **Given** the homepage markup, **When** it is inspected, **Then** `The system underneath`, its contents, its wrapper, and its reserved visual space are absent.
3. **Given** any portfolio card or inbound homepage portfolio link, **When** it is used, **Then** the existing card content, route behavior, and `#portfolio` anchor continue to work.

---

### User Story 3 - Use consistent shared navigation and footer links (Priority: P1)

A visitor can reach the company site and current skill download from the main-site and documentation navigation, while the simplified shared footer retains only useful destinations.

**Why this priority**: Shared chrome is the persistent wayfinding surface on the homepage, download pages, and all documentation pages.

**Independent Test**: Render the homepage, a brand download route, the docs index, and a docs article in desktop and mobile modes, then verify exact labels, order, destinations, link attributes, focus behavior, and neutral guideline isolation.

**Acceptance Scenarios**:

1. **Given** shared main-site or docs navigation, **When** its desktop or mobile form is opened, **Then** `Company` and `Download Skill` appear with canonical destinations and safe external-link opener isolation.
2. **Given** a shared main-site or docs footer, **When** it renders, **Then** `Brands` is absent and the skill link reads exactly `Download Skill`.
3. **Given** the shared footer, **When** its links are inspected, **Then** Download Skill, Source, and License retain new-tab opener isolation, while Company retains the same-tab behavior explicitly established by S022.
4. **Given** a neutral per-brand guidelines portal, **When** it renders, **Then** the new ShruggieTech promotional navigation and shared footer changes do not alter its dedicated navigation contract.

---

### User Story 4 - Navigate without shell or reading-column movement (Priority: P1)

A visitor can move between the homepage and brand download pages, and between documentation pages with differing table-of-contents states, without persistent navigation or reading content shifting sideways.

**Why this priority**: Visible movement in shared UI undermines continuity and makes the site feel unstable.

**Independent Test**: Automated browser checks compare bounding boxes at identical viewport, zoom, theme, and scrollbar conditions across representative routes and fail when drift exceeds one CSS pixel.

**Acceptance Scenarios**:

1. **Given** identical desktop rendering conditions, **When** measurements are taken on `/` and every `/<brand-slug>/downloads/` route, **Then** the shared header container, logo, and menu controls have equivalent left edge, right edge, width, and center within one CSS pixel.
2. **Given** the docs index and representative articles with and without a right table of contents, **When** their outer shell and reading column are measured, **Then** the article left edge, width, and center remain equivalent within one CSS pixel.
3. **Given** short and tall routes, light and dark themes, and 100% and 200% browser scale emulation, **When** navigation occurs, **Then** scrollbar presence and table-of-contents state do not destabilize the persistent shell.
4. **Given** a mobile or narrow viewport, **When** the navigation or table of contents collapses, **Then** content remains visible and the document has no horizontal overflow.

### Edge Cases

- A route is shorter than the viewport while its comparison route requires a vertical scrollbar.
- Browser zoom or device scale changes produce fractional CSS-pixel measurements near a responsive breakpoint.
- A documentation page has no headings and therefore no right-hand table of contents.
- A documentation page has enough headings for a sticky right-hand table of contents and enough content to scroll.
- Hero actions wrap to multiple rows at narrow widths without changing semantic order.
- JavaScript is unavailable, so links and static navigation remain directly usable.

## Requirements

### Functional Requirements

- **FR-001**: The homepage hero MUST render `Documentation` as the leftmost orange primary action linked to `/docs`.
- **FR-002**: The homepage hero MUST render `Download Skill` immediately after Documentation as the green outline action linked to `https://github.com/ShruggieTech/shruggie-brand/releases/latest` with safe new-tab opener isolation.
- **FR-003**: The homepage hero MUST render a separated green `Explore Our Portfolio` link below the button row, target `#portfolio`, and include a vertically aligned decorative downward arrow.
- **FR-004**: Hero controls MUST preserve document order, complete labels, at least 44 by 44 CSS-pixel targets, visible hover/focus/active behavior, and reduced-motion behavior at supported desktop and mobile widths.
- **FR-005**: The portfolio heading MUST read exactly `Our Portfolio`; the adjacent description MUST contain the exact phrase `identity spectrum`; and the existing `portfolio` anchor, card content, and card routes MUST remain unchanged.
- **FR-006**: The authoritative homepage markup MUST NOT emit the `The system underneath` section, its content, empty wrapper, reserved space, or obsolete section-specific styles.
- **FR-007**: Shared navigation on the main site and every `/docs/` page MUST contain `Company` and `Download Skill` in desktop and accessible mobile variants, using `https://shruggie.tech/` and the canonical releases URL respectively.
- **FR-008**: Shared-navigation Company and Download Skill links MUST use safe external-link behavior with explicit opener isolation while preserving modifier-click and keyboard behavior.
- **FR-009**: Shared site and docs footers MUST omit `Brands`, use the exact label `Download Skill`, and preserve canonical destinations.
- **FR-010**: Footer Download Skill, Source, and License links MUST open in a new tab with opener isolation, while footer Company MUST retain same-tab behavior from S022.
- **FR-011**: Per-brand guidelines navigation and footer behavior MUST remain unchanged.
- **FR-012**: The homepage and every retained brand downloads route MUST consume the same shared shell width and horizontal gutter rules, with no route-specific transform, negative margin, or unexplained correction offset.
- **FR-013**: The docs index and docs articles MUST use a stable outer shell and reading-column allocation whether the right-hand table of contents is absent or present, and the rail MUST remain usable and sticky where designed.
- **FR-014**: The shared document shell MUST prevent vertical-scrollbar presence from moving persistent navigation or intended aligned content edges.
- **FR-015**: Automated source and rendered-site checks MUST verify exact copy, canonical destinations, external-link attributes, removed content, route scope, mobile availability, and neutral-guideline isolation.
- **FR-016**: Automated browser checks MUST compare relevant bounding boxes across all download routes and representative docs layouts at desktop, narrow, light, dark, 100%, and 200% scale conditions with a maximum one CSS-pixel tolerance.
- **FR-017**: Static export, route inventory validation, WCAG 2.1 AA audits, keyboard interaction checks, and repository hygiene checks MUST pass with no new violations.

### Key Entities

- **Shared navigation link**: A canonical label, destination, placement, and external-link policy consumed by main-site and documentation shells.
- **Shared footer link**: A canonical label, destination, and surface-specific browsing-context policy consumed by main-site and documentation footers.
- **Shell measurement**: A route, viewport, theme, scale, scrollbar state, selector, and measured bounding box used to detect visible drift.
- **Documentation layout state**: A docs route categorized by right-table-of-contents presence and content height for stable-column comparisons.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All six linked GitHub issues have automated acceptance coverage and are traceable from the S023 specification and pull request.
- **SC-002**: Homepage tests confirm all approved labels, order, destinations, token-backed treatments, copy, anchor behavior, and complete removal of the obsolete callout.
- **SC-003**: Navigation and footer tests pass on the homepage, every retained download route, the docs index, representative docs articles, and mobile navigation, with zero affected-surface label or target-policy discrepancies.
- **SC-004**: Cross-route header and reading-column bounding boxes differ by no more than one CSS pixel under every declared comparison condition.
- **SC-005**: Every tested page has zero horizontal overflow at supported desktop and narrow widths and at 100% and 200% scale emulation.
- **SC-006**: The complete documented repository validation reports zero production-kit verification problems, zero glyph failures, zero accessibility violations, and zero repository-hygiene violations.

## Assumptions

- The S022 footer behavior is authoritative: footer Company remains same-tab, even though Company is a safely isolated external link in shared navigation.
- Fumadocs remains the shared main-site/docs navigation implementation and may be constrained with shared CSS rather than forked or replaced.
- One CSS pixel is the maximum acceptable cross-route measurement variance because smaller differences are raster-rounding noise rather than visible layout drift.
- Browser scale coverage may use equivalent viewport and device-scale emulation when automated browsers cannot directly control interactive zoom.
- Issues #173, #174, #175, #179, and #180 are outside S023 and must not be implemented incidentally.

## Traceability

- GitHub #170: FR-001 through FR-004, FR-015, SC-002
- GitHub #171: FR-005, FR-015, SC-002
- GitHub #172: FR-006, FR-015, SC-002
- GitHub #176: FR-012, FR-014, FR-016, SC-004, SC-005
- GitHub #177: FR-007 through FR-011, FR-015, SC-003
- GitHub #178: FR-013, FR-014, FR-016, SC-004, SC-005
