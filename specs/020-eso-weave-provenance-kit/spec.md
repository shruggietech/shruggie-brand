# Feature Specification: ESO Weave Provenance and Current-Spec Kit

**Feature Branch**: `codex/020-eso-weave-provenance-kit`

**Created**: 2026-09-07

**Status**: Gate 1 and Gate 2 approved, implementation and local validation complete

**Input**: User description: "Deliver issue #153 as S020: establish auditable ESO Weave provenance, model the identity as an independent third-party brand, preserve its authoritative artwork, produce a complete current-spec kit, and publish only after two explicit owner approvals."

## Clarifications

### Session 2026-09-07

- Q: Is the statement that ESO Weave originated through the ShruggieTech brand-building system independently proven by public history? -> A: No. It is an operator-supplied provenance fact and must be labeled as such.
- Q: What affiliation may the kit claim? -> A: ESO Weave is an independent third-party identity with no ShruggieTech parent, ownership, endorsement, maintenance, or warranty claim. The only permitted service credit is `Brand system by ShruggieTech`.
- Q: May synchronized upstream paths replace stale intake paths without a separate approval? -> A: Yes. Use the current default-branch equivalents, record the mapping, and treat content or authoritative-hash drift as stale approval evidence.
- Q: When may derivative geometry and public surfaces be created? -> A: Derivative identity geometry requires the first hash-bound owner approval. Publication requires a second owner approval of the completed kit and exact public surfaces.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Establish trustworthy provenance (Priority: P1)

As the identity owner, I can inspect one complete source inventory that distinguishes public historical evidence from the operator-supplied origin statement, records the synchronized upstream revision, and traces every accepted input by role and hash.

**Why this priority**: Every later derivative, generated asset, and public claim depends on a stable and accurate source baseline.

**Independent Test**: Compare the recorded upstream revision, paths, hashes, roles, licenses, and provenance classifications with the synchronized source repository. Every required input is present or explicitly mapped to its current equivalent, and the two SVG masters are byte-identical to upstream.

**Acceptance Scenarios**:

1. **Given** the upstream default branch has advanced since issue intake, **When** S020 inventories it, **Then** the current revision and path changes are recorded and every authoritative identity or font hash is compared with the intake record.
2. **Given** the issue supplies an origin statement that public history does not independently establish, **When** provenance is documented, **Then** the statement is labeled as operator-supplied while the introducing commit and S012 records are labeled as public historical evidence.
3. **Given** a required intake document moved upstream, **When** a current canonical equivalent exists, **Then** the inventory records the old-to-current path mapping without representing the move as content or identity drift.
4. **Given** any authoritative hash changes before approval, **When** the gate is evaluated, **Then** prior approval is stale and the affected proposal returns to owner review.

---

### User Story 2 - Approve only faithful identity derivatives (Priority: P1)

As the identity owner, I receive a hash-bound proposal describing the load-bearing character of the current mark, every required derivative, each transformation boundary, and side-by-side proofs at 256, 64, 32, and 16 pixels on light and dark surfaces before any derivative master is added to production sources.

**Why this priority**: The repository constitution prohibits unapproved changes to shipped identity geometry, while the current kit contract requires assets not supplied upstream.

**Independent Test**: Inspect the first approval packet and confirm it contains the two exact SVG sources and hashes, proposed derivatives, stated no-change boundaries, size and surface comparisons, measured differences, recommendations, and an unambiguous approval ledger awaiting owner action.

**Acceptance Scenarios**:

1. **Given** the supplied badged mark and badge-less glyph are authoritative, **When** the proposal is prepared, **Then** neither source file nor its path data is normalized, traced, simplified, recolored, or overwritten.
2. **Given** horizontal, stacked, wordmark-only, single-ink, and reduced deliverables are required, **When** transformation boundaries are proposed, **Then** each proposed construction states which authoritative source it uses and which new geometry or layout it would introduce.
3. **Given** the first owner approval has not been recorded against the current hashes, **When** implementation reaches derivative creation, **Then** work halts before production derivative geometry is created.

---

### User Story 3 - Build a complete ownership-safe kit (Priority: P2)

As a brand consumer, I can use a complete current-spec ESO Weave kit whose identity, local typography, semantic colors, platform assets, UI specimen, and guidance are generated from approved sources and whose copy cannot imply ShruggieTech ownership or official game-vendor status.

**Why this priority**: Provenance becomes useful only when it governs a complete, verifiable deliverable.

**Independent Test**: Build the ESO Weave kit offline from repository sources, validate its contract and glyphs, inspect every required layer, and scan every generated text and metadata surface for prohibited affiliation claims and missing vendor disclaimers.

**Acceptance Scenarios**:

