# Feature Specification: Authoritative Logo Source Contract

**Feature Branch**: `codex/016-authoritative-logo-contract`

**Created**: 2026-09-07

**Status**: In Review

**Input**: GitHub issue #151, lock approved logo images as authoritative assets and prohibit automatic reconstruction.

## Clarifications

### Session 2026-09-07

- Q: How should existing brands without supplied artwork behave? -> A: Every production brand declares an explicit source mode; existing path-authored brands use `constructed`, while brands whose approved identity is supplied artwork use `authoritative`.
- Q: How should Full and Reduced authoritative variants be bound? -> A: Each variant names its own approved authoritative input ID so distinct masters remain independently protected.
- Q: What may happen to an authoritative mark downstream? -> A: Only declared transformations may produce derivatives, and every exported mark or lockup records its source ID, source hash, variant, and applied transformations.

## User Scenarios & Testing

### User Story 1 - Bind approved marks to immutable sources (Priority: P1)

As a brand owner, I can designate exact approved files as the authoritative Full and Reduced logo masters so the normal build cannot substitute reconstructed geometry while still succeeding.

**Why this priority**: A successful build that publishes a visibly different character violates owner approval and the repository's identity-preservation law.

**Independent Test**: Build a temporary authoritative brand whose approved Full and Reduced inputs are correctly bound, then introduce unrelated constructed paths, a stale hash, a mismatched role, a reference-only input, or a generated construction file and confirm each invalid state is rejected before publishable output is created.

**Acceptance Scenarios**:

1. **Given** approved Full and Reduced image masters with current hashes, **When** the brand is validated, **Then** both variants resolve to the exact declared authoritative inputs and validation succeeds.
2. **Given** authoritative mode and any independently constructed Full or Reduced geometry, **When** validation runs, **Then** the build fails before generation and identifies the conflicting variant.
3. **Given** an authoritative input that is missing, changed, reference-only, assigned the wrong role, or not bound by the logo contract, **When** validation runs, **Then** the build fails with the source ID and reason.
4. **Given** authoritative mode and a `build/mk_paths.py` construction helper, **When** the kit build starts, **Then** the build fails before any logo generation rather than executing or ignoring an ambiguous substitute source.

---

### User Story 2 - Preserve provenance through every derivative (Priority: P1)

As a kit consumer, I can inspect generated logo provenance and know which exact approved source produced every mark and lockup, which transformations were applied, and whether the visible silhouette remained protected.

**Why this priority**: Binding the source is insufficient if later export steps can silently replace or reshape it.

**Independent Test**: Generate an authoritative kit and verify that every SVG mark and lockup plus the logo provenance index names the correct input ID and SHA-256, uses only declared transformations, preserves the authoritative aspect ratio and alpha silhouette for resized or recolored variants, and embeds unchanged bytes when no transformation is declared.

**Acceptance Scenarios**:

1. **Given** an authoritative source approved for unchanged embedding, **When** an unchanged derivative is exported, **Then** the derivative contains the approved source bytes and records no identity-changing operation.
2. **Given** an authoritative raster source approved for recoloring and resizing, **When** color and size variants are exported, **Then** their aspect ratio and alpha silhouette match the source within the documented measurement tolerance.
3. **Given** a horizontal or stacked lockup, **When** it is generated, **Then** the mark remains derived from the bound authoritative source and only placement plus approved wordmark composition is added.
4. **Given** an output requests an undeclared transformation or changes the source silhouette, **When** generation or verification runs, **Then** publication fails and identifies the affected derivative.
5. **Given** generated guidelines and platform icon suites, **When** they reference the identity, **Then** they consume derivatives recorded in the same authoritative lineage rather than independently reconstructed artwork.

---

### User Story 3 - Keep constructed identities explicit and compatible (Priority: P2)

As a maintainer, I can continue generating path-authored brands under an explicit constructed mode while all production definitions, schema guidance, and generated agent instructions clearly distinguish constructed geometry from authoritative supplied artwork.

