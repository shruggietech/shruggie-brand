# Feature Specification: Glitchpad AppFrame Adoption Pilot

**Feature Branch**: `codex/042-glitchpad-appframe-pilot`

**Created**: 2026-09-19

**Status**: Ready for Planning

**Input**: User description: "Deliver S042 under Spec Kit autopilot as the first BrandBuilder consumer pilot, completing upstream issue #219 and coordinated Glitchpad issue #196 through a pinned AppFrame adoption, Android safe-area proof, desktop proof, and comparable pilot observations."

## Clarifications

### Session 2026-09-19

- Q: Which layer owns Glitchpad's safe-area and IME consumption? -> A: Generated Web AppFrame owns safe-area and IME consumption. The Tauri host supplies capabilities and retains native titlebar regions, but it does not add duplicate content padding.
- Q: What evidence can satisfy actual consumer-host acceptance? -> A: Only checks executed against the Glitchpad consumer target qualify. Upstream fixtures and browser simulation remain reference evidence, while a real Android emulator or device and a Windows Tauri build and smoke path qualify as actual consumer-host evidence.
- Q: How should unavailable historical pilot measurements be handled? -> A: Record the inspected baseline facts and begin a prospective observation window. State unavailable timing or correction-round history explicitly and never infer a before-and-after improvement.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Adopt one authoritative shell contract (Priority: P1)

As a Glitchpad maintainer, I can pin one exact BrandBuilder contract and make its application-shell boundary authoritative without replacing Glitchpad's document workflows or visual identity.

**Why this priority**: The pilot cannot prove reusable interface infrastructure until the consumer uses exact governed bytes instead of a parallel local approximation.

**Independent Test**: Start from the recorded consumer revision, install the pinned contract using its bundled guidance, and confirm that the renderer, host, versions, provenance, ownership rules, and verification entry points are discoverable from a fresh repository session.

**Acceptance Scenarios**:

1. **Given** a fresh Glitchpad checkout, **When** an implementer follows repository instructions, **Then** the exact pinned BrandBuilder contract, AppFrame boundary, assets, and verification commands are discoverable without prior conversation memory or an unspecified latest download.
2. **Given** existing Glitchpad tabs, menus, inspectors, and document surfaces, **When** the shared shell contract is adopted, **Then** those product workflows remain downstream and retain their existing behavior.
3. **Given** a local value or shell behavior that conflicts with the pinned contract, **When** conformance runs, **Then** the conflict is reported against its owning layer instead of being silently accepted as a local replacement system.

---

### User Story 2 - Keep controls reachable across Android boundaries (Priority: P2)

As a Glitchpad user on Android, I can reach the application menu, fixed chrome, and active document through portrait, landscape, display-cutout, system-bar, and on-screen-keyboard changes without duplicate padding or hidden controls.

**Why this priority**: The Android safe-area failure is the mandatory regression case that motivated AppFrame and the first consumer pilot.

**Independent Test**: Exercise a known-bad duplicate-owner trace and the corrected consumer shell across the declared Android profiles. The known-bad trace must fail, while the adopted shell retains one owner per inset and positive usable content through every transition.

**Acceptance Scenarios**:

1. **Given** native and Web layers both claim the same safe-area inset, **When** ownership verification runs, **Then** adoption fails with a duplicate-owner diagnostic.
2. **Given** the corrected Web-owned safe-area contract, **When** the device rotates, a cutout changes usable geometry, or the IME opens and closes, **Then** menu controls, fixed chrome, the scroll root, and active content remain reachable.
3. **Given** an inset large enough to consume all usable content, **When** the shell resolves geometry, **Then** it fails closed with an obstruction diagnostic rather than reporting conformance.

---

### User Story 3 - Preserve desktop host behavior (Priority: P3)

As a Glitchpad desktop user, I retain a compact, keyboard-accessible shell on Windows while the same shared contract keeps titlebar ownership at the host boundary.

**Why this priority**: The pilot must prove that the Android correction does not regress the desktop host that shares the React renderer.

**Independent Test**: Build and exercise the Windows desktop target at normal and narrow sizes with keyboard and pointer input, confirming that native titlebar regions, menu placement, fixed chrome, focus, and document scrolling remain usable.

**Acceptance Scenarios**:

1. **Given** a desktop window with native titlebar regions, **When** AppFrame resolves the shell, **Then** the host owns titlebar geometry and the Web layer does not consume it a second time.
2. **Given** narrow and normal desktop window classes, **When** the window resizes, **Then** the menu, chrome, focus order, and document scroll root remain reachable.
3. **Given** keyboard-only interaction, **When** the user traverses the shell, **Then** all affected controls retain visible focus and their existing commands.

---

### User Story 4 - Hand over reviewable pilot evidence (Priority: P4)

As a program reviewer, I can compare the Glitchpad baseline with the adopted state and distinguish upstream fixture readiness, actual consumer proof, limitations, and reusable capability gaps.

