# Feature Specification: Identity-Locked I Heart PR Tours Brand Guide

**Feature Branch**: `codex/028-i-heart-pr-tours-brand-guide`

**Created**: 2026-09-10

**Status**: Gate 2 candidate `iheartpr-g2-r4` approved; owner-corrected complete public website publication in progress

**Input**: User description: "Deliver issue #188 as S028: ingest the existing I Heart PR Tours identity without redesign, establish exact source authority and typography under a first owner gate, generate the current-spec guide and kit under S027 continuity protection, halt at a second owner gate before publication, then publish an official pull request and reconcile no more than two Codex review rounds."

## Clarifications

### Session 2026-09-10

- No critical ambiguity required an operator question before planning. Issue #188 already fixes the identity relationship, source-preservation rule, two approval gates, privacy boundary, accessibility floor, and publication workflow.
- The operator-supplied identity package is higher authority than current website styling or downloaded website assets. Website evidence may inform voice and use context only.
- Public eligibility, registry inclusion, hosted-guide inclusion, and service credit remain disabled unless the operator explicitly approves their exact values at Gate 1 and the resulting surfaces at Gate 2.
- Contract, registration, and other business documents colocated with intake material are outside the identity-source scope and must not be opened, copied, summarized, or committed.

### Session 2026-09-11

- The owner rejected Gate 2 candidate `iheartpr-g2-r1`. Requested changes to copy, palette, surface mode, and transformation scope invalidate the affected `iheartpr-g1-r2` approval under FR-018 and return S028 to Gate 1.
- The exact slogan is `Experience Puerto Rico`. The exact description is `Thoughtfully guided tours on the island we love.`
- The live client website is authoritative contextual evidence for the red action color and blue support family. The two owner-supplied brochure masters are reference evidence for brand voice, usage hierarchy, photography, and an occasional earth-brown support role.
- The guide must be light-first and resemble a white-paper document. Repository-wide generator and hosted-site gaps discovered by this requirement are tracked in issues #193 and #194 without expanding S028 beyond the client-specific implementation needed for Gate 2.
- A deterministic, knockout-aware single-ink transform is eligible for explicit Gate 1 approval. It derives black and white variants from unchanged approved light-background artwork, suppresses the source raster shadow, preserves intentional white negative space, and performs no tracing or geometry reconstruction.
- Live-site verification confirms that the website declares one 32 × 32 colored-heart PNG for favicon, nominal 192 × 192 favicon, and Apple touch roles. Its pixels match the supplied package's `favicon-32x32.png` within 0.68 mean RGB levels after white compositing, while the rejected Gate 2 generated favicon differs by 37.74. Revised Gate 1 therefore promotes the supplied favicon family as exact per-size authority and reserves the colored `heart.svg` for missing modern app sizes with framing measured from supplied platform masters.
- The owner requested one focused revision to Gate 2 candidate `iheartpr-g2-r2`: section labels and table row or column headings must use the supplied Poppins and Source Sans 3 families instead of preformatted Courier Prime styling. Live-site measurement confirms Poppins Bold for primary headings, Source Sans Pro for supporting copy, near-black `#111111` for most headings, and blue `#1C5B8D` for occasional uppercase eyebrow labels. Courier Prime remains reserved for genuine code-like values and identifiers.
- Candidate `iheartpr-g2-r3` exposed four remaining corrections. Footer text and page numbers, cover metadata, and all other small semantic text must use the supplied body family rather than Courier Prime. The footer's left side must read exactly `I Heart PR Tours | Brand System`. Courier Prime is permitted only inside the literal command block, retaining its current weight. `IHPRT` is an approved casual shorthand in general prose after the full company name is established, but is not a substitute identity mark. The first two page-3 previews must render their dark-surface source assets on dark preview wells so their white lettering remains visible and centered.
- After the first merge-readiness handoff, the owner corrected the agent's private-publication assumption: every brand built with the ShruggieTech brand skill must be proudly displayed on the public brand website without exception. This explicitly authorizes the complete website surface set for I Heart PR Tours and supersedes every prior zero-public-surface statement. Release tags and unrelated external services remain outside S028.

## User Scenarios & Testing

### User Story 1 - Approve exact source authority (Priority: P1)

As the identity owner, I can review a complete private inventory of supplied brand files, visual role groupings, palette measurements, font evidence, and proposed transformations before any source is committed or derivative identity asset is generated.

