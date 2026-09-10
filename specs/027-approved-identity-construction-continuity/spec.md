# Feature Specification: Approved Identity Construction Continuity

**Feature Branch**: `codex/027-approved-identity-construction-continuity`

**Created**: 2026-09-09

**Status**: Draft

**Input**: User description: "Deliver GitHub issue #185 as S027. Permanently prevent approved identity drift by separating exploratory direction selection from canonical-master approval, binding approval to the exact production source and rendering contract, failing closed on later drift, qualifying palettes before approval, retaining reviewable visual comparison evidence, and auditing existing constructed brands without changing their approved geometry. Push and open the official pull request automatically, process no more than two Codex review rounds, and halt for the owner merge ritual only after reviews and CI are satisfied."

## Clarifications

### Session 2026-09-09

- Q: Does S027 reopen or redesign the merged Cueson identity? -> A: No. Cueson remains unchanged and serves as the primary regression case for the repository-wide continuity contract.
- Q: How should existing brands without complete historical approval bundles migrate? -> A: Record current authoritative facts and evidence limits without fabricating retrospective approval, changing public eligibility, or altering identity source.
- Q: Are the preliminary perceptual thresholds in issue #185 binding? -> A: No. Exact structural invariants are binding, while cross-renderer perceptual thresholds must be calibrated during research against known-equivalent and known-divergent fixtures.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Approve the exact production identity (Priority: P1)

As an identity owner, I can first select a promising creative direction and later approve the exact canonical master rendered through its production path, so my approval cannot be mistaken for permission to reconstruct the design afterward.

**Why this priority**: The recurring failure begins when an exploratory rendering is treated as final approval even though production construction has not happened. A truthful approval boundary is the foundation for every other protection.

**Independent Test**: Run a constructed-identity approval exercise from exploration through canonical approval and verify that direction selection remains nonbinding, canonical approval is unavailable until the complete production-rendered evidence exists, and the recorded approval identifies the exact full and reduced masters, palette, framing, topology, rendering configuration, and proof set.

**Acceptance Scenarios**:

1. **Given** several exploratory concepts, **When** the owner chooses one for refinement, **Then** the decision is recorded as direction selection and does not authorize production derivatives or publication.
2. **Given** a selected direction, **When** the candidate is prepared for final identity approval, **Then** every required conversion and construction decision has already occurred and the displayed proofs come from the exact provisional production source.
3. **Given** complete canonical evidence, **When** the owner approves the identity, **Then** the decision binds the exact full and reduced masters, palette, framing, topology, renderer configuration, proof hashes, owner wording, and timestamp.
4. **Given** incomplete or internally inconsistent evidence, **When** canonical approval is attempted, **Then** approval is rejected before any derivative or public work begins.

---

### User Story 2 - Promote and verify without reconstruction (Priority: P1)

As a brand maintainer, I can promote an approved provisional master into permanent brand source without translating or redrawing it, and subsequent generation fails if any governed identity property drifts.

**Why this priority**: Approval is only trustworthy if the exact approved source crosses into production unchanged and remains mechanically bound to later output.

**Independent Test**: Approve a provisional constructed master, promote it, and verify byte-for-byte source continuity and complete contract equality. Then independently alter the construction method, path data, role mapping, framing, topology, palette, or governed proof and confirm that each drift case fails before derivative generation.

**Acceptance Scenarios**:

1. **Given** an approved provisional source and approval bundle, **When** promotion runs, **Then** the permanent source and configuration are copied without reconstruction and retain their approved hashes.
2. **Given** an approved identity, **When** production generation begins, **Then** source, method, geometry, topology, framing, palette, and proof values are checked against the approval bundle before derivatives are emitted.
3. **Given** any governed value differs, **When** verification runs, **Then** generation fails closed, identifies the exact mismatch, and returns the identity to canonical approval.
4. **Given** a constructed identity, **When** its source is audited, **Then** its construction provenance is explicit and any unapproved parallel geometry vocabulary is rejected.

