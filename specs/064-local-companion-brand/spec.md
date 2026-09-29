# Feature Specification: Local Companion Brand Kit and Public Showcase

**Feature Branch**: `codex/064-local-companion-brand`
**Created**: 2026-09-28
**Status**: Complete; both creative gates approved, required CI passed, v2.8.0 published, and live Local Companion assets verified
**Input**: Construct a formal Local Companion kit for the official ShruggieTech brand subdomain. The owner confirmed ShruggieTech ownership, public showcase permission, rights to the existing app assets, an independent graphite and indigo palette, and a new abstract symbol instead of the current LC monogram.

## Clarifications

Local Companion is a private Windows workspace for chatting with personalized AI companions, creating images, and managing the local characters and models behind those experiences. The public brand presentation must describe the product without exposing private chats, companion imagery, owner data, model files, or screenshots that are not ready to share. The existing LC SVG is a rejected reference because its letter orientation is unsatisfactory. The W placeholder packaging icon is not approved artwork. The S014 local-only brand decision applied to that implementation and is superseded here by the owner's explicit request for a formal, public kit.

The owner selected independent graphite and indigo rather than house orange: graphite `#090B10` and `#11151D`, primary indigo `#8B9CFF` with `#A8B5FF` and `#7184EB` variants, and near-white `#F4F6FB`. The owner selected the lower-right calm-orbit abstract direction and approved its exact Gate 1 candidate on 2026-09-28. The owner also chose app parity for the four functional cues and approved the corrected exact Gate 2 packet (SHA-256 `4f668c3e328fb84593812374791f7659156cd851785b62e3c02cd6e8409bf71c`), including its single-line social image and public surface scope. This correction changes only the Web forced-colors status badge and toast CSS; approved visual and social asset hashes are unchanged.

## User Scenarios & Testing

### User Story 1 - Approve a distinct product identity (Priority: P1)

The owner reviews actual Full and Reduced production masters for a new abstract Local Companion mark, with proof at small sizes and on dark and light surfaces, before any derivative becomes official.

**Independent Test**: Present the exact source-bound Gate 1 packet and confirm that its source hashes, geometry, palette, renderer settings, and 32 proofs match the source subsequently used for generation.

**Acceptance Scenarios**:

1. Given the existing LC monogram and W placeholder, when the new mark is proposed, then neither is silently promoted as the official source.
2. Given a selected abstract direction, when the owner approves Gate 1, then the production Full and Reduced masters and all 32 proofs are bound to that exact approval.
3. Given a source or renderer change after approval, when the build runs, then stale approval blocks publication.

### User Story 2 - Receive a complete, usable kit (Priority: P1)

A brand or product implementer downloads Local Companion's brand kit and receives coherent marks, color roles, typography, platform assets, implementation bindings, guidance, and exact verification evidence.

**Independent Test**: Build the kit from committed source, run its geometry and full verification gates, and inspect the generated visual and manifest evidence without manually editing generated output.

**Acceptance Scenarios**:

1. Given approved source and both creative gates, when the kit is compiled, then every required role is present in its manifest and the measured checks report zero problems.
2. Given dark and light surfaces, when the palette is applied, then text and controls meet WCAG 2.1 AA and states have non-color cues.
3. Given a regenerated kit, when a consumer reads the contract, then exact source, brand, compiler, and asset identities are available.

### User Story 3 - Discover the official public brand (Priority: P1)

A visitor reaches Local Companion from the official brand catalog, sees accurate product positioning and approved identity, and can download the versioned kit and guidance.

**Independent Test**: Export the site from verified kits, inspect the Local Companion catalog card, routes, registry, download links, and public metadata, then verify the exact published release and live route.

**Acceptance Scenarios**:

1. Given a verified Local Companion kit, when the official site is built, then its public pages and downloads are projected from that kit.
2. Given a visitor to the public pages, when they inspect product material, then private companion content, chats, local paths, and unapproved screenshots are absent.
3. Given a release publication, when the Pages deployment completes, then the official subdomain serves the approved Local Companion identity and exact downloadable artifact.

### User Story 4 - Review assembled fundamentals (Priority: P1)

The owner reviews lockups, formal colors, separate interface cues, typography, representative applications, and a distinct social share image with exact copy before final compilation.