**Why this priority**: Every later artifact depends on a truthful source hierarchy. A convenient but unauthorized source choice would reproduce the identity-drift failure that S027 was built to prevent.

**Independent Test**: Review a private Gate 1 packet and verify that every in-scope intake file has a hash, preview, proposed role, authority rank, and disposition; every font and transformation is explicit; unrelated private files are absent; and no production brand source or derivative has been committed.

**Acceptance Scenarios**:

1. **Given** the operator-supplied package, **When** S028 inventories it, **Then** 100 percent of in-scope files are hash-recorded before ingestion and all unrelated colocated documents remain unread and excluded.
2. **Given** multiple representations of the same mark, **When** source authority is proposed, **Then** each role names one exact preferred source and explains the treatment of every lower-authority reference without altering any file.
3. **Given** palette and typography claims in the supplied guide, **When** Gate 1 is prepared, **Then** claims are measured or verified independently and any ambiguity is presented as an owner decision rather than silently resolved.
4. **Given** required current-kit deliverables, **When** transformation boundaries are proposed, **Then** every allowed operation and every deliverable requiring creative reconstruction is listed separately.
5. **Given** a complete Gate 1 packet, **When** the operator revises or rejects any element, **Then** no approval is inferred and the packet remains blocked until one exact revision receives explicit approval.

---

### User Story 2 - Preserve and bind the approved identity (Priority: P1)

As the identity owner, I can rely on approved artwork entering the repository byte for byte and on every permitted derivative remaining traceable to its exact source, transformation, renderer, framing, and comparison evidence.

**Why this priority**: Faithful source promotion and fail-closed continuity are the core safeguards against post-approval reconstruction or accidental normalization.

**Independent Test**: Promote an approved synthetic intake through the same contract and prove exact source-byte equality, deterministic derivative traceability, rejection of stale approval or source drift, and rollback on partial failure.

**Acceptance Scenarios**:

1. **Given** approved source hashes and a transformation contract, **When** source promotion occurs, **Then** every promoted identity file is byte-identical to its approved input.
2. **Given** a proposed transformation that changes geometry, lettering, framing, crop, proportions, color placement, negative space, or apparent scale, **When** validation runs, **Then** promotion and derivative generation stop before mutation.
3. **Given** any source, approval, renderer, transformation, or proof hash drift, **When** the brand is built or verified, **Then** the affected approval is stale and the process returns to Gate 1.
4. **Given** a missing current-kit variant, **When** it cannot be made through an approved non-creative transformation, **Then** it is reported as unavailable rather than invented.

---

### User Story 3 - Review the complete guide and delivery (Priority: P2)

As the identity owner, I can review a complete current-spec brand guide, source-governed asset catalog, implementation system, and representative visual evidence before any public surface is enabled.

**Why this priority**: The complete system must be judged as a coherent delivery, not inferred from isolated source files or partial previews.

**Independent Test**: Build the approved private kit and inspect the rendered guide, asset catalog, typography specimens, accessible examples, implementation artifacts, multi-size comparisons, and verification reports while all public surfaces remain disabled.

**Acceptance Scenarios**:

1. **Given** exact Gate 1 approval, **When** the kit is generated, **Then** it contains every applicable current-spec source contract, guide, catalog, token, style, component, framework binding, enforcement record, specimen, platform asset, and verification record without unauthorized identity invention.
2. **Given** fixed identity colors, **When** accessibility validation finds a text-role failure, **Then** the color is preserved and constrained to a suitable non-text or large-treatment role while accessible semantic roles are supplied separately.
3. **Given** the complete Gate 2 packet, **When** the operator reviews it, **Then** representative 256, 64, 32, and 16 pixel outputs on approved light and dark surfaces are traceable to the Gate 1 contract and comparison evidence.
4. **Given** a Gate 2 change request affecting source, geometry, framing, color, typography, copy, or transformation, **When** the request is accepted, **Then** the affected approval is invalidated and work returns to Gate 1.

---

### User Story 4 - Publish the approved brand on the website (Priority: P3)

As the repository owner, I can receive a reviewable pull request with complete validation and third-party review reconciliation that publishes I Heart PR Tours across the same complete governed website surface set as every other brand.

**Why this priority**: Public website presentation is a required outcome for every brand built with the skill. Third-party ownership affects claims and notices, not eligibility for the portfolio.

