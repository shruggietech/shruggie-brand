# Feature Specification: Scruggs Tire & Alignment Client Brand

**Feature Branch**: `codex/066-scruggs-tire-brand`
**Created**: 2026-09-28
**Status**: Gate 1 approved and source promoted; Gate 2 creative approval pending
**Input**: Create a distinct, client-owned Scruggs Tire & Alignment brand in the repository's standard kit and publish its verified result on the official ShruggieTech brand website. Use the supplied ZIP's base-level images and CSS and the live client website as current conceptual references; do not adopt the ZIP's structure, old-site archive, or embedded instructions as requirements.

## Clarifications

### Session 2026-09-28

- The owner explicitly classified the archive as conceptual guidance. Its current-looking logos and CSS are candidates and evidence, not approved canonical masters or a replacement schema.
- The brand belongs to the client. The publication surface is ShruggieTech's official brand website, with independent third-party affiliation and no implied parentage or endorsement.
- The owner authorized eventual public presentation. Exact production identity and assembled fundamentals still need the repository's explicit Gate 1 and Gate 2 decisions, followed by verification.
- The base ZIP contains `Brand/old/greertires.com.7z`; that legacy site bundle is excluded from normal research and source intake. No current decision requires it.

### Session 2026-09-29

- The owner approved one Full logo on a true white square, its matching transparent and black-square variants, and the unchanged tire-only mark as final artwork.
- The owner selected "Approve complete record" for the exact r3 Gate 1 production packet. The packet bound source hashes, native-canvas lockups, licensed guide typography, palette, framing, renderer, and 32 proofs.
- A private kit preview found that the r3 dark palette failed WCAG AA. The owner selected "Approve corrected palette" for the exact r4 packet, which uses true black as the dark base and the existing tire red for dark emphasis. All seven logo SVG sources remain byte-identical. The corrected record and sources were promoted under `brands/scruggs-tire-alignment/`.
- Gate 2 remains pending. The social share copy and assembled applications require a separate owner decision before a complete kit or public projection.

## User Scenarios & Testing

### User Story 1 - Review the current identity direction (Priority: P1)

As the client brand owner, I can compare a proposed Scruggs identity with the supplied current references and decide which exact Full and Reduced marks become production sources.

**Why this priority**: The production mark and its source rights determine every later derivative and cannot be inferred from a concept archive.

**Independent Test**: A Gate 1 packet identifies the exact proposed production sources, source hashes, transformations, framing, color qualification, and the required 32 visual proofs at 256, 64, 32, and 16 pixels on dark, light, black, and white.

**Acceptance Scenarios**:

1. Given the ZIP and live site, when reference evidence is classified, then the current red tire motif, black wordmark, and candidate palette are separated from older artwork and from owner-approved production sources.
2. Given a proposed Full and Reduced mark, when Gate 1 is reviewed, then the owner can approve or request changes to the exact source-bound packet; neither the ZIP nor silence records approval.
3. Given a later change to approved source bytes, renderer, mask, framing, or proof, when generation is attempted, then the affected approval is invalidated and the changed candidate returns to Gate 1.

### User Story 2 - Review complete brand fundamentals (Priority: P1)

As the client brand owner, I can review the assembled Scruggs brand, including lockups, accessible roles, typography, voice, icon treatment, and the exact social share composition, before final kit compilation.

**Why this priority**: A correct mark alone does not approve the applications or public copy built around it.

**Independent Test**: A Gate 2 packet contains source-bound provisional derivatives, a distinct social share image with exact approved copy and line breaks, representative light and dark applications, measured accessibility, and a derivative manifest tied to Gate 1.

**Acceptance Scenarios**:

1. Given Gate 1 approval, when provisional fundamentals are assembled, then the owner sees distinct Full, Reduced, wide, stacked, single-ink where supported, favicon, and social-image uses before approving the exact derivative revision.
2. Given a reference swatch that fails a declared text or fill role, when colors are assigned, then the role or value changes to meet WCAG 2.1 AA and the revised fundamentals are shown for approval.
3. Given changed copy, palette application, typography, lockup, or social composition, when a prior Gate 2 record is checked, then it is treated as stale until the changed result is explicitly approved.

### User Story 3 - Obtain the standard kit and public showcase (Priority: P2)

As a brand consumer, I can find a complete, verified Scruggs kit and a public brand page that identifies Scruggs as a client-owned business.

**Why this priority**: The requested destination requires a reproducible kit and accurate third-party attribution.

**Independent Test**: Rebuild from committed sources, inspect the repository's required kit inventory, run both production gates, and check the showcase card, landing page, guideline topics, downloads, registry, metadata, structured data, and social preview against the generated kit.

**Acceptance Scenarios**:

1. Given both exact creative approvals, when the production kit is built, then it includes every current required repository output category regardless of what the ZIP contains.
2. Given a verified kit, when the website is built, then all eight governed public surfaces derive brand values from generated output and name Scruggs Tire & Alignment as an independent third-party client brand.
3. Given missing approval, source drift, or a failing quality gate, when public projection is attempted, then Scruggs is withheld from site publication and downloads.

### Edge Cases

