# Feature Specification: Documentation Contract Boundaries

**Feature Branch**: `codex/041-documentation-contract-boundaries`

**Created**: 2026-09-17

**Status**: Ready for Planning

**Input**: User description: "Deliver S041 under Spec Kit autopilot as the documentation-contract-boundaries slice, closing GitHub issue #213 by separating the main BrandBuilder manual, hosted child-brand references, and bundled implementation contracts while deriving shared facts from governed sources."

## Clarifications

### Session 2026-09-17

- Q: How should hosted guidance behave after newer BrandBuilder versions are published? -> A: Hosted guidance identifies the exact current generated contract, while the bundled implementation contract remains authoritative for older pinned bytes; this slice does not create a public historical-version archive.
- Q: What is the route migration policy for current published documentation and brand-guide URLs? -> A: Preserve every current route in place, add only necessary system-manual routes, and record a complete disposition ledger; no useful current route is silently retired.
- Q: How should the three overview graphics remain usable without script or image-export tooling? -> A: Publish semantic, responsive HTML structures with adjacent text equivalents and accessible labels; optional image exports are not a completion dependency.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Learn and extend BrandBuilder from one manual (Priority: P1)

As a maintainer or contributor, I can navigate one system manual that explains BrandBuilder architecture, operating modes, canons, recipes, adapters, verification, versioning, installation, releases, agent integration, and extension workflows without mixing those topics into an individual brand showcase.

**Why this priority**: The compiler and adapter foundation is now implemented, but its authoritative guidance is scattered across reference files and generated outputs. A coherent system manual is the prerequisite for maintaining and extending the platform safely.

**Independent Test**: Build the documentation site from governed sources, navigate every manual section at desktop and narrow widths with and without script, and confirm that all required system topics, ownership boundaries, cross-links, and current contract versions are present.

**Acceptance Scenarios**:

1. **Given** a maintainer starts at `/docs/`, **When** they follow the manual navigation, **Then** they can reach every required architecture, operation, implementation, verification, and release topic through a hierarchy distinct from brand references.
2. **Given** a contributor needs to extend a canon, recipe, adapter, verifier, or documentation source, **When** they read the relevant manual section, **Then** the section identifies the owning source, required workflow, generated outputs, validation entry points, and prohibited generated-output edits.
3. **Given** JavaScript is unavailable, **When** a reader opens any manual page, **Then** the full hierarchy, current-page indication, page content, diagrams, and adjacent text equivalents remain available.

---

### User Story 2 - Inspect one brand without reading the compiler manual (Priority: P2)

As a designer, implementer, or client stakeholder, I can use a hosted child-brand reference to understand that brand's identity, assets, interface specimens, supported bindings, inherited and overridden rules, exact supported kit version, and integration entry points without duplicated compiler architecture prose.

**Why this priority**: Hosted guidance is the public, brand-specific review surface. It must present the approved identity accurately while making its generated contract and version boundary explicit.

**Independent Test**: Build every production brand and site route, then inspect each hosted guide and confirm it uses generated brand data, declares exact contract versions and supported bindings, preserves affiliation boundaries, and contains no duplicated system-manual sections.

**Acceptance Scenarios**:

1. **Given** any production brand, **When** its hosted overview or integration guidance is opened, **Then** the page identifies the brand version and exact generated canon, recipe, Web/React, egui, and compiler contract versions used by that kit.
2. **Given** an independent client brand, **When** its hosted guide is reviewed, **Then** its approved identity, ownership, affiliation, and inheritance boundaries remain distinct from ShruggieTech identity while shared interface capabilities remain discoverable.
3. **Given** a reader needs compiler architecture or extension details, **When** they follow the hosted guide's system-documentation link, **Then** the system facts resolve to the main manual instead of being copied into the brand guide.

---

### User Story 3 - Implement exact delivered bytes offline (Priority: P3)

As a consumer agent or engineer, I can use the bundled implementation contract without network access to find exact paths, versions, tokens, component recipes, adapters, constraints, verification commands, recovery bytes, and capability-gap escalation rules for the delivered kit.

**Why this priority**: A consumer pins delivered bytes. Its instructions must remain complete after the public site advances and must agree mechanically with the hosted reference generated from the same source revision.

**Independent Test**: Generate a kit in an isolated temporary directory, disconnect hosted assumptions, follow the bundled contract from a fresh session, and prove that all declared files, versions, checks, recovery paths, and shared guidance facts resolve locally and match the same kit's hosted payload.

**Acceptance Scenarios**:

1. **Given** a delivered kit with no network access, **When** a fresh consumer reads `enforcement/consumer-contract.json` and `enforcement/IMPLEMENTATION.md`, **Then** every required implementation path, version, command, recovery byte, checksum, and escalation instruction is locally resolvable.
2. **Given** hosted and bundled guidance generated from the same kit, **When** their shared fact records are compared, **Then** identity, versions, bindings, verification, and escalation facts match exactly.
3. **Given** the public site later describes a newer contract, **When** an older consumer uses its delivered bundle, **Then** the bundled instructions remain explicitly authoritative for those pinned bytes and never redirect the consumer to an unspecified latest release.