**Independent Test**: Inspect the final pull request and generated site to confirm issue traceability, green CI, resolved review threads, no more than two Codex rounds, clean source/artifact boundaries, and complete I Heart PR Tours showcase, guideline, download, registry, metadata, structured-data, and social-preview routes.

**Acceptance Scenarios**:

1. **Given** Gate 2 approval, **When** S028 is committed and pushed, **Then** the official pull request closes #188 and contains the required identity, accessibility, documentation, and validation ledger.
2. **Given** automated review feedback, **When** a finding is valid, **Then** it is fixed and answered without silently changing approved identity values; identity-affecting changes reopen the appropriate human gate.
3. **Given** all reviews are satisfied and exact-head CI is green, **When** the PR becomes mergeable, **Then** S028 halts and asks the owner to perform the final review and merge ritual.

### Edge Cases

- A supplied PDF contains flattened artwork but no separable vector master. Treat it as a rendered authority or reference according to Gate 1, never as permission to trace it.
- Two supplied files appear visually identical but have different bytes, dimensions, metadata, crops, or embedded color definitions. Inventory both and ask the owner to approve the role hierarchy.
- A guide names a font imprecisely or conflicts with internal font metadata. Do not ingest a substitute; expose the exact ambiguity at Gate 1.
- A named font is proprietary, lacks redistribution permission, or is unavailable offline. Do not purchase, download, imitate, or commit it; propose a delivery-safe role boundary for approval.
- The guide's printed or sampled color differs from a source asset. Record both measurements and authority implications rather than averaging or normalizing them.
- A fixed customer color cannot meet AA for ordinary text. Preserve the identity value and prohibit that use while providing an accessible semantic alternative.
- The public website changes during the slice. Record retrieval time and use it only as non-authoritative voice and context evidence.
- A generated logo appears clipped or differently scaled because the current generator assumes another framing convention. Adapt the generator only through a declared non-creative transformation; never change the source.
- A review bot proposes simplifying or redrawing imported paths. Reject the identity change unless the operator explicitly reopens Gate 1.
- An intake directory contains contracts, registrations, personal data, credentials, or unrelated customer records. Exclude them from discovery, evidence, copying, and publication.

## Requirements

### Functional Requirements

