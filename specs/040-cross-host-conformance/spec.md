# Feature Specification: Cross-Host Conformance Fixtures

**Feature Branch**: `codex/040-cross-host-conformance`

**Created**: 2026-09-17

**Status**: Ready for Planning

**Input**: User description: "Deliver S040 under Spec Kit autopilot as the cross-host conformance slice, closing GitHub issue #217 by making the public site the browser reference and adding minimal browser/React, Tauri, Wails, and egui fixtures with fail-closed evidence policy."

## Clarifications

### Session 2026-09-17

- Q: What evidence is sufficient for a reference-host track without claiming downstream consumer adoption? -> A: Each track must execute a renderer or host-specific fixture and publish its exact tool, target, version, capability profile, and result. Browser emulation may prove only the browser track, while Tauri, Wails, and egui require their own executable fixture evidence. Consumer adoption remains separate.
- Q: How can visual baselines be reviewable without committing generated screenshots? -> A: CI generates candidate screenshots and a checksummed evidence manifest as ephemeral artifacts. Acceptance records are governed source metadata that name the candidate identity and human reviewer, while automated runs fail closed on missing, stale, or machine-authored approval.
- Q: Does S040 absorb the open integration-preview visibility defect? -> A: No. S040 applies the same contrast and nonvisual diagnostic principles to its own specimens, while issue #202 remains owned by the existing S035 branch.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Inspect every brand in the browser reference (Priority: P1)

As a BrandBuilder maintainer or consumer, I can open a public conformance route for every production brand and inspect the same governed component vocabulary across the canonical viewport and capability profiles.

**Why this priority**: The public site is the fastest review surface and the browser foundation used by the first two product pilots.

**Independent Test**: Build all production kits and the static site, visit each conformance route, exercise every declared profile, and confirm that component states, keyboard operation, accessible names, focus, target sizing, contrast, scaled text, and reduced motion remain usable.

**Acceptance Scenarios**:

1. **Given** any production brand, **When** its browser reference is opened, **Then** all bounded component recipes are represented with the exact brand and contract identities used to generate the specimen.
2. **Given** phone portrait touch, phone landscape touch, narrow desktop, normal desktop, reduced motion, forced colors or high contrast, and enlarged text profiles, **When** each supported profile is selected, **Then** the specimen preserves reachable controls, usable content, and explicit capability status.
3. **Given** a visual, accessibility, or interaction failure, **When** verification reports it, **Then** the diagnostic identifies exactly one failure class, brand, profile, and affected element or contract.

---

### User Story 2 - Prove host boundary ownership (Priority: P2)

As a host-adapter maintainer, I can run minimal Tauri, Wails, and egui fixtures that prove environment ownership and native renderer behavior without treating a browser screenshot as host evidence.

**Why this priority**: Glitchpad, go-schedule, and ESO Weave cannot begin their declared pilot evidence until the relevant reference-host tracks exist.

**Independent Test**: Run each host fixture independently and verify that Tauri accepts one Android inset owner, Wails preserves desktop window-control regions, and egui exercises native input, focus, selection, validation, density, and scaling states.

**Acceptance Scenarios**:

1. **Given** an Android WebView envelope with display-cutout and system-bar insets, **When** the Tauri fixture resolves ownership, **Then** AppFrame consumes each application-owned boundary once and rejects host-plus-AppFrame double consumption.
2. **Given** a Windows desktop window with titlebar control regions, resize, and mixed input capability changes, **When** the Wails fixture resolves usable geometry, **Then** fixed chrome and content avoid reserved native regions without OS-name routing.
3. **Given** an egui fixture, **When** rendered-state checks execute, **Then** native input, focus, selection, error, density, scaling, and unsupported capability evidence remains distinct from DOM evidence.

---

### User Story 3 - Reproduce and prevent the safe-area regression (Priority: P3)

As a reviewer, I can run one canonical known-bad Glitchpad-style safe-area trace that fails and a corrected trace that passes across orientation, resize, IME, and input changes.

**Why this priority**: The Android display-cutout failure is the mandatory first cross-runtime regression and the practical reason AppFrame ownership exists.

**Independent Test**: Feed the same capability and geometry events to the known-bad and corrected traces. The bad trace must produce obstruction and duplicate-ownership diagnostics, while the corrected trace must retain reachable controls and positive usable content through every transition.

**Acceptance Scenarios**:

1. **Given** the known-bad trace, **When** both native host and AppFrame consume the top or bottom inset, **Then** verification fails with a host-boundary diagnostic before evidence can be accepted.
2. **Given** the corrected trace, **When** portrait changes to landscape, the IME opens and closes, the window resizes, and input capabilities change, **Then** each boundary retains exactly one owner and all required controls remain reachable.
3. **Given** missing native-host proof, **When** certification state is calculated, **Then** the track remains pending or blocked and browser evidence cannot promote it.

---

### User Story 4 - Review baselines without automatic blessing (Priority: P4)

