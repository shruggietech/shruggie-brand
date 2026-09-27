# Feature Specification: Generated Artifact Semantics

**Feature Branch**: `codex/060-artifact-semantics`
**Created**: 2026-09-27
**Status**: In progress
**Input**: S060 implements issue #269, an end-to-end inventory and semantic audit of generated kits, skill distribution, hosted data, downloads, and release candidates. Guideline facts intersect issue #270 but its reader-facing content redesign remains separate.

## User Scenarios & Testing

### User Story 1 - Trust a complete kit (Priority: P1)

A consumer receiving a brand kit can tell that its advertised indexes and manifests name real, usable artifacts rather than empty lists or dangling references.

**Independent Test**: Tamper with a required inventory, referenced file, hash, or version in an isolated generated kit and run its certification. Each mutation fails with a specific diagnostic; an intentionally optional absence retains its explicit status.

**Acceptance Scenarios**:

1. **Given** a complete kit, **when** its generated records are checked, **then** every required item has a real delivery and agrees with its declared identity and version.
2. **Given** a missing required item, **when** certification runs, **then** the kit cannot be published as complete.
3. **Given** a genuinely unsupported or optional capability, **when** certification runs, **then** the absence is recorded truthfully and does not gain invented data.

### User Story 2 - Trust the hosted copy (Priority: P1)

A visitor can use each advertised hosted registry item, download, conformance fixture, and documentation record from the same candidate that was verified.

**Independent Test**: Change or remove a hosted item after site preparation. The publication audit rejects missing or changed bytes and mismatched catalog or version data before upload.

**Acceptance Scenarios**:

1. **Given** the eight verified kits and exported site, **when** the publication audit runs, **then** public indexes resolve to the exported files and published bytes match their kit source.
2. **Given** a catalog entry or download that is missing or altered, **when** the audit runs, **then** publication fails rather than reporting success from marker counts.

### User Story 3 - Review the evidence (Priority: P2)

A maintainer can see which producer and consumer owns each generated artifact family, its expected population, its legitimate empty states, and what was actually tested.

**Independent Test**: Review a coverage matrix that accounts for each generated family across the kit, skill, site, and release candidate, with source-to-consumer traces and classifications for any gaps.

**Acceptance Scenarios**:

1. **Given** a reported suspicious skeleton, **when** the maintainer reads the audit, **then** it is labeled as a demonstrated defect, legitimate optional state, or bounded unverified behavior with a producer and downstream effect.
2. **Given** a repair outside this coherent slice, **when** the audit closes, **then** it has its own closeable issue and the audit does not claim the repair is done.

### Edge Cases

- A required inventory may be a syntactically valid empty array; it must still fail.
- A declared reference can point outside its publication root or through a symlink; containment must be checked before reading.
- A file can exist with the wrong bytes, identity, or version; existence alone does not suffice.
- An optional capability can be absent when its published status explains why; the audit must not synthesize a false entry.
- A candidate may contain all eight brand markers while omitting registry or documentation data; marker counts alone must not pass.
- Published archive, site copy, and generated indexes can drift after their individual producer checks; the exact staged candidate must be rechecked.

## Requirements

### Functional Requirements

- **FR-001**: Maintain a reviewed coverage matrix for every generated index, registry, manifest, schema-directed payload, and advertised component family, including purpose, producer, consumer, schema/version, expected population, empty state, publication location, references, existing validation, and concrete use test.
- **FR-002**: Reject empty required inventories, malformed or unsafe references, missing files, hash/size mismatches, duplicate entries, and inconsistent brand, kit, compiler, or contract versions at the appropriate kit or publication gate.
- **FR-003**: Verify that published registry and download entries resolve to the exact certified kit output, and that site projections agree with the kit authority.
- **FR-004**: Distinguish source inspection, schema checks, semantic checks, consumer tests, and exact candidate checks in the recorded evidence.
- **FR-005**: Preserve explicit legitimate optional or unsupported states without invented records, while reporting unverified behavior and follow-up repairs precisely.
- **FR-006**: Run the semantic audit on the exact release candidate before its assets are uploaded or promoted.
- **FR-007**: Preserve WCAG 2.1 AA and approved identity geometry; no audit fix may weaken those gates.

### Key Entities

- **Artifact family**: A generated record type and its producer, schema, consumer, and publication surfaces.
- **Reference**: An artifact-declared path, URL, version, hash, or dependency that must resolve in its declared scope.
- **Candidate**: The complete staged kit, site, and release output from one source revision.
- **Finding**: A defect, legitimate empty state, or bounded unverified behavior, with evidence and disposition.

## Success Criteria

- **SC-001**: The coverage matrix accounts for all generated JSON, manifest, registry, index, and advertised component families in the eight production kits, the skill bundle, site data, public routes, and release staging.
- **SC-002**: Negative regressions reject empty required data, missing references/dependencies, and mismatched hashes, inventories, and versions; a valid optional absence passes.
- **SC-003**: All eight production kits pass zero-problem kit and glyph validation, and the exported site and staged release candidate pass semantic publication checks.
- **SC-004**: Every reported gap has a reproducible classification and a completed source fix or linked closeable follow-up; the evidence does not claim consumer behavior from an HTTP 200 alone.

## Assumptions and Boundaries

- This slice certifies BrandBuilder-produced artifacts and their hosted publication. It does not adopt kits in downstream repositories.
- Existing deep validators remain authoritative for their respective families; the new audit composes them at publication boundaries rather than duplicating every contract.
- Issue #270 remains open for its full guideline content and reader-task audit. S060 checks the generated documentation facts and links that overlap its data-integrity concerns.
- The 2.6.0 source line is an unpublished candidate. S060 changes certification and evidence without changing approved identity data or the public kit shape, so it retains the candidate version and records the change under Unreleased.
