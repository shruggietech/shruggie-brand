# Research: Complete Kit Downloads and Explicit Brand Actions

## Decision 1: Use one production archive inventory

**Decision**: Export the production brand tuple from `release_contract.py` and consume it from release packaging. Add ESO Weave so the contract covers the same six public brands as the homepage.

**Rationale**: Release metadata and packaging currently repeat a five-brand tuple and omit the sixth public brand. One authoritative tuple prevents another release/site mismatch.

**Alternatives considered**: Discovering arbitrary `dist/*` directories would allow stale or synthetic output into releases. Maintaining a second six-brand site list would preserve the current drift risk.

## Decision 2: Reuse one atomic deterministic archive writer

**Decision**: Extract a writer that stages a complete archive beside its destination, applies stable ZIP metadata, verifies paths, required files, recorded byte counts, hashes, brand identity, version, canon, and licenses, then atomically replaces the destination only after validation.

**Rationale**: Release packaging already contains the correct deterministic primitives and the release contract already checks manifest completeness. Reuse makes the site download byte-equivalent to the release artifact and prevents partial files from surviving a failed build.

**Alternatives considered**: Copying a pre-existing `release/` archive into the site would make ordinary Pages builds depend on a separate command and stale local state. A second site-specific ZIP implementation would drift.

## Decision 3: Publish archives on the same static origin

**Decision**: Materialize each archive at `/<slug>/downloads/<slug>-brand-<version>.zip` and render a same-origin anchor with an exact `download` filename.

**Rationale**: The site is a static export and must be self-contained on every main-branch deployment. GitHub Pages derives the media type from `.zip`, while the anchor download attribute supplies browser download disposition without a custom server.

**Alternatives considered**: Linking only to GitHub Releases would leave newly added brands or current main revisions unavailable until a later tag. A client-generated archive would duplicate inventory logic and require JavaScript.

## Decision 4: Use native HTML disclosure for mobile

**Decision**: Render mobile portfolio entries as `details` and `summary`, with the description and two anchors inside the disclosure panel. Render desktop cards as separate non-interactive articles from the same component and data record, using CSS breakpoints to expose exactly one variant.

**Rationale**: Native disclosure provides expanded state, keyboard activation, focus exclusion while closed, and no-JavaScript operation. A separate desktop article avoids making its header or unused card space interactive.

**Alternatives considered**: A client-state accordion adds hydration and a script-failure mode. Reusing `summary` on desktop would create an unwanted third interactive target.

## Decision 5: Swap desktop content without 3D flipping

**Decision**: Overlay the description and action group in one reserved content stage and transition opacity plus a short vertical translation on hover or focus within. Remove movement under reduced-motion preferences.

**Rationale**: This preserves card dimensions, avoids mirrored text and blank flip phases, and keeps actions stationary under the pointer.

**Alternatives considered**: A 3D card flip adds backface and focus complexity without improving the required action choice. Resizing the card would violate the grid-stability gate.

## Decision 6: Render one generated vendor notice region

**Decision**: Mark only records with a generated vendor boundary and render their complete notices within one portfolio-level aside. Associate each visible asterisk and screen-reader label with that region.

**Rationale**: The full generated notice remains the legal authority while repeated card paragraphs disappear. One container also supports future distinct third-party notices without inventing a generic substitute.

**Alternatives considered**: Retaining the current summary in each card fails the issue. Replacing the full notice with a newly authored sentence would weaken the generated vendor contract.

## Decision 7: Verify archives and UI at complementary layers

**Decision**: Use Python unit tests for deterministic bytes, manifest coverage, atomic replacement, and site publication; Node source tests for exact generated records and markup policy; and Playwright for computed desktop/mobile behavior, accessibility, response media type, ZIP signature, and layout stability.

**Rationale**: No single layer proves both file integrity and rendered interaction. The existing repository gate already runs all three layers.

**Alternatives considered**: Browser-only checks cannot certify archive inventory. Source-only checks cannot prove focus, disclosure, breakpoint, or computed layout behavior.