- **FR-001**: S028 MUST trace issue #188, S027 issue #185, authoritative-logo issue #151, light-theme issue #193, custom-assets issue #194, and synchronized baseline revision `435019dbc37e754fd1f0b16228a576c985e9468a`.
- **FR-002**: Before repository ingestion, S028 MUST privately inventory and hash every in-scope operator-supplied identity, font, guide, favicon, and reference file while excluding unrelated colocated material.
- **FR-003**: The intake inventory MUST record original filename, media type, byte length, SHA-256, dimensions or page count where applicable, embedded metadata where applicable, proposed role, authority rank, and disposition.
- **FR-004**: S028 MUST preserve every imported identity source byte for byte and MUST NOT redraw, recreate, trace, vectorize, simplify, normalize, optimize, crop, reframe, or replace its geometry or lettering. Re-keying or recoloring is permitted only through a separately approved deterministic transformation that leaves the source unchanged.
- **FR-005**: S028 MUST establish a per-role authority hierarchy among every supplied vector, raster, PDF, favicon, and brand-guide reference without silently preferring a convenient representation.
- **FR-006**: Website content from `https://iheartprtours.com` MAY inform current voice, audience, and use context but MUST NOT override the operator-supplied identity package or authorize downloaded website assets.
- **FR-007**: Gate 1 MUST present a complete private source inventory, grouped contact sheets, authority hierarchy, palette measurements, font identity and licensing evidence, every proposed transformation, unavailable deliverables, and proposed affiliation, privacy, service-credit, and publication values.
- **FR-008**: Gate 1 approval MUST bind exact source hashes, font records, transformation boundaries, affiliation values, privacy values, publication values, displayed evidence, owner wording, approved scope, and timestamp.
- **FR-009**: Before Gate 1 approval, S028 MUST NOT commit production brand source, promote intake bytes, generate derivative identity assets, enable public surfaces, or infer approval from silence or revision requests.
- **FR-010**: I Heart PR Tours MUST be modeled as an independent third-party customer with no ShruggieTech ownership, parentage, identity authorship, endorsement, maintenance, or warranty claim.
- **FR-011**: Every brand built with the skill MUST be eligible for and included in the public brand website after Gate 2 approval. Service credit, release tags, deployment to unrelated services, and other non-website publication scopes MUST remain disabled unless the operator explicitly approves their exact values.
- **FR-012**: Font evidence MUST bind claimed family, subfamily, version, internal names, weight, style, format, source provenance, license, redistribution rights, and offline-delivery disposition before inclusion.
- **FR-013**: Each permitted derivative MUST bind an approved source hash, output role, deterministic transformation recipe, renderer identity and version, output dimensions, framing behavior, and reviewable comparison evidence.
- **FR-014**: S028 MUST NOT invent a monochrome, reduced, outlined, wordmark-only, platform, or other missing identity variant. A missing family MAY be generated only through an exact non-creative Gate 1 transformation approved by the owner; otherwise it MUST be listed for owner disposition.
- **FR-015**: The S027 continuity lifecycle MUST reject stale approval and source, geometry, topology, framing, palette, typography, renderer, transformation, proof, or generated-report drift before publication.
- **FR-016**: After Gate 1 approval, S028 MUST generate the complete applicable current-spec kit and guide while preserving the approved source and transformation contract.
- **FR-017**: Gate 2 MUST present the rendered guide, asset catalog, representative source-to-output comparisons, 256/64/32/16 pixel light/dark proofs, typography specimens, accessible color examples, implementation artifacts, and full verification results.
- **FR-018**: A Gate 2 change to source, geometry, framing, color, typography, copy, or transformation MUST invalidate the affected approval and return work to Gate 1.
- **FR-019**: Every ordinary-text, large-text, interface, declared fill, state, and focus role MUST meet WCAG 2.1 AA without waivers; fixed failing identity colors MUST be preserved and role-constrained rather than silently altered.
- **FR-020**: Approved source-only definitions MUST live under `brands/i-heart-pr-tours/`; approved redistributable shared fonts MAY live under `assets/fonts/`; generated kits, PDFs, rasters, registries, site exports, archives, and review packets MUST remain ignored.
- **FR-021**: `verify.py` MUST report zero problems and `validate_glyph.py` MUST report zero failures for every applicable production asset without modifying imported identity sources to satisfy either validator.
- **FR-022**: Tests MUST cover source-byte equality, authority and transformation completeness, stale approvals, unsafe paths, private-file exclusion, third-party affiliation, complete website publication, accessibility, deterministic derivatives, rollback, and representative identity continuity.
- **FR-023**: The full repository validation MUST pass with UTF-8 without BOM, LF line endings, no mojibake, no private workstation paths, and no tracked generated artifacts.
- **FR-024**: After Gate 2 approval, the authorized workflow MUST push an official pull request closing #188, process every review finding, request at most one second Codex round, and halt before merge once exact-head CI and review state are green.
- **FR-025**: S028 MUST NOT read, copy, summarize, hash into public evidence, or commit unrelated contracts, registrations, credentials, personal records, or other private files encountered near the approved intake sources.
- **FR-026**: Every guide and review surface MUST use the exact slogan `Experience Puerto Rico` and description `Thoughtfully guided tours on the island we love.` where those fields appear.
- **FR-027**: The semantic palette MUST use live-site action red `#C5342C`, frequent support blue `#1C5B8D`, light blue support values `#68A9DD` and `#A1CFF4`, and brochure-derived occasional earth brown `#5D4A46`, with role restrictions based on measured WCAG contrast.
- **FR-028**: The I Heart PR Tours guide MUST be a light-first, white-paper presentation with white as the primary surface, dark ink for ordinary text, and dark-surface examples confined to bounded demonstrations.
- **FR-029**: If approved at revised Gate 1, black and white single-ink variants MUST derive from an unchanged approved light-background master through the exact alpha-floor, white-knockout, recolor, and antialias recipe in candidate `iheartpr-g1-r4`; proof drift MUST invalidate approval.
- **FR-030**: The I Heart PR Tours guide MUST include an optional `Expressions and atmosphere` section containing the supplied vertical and horizontal sandy treatments as promotional compositions, not primary identity replacements.
- **FR-031**: S028 MUST record the reusable light-theme and optional custom-asset system gaps in dedicated GitHub issues while keeping their cross-brand implementation outside this slice.
- **FR-032**: Favicons and app icons MUST use the colored heart. Exact supplied favicon or platform targets MUST be copied byte for byte where available; missing modern sizes MUST derive from unchanged `heart.svg` with source-shadow suppression and safe-area framing measured from supplied 192 and 310 pixel platform masters. Monochrome substitution is prohibited for these roles.

