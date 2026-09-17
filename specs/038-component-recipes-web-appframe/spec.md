# Feature Specification: Component Recipes and Web AppFrame

**Feature Branch**: `codex/038-component-recipes-web-appframe`

**Created**: 2026-09-17

**Status**: Ready for Planning

**Input**: User description: "Deliver S038 under Spec Kit autopilot as the next tightly packed slice, closing GitHub issues #214 and #215 by defining the bounded shared component-recipe contract and generating the shared Web/React adapter and application shell."

## Clarifications

### Session 2026-09-17

- Q: Does the initial contract include every component family named by the architecture work order? -> A: Yes. The contract and generated adapter cover all 14 named families through 15 recipes, splitting Field semantics from native form-control behavior so the slice can close #214 and #215 without an ambiguous partial vocabulary.
- Q: Who owns application-level environment adaptation? -> A: AppFrame owns every application-level boundary by default, with a host allowed to take one responsibility only through an explicit single-owner handoff.
- Q: Does the minimum specimen work close the broader conformance issue? -> A: No. S038 emits reusable fixtures and checks required to validate this adapter, while #217 remains open for cross-runtime baselines, comparison reporting, and the full conformance harness.

## User Scenarios & Testing

### User Story 1 - Author bounded component recipes (Priority: P1)

As a design-system maintainer, I can define a shared component through a bounded recipe that references semantic interface roles, declares supported variants and states, and preserves accessibility and behavior invariants without describing arbitrary product screens.

**Why this priority**: A validated recipe vocabulary is the contract that makes renderer adapters comparable and prevents component behavior from drifting into local product conventions.

**Independent Test**: Validate the complete initial recipe catalog and representative invalid mutations, confirming that unknown roles, missing states, invalid variants, inaccessible behavior, unbounded composition, and prohibited brand overrides fail closed.

**Acceptance Scenarios**:

1. **Given** a recipe for any initial shared component, **When** a maintainer inspects it, **Then** the recipe identifies semantic role assignments, supported variants and densities, required interaction states, keyboard behavior, target size, accessible naming, focus behavior, motion behavior, responsive adaptation, and permitted brand overrides.
2. **Given** a recipe that uses a raw visual value, omits a required accessible behavior, or attempts to define an arbitrary screen, **When** validation runs, **Then** generation stops with an actionable diagnostic naming the component and violated rule.
3. **Given** a brand-specific override, **When** validation runs, **Then** only explicitly permitted expressive assignments are accepted and invariant behavior remains unchanged.

---

### User Story 2 - Consume a shared web adapter (Priority: P2)

As a Web or React application maintainer, I can consume framework-neutral semantic tokens and generated shared components whose appearance and behavior derive from the pinned BrandBuilder contract rather than local literal styling.

**Why this priority**: The first production adapter proves that Interface Canon and component recipes can compile into useful application code while keeping the contract portable to later runtimes.

**Independent Test**: Generate a production kit and use its web outputs in both server-aware and client-interactive specimens, verifying semantic token availability without React, component export completeness, accessible behavior, and the absence of ungoverned visual literals.

**Acceptance Scenarios**:

1. **Given** a consumer that does not use React, **When** it loads the generated web token layer, **Then** it can style compatible controls using stable semantic custom properties.
2. **Given** a React consumer, **When** it imports the generated adapter, **Then** it receives the complete initial component vocabulary with accessible defaults and recipe-governed variants.
3. **Given** a server-rendering environment, **When** it imports server-safe exports, **Then** no browser-only global is evaluated before client hydration.
4. **Given** a component with interactive behavior, **When** a keyboard, touch, reduced-motion, forced-color, or scaled-text capability is active, **Then** the declared behavior remains operable and perceivable.

---

### User Story 3 - Establish one application-frame owner (Priority: P3)

As an application shell maintainer, I can use one AppFrame contract that owns safe areas, titlebar regions, root scrolling, fixed chrome, IME obstruction, and the global focus boundary without double-applying host insets.

**Why this priority**: Shared components remain unreliable across browser and desktop-web hosts unless the shell has a single, explicit ownership boundary for environment-sensitive layout.

**Independent Test**: Exercise browser, Tauri-style, and Wails-style host fixtures across compact, expanded, touch, keyboard, safe-area, titlebar, IME, reduced-motion, and forced-color profiles, then prove that a dual-owner configuration is rejected.

**Acceptance Scenarios**:

1. **Given** a browser host without native window chrome, **When** AppFrame resolves its environment, **Then** it owns document scrolling and safe-area adaptation while leaving titlebar regions empty.
2. **Given** a native webview host that owns an inset, **When** AppFrame receives the host handoff, **Then** the inset is applied exactly once and window-control regions remain unobstructed.
3. **Given** an on-screen keyboard or IME obstruction, **When** focused content would be covered, **Then** AppFrame exposes the obstruction and preserves a usable focus path without globally disabling scrolling.
4. **Given** conflicting declarations that both the host and AppFrame own the same boundary, **When** validation runs, **Then** generation or verification fails closed with an ownership diagnostic.

