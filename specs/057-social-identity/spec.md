# Feature Specification: Current Go Schedule Identity and Brand Social Images

**Feature Branch**: `codex/057-social-identity`
**Created**: 2026-09-25
**Status**: Clarified for planning
**Input**: Owner-directed issues #282 and #281, following S056's adaptive brief and two approval gates.

## User Scenarios & Testing

### User Story 1 - Use the current go-schedule mark (Priority: P1)

As the go-schedule owner, I see the existing blue prompt and mint cursor as the primary mark in every current mark, paired lockup, icon, and brand preview. The terminal frame, five asterisks, and rails are retired from current presentation without altering the approved reduced path data.

**Independent Test**: Compare the reduced source elements with the new primary master and generated lockups, then inspect full-color and monochrome wide and stacked proofs at large and small sizes.

### User Story 2 - Publish exact approved social copy (Priority: P1)

As a brand owner, I can explicitly approve a slogan and choose either a slogan-only composition or a slogan with a separate description line. No generator treats an existing descriptor or brand idea as my slogan without a recorded decision.

**Independent Test**: Build all eight brands from explicit copy decisions and reject a missing approval source, altered slogan, invalid line break, or unchosen description.

### User Story 3 - Deliver one distinct social image per brand (Priority: P1)

As a kit and website user, I can distinguish a 1280 by 640 social share image from wide and stacked logo lockups. The same approved identity and copy appears in the kit, downloads, brand-page Open Graph and Twitter metadata, and an upload-ready repository image.

**Independent Test**: Compare the generated image's digest with the brand-page exported image, inspect its manifest role and direct downloads, and verify unrelated routes still use route-specific cards.

### Edge Cases

- A brand has only an approved supplied lockup containing its wordmark and no standalone wordmark.
- A brand has a Gate 2 historical baseline but no explicit approval of the text as a slogan.
- The owner chooses a description but provides no approved description line breaks, or changes a slogan after image generation.
- The logo source changes after Gate 1 or the social image changes after Gate 2.
- An existing social-preview direct URL or repository image consumer still uses the former filename.
- Social crops, small-screen previews, or light and dark backgrounds reduce wordmark or slogan legibility.

## Clarifications

### Session 2026-09-25

- Q: Which exact social slogans and optional descriptions are approved for the six brands with ambiguous legacy fields? → A: The owner approved ShruggieTech “We advance your vision.”, I Heart PR Tours “Experience Puerto Rico”, Glitchpad “View your files.”, fragcap “See what your game is actually saying.”, ESO Weave “Unofficial automation for ESO”, and Covarity “See what is known.”, all with slogan-only layouts. Go Schedule retains its documented slogan with a slogan-only layout. Cueson retains its documented slogan and previously approved two-line description. This approval does not itself approve the assembled Gate 2 images.

### Session 2026-09-26

- Q: Does the later instruction to push approve the present go-schedule primary-mark and paired-lockup Gate 1 proof after an earlier request for changes? → A: Yes. The owner explicitly approved the current proof unchanged and instructed us to push.
- Q: Are the eight assembled social images approved for publication? → A: Yes. The owner said all social images look good for now and instructed us to push them.

## Requirements

### Functional Requirements

- **FR-001**: The go-schedule primary Full and Reduced roles MUST use byte-equivalent element data from the existing approved reduced path list, with the relationship recorded in provenance. The source comparison MUST reject a redrawn or normalized path. The owner direction in #282 is the identity decision; source-bound Gate 1 proof and assembled Gate 2 approval remain required before publication.
- **FR-002**: Go-schedule wide and stacked full-color and single-ink lockups, icon masters, guides, previews, and current direct downloads MUST use the simplified mark with the approved outlined wordmark. Existing applicable delivery families, formats, and sizes MUST remain available.
- **FR-003**: Every published brand MUST declare an exact slogan, a slogan-only or explicitly chosen slogan-and-description layout, approved copy provenance, and any approved line breaks. Missing or ambiguous decisions MUST block social-image publication. The six formerly ambiguous phrases were explicitly approved by the owner in the 2026-09-25 S057 clarification, all with slogan-only layouts.
- **FR-004**: The social composition MUST use the approved full-color wordmark or a supplied approved lockup containing it, exact approved copy, and a distinct social-image role. It MUST NOT be classified as a wide or stacked logo lockup.
- **FR-005**: The generator MUST emit a 1280 by 640 upload-ready PNG below 1 MB and a vector master where applicable, with direct download compatibility for previously published social-preview paths. The manifest and provenance MUST distinguish the canonical social image from any compatibility alias.
- **FR-006**: Brand-page Open Graph and Twitter metadata MUST point to image bytes derived from that brand's approved kit social image, with truthful size, media type, and alt text. Other route cards MUST remain route-specific.
- **FR-007**: Hosted and portable guidelines, downloads, usage guidance, and release notes MUST explain the social image's distinct purpose and the go-schedule identity change. This slice supplies only the social role terms needed by #281; the cross-brand asset naming grammar and one-design-per-card redesign remain in #283 and #284.
- **FR-008**: Managed repository Social Previews MUST be inventoried with their upload-ready assets and post-merge publication action. A repository setting MUST NOT be changed to unmerged or unapproved artwork.
- **FR-009**: Full documented kit, site, accessibility, source-continuity, manifest, and publication validation MUST pass. No generated `dist/` artifact is committed.

### Key Entities

- **Approved social copy**: Exact slogan, optional description, chosen layout and line breaks, approver, approval date, and source evidence.
- **Primary mark binding**: Current Full and Reduced roles, immutable path elements, source decision, continuity proof, and derivative lineage.
- **Social share image**: Canonical vector/raster paths, distinct role, image dimensions, checksum, brand binding, and compatibility alias.
- **Route social metadata**: Brand-page image URL and alt text, dimensions and type, and exported image identity.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All eight production brands build with an explicit approved slogan and selected social layout; missing or mismatched approval evidence fails before publication.
- **SC-002**: Every go-schedule current mark and paired lockup uses the existing reduced path elements without alteration, and no current preview shows terminal-frame or asterisk geometry.
- **SC-003**: Every brand has a distinct social-image manifest role, 1280 by 640 PNG below 1 MB, and a brand-page social URL whose exported bytes match the kit image.
- **SC-004**: Old social-preview direct links remain usable, non-brand route cards remain route-specific, and all eight kits pass zero-problem verification, zero-failure glyph checks, and the site WCAG 2.1 AA gate.

## Assumptions

- The exact go-schedule slogan is “A cross-platform scheduler in Go.” and the exact Cueson slogan is “Universal captions and subtitles,” as recorded in owner-directed issues and brand notes. The Cueson source notes explicitly preserve its two description lines and approved Gate 2 composition. The other six exact slogans and slogan-only layout are owner-approved in this S057 session. Their one-line visual treatment remains subject to Gate 2 proof review.
- S056's two creative approval gates apply. Repository social-preview upload is a separate publication action after the approved image is merged and released, not a third creative gate.
- The shared plain-English asset grammar and redesigned downloads grouping are separate issues #283 and #284; this slice must still name and classify social images truthfully.