**Why this priority**: The pilot exists to measure everyday adoption and expose the next shared improvement, not merely to demonstrate a reference fixture.

**Independent Test**: Review one evidence record that binds upstream and consumer revisions, pinned versions, renderer and host, tested targets, baseline and post-adoption observations, fresh-session continuation, handover completeness, and any blocked actual-host proof.

**Acceptance Scenarios**:

1. **Given** baseline and post-adoption observations, **When** they are compared, **Then** correction rounds, repeated local exceptions, kit-application time, and escaped defects use comparable task scope and disclose measurement limits.
2. **Given** upstream reference-fixture results and downstream application results, **When** evidence is classified, **Then** neither browser emulation nor a reference host is presented as actual consumer-host proof.
3. **Given** a reusable gap discovered during adoption, **When** the pilot completes, **Then** it is corrected in governed BrandBuilder source or recorded for authorized upstream follow-up, while product-specific composition remains in Glitchpad.

### Edge Cases

- The downstream checkout advances after the baseline is captured but before adoption evidence is finalized.
- The pinned kit verifies, but one provenance checksum or declared version differs from the copied consumer bytes.
- Android native code and Web CSS both consume a system-bar or display-cutout inset.
- Safe-area, titlebar, or IME geometry is missing, stale, negative, inverted, differently scaled, or larger than the viewport.
- The application menu opens near a cutout, narrow edge, or visible keyboard and would otherwise extend outside usable content.
- A document surface creates a second page-level scroll root beneath AppFrame.
- Text scaling, forced colors, reduced motion, coarse pointer, or keyboard input changes while the window is active.
- The desktop target passes while Android actual-host proof is unavailable, or the inverse.
- A fresh session finds legacy brand assets but not the pinned interface contract or verification entry point.
- Post-adoption evidence cannot reconstruct a historical baseline reliably.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: S042 MUST link upstream issue #219 and downstream Glitchpad issue #196 and keep each repository's commits, checks, review threads, and pull requests distinct.
- **FR-002**: The pilot MUST record the exact starting and adopted upstream and consumer revisions, BrandBuilder contract versions, Glitchpad brand version, renderer, host, target configurations, and observation method.
- **FR-003**: Glitchpad MUST pin exact governed BrandBuilder consumer bytes with integrity-verifiable provenance and MUST NOT substitute an unspecified latest distribution.
- **FR-004**: A fresh Glitchpad session MUST be able to locate the pinned contract, implementation guidance, assets, authority order, permitted exceptions, capability-gap path, and verification entry points without prior conversation memory.
- **FR-005**: The adopted shell MUST use AppFrame as the single Web owner of safe areas, usable viewport height, root scrolling, fixed application chrome, IME obstruction, and the global focus boundary.
- **FR-006**: Native titlebar and window-control geometry MUST remain host-owned, and every inset or obstruction MUST have exactly one declared consumer.
- **FR-007**: Verification MUST reject duplicate ownership, missing ownership, obstructed required controls, non-positive usable content, unsafe geometry, stale geometry, or differently scaled geometry with actionable diagnostics.
- **FR-008**: The consumer shell MUST preserve reachable application-menu controls, fixed chrome, active document content, and the declared scroll root through portrait, landscape, display-cutout, system-bar, IME, resize, text-scale, and input-capability transitions.
- **FR-009**: The pilot MUST retain Glitchpad's existing product-specific tabs, document surfaces, inspectors, file workflows, commands, and composition outside BrandBuilder.
- **FR-010**: The pilot MUST preserve approved Glitchpad identity, logo geometry, palette authority, affiliation, and provenance and MUST NOT patch generated output to compensate for generator defects.
- **FR-011**: Upstream reference-fixture evidence, browser evidence, Android actual-host evidence, Windows desktop evidence, and downstream adoption evidence MUST remain separately classified.
- **FR-012**: The known-bad duplicate-inset trace MUST fail, and the corrected consumer adoption MUST prevent the original obstructed-control defect unless the governed shell contract is bypassed.
- **FR-013**: Affected UI MUST meet WCAG 2.1 AA and retain keyboard-visible focus, accessible names, target sizing, contrast, reduced-motion behavior, forced-color behavior where supported, and usable 200 percent text scaling.
- **FR-014**: The pilot record MUST compare baseline and post-adoption correction rounds, repeated local exceptions, kit-application time, and escaped defects with comparable task scope and stated measurement limits.
- **FR-015**: The handover record MUST include fresh-session continuation, offline contract discovery, exact assets and versions, instructions, checks, known limitations, and the ownership or disposition of every reusable gap.
- **FR-016**: If actual Android or desktop host evidence cannot be produced, the relevant acceptance item MUST remain explicitly blocked and MUST NOT be replaced by emulation or reference-fixture success.
- **FR-017**: Existing production brands MUST rebuild with zero `verify.py` problems and zero `validate_glyph.py` failures after any upstream source correction.
- **FR-018**: Upstream generated kits, release archives, site exports, screenshots, raster evidence, native build outputs, and synthetic fixtures MUST remain uncommitted.
- **FR-019**: Both repositories MUST use their installed Spec Kit workflow, preserve unrelated work, and complete their documented CI-parity checks before publication.
- **FR-020**: Authored text MUST use UTF-8 without BOM and LF line endings and MUST pass a mojibake scan.

