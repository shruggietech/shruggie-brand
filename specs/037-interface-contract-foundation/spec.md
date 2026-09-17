# Feature Specification: Interface Contract Foundation

**Feature Branch**: `codex/037-interface-contract-foundation`

**Created**: 2026-09-17

**Status**: Ready for Planning

**Input**: User description: "Deliver S037 under Spec Kit autopilot as the shared foundation for GitHub issues #210, #211, and #212: establish the renderer-neutral Interface Canon, route BrandBuilder work contextually among Author, Implementation, and Audit modes, and generate a pinned consumer contract with deterministic recovery and upstream gap reporting."

## Clarifications

### Session 2026-09-17

- Q: Where do backward-compatible interface defaults live? -> A: One governed shared default contract applies to production brands unless a brand explicitly declares a permitted override.
- Q: What happens when a pre-existing governed instruction block is duplicated or malformed? -> A: Generation fails closed and preserves the file unchanged with an actionable diagnostic.
- Q: Does recording a reusable capability gap authorize filing or changing an upstream issue? -> A: No. The record is generated locally; submission or upstream mutation requires the consuming task's existing authorization.

## User Scenarios & Testing

### User Story 1 - Consume governed interface intent (Priority: P1)

As a maintainer or adapter author, I can read one renderer-neutral Interface Canon that separates primitive values from semantic roles, describes runtime capabilities without operating-system assumptions, and protects each brand's identity and override boundaries.

**Why this priority**: Skill routing and consumer instructions cannot be authoritative until the interface concepts, inheritance rules, and runtime vocabulary have one validated source.

**Independent Test**: Validate the canonical contract against every production brand, a ShruggieTech-owned product, and an independent client brand, then exercise invalid aliases, cycles, missing roles, inaccessible state pairs, and unsupported overrides to prove they fail closed.

**Acceptance Scenarios**:

1. **Given** a production brand without explicit interface overrides, **When** the contract is resolved, **Then** it receives documented backward-compatible defaults without changing its identity, affiliation, artwork, or inheritance boundary.
2. **Given** an adapter observing viewport, input, accessibility, titlebar, safe-area, or keyboard capabilities, **When** it reads the runtime contract, **Then** it can select normalized semantic behavior without inferring behavior from an operating-system name.
3. **Given** an invalid alias, cycle, missing role, inaccessible state pair, or unsupported override, **When** validation runs, **Then** generation stops with an actionable diagnostic before publishable output exists.

---

### User Story 2 - Route BrandBuilder work from context (Priority: P2)

As an agent starting a clear brand-system task, consumer implementation, or conformance review, I can infer Author, Implementation, or Audit mode from the request and repository evidence without relying on magic wording.

**Why this priority**: Correct routing prevents consumer work from mutating governed identity, prevents audits from becoming unsolicited redesigns, and directs reusable gaps back upstream.

**Independent Test**: Evaluate representative clear, ambiguous, and conflicting prompts across supported host instruction surfaces, including an existing-brand styling request and a missing-skill case, and record the selected mode plus the evidence used.

**Acceptance Scenarios**:

1. **Given** a request to change canon, a generator, an adapter, a recipe, or governed identity, **When** routing evaluates the request, **Then** it selects Author mode and retains existing authorization and Spec Kit safeguards.
2. **Given** a request to apply an existing pinned brand system, **When** routing evaluates the request, **Then** it selects Implementation mode, reads the contract, and prohibits identity reinterpretation or a permanent parallel design system.
3. **Given** a conformance assessment without remediation authorization, **When** routing evaluates the request, **Then** it selects read-only Audit mode and reports evidence plus any required handoff.
4. **Given** genuinely conflicting intent, **When** routing cannot preserve authorization through inference, **Then** it asks one narrow clarification instead of broadening authority.

---

### User Story 3 - Resume consumer work from delivered bytes (Priority: P3)

