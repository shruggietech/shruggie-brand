# Feature Specification: Ownership-Neutral Authoritative Inputs

**Feature Branch**: `codex/007-ownership-neutral-inputs`

**Created**: 2026-09-05

**Status**: Clarified

**Input**: Deliver GitHub issues #104 and #105 together: support third-party brands without false ShruggieTech affiliation, and support authoritative supplied marks and fixed fonts without altering or silently replacing them.

## Context

The current brandbuilder assumes every brand belongs to ShruggieTech, inherits from ShruggieTech, uses the house type families, and may receive a ShruggieTech ownership endorsement. It also has a narrow imported-raster exception but no complete source contract for supplied marks, wordmarks, palette evidence, or fixed fonts. S007 replaces those assumptions with explicit affiliation, showcase, credit, input-provenance, palette-approval, and typography modes while preserving the current five production brands through an explicit migration.

## Clarifications

### Session 2026-09-05

- Q: Must existing behavior remain available through an implicit fallback or an explicit migration? → A: Every production brand is migrated to explicit values, and missing affiliation, inheritance, or typography modes fail validation.
- Q: Does third-party ownership automatically inherit ShruggieTech semantic colors? → A: No. Every brand explicitly selects house or independent inheritance; independent brands supply their own emphasis and action colors.
- Q: When may extracted colors become canonical brand tokens? → A: Only after a human records approval of a named candidate and the resulting tokens pass accessibility validation.
- Q: When may the system fetch a fixed font? → A: Only during an explicit controlled ingestion operation with an authoritative HTTPS source, expected hash, license evidence, and local destination; ordinary builds remain offline.
- Q: How are supplied source assets protected from transformation? → A: Original bytes and path data remain immutable; every permitted derived transformation is separately declared and approved.

## User Scenarios & Testing

### User Story 1 - Build a third-party brand without false affiliation (Priority: P1)

As a brand operator, I can declare that a brand belongs to a third party, separately declare whether it may appear in the public portfolio, and optionally approve a neutral ShruggieTech service credit without generating an ownership claim.

**Why this priority**: A false ownership statement is the highest-risk current behavior and blocks safe use of the brandbuilder for client work.

**Independent Test**: Generate a complete isolated third-party kit from an explicit affiliation record, then scan its guidelines, PDF source, manifests, templates, metadata, registry, documentation, and public-site record. The kit contains no ShruggieTech ownership or parent claim, and a public record appears only when showcase permission is granted.

**Acceptance Scenarios**:

1. **Given** a third-party brand with no approved service credit, **When** the complete kit is generated, **Then** no ShruggieTech ownership, parentage, endorsement, or credit language appears anywhere in the output.
2. **Given** a third-party brand with an approved neutral service credit, **When** the complete kit is generated, **Then** only the configured neutral credit appears and it cannot be mistaken for ownership.
3. **Given** a third-party brand without public showcase permission, **When** the public portfolio is prepared, **Then** the brand is excluded even when a verified kit exists.
4. **Given** a ShruggieTech-owned sub-brand with explicit parent, house inheritance, and endorsement values, **When** it is generated, **Then** its intended parent relationship and house semantic colors remain available.
5. **Given** a brand definition missing explicit affiliation fields, **When** validation begins, **Then** generation stops before any publishable output is produced.
6. **Given** a third-party brand with independent inheritance, **When** it is generated, **Then** its explicit emphasis and action colors replace ShruggieTech house orange throughout tokens and bindings.

---

### User Story 2 - Preserve authoritative supplied marks and derive reviewable palette evidence (Priority: P2)

As a brand operator, I can declare supplied mark or wordmark masters as authoritative, retain their original bytes and path data, and obtain deterministic color candidates without allowing the system to silently redraw the identity or canonize unapproved colors.

**Why this priority**: Supplied artwork is common in client work and the repository constitution prohibits unapproved identity changes.

**Independent Test**: Run an isolated build with a supplied master record, compare the original source hash and declared path data before and after the build, inspect the generated candidate-color evidence, and prove that an absent or mismatched approval blocks canonical palette use.

**Acceptance Scenarios**:

1. **Given** an authoritative vector master, **When** the kit is generated, **Then** its original bytes and path data remain unchanged and the evidence identifies the source role, hash, format, color profile, license or usage status, and approved transformations.
2. **Given** an authoritative raster master with transparency, **When** palette analysis runs, **Then** transparent pixels are excluded, representative color candidates and limitations are recorded, and the source bytes remain unchanged.
3. **Given** only a supplied mark or only a supplied wordmark, **When** the remaining identity component is constructed through the normal workflow, **Then** the supplied component remains authoritative and the two roles stay distinguishable.
4. **Given** extracted candidate colors without recorded human approval, **When** a build attempts to use them as canonical tokens, **Then** validation fails before publication.
5. **Given** a selected candidate and resulting canonical tokens, **When** accessibility validation runs, **Then** the ordinary WCAG 2.1 AA gates remain mandatory.
6. **Given** a source hash drift or an undeclared transformation, **When** validation runs, **Then** the build fails with the affected source role and reason.

---

### User Story 3 - Ingest and use fixed fonts without build-time networking (Priority: P3)

As a brand operator, I can explicitly select fixed typography outside the house families, ingest legally usable font binaries from an authoritative source under controlled conditions, and generate the kit from local verified files only.

**Why this priority**: Fixed typography is part of the same authoritative-input contract and must not be silently substituted, fetched during a build, or used without provenance and license evidence.

**Independent Test**: Ingest a controlled local test font through the same validation path used for remote sources, verify its expected hash and metadata, generate typography bindings and documents from the local file, disable network access, and complete the build without fallback to house font names.

**Acceptance Scenarios**:

1. **Given** an explicit fixed-font declaration with complete approved local files, **When** the kit is generated offline, **Then** every generated typography surface uses the declared families, weights, styles, and formats.
2. **Given** a controlled ingestion request, **When** the authoritative source, expected hash, license identifier, and destination are valid, **Then** the font is stored under the repository font boundary with auditable provenance.
3. **Given** a missing license, unexpected hash, family-name mismatch, unavailable required weight or style, corrupt binary, insecure source, or destination outside the font boundary, **When** ingestion or validation runs, **Then** it fails before publication and leaves no partial approved asset.
4. **Given** a house-typography brand, **When** it is generated, **Then** it uses the existing local house fonts through an explicit house mode.
5. **Given** a fixed-font brand, **When** ordinary generation begins without network access, **Then** it never attempts a network request or silently substitutes another family.

---

### User Story 4 - Audit and migrate the complete system (Priority: P4)

As a maintainer, I can rely on one contract across source definitions, generators, validators, documentation, archives, and the public site, with all current production brands migrated and regressions covered at the minimum supported runtimes.

**Why this priority**: Partial adoption would leave the dangerous defaults active on an untested output surface.

**Independent Test**: Rebuild all five production kits and the site from migrated definitions, run isolated third-party, supplied-input, and fixed-font regressions, and verify that every output consumes the same explicit contract.

**Acceptance Scenarios**:

1. **Given** the five current production brands, **When** the repository build runs, **Then** all five pass with explicit affiliation and typography modes and retain intended current identity behavior.
2. **Given** any generated text-bearing or metadata surface, **When** its affiliation output is inspected, **Then** it agrees with the source contract and contains no prohibited claim.
3. **Given** Python 3.8 and the supported full build environment, **When** the contract and regressions run, **Then** both complete successfully without weakening identity or accessibility gates.
4. **Given** S007 is merged, **When** the remaining milestone is inspected, **Then** #104 and #105 are eligible for completion while #106 remains open for S008.

### Edge Cases

- A third-party brand sets ShruggieTech as its parent or selects the ownership endorsement.
- A ShruggieTech parent brand attempts to endorse itself as a project.
- Public showcase permission is absent, unknown, or conflicts with a legacy site entry.
- A service credit is selected for an owned brand or contains arbitrary prose.
- Two authoritative input records claim the same role or identifier.
- A declared source path escapes the brand source or staged kit boundary, resolves through a link, or targets a missing file.
- A supplied SVG contains live text, external references, scripts, event handlers, or network URLs.
- A supplied image has no visible pixels, unsupported color mode, embedded profile ambiguity, or too many near-identical colors.
- Palette candidates change because the input bytes changed after approval.
- A fixed font has a valid extension but invalid binary contents, mismatched internal family names, unsupported variable axes, or a missing required face.
- A controlled font ingestion is interrupted after download but before validation.
- A private third-party kit exists in `dist/` alongside public brands.
- Historical prose and code examples need to describe prohibited phrases without causing generated deliverables to emit them.

