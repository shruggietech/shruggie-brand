# Feature Specification: Adaptive Brand Brief and Two Approval Gates

- **Feature Branch**: `codex/056-adaptive-brand-brief`
- **Created**: 2026-09-25
- **Status**: Approved for implementation
- **Input**: Issue #266, with the social-copy discovery and Gate 2 preview interface needed by #281. The owner approved this as S056 after confirming S055 was already merged.

## User Scenarios & Testing

### User Story 1 - Develop a useful brief (Priority: P1)

As an operator, I can provide extensive existing identity information or start with little context. The authoring agent reuses what I supplied, asks relevant follow-ups, and records facts, constraints, proposals, and unresolved choices separately.

**Independent Test**: Walk richly specified and sparse-input examples through the interview; neither imposes a question ceiling or silently treats a missing answer as approval.

### User Story 2 - Approve the actual logo source (Priority: P1)

As an owner, I make one explicit logo approval decision after seeing the production Full and Reduced sources with their proof matrix. A concept selection is not an approval of later artwork.

**Independent Test**: Walk constructed, supplied-artwork, changed-source, and silent-owner scenarios through the instructions and source ledger; only explicit source-bound approval advances.

### User Story 3 - Approve assembled fundamentals before final compilation (Priority: P1)

As an owner, I see provisional lockups, formal colors, interface cues, typography, representative uses, and the chosen social share image with my exact copy, then give one explicit fundamentals approval before final compilation.

**Independent Test**: Inspect a pending Gate 2 packet and verify the social image is identified separately from logo lockups, its copy and layout are explicit, and publication stays disabled until approval.

## Requirements

- **FR-001**: Discovery MUST accept supplied material, ask only questions that inform a named design decision, invite follow-ups, and distinguish supplied facts, constraints, proposals, and unresolved choices in a reusable brief.
- **FR-002**: The brief MUST separately cover purpose, audience, positioning, voice, references, existing identity, lockup use, formal brand colors, interface cues, typography, deliverables, affiliation, and social-copy choices.
- **FR-003**: The operator MUST provide or explicitly approve exact slogan text, optional exact description text, slogan-only or two-line layout, and intended line breaks before a social image is presented as approved. Missing copy MUST remain unresolved, not be inferred from `descriptor` or `brand_idea`.
- **FR-004**: There MUST be exactly two mandatory creative approval stops: source-bound logo approval (Gate 1) and assembled brand-fundamentals approval (Gate 2). Brief discussion, direction selection, palette discussion, automated verification, and publication authorization are distinct activities, not additional creative gates.
- **FR-005**: Gate 1 MUST bind the actual production source and proofs. Source drift MUST invalidate its approval and any affected Gate 2 approval.
- **FR-006**: Gate 2 MUST present provisional derivatives including the chosen social share image before final kit compilation; it MUST distinguish the social composition from wide and stacked lockups and bind explicit approval to the reviewed derivative evidence. Rejection MUST return to affected decisions.
- **FR-007**: The operator may not be bypassed by silence, timeout, or unattended default at either gate. Provisional review outputs MUST remain private until the applicable publication authorization and verification pass.
- **FR-008**: Skill entry points, generated agent instructions, interview, logo protocol, continuity guidance, hosted manual, and packaged references MUST describe the same workflow.
- **FR-009**: Existing approved brand geometry, approvals, and deliverables MUST remain intact. The generator's brand-wide social-image migration is tracked in #281.

## Success Criteria

- **SC-001**: Six representative scenarios (new identity, supplied identity, sparse input, rich input, revision, and nonresponsive operator) produce only the two required creative approval stops and never infer approval.
- **SC-002**: The public and packaged authoring guidance agrees on the order of Gate 1, provisional Gate 2 review, final compilation, and publication verification.
- **SC-003**: A Gate 2 review checklist rejects missing social copy or image and distinguishes it from the logo lockups before final compilation.

## Assumptions and Scope

- The existing `approval_ledger.gate_1` and `gate_2` are the authoritative approval records. This slice clarifies their human workflow without retroactively claiming approval for historical brands.
- The social copy contract and review packet are established here. Replacing generated social images and migrating all eight published brands belongs to #281, where exact approved copy must be resolved against owner records.
- Publication remains a separate authorization boundary; it is not a third creative approval gate.
