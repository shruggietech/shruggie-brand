# Feature Specification: Local Media Gallery Brand and Official Showcase

**Feature Branch**: `codex/071-localmedia-gallery-brand`

**Created**: 2026-10-21

**Status**: Both creative gates are approved with exact source and social-image bindings. The final Local Media Gallery 1.0.0 kit, all 13 production builds, full aggregate validation and staged publication audits pass. The source-only publication candidate is prepared for PR review; live publication remains outstanding.

**Input**: The owner requests an official new brand package for domain `localmedia.gallery`, published on the ShruggieTech brands website as an official ShruggieTech project. Exact slogan: "Your media presented beautifully." Exact description: "A lightweight, interactive gallery for browsing local images and videos." Explore LMG lettermarks and recognizable media/gallery/image/video glyphs, both including and excluding the abbreviation. The domain-registration screenshot is spelling/context evidence, not supplied identity artwork or additional instructions.

**Tracking issue**: [#326](https://github.com/shruggietech/shruggie-brand/issues/326)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Choose and approve a logo (Priority: P1)

The owner compares concrete lettermark and media-symbol directions, refines the selected direction and palette, then approves the actual proposed production Full and Reduced masters.

**Why this priority**: All subsequent brand applications must derive from an owner-approved identity.

**Independent Test**: Review the direction comparison and, later, the exact source-bound approval packet with both masters at four sizes on four surfaces.

**Acceptance Scenarios**:

1. **Given** the owner brief, **When** directions are prepared, **Then** the comparison includes LMG and media/gallery/image/video concepts with and without letters.
2. **Given** direction feedback, **When** the production candidate is constructed, **Then** the exact geometry, palette, framing and complete 32-proof matrix are presented before approval.
3. **Given** an approved candidate, **When** derivatives are produced, **Then** they preserve the approved source, and governed drift requires a new source decision.

### User Story 2 - Review and receive the brand package (Priority: P2)

The owner reviews the assembled identity, including lockups, typography, formal palette, separate functional colors, representative gallery application and social image, then receives a verified package.

**Why this priority**: The brand must work in real gallery and public-brand contexts, using the supplied messages exactly.

**Independent Test**: Inspect the assembled fundamentals packet and verify the final package has zero mandatory kit problems and zero glyph failures.

**Acceptance Scenarios**:

1. **Given** the supplied slogan and description, **When** public messages are prepared, **Then** their wording is preserved exactly and no unsupported product claim or additional message role is inferred.
2. **Given** approved logo source, **When** fundamentals are assembled, **Then** both light and dark uses, wide and stacked lockups, small icons, typography and the distinct social composition can be reviewed.
3. **Given** complete approvals, **When** the final kit is compiled, **Then** mandatory validation passes and any optional missing capability is named.

### User Story 3 - Find the official published brand (Priority: P3)

A visitor finds localmedia.gallery in the official ShruggieTech brands catalog and accesses matching guidelines, assets and downloads.

**Why this priority**: Official publication is part of the requested outcome.

**Independent Test**: Verify official catalog, guidelines and downloads resolve to the approved identity and version after the reviewed publication workflow.

**Acceptance Scenarios**:

1. **Given** a verified approved kit, **When** the site is built and published, **Then** its public entry identifies an official ShruggieTech project and projects the approved source and exact messages.
2. **Given** public download links, **When** a visitor downloads a package, **Then** the delivered version and checksums match the published inventory.
3. **Given** private directions and pending approvals, **When** the site builds, **Then** exploratory files are excluded.

### Edge Cases

- The owner-corrected display name is `Local Media Gallery`; `localmedia.gallery` is the address.
- Direction selection is not production-source approval. Silence approves neither creative gate.
- Tiny marks may need a simpler Reduced master rather than compressed letters or collapsed counters.
- An image-only icon must not imply that the product excludes video; a play-only icon must not imply that it excludes images.
- "Local" describes the supplied scope, without inferring privacy, offline, no-cloud, installation or performance claims.
- The screenshot's registrar branding and administrative controls are not identity source.
- Formal identity colors and functional state colors are separate decisions; inaccessible values change.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Maintain a working brief separating owner facts, constraints, proposals and unresolved decisions.
- **FR-002**: Preserve `Local Media Gallery` as the display/typed name and `localmedia.gallery` as the address. Preserve the supplied slogan and description exactly in their intended roles.
- **FR-003**: Explore at least one LMG lettermark and at least two recognizable media/gallery/image/video directions without letters.
- **FR-004**: Present the actual production Full and Reduced source, palette qualification, framing, renderer and 32 proofs before Gate 1 approval.
- **FR-005**: Preserve approved source through promotion and generation; invalidate approvals on governed drift.
- **FR-006**: Present wide/stacked lockups, applicable wordmark, formal palette, separate interface cues, typography, representative use and a distinct exact-copy social composition at Gate 2.
- **FR-007**: Record message roles and social-image decisions independently; preserve unresolved additional messages rather than inventing claims.
- **FR-008**: Meet WCAG 2.1 AA for declared text and functional cues on light and dark surfaces and provide non-color state signals.
- **FR-009**: Compile the final package only after both creative approvals and require zero mandatory verification problems and zero glyph failures.
- **FR-010**: Publish approved verified content through the official reviewed site/release workflow and verify live routes and matching downloads.
- **FR-011**: Keep exploratory material and generated outputs out of committed production source; preserve all existing identity geometry.
- **FR-012**: Save authored text as UTF-8 without BOM and LF and inspect delivered text/artifacts for encoding corruption.
- **FR-013**: Shared geometry tooling MUST support transparent compound cutouts through approved primitives without changing selected or existing logo geometry; invalid/open path composition MUST be rejected.
- **FR-014**: Generated type specimens MUST keep the complete brand name inside the header, preserve approved wordmark segment colors and retain supplied path fill rules without rewriting mark geometry.
- **FR-015**: The shared generator MUST support source-owned horizontal wordmark lines with exact text, font sizes, roles, visible-ink alignment and spacing. Local Media Gallery MUST reproduce selected B (48-unit Local Media above 84-unit Gallery beside a 160-unit icon) without changing standalone, symbol-above-name or existing-brand layouts. Invalid line geometry, text/role mismatches or contradictory supplied wordmark bindings MUST fail before publication.

### Key Entities

- **Working brief**: Facts, proposals, decisions and exact-copy evidence for one owned project.
- **Logo candidate**: Full/Reduced production source, geometry evidence and approval-bound proofs.
- **Fundamentals packet**: Source-derived applications, palettes, type and exact social composition.
- **Verified kit**: Versioned assets, supported bindings, guides and measured verification.
- **Official projection**: Catalog, guidelines, assets and downloads from the same approved kit.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The owner receives four concrete initial directions spanning LMG and media-symbol concepts.
- **SC-002**: Both creative approvals bind actual review packets; Gate 1 includes all 32 production proofs.
- **SC-003**: The final kit reports zero mandatory verification problems and zero glyph failures, and rendered deliverables are inspected.
- **SC-004**: Every public message retains its explicitly supplied or separately approved wording and intended role.
- **SC-005**: Official routes and downloads resolve to the approved version and matching checksums.
- **SC-006**: No generated kit, concept raster, PDF, registry or archive enters version control; existing identities pass the documented aggregate checks.

## Assumptions

- ShruggieTech ownership, official-project relationship and official-brand-site publication are explicitly supplied by the owner.
- Owner-corrected display name: `Local Media Gallery`. Source brand slug: `localmedia-gallery`; domain: `localmedia.gallery`.
- The owner approved Jade, #69D4BB on dark and #08745F on light, with the then-shown lowercase domain in Space Grotesk Bold. The owner subsequently corrected the typed name to Local Media Gallery; revised lettering must replace that superseded wordmark. Full/Reduced geometry and Jade remain preserved.
- Proposed endorsement: `A ShruggieTech project`, with no separate service credit. Formal affiliation and palette declarations will reflect the owner's actual decisions.
- The supplied slogan and description are approved for their declared roles. The final social image is approved with only the exact slogan and selected horizontal logo, vertically centered as a group. Additional undeclared messages remain unresolved.
- Intended first examples: gallery interface, web/app icons, official guidelines and social share image. The product application and domain deployment are separate from this package.

## Clarifications

- 2026-10-21: The owner explicitly supplies the domain, slogan, description, official ownership/publication relationship and logo-exploration scope. No existing mark is supplied.
- 2026-10-21: Start four private vector directions in one provisional palette to compare geometry without making an unapproved formal color decision. Full production-source approval follows direction refinement.

- 2026-10-21: The owner states "Let's go with D. Continue down that direction." Select Contact sheet for production development; retain the four-tile arrangement and image/video cues. This is direction selection, with exact production-source and assembled-fundamentals approvals still pending.

- 2026-10-21: Preserve selected Full geometry exactly and prepare a Reduced master that keeps all four tiles, removes the sun and simplifies the landscape to one peak. Proposed Periwinkle source packet passes geometry, qualified palette and 32 repeated production-proof checks. Gate 1 remains pending.

- 2026-10-21: The owner selects "Jade" (B) and asks for a wordmark paired with the square logos. Preserve both square masters unchanged, requalify Jade, and prepare private standalone, horizontal and stacked wordmark previews before exact Gate 1 approval as explicitly requested. This changes the preview order without granting source or publication approval.

- 2026-10-21: The owner states "Approved as shown. Continue with the Jade logo, wordmark, and pairings, and assemble the remaining brand fundamentals for review." Record Gate 1 approval of packet 6425438892c7dbcfc9e1bcf84adaa38e0f60db3fdd15bd4d704c44a6a03f9e44 and promote exact source with canonical binding cea811ec0e040d1fa19645f25882e21d0fc463c22e4d528122d0030835cd0d41. The assembled fundamentals and exact social layout remain pending the second creative decision.

- 2026-10-21: The owner corrects the typed brand name: "Let's not format the typed form as a domain. It's "Local Media Gallery" - or Local Media stacked on top of the word "Gallery", if necessary.". Use title-case Local Media Gallery for wordmarks and display copy; retain localmedia.gallery only as the domain. The primary name fits one line. Preserve approved square masters and Jade while preparing the changed wordmark/source binding for review.

- 2026-10-21: The owner requests smaller type and a larger icon in the horizontal pairing, and asks to consider Local Media above a larger Gallery. Prepare two private outlined typography studies with the same visible icon size; recommend the two-line hierarchy. The prior equal-height horizontal layout is superseded for this request. Do not infer approval of either new layout.

- 2026-10-21: The owner explicitly chooses and authorizes B: "Let's go with B. Use that horizontal pairing with Local Media above Gallery and the larger icon, and update the brand fundamentals for review." Adopt the actual shown B row hierarchy and relative icon size. Preserve prior square-source approval and require production output to reproduce the selected outlined artwork before updating the fundamentals. This authorizes the source amendment and review refresh, while assembled Gate 2 approval remains pending.

- **FR-016**: The social share image MUST omit the description and retain the approved horizontal logo and exact slogan at their existing sizes and spacing. Center their combined visible ink vertically on the 1280 by 640 canvas through an explicit centered-group composition; preserve other brands' default social layouts and all approved logo geometry.

- **FR-017**: Full publication validation MUST retain the required npm audit floor. If the pinned WordPress test fixture fails that gate, apply narrowly scoped patched dependency pins and verify the fixture transport, affected dependency behavior and both declared WordPress/PHP runtime pairs. Do not weaken audit thresholds or change consumer adapter contracts.