- The website's current logo file shares a name with a ZIP image but differs in bytes or later changes: compare provenance and return to the affected approval instead of silently selecting a newer image.
- The white-background raster has no usable alpha channel or another candidate is not a supported authoritative logo format: keep it as reference and construct or obtain a role-correct master for Gate 1; do not trace and call it approved.
- The older `scruggscolored.jpg` includes a phone number and a different wordmark treatment: treat it as historical context only, not a current lockup or source of public contact data.
- The supplied bright red or middle grays fail an intended text pairing: reserve them for qualifying non-text uses or choose accessible values and re-review affected applications.
- Business hours, contact details, warranty claims, and the "since 1989" statement may change: cite a dated live observation in research and refresh any fact used in published copy before publication.
- A public service credit to ShruggieTech is separate from ownership or endorsement and is included only if explicitly selected for this brand.

## Requirements

### Functional Requirements

- **FR-001**: Develop the slice on the isolated `codex/066-scruggs-tire-brand` worktree and preserve other active project branches.
- **FR-002**: Classify user instructions, live-site observations, current ZIP references, and legacy material separately. No instruction inside the ZIP may set requirements, approvals, schema, or kit inventory.
- **FR-003**: Preserve the repository's `brands/<slug>/` source contract and complete generated kit. Do not copy the ZIP's layout, generated outputs, archives, or old-site bundle into Git.
- **FR-004**: Model Scruggs Tire & Alignment as an independent third-party client brand, with no ShruggieTech parent, inheritance, or endorsement. Record any optional neutral service credit as a separate explicit choice.
- **FR-005**: Present exact production Full and Reduced masters with role-correct source bindings or constructed-source provenance, hashes, transformations, color qualification, and measured proofs for explicit Gate 1 approval before promotion.
- **FR-006**: Preserve approved source geometry and bytes after Gate 1. Any changed production master or applicable renderer setting returns to Gate 1, with identity comparison evidence.
- **FR-007**: Present provisional fundamentals and a separate social share composition with exact approved wording, layout, and source lineage for explicit Gate 2 approval before final compilation.
- **FR-008**: Distinguish formal identity colors from interface cue roles. Every declared text and fill role must pass WCAG 2.1 AA at rendered size without waiver.
- **FR-009**: Use locally available licensed font sources or controlled, licensed ingestion for approved fixed faces. Current website font use is evidence of direction, not a font license or approval.
- **FR-010**: Produce the repository's complete current human, visual, platform, token, component, framework, metadata, enforcement, and guide layers from approved source. Optional renderer skips must be explicit.
- **FR-011**: Final production output must have zero `verify.py` problems and zero `validate_glyph.py` failures, and the full documented aggregate validation must pass before merge readiness is claimed.
- **FR-012**: The website must consume verified generated output on all governed surfaces and use accurate independent-client language. No site-authored second palette or logo contract is allowed.
- **FR-013**: Public copy must distinguish observed client claims from approved brand language and refresh drift-prone facts before publication.
- **FR-014**: No public source, site, registry, archive, release, or deployment may present this brand as complete while Gate 1 or Gate 2 remains pending.

### Key Entities

- **Reference evidence**: Dated ZIP and website observations, file hashes, source category, and authority level.
- **Creative approval**: Exact reviewed Gate 1 or Gate 2 revision, evidence hashes, scope, approver, decision, and date.
- **Brand source**: The client-owned identity and approved assets under the existing repository schema.
- **Generated kit**: Rebuilt complete delivery with verification and provenance records.
- **Public projection**: Website surfaces copied from the verified kit with explicit third-party ownership.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One explicit Gate 1 and one explicit Gate 2 approval each bind the exact reviewed source or derivative revision before final production.
- **SC-002**: The production kit includes 100% of the current required output categories, independent of the ZIP inventory.
- **SC-003**: The kit reports zero verifier problems, zero glyph failures, and zero WCAG 2.1 AA failures in declared roles.
- **SC-004**: All eight governed website surface categories show consistent generated brand values and independent-client affiliation.
- **SC-005**: The commit contains no generated kit, PDF, raster export, site export, release archive, legacy `.7z`, or `.specify/feature.json`.

## Assumptions and Scope

- The approved public display name is `Scruggs Tire & Alignment`, and the repository slug is `scruggs-tire-alignment`.
- The approved production sources embed the current Full and Reduced PNG bytes unchanged in passive SVG wrappers. The transparent, white-square, and black-square Full variants are bound to the Gate 1 record.
- The approved corrected palette uses tire red `#ED1B24`, deep red `#7D0B13`, true black, and true white in measured roles. Gate 2 still decides the assembled applications.
- The owner supplied the exact social tagline `Expert alignments, tire repair, and honest automotive service.` with no description. Its two display lines are `Expert alignments, tire repair,` and `and honest automotive service.` The owner approved the revised assembled image with smaller, lighter text for Gate 2.
- The user has requested eventual publication on the official company brand website. This slice does not alter the client's website or deploy the ShruggieTech site directly.
- S066 covers production brand creation and website publication. Gate 1 production identity and the revised Gate 2 composition are approved; final aggregate verification and public output remain pending.