### Edge Cases

- A recipe references a semantic role that exists in another theme but not in the resolved contract.
- A component state combines disabled, busy, selected, expanded, or invalid flags in a contradictory way.
- An icon-only control has no accessible name or has a visual target smaller than the invariant minimum.
- A menu, dialog, tab set, or toast is rendered without the keyboard, focus, dismissal, or announcement behavior required by its recipe.
- A server-rendered entry point is imported where `window`, `document`, or layout measurement is unavailable.
- A host reports mixed capabilities that contradict an operating-system stereotype.
- Safe-area and titlebar regions overlap, or the IME consumes nearly the entire usable viewport.
- Forced colors remove decorative fills, reduced motion disables transitions, or text scaling causes navigation and action labels to wrap.
- A consumer requests an unsupported variant or tries to pass a raw color, pixel measure, or font family through a component property.
- A production brand has no component-specific override and must inherit the shared defaults without identity drift.

## Requirements

### Functional Requirements

- **FR-001**: BrandBuilder MUST provide a versioned, machine-readable component-recipe contract coordinated with the Interface Canon.
- **FR-002**: The initial recipe catalog MUST cover AppFrame, Button, IconButton, Toolbar, Tabs, Menu, Dialog, Field and core form controls, ListRow, SplitPane, Toast, StatusBadge, Card, and EmptyState.
- **FR-003**: Each recipe MUST declare supported variants and densities, semantic role assignments, interaction and validation states, keyboard behavior, minimum target behavior, icon policy, accessible naming, focus handling, motion and reduced-motion behavior, responsive adaptation, and permitted brand overrides.
- **FR-004**: Recipes MUST reference governed semantic roles and MUST NOT contain raw colors, font families, physical pixel literals, renderer property bags, or arbitrary screen composition.
- **FR-005**: Validation MUST reject unknown components, roles, variants, densities, states, and override keys; missing required behavior; invalid state combinations; undersized targets; inaccessible naming; unbounded composition; and attempts to override invariants.
- **FR-006**: Brand-specific recipe overrides MUST preserve affiliation, identity geometry, accessibility, keyboard, focus, target, and motion invariants.
- **FR-007**: The contract MUST include a coverage record showing how each initial component satisfies the required recipe dimensions and which layer owns each behavior.
- **FR-008**: BrandBuilder MUST generate a framework-neutral web token layer whose public names represent semantic roles and can be consumed without React.
- **FR-009**: BrandBuilder MUST generate a React adapter for the complete initial recipe catalog with typed public properties, governed variants, safe defaults, and explicit server-safe versus client-interactive entry points.
- **FR-010**: Generated components MUST consume recipe assignments and semantic roles rather than introduce local tokenizable literals.
- **FR-011**: Interactive components MUST provide the declared keyboard operation, accessible name and relationship semantics, visible focus, target sizing, status announcement, dismissal, validation, and reduced-motion behavior appropriate to the component.
- **FR-012**: The adapter MUST document and verify integration for Next.js and Vite consumers without requiring either application framework to become canonical.
- **FR-013**: The adapter MUST include explicit packaging and capability notes for browser, Tauri-style, and Wails-style hosts without inferring interaction behavior from an operating-system name.
- **FR-014**: AppFrame MUST be the single application-level owner of safe-area consumption, titlebar avoidance, root scrolling, fixed chrome placement, IME obstruction exposure, and the global focus boundary unless a declared host handoff transfers one specific responsibility.
- **FR-015**: Each AppFrame responsibility MUST declare exactly one owner, and validation MUST reject missing or duplicate ownership.
- **FR-016**: AppFrame MUST adapt to normalized runtime capabilities for usable viewport, safe area, window class, pointer precision, hover, keyboard, touch, text scaling, reduced motion, forced colors, theme, IME obstruction, and titlebar regions.
- **FR-017**: Generated specimens MUST demonstrate the token layer, component states, keyboard and focus behavior, responsive adaptation, and AppFrame ownership for supported browser and desktop-web host profiles.
- **FR-018**: Tests MUST cover semantic markup, keyboard paths, focus transitions, accessible names and relationships, target sizing, reduced motion, forced colors, text scaling, server safety, and ownership failures.
- **FR-019**: Generated consumer contracts MUST identify the component-recipe and Web/React adapter versions while retaining the existing canon, compiler, and brand version meanings.
- **FR-020**: The slice MUST evaluate whether an accessible headless component dependency should be adopted, record the decision and tradeoffs, and keep BrandBuilder authoritative for semantics, variants, tokens, and conformance.
- **FR-021**: Existing production brands MUST regenerate through the shared defaults or receive an explicit migration disposition without approved logo geometry, affiliation, provenance, or identity changes.
- **FR-022**: Every compiler or generator change in this slice MUST rebuild and verify all production brands without committing generated output.
- **FR-023**: Authored text MUST use UTF-8 without BOM and LF line endings and MUST pass a mojibake scan.