---

### User Story 3 - Judge visual and color continuity before approval (Priority: P2)

As an identity owner or reviewer, I can inspect deterministic multi-size and multi-surface comparisons plus qualified color evidence before approving a canonical master, so low-resolution geometric artifacts, framing changes, topology changes, and palette conflicts are visible at the correct lifecycle point.

**Why this priority**: Source hashes alone cannot communicate perceptual continuity, and accessible colors selected too late create avoidable rework.

**Independent Test**: Generate an approval packet for full and reduced masters at 256, 64, 32, and 16 pixels on dark, light, black, and white treatments. Verify that the packet includes side-by-side, overlay, silhouette-difference, and color-difference evidence, palette qualification, explicit thresholds, and a clear disposition for every comparison.

**Acceptance Scenarios**:

1. **Given** a canonical candidate, **When** its approval packet is generated, **Then** exact full and reduced production proofs exist at all required sizes and surface treatments.
2. **Given** approval and production proofs from the same renderer, **When** they are compared, **Then** exact equality is required.
3. **Given** a documented renderer difference, **When** proofs are compared, **Then** topology and intended colors remain exact while bounded edge-aware perceptual measurements and reviewable difference images support the disposition.
4. **Given** a candidate palette, **When** it is offered for canonical approval, **Then** contrast, sibling-brand separation, color-vision robustness, semantic-role separation, light and dark behavior, and rendered-color continuity already pass.

---

### User Story 4 - Protect existing identities during migration (Priority: P2)

As the repository owner, I can adopt the stronger approval contract for existing constructed brands without redrawing, normalizing, or silently reapproving their shipped geometry.

**Why this priority**: A new contract that mutates established marks would violate identity preservation and reproduce the harm it is intended to prevent.

**Independent Test**: Audit every production brand, classify its source model, create continuity records where evidence permits, and prove that all pre-existing authoritative geometry hashes remain unchanged before and after migration.

**Acceptance Scenarios**:

1. **Given** the current production-brand inventory, **When** migration is planned, **Then** each brand is classified as constructed, imported, or otherwise governed and receives an explicit migration disposition.
2. **Given** an existing authoritative identity, **When** its continuity record is created, **Then** the record describes the current source without modifying path data, palette values, framing, or generated visual output.
3. **Given** historical approval evidence is insufficient for a claim, **When** migration runs, **Then** the record states the limitation and does not invent owner approval or normalize the source.
4. **Given** the migrated repository, **When** all kits are rebuilt, **Then** every existing identity remains geometrically unchanged and all production kits retain zero verification problems and zero glyph failures.

---

### User Story 5 - Apply the safer workflow consistently (Priority: P3)

As a future operator or agent, I can follow one unambiguous identity workflow whose documentation, approval schema, generated evidence, verification, and Spec Kit guidance agree about when an identity is exploratory, canonical, promoted, invalidated, or eligible for derivative work.

**Why this priority**: Machine enforcement is strongest when the human instructions and planning templates cannot direct an agent toward a contradictory approval boundary.

**Independent Test**: Start a synthetic future identity work order and verify that repository guidance prevents final approval before production construction, prevents Gate 2 from first revealing production geometry, names every invalidation condition, and requires the same evidence enforced by verification.

**Acceptance Scenarios**:

1. **Given** a future brand brief, **When** an operator follows the documented workflow, **Then** direction selection and canonical-master approval are clearly distinct decisions.
2. **Given** a work order that prohibits production construction before purported final glyph approval, **When** it is evaluated, **Then** the contradiction is rejected or corrected before work begins.
3. **Given** canonical approval has occurred, **When** Gate 2 derivatives are prepared, **Then** they consume the approved master without geometry reconstruction and cannot be the first production rendering shown to the owner.
4. **Given** a requested change to any governed identity property, **When** the change is evaluated, **Then** the affected approval is invalidated and the workflow returns to the correct gate.