**Independent Test**: Validate the private Gate 2 packet against the current Gate 1 source digest and checksummed preview files, record the owner's decision, and reject drift.

**Acceptance Scenarios**:

1. Given Gate 1 approval, when provisional fundamentals are ready, then the private packet contains all required assets and measured evidence.
2. Given exact approved social copy, when the owner approves Gate 2, then the resulting social image binds its SVG and PNG digests.
3. Given a changed derivative or social line break, when verification runs, then Gate 2 must be renewed.

### Edge Cases

- A visually attractive concept is not production approval. Only the final vector source and proof matrix can pass Gate 1.
- No existing product screenshot is authorized for public use. A representative application may use clearly synthetic, nonprivate content.
- Existing Segoe UI Variable is a system font, not a redistributable local font; typography selection must not assume a license to bundle it.
- A hosted catalog entry without an exact release asset and checksum is incomplete for this request.
- Missing raster or PDF tooling must be reported as a named skip, and mandatory AA, glyph, source, and kit checks cannot be skipped.

## Requirements

### Functional Requirements

- **FR-001**: Declare Local Companion as ShruggieTech-owned with public showcase permission and independent palette inheritance; keep parentage, endorsement, and service credit explicit.
- **FR-002**: Build a new abstract Full and Reduced mark from governed source, without reusing the LC monogram, W placeholder, or companion character art as production geometry.
- **FR-003**: Obtain source-bound Gate 1 approval over masters, palette qualification, renderer configuration, geometry, and the 32 dark/light/black/white size proofs before generating publishable derivatives.
- **FR-004**: Provide formal identity colors and separate functional interface cues, including dark and light role pairs measured against WCAG 2.1 AA.
- **FR-005**: Define suitable local licensed typography for the portable kit and identify the existing app's Segoe UI Variable and Cascadia Mono stack as consumer context rather than silently claiming the same files are bundled.
- **FR-006**: Prepare a private Gate 2 packet with wide and stacked lockups, social share image and exact copy, palette, interface cues, typography, representative application, and derivative manifest; obtain owner approval before final compilation.
- **FR-007**: Generate and verify the complete kit, including platform assets, guidance, versioned consumer contract, manifest, and release archive, from committed source only.
- **FR-008**: Add Local Companion to the official site and release inventories, tests, publication audits, and deployment artifact coverage without weakening existing brand gates.
- **FR-009**: Keep private chats, character imagery, model artifacts, local file paths, and unapproved screenshots out of public assets and metadata.
- **FR-010**: Publish the approved versioned release and the exact verified site artifact so the official subdomain displays Local Companion after all required gates pass.

### Key Entities

- **Local Companion brand source**: Owner-approved affiliation, voice, palette, typography, mark source, and public permissions.
- **Canonical identity record**: Source hashes, renderer and proof evidence, and Gate 1 decision.
- **Gate 2 review packet**: Private checksummed derivative previews and exact social copy awaiting approval.
- **Verified kit**: Generated assets, bindings, guidance, manifest, and zero-problem reports.
- **Publication record**: Exact release and Pages artifact identity for the public site.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The owner explicitly approves the exact Gate 1 production source and Gate 2 assembled fundamentals; both approvals remain current after the final build.
- **SC-002**: Local Companion and all existing production kits report zero `verify.py` problems and zero `validate_glyph.py` failures.
- **SC-003**: Local Companion's public catalog, guidance, download, registry, and social routes resolve from the verified kit and expose no private product data.
- **SC-004**: The release archive and public download match their published SHA-256 checksums, and the live official subdomain serves the approved version.
- **SC-005**: No generated kit, site export, PDF, raster export, registry, or release archive is committed to Git.

## Assumptions and Boundaries

- The owner has authorized publication of the completed kit and site entry, subject to the two exact creative approvals and required release verification.
- The Local Companion application's existing local brand files are read-only source material for this slice. App integration or replacement of its installed icon is separate work.
- The current graphite and indigo values are a direction; any failing accessible role value may change to satisfy the non-exemptable AA floor.
- The owner approved the exact Full and Reduced calm-orbit production forms and their 32 proofs at Gate 1. Source changes that affect this binding require renewed approval.