As a human reviewer, I receive exact, checksummed candidate evidence and can record an explicit decision without an agent or CI job silently accepting changed visual output.

**Why this priority**: A screenshot system that automatically replaces its expected output hides regressions instead of governing them.

**Independent Test**: Generate candidate evidence, attempt machine-authored, incomplete, stale, and mismatched approvals, confirm all are rejected, then validate a complete human decision against the exact candidate identity.

**Acceptance Scenarios**:

1. **Given** changed visual output, **When** CI runs, **Then** a candidate artifact is produced and the gate remains unresolved until a human records a decision and reason for that exact identity.
2. **Given** an approval with no human reviewer, reason, source revision, host, viewport, font settings, rendering settings, brand version, or contract version, **When** verification runs, **Then** it fails closed with a baseline diagnostic.
3. **Given** an accepted baseline for different bytes or metadata, **When** the candidate is checked, **Then** the stale approval is rejected and no source baseline is rewritten.

### Edge Cases

- A production brand generates a conformance manifest but omits one recipe, profile, or evidence class.
- A profile claims forced-color support on a renderer that can only record the capability as unsupported.
- A browser run attempts to satisfy a Tauri, Wails, or egui evidence slot.
- Android cutout, navigation-bar, IME, or titlebar regions overlap or consume the entire viewport.
- Orientation or resize events arrive while the IME is open and input changes from touch to keyboard.
- A host envelope contains negative, non-finite, inverted, stale, or differently scaled geometry.
- A baseline candidate is generated from different fonts, renderer settings, contract versions, brand version, or source revision.
- An approval is authored by automation, lacks a reason, or references candidate bytes no longer available.
- A visual failure is mislabeled as accessibility, interaction, or host-boundary evidence.
- An unlisted production brand or synthetic fixture enters site publication or baseline acceptance.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: BrandBuilder MUST define one versioned cross-host conformance contract that names required profiles, evidence classes, host tracks, diagnostics, and baseline decision rules.
- **FR-002**: Every production brand MUST generate an interactive browser specimen containing all bounded component recipes and exact brand, canon, recipe, adapter, compiler, and source-revision identities.
- **FR-003**: The public BrandBuilder site MUST expose an indexed browser reference route for every production brand and consume verified generated conformance data rather than restating brand values.
- **FR-004**: The profile matrix MUST cover phone portrait touch, phone landscape touch, narrow desktop, normal desktop, reduced motion, forced colors or high contrast where supported, and relevant text scaling.
- **FR-005**: Browser verification MUST exercise semantic markup, keyboard paths, focus transitions, accessible names and relationships, target sizing, contrast, reduced motion, forced-color status, scaled text, orientation, resize, and IME obstruction.
- **FR-006**: Visual, accessibility, interaction, and host-boundary failures MUST use distinct machine-readable diagnostic classes with brand, profile, host, and subject context.
- **FR-007**: BrandBuilder MUST provide executable minimal reference fixtures for browser/React, Tauri Android ownership, Wails Windows window chrome, and native egui rendered states.
- **FR-008**: Each fixture result MUST name its renderer, host, target, exact tool versions, source revision, capability profile, evidence class, and supported, unsupported, pending-proof, blocked, or failed status.
- **FR-009**: Browser emulation MUST NOT satisfy a Tauri, Wails, egui, actual-host, or downstream-consumer evidence requirement.
- **FR-010**: The Tauri fixture MUST prove Android WebView safe-area and display-cutout ownership with one canonical known-bad trace that fails and one corrected trace that passes.
- **FR-011**: The corrected Tauri trace MUST preserve positive usable content and reachable required controls through portrait, landscape, display-cutout, system-bar, IME, resize, and input-capability transitions.
- **FR-012**: The Wails fixture MUST prove desktop titlebar and window-control-region avoidance across normal and narrow window classes, resize, keyboard, pointer, hover, and touch capability changes.
- **FR-013**: The egui fixture MUST retain renderer-native evidence for input, focus, selection, visible error, density, text scale, pixels-per-point scale, and unsupported host capabilities.
- **FR-014**: Host fixtures MUST route on observed capabilities and explicit geometry rather than operating-system stereotypes.
- **FR-015**: Site self-hosting MUST remain necessary browser evidence but MUST NOT be reported as proof of native-host or downstream-consumer adoption.
- **FR-016**: Generated visual candidates MUST remain uncommitted artifacts and MUST include checksums plus brand version, contract versions, source revision, host, viewport, fonts, rendering settings, and review state.
- **FR-017**: Baseline acceptance MUST fail closed unless a human-authored decision records reviewer identity, reason, timestamp, exact candidate identity, and matching environment metadata.
- **FR-018**: Agents and CI MUST NOT create, replace, or promote an accepted visual baseline decision automatically.
- **FR-019**: Verification MUST reject missing profiles, recipes, fixture evidence, version data, unsafe paths, stale approvals, unknown statuses, evidence-class substitution, or conflicting ownership with actionable diagnostics.
- **FR-020**: Conformance outputs MUST remain renderer infrastructure and MUST NOT contain Glitchpad, go-schedule, ESO Weave, or other product-specific composition or business logic.
- **FR-021**: The slice MUST coordinate diagnostic and fallback principles with issue #202 while leaving its implementation and existing S035 branch untouched.
- **FR-022**: Existing production brands MUST rebuild and verify with zero `verify.py` problems and zero glyph failures, without approved identity geometry, affiliation, provenance, or inheritance changes.
- **FR-023**: Generated kits, screenshots, host build outputs, site exports, and synthetic fixtures MUST remain uncommitted and ineligible for production discovery or publication as source.
- **FR-024**: Authored text MUST use UTF-8 without BOM and LF line endings and MUST pass a mojibake scan.

