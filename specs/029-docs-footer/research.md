# Research: Documentation Footer Removal

## Decision 1: Remove the footer at the documentation page composition boundary

**Decision**: Remove the `Footer` import and `<Footer />` element from `site/app/docs/[[...slug]]/page.tsx`, then remove the obsolete `.docs-page .site-footer` spacing selector from `site/app/globals.css`.

**Rationale**: The documentation page is the only place that opts into the shared marketing footer. Removing it there keeps route ownership explicit, prevents the element from entering the document and accessibility tree, and leaves the marketing layout's footer behavior untouched. Removing the dead selector prevents stale route coupling and a future footer-sized spacing regression.

**Alternatives considered**: A pathname-aware conditional inside `Footer` would introduce route coupling into a stable presentation component. CSS-only hiding would leave unnecessary markup and could preserve spacing or accessibility problems. Moving pagination was unnecessary because Fumadocs already owns the correct contextual footer slot.

## Decision 2: Preserve the shared footer component and its policy tests

**Decision**: Do not edit `site/components/footer.tsx`; retain the existing footer records and homepage rendering assertions.

**Rationale**: Issue #191 is about route scope, not footer content. Keeping the component unchanged narrows regression risk and preserves the ordered link and browsing-context decisions from S023.

**Alternatives considered**: Creating a documentation-specific footer variant would add an unused concept. Deleting the shared footer would regress the main marketing surface.

## Decision 3: Test source composition and rendered route behavior

**Decision**: Add source-contract assertions for import and render absence, then verify zero `.site-footer` elements across all documentation routes and retained pagination at desktop and narrow widths.

**Rationale**: Source checks fail quickly if the component is reintroduced, while rendered checks prove the export and accessibility-facing DOM satisfy the route boundary. Both are needed because either layer alone could miss a future composition regression.

**Alternatives considered**: A screenshot-only regression would be brittle and is prohibited as a byte-identity gate. Testing only one documentation article would not prove the shared route contract across the complete inventory.
