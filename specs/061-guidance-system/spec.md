# Feature Specification: Durable Guidance System

**Feature Branch**: `codex/061-guidance-system`
**Created**: 2026-09-27
**Status**: In progress
**Input**: S061 delivers issues #270, #271, and #272 together: a durable, annotated source library, useful generated guideline topics, and applied source-aware guidance throughout the main manual and skill. The owner explicitly selected this combined slice to reduce repeated delivery cycles.

## Clarifications

No blocking ambiguity remains after reviewing the three issue acceptance contracts and the repository constitution. The public facts resource will be a static projection of the verified kit, and References will be authored in the existing manual source tree so the hosted manual and offline skill share exact source text. External source availability is reviewed separately from local citation integrity.

## User Scenarios & Testing

### User Story 1 - Find a trustworthy source and apply it (Priority: P1)

A designer or developer can find an annotated References section in the official manual and offline skill, identify whether an entry is a standard, platform requirement, advisory framework, implementation guide, or further reading, and follow its stable identifier from a concrete local instruction.

**Independent Test**: Navigate the published References page from the docs menu and search, then follow an in-manual citation to a known entry. The same source file appears in the packaged skill. Unknown or duplicate source IDs fail validation.

**Acceptance Scenarios**:

1. **Given** a brand, accessibility, Android, WordPress, HTML/CSS, web, or egui task, **when** a reader opens References, **then** they find a source with its use, scope, edition/version caveat, and a local application rather than an unexplained link.
2. **Given** a required accessibility rule, **when** it cites WCAG, **then** the local obligation is distinguished from informative explanations and unrelated advisory design systems.
3. **Given** an offline skill package, **when** a consumer follows a documented source ID, **then** the entry and its explanation are available without a network request.

### User Story 2 - Understand and use every brand guideline topic (Priority: P1)

A visitor can understand a brand's affiliation, interface rules, versions, assets, typography, components, registry, and exact authority without decoding internal identifiers or reading repetitive filler.

**Independent Test**: Audit all eight generated portals across overview, voice, logos, color, typography, components, integrations, assets, and conditional expressions. Complete a reader task on the hosted and portable guides: locate an override's meaning, download a verified asset, and identify the exact implementation fact source.

**Acceptance Scenarios**:

1. **Given** an overview with no override, **when** a visitor reads it, **then** the page explains that default interface rules apply and never implies that no interface exists.
2. **Given** an override, **when** a visitor reads it, **then** the default, effective value, source, and affected scope are explained without inventing an approver or rationale.
3. **Given** versions with long labels at narrow width or 200% zoom, **when** a visitor scans them, **then** each value stays aligned and readable without horizontal page overflow.
4. **Given** a public registry or implementation fact, **when** a visitor uses its link, **then** the linked static JSON resource exists, has a documented schema/version, and agrees with the corresponding certified kit record.

### User Story 3 - Follow practical guidance through authoring and integration (Priority: P1)

An operator or downstream agent can move from discovery through identity, color, components, documentation, web, Android, WordPress, and egui decisions with a clear task, useful example, source, and required-versus-advisory status at each meaningful point.

**Independent Test**: Audit each main manual and relevant skill/generated instruction surface. For each area, demonstrate one concrete task using the guidance and verify its citation resolves to the durable library; explicitly mark unsupported or unverified host behavior.

**Acceptance Scenarios**:

1. **Given** an adaptive discovery brief, **when** an operator asks for identity direction, **then** the prompts explain how the answers affect design without a fixed question cap, fabricated research, or new approval gates.
2. **Given** an integration task, **when** an agent selects platform guidance, **then** it can tell what this repository supports now, what belongs to the host, and what remains untested.
3. **Given** a regenerated kit, **when** bundled instructions and hosted manuals are compared, **then** applicable source IDs and guidance agree with the main documentation's pinned release identity.

### Edge Cases

