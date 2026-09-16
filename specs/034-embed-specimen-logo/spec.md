# Feature Specification: Embed Specimen Logo

**Feature Branch**: `codex/034-embed-specimen-logo`

**Created**: 2026-09-15

**Status**: Complete

**Input**: User description: "Implement GitHub issue #204 for I Heart PR Tours by embedding the missing logo image in the generated type specimen, preserving authoritative identity bytes and geometry, adding dependency and rendered-pixel regression coverage, validating downloadable and hosted copies, completing the repository Spec Kit workflow as S034, and applying the owner's follow-up request to use the wider stacked lockup."

## User Scenarios & Testing

### User Story 1 - Open a complete portable specimen (Priority: P1)

A visitor opens the I Heart PR Tours type specimen directly from the hosted site or from an extracted kit and sees the complete approved mark in the specimen header without any network or neighboring-file dependency.

**Why this priority**: The current published specimen returns successfully but displays a broken-image placeholder, so the primary artifact is visibly incomplete.

**Independent Test**: Build the I Heart PR Tours kit, open the exact generated specimen by direct hosted-style navigation and by offline local file navigation, and confirm that the approved mark is visibly present in both paths.

**Acceptance Scenarios**:

1. **Given** the generated specimen is opened directly in a representative browser, **When** its header is rendered, **Then** the complete approved I Heart PR Tours mark is visible and no broken-image placeholder appears.
2. **Given** the generated specimen is copied without its source asset directory and opened offline, **When** its header is rendered, **Then** the same complete approved mark is visible.
3. **Given** the specimen source is inspected, **When** every `href` and `xlink:href` is enumerated, **Then** each value is either an embedded `data:` payload or an internal fragment reference beginning with `#`.
4. **Given** I Heart PR Tours declares an approved horizontal color lockup, **When** its specimen header is generated, **Then** that wider stacked lockup is used instead of the canonical full mark and is centered without changing its aspect ratio.

---

### User Story 2 - Preserve the approved identity during embedding (Priority: P1)

A brand owner receives the portability repair without any redraw, trace, normalization, substitution, recoloring, or unintended change to the authoritative logo artwork.

**Why this priority**: Portability cannot come at the cost of changing identity source bytes, geometry, placement, proportions, colors, transparency, or the repository's source-preservation boundary.

**Independent Test**: Compare the embedded payload with the governed source bytes and compare the generated specimen placement contract before and after the repair while running the existing identity continuity gates.

**Acceptance Scenarios**:

1. **Given** a governed image-based logo component, **When** it is embedded in the specimen, **Then** the embedded payload decodes to the exact approved source bytes unless an already-governed transformation explicitly applies.
2. **Given** the repaired specimen, **When** its mark group is inspected and rendered, **Then** the mark retains its governed position, dimensions, proportions, colors, and transparency.
3. **Given** all production brands, **When** the full identity verification suite runs, **Then** no existing authoritative logo source or geometry changes.

---

### User Story 3 - Detect future specimen artwork regressions (Priority: P2)

A maintainer receives an automated failure if a generated specimen contains an unresolved image dependency or if its declared mark region renders no visible pixels.

**Why this priority**: Status-only and syntax-only checks allowed the defect to ship, so both structural portability and rendered output must become release gates.

**Independent Test**: Exercise an isolated synthetic brand whose specimen mark contains an image component, prove the pre-fix output fails the new checks, then prove the repaired output passes structural, browser, offline, renderer, downloadable-kit, and hosted-copy checks.

**Acceptance Scenarios**:

1. **Given** an isolated synthetic image-based specimen, **When** its generated SVG retains a relative, filesystem, or network reference, **Then** regression verification fails with an actionable portability error.
2. **Given** a syntactically valid specimen whose mark region renders no visible artwork, **When** rendered-pixel verification runs, **Then** verification fails even if the document returns status 200.
3. **Given** the production I Heart PR Tours specimen, **When** the kit and site publication copies are compared, **Then** both copies are equivalent, self-contained, and visibly complete.

### Edge Cases

- A governed image path may contain characters that require safe URI media payload encoding.
- An image-bearing source may be SVG or another governed raster format, so its media type must match its source format.
- Both modern `href` and legacy `xlink:href` may be present and must resolve to the same self-contained value.
- Internal fragment references beginning with `#` remain valid and must not be rejected as external dependencies.
- A data payload can be structurally present but invalid or empty; rendered-pixel coverage must still reject an invisible mark region.
- The specimen may render through browser navigation, a local `file:` opening, or the repository SVG renderer, and all supported paths must show the mark.
- Synthetic regression inputs must remain isolated from production discovery, publication, registries, archives, and source control.
- Generated outputs under `dist/`, `site/out/`, and other publication directories must remain uncommitted.

## Requirements

### Functional Requirements

