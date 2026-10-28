# Feature Specification: Owner-decided portfolio messaging

**Feature Branch**: `codex/072-approved-brand-messaging`

**Created**: 2026-10-21

**Status**: In progress

**Input**: S072 implements issue #309. Apply recorded owner messaging decisions, including four short descriptions approved on 2026-10-27. Research remaining fields and retain unreviewed suggestions as unresolved when the owner defers further questions. Explicit absence is a separate valid decision.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Apply decisions already made (Priority: P1)

The owner sees the recorded Covarity, Cueson, DanceWithMe865, fragcap, Glitchpad, go-schedule, and ShruggieTech decisions reflected exactly in brand guidance and applicable public descriptions.

**Why this priority**: A rejected sentence is currently presented as approved, while accepted messages remain unresolved.

**Independent Test**: Compare each changed role with the dated issue #309 comment, then inspect generated guidance and public projections.

**Acceptance Scenarios**:

1. **Given** Covarity's recorded decisions, **When** regenerated, **Then** its reusable slogan is `See what is known`, its short description is `An evidence-backed knowledge graph and a policy-enforcing context compiler.`, and its long description is intentionally absent.
2. **Given** Cueson's recorded decisions, **When** regenerated, **Then** its reusable slogan is `Universal captions and subtitles` and its long description is `A lossless, structured interchange layer for subtitle and caption content.`, with the existing short description preserved.
3. **Given** the later DanceWithMe865 slogan decision, **When** regenerated, **Then** its reusable slogan is `Join the Krucial Crew.`, its short and long descriptions are intentionally absent, and the rejected sentence is absent from public outputs.
4. **Given** existing social-image approvals, **When** reusable messages change, **Then** social wording and composition retain their independent approvals.
5. **Given** the 2026-10-27 short-description decisions, **When** regenerated, **Then** fragcap, Glitchpad, go-schedule, and ShruggieTech show the exact approved sentences on portfolio cards and formal brand outputs, while unrelated roles keep their independent states.

### User Story 2 - Choose remaining copy without pressure (Priority: P2)

The owner reviews researched suggestions for one brand at a time and may approve exact wording, revise it, explicitly choose no copy, or defer the decision.

**Why this priority**: Completing a field is less valuable than avoiding an inaccurate or unwanted brand statement.

**Independent Test**: Trace every additional approved value to an explicit owner reply and verify undecided fields remain tracked without public fallback copy.

**Acceptance Scenarios**:

1. **Given** an unresolved brand, **When** suggestions are presented, **Then** the owner sees existing approved text, suggested slogan and description options, factual basis, and independent absence/defer choices.
2. **Given** a selection for only one role, **When** recorded, **Then** other roles keep their prior states.
3. **Given** an explicit no-copy decision, **When** output is generated, **Then** no invented substitute or orphan label appears.
4. **Given** the owner stops before all brands are reviewed, **When** handed off, **Then** unresolved roles remain visible and do not block delivery of approved corrections.

### User Story 3 - Keep all consumers faithful (Priority: P1)

Public portfolio cards, metadata, guides, and starter applications use only messages approved for their surface.

**Why this priority**: Correct source decisions must not be bypassed by a legacy descriptor fallback.

**Independent Test**: Generate approved, absent, and unresolved descriptions and compare exact text/state across website, Next.js, and WordPress surfaces.

**Acceptance Scenarios**:

1. **Given** a legacy descriptor and an absent or unresolved canonical description, **When** generating a starter, **Then** legacy text is not promoted into public copy or alt text.
2. **Given** a short description approved for public metadata, **When** generating a starter, **Then** that exact description is used where one is presented.
3. **Given** a title-only identity, **When** alternative text is required, **Then** its accessible name remains meaningful without a fabricated description.

### Edge Cases

- The issue body predates the 2026-10-01 DanceWithMe865 slogan comment; the later explicit decision wins for that role only.
- Covarity's canonical slogan has no final period; its social-image slogan retains its period.
- Explicit absence and unresolved state are distinct, although both omit public text.
- Identical Cueson short and long descriptions remain independently approved roles.
- Historical records may retain superseded claims only with an explicit correction; active sources must not assert revoked approval.
- Suggestions use capabilities supported by inspected project material and remain unapproved until selected.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Apply latest recorded owner decisions independently per role, preserving exact case and punctuation.
- **FR-002**: Record provenance and allowed uses; absent and unresolved records contain no public text.
- **FR-003**: Remove DanceWithMe865's revoked description from active public projections and correct historical approval inventory without replacement copy.
- **FR-004**: Preserve other approved copy and social-image decisions unless explicitly changed by the owner.
- **FR-005**: Audit all production brands, including insonic and Local Media Gallery, and track each unresolved core role.
- **FR-006**: Research and present suggestions one brand at a time, offering independent approval, revision, absence, and defer choices.
- **FR-007**: Never promote suggestions, descriptors, brand ideas, or social-only messages into another role without owner approval.
- **FR-008**: Consumers honor allowed uses and omit absent/unresolved descriptive copy, retaining useful title-based accessible names.
- **FR-009**: Preserve logo geometry and identity snapshots; refresh source-bound evidence only where changed source digests require it.
- **FR-010**: Run full documented validation before completion, including zero kit problems, zero glyph failures, accessibility, encoding, and generated-artifact exclusion checks.

### Key Entities

- **Message decision**: Brand, role, exact text or state, permitted uses, provenance, date, and superseded decision.
- **Suggestion**: Candidate text, supporting source, rationale, and pending owner disposition, separate from canonical messages.
- **Inventory**: Every production brand and its core message states, reviewed status, and remaining work.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All seven brands with recorded #309 decisions match their latest role-specific decisions exactly.
- **SC-002**: No generated public output publishes the revoked description or substitutes legacy copy for absent/unresolved roles.
- **SC-003**: Every production brand has a three-role inventory; all newly approved values have explicit provenance.
- **SC-004**: The owner can decline or defer every suggestion independently, with zero automatic approvals.
- **SC-005**: All affected deliverables pass documented gates, with unavailable capabilities recorded as skips and no geometry changes.

## Assumptions

- This request authorizes recorded decisions, not unattended approval of new wording. On 2026-10-27 the owner requested no further input during cleanup, so unreviewed suggestions remain unresolved.
- Covarity's short-description period follows the candidate sentence recorded in #309; its trailing comma was list punctuation.
- Reusable slogans use visual guidance, strategy reference, and consumer data. Descriptions additionally use site metadata. This grants no new social-image wording or composition approval.
- No release, tag, or website deployment is included. The 2026-10-27 cleanup request authorizes pushing and merging the completed slice after required checks and review.
- #328 guide-cover hierarchy and #310/#311 site layouts remain separate work.

## Clarifications

### Session 2026-10-21

- The owner prefers unresolved or absent copy over weak decisions; partial copy completion succeeds when remaining roles are tracked.
- Later role-specific decisions supersede earlier ones without resetting other roles.
- Clarification found no blocking product ambiguity. US2 editorial selections are not prerequisites for US1/US3.

### Session 2026-10-27

- The owner's four exact short-description decisions supersede prior suggestions for those roles. Markdown emphasis around the Glitchpad sentence is presentation, not canonical text.
- The owner requests no further input during repository cleanup. Defer all other optional copy choices independently and complete the approved subset.
