# Feature Specification: Native egui Adapter and Versioned Contracts

**Feature Branch**: `codex/039-egui-adapter-version-contracts`

**Created**: 2026-09-17

**Status**: Ready for pull request review

**Input**: User description: "S039 combines GitHub issues #216 and #218: generate a native egui adapter from the shared Interface Canon and establish independent, recoverable version contracts for canon, compiler, brands, recipes, adapters, and deliberate consumer adoption."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consume the shared interface contract in a native renderer (Priority: P1)

A native application implementer can use a generated adapter that expresses the same semantic interface roles and bounded component behavior as the Web adapter without importing browser assumptions or product-specific composition.

**Why this priority**: The native adapter is the remaining generated-contract dependency for native conformance, version readiness, and the ESO Weave pilot.

**Independent Test**: Generate a production brand kit, inspect its native adapter and support declaration, and exercise representative rendered states to prove semantic traceability, density and scaling behavior, and explicit unsupported capabilities.

**Acceptance Scenarios**:

1. **Given** a production brand and the governed interface and recipe catalogs, **When** its kit is generated, **Then** the kit includes a native adapter whose semantic roles and component recipes trace to the exact source contract versions.
2. **Given** representative input, focus, selection, error, density, and scaling states, **When** the native specimen is exercised, **Then** supported states have deterministic evidence and unsupported host capabilities are reported explicitly.
3. **Given** a browser-only behavior or capability, **When** the native adapter is generated, **Then** the adapter records an intentional native adaptation or unsupported status instead of emulating browser source.

---

### User Story 2 - Version generated contracts independently (Priority: P1)

A BrandBuilder maintainer can evolve interface canon, recipes, framework adapters, compiler behavior, and individual brands without conflating their compatibility or implying that every consumer has deployed the latest generated kit.

**Why this priority**: Release compatibility is the gate between generated artifacts and deliberate consumer adoption. Native readiness cannot be complete until the native adapter has its own version identity and compatibility rules.

**Independent Test**: Produce release metadata and consumer manifests for multiple brands, change one governed contract dimension at a time, and prove that version identities, bump rules, compatibility results, and migration diagnostics change only where required.

**Acceptance Scenarios**:

1. **Given** a generated kit, **When** its manifest and release record are inspected, **Then** brand, Brand Canon, Interface Canon, recipe, Web adapter, native adapter, and compiler versions have distinct meanings and complete provenance.
2. **Given** a compatible change to one contract dimension, **When** compatibility is evaluated, **Then** unaffected versions and consumer deployment state remain unchanged.
3. **Given** an incompatible contract combination, **When** generation, verification, packaging, or recovery is attempted, **Then** the operation fails with the incompatible fields, expected relationship, and an actionable migration direction.

---

### User Story 3 - Recover an exact pinned consumer contract (Priority: P2)

A consumer maintainer can remain on a known-good generated contract and later retrieve the exact matching kit and implementation guidance, even after BrandBuilder and other brands have advanced.

**Why this priority**: Consumers must upgrade deliberately. Exact recovery prevents an upstream merge or publication from silently changing a downstream product.

**Independent Test**: Stage a versioned release candidate, resolve a pinned consumer record from it, and prove that all recovered contract bytes, checksums, source revision, adapter versions, and guidance agree while mismatched or tampered inputs fail closed.

**Acceptance Scenarios**:

1. **Given** a pinned consumer manifest and a matching release record, **When** recovery is requested, **Then** the exact kit, adapter contracts, and bundled guidance can be identified and integrity-checked.
2. **Given** a later BrandBuilder release, **When** an older supported consumer pin is inspected, **Then** its deployment status remains distinct from current generation status and the pin is not silently rewritten.
3. **Given** a missing, ambiguous, or checksum-mismatched artifact, **When** recovery is attempted, **Then** recovery fails closed with the exact missing or conflicting identity.

### Edge Cases