- A reference URL redirects, becomes unavailable, or changes edition. The local annotated explanation remains usable, and a separate review reports external link status without treating a transient outage as invalid local documentation.
- A source is only known from a book's bibliographic record or abstract. Do not attribute unread passages or exact recommendations to it.
- A brand has independent styling, no parent, no override, optional expressions, or a capability gap. Generated prose must explain the actual declared state without placeholder claims.
- A link can point to a current hosted fact or an older pinned kit. Labels must distinguish those authorities and prevent an apparent current value from being mistaken for a historical package value.
- WordPress and Android reference entries may guide future work; their presence must not imply an adapter or runtime support that has not shipped.
- Long text, localization, mobile width, 200% zoom, reduced motion, keyboard use, and absent color cues must not make guideline information inaccessible.

## Requirements

### Functional Requirements

- **FR-001**: Publish a categorized References section in the main manual with stable unique IDs, descriptive anchors, useful annotations, source classification, scope/version caveats, and an explicit local application for each entry; include all owner-named sources from #271 or document a specific replacement/exclusion rationale.
- **FR-002**: Curate prior issue, PR, manual, and Spec Kit source history with recorded inspection coverage and dispositions, without claiming inaccessible conversation history was recovered.
- **FR-003**: Validate reference IDs, citation resolution, catalog membership, navigation/search inclusion, source packaging, and offline availability; do not require external sites at render time.
- **FR-004**: Audit every shared guideline topic and conditional state across eight brands using a topic-by-brand matrix with reader, meaning, action, and authority columns.
- **FR-005**: Replace opaque affiliation, inheritance, override, version, binding, registry, typography, component, integration, and empty-state presentation with specific reader guidance; preserve exact generated fact values and approved brand data.
- **FR-006**: Give public facts a direct stable static JSON resource with schema/version context and meaningful links from the guide; keep hosted HTML and JSON generated from the same kit authority and preserve pinned bundle links.
- **FR-007**: Repair heading containment, table of contents, version alignment, route titles, link purpose, focus/keyboard behavior, responsive reading order, and 200% zoom without weakening WCAG 2.1 AA.
- **FR-008**: Keep hosted, portable HTML, and PDF explanations consistent where they share facts; implement fixes in source templates and never patch generated kit files.
- **FR-009**: Audit every main manual and relevant skill/generated instruction surface with a documented disposition, then apply #271 sources contextually to discovery, identity, palette, components, documentation, web, Android, WordPress, and egui guidance; distinguish required rules from advice and supported behavior from unverified examples.
- **FR-010**: Preserve existing owner-approved creative gates, independent palettes, identity path data, exact version contracts, source/provenance boundaries, and existing adapter behavior.
- **FR-011**: Include meaningful automated citation, publication, and consumer tests plus qualitative reader-task review. Passing a schema or HTTP status alone cannot establish guidance usefulness.

### Key Entities

- **Reference entry**: Stable ID, title, URL, collection, source type, scope/edition, reader use, local application, and caveat.
- **Guideline fact**: Source-bound brand, interface, version, affiliation, or asset statement projected into hosted and bundled output.
- **Citation**: A local link from a manual or generated instruction to a reference entry; its ID and destination must resolve.
- **Reader-task audit**: Topic and brand state, intended reader, question, next action, authority, observed outcome, and repair disposition.

## Success Criteria

- **SC-001**: Issues #270, #271, and #272 each have an acceptance-to-test mapping and a completed disposition; no issue is marked complete from partial coverage.
- **SC-002**: All eight brands and every conditional guideline topic pass the reader-task matrix, with no unexplained internal identifier, filler-only section, or broken action/resource link in the audited output.
- **SC-003**: Every main manual and relevant skill/generated instruction has a reviewed disposition; required citations resolve in both the hosted manual and offline package.
- **SC-004**: All eight production kits pass zero-problem `verify.py` and zero-failure `validate_glyph.py`; site and release-candidate validation, including WCAG 2.1 AA browser checks, pass for the changed scope.
- **SC-005**: A representative user can complete override interpretation, registry installation orientation, artifact authority lookup, and source-guided platform selection without relying on internal issue history or guessing unsupported functionality.

## Assumptions and Boundaries

- Use the current 2.6.0 source candidate unless a real public contract change requires a version decision during planning; no identity geometry change is authorized.
- #273 WordPress adapter and #274 installable starter remain separate deliverables. S061 documents WordPress's actual reference and support boundary rather than claiming either adapter exists.
- A formal public release is not part of this PR request. Generated outputs remain ignored; PR CI rebuilds from the commit.