### Edge Cases

- A concept is generated as a sketch, bitmap, or stroke model but production requires filled vector paths. The conversion must occur before canonical approval, and the owner approves the converted production rendering.
- Full and reduced masters intentionally use different framing or geometry. Both variants require explicit independent bindings inside one canonical approval bundle.
- A renderer upgrade changes only antialiasing edges. Exact source, topology, intended colors, and framing remain mandatory, while a documented edge-aware comparison determines whether a new canonical approval is required.
- A renderer change alters coverage, centroid, components, holes, or minimum features. The approval is invalidated even if a reviewer considers the difference subtle.
- A palette passes contrast but collides perceptually with a sibling brand or loses semantic distinctions under color-vision simulation. It cannot be offered for canonical approval.
- An existing imported logo has no construction helper. Its authoritative imported bytes remain the source of truth and are recorded without conversion to construction primitives.
- An existing constructed brand predates approval ledgers. Migration records current authoritative facts and historical evidence limits without fabricating retrospective approval.
- A generated proof is missing, stale, or produced by an unknown renderer configuration. Canonical approval and derivative generation remain ineligible.
- A third-party review proposes changing approved geometry. The finding is answered, but implementation returns to owner approval instead of silently changing the mark.
- Optional native rendering capability is unavailable locally. Local evidence records the skip, but hosted full-capability verification must succeed before merge readiness.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: S027 MUST trace GitHub issue #185 and the merged S026 correction that makes Cueson the primary regression case.
- **FR-002**: The workflow MUST define direction selection as nonbinding and distinct from canonical-master approval.
- **FR-003**: A constructed identity MUST NOT receive canonical approval until all conversions are complete and its proofs are rendered from the exact provisional production source through the production rendering path.
- **FR-004**: Canonical approval MUST bind the full master, reduced master when present, palette and role mapping, view box, artwork bounds, clear space, crop and framing values, construction provenance, topology, renderer configuration, and required proof hashes.
- **FR-005**: Canonical approval MUST record the exact owner wording, approved scope, approval-bundle identifier, timestamp, and synchronized source revision.
- **FR-006**: Missing, stale, malformed, contradictory, or incomplete approval evidence MUST fail closed.
- **FR-007**: Promotion MUST copy approved provisional source and configuration into the permanent brand-source boundary without reconstruction, translation, normalization, or manual path edits.
- **FR-008**: Promotion MUST prove that the permanent source and configuration hashes equal the approved hashes.
- **FR-009**: Production generation MUST verify every governed approval value before emitting derivative identity assets.
- **FR-010**: Any change to construction engine, source bytes, geometry, topology, fill behavior, framing, palette, role mapping, renderer configuration, or governed proofs MUST invalidate canonical approval and return work to that gate.
- **FR-011**: Constructed production sources MUST identify their approved construction system and MUST reject unapproved custom path serialization, direct path strings, or parallel geometry vocabularies.
- **FR-012**: Imported authoritative identities MUST remain eligible without forced reconstruction, provided their immutable source bytes and provenance are bound explicitly.
- **FR-013**: Approval comparison MUST cover full and reduced variants at 256, 64, 32, and 16 pixels on dark, light, black, and white treatments.
- **FR-014**: Approval evidence MUST include side-by-side views, alpha overlays, silhouette-difference views, and color-difference views for every governed comparison family.
- **FR-015**: Comparisons using the same deterministic renderer MUST require exact proof equality.
- **FR-016**: Documented cross-renderer comparisons MUST require exact source, topology, fill behavior, intended interior colors, and framing, plus explicit edge-aware thresholds for silhouette overlap, changed pixels, visible bounds, centroid movement, components, holes, and rendered color difference.
- **FR-017**: Cross-renderer thresholds MUST be calibrated against known equivalent output and the known S026 failure rather than copied from unverified issue estimates.
- **FR-018**: Every candidate palette MUST pass contrast, sibling-brand separation, color-vision simulation, semantic-role separation, light and dark surface behavior, single-ink behavior, and rendered-color equivalence before canonical approval.
- **FR-019**: Approval packets MUST expose every measured value, threshold, renderer identity, source hash, and disposition needed for an owner or reviewer to understand continuity.
- **FR-020**: Gate 2 and later derivative work MUST consume the canonical approved master and MUST NOT reconstruct, translate, normalize, or first reveal production geometry.
- **FR-021**: A synthetic regression MUST reproduce the S026 stroke-to-filled-geometry and framing divergence and MUST be rejected before Gate 2 eligibility.
- **FR-022**: Focused tests MUST cover valid direction selection, valid canonical approval, incomplete bundles, byte-preserving promotion, source drift, method drift, geometry drift, topology drift, framing drift, palette drift, renderer drift, proof drift, and invalid state transitions.
- **FR-023**: Security-oriented tests MUST reject path traversal, source paths outside approved roots, symlink escapes, untrusted executable renderer declarations, malformed hashes, duplicate evidence keys, and approval records that attempt to authorize generated or external destinations.
- **FR-024**: Migration MUST inventory every production identity and classify its authoritative source and construction model.
- **FR-025**: Migration MUST preserve all existing authoritative geometry and palette values byte-for-byte unless a separate explicit owner identity decision exists.
- **FR-026**: Historical evidence gaps MUST be recorded as limitations and MUST NOT be represented as retrospective owner approvals.
- **FR-027**: Existing brands MUST receive a compatible continuity disposition without changing their published eligibility solely because historical workflows lacked the new bundle.
- **FR-028**: Repository guidance and planning templates MUST distinguish direction selection, canonical approval, promotion, derivative approval, invalidation, and publication eligibility consistently.
- **FR-029**: Repository guidance MUST reject future work orders that define final glyph approval while prohibiting creation of the exact production master being approved.
- **FR-030**: Generated comparison evidence, approval packets, raster exports, migrated audit output, kits, registries, archives, and site exports MUST remain under ignored generated-output paths.
- **FR-031**: All production kits MUST rebuild with zero verification problems and every applicable constructed derivative MUST retain zero glyph-validation failures.
- **FR-032**: Verification MUST preserve WCAG 2.1 AA without exemptions and MUST confirm no existing authoritative identity geometry changed.
- **FR-033**: Changed text and downloadable evidence MUST use UTF-8 without BOM, LF line endings, and contain no mojibake or private workstation paths.
- **FR-034**: S027 MUST NOT redesign any existing identity, modify a consumer-product repository, activate a domain, merge its own pull request, tag, publish a release, or deploy production state.
- **FR-035**: After specification, implementation, and local verification pass, S027 MUST push its feature branch and open an official pull request that closes #185 without a separate pre-push halt, as explicitly authorized by the owner.
- **FR-036**: S027 MUST process every actionable continuous-integration, Codex, security-bot, and human-review finding, answer and resolve every review thread appropriately, MAY request exactly one second Codex review round, and MUST NOT request a third round.
- **FR-037**: S027 MUST halt for the owner merge ritual only after required continuous-integration checks are green and all received reviews are satisfied or accurately documented as non-actionable.