### Key Entities

- **Component Recipe Catalog**: Versioned renderer-neutral set of bounded shared components and their semantic, behavioral, accessibility, responsive, and override contracts.
- **Component Recipe**: Contract for one component family, including its variants, densities, states, role assignments, interaction rules, and invariant ownership.
- **Web Token Layer**: Framework-neutral semantic custom properties compiled from the resolved Interface Canon and brand contract.
- **React Adapter**: Generated typed bindings that expose recipe-governed components through server-safe and client-interactive entry points.
- **AppFrame Ownership Map**: Single-owner declaration for safe areas, titlebar regions, root scrolling, fixed chrome, IME obstruction, and the global focus boundary.
- **Runtime Host Profile**: Capability record for a browser, Tauri-style, or Wails-style environment without operating-system inference.
- **Coverage Record**: Machine-checkable matrix connecting every initial component and required recipe dimension to its declared behavior and owning layer.

## Scope

### In Scope

- GitHub issues #214 and #215 in full.
- The complete initial bounded component vocabulary and its schema, validation, defaults, examples, coverage record, and override policy.
- Framework-neutral semantic web tokens, generated React components, AppFrame, public exports, and consumer integration guidance.
- Browser, Next.js, Vite, Tauri-style, and Wails-style capability and packaging guidance required by #215.
- Minimum generated specimens and automated checks needed to prove the adapter contract, without establishing the broader multi-runtime conformance system.
- Provisional component-recipe and Web/React adapter version fields coordinated with the existing consumer contract.

### Out of Scope

- The egui adapter tracked by #216.
- The full cross-runtime conformance harness, golden screenshots, fixture application suite, and comparison reporting tracked by #217.
- The final compatibility, release, and consumer adoption policy tracked by #218.
- Consumer repository adoption or mutation tracked by #219 through #221.
- Documentation information-architecture migration tracked by #213.
- Light-theme guide completion, custom expressive assets, and the S035 preview repair tracked by #193, #194, and #202.
- Publication of a release tag, package registry artifact, or consumer deployment.

## Success Criteria

### Measurable Outcomes

- **SC-001**: The initial catalog contains all 15 recipes spanning the 14 named component families and every recipe has a complete coverage entry for 100% of the required dimensions.
- **SC-002**: A negative contract suite rejects 100% of representative raw-value, unknown-role, missing-behavior, invalid-state, inaccessible-name, undersized-target, unbounded-composition, unsupported-override, and duplicate-ownership fixtures with a diagnostic naming the failed concept.
- **SC-003**: A consumer can use every semantic web token without loading the component adapter, and 100% of generated component visual assignments trace to governed semantic roles.
- **SC-004**: The generated adapter exposes all 15 recipes and passes every declared semantic, keyboard, focus, naming, target, motion, forced-color, and scaled-text check.
- **SC-005**: Server-safe imports execute in environments without browser globals, while each client-interactive entry point is explicitly isolated and documented.
- **SC-006**: Browser, Tauri-style, and Wails-style fixtures assign each AppFrame responsibility to exactly one owner across compact, medium, expanded, safe-area, titlebar, and IME profiles.
- **SC-007**: Next.js and Vite integration exercises complete using only documented generated entry points and without local visual literals.
- **SC-008**: Every production kit reports zero verification problems and zero glyph failures after the slice changes.
- **SC-009**: Two consecutive generations from identical governed inputs produce byte-identical recipe, token, adapter, ownership, and consumer-contract outputs.
- **SC-010**: Repository validation reports no generated artifacts, UTF-8 BOMs, mojibake, or uncommitted synchronized instruction drift.

## Assumptions

- S038 begins from merged S037 on `main` at `690f63c013ec1b5c8ce97acf669dd7580346f473`.
- The Interface Canon, consumer contract, and contextual operating modes delivered by S037 remain authoritative inputs.
- The shared catalog is intentionally bounded to 15 recipes spanning the 14 named component families. Field labeling and messaging are separate from native form-control behavior; product navigation, page composition, data visualization, and domain widgets remain consumer-owned.
- AppFrame owns application-level environment adaptation by default. A host may take one responsibility only through an explicit, validated handoff.
- A mature accessible headless dependency may implement behavior-heavy controls only when its exact version, license, host compatibility, React range, offline prerequisite, and bounded BrandBuilder wrapper are recorded.
- The broader conformance system in #217 will reuse S038 specimens and behavior records but is not required to close this slice.
- The final lock-step compatibility policy remains owned by #218. This slice introduces stable provisional fields sufficient for generated consumers and future policy work.
- The user separately authorized pushing this feature branch and opening its pull request after local verification.
