# Data Model: Glitchpad Identity Color Approval

## Candidate matrix

- **Identifier**: Stable direction key and human-readable name.
- **Status**: `exploratory`, `approved`, `adjustment-requested`, or `rejected`.
- **Context mappings**: Dark and light values for surface, permanent square, square edge, paper, fold, and wordmark.
- **Monochrome mappings**: Black and white delivery roles, normally unchanged.
- **Validation**: Six-digit hexadecimal values, complete required roles, explicit inapplicable roles, no implicit fallback between dark and light contexts.

## Comparison context

- **Identifier**: Surface, asset form, rendered size, and platform presentation.
- **Asset forms**: Full mark, reduced mark, horizontal lockup, stacked lockup, launcher tile, and store artwork.
- **Sizes**: 16, 24, 32, 48, and large reference pixels where applicable.
- **Invariant**: Every mark uses one square canvas and safe enclosure around byte-identical rectangular page paths. Geometry, scale, location, and labels are identical across candidate directions.

## Contrast observation

- **Candidate and context**: References one candidate matrix and comparison context.
- **Relationship**: Foreground/background or adjacent-fill pair.
- **Values**: Two exact hexadecimal values, measured WCAG ratio, applicable threshold, and pass/fail disposition.
- **Interpretation**: Objective measurement only; aesthetic approval remains an owner decision.

## Geometry fingerprint

- **Protected inputs**: Ordered `logo.paths.full`, `logo.paths.reduced`, canvas dimensions, lockup dimensions, and canonical path strings.
- **Value**: SHA-256 over a stable serialized representation.
- **Lifecycle**: Captured before comparison, asserted during study generation, and compared after implementation.

## Owner disposition

- **State**: `approved`, `adjustment-requested`, or `rejected`.
- **Direction**: Candidate identifier, omitted only when all candidates are rejected.
- **Adjustments**: Exact bounded role/value changes when requested.
- **Rationale**: Owner-authored or owner-confirmed identity reasoning.
- **Transition**: `exploratory` to one disposition; only `approved` authorizes production source changes.

## Approved identity matrix

- **Source authority**: `brands/glitchpad/brand.json` after approval.
- **Roles**: Permanent square, square edge, full-mark paper/fold, reduced page, wordmark, black, and white.
- **Consumers**: Shared logo generator, icon generator, guidelines, specimens, registries, site materialization, and tests.
- **Absent behavior**: Any new optional shared role leaves sibling brand output unchanged when omitted.