### Key Entities

- **Intake File**: An operator-supplied file considered for identity, font, guide, favicon, or contextual reference use, with private origin and measured metadata.
- **Source Authority Decision**: The Gate 1 selection of one exact source for one role, including lower-authority references and conflict disposition.
- **Transformation Contract**: An exhaustive list of non-creative operations permitted for one source-to-output relationship.
- **Font Evidence Record**: The verified identity, metadata, provenance, licensing, redistribution, and delivery status of a typeface candidate.
- **Gate 1 Approval**: The owner's hash-bound authorization of source authority, fonts, transformations, affiliation, privacy, and publication classification.
- **Derived Asset Record**: Traceability from an approved source through one deterministic transformation and renderer to one output role and proof set.
- **Gate 2 Approval**: The owner's approval of the complete generated guide, kit, and exact allowed public surfaces.
- **Publication Classification**: Closed values controlling public eligibility, showcase, registry, hosted guide, service credit, release, and deployment.

## Success Criteria

### Measurable Outcomes

- **SC-001**: One private Gate 1 inventory accounts for 100 percent of in-scope supplied files and zero unrelated private files, with no unclassified candidate.
- **SC-002**: Every approved imported identity source has byte-for-byte equality between intake, staged promotion, committed source, and final build input.
- **SC-003**: Gate 1 contains 100 percent of required source, hierarchy, palette, font, transformation, affiliation, privacy, publication, evidence, and owner-binding fields.
- **SC-004**: Every generated identity asset has exactly one approved source relationship and one complete deterministic transformation record; zero outputs depend on reconstructed or unapproved geometry.
- **SC-005**: All applicable 256, 64, 32, and 16 pixel proof coordinates preserve approved framing, topology, color placement, and legibility on approved light and dark surfaces.
- **SC-006**: Every applicable accessibility role passes WCAG 2.1 AA with zero waivers and zero unauthorized changes to fixed identity colors.
- **SC-007**: Gate 2 presents 100 percent of applicable current-spec deliverables and explicitly accounts for every inapplicable or owner-blocked deliverable.
- **SC-008**: Production verification reports zero problems, applicable glyph validation reports zero failures, and full repository CI is green on the exact pull-request head.
- **SC-009**: Public discovery exposes zero I Heart PR Tours surfaces before Gate 2 approval and only the exact surfaces approved afterward.
- **SC-010**: Every automated review comment receives a response and disposition, zero review threads remain unresolved, no more than two Codex review rounds occur, and the workflow halts before merge.

## Assumptions

- The supplied brand guide is a contextual and identity reference whose internal artwork authority must be explicitly ranked at Gate 1; it is not automatically a separable vector master.
- The operator-supplied ZIP is the complete known identity package. Its SVG family supplies exact vertical, horizontal, heart, and sand-treatment sources; no standalone wordmark-only or monochrome source exists in that package.
- S027's merged continuity machinery is available and is the mandatory approval, promotion, proof, and drift foundation for S028.
- The repository's existing independent-third-party affiliation model is suitable unless the Gate 1 evidence exposes a customer-specific gap.
- Public website publication through the complete governed surface set is mandatory after Gate 2. Release tags and deployment to unrelated external services remain separate decisions.

## Scope Boundaries

### In scope

- Private inventory and source-authority analysis of operator-supplied brand inputs.
- Faithful source promotion after Gate 1.
- Current-spec I Heart PR Tours source contract, generated kit, guide, and verification evidence after Gate 1.
- Narrow generator or verifier corrections required to preserve imported-source fidelity and fail closed.
- Official pull request and bounded automated review reconciliation after Gate 2.

### Out of scope

- Redesigning, recreating, tracing, or modernizing the I Heart PR Tours identity.
- Altering the customer website, booking system, tours, prices, or business content.
- Reading or publishing contracts, registrations, personal records, credentials, or unrelated customer material.
- Purchasing font licenses or substituting visually similar fonts without approval.
- Claiming ShruggieTech ownership, authorship, endorsement, maintenance, or warranty.
- Release tags, deployment to unrelated external services, or publication beyond the approved brand website without explicit authority.
