# Research: Site Interaction Affordances

## Decision 1: Encode footer behavior as explicit destination metadata

**Decision**: Define the six existing footer destinations once in the shared footer component and attach a separate-context policy only to Download the skill, Source, and License.

**Rationale**: Issue #163 explicitly requires Company to remain same-tab even though it uses another hostname. An explicit record is deterministic, reviewable, and safe for future links.

**Alternatives considered**: Hostname inference was rejected because it would incorrectly change Company. Repeating attributes in markup was rejected because policy could drift between links or future footer instances.

## Decision 2: Preserve dependency semantics and correct presentation through narrow selectors

**Decision**: Retain the dependency-rendered pagination links, chevrons, label groups, and theme buttons. Apply site-owned selectors beneath `.docs-pagination` and `[data-theme-toggle]` to normalize alignment, icon sizing, and cursor state.

**Rationale**: The dependency already emits links, buttons, accessible labels, selected styling, and theme-change behavior. The defects are presentational, so replacing or wrapping the components would create avoidable maintenance and accessibility risk.

**Alternatives considered**: Forking dependency components was rejected as disproportionate. Route-specific offsets were rejected because wrapping and responsive widths require one shared contract.

## Decision 3: Measure real rendered relationships

**Decision**: Extend Playwright verification to compare chevron and complete label-group vertical centers, inspect icon dimensions and shrink behavior, and read cursor plus semantic state from the actual theme controls.

**Rationale**: A source substring can prove that a selector exists but cannot prove the dependency DOM matches it or that the visible cue is centered. Rendered measurements catch integration drift.

**Alternatives considered**: Screenshot-only review was rejected as subjective and non-blocking. Exact pixel snapshots were rejected because cross-platform antialiasing is irrelevant to box alignment.

## Decision 4: Use representative route shapes plus the existing full visual sweep

**Decision**: Exercise `/docs/`, one interior page with two neighbors, and the terminal documentation page, at 360 and 1280 CSS pixels in both themes. Retain the existing complete route and accessibility verification.

**Rationale**: These routes cover one-card next-only, two-card previous/next, and one-card previous-only pagination structures without multiplying redundant checks across identical shared markup.

**Alternatives considered**: Measuring every documentation page was rejected as redundant and slower. Checking only the index was rejected because it omits previous and two-card layouts.

## Decision 5: Treat disabled cursor behavior as a contract even when current controls are enabled

**Decision**: Style enabled buttons with `pointer` and disabled buttons with the established disabled cursor, and cover both selector states with static negative fixtures. Rendered checks require the current light/dark control to remain enabled and semantically selected through existing cues.

**Rationale**: This prevents a future disabled state from looking actionable while satisfying the current issue without inventing disabled behavior in the live UI.

**Alternatives considered**: Applying `cursor: pointer` indiscriminately was rejected because it would misrepresent disabled controls. Disabling the current theme was rejected because the dependency models the switcher as an enabled toggle.
