# Feature Specification: DanceWithMe865 Brand Restart

**Feature Branch**: `codex/065-dancewithme865-restart`
**Created**: 2026-09-29
**Status**: Gate 1 and Gate 2 approved; local verification passed, PR pending
**Input**: Create the independent DanceWithMe865 client brand for the official brand website from a fresh visual and approval baseline. The owner-provided Natalie image establishes the direction: an angular DWM lettermark above an upright DANCEWITHME wordmark, followed by white 865 numerals in a red rectangular block. The supplied ZIP is conceptual source material, not a schema or kit template.

## Clarifications

### Session 2026-09-29

- Q: Does the latest owner image change the earlier prohibition on pairing DWM with the full wordmark? A: Yes. The new image explicitly shows that stacked pairing and the owner ordered a complete restart. The pictured composition is the direction for this new candidate.
- Q: Do prior S065 creative approvals carry over? A: No. This branch starts a new Gate 1 candidate and requires new source-bound and derivative approvals.
- Q: Does the supplied archive define the kit layout or canonical brand metadata? A: No. Its artwork is candidate source material; the repository schema and required deliverables control output.
- Q: Did approval of the first Gate 1 packet remain valid after the Windows icon treatment and social renderer changed? A: No. The first packet and exact owner wording remain recorded, but its renderer digest and derivative settings no longer match the current candidate. The owner separately approved candidate `dwm865-s065-g1-r2`.
- Q: What wording did the owner select for the social share image? A: `DanceWithMe865` only, with no separate slogan or description.

## User Scenarios & Testing

### User Story 1 - Recognize the supplied identity (Priority: P1)

As the client and brand owner, I can inspect a proposed production identity that preserves the DWM silhouette, upright wordmark, boxed 865, and stacked hierarchy visible in Natalie's image.

**Why this priority**: A visually different identity would repeat the rejected work.

**Independent Test**: Compare the reference image, proposed source files, and rendered light-surface stacked treatment side by side at matching aspect ratio; verify the proposed masters are byte-bound to reviewed source and the 32-proof matrix is complete.

**Acceptance Scenarios**:

1. **Given** the owner-provided image, **when** the light stacked treatment is reviewed, **then** the DWM shape, upright DANCEWITHME outlines, white 865 numerals, red rectangle, and their arrangement remain recognizable.
2. **Given** supplied SVG candidates, **when** they are evaluated, **then** their geometry is preserved byte for byte if bound as authoritative source, and any invalid source is reported for a new owner decision.
3. **Given** an exact Gate 1 candidate, **when** the owner has not approved that candidate, **then** neither canonical promotion nor publishable generation occurs.

---

### User Story 2 - Receive a complete standard kit (Priority: P1)

As the client, I receive the repository's required brand kit content and verified website presentation without adopting the ZIP's directory layout or its claims as policy.

**Why this priority**: The kit must be usable by the official website and downstream consumers under the same contract as other brands.

**Independent Test**: Inspect the source contract and generated manifest, verify every required deliverable, run the documented validation with zero problems and glyph failures, and confirm generated output remains outside Git.

**Acceptance Scenarios**:

1. **Given** approved sources and assembled derivatives, **when** the kit is built, **then** standard logo, token, icon, typography, guide, social-image, and site surfaces are present or a contract-defined exception is documented.
2. **Given** the supplied ZIP, **when** sources are imported, **then** only reviewed source assets enter `brands/` or shared font assets enter `assets/fonts/`; ZIP paths and metadata do not define the output schema.
3. **Given** an independent client brand, **when** the site displays it, **then** ownership and service credit are truthful and no ShruggieTech ownership is implied.

---

### User Story 3 - Approve the assembled brand (Priority: P2)

As the owner, I can review wordmarks, lockups, icons, palette, typography, social copy and image, and representative website applications before the final kit is compiled.

**Independent Test**: Inspect the private Gate 2 packet and its source and derivative hashes; verify changed source returns to Gate 1 and changed derivatives return to Gate 2.

**Acceptance Scenarios**:

1. **Given** Gate 1 approval, **when** provisional derivatives are assembled, **then** they derive from that exact source and retain the pictured hierarchy in the light stacked lockup.
2. **Given** no Gate 2 approval, **when** generation is attempted, **then** final kit compilation and public site publication remain unavailable.

### Edge Cases

- A supplied asset conflicts with SVG safety, font licensing, accessibility, or the repository schema: preserve the source for review, identify the conflict, and request a new decision before substitution.
- The DWM mark is unclear at 16 or 32 pixels: show the actual small-size proof and offer a source-preserving treatment or revised Reduced candidate for Gate 1.
- Exact social copy is absent: leave it unresolved; do not convert a descriptor or ZIP prose into approved slogan text.
- A new requirement contradicts an earlier approval: bind approvals to the revised candidate; do not reuse the abandoned S065 approval records.

## Requirements

### Functional Requirements

- **FR-001**: The brand MUST be recorded as an independent client identity owned by DanceWithMe865, with public showcase permission and no inferred ShruggieTech parentage, endorsement, or service credit.
- **FR-002**: The proposed light stacked lockup MUST visually follow Natalie's supplied image, including DWM over upright DANCEWITHME and boxed 865.
- **FR-003**: The proposed Full and Reduced masters MUST preserve any selected authoritative supplied SVG bytes and declare source roles, hashes, provenance, usage, and allowed transformations.
- **FR-004**: The system MUST produce the full Gate 1 source-bound packet, including formal palette qualification and 32 rendered proofs with comparison evidence, before seeking canonical approval.
- **FR-005**: The system MUST require explicit approval of the new Gate 1 candidate and of the assembled Gate 2 derivative packet; prior approval records cannot be transferred.
- **FR-006**: The final source MUST use the repository's brand schema and standard deliverable contract, independent of the ZIP's layout and metadata structure.
- **FR-007**: Formal identity colors and functional interface cues MUST be separately declared and meet WCAG 2.1 AA wherever applicable.
- **FR-008**: The final kit MUST include the repository-required logo, typography, icon, token, guide, social-image, and site outputs, with only governed exceptions.
- **FR-009**: No generated contents of `dist/` MUST be committed.
- **FR-010**: Final publication MUST depend on zero `verify.py` problems and zero `validate_glyph.py` failures.
- **FR-011**: Public-facing claims and social copy MUST be sourced to the owner or explicitly approved; supplied ZIP prose is proposal material.
- **FR-012**: General generator extensions MUST retain exact approved proof behavior for unrelated existing brands; any proof change requires the applicable identity reapproval.

### Key Entities

- **Brand source**: Client affiliation, palette, typography, authoritative inputs, and approved uses under the standard schema.
- **Canonical candidate**: Gate 1 approved Full and Reduced production sources, renderer, palette qualification, 32 proofs, and comparison artifacts.
- **Derivative packet**: Gate 2 approved lockups, wordmark, icons, palette, typography, applications, and distinct social share image.
- **Published kit**: Generated versioned delivery compiled only from approved source and verified against the repository contract.

## Success Criteria

### Measurable Outcomes

- **SC-001**: A reviewer can identify the image's five defining features in the proposed stacked light treatment without viewing implementation notes.
- **SC-002**: Gate 1 contains 32 of 32 required Full and Reduced size-and-surface proofs and all required comparisons.
- **SC-003**: The approved assembled packet contains each required derivative type, with a separate social share composition.
- **SC-004**: Final validation reports zero problems and zero glyph failures, and no generated files are tracked.
- **SC-005**: The official website presents the client identity and correct ownership without a ShruggieTech ownership claim.

## Assumptions

- The latest owner-supplied image replaces the previous creative direction and its approvals. It is direction, not itself Gate 1 approval.
- The supplied archive may contain candidate source artwork; its own packaging and claims do not govern this repository.
- The owner authorizes using supplied assets as review candidates and displaying the finished client brand on the company brand website.
- The owner selected `DanceWithMe865` as the only social image wording and approved the assembled image, support typography, and application treatments at Gate 2. No service claims or homepage are inferred from the ZIP.