### Key Entities

- **Conformance Contract**: Versioned source policy connecting profiles, hosts, evidence classes, diagnostics, acceptance rules, and fixture entry points.
- **Capability Profile**: Canonical viewport, input, motion, contrast, text-scale, IME, safe-area, and window-class conditions used by one or more fixtures.
- **Host Track**: Browser/React, Tauri Android WebView, Wails Windows webview, or native egui evidence boundary.
- **Host Envelope**: Explicit capability and geometry events supplied by a host to the shared shell contract.
- **Fixture Result**: Exact tool, target, version, source, profile, status, and diagnostic record produced by one executable reference fixture.
- **Visual Candidate**: Ephemeral screenshot and manifest proposed for review, never an automatically accepted source artifact.
- **Baseline Decision**: Human-authored acceptance or rejection bound to one exact visual candidate identity and environment.
- **Diagnostic**: Machine-readable failure record classified as visual, accessibility, interaction, or host-boundary.

## Scope

### In Scope

- GitHub issue #217 in full.
- Public browser reference routes and an index covering all production brands.
- Canonical viewport and capability profiles, distinct diagnostics, host/version matrix, and fail-closed baseline policy.
- Executable browser/React, Tauri Android ownership, Wails Windows chrome, and native egui reference fixtures.
- The Glitchpad-style known-bad and corrected safe-area traces as generic reference-host regression data.
- CI-parity checks, ephemeral candidate evidence, verification integration, site publication checks, and Spec Kit evidence.

### Out of Scope

- Issue #202 implementation, which remains on `codex/035-integration-preview-visibility`.
- Main documentation information architecture tracked by #213.
- Actual Glitchpad, go-schedule, or ESO Weave repository changes and consumer adoption evidence tracked by #219 through #221.
- Product-specific application screens, navigation, business logic, or local replacement design systems.
- A release tag, package publication, deployment, or automatic baseline acceptance.
- Committed generated kits, screenshots, native build output, site export, or synthetic fixture brands.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All production brands expose one public browser conformance route containing 100 percent of the bounded recipe vocabulary and required contract identities.
- **SC-002**: Every required profile executes for every production brand with zero unresolved accessibility, interaction, ownership, or usable-content failures.
- **SC-003**: Tauri known-bad evidence fails with at least one duplicate-ownership and one obstruction diagnostic, while the corrected trace passes every required transition.
- **SC-004**: Tauri, Wails, and egui evidence is produced only by their declared fixture entry points, and every attempted browser-evidence substitution fails.
- **SC-005**: One representative failure in each of the four diagnostic classes is reported under the correct class with no ambiguous fallback category.
- **SC-006**: Every visual candidate manifest contains all required identity and environment fields and rejects 100 percent of tested machine-authored, incomplete, stale, or mismatched approvals.
- **SC-007**: Two generations from identical governed inputs produce byte-identical conformance contracts, fixtures, manifests, and site staging data, excluding explicitly ephemeral screenshots and timestamps.
- **SC-008**: Every production kit reports zero verification problems and zero glyph failures, and the site passes static export, route, interaction, and WCAG 2.1 AA checks.
- **SC-009**: Repository validation reports no committed generated evidence, host build output, UTF-8 BOMs, mojibake, or synchronized-instruction drift.

## Assumptions

- S040 begins from merged S039 on `main` at `31fba0db9617033dc9ee1fb3f89fa7af4a2f4f50`.
- Issues #214, #215, #216, and #218 supply stable recipe, Web/React, AppFrame, egui, and version-contract foundations.
- Reference-host fixture success establishes BrandBuilder foundation readiness but does not claim actual downstream consumer adoption.
- Tauri and Wails fixtures may isolate the host-envelope boundary to keep fixtures small, but their executable evidence must use their own declared host fixture entry points and cannot be replaced by browser emulation.
- Visual screenshot candidates remain ephemeral CI or local outputs. Governed source stores policy and explicit human decisions, not generated raster bytes.
- The user explicitly authorized pushing this feature branch and opening its pull request after verification.
