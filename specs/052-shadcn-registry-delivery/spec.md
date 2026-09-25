# Feature Specification: shadcn Registry Delivery

**Feature Branch**: `codex/052-shadcn-registry-delivery`

**Created**: 2026-09-25

**Status**: Approved for implementation

**Input**: S052 implements [#263](https://github.com/shruggietech/shruggie-brand/issues/263). The broader generated-artifact inventory in #269 remains independently open.

## User Scenarios & Testing

### User Story 1 - Discover a truthful registry (Priority: P0)

As a Next.js consumer, I can inspect a public brand catalog and see the actual theme and component items available, their payloads, and their requirements.

**Independent Test**: Generate every production kit, compare catalog entries with individual item payloads, and reject missing, mismatched, or placeholder entries.

**Acceptance Scenarios**:

1. **Given** a generated catalog, **when** a consumer opens it, **then** every advertised item has a resolvable endpoint and a complete description derived from the same item data.
2. **Given** a theme item with no files but real theme variables, **when** it is validated, **then** it remains valid and installable.
3. **Given** an incomplete component item, **when** publication validation runs, **then** it fails before the catalog is copied to public output.

---

### User Story 2 - Install supported items (Priority: P0)

As a consumer of the declared Next.js and Tailwind context, I can install the brand theme and representative components using a pinned shadcn CLI without repairing generated JSON.

**Independent Test**: Install from generated item endpoints in an isolated clean fixture and inspect emitted theme variables and component files.

**Acceptance Scenarios**:

1. **Given** a clean supported consumer, **when** the theme is added, **then** both light and dark tokens become available without changing the kit's approved color values.
2. **Given** an advertised component, **when** it is added, **then** its source file appears at the documented target and can be compiled in its declared context.
3. **Given** an invalid item, **when** validation runs, **then** the failure names the item and cause rather than publishing it.

---

### User Story 3 - Use bundled local fonts (Priority: P1)

As a Next.js consumer, I can connect the kit's approved local fonts without being told an unsupported registry font item is installable.

**Independent Test**: Follow the local font instructions in a temporary consumer and confirm each declared face resolves from the bundled files without font-network requests.

**Acceptance Scenarios**:

1. **Given** the kit's font tree and helper file, **when** they are copied according to the guide, **then** the declared font variables resolve to local files.
2. **Given** the public catalog, **when** a consumer inspects it, **then** it does not advertise a local-font item using an unsupported provider.

### Edge Cases

- Empty files are valid for a theme with usable CSS variables; they are invalid for a declared UI component.
- Catalog and item payloads must agree on names, types, file paths, targets, dependencies, and content without inventing files.
- Names and paths must not allow traversal, duplicate destinations, or references outside the consumer project.
- Valid JSON and HTTP 200 alone do not establish installation or rendered behavior.
- The public static route may display catalog metadata without acting as a shadcn build-source directory. Its purpose must be documented accurately.

## Requirements

### Functional Requirements

- **FR-001**: The generator MUST create catalog and individual payloads from one authoritative typed item collection, with complete matching metadata and no placeholder entries.
- **FR-002**: All advertised items MUST satisfy a pinned shadcn registry contract and have resolvable public endpoints. Valid fileless theme items MUST remain supported.
- **FR-003**: UI items MUST include usable source content, valid target paths, and declared dependencies. Publication MUST reject empty or inconsistent required content.
- **FR-004**: Bundled local fonts MUST remain local. Until supported by the pinned registry contract, the catalog MUST NOT advertise a `registry:font` item for them; the kit MUST provide a working manual font setup.
- **FR-005**: Validation MUST check the complete item/catalog shape, cross-item parity, file and dependency integrity, and exact publication inventory before copying a registry to the site.
- **FR-006**: CI MUST install documented theme and representative component items in isolated clean consumers and verify resulting files, theme variables, and local font wiring.
- **FR-007**: Kit, skill, and hosted guidance MUST distinguish catalog discovery from item installation, state prerequisites and supported versions, and explain manual alternatives.
- **FR-008**: The full documented production-kit, glyph, site, formatting, encoding, and publication checks MUST pass. Source geometry and generated-output exclusion rules remain in force.
- **FR-009**: S052 MUST NOT claim #269's wider artifact audit is complete, recolor existing brands, tag a release, or merge its own pull request.

### Key Entities

- **Registry item**: An installable theme or UI payload with one authoritative set of metadata, dependencies, and files.
- **Public catalog**: A discoverable inventory of those items, derived from the same item collection.
- **Local font bundle**: Approved font binaries and the generated helper that points to them, delivered outside the shadcn CLI.
- **Consumer fixture**: An isolated test project used to prove the documented installation path.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every production catalog item matches its individual item payload, and all advertised endpoints exist in the generated and hosted inventory.
- **SC-002**: The pinned CLI installs a theme and representative UI component in a clean supported consumer with zero manual JSON repairs.
- **SC-003**: All declared local font faces resolve from bundled assets with zero font-network requests.
- **SC-004**: Negative tests reject missing files, empty required UI content, unsafe targets, mismatched names/types, unsupported font providers, and broken dependencies before publication.
- **SC-005**: Complete documented validation and required CI checks pass before owner handoff. Public-route checks following a later release are reported separately from PR checks.

## Assumptions

- The public `/r/registry.json` route is a discovery catalog; direct `/r/{name}.json` endpoints are the supported CLI install path. Source-registry build behavior is not claimed unless separately tested.
- The current shadcn schema supports only Google as a `registry:font` provider. A manual local-font step preserves the repository's bundled-font requirement.
- The implementation does not change the meaning or quality of existing domain row components beyond what installation correctness requires. Broader component semantics belong to #269.