As an agent in a fresh consumer session, I can locate the exact brand and interface contract, distinguish renderer from host, recover the pinned BrandBuilder distribution when absent, run the declared checks, and report a reusable upstream gap without prior conversation memory.

**Why this priority**: A governed system is not usable in daily work if its authority, exact version, installation path, or verification entry point disappears during handover.

**Independent Test**: Generate the same consumer package twice, compare the governed contract outputs for deterministic equality, then use a fresh isolated session and an offline delivered kit to locate the contract, verify integrity, identify checks, and produce a complete reusable-gap record.

**Acceptance Scenarios**:

1. **Given** a consumer with the exact BrandBuilder distribution available, **When** a fresh agent reads repository instructions, **Then** it finds the pinned manifest, deeper implementation guidance, permitted exceptions, and verification entry point.
2. **Given** the BrandBuilder skill is absent, **When** the consumer has a bundled exact distribution, **Then** recovery uses that version, verifies its integrity, and does not download an unspecified latest release.
3. **Given** a reusable need that the contract cannot express, **When** the consumer records the gap, **Then** the record distinguishes a shared capability gap from product composition and carries enough evidence to trace an eventual upstream resolution and adopted version.
4. **Given** unrelated human-authored content around the generated instruction block, **When** generation repeats, **Then** the governed block updates deterministically without overwriting the unrelated content.

### Edge Cases

- A semantic alias references itself indirectly through multiple aliases.
- A brand override targets an invariant behavioral role or crosses an affiliation boundary.
- A runtime reports combinations that do not fit an operating-system stereotype, such as coarse pointer and hover, or desktop viewport with touch and an on-screen keyboard.
- A consumer renderer is known but its native host is absent, unknown, or intentionally none.
- A manifest references an adapter or verification runtime that is not included in the delivered kit.
- The pinned distribution is unavailable online but is present in the delivered offline artifacts.
- A generated instruction block is missing, duplicated, malformed, or surrounded by human-authored content.
- A request combines implementation with identity redesign, or combines audit with remediation, without adequate authorization.
- A screenshot or legacy local stylesheet contradicts the pinned contract.
- A reported need is product-specific composition rather than a reusable upstream concept.

## Requirements

### Functional Requirements