1. **Given** the approved affiliation record, **When** the kit is generated, **Then** it identifies ESO Weave as public, independent, and third-party, uses only the exact neutral service credit, and emits no ownership, endorsement, parentage, maintenance, or warranty claim.
2. **Given** ESO Weave is independently themed, **When** semantic tokens are generated, **Then** explicit ESO Weave emphasis and action colors are used instead of inherited ShruggieTech house colors.
3. **Given** current upstream Inter files and license evidence, **When** typography is packaged, **Then** every approved face is locally available, license-traced, metadata-validated, and usable without network access.
4. **Given** approved derivatives, **When** the kit is generated, **Then** all required lockups, single-ink variants, platform icons, bindings, registries, specimens, guidelines, UI specimen, PDF, manifest, verification record, and migration notes are present.
5. **Given** a public or generated surface could imply official Elder Scrolls Online vendor status, **When** it is rendered, **Then** the upstream ZeniMax, Bethesda, and Microsoft non-affiliation and trademark boundary remains visible and accurate.

---

### User Story 4 - Publish only the approved representation (Priority: P3)

As the identity owner, I can review the complete rendered kit, verification evidence, and exact proposed public surfaces before any ESO Weave registry or site entry becomes public.

**Why this priority**: Public showcase permission is explicit, but publication remains unsafe until the owner verifies derivative fidelity in the finished context.

**Independent Test**: Before publication, inspect the source inventory, approval ledger, derivative comparison sheet, rendered guide, UI specimen, all gate results, and an exact list of site and registry surfaces. Confirm no public ESO Weave entry exists until approval is recorded.

**Acceptance Scenarios**:

1. **Given** the complete kit passes local verification but final owner approval is absent, **When** site preparation runs, **Then** ESO Weave remains excluded from public site and registry output.
2. **Given** the owner approves the completed representation and exact public surfaces, **When** publication is enabled, **Then** only those approved surfaces are added and they consume the verified generated kit.
3. **Given** authoritative hashes or approved derivative hashes drift after approval, **When** publication is attempted, **Then** the gate fails closed and requires renewed owner approval.

### Edge Cases

- Upstream advances while S020 is in progress. Re-fetch before each approval gate and invalidate affected approvals if authoritative inputs changed.
- A historical path named in issue #153 no longer exists. Record its current canonical replacement and both revisions rather than recreating a stale path.
- The badged mark works at 16 pixels but the badge-less glyph does not. Reduced-use approval may select the existing badged master while prohibiting the glyph at that size.
- A single-ink conversion changes apparent strand order or closes the weave gap. Reject it rather than weakening the geometric fidelity gate.
- A font file has the expected filename but unexpected internal family, weight, style, format, license, or hash. Stop ingestion before changing shared fonts.
- A generated page uses the service credit correctly but omits the game-vendor boundary where its context could imply official status. Treat the page as unpublishable.
- Optional native rendering capabilities are unavailable locally. Record the explicit skip, retain all non-optional measured gates, and require CI capability coverage before completion.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: S020 MUST record the synchronized upstream default-branch revision and compare every authoritative SVG and fixed-font hash with the issue intake record.
- **FR-002**: The source inventory MUST record contained path, identity role, media format, byte size, SHA-256, color-profile status, license or usage basis, usage status, provenance class, and explicitly approved transformations for every acquired input.
- **FR-003**: The provenance record MUST distinguish the operator-supplied ShruggieTech origin statement from independently observable public commit and specification history.
- **FR-004**: Current upstream canonical replacements for stale intake paths MUST be mapped explicitly, with no claim that a path move is an identity change.
- **FR-005**: The authoritative `eso-weave-mark.svg` and `eso-weave-glyph.svg` bytes and path data MUST remain unchanged.
- **FR-006**: The source contract MUST model ESO Weave as `third-party`, publicly showcaseable, parentless, independently themed, unendorsed, and credited only by `Brand system by ShruggieTech`.
- **FR-007**: Missing affiliation fields, ShruggieTech parentage, owned-project endorsement, ownership, maintenance, or warranty claims MUST fail before publishable output is produced.
- **FR-008**: ESO Weave MUST declare independent semantic emphasis and action colors and MUST NOT inherit ShruggieTech house orange.
- **FR-009**: Palette approval MUST be bound to the current authoritative source hashes and invalidated by source drift.
- **FR-010**: Fixed typography MUST be sourced from the synchronized upstream files, locally delivered, metadata and license verified, and network-independent during routine generation.
- **FR-011**: Any additional font face required by the current contract MUST be proposed with license and metadata evidence and MUST receive owner approval before ingestion.
- **FR-012**: Before derivative identity geometry is created, the first owner gate MUST present exact sources and hashes, load-bearing characteristics, required derivatives, transformation boundaries, light and dark comparisons at 256, 64, 32, and 16 pixels, measured differences, and a recommendation for every derivative.
- **FR-013**: No derivative approval is valid unless it names the approved derivative set and is bound to the displayed authoritative hashes.
- **FR-014**: If faithful compliance is impossible without moving the identity, S020 MUST stop and report the conflict rather than approximate it.
- **FR-015**: After derivative approval, the generated kit MUST contain the complete current specification contract: human and agent entry points, source contract, manifest, verification record, migration notes, tokens, components, styles, framework bindings, registry entries, enforcement rules, required lockups and variants, platform icon suites and manifests, local fonts and licenses, outlined specimen, guidelines, UI specimen, and brand-guide PDF.
- **FR-016**: The UI specimen MUST express current ESO Weave purpose, voice, safety posture, domain components, and representative application presentation without becoming a second product specification.
- **FR-017**: Relevant public and generated surfaces MUST preserve the upstream ZeniMax Online Studios, ZeniMax Media Inc., Bethesda Softworks, Microsoft, and Elder Scrolls trademark and non-affiliation boundary.
- **FR-018**: Automated tests MUST prove the valid third-party contract passes, prohibited combinations fail closed, forbidden ShruggieTech claims are absent, vendor-boundary requirements are enforced, and stale approvals cannot publish.
- **FR-019**: Every approved constructed derivative MUST report zero glyph-validation failures, and the kit MUST report zero verification problems and no WCAG 2.1 AA waivers.
- **FR-020**: Generated assets, registries, static exports, PDFs, rasters, and release archives MUST remain under ignored generated-output locations and MUST NOT be committed.
- **FR-021**: Before publication, the second owner gate MUST present the source inventory, approval ledger, derivative comparison sheet, rendered guide, UI specimen, complete verification results, and exact proposed public surfaces.
- **FR-022**: Site, registry, release, and other public ESO Weave output MUST remain disabled until the second approval is recorded against the completed derivative and source hashes.
- **FR-023**: Once approved, public presentation MUST consume the verified generated kit and MUST contain only the approved neutral credit and vendor boundary.
- **FR-024**: The full documented repository validation and hosted CI MUST pass before the slice is merge-ready.
- **FR-025**: S020 MUST trace implementation and pull-request closure to GitHub issue #153.