---

### User Story 4 - Review ownership and migration evidence (Priority: P4)

As a reviewer, I can inspect a complete content disposition and three concise overview graphics that explain documentation ownership, operating modes, and the shared-improvement loop, with accessible text equivalents and no broken published links.

**Why this priority**: The migration is safe only when every current documentation page has an explicit owner and destination, and the new boundary is understandable without relying on source-code knowledge.

**Independent Test**: Validate the disposition ledger against all governed documentation sources and published routes, then review the three graphics and text equivalents at desktop, narrow width, 200 percent zoom, keyboard-only, no-script, reduced-motion, and forced-colors settings.

**Acceptance Scenarios**:

1. **Given** the pre-S041 documentation inventory, **When** the migration ledger is checked, **Then** every page is classified as preserved, consolidated, generated, redirected, or explicitly retired with owner, source, destination, and rationale.
2. **Given** any current public documentation or hosted brand route, **When** the new site is built, **Then** the route remains valid or has an explicit tested redirect and no useful content disappears.
3. **Given** the ownership, operating-mode, or improvement-loop graphic, **When** it is viewed under accessible display conditions or without styling, **Then** its labels, reading order, relationships, and equivalent text communicate the same information.

### Edge Cases

- A new Markdown reference is added without a documentation owner, navigation assignment, description, or disposition record.
- A hosted guide and bundled contract name different versions, bindings, verification commands, or capability-gap rules for the same generated kit.
- A current published route disappears, changes canonical URL, or is omitted from navigation without a disposition.
- A main manual page repeats brand-specific identity prose or a hosted brand page copies compiler architecture that has a governed manual owner.
- An older pinned kit is opened after the hosted site advances to newer contract versions.
- A diagram loses meaning when CSS, color, motion, or JavaScript is unavailable, or when content is enlarged to 200 percent.
- A third-party brand accidentally inherits ShruggieTech identity, endorsement, or presentation from shared documentation components.
- A generated path, link, or Markdown reference escapes its allowed source or publication root.
- Issue #193, #194, or #202 work is accidentally absorbed into this slice instead of remaining independently traceable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: BrandBuilder MUST define one governed documentation contract that assigns every documentation fact and surface to the main manual, hosted child-brand reference, bundled implementation contract, or an explicitly shared generated record.
- **FR-002**: The documentation contract MUST identify source ownership, generated consumers, navigation placement, version scope, offline availability, drift checks, and migration disposition without treating generated `dist/` output as source.
- **FR-003**: Every current documentation page and published documentation or brand-guide route MUST have a machine-checkable preserve, consolidate, generate, redirect, or retire disposition with a rationale and destination when applicable.
- **FR-004**: The main manual MUST cover system architecture, Author/Implementation/Audit modes, Brand and Interface Canons, component recipes, Web/React and egui adapters, verification, conformance, independent versioning, installation and recovery, releases, agent integration, and extension workflows.
- **FR-005**: The main manual MUST identify authoritative source paths, generated outputs, validation commands, and source-versus-artifact boundaries for extension workflows.
- **FR-006**: Hosted child-brand references MUST present approved identity, assets, interface specimens, supported bindings, inherited and overridden rules, affiliation boundaries, and integration entry points from verified generated data.
- **FR-007**: Each hosted child-brand reference MUST identify the exact brand, Brand Canon, Interface Canon, component recipe, Web/React adapter, egui adapter, and compiler versions supported by its generated kit.
- **FR-008**: Hosted child-brand references MUST link to system-manual owners for shared architecture and workflow facts instead of maintaining divergent copies.
- **FR-009**: Each bundled `IMPLEMENTATION.md` MUST remain complete offline and name exact local paths, versions, semantic tokens, component recipes, adapters, constraints, verification commands, recovery bytes and checksums, authority order, permitted exceptions, and capability-gap escalation.
- **FR-010**: Bundled guidance MUST state that it governs the delivered pinned bytes after hosted guidance advances and MUST NOT require an unspecified latest release or network access when delivered recovery bytes exist.
- **FR-011**: Hosted and bundled surfaces generated from one kit MUST consume a shared machine-readable fact record, and verification MUST fail on divergent identity, version, binding, verification, recovery, or escalation facts.
- **FR-012**: Documentation navigation MUST distinguish the system manual from brand references while preserving contextual previous/next navigation, semantic hierarchy, keyboard access, and no-script access.
- **FR-013**: Existing public documentation, guideline, download, and integration routes MUST remain valid unless an explicit tested disposition provides a redirect; no current useful route may disappear silently.
- **FR-014**: The main manual MUST include restrained documentation-ownership, operating-mode, and shared-improvement-loop graphics implemented with semantic reading order, readable labels, adjacent text equivalents, and responsive behavior.
- **FR-015**: Documentation and graphics MUST meet WCAG 2.1 AA and remain usable at desktop and narrow widths, 200 percent zoom, keyboard-only, no-script, reduced-motion, and forced-colors conditions.
- **FR-016**: Documentation prose MUST use direct operational language, avoid investor framing and repeated disclaimers, and preserve each hosted brand's approved presentation and identity boundaries.
- **FR-017**: Verification MUST reject missing owners, missing dispositions, duplicate navigation positions, unsafe paths, broken internal links, shared-fact drift, missing version scope, inaccessible diagram structure, and unapproved documentation sources with actionable diagnostics.
- **FR-018**: All eight production brands MUST rebuild and verify with zero `verify.py` problems and zero `validate_glyph.py` failures, with no approved artwork, geometry, palette, affiliation, or provenance changes.
- **FR-019**: Generated kits, site exports, PDFs, screenshots, archives, registries, and synthetic fixtures MUST remain uncommitted; authored text MUST use UTF-8 without BOM and LF line endings and pass a mojibake scan.
- **FR-020**: S041 MUST close issue #213 without implementing first-class light-theme presentation from #193, custom expressive assets from #194, or integration-preview repair from #202 and its existing S035 branch.

