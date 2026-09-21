# Feature Specification: Immutable Kit Publication

**Feature Branch**: `codex/043-immutable-kit-publication`

**Created**: 2026-09-20

**Status**: Pull request review in progress

**Input**: User description: "Use Spec Kit autopilot to correct the release/site version skew, give generated brand kits an immutable package identity, reconcile release notes, and explain identity versus implementation changes without tracking downstream utility."

**Issues**: [#233](https://github.com/shruggietech/shruggie-brand/issues/233), [#234](https://github.com/shruggietech/shruggie-brand/issues/234), [#235](https://github.com/shruggietech/shruggie-brand/issues/235), and slice [#222](https://github.com/shruggietech/shruggie-brand/issues/222), under parent [#209](https://github.com/shruggietech/shruggie-brand/issues/209)

## Clarifications

### Session 2026-09-20

- Q: What may the production brand site represent when `main` is ahead of the latest formal release? → A: Production represents only an exact formal release; unreleased `main` output remains a CI artifact and is not deployed as production.
- Q: How should an unchanged brand identity distinguish kits built by different BrandBuilder releases? → A: Add an immutable kit-package identity derived from the brand version and BrandBuilder release while leaving the brand identity version unchanged.
- Q: What downstream evidence is required? → A: None; BrandBuilder publishes migration impact and compatibility facts but does not track consumer adoption or utility.
- Q: What release version should carry the incompatible archive naming and consumer-contract changes? → A: Use BrandBuilder `2.0.0`; `1.3.0` was never published, and assigning a major version before the first release of the new layout preserves semantic versioning.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Download one coherent released system (Priority: P1)

As a brand-kit user, I can trust that the production site, its skill download, its kit downloads, and their displayed version facts all represent one exact formal release.

**Why this priority**: A production site that serves newer generated contracts while linking an older compiler cannot be reproduced or recovered reliably.

**Independent Test**: Compare the production publication record, site metadata, skill action, generated kit metadata, and release record for one release candidate; every surface identifies the same formal release, and an unreleased candidate is rejected from production deployment.

**Acceptance Scenarios**:

1. **Given** a verified tagged release, **When** production publication is prepared, **Then** the site, skill action, kit downloads, and release artifacts identify that exact tag and release version.
2. **Given** verified `main` is ahead of the latest tag, **When** continuous integration completes, **Then** reviewable candidate artifacts remain available without replacing production Pages.
3. **Given** a stale or moving skill destination, **When** publication validation runs, **Then** production publication fails before deployment.

---

### User Story 2 - Pin an immutable generated kit (Priority: P1)

As an integrator, I can distinguish two generated kits that share the same approved brand identity version but were built by different BrandBuilder releases or governed contract bundles.

**Why this priority**: Reusing one archive name and production URL for different bytes defeats exact pinning, caches, checksums, and offline recovery.

**Independent Test**: Build the same unchanged brand against two release identities and confirm that the canonical archive identities differ, while the declared brand identity version remains unchanged.

**Acceptance Scenarios**:

1. **Given** an unchanged brand at version `1.0.0`, **When** BrandBuilder advances from one release to another, **Then** the kit-package identity and archive name change while the brand identity remains `1.0.0`.
2. **Given** a kit archive, **When** its filename, manifest, source revision, release identity, or checksum authority disagrees, **Then** package and publication verification fail closed.
3. **Given** an older brand-only archive name, **When** a user follows current guidance, **Then** the legacy form is identified as non-canonical and never acts as a mutable alias for newer bytes.

---

### User Story 3 - Understand migration impact without identity confusion (Priority: P2)

As a consumer evaluating a new kit, I can read one generated bundle record and migration summary that distinguish unchanged approved identity from changes to palette semantics, typography, platform assets, Web/React contracts, egui contracts, or other implementation surfaces.

**Why this priority**: The complete version tuple is precise, but without a summary it is easy to mistake implementation changes for a logo redesign or assume every surface requires migration.

**Independent Test**: Inspect hosted, bundled, portable, and release guidance for a release with unchanged identity and changed implementation contracts; each presentation derives the same bundle facts and makes the same migration classification.

**Acceptance Scenarios**:

1. **Given** unchanged identity geometry and a newer implementation bundle, **When** migration guidance is generated, **Then** it explicitly reports no identity redesign and names only the affected implementation surfaces.
2. **Given** a consumer that does not use an affected adapter, **When** it reads the migration summary, **Then** that surface is classified as optional or no-op rather than universally required.
3. **Given** any generated guidance surface, **When** its bundle facts drift from the governed record, **Then** validation rejects the publication.

### Edge Cases

- A release tag exists but does not match the compiler version declared by the tagged source.
- The site was last deployed from an unreleased `main` revision before tag-only production publication is introduced.
- A brand version changes in the same release as the compiler version.
- Two builds use the same version tuple but different source revisions or archive bytes.
- A legacy archive name is linked by old documentation or an external cache.
- A release changes only documentation or verification behavior and requires no consumer implementation migration.
- An adapter changes while identity geometry, palette authority, and typography remain unchanged.
- Release notes omit earlier commits that are already included in the declared release version.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Production publication MUST represent one exact formal release across the site, skill action, kit downloads, version facts, release notes, and checksums.
- **FR-002**: Unreleased `main` output MUST remain verifiable without being presented through the production site as an immutable released delivery.
- **FR-003**: Production publication MUST fail closed when the release tag, declared compiler version, source revision, changelog boundary, skill destination, or artifact metadata disagree.
- **FR-004**: The public skill action MUST identify and resolve to the exact formal release represented by production content rather than an unqualified moving destination.
- **FR-005**: Every generated brand kit MUST have an immutable package identity distinct from the governed brand identity version.
- **FR-006**: The package identity MUST distinguish kits when the brand version is unchanged but the BrandBuilder release or governed contract bundle changes.
- **FR-007**: Canonical archive names, hosted paths, manifests, release assets, checksums, and recovery records MUST agree on the same package identity.
- **FR-008**: Every kit MUST declare its brand version, BrandBuilder release, complete compatible contract tuple, source revision, canonical package filename, and checksum authority through one governed bundle record.
- **FR-009**: Verification MUST reject archive filenames, bundle records, source revisions, release identities, recovery records, or checksums that disagree.
- **FR-010**: Legacy brand-only archive names MUST be documented as non-canonical and MUST NOT become mutable aliases for current package bytes.
- **FR-011**: Brand identity versions MUST retain their existing semantic meaning and MUST NOT advance solely because generated implementation artifacts changed.
- **FR-012**: One governed release-impact record MUST classify identity, palette semantics, typography, platform assets, Web/React contracts, egui contracts, documentation, and recovery impact for the release.
- **FR-013**: Human-readable migration guidance MUST derive from the governed bundle and impact records and distinguish required compatibility work, optional capability adoption, and unaffected surfaces.
- **FR-014**: Hosted, bundled, portable, and release guidance MUST present consistent bundle and migration facts and MUST fail drift validation when they disagree.
- **FR-015**: The `2.0.0` changelog boundary and generated notes MUST include every change shipped by `2.0.0`, including work previously staged under the unpublished `1.3.0` heading, and exclude later unreleased work.
- **FR-016**: Release assets MUST continue to be built by CI from the exact tagged revision; S043 MUST NOT create a release tag or publish a release before owner merge authorization.
- **FR-017**: All production kits MUST retain zero verifier problems and zero glyph failures, and applicable publication surfaces MUST retain WCAG 2.1 AA.
- **FR-018**: Approved logo geometry, authoritative source bytes, affiliation, ownership, and inheritance boundaries MUST remain unchanged.
- **FR-019**: Generated records and guidance MUST use UTF-8 without BOM, LF line endings, and contain no mojibake.
- **FR-020**: BrandBuilder MUST NOT require, collect, or report named downstream adoption, productivity, utility, correction-round, elapsed-time, escaped-defect, or handover evidence.
- **FR-021**: The implementation and pull request MUST trace to #233, #234, #235, #222, and parent #209 with closure language that does not claim a release was published before it exists.
- **FR-022**: Every governed change that can alter generated kit bytes, bundle fields, or compatibility semantics MUST require a BrandBuilder version change so the canonical package identity cannot be reused for a different governed bundle.
- **FR-023**: Generated publication metadata MUST identify whether it is an unreleased candidate or an exact formal release, and only exact formal release metadata MAY pass the production deployment gate.

### Key Entities

- **Formal Release**: An immutable tagged BrandBuilder publication with exact source revision, release version, notes, assets, and checksums.
- **Kit Package Identity**: The immutable identity of one generated brand-kit bundle, separate from its brand identity version.
- **Bundle Record**: The single machine-readable bill of materials for brand, compiler, canon, recipe, adapter, source, filename, and checksum authority.
- **Release Impact Record**: Governed classification of identity and implementation surfaces changed by one BrandBuilder release.
- **Migration Summary**: Generated human-readable guidance derived from bundle and impact records.
- **Production Publication**: The public site and downloadable artifacts representing one formal release.
- **Candidate Artifact**: Verified output from an unreleased revision that remains outside production publication.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One hundred percent of production site version facts, skill destinations, kit downloads, release assets, and checksums identify the same formal release.
- **SC-002**: Zero unreleased compiler versions can pass the production deployment gate.
- **SC-003**: Across all production brands, zero canonical archives share a filename or production URL when their BrandBuilder release identity differs.
- **SC-004**: Every production kit contains exactly one valid governed bundle record and one consistent generated migration summary.
- **SC-005**: One hundred percent of bundle fields agree across archive filename, kit manifest, consumer recovery metadata, hosted registry, and release contract.
- **SC-006**: All unchanged brand identities retain their current brand version and authoritative geometry hashes.
- **SC-007**: The full documented local validation and hosted CI complete successfully, every production kit reports zero verifier problems and zero glyph failures, and publication accessibility retains zero WCAG 2.1 AA violations.
- **SC-008**: The pull request receives bounded review with every actionable finding addressed and resolved before owner merge.
- **SC-009**: No generated kit, archive, site export, PDF, raster output, registry, or release artifact is committed.
- **SC-010**: No generated or authored guidance requires downstream adoption or utility evidence.

## Assumptions

- The existing independent semantic versions remain authoritative; S043 adds a package identity rather than collapsing version domains.
- BrandBuilder release `1.3.0` remains unpublished and is superseded by `2.0.0` because the archive identity and consumer-contract layout change incompatibly.
- Production Pages should be release-backed; continuous `main` candidates remain available through CI artifacts rather than a public production route.
- The next formal release and any post-merge production correction remain separately owner-authorized actions.
- Existing release verification, checksummed recovery, and generated documentation contracts are extended rather than replaced.