### Key Entities

- **Direction Selection**: A nonbinding owner choice that identifies a concept for production refinement without approving canonical source, derivatives, or publication.
- **Provisional Canonical Source**: The exact production-ready source and configuration used to render the candidate offered for canonical approval.
- **Canonical Approval Bundle**: The hash-bound record of source, construction provenance, full and reduced geometry, palette, role mapping, framing, topology, renderer configuration, proofs, owner decision, and state.
- **Promotion Record**: Evidence that approved provisional source and configuration entered permanent brand source unchanged.
- **Continuity Comparison**: A deterministic comparison between approval and production evidence with exact invariants, bounded renderer-edge metrics, visual difference artifacts, and disposition.
- **Palette Qualification**: Pre-approval evidence for contrast, sibling-brand separation, color-vision robustness, semantic separation, surface behavior, single-ink behavior, and rendered-color continuity.
- **Identity Migration Record**: A classification and continuity disposition for an existing brand that preserves authoritative geometry and states historical evidence limits.
- **Approval State**: One of exploratory, direction-selected, canonical-candidate, canonical-approved, promoted, invalidated, derivative-approved, or publication-eligible, with explicit permitted transitions.
- **Review Ledger**: The bounded record of CI results, received reviews, responses, corrections, resolutions, and no more than two Codex review rounds.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In 100% of constructed-identity tests, direction selection alone cannot authorize promotion, derivative generation, or publication.
- **SC-002**: In 100% of canonical-approval tests, all required source, geometry, palette, framing, topology, renderer, proof, owner, and revision fields are present and hash-bound before approval succeeds.
- **SC-003**: Promotion preserves 100% byte equality for approved provisional source and configuration, and every tested post-approval drift class fails before derivatives are emitted.
- **SC-004**: Approval comparison covers both applicable master variants at all four required sizes and all four required surface treatments, with every required visual evidence family present.
- **SC-005**: The known S026 construction-method and framing divergence is rejected, while calibrated equivalent cross-renderer output passes without weakening exact geometry, topology, framing, or intended-color invariants.
- **SC-006**: Every candidate palette offered for canonical approval passes 100% of required accessibility, sibling-separation, color-vision, semantic, surface, single-ink, and rendered-color checks.
- **SC-007**: Every production identity receives an explicit migration classification and disposition, while before-and-after inspection finds zero changed authoritative geometry or palette values.
- **SC-008**: All production kits rebuild with zero verification problems, every applicable glyph check reports zero failures, and all rendered accessibility checks meet WCAG 2.1 AA.
- **SC-009**: Documentation, approval schemas, generated evidence, verification behavior, and planning guidance agree on every permitted lifecycle state and invalidation condition with zero contradictory instructions.
- **SC-010**: The official pull request closes #185, all required checks pass, every received review thread is answered and resolved appropriately, no more than two Codex review rounds occur, and final merge remains solely with the owner.