### Key Entities

- **Documentation Contract**: The versioned source record that assigns facts, owners, audiences, version scope, navigation, consumers, and drift rules across documentation surfaces.
- **Documentation Fact**: A governed statement such as a version, binding, verification command, authority path, recovery rule, or escalation rule that may be projected into more than one surface.
- **Documentation Surface**: The main system manual, one hosted child-brand reference, or one bundled offline implementation contract.
- **Content Disposition**: The preserve, consolidate, generate, redirect, or retire decision for an existing source page or published route.
- **Hosted Contract Summary**: The brand-specific generated facts exposed by the hosted reference for one exact kit.
- **Overview Graphic**: An accessible semantic relationship view with an adjacent text equivalent.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One hundred percent of current governed documentation source pages and published documentation or brand-guide routes appear in the disposition ledger with owner, source, destination, and rationale.
- **SC-002**: A reader can reach all ten required system-manual topic groups from `/docs/` and identify the authoritative source and validation entry point for each extension workflow.
- **SC-003**: All eight production hosted brand references declare the complete seven-domain version set and supported implementation bindings from their generated kit.
- **SC-004**: For every production kit, automated comparison reports zero differences between shared hosted and bundled identity, version, binding, verification, recovery, and escalation facts.
- **SC-005**: A fresh offline session can locate and validate every path, command, recovery artifact, and checksum required by the bundled implementation contract without network access or prior conversation context.
- **SC-006**: Existing public documentation and brand-guide routes have zero broken internal links, zero missing routes, and zero undocumented retirements after migration.
- **SC-007**: The manual, hosted references, and all three overview graphics pass desktop, narrow viewport, keyboard, no-script, 200 percent zoom, reduced-motion, forced-colors, and WCAG 2.1 AA verification with zero violations.
- **SC-008**: All eight production kits report zero verifier problems and zero glyph failures, and repository hygiene reports zero committed generated artifacts, UTF-8 BOMs, mojibake, or synchronized-instruction drift.

## Scope

### In Scope

- GitHub issue #213 in full.
- A governed documentation contract, complete source and route disposition, and drift validation.
- Main manual information architecture and missing system-manual coverage.
- Exact-version hosted child-brand summaries and system-manual cross-links.
- Complete offline bundled implementation guidance derived from shared facts.
- Three accessible overview graphics and text equivalents.
- Site navigation, route, no-script, accessibility, and link verification required by the documentation boundary.

### Out of Scope

- First-class light-theme guide presentation tracked by #193.
- Custom expressive and mood assets tracked by #194.
- Integration-preview visibility implementation tracked by #202 and `origin/codex/035-integration-preview-visibility`.
- Consumer repository adoption or mutation tracked by #219 through #221.
- Accepting visual conformance baselines, release tagging, publication, or deployment.
- Changes to approved identity artwork, geometry, palettes, affiliation, ownership, or provenance.

## Assumptions

- S041 begins from merged S040 on `main` at `454e7ccf2bacee822a6d42d7a220e571527157b2`.
- Issues #210 through #218 provide stable terminology, component, adapter, conformance, and version facts required by the manual.
- Existing public documentation and brand-guide routes are useful and should be preserved in place.
- The public site describes the current generated contract; exact older implementation guidance remains available inside the pinned delivered kit.
- Semantic responsive HTML is the authoritative graphic form because it remains accessible and reviewable without an export tool.
