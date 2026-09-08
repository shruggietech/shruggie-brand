# Feature Specification: Site Interaction Affordances

**Feature Branch**: `codex/022-site-interaction-affordances`

**Created**: 2026-09-08

**Status**: Ready for owner merge review

**Input**: User description: "Combine GitHub issues #163 and #164 into S022, preserving browsing context for three named footer destinations while aligning documentation pagination cues and restoring pointer affordances on enabled theme controls."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Keep the brand site available from selected footer links (Priority: P1)

A visitor following Download the skill, Source, or License from any shared site footer opens that destination in a separate tab while the current brand-site page remains available.

**Why this priority**: These links currently replace the visitor's active brand-site context, creating unnecessary interruption across every page that uses the shared footer.

**Independent Test**: Inspect and activate every shared-footer link from representative marketing, brand, download, and documentation routes. The three named destinations must open separately with opener isolation, while Brands, Documentation, and Company remain ordinary same-tab links.

**Acceptance Scenarios**:

1. **Given** any page with the shared footer, **When** the visitor activates Download the skill, Source, or License with pointer or keyboard input, **Then** the destination opens in a separate browsing context and the current page remains available.
2. **Given** any page with the shared footer, **When** the visitor activates Brands, Documentation, or Company, **Then** the link retains normal same-tab behavior.
3. **Given** a selected new-tab link, **When** its relationship is inspected, **Then** it prevents the destination from accessing the originating page through an opener relationship and suppresses referrer disclosure.

---

### User Story 2 - Recognize and follow documentation controls (Priority: P2)

A documentation reader sees previous and next chevrons centered with their labels and receives a pointer cue over every enabled light- or dark-theme control.

**Why this priority**: Misaligned navigation cues and non-pointer controls make stable interactions appear visually broken or non-interactive.

**Independent Test**: Exercise documentation index and subpage navigation plus light and dark theme controls at desktop and mobile widths, with single-line and wrapped labels. Chevrons remain centered, enabled controls use a pointer, and all semantic, active, focus, and touch behavior remains intact.

**Acceptance Scenarios**:

1. **Given** a documentation pagination card, **When** its label occupies one or multiple lines, **Then** the directional chevron remains vertically centered with the label group and keeps a stable non-collapsing size.
2. **Given** either an enabled light- or dark-theme control, **When** a pointer hovers it, **Then** the control presents a pointer cursor without changing its semantic button behavior.
3. **Given** a current-theme or unavailable theme state, **When** a visitor inspects or operates the switcher, **Then** the state remains understandable through existing selected, disabled, label, and focus cues rather than cursor shape alone.

---

### User Story 3 - Prevent interaction-affordance regressions (Priority: P3)

A maintainer receives a failing gate when footer destination policy, pagination alignment, or theme-control cursor behavior drifts from the approved interaction contract.

**Why this priority**: The shared components affect many routes, so static and rendered checks are needed to prevent a small styling or metadata change from silently regressing the entire site.

**Independent Test**: Mutate each contract independently in an isolated fixture or source assertion. Missing new-tab safety attributes, accidental new-tab behavior on same-tab links, misaligned chevrons, and non-pointer enabled theme controls must each fail before publication.

**Acceptance Scenarios**:

1. **Given** a footer link with incorrect browsing-context metadata, **When** verification runs, **Then** it identifies the affected label and rejects publication.
2. **Given** a pagination label or chevron whose rendered centers diverge beyond normal rounding tolerance, **When** responsive verification runs, **Then** it identifies the route and rejects publication.
3. **Given** an enabled theme control without a pointer cursor or a disabled control presented as enabled, **When** interaction verification runs, **Then** it rejects publication.

### Edge Cases

- Company points to a different hostname but intentionally remains same-tab because the approved new-tab set is defined by explicit footer behavior, not hostname inference.
- External-looking URLs added later must not inherit new-tab behavior unless their footer metadata explicitly opts in.
- A wrapped previous or next label must align the chevron to the complete label group's vertical center rather than the first text line.
- A single-card first or last documentation page must preserve the same internal alignment as a two-card page.
- The chevron must not shrink when space is constrained at mobile widths.
- Current-theme state may be selected without being disabled; cursor treatment must follow actual enabled or disabled state.
- Keyboard activation and visible focus must remain equivalent to pointer activation for all affected links and controls.
- Reduced-motion preferences must not alter alignment, semantics, or browsing-context behavior.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Every shared-footer instance MUST apply the same explicit destination behavior contract.
- **FR-002**: Download the skill, Source, and License MUST open in a separate browsing context.
- **FR-003**: Each separate-context footer link MUST prevent opener access and referrer disclosure.
- **FR-004**: Brands, Documentation, and Company MUST retain same-tab navigation.
- **FR-005**: Footer destination behavior MUST be declared once as shared link metadata rather than inferred from hostname or repeated independently per route.
- **FR-006**: Existing footer labels, destinations, order, semantics, focus treatment, touch targets, and responsive layout MUST remain unchanged.
- **FR-007**: Previous and next pagination chevrons MUST share the vertical center of their complete label group within one rendered pixel.
- **FR-008**: Pagination alignment MUST remain correct for left- and right-pointing chevrons, single-line and wrapped labels, one-card and two-card layouts, and supported desktop and mobile widths.
- **FR-009**: Pagination chevrons MUST retain a stable non-collapsing visual size when labels wrap or available width contracts.
- **FR-010**: Every enabled light- and dark-theme control MUST use a pointer cursor when pointer input is available.
- **FR-011**: A genuinely disabled theme control MUST retain the project's established disabled treatment and MUST NOT be represented as enabled solely by cursor styling.
- **FR-012**: Current-theme state MUST remain perceivable through semantic and visual state independent of cursor shape.
- **FR-013**: Keyboard activation, accessible names, visible focus, selected and disabled semantics, reduced-motion behavior, and minimum touch targets MUST remain correct for affected controls.
- **FR-014**: Automated static coverage MUST distinguish all six footer destinations, enforce their exact browsing-context policy, and enforce the shared pagination and theme-control style contracts.
- **FR-015**: Automated rendered coverage MUST measure pagination label and chevron centers, inspect enabled and disabled theme-control cursor and semantic states, and exercise representative footer links with keyboard input.
- **FR-016**: Rendered verification MUST cover the documentation index, an interior documentation page, and an endpoint documentation page at supported desktop and mobile widths in both light and dark themes.
- **FR-017**: The final site MUST pass its existing static-export, responsive-layout, payload-integrity, interaction, and WCAG 2.1 AA gates.
- **FR-018**: This slice MUST NOT alter brand identity assets, generated kit contents, site information architecture, footer destinations, documentation sequence, or theme selection behavior.