**Why this priority**: The protection must fail closed without forcing unrelated brands into a supplied-image workflow or changing their existing identities.

**Independent Test**: Migrate all five production definitions to an explicit source mode, rebuild all kits, and confirm constructed brands retain their exact path data while the authoritative ShruggieTech kit uses its approved image masters and every kit passes its normal verification gates.

**Acceptance Scenarios**:

1. **Given** a constructed brand with existing Full and Reduced paths, **When** it is validated and built, **Then** its prior geometry remains byte-for-byte unchanged and the standard glyph gate still applies.
2. **Given** a brand with no source mode or a mode that conflicts with its paths and authoritative inputs, **When** validation runs, **Then** the contract fails with actionable migration guidance.
3. **Given** the repository's production brands, **When** the aggregate build runs, **Then** each definition declares exactly one valid source mode and all generated kits remain shippable.
4. **Given** a future operator using the skill documentation, **When** they approve supplied logo artwork, **Then** the documented workflow directs them to authoritative mode and prohibits tracing, reconstruction, simplification, or replacement without new approval.

### Edge Cases

- Full and Reduced may bind to distinct files, but each binding must use the matching unique `mark` or `reduced-mark` role.
- One file cannot be declared twice under different protected roles, and one authoritative variant cannot fall back to another variant's source.
- SVG sources must remain passive and self-contained; raster sources must retain measurable transparency when silhouette validation is required.
- A source that permits palette analysis but not generated use cannot satisfy an authoritative logo binding.
- An authoritative input may coexist with reference artwork, but reference artwork cannot become a logo source through inference.
- Generated output from an older kit must not satisfy current verification if its provenance index is absent, stale, incomplete, or names an unapproved operation.
- Constructed mode may retain reference-art authoritative inputs, but it cannot use approved mark-role inputs while also claiming independently authored Full or Reduced geometry.
- Platform-specific monochrome and masked variants may transform color, not identity silhouette, and must retain lineage to the correct bound variant.

## Requirements

### Functional Requirements

- **FR-001**: Every production brand MUST explicitly declare `logo.source_mode` as either `constructed` or `authoritative`; omission and unknown values MUST fail validation.
- **FR-002**: Authoritative mode MUST bind both Full and Reduced logo variants to stable authoritative input IDs.
- **FR-003**: A Full binding MUST resolve to one approved `mark` input and a Reduced binding MUST resolve to one approved `reduced-mark` input, with exact current SHA-256 hashes.
- **FR-004**: Authoritative mode MUST reject independently constructed path geometry, inferred source selection, reference-only inputs, mismatched roles, missing files, stale hashes, and duplicate protected sources.
- **FR-005**: Authoritative mode MUST reject a construction helper for the logo mark before that helper can execute or publish output.
- **FR-006**: Constructed mode MUST retain non-empty Full and Reduced path definitions and MUST reject mark-role authoritative inputs that conflict with that declared source mode.
- **FR-007**: Source-mode migration MUST preserve every existing constructed path string and supplied authoritative input byte exactly.
- **FR-008**: The allowed transformation vocabulary MUST distinguish unchanged embedding, recoloring by an existing mask, proportional resizing, and placement in a lockup.
- **FR-009**: Every operation applied to an authoritative source MUST be declared by that source's approved transformation list before generation.
- **FR-010**: Every generated authoritative mark and lockup MUST record its variant, source input ID, source SHA-256, output path, and ordered transformations in a deterministic provenance index.
- **FR-011**: Generated authoritative SVG marks and lockups MUST carry machine-readable source ID and source-hash metadata consistent with the provenance index.
- **FR-012**: Unchanged derivatives MUST embed the approved source bytes directly; resized, recolored, and lockup derivatives MUST preserve the source aspect ratio and alpha silhouette within a documented exact or measured tolerance.
- **FR-013**: Verification MUST reject missing, extra, stale, conflicting, or duplicate provenance records and any output whose declared lineage does not match its embedded source metadata.
- **FR-014**: Verification MUST reject an authoritative raster derivative whose visible alpha silhouette differs from its approved source after accounting only for declared proportional scaling and placement.
- **FR-015**: Guidelines, logo catalogs, favicons, and platform icon suites MUST consume generated derivatives from the same authoritative lineage and MUST NOT construct a substitute logo.
- **FR-016**: The contract, generator, verifier, schema, and operator documentation MUST use the same definitions for source mode, bound variant, authoritative source, derivative, and approved transformation.
- **FR-017**: Validation failures MUST identify the affected brand, variant or derivative, source ID when available, and the violated authority rule before publishable outputs are produced.
- **FR-018**: Regression coverage MUST include every negative and positive case enumerated in issue #151, including unrelated paths, construction helpers, hash drift, valid lockups, valid recolors, silhouette-changing recolors, and unapproved reduced redraws.
- **FR-019**: The aggregate production gate MUST continue to require zero `verify.py` problems and zero `validate_glyph.py` failures for every production kit, with authoritative marks exempted only from constructed-geometry advice that would require redrawing.
- **FR-020**: S016 MUST close issue #151 without changing approved colors, logo geometry, source artwork bytes, public site design, or release versioning.
- **FR-021**: Changing an authoritative variant binding, bound source hash, source artwork, mask method, or visible identity geometry after approval MUST require a new explicit owner approval recorded before generation.