- **FR-001**: Generated type specimens MUST embed every governed image-based logo component rather than preserve its source path as an output dependency.
- **FR-002**: Every generated specimen `href` and `xlink:href` value MUST be either a self-contained `data:` payload or an internal fragment reference beginning with `#`.
- **FR-003**: Generated specimens MUST contain no relative path, absolute filesystem path, or external network image dependency.
- **FR-004**: An embedded authoritative source payload MUST preserve the exact governed source bytes and declared media type unless the source contract explicitly authorizes a different existing transformation.
- **FR-005**: Embedding MUST preserve the logo component's governed geometry, placement, proportions, colors, transparency, and SVG presentation attributes.
- **FR-006**: The I Heart PR Tours specimen header MUST display the complete approved mark in representative browser direct-navigation, offline local-opening, and SVG-renderer paths.
- **FR-007**: Generator regression coverage MUST include an isolated synthetic brand whose specimen mark contains an image element.
- **FR-008**: Regression coverage MUST fail when any specimen retains a non-self-contained image reference.
- **FR-009**: Verification MUST inspect rendered visible pixels inside the declared specimen mark region and fail when that region contains no visible artwork.
- **FR-010**: Verification MUST exercise the exact generated I Heart PR Tours specimen rather than a hand-authored or substituted fixture.
- **FR-011**: The downloadable kit specimen and hosted publication specimen MUST contain equivalent self-contained output.
- **FR-012**: Synthetic inputs MUST be created only in isolated temporary storage and MUST remain ineligible for production discovery or publication.
- **FR-013**: The correction MUST be implemented in governed brand source and/or shared generator templates and MUST NOT patch generated output under `dist/`.
- **FR-014**: All production kits MUST complete with zero `verify.py` problems and zero `validate_glyph.py` failures.
- **FR-015**: The full documented Python, generator, publication, release, site, browser, accessibility, identity, Markdown, and repository-hygiene validation MUST pass.
- **FR-016**: Automated checks MUST preserve Python 3.8 compatibility for shared generator and verification code.
- **FR-017**: Specimen generation MUST prefer an approved supplied horizontal color lockup when the governed brand contract declares one, center it at its native proportions within the existing mark grid, and otherwise retain the canonical full/reduced mark fallback.

### Key Entities

- **Governed image component**: A logo path entry whose approved artwork is sourced from a governed file and placed into generated SVG output with declared geometry.
- **Embedded specimen payload**: A media-typed `data:` value containing the governed source bytes within the specimen document.
- **Specimen mark region**: The output-space rectangle occupied by the header mark and used for rendered visible-pixel measurement.
- **Portable specimen**: A generated SVG whose references are exclusively embedded payloads or internal fragments.
- **Publication copy pair**: The downloadable kit specimen and the hosted site copy derived from that same verified generated artifact.
- **Specimen lockup selection**: The governed choice between an approved supplied horizontal color lockup and the canonical full/reduced fallback.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100 percent of `href` and `xlink:href` values in every tested generated specimen are self-contained `data:` payloads or internal `#` references.
- **SC-002**: The embedded I Heart PR Tours mark payload decodes byte-for-byte to its authoritative source, with zero source or geometry changes.
- **SC-003**: The I Heart PR Tours mark region contains visible non-background pixels in every representative browser, offline/local, and SVG-renderer check.
- **SC-004**: The downloadable and hosted I Heart PR Tours specimens are equivalent and each passes the same self-containment and rendered-pixel checks.
- **SC-005**: The isolated image-component regression fails for unresolved references and invisible mark output, then passes with the repaired generator.
- **SC-006**: Every production kit reports zero verification problems and zero glyph failures.
- **SC-007**: The complete documented repository validation finishes with zero failing required gates and records any unavailable optional renderer as an explicit skip.
- **SC-008**: The I Heart PR Tours embedded payload equals `horizontal_darkbg.svg` byte-for-byte, uses centered `297` by `183.75` serialized geometry, and leaves the authoritative horizontal and vertical source files unchanged.

## Scope

### In Scope

- Shared type-specimen generation for governed image-based logo components.
- I Heart PR Tours specimen portability and visible mark rendering.
- Structural reference validation, decoded-payload identity checks, and rendered-pixel checks in the generator regression harness.
- Direct browser navigation, offline/local opening, SVG-renderer coverage, and kit-to-hosted-copy equivalence.
- Spec Kit artifacts, changelog entry, and local commit for S034.

### Out of Scope

- Redrawing, tracing, normalizing, optimizing, recoloring, or substituting any authoritative logo source.
- Changing I Heart PR Tours logo geometry, placement, proportions, approved colors, transparency, or identity approvals.
- Patching or committing generated kits, site exports, PDFs, PNGs, registries, archives, or other `dist/` content.
- Changing unrelated specimens, site navigation, brand copy, or release versioning except where shared regression coverage proves no breakage.
- Publishing, pushing, tagging, releasing, or deploying the change.

## Assumptions

- Issue #204 is the authoritative acceptance source and its listed preservation boundaries are final.
- Base64-encoded media data is an acceptable self-contained representation because it preserves governed source bytes exactly and is already used by repository identity flows.
- The existing header mark grid and outer placement are correct. The owner-requested wider lockup may use its approved native dimensions centered within that grid rather than inheriting the canonical full mark's component geometry.
- Existing browser and SVG rasterizer infrastructure can be extended to measure the exact generated specimen without committing rendered artifacts.
- The repository is a public static brand system with no authentication, private user data, tenant boundary, or mutable user input. Security coverage applies to safe local source resolution, URI containment, and publication-path integrity.

## Dependencies

- [GitHub issue #204](https://github.com/shruggietech/shruggie-brand/issues/204) defines the defect and acceptance criteria.
- `brands/i-heart-pr-tours/brand.json` identifies the approved image-based full mark, authoritative input inventory, and supplied horizontal color lockup.
- `skill/templates/build_specimen.py` emits the shared type specimen.
- Existing pipeline, identity, publication, site, and renderer verification provide the regression and release-gate foundation.