## Requirements

### Functional Requirements

- **FR-001**: Every brand definition MUST explicitly declare an ownership mode, a public showcase state, a parent relationship or explicit absence, a house or independent inheritance mode, an ownership endorsement mode, and a neutral service-credit mode.
- **FR-002**: Ownership, showcase permission, parentage, inheritance, ownership endorsement, and service credit MUST remain separate fields with closed allowed values where applicable.
- **FR-003**: Third-party brands MUST reject ShruggieTech ownership endorsements and MUST default to no neutral service credit through an explicit `none` value.
- **FR-004**: Neutral service credit MUST be opt-in, use an approved fixed phrase, and MUST NOT imply ownership or parentage.
- **FR-005**: The public portfolio MUST include only verified brands whose explicit showcase state permits publication.
- **FR-006**: Missing, contradictory, or unsupported affiliation values MUST fail before publishable generation.
- **FR-007**: All text, metadata, manifest, registry, guideline, PDF, UI, README, and enforcement outputs MUST derive affiliation language from the same source contract.
- **FR-008**: Automated output scanning MUST reject prohibited ShruggieTech affiliation phrases in third-party outputs and reject undeclared credit text.
- **FR-009**: Existing production brands MUST be migrated to explicit affiliation values with no identity change.
- **FR-010**: Brand definitions MUST explicitly select house or fixed typography; missing typography mode MUST fail validation.
- **FR-011**: Fixed typography MUST declare every required family role, family name, face path, weight, style, format, expected hash, license identifier, provenance source, and usage status.
- **FR-012**: Fixed-font validation MUST compare declared values to the local binary's measured format, internal family metadata, weight, style, and hash.
- **FR-013**: Ordinary build, verification, documentation, site, and release operations MUST use local font files only and MUST NOT make font-network requests.
- **FR-014**: Controlled font ingestion MUST require an authoritative secure source or controlled local source, an expected hash, license evidence, an allowed destination under the repository font boundary, and atomic validation before placement.
- **FR-015**: Controlled ingestion MUST reject incomplete, corrupt, mismatched, unlicensed, insecure, or out-of-bound inputs without leaving a partially approved destination.
- **FR-016**: Generated styles, framework bindings, registries, specimens, guidelines, PDFs, and enforcement rules MUST use the selected typography contract rather than fixed house-family assumptions.
- **FR-017**: Brand definitions MUST support zero or more authoritative supplied-input records that distinguish mark, reduced mark, wordmark, and reference-art roles.
- **FR-018**: Each supplied-input record MUST declare a stable identifier, repository-relative source path, role, media format, expected hash, color-profile status, license or usage status, and an explicit list of approved transformations.
- **FR-019**: Validation MUST preserve and recheck original supplied bytes and declared path data and MUST reject hash drift, role collisions, unsupported active content, external dependencies, or undeclared transformations.
- **FR-020**: A brand MUST be able to supply a mark without a supplied wordmark, a wordmark without a supplied mark, or both, while constructed components remain governed by the existing identity workflow.
- **FR-021**: Deterministic palette analysis MUST ignore fully transparent pixels, record sampling and color-profile limitations, and emit ranked review candidates with source-hash linkage.
- **FR-022**: Candidate colors MUST NOT become canonical tokens until a human approval record names the source hash and selected candidate; canonical tokens MUST still pass ordinary accessibility validation.
- **FR-023**: Approval MUST become stale when its source hash or selected candidate no longer matches current evidence.
- **FR-024**: Source provenance, palette evidence, affiliation decisions, typography mode, and validation outcomes MUST be auditable without storing confidential contract text.
- **FR-025**: Test-only third-party and fixed-font data MUST be created in isolated temporary storage and MUST never enter production discovery, site publication, or release archives.
- **FR-026**: Python 3.8 compatibility, Windows hidden-process guarantees, UTF-8 without BOM, LF endings, and the existing identity and WCAG 2.1 AA gates MUST remain intact.
- **FR-027**: S007 MUST close only #104 and #105 after merge evidence; native Android, Apple, macOS, and Windows icon-suite generation in #106 remains out of scope.
- **FR-028**: Every negative Codex review finding on the S007 pull request MUST be answered, corrected when warranted, and resolved, with no more than two total review rounds.
- **FR-029**: Independent inheritance MUST require explicit emphasis and action colors and MUST prevent ShruggieTech house orange from entering generated brand tokens, framework bindings, or guidance.

