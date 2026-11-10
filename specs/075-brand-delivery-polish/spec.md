# Feature Specification: Brand Messaging and Delivery Polish

**Feature Branch**: `codex/075-brand-delivery-polish`

**Created**: 2026-11-09

**Status**: Locally verified, pre-push checkpoint (#352 blocked; publication pending)

**Input**: Owner kickoff: "Kick off S075 under autopilot. Target all three issues, and if Cloudflare access is blocked, finish the other two and report exactly what remains." Issues: [#328](https://github.com/shruggietech/shruggie-brand/issues/328), [#353](https://github.com/shruggietech/shruggie-brand/issues/353), and [#352](https://github.com/shruggietech/shruggie-brand/issues/352).

## User Scenarios & Testing

### User Story 1 - Read the brand message first (Priority: P1)

A reader opening a brand guide sees the identity, actual approved slogan and supporting description, with no prominent schema field names competing for attention.

**Why this priority**: The shared guide currently makes generic labels larger than the approved message in every production kit with cover messaging.

**Independent Test**: Compare Local Media Gallery cover proofs at A4 actual size and fit-to-page, then inspect representative light/dark and sparse/rich messaging examples.

**Acceptance Scenarios**:

1. **Given** an approved slogan, **when** the guide opens, **then** the actual slogan uses the 23pt display treatment and visible role keys are absent from the cover.
2. **Given** supporting descriptions, **when** the guide opens, **then** the short description uses readable body typography with measured AA contrast, and all approved cover text fits without truncation, clipping or overlap.
3. **Given** absent or unresolved messaging, **when** the guide opens, **then** no role labels, placeholders, orphan rules or invented copy appear.
4. **Given** altered wording, swapped roles, repeated roles or an unauthorized substitution, **when** output is checked, **then** validation rejects the mismatch while accepting a label-free cover.

### User Story 2 - Read the approved DanceWithMe865 description (Priority: P1)

A visitor sees `Learn to dance with Greg "Krucial" Carney.` on the desktop portfolio card, mobile portfolio panel and applicable generated short-description surfaces.

**Why this priority**: The owner has supplied the exact wording; no further creative decision is needed.

**Independent Test**: Compare the source approval record and generated output, then verify the exact sentence on desktop and mobile after publication.

**Acceptance Scenarios**:

1. **Given** the owner's November 9 approval, **when** messaging is recorded, **then** the approved short description preserves straight quotes, capitalization and final period, together with provenance and approval date.
2. **Given** the updated source, **when** brand outputs and the site are rebuilt, **then** the same approved sentence appears on applicable surfaces without changing independent social-image approvals or inventing other descriptions.

### User Story 3 - Reach the canonical site through its alias (Priority: P2)

A visitor opening `brands.shruggie.tech` reaches the matching path and query on `https://brand.shruggie.tech` through one permanent redirect.

**Why this priority**: The owner requests an automated alias without manual dashboard steps, independent of the messaging changes.

**Independent Test**: Request HTTP and HTTPS root/nested URLs with queries, inspect the permanent destination, repeat reconciliation, and verify the canonical site still works.

**Acceptance Scenarios**:

1. **Given** authenticated management access, **when** the alias is reconciled, **then** unrelated configuration is preserved and the alias redirects at the edge with valid TLS, preserved path/query and no loop or avoidable extra hop.
2. **Given** correct configuration, **when** reconciliation repeats, **then** no duplicate record or rule is created.
3. **Given** unavailable Cloudflare access, **when** the blocker is established, **then** the other two stories continue and the exact remaining provisioning and verification work is reported.

### Edge Cases

- Cover cases include dark-first/light-first brands, wrapping slogans, long description and introduction, slogan-only, description-only and no approved messages.
- Overlong content must flow into an explicitly identified continuation sheet with exact wording rather than shrink below the declared typography, truncate or overlap. Normal production messages remain on the first sheet.
- Useful role labels remain in reference sections; machine-readable roles remain on presentation elements. Opening surfaces are inventoried separately from reference sections.
- Existing alias DNS/rules may conflict or TLS may not yet cover the hostname; inspect before mutation and report partial state accurately.
- Publication remains incomplete until the matching tagged release and live Pages outputs are verified. A local commit does not close a live-publication acceptance criterion.

## Requirements

### Functional Requirements

- **FR-001**: Cover presentation MUST remove visible role keys and present the actual approved slogan at 23pt in the declared display face/available weight, with the identity as its overall anchor.
- **FR-002**: Short descriptions MUST use a declared 13-14pt body size, readable leading and measured AA contrast. Long descriptions and introductions MUST retain exact copy with a documented overflow treatment and no clipping or overlap of messages, logo, footer or page bounds.
- **FR-003**: Every output MUST preserve approved wording, role and intended-use authorization, with no promotion of absent/unresolved values, no role swaps, duplicate roles, legacy fallbacks or unauthorized substitutions. Label-free cover validation MUST preserve these guarantees.
- **FR-004**: The source approval for DanceWithMe865 MUST record the exact sentence, repository-owner provenance and approval date 2026-11-09, and project into applicable desktop/mobile and generated short-description surfaces.
- **FR-005**: The implementation MUST inventory all thirteen production kits across PDF, print HTML, portable and hosted openings, retain useful reference labels, and reconcile the superseded S067 cover-label contract and explanatory prose.
- **FR-006**: The alias MUST be reconciled automatically as an exact-host, permanent edge redirect to canonical HTTPS, preserving path/query with valid TLS. Its redirect-only DNS record MUST be proxied with automatic TTL and no real/private origin address.
- **FR-007**: Alias reconciliation MUST inspect conflicts, preserve unrelated records/rules, avoid duplicates on repeat execution and provide redacted before/after evidence and a rollback procedure. Credentials and private operational identifiers MUST remain outside source and evidence.
- **FR-008**: Unavailable Cloudflare access MUST be recorded as a blocker for #352 without blocking #328/#353; incomplete external operations MUST remain explicitly incomplete.
- **FR-009**: All production kits MUST pass the documented verifier, glyph and applicable layout gates; changed responsive surfaces MUST pass 200% text enlargement, 320 CSS-pixel reflow and WCAG 2.1 AA checks. Representative rendered proofs MUST receive visual review.
- **FR-010**: Source, specification, contracts, tests and verification evidence MUST remain synchronized, with generated outputs excluded from Git and UTF-8 without BOM/LF text checked for mojibake.
- **FR-011**: Release preparation MUST use the existing verified publication path and accurate version/migration metadata. Live issue completion requires successful reviewed publication and direct verification of the released outputs.

### Key Entities

- **Approved message**: Independent role, approval state, exact text, intended uses and provenance.
- **Cover projection**: Identity and authorized message elements, with explicit role semantics and measured presentation.
- **Alias configuration**: Exact source host, permanent destination policy, proxied DNS and redirect rule, with private management identity retained outside Git.
- **Verified candidate**: Source revision, generated kits/site, validation evidence and coordinated release metadata.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All thirteen production kits have inventoried opening surfaces and zero verifier problems, glyph failures and applicable PDF layout problems; representative cover proofs show the slogan as the prominent message without visible cover keys.
- **SC-002**: Exact-copy negative cases reject wording drift, wrong/duplicate roles and unauthorized substitutions, while approved label-free covers pass.
- **SC-003**: The exact approved DanceWithMe865 sentence is present on rebuilt desktop/mobile portfolio surfaces and applicable brand outputs, and subsequently verified on the published site before #353 is closed.
- **SC-004**: With management access, HTTP/HTTPS root/nested alias requests preserve path/query in one permanent hop, repeat reconciliation creates no duplicates, and the canonical site remains available; otherwise the exact external blocker and outstanding acceptance criteria are recorded.
- **SC-005**: Full documented validation and text/source hygiene checks pass before the autopilot local-commit checkpoint; live-publication evidence is required before claiming deployed completion.

## Clarifications

### Session 2026-11-09

- Q: Label-free cover or secondary labels? A: Use the owner's preferred label-free cover, preserving role semantics and reference labels; the current 23pt treatment belongs to the slogan.
- Q: How should unusually rich copy fit? A: Keep declared readable sizes and use a clearly identified continuation sheet only when measured content cannot fit the opening sheet; do not truncate or silently shrink approved messages.
- Q: Does missing Cloudflare access block the slice? A: No. The owner explicitly requests completion of the other two issues with an exact remaining-work report.
- Q: Does kickoff authorize publication? A: Follow the usual autopilot pre-push halt. Prepare the complete verified candidate locally, then require explicit push/publication authorization before remote publication.

## Assumptions

- No identity geometry, palette, font-family, social-image composition or unapproved copy changes are requested.
- The current feature-branch model and standard autopilot protocol apply. The next coordinated patch release is provisionally v3.1.2, subject to release-contract verification.
- Cloudflare management access is an environmental dependency to investigate early, not an invented prerequisite for the messaging fixes.