### Key Entities

- **Footer destination record**: A shared declaration containing the visible label, destination, and explicit browsing-context policy for one footer link.
- **Separate-context destination**: One of the approved Download the skill, Source, or License records, including its opener-isolation and referrer policy.
- **Same-tab destination**: One of Brands, Documentation, or Company, which retains ordinary navigation behavior regardless of hostname.
- **Pagination cue**: A previous or next link containing a directional chevron and a complete label group whose centers form the alignment contract.
- **Theme control**: A semantic light- or dark-mode button with enabled, selected, and disabled states plus pointer and keyboard affordances.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100 percent of shared-footer instances open exactly Download the skill, Source, and License separately and leave exactly Brands, Documentation, and Company as same-tab links.
- **SC-002**: 100 percent of separate-context footer links prevent opener access and referrer disclosure.
- **SC-003**: Across every tested documentation route and supported width, previous and next chevron centers differ from their complete label-group centers by no more than one rendered pixel.
- **SC-004**: 100 percent of enabled light- and dark-theme controls report a pointer cursor, while every genuinely disabled control retains its disabled semantics and treatment.
- **SC-005**: All affected links and controls retain keyboard activation, accessible names, visible focus, semantic state, and touch targets of at least 44 by 44 CSS pixels.
- **SC-006**: Both themes and all tested responsive widths produce zero WCAG 2.1 AA violations on affected routes.
- **SC-007**: Static and rendered negative fixtures reject all four defect classes: unsafe or missing new-tab metadata, accidental new-tab metadata on same-tab destinations, pagination center drift, and incorrect enabled or disabled cursor treatment.
- **SC-008**: The complete static export and documented site verification finish with zero failures and no generated kit or identity-asset changes.

## Assumptions

- GitHub issues #163 and #164 are the complete scope of S022.
- The approved separate-context set is exactly Download the skill, Source, and License, even though Company also uses a different hostname.
- Company intentionally remains same-tab because issue #163 explicitly names it among the same-tab destinations.
- Existing shared pagination and theme controls remain the semantic source; this slice may apply shared site styling and verification but will not fork or replace those components.
- Supported viewports, themes, touch targets, and accessibility gates remain those already documented by the site verification suite.
- No release, dependency upgrade, documentation-content rewrite, or information-architecture change is included.

## Scope Boundaries

### In Scope

- Add explicit shared metadata for the six existing footer destinations and apply safe separate-context attributes to the three approved links.
- Normalize documentation pagination label and chevron alignment through a shared style contract.
- Apply correct cursor treatment to enabled and disabled light- and dark-theme controls.
- Add static and rendered regression coverage for destination policy, opener isolation, alignment, cursor behavior, semantics, keyboard interaction, focus, responsive layout, both themes, and accessibility.
- Update the site changelog and record verification evidence.

### Out of Scope

- Changing footer labels, order, destinations, or adding an external-link icon.
- Opening Company or all cross-domain destinations in a new tab.
- Replacing the existing pagination or theme-switcher components.
- Changing theme persistence, default theme, documentation ordering, page content, or navigation structure.
- Altering brand sources, generated kits, downloadable artifacts, identity geometry, or release versions.
- Cutting a release or deploying the site.

## Done When

- Issues #163 and #164 are satisfied by one shared, tested interaction contract.
- Exactly the approved three footer links use safe separate-context behavior on every shared-footer route.
- Documentation pagination cues and theme controls meet the measured alignment, cursor, keyboard, focus, responsive, and WCAG requirements.
- Negative regression coverage fails on each observed defect class.
- Static export and the complete documented site verification pass with zero failures.
- Spec Kit artifacts, implementation, tests, changelog, and evidence agree, and no generated outputs are committed.