### Key Entities

- **Affiliation Contract**: Explicit ownership, parent relationship, inheritance mode, ownership endorsement, neutral service credit, and public showcase state for one brand.
- **Authoritative Input**: Immutable supplied source record with identity role, path, hash, media facts, usage status, and approved transformations.
- **Palette Evidence**: Deterministic color candidates and analysis limitations linked to one exact authoritative input hash.
- **Palette Approval**: Human decision linking one candidate and source hash to canonical token values.
- **Typography Contract**: Explicit house or fixed mode with role-to-family and face requirements.
- **Font Face Record**: Local font file facts, expected hash, family metadata, weight, style, format, license, provenance, and usage status.
- **Ingestion Record**: Controlled request and measured result for placing one approved font under the repository font boundary.
- **Publication Record**: Derived site eligibility and public-safe presentation fields for one verified brand.

## Success Criteria

### Measurable Outcomes

- **SC-001**: An isolated third-party build completes with zero prohibited ShruggieTech ownership or parent claims across all generated text and metadata surfaces.
- **SC-002**: All five production brands rebuild with zero verification problems and zero glyph failures after explicit migration.
- **SC-003**: Every authoritative supplied input in a completed build has a matching measured hash, unique role record, and auditable usage status, with zero silent source changes.
- **SC-004**: Palette evidence is reproducible for unchanged source bytes, and 100 percent of canonical selections are linked to a current human approval and still pass accessibility gates.
- **SC-005**: Fixed-font generation completes with networking disabled and uses 100 percent of the declared required faces with no silent substitutions.
- **SC-006**: Each defined font-ingestion failure class stops before destination placement and leaves zero partial approved files.
- **SC-007**: Public preparation publishes 100 percent of eligible verified brands and zero private or unapproved brands.
- **SC-008**: Repository, Python 3.8, full-kit, release-contract, site, and Markdown checks all pass on the final pull-request revision.
- **SC-009**: Every review thread from no more than two Codex review rounds is answered and resolved before owner handoff.

## Scope

### In Scope

- GitHub issues #104 and #105.
- Source schema and runtime validation for affiliation, showcase, inheritance, authoritative inputs, palette evidence and approval, and typography mode.
- Explicit migration of the five production brand definitions.
- Controlled fixed-font ingestion tooling and offline consumption of approved local fonts.
- Generator, validator, documentation, site, test, release, and skill updates needed for end-to-end consistency.

### Out of Scope

- Native Android, iOS, iPadOS, macOS, Windows, store-listing, or adaptive icon suites tracked by #106 and planned for S008.
- Selecting a new production brand palette, redrawing any current mark, changing current wordmarks, or fetching a new production font during this slice.
- Storing client agreements, customer identities not already public, pricing, or confidential permission evidence.
- Publishing a release or merging the pull request without the owner ritual.

## Assumptions

- Existing public production brands have showcase permission and can be migrated to explicit `public` state.
- Existing ShruggieTech product brands retain their current parent relationship through explicit owned-brand configuration; the ShruggieTech parent brand has no parent or project endorsement.
- A neutral service credit uses one fixed approved phrase and is absent unless explicitly selected.
- Fixed-font test coverage can reuse repository-licensed font files in isolated temporary directories without introducing a new production font.
- Network retrieval is an operator-invoked ingestion concern and is never part of routine kit generation.
- S007 may add a schema and shared contract module because the current `$schema` references point to an absent file; this discovered defect must be corrected rather than preserved.
