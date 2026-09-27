# Feature Specification: Shared Asset Language and Distinct Download Cards

**Feature Branch**: `codex/058-asset-language-download-cards`

**Created**: 2026-09-26

**Status**: Ready for Review

**Input**: S058 implements issues #283 and #284 under Spec Kit and autopilot. Define one plain-English asset grammar and present each distinct design in its own expandable download card while preserving existing deliveries and URLs.

## Clarifications

- **2026-09-26, approval boundary**: Existing logo derivative filenames and bytes remain in each approved Gate 2 manifest. New descriptive delivery names are separately verified publication aliases, not retroactive changes to approved identity derivatives. Every alias must bind to one exact existing source path and digest.
- **2026-09-26, routes**: Asset-file names and labels may evolve; brand guideline page routes remain stable in S058. Issue #285 owns canonical page-route migration.
- **2026-09-26, versioning**: A backward-compatible compiler minor bump is appropriate for new governed delivery metadata and aliases. Brand Canon stays at its current version if source identity meaning and approved paths remain unchanged.
- **2026-09-26, provenance**: Approved legacy provenance fields remain byte-identical. A generated semantic companion record maps their values to the new independent axes and explicitly identifies aliases. Reader-facing surfaces consume the companion record rather than reinterpreting legacy fields.
- **2026-09-26, card sizes**: The owner confirmed that visually identical artwork at different sizes belongs under one card. A card with options presents size variants of its face design. The face uses SVG when supplied, otherwise the smallest raster sharp enough for the displayed card (or the largest available raster when all are smaller).
- **2026-09-26, signed sources**: Some brand READMEs are included in approved source-byte inventories. They remain byte-identical; the new glossary and generated companion records explain legacy wording without changing their approvals.
- **2026-09-26, icon backgrounds**: Icon alpha determines whether its file has a clear or opaque background. Appearance values such as light-unplated describe the intended viewing surface separately; an opaque default icon must never be labeled clear.

## User Scenarios & Testing

### User Story 1 - Understand the right asset (Priority: P1)

A reader can distinguish a brand kit from a guide, a mark from a wordmark or paired lockup, and a social share image from a logo. The reader can identify artwork treatment, background suitability, size, and format from a consistent name.

**Why this priority**: The vocabulary and metadata in #283 are required by the downloads redesign in #284.

**Independent Test**: A reader uses the glossary and one generated guide to choose an asset for a stated use without interpreting ambiguous `color`, `light`, `black`, or repeated technical labels.

**Acceptance Scenarios**:

1. **Given** wide and stacked full-color lockups, **when** the reader inspects the guide or manifest, **then** distinct names identify layout and purpose.
2. **Given** transparent, light-background, dark-background, and monochrome deliveries, **when** the reader compares them, **then** background and ink meanings are separate and unambiguous.
3. **Given** a social share image, **when** the reader inspects the kit, **then** it has a distinct role and is never called a logo lockup.

---

### User Story 2 - Browse one design per card (Priority: P1)

A visitor sees a separate representative card for every genuinely distinct design and purpose. Sizes, formats, and true aliases of that design remain within its card.

**Why this priority**: Issue #284 is a user-visible grouping defect across all brand portals.

**Independent Test**: Each applicable portal shows wide lockup, stacked lockup, and social share image as distinct cards, each expanding only its own deliveries.

**Acceptance Scenarios**:

1. **Given** a brand with wide and stacked lockups and a social image, **when** downloads appear, **then** three distinct cards have matching heading, preview, usage hint, and files.
2. **Given** a supplied-lockup brand without a standalone wordmark, **when** downloads appear, **then** no wordmark card is invented and all actual assets remain available.
3. **Given** an icon or monochrome variant, **when** purpose, layout, foreground, or background treatment differs, **then** it cannot be grouped under an unrelated representative.

---

### User Story 3 - Continue using old links (Priority: P2)

A downstream consumer using a current direct kit or hosted download path can still retrieve the same asset after names become clearer.

**Why this priority**: Existing consumers pin immutable packages and direct links.

**Independent Test**: An old-to-new path map covers changed public names and existing direct URLs resolve to the corresponding bytes in the new kit and site.

**Acceptance Scenarios**:

1. **Given** a legacy filename, **when** a consumer requests its existing path, **then** a compatibility alias or redirect resolves to the same design and size/format.
2. **Given** multiple sizes or SVG and PNG renditions, **when** the new catalog is built, **then** every former delivery remains present and canonical entries are distinguishable from aliases.

### Edge Cases