### Key Entities

- **Upstream Snapshot**: The synchronized ESO Weave default-branch revision and retrieval time from which all evidence is derived.
- **Source Evidence Record**: One acquired input with path, role, format, size, hash, profile, license, provenance class, status, and transformation policy.
- **Affiliation Contract**: The closed third-party ownership, showcase, parentage, inheritance, endorsement, and service-credit declaration.
- **Approval Ledger Entry**: An owner decision bound to a gate, source hashes, proposed or completed derivative hashes, exact scope, timestamp, and status.
- **Derivative Proposal**: A named required asset, its source dependency, allowed transformations, forbidden transformations, comparison evidence, measurements, and recommendation.
- **ESO Weave Kit**: The source definition and complete generated current-spec deliverable derived from approved evidence.
- **Publication Surface Set**: The exact site, registry, metadata, and downloadable representations proposed at the second gate.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One inventory accounts for 100 percent of required identity, font, reproduction, rendered-reference, product-voice, and provenance inputs, with no unclassified authoritative input.
- **SC-002**: The two upstream SVG masters and all approved fixed-font files match their recorded SHA-256 values, and authoritative source bytes have zero changes in the final source diff.
- **SC-003**: Every proposed derivative has eight comparison contexts (four sizes on two surfaces), an explicit transformation boundary, measured differences, and one recorded recommendation before approval.
- **SC-004**: Generated ESO Weave output contains zero prohibited ShruggieTech ownership, endorsement, parentage, maintenance, or warranty claims.
- **SC-005**: Every relevant public representation contains the required game-vendor boundary and contains zero claims of official vendor status.
- **SC-006**: The completed kit contains 100 percent of the current required layers and platform suites, with no generated deliverable committed to Git.
- **SC-007**: Glyph validation reports zero failures for every approved constructed derivative, kit verification reports zero problems, and all declared text and fill roles pass WCAG 2.1 AA without waivers.
- **SC-008**: Before the second approval, public ESO Weave site and registry entries number zero; after approval, the approved surface set is complete and no unapproved surface exists.
- **SC-009**: A clean full repository build, site export, tests, hygiene audit, hosted CI, and bounded review process all complete successfully before owner merge review.

## Assumptions

- Issue #153 supplies explicit permission for public showcase and the exact neutral service credit, but not permission to claim ownership, endorsement, maintenance, warranty, or game-vendor affiliation.
- The current upstream default branch is the evidence source. Historical S012 material remains provenance evidence even when later documentation reorganizes its canonical paths.
- The supplied badged mark is the strongest candidate for the reduced mark because it is already the documented icon used at 16 pixels, but this remains an owner decision at the first gate.
- Inter Regular, Medium, and SemiBold are sufficient for the current proportional typography contract. Any missing mono requirement will be handled as a separate approval item rather than inferred.
- Generated proof sheets and completed kit artifacts remain ignored and reproducible; committed evidence records their inputs, measurements, hashes, and approval decisions.

## Scope Boundaries

### In Scope

- GitHub issue #153 in full.
- Current upstream acquisition, provenance, affiliation, source preservation, approved derivative construction, complete kit generation, verification, and approved public showcase integration.
- Generator or verifier corrections required to make the explicit third-party, disclaimer, approval, or supplied-source contracts fail closed.

### Out of Scope

- Changes to the ESO Weave application, its upstream runtime behavior, roadmap, repository settings, or release packages.
- Redesigning, modernizing, simplifying, recoloring, or otherwise improving the supplied identity.
- Claiming independent proof for the operator-supplied ShruggieTech origin statement.
- Publishing before the second approval or cutting a shruggie-brand release.