### Key Entities

- **Logo Source Mode**: The required brand-level choice between path-authored construction and immutable approved artwork.
- **Variant Binding**: The explicit association from Full or Reduced to one authoritative input ID with the matching role.
- **Authoritative Input**: The existing immutable supplied-file record carrying path, SHA-256, media facts, usage status, and approved transformations.
- **Logo Derivative**: A generated mark, lockup, or platform input whose identity content descends from one bound source through approved operations.
- **Provenance Index**: Deterministic generated evidence mapping every authoritative logo derivative to its exact source and transformations.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All five production brands declare one valid source mode, and the aggregate build completes with zero contract, verification, and glyph failures.
- **SC-002**: Every authoritative Full and Reduced export and every generated lockup has exactly one matching provenance record with a current source hash and no undeclared transformations.
- **SC-003**: All seven required regression classes from issue #151 pass, and each negative case fails before publishable logo output is created.
- **SC-004**: Measured authoritative resized and recolored raster masks retain 100 percent binary topology agreement with the declared alpha or luminance source mask after deterministic nearest-neighbor normalization.
- **SC-005**: All existing constructed logo path strings and all authoritative source-file hashes remain unchanged from the pre-S016 baseline.
- **SC-006**: A clean checkout can rebuild, verify, package, and publish the static site from source with zero new manual artwork steps and no generated artifacts committed.

## Assumptions

- ShruggieTech is the current production example of authoritative raster masters; Covarity, Fragcap, Glitchpad, and Go Schedule remain constructed in S016.
- Existing approved input records and hashes are trustworthy owner decisions; S016 strengthens their downstream enforcement rather than reopening identity approval.
- Exact alpha comparison is applicable to raster mask derivatives after normalization; passive SVG sources use preserved source bytes and structural lineage rather than raster byte comparison.
- Wordmarks remain generated from approved local typography unless independently declared as authoritative in a future slice.
- No network access, image generation, tracing, or computer-vision similarity judgment is needed for a normal build.

## Scope Boundaries

### In Scope

- Source-mode schema and runtime contract, variant bindings, transformation approval, deterministic derivative provenance, authoritative-output verification, production-brand migration, tests, and operator documentation.

### Out of Scope

- Redesigning or reapproving any identity, importing new supplied artwork, creating a visual approval UI, perceptual similarity scoring, changing brand colors, altering public site presentation, or cutting a release.

## Done When

- Issue #151 is fully covered by synchronized Spec Kit artifacts, all production definitions are migrated without identity drift, all requested regression cases and repository quality gates pass, generated provenance is complete and fail-closed, the official PR has no unresolved review comments, and hosted CI is green.
