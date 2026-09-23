# Feature Specification: First-Class Light Brand Systems

**Feature Branch**: `codex/050-light-brand-systems`

**Created**: 2026-09-23

**Status**: Draft

**Input**: S050 approval to complete issue [#193](https://github.com/shruggietech/shruggie-brand/issues/193): make a brand-declared light presentation coherent across generated guides, hosted guidelines, portfolio surfaces, and quality gates without changing dark-first brands.

## User Scenarios & Testing

### User Story 1 - Read a light-first brand guide (Priority: P1)

As a reader of a light-first brand, I can open the PDF and portable guide and see consistent light paper, readable text, controls, examples, and approved identity artwork throughout.

**Why this priority**: A guide that switches unexpectedly to dark presentation misrepresents the approved light-first identity.

**Independent Test**: Build a declared light guide and a default-dark guide, inspect every page and the portable view, and measure their actual foreground and background pairings.

**Acceptance Scenarios**:

1. **Given** a brand explicitly declaring light presentation, **when** its PDF and portable guide are generated, **then** every outer page and nested reading surface uses light presentation with readable typography, borders, callouts, code, and logo wells.
2. **Given** a brand without a presentation declaration, **when** its guide is generated, **then** its established dark presentation remains the default.
3. **Given** an invalid presentation value or a light declaration without suitable governed light colors, **when** the brand is validated, **then** publication is blocked with a specific error.

---

### User Story 2 - Browse a light brand inside the public portfolio (Priority: P2)

As a visitor, I can browse a light-first brand's card, guideline route, and downloads without dark inherited panels or illegible assets, even while the surrounding portfolio remains dark.

**Why this priority**: The public surface is the first encounter with the identity and must not invert or obscure approved artwork.

**Independent Test**: Inspect a light brand and a dark brand across card, guideline, and download views at desktop, narrow mobile, and enlarged text sizes with and without client scripting.

**Acceptance Scenarios**:

1. **Given** a dark portfolio shell, **when** a light-first brand card is shown, **then** its foreground, icon well, actions, hover, and focus states form a complete light scope.
2. **Given** a light-first brand guideline or download route, **when** the page is opened, **then** its navigation, content panels, tables, asset wells, controls, and footer use the declared presentation rather than inherited dark styling.
3. **Given** a dark-first brand, **when** the same routes are opened, **then** its existing dark presentation remains intact.
4. **Given** a default-dark guide with a `light.*` showcase surface, **when** the brand is validated and published, **then** the light palette is complete and accessible, including at least 3:1 meaningful borders on each local light surface.

---

### User Story 3 - Trust the light and dark quality gates (Priority: P3)

As a maintainer, I can validate that each brand's declared presentation is actually used across generated documents and site views, and detect dark regressions on light surfaces before publishing.

**Why this priority**: A configuration field alone cannot prevent a dark cover, inherited dark card, or unreadable control from reappearing.

**Independent Test**: Run production and site validation with both presentation modes and inject an opposite-ground or low-contrast fixture to confirm the appropriate gate fails.

**Acceptance Scenarios**:

1. **Given** a light-first brand, **when** guide and page quality checks run, **then** they assess every page's outer ground and nested visible states and reject dark or inaccessible regressions.
2. **Given** a dark-first brand, **when** the same checks run, **then** its baseline still passes without a visual redesign.
3. **Given** a white-well logo asset, **when** it is previewed, **then** its intended light well remains visible in generated and hosted views.

### Edge Cases

- A declaration may be missing, malformed, or inconsistent with the available governed light colors. Missing means dark; malformed or incomplete explicit light must fail closed.
- A light portfolio showcase may be declared independently of the guide mode; it must receive the same light-palette validation even when the guide remains dark.
- Light artwork may be dark-lettered, transparent, or pale. Preview wells must be selected by approved surface role rather than a universal near-black fill.
- Brand-specific theme scopes must not silently change unrelated documentation or the portfolio shell.
- Text enlargement to 200 percent, 360 to 390px layouts, no-script navigation, reduced motion, and print output must preserve access to content and controls.
- The light and dark comparison samples remain available within a guide, but their surrounding document follows the declared mode.

## Requirements

### Functional Requirements

- **FR-001**: Each brand MUST have an optional, validated light or dark guide presentation declaration; absent declarations MUST preserve dark as the default.
- **FR-002**: An explicit light declaration MUST require governed light surfaces and foregrounds suitable for the guide's reading and interaction roles, with all required local pairings meeting WCAG 2.1 AA.
- **FR-003**: Generated PDF guides MUST use the declared presentation on every page, including cover, cards, tables, callouts, code, footers, and identity samples, with dark/light comparison samples explicitly contained.
- **FR-004**: Portable guidelines MUST use the declared presentation for outer document, nested panels, controls, focus and print without an unconditional dark body.
- **FR-005**: Hosted guideline and download routes MUST apply the brand's declared presentation to navigation, content, controls, asset previews, mobile accordions, and footer, independent of the public portfolio shell.
- **FR-006**: Portfolio cards and large logo wells MUST support a complete governed light scope, including foreground, action, hover, focus, meaningful border, and preview-well roles, while preserving dark-first cards. A `light.*` showcase role MUST require a complete accessible light palette independently of the guide mode.
- **FR-007**: Generated and hosted output MUST identify asset preview wells according to governed asset presentation, including approved marks requiring white wells, without changing master asset bytes.
- **FR-008**: Quality gates MUST reject a light-declared guide with dark outer pages or inherited dark UI areas and MUST validate measured WCAG 2.1 AA foreground, border, control, hover, focus, and semantic-state pairings on their actual surfaces.
- **FR-009**: Coverage MUST include light and dark brands, PDF pages, portable and hosted views, no-script output, 360 to 390px layouts, 200 percent zoom, reduced motion, print, and representative white-well assets.
- **FR-010**: Documentation MUST describe the authoritative brand-level presentation declaration, its dark default, validation requirements, and the distinct role of bounded light/dark comparison samples.
- **FR-011**: This slice MUST preserve approved logo geometry and bytes and MUST NOT modify downstream consumer repositories, custom imagery policy (#194), or publish a new release.

### Key Entities

- **Guide presentation**: An optional brand-owned light or dark declaration, defaulting to dark when absent.
- **Governed surface roles**: Brand-specific page, panel, reading, interactive, and asset-well colors evaluated as local foreground/background pairings.
- **Published guide surface**: A PDF page, portable document, hosted route, or portfolio component using the brand's declared presentation.
- **Presentation evidence**: Measured page ground, contrast, accessibility, and browser-state results linked to the declared mode.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One representative light-first and one default-dark production brand pass all guide generation and verification gates with zero problems, with the declared ground on 100 percent of PDF pages.
- **SC-002**: Across the card, hosted guide, downloads, and portable guide, all sampled text, border, control, hover, focus, and semantic state pairings meet WCAG 2.1 AA on their visible local surfaces.
- **SC-003**: Light and dark browser checks pass at 360px, 390px, desktop width, 200 percent text enlargement, no-script, reduced-motion, and print modes, with no inaccessible or clipped primary action.
- **SC-004**: At least one negative fixture each for invalid declaration, wrong PDF ground, and dark inherited light-brand UI fails its intended gate.
- **SC-005**: Dark-first output remains visually and mechanically consistent with the current baseline, with zero unintended theme switches or asset-byte changes.

## Assumptions

- Issue #193 is the authoritative scope for S050. Existing partial light-mode support is retained and completed rather than replaced wholesale.
- The I Heart PR Tours identity is a representative light-first fixture; its supplied master artwork is immutable.
- The portfolio shell may remain dark. Brand-specific surfaces must make an explicit local light scope where required.
- No downstream usage verification, consumer migration, new imagery rule, official release tag, or deployment is included in this PR.