### Key Entities

- **Pilot Adoption Record**: The binding between upstream and consumer revisions, contract versions, renderer, host, target configurations, observation method, results, and limitations.
- **Pinned Consumer Contract**: Exact BrandBuilder bytes, versions, authority order, provenance, checksums, implementation guidance, recovery path, and verification commands adopted by Glitchpad.
- **Inset Ownership Map**: One declared owner for safe-area edges, titlebar regions, IME obstruction, usable viewport, fixed chrome, root scrolling, and global focus.
- **Host Evidence Record**: Separately classified browser, reference-host, Android actual-host, Windows desktop, or downstream consumer result with exact environment data.
- **Pilot Observation**: Comparable baseline or post-adoption measurement for correction rounds, local exceptions, kit-application time, escaped defects, fresh-session continuation, or handover completeness.
- **Capability Gap**: A reusable BrandBuilder need with consumer and version context, reproduction, affected shared concept, evidence, owner, and authorized disposition.

## Scope

### In Scope

- GitHub issue #219 and coordinated Glitchpad issue #196.
- A pinned Glitchpad consumer contract, AppFrame adoption, safe-area and IME ownership, root-scroll and fixed-chrome integration, and affected accessibility behavior.
- Android portrait, landscape, display-cutout, system-bar, IME, resize, and input transitions plus Windows desktop shell proof.
- Upstream source corrections discovered by actual adoption, provided they remain proportional to the pilot and regenerate every production brand.
- Comparable baseline and post-adoption observations, fresh-session continuation, offline handover, and reusable-gap disposition.
- Separate upstream and downstream feature branches, commits, CI, review responses, and pull requests.

### Out of Scope

- Glitchpad document-navigation redesign, file-format work, editor behavior, inspector redesign, or other product composition.
- A Glitchpad identity redesign, logo geometry change, palette reinterpretation, or affiliation change.
- go-schedule, ESO Weave, WordPress, or other consumer adoption.
- Automatic release, tag, deployment, visual-baseline acceptance, or publication of generated outputs.
- Treating browser emulation, the BrandBuilder reference host, or a planned downstream change as completed actual-host adoption evidence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: One downstream issue, one upstream issue, and their evidence records identify 100 percent of the starting and adopted revisions, contract versions, renderer, host, tested targets, and verification entry points.
- **SC-002**: Every shell responsibility has exactly one declared owner, and 100 percent of tested duplicate-owner, missing-owner, invalid-geometry, and obstruction mutations fail with the expected diagnostic class.
- **SC-003**: The known-bad Android trace fails, while every corrected portrait, landscape, cutout, system-bar, IME, resize, and input transition retains positive usable content and reachable menu, chrome, and document controls.
- **SC-004**: Windows normal and narrow window checks retain reachable menu controls, one root scroll owner, visible keyboard focus, and no titlebar-region double consumption.
- **SC-005**: A fresh session locates the exact pinned contract, implementation guidance, recovery bytes, assets, and verification entry points with zero reliance on prior conversation memory or network retrieval of an unspecified version.
- **SC-006**: The pilot reports all six required observation classes with comparable scope or an explicit measurement limitation, and invents zero savings, percentages, dates, or actual-host claims.
- **SC-007**: Every affected automated accessibility check passes with zero WCAG 2.1 AA violations, and the declared 200 percent text-scale profile retains usable content.
- **SC-008**: All production BrandBuilder kits report zero verification and glyph failures, Glitchpad's aggregate gate passes, and repository hygiene finds zero committed generated artifacts, UTF-8 BOMs, mojibake, or instruction drift.

## Assumptions

- S042 begins from merged S041 at `ce516dd904d9b97434a93f6f48c09766db46b1ac` and Glitchpad `main` at `3d9a560`.
- Upstream issues #212, #215, #217, and #218 provide the current consumer contract, AppFrame, conformance, and web-readiness foundation.
- The user's S042 kickoff authorizes the separately tracked Glitchpad work required by the proposed pilot approach, plus push and pull-request publication in both repositories. It does not authorize releases or deployments.
- The Web layer is the safe-area and IME owner for this pilot unless live host inspection proves that a required native boundary cannot be represented without one explicit host-owned handoff.
- Historical pilot timings may be unavailable. The record may use a prospective baseline and must state that limitation instead of reconstructing unsupported values.
- Actual Android and Windows evidence may run in repository CI when the local host lacks a compatible emulator or packaging environment, but it must execute the real declared consumer target and remain distinct from reference fixtures.