- A brand supports the Web adapter but declares a native capability unsupported or pending proof.
- A native host can supply a capability but the renderer cannot observe it directly.
- Logical-unit or density transforms produce a non-finite, non-positive, or otherwise invalid native value.
- A recipe names a semantic role or state that the native adapter cannot represent.
- Version metadata is syntactically valid but names an incompatible canon, recipe, adapter, compiler, or brand combination.
- An adapter payload is altered without updating its checksum or provenance record.
- A pinned release exists but its implementation guidance or one adapter artifact is absent.
- A release rebuild changes generated bytes without changing the governed source identity recorded for those bytes.
- Two brands share interface semantics while retaining different approved identity values.
- Optional native verification tooling is unavailable in an environment that is not authorized to substitute browser evidence.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: BrandBuilder MUST generate a native adapter for every production brand from the same governed Brand Canon, Interface Canon, and component recipe sources used by other adapters.
- **FR-002**: The native adapter MUST expose semantic token roles, logical-unit transforms, density behavior, environment capabilities, and bounded component contracts without browser or stylesheet assumptions.
- **FR-003**: Every generated native role and component contract MUST trace to the exact governing source contract and version.
- **FR-004**: Native logical-unit, density, text-scaling, and interaction-target transforms MUST be explicit, deterministic, and reject invalid values.
- **FR-005**: Supported, adapted, unsupported, and pending-proof native capabilities MUST be distinguishable, and unsupported capabilities MUST NOT masquerade as supported.
- **FR-006**: Shared component behavior MUST be expressed idiomatically for the native renderer rather than through browser-source emulation or a new cross-renderer interface language.
- **FR-007**: Representative native evidence MUST cover input, focus, selection, error, density, scaling, and at least one explicitly unsupported capability.
- **FR-008**: Generated native artifacts MUST remain renderer infrastructure and MUST NOT include product-specific composition or consumer business logic.
- **FR-009**: BrandBuilder MUST assign independent identities to the Brand Canon, Interface Canon, component recipes, Web adapter, native adapter, compiler, and each production brand.
- **FR-010**: Each version identity MUST have documented meaning, ownership, compatibility scope, and change rules that distinguish compatible additions, compatible corrections, and breaking changes.
- **FR-011**: Adapter and recipe compatibility MUST be represented independently from product-brand versions and consumer deployment state.
- **FR-012**: Generated consumer manifests, kit metadata, release records, and bundled guidance MUST agree on all applicable version identities.
- **FR-013**: Every generated contract MUST identify its exact source revision, provenance, and integrity checksum.
- **FR-014**: Verification MUST reject missing, malformed, unknown, inconsistent, or checksum-mismatched version and provenance data with actionable diagnostics.
- **FR-015**: Breaking contract combinations MUST fail before publication and identify the incompatible fields, expected relationship, and migration action.
- **FR-016**: Every candidate BrandBuilder release MUST rebuild and validate every production brand while preserving approved identity geometry, affiliation, and inheritance boundaries.
- **FR-017**: Release records MUST distinguish current generation compatibility, published artifact availability, and actual downstream adoption.
- **FR-018**: A consumer MUST be able to remain pinned to a known-good release until an intentional upgrade changes its recorded contract.
- **FR-019**: A pinned consumer MUST be able to identify and integrity-check its exact kit, matching adapter contracts, and bundled implementation guidance after later releases exist.
- **FR-020**: Recovery MUST fail closed when any pinned artifact, version identity, source revision, checksum, or guidance record is missing or conflicts with the release record.
- **FR-021**: Generated artifacts and synthetic verification inputs MUST remain outside committed publication sources and ineligible for accidental discovery or release.
- **FR-022**: The slice MUST NOT modify a consumer repository, claim actual downstream adoption, implement the full cross-host conformance matrix, or publish a new release.
- **FR-023**: The release and compatibility contract MUST preserve Python 3.8 consumer-generation compatibility and the repository's documented build and verification guarantees.

### Key Entities

- **Native Adapter Contract**: The generated renderer-specific semantic data, bounded component behavior, unit transforms, capability declarations, version identity, and source lineage for native consumers.
- **Contract Version Identity**: A named version for one governed compatibility domain, including Brand Canon, Interface Canon, component recipes, adapters, compiler, or brand definition.
- **Compatibility Relationship**: The declared supported relationship among contract version identities, including failure guidance for incompatible combinations.
- **Consumer Pin**: The immutable set of versions, source revision, artifact identities, and checksums a consumer intentionally adopts.
- **Release Record**: The exact-source inventory that binds generated kits, adapters, documentation, checksums, and compatibility declarations to one verified revision.
- **Native Capability Declaration**: A status and ownership record describing whether a renderer or host supports, adapts, lacks, or still needs proof for a runtime capability.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All production brands produce a native adapter with zero missing required semantic roles and zero untraceable component contracts.
- **SC-002**: The representative native-state suite covers 100 percent of the required input, focus, selection, error, density, scaling, and unsupported-capability categories with deterministic pass or explicit skip evidence.
- **SC-003**: Every generated consumer manifest and release record contains a complete, mutually consistent set of applicable contract version identities, source revision, provenance, and checksums.
- **SC-004**: All tested incompatible version, provenance, and checksum scenarios fail before publication with an actionable diagnostic naming the conflicting identity.
- **SC-005**: All production brands rebuild and pass their required verification gates without approved artwork or identity geometry changes.
- **SC-006**: An exact pinned kit and its matching implementation guidance can be resolved and integrity-checked from a staged release record after a newer candidate is present.
- **SC-007**: No generated kit, native build output, rendered baseline, release archive, or synthetic fixture is added to the committed source tree.
- **SC-008**: The full documented validation and CI-equivalent checks complete with zero failures on the slice revision.

## Assumptions

- The Interface Canon and bounded component vocabulary delivered by S037 and S038 are stable inputs for the first native adapter.
- The native adapter provides shared semantic data and representative idiomatic helpers, not a product UI framework or an arbitrary cross-renderer language.
- Rendered-state evidence inside BrandBuilder proves adapter readiness but does not constitute ESO Weave adoption or close the full runtime-conformance issue.
- Existing release and consumer-contract machinery is extended rather than replaced.
- Version identities use the repository's existing semantic-version conventions unless research finds an incompatible current contract.
- Downstream Glitchpad, go-schedule, and ESO Weave work requires separate authorization and tracking.