## Assumptions

- S026 is merged and Cueson is the canonical regression case for construction and framing drift, not a candidate for redesign in S027.
- Existing shipped source data is authoritative even where historical approval records are less complete than the new contract.
- Imported identities and constructed identities require different provenance assertions, but both must be bound to immutable authoritative source.
- Cross-renderer equality cannot always be expressed as byte-identical pixels; thresholds will be calibrated from known equivalent and known divergent fixtures while exact structural invariants remain non-negotiable.
- The current two-gate brand workflow remains useful once direction selection and canonical-master approval are made explicit within the first creative phase.
- Automatic push and official pull-request creation are authorized after local verification, but merge, release, deployment, consumer-repository changes, identity redesign, and domain activation remain outside that authorization.

## Scope Boundaries

### In Scope

- Approval lifecycle and schema, canonical-source promotion, construction provenance, continuity verification, visual and palette qualification evidence, regression coverage, existing-brand migration records, and aligned workflow documentation.
- Cueson-based synthetic regression coverage for the previously observed method and framing divergence.
- Complete repository validation, official pull request, bounded review processing, and final owner handoff.

### Out of Scope

- Redesigning, redrawing, normalizing, or changing any existing approved identity.
- Creating a new brand or changing Cueson’s approved mark, palette, wordmark, kit, consumer repository, or domain.
- Publishing a brandbuilder release, tagging, deploying the site, or merging the S027 pull request.

## Traceability

- GitHub issue #185 is the complete defect diagnosis and corrective intake for S027.
- S026 issue #184 and PR #186 provide the known divergent and corrected Cueson construction history used to define the regression.
- The owner’s 2026-09-09 kickoff authorizes the complete S027 autopilot run, automatic push, and official pull-request creation, but not final merge, release, deployment, identity changes, or more than two Codex review rounds.