- **FR-001**: BrandBuilder MUST provide a machine-readable Interface Canon that is distinct from, coordinated with, and versioned alongside the existing Brand Canon.
- **FR-002**: The Interface Canon MUST structurally separate primitive values from semantic aliases selected by consumers.
- **FR-003**: The canon MUST define semantic roles for density, typography, surfaces, text, actions, borders, focus, state, motion, interaction targets, spacing, and layout measures without encoding renderer property bags or product layouts.
- **FR-004**: Canonical measures MUST use logical UI units and document transform expectations for Web, egui, and future native adapters.
- **FR-005**: The runtime environment contract MUST normalize usable viewport, safe-area insets, window class, pointer precision, hover, keyboard, touch, text scaling, reduced motion, forced colors or high contrast, theme, IME obstruction, and titlebar or window-control regions.
- **FR-006**: Runtime adaptation MUST be capability-based and MUST NOT equate an operating-system name with an input or layout profile.
- **FR-007**: Brand override rules MUST distinguish permitted visual expression from invariant accessibility and behavioral requirements.
- **FR-008**: Interface defaults and overrides MUST preserve ownership, affiliation, inheritance, provenance, and approved artwork boundaries for both product and independent client brands.
- **FR-009**: Existing production brands MUST resolve through documented backward-compatible defaults or receive an explicit migration disposition.
- **FR-010**: Validation MUST reject unknown roles, missing required roles, invalid alias targets, alias cycles, inaccessible declared state pairs, unsupported overrides, and cross-boundary inheritance with actionable diagnostics.
- **FR-011**: The canon, schema, examples, migration guidance, and version consequences MUST remain synchronized and machine-checkable.
- **FR-012**: BrandBuilder MUST define Author, Implementation, and Audit as the canonical operating modes.
- **FR-013**: Routing MUST infer a mode from request intent, repository evidence, and the pinned contract without requiring a user to name the mode.
- **FR-014**: Author mode MUST retain existing identity, approval, provenance, authorization, and Spec Kit safeguards.
- **FR-015**: Implementation mode MUST consume the pinned contract, MUST NOT reinterpret identity or permanently invent a parallel system, and MUST escalate reusable gaps upstream.
- **FR-016**: Audit mode MUST remain read-only by default and MUST route remediation through separately authorized Author or Implementation work.
- **FR-017**: Mode selection MUST NOT independently authorize source changes, identity redesign, upstream issue submission, publication, or consumer mutation.
- **FR-018**: Routing guidance MUST define evidence for each mode, include clear, ambiguous, and conflicting examples, and prescribe a narrow clarification only when intent genuinely conflicts.
- **FR-019**: Distributed skill instructions MUST keep contextual routing equivalent between metadata-aware and ambient host instruction surfaces.
- **FR-020**: Behavioral evaluation MUST cover representative mode prompts, existing-brand styling, contract discovery, and a missing-skill scenario on supported agent hosts.
- **FR-021**: Every generated consumer package MUST include a concise governed instruction block and a machine-readable manifest for the exact delivered contract.
- **FR-022**: The consumer manifest MUST declare brand identity, renderer, host, supported targets, viewport profiles, adapter versions, permitted exceptions, verification entry point, `canon_version`, `compiler_version`, and `brand_version`.
- **FR-023**: Manifest provenance MUST identify the exact governed inputs and include checksums for integrity-sensitive delivered contract files.
- **FR-024**: Generated instructions MUST state when BrandBuilder is mandatory, where deeper bundled guidance lives, how to run verification, and how authority is resolved when screenshots or legacy styles disagree.
- **FR-025**: Missing-skill recovery MUST locate or install the exact pinned distribution, verify integrity, prefer delivered offline artifacts when present, and MUST NOT recommend an unspecified latest release.
- **FR-026**: Generation MUST preserve unrelated human-authored instruction content while replacing exactly one governed block deterministically.
- **FR-027**: Existing enforcement MUST continue to reject ungoverned tokenizable values while permitting narrow documented renderer or platform literals.
- **FR-028**: A reusable capability-gap record MUST include consumer brand and version, renderer and host, reproduction or requirement, affected shared concept, evidence, ownership classification, upstream resolution, and adopted version.
- **FR-029**: The gap workflow MUST distinguish reusable system capabilities from product-specific composition and MUST follow the consuming repository's authorized reporting workflow.
- **FR-030**: Offline handover guidance MUST identify all delivered assets, exact versions, instructions, checks, known limitations, and any verification-runtime prerequisite not bundled with the kit.
- **FR-031**: Every compiler or generator change in this slice MUST rebuild and verify all production brands without committing generated output.
- **FR-032**: Authored text MUST use UTF-8 without BOM and LF line endings and MUST pass a mojibake scan.

### Key Entities

- **Interface Canon**: Versioned renderer-neutral authority containing primitive values, semantic aliases, logical measures, runtime capability vocabulary, invariants, and override rules.
- **Runtime Environment Profile**: Normalized set of observed viewport, input, accessibility, window, safe-area, and keyboard capabilities supplied to an adapter.
- **Operating Mode**: Author, Implementation, or Audit routing result, including evidence, permissions inherited from the task, and handoff rules.
- **Consumer Manifest**: Machine-readable record that binds a brand, interface canon, compiler, adapters, host and renderer targets, verification entry point, provenance, and checksums.
- **Governed Instruction Block**: Concise generated repository guidance that identifies authority and links to the deeper exact-version implementation contract.
- **Capability Gap Record**: Structured evidence for a reusable concept missing from the contract, separate from product composition and traceable through resolution and adoption.