- A supplied identity may have a lockup but no independent wordmark. Available source forms govern cards and labels.
- Mark-only, wordmark-only, icon, monochrome, platform, and social assets may lack layout or ink axes. Not-applicable values must remain explicit.
- Clear means transparent; light and dark describe intended backgrounds; black and white describe monochrome ink. Intended background is distinct from actual opaque image pixels.
- A compatibility alias must not create a second design card or lose provenance.
- Different semantic uses can have identical bytes. Role and intended use still govern grouping.

## Requirements

### Functional Requirements

- **FR-001**: Publish one central glossary with short layperson definitions and examples of brand kit, brand guide/guidelines, brand mark, logomark/icon, lettermark, wordmark, logo lockup/lockup, wide lockup, stacked lockup, full color, monochrome, slogan, description, and social share image. Define legacy terms as aliases or retire them deliberately.
- **FR-002**: Define and apply a human-readable asset grammar separating purpose/role, form, layout, color treatment, background, foreground ink where relevant, size, and format. Clear/light/dark refer to backgrounds; black/white refer to ink. Unused axes have explicit not-applicable semantics.
- **FR-003**: Companion semantic provenance and manifests, downloadable filenames, guide/PDF/portable/site labels, alt text, and shared main documentation use the same meanings across all eight brands and future brands. Approved legacy provenance and approval-bound source documents remain intact with an explicit companion mapping to those meanings.
- **FR-004**: Every generated brand guide and dedicated sub-documentation page defines a term at first use or links directly to its central glossary definition.
- **FR-005**: Canonical names distinguish wide/stacked, full color/monochrome, clear/light/dark backgrounds, black/white ink, and social share images from logo roles when applicable.
- **FR-006**: Generated catalog and hosted downloads UI share an explicit design identity containing enough role, form, layout, treatment, background, and ink axes to prevent unrelated designs sharing one card. Where the generator reuses the same artwork for several delivery roles, one card may list those roles with their destinations.
- **FR-007**: A card's heading, preview, usage hint, filters/search terms, and expanded file list describe the same design. Sizes, formats, and true aliases remain within that design.
- **FR-007a**: Size differences alone never split visually identical deliveries into separate cards. The card face uses an optimally sized supplied variant and its expanded options expose all delivered sizes without mixing other artwork.
- **FR-008**: All existing distinct deliverables and usable direct paths remain available. Publish an old-to-new name/path map with canonical names and aliases or redirects. Kit, site, and release inventories remain complete.
- **FR-009**: The expanded card library supports keyboard and screen readers, visible focus, responsive layout, and WCAG 2.1 AA contrast.
- **FR-010**: Preserve approved logo geometry byte-for-byte; do not claim absent standalone assets.
- **FR-011**: Contract and reader-task checks reject ambiguous or duplicate labels, mixed-design cards, broken aliases, and meaning drift across hosted guides, portable HTML, PDF guidance, manifests, and source examples.

### Key Entities

- **Vocabulary entry**: Canonical term, definition, examples, aliases, and stable glossary anchor.
- **Asset design**: One recognizable composition and use, identified by independent semantic axes and one representative.
- **Asset delivery**: A size/format rendition or compatibility alias of one design, with path, provenance, and bytes.
- **Download card**: Hosted projection of one design and its deliveries.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All eight production brands have unambiguous design labels and accessible first-use glossary paths in hosted and portable guides; the glossary contains every FR-001 term.
- **SC-002**: Every applicable brand has separate wide, stacked, and social image cards, and no card mixes distinct visual layout, treatment, background, or ink values. Reused web artwork may include favicon, touch, and installable sizes under one face.
- **SC-003**: Every pre-S058 public asset path resolves to the same design and size/format; canonical and alias inventories reconcile exactly.
- **SC-004**: All eight kits report zero `verify.py` problems and zero `validate_glyph.py` failures; site and catalog pass documented validation including WCAG 2.1 AA.
- **SC-005**: A reader-task review identifies a requested wide or stacked lockup, social image, and monochrome variant from closed cards without opening unrelated designs.

## Assumptions

- Issue #285's guideline page route migration is a later slice. S058 preserves current page URLs and focuses on asset names, file paths, and download presentation.
- Approved social images from S057 are reused unchanged. Renaming or aliasing delivery paths does not approve new identity pixels.
- Existing source and generated kit bytes determine which optional forms exist; no standalone wordmark is synthesized for a supplied-lockup brand.
- S058 does not cut a formal release. The PR carries version and migration guidance appropriate to implementation; publication is separately authorized.