## Scope

### In Scope

- GitHub issues #210, #211, and #212 in full.
- Interface canon data, schema, validation, examples, migration/default behavior, and documentation needed to close #210.
- Contextual mode guidance, synchronization, fixtures, and behavioral evaluation needed to close #211.
- Generated manifest, governed instruction block, deterministic merge behavior, pinned recovery, offline handover, integrity evidence, and capability-gap format needed to close #212.
- The minimum precise meanings for `canon_version`, `compiler_version`, and `brand_version` required by the consumer manifest.

### Out of Scope

- The component recipe grammar and initial primitive vocabulary tracked by #214.
- Web/React, Tauri, Wails, or egui adapter implementation tracked by #215 and #216.
- Conformance hosts, screenshot baselines, and cross-runtime fixtures tracked by #217.
- Full compatibility, release, and consumer adoption policy tracked by #218 beyond the three manifest field meanings required here.
- Consumer repository adoption or mutation tracked by #219 through #221.
- Documentation information-architecture migration tracked by #213.
- Light-theme guide completion, custom expressive assets, and the S035 preview repair tracked by #193, #194, and #202.
- Release publication, tags, deployment, or milestone certification.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All production brands resolve the Interface Canon with zero validation failures and without changes to approved identity geometry, affiliation, provenance, or inheritance boundaries.
- **SC-002**: A negative validation suite rejects 100% of representative unknown-role, missing-role, invalid-alias, alias-cycle, inaccessible-state-pair, unsupported-override, and cross-boundary inheritance fixtures with a diagnostic naming the failed concept.
- **SC-003**: Every required runtime capability is represented independently of operating-system names, and the contract accepts at least three mixed-capability profiles that contradict common device stereotypes.
- **SC-004**: Representative routing evaluation selects the expected mode and discovers the intended contract for 100% of the declared clear Author, Implementation, and Audit fixtures.
- **SC-005**: Every conflicting routing fixture either selects a safe read-only interpretation or requests one narrow clarification without broadening authorization.
- **SC-006**: Metadata-aware and ambient skill distributions contain equivalent non-frontmatter routing requirements after synchronization.
- **SC-007**: Two consecutive consumer generations from identical governed inputs produce byte-identical manifest and governed instruction-block content.
- **SC-008**: A fresh isolated session can locate the pinned contract, identify the renderer and host, find exact recovery guidance, and name the verification entry point using only delivered repository instructions.
- **SC-009**: An offline handover exercise resolves every required governed asset and instruction from delivered bytes, with any unbundled verification prerequisite named explicitly.
- **SC-010**: Regeneration preserves 100% of unrelated human-authored content around the governed instruction block in representative beginning, middle, end, missing-block, and malformed-block fixtures.
- **SC-011**: Every production kit reports zero verification problems and zero glyph failures after the slice changes.
- **SC-012**: Repository validation reports no generated artifacts, UTF-8 BOMs, mojibake, or uncommitted synchronized agent-instruction drift.

## Assumptions

- S037 begins from `main` at `d4665c72b91c7966d87d336352742f0cfb99fba5`; S035 remains a separate branch and issue.
- Existing production brand definitions remain authoritative identity sources and receive backward-compatible interface defaults unless an explicit migration is unavoidable.
- Renderer and host values may be `none`, `unknown`, or pending when a consumer does not have or has not declared that layer; they are never inferred from the operating system.
- The full version compatibility matrix remains owned by #218. This slice defines stable field semantics sufficient for deterministic manifests and recovery.
- Authentication and tenancy are not introduced by this source-generation feature. Security scope is integrity, bounded paths, authorization preservation, safe instruction merging, offline recovery, and rejection of untrusted authority claims.
- S037 does not push, publish, or mutate consumer repositories. The user separately authorized pushing this feature branch and opening its pull request after local verification.
