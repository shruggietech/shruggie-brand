# Feature Specification: Cueson Brand Kit

**Feature Branch**: `codex/026-cueson-brand-kit`

**Created**: 2026-09-09

**Status**: Draft, Gate 1 proposal in progress

**Input**: User description: "Deliver GitHub issue #184 as S026: research and propose a distinctive Cueson glyph and color system, iterate to explicit owner approval, derive and iterate the complete wordmark and icon spread to a second explicit owner approval, then generate and publish the verified current-specification brand kit. Push and open the official pull request automatically after both identity gates are satisfied, process no more than two review rounds, and halt for the owner merge ritual only after reviews and CI are satisfied."

## Clarifications

### Session 2026-09-09

- Q: Do the three supplied explainer images provide visual direction? -> A: No. Only their textual product meaning is evidence; their typography, colors, spacing, composition, and visual language are excluded as identity input.
- Q: What authority does the kickoff grant? -> A: It authorizes the complete S026 autopilot run, automatic branch push, and official pull-request creation, but does not waive either identity approval gate, authorize more than two review rounds, authorize the final merge, or authorize `cueson.io` activation.
- Q: Where is brand creation performed relative to the Cueson source repository? -> A: S026 is the external brand process anticipated by Cueson's roadmap. It creates the governed brand in this repository and a handoff manifest, but Cueson consumer import requires a later issue and Spec Kit slice in `shruggietech/cueson`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Choose a meaningful identity direction (Priority: P1)

As the identity owner, I can compare a small set of reasoned glyph concepts and one recommended color system that arise from Cueson's actual purpose, then request improvements until one exact glyph and palette revision earns my explicit approval.

**Why this priority**: Every later wordmark, icon, application, and public surface depends on an identity idea that is distinctive, product-grounded, accessible, and owner-approved.

**Independent Test**: Review the Gate 1 packet without inspecting implementation files. It contains three to five materially distinct concepts, an evidence-based palette recommendation, representative size and surface proofs, clear tradeoffs, and an approval ledger that prevents production identity work until an exact revision is approved.

**Acceptance Scenarios**:

1. **Given** current Cueson product evidence and the supplied explainer images, **When** research is performed, **Then** the criteria reflect timed language, structured interchange, format translation, source preservation, bitmap inputs, derived OCR, and explicit loss handling while excluding the images' styling.
2. **Given** the identity criteria, **When** Gate 1 is presented, **Then** the owner receives three to five thoughtful glyph directions and one clearly recommended accessible color system with product rationale, silhouette behavior, resemblance risks, and known tradeoffs.
3. **Given** the owner requests changes instead of approving a proposal, **When** the next Gate 1 revision is prepared, **Then** the feedback is incorporated or answered explicitly and no production master or canonical palette is committed.
4. **Given** the owner explicitly approves one exact glyph and palette revision, **When** the decision is recorded, **Then** the approval is bound to the displayed candidate identifiers, hashes, evidence, scope, wording, and timestamp.

---

### User Story 2 - Approve the complete derived spread (Priority: P1)

As the identity owner, I can inspect the complete family of wordmarks, lockups, icon crops, reduced treatments, copy compositions, and platform applications derived from the approved Gate 1 identity, then request improvements until the exact final spread earns explicit approval.

**Why this priority**: A promising glyph does not by itself prove that typography, spacing, platform masks, tiny sizes, monochrome output, and product copy work as one coherent identity system.

**Independent Test**: Review the Gate 2 packet and verify that every required derivative is present, traceable to the approved Gate 1 sources, compared on representative surfaces and sizes, measured, hash-listed, and blocked from publication until the exact set is approved.

**Acceptance Scenarios**:

1. **Given** an approved Gate 1 glyph and palette, **When** the derived spread is prepared, **Then** it includes the complete required lockup, wordmark, icon, platform, monochrome, reduced-size, and copy-composition families without changing the approved core idea silently.
2. **Given** the exact slogan and description, **When** promotional compositions are shown, **Then** they preserve the approved wording and prefer the specified two-line description treatment where space permits.
3. **Given** the owner requests changes instead of approving the spread, **When** the next Gate 2 revision is prepared, **Then** every affected derivative and measurement is updated and no public or consumer surface is enabled.
4. **Given** the owner explicitly approves the final spread, **When** the decision is recorded, **Then** the approval names and hashes every approved master and derivative family and invalidates itself if any governed source drifts.

---

### User Story 3 - Consume a complete verified Cueson kit (Priority: P2)

As a brand consumer, I can obtain a complete current-specification Cueson kit whose source contract, identity assets, typography, semantic colors, components, platform assets, guidance, and machine-readable bindings are coherent, accessible, and traceable to both owner approvals.

**Why this priority**: The approved identity becomes useful only when it is delivered through the same complete and verifiable contract as other production brands.

**Independent Test**: Build the Cueson kit offline from committed sources, verify the complete artifact inventory, inspect representative rendered output, and confirm that all measured brand and accessibility gates pass with no generated output committed.

**Acceptance Scenarios**:

1. **Given** both owner approvals, **When** the Cueson kit is generated, **Then** every current required human, agent, visual, platform, documentation, and framework layer is present and traces to the approved sources.
2. **Given** Cueson is a ShruggieTech-owned product with a distinct identity, **When** the kit and public surfaces are inspected, **Then** ownership is accurate, parent-brand governance is respected, and Cueson's own product identity remains recognizable.
3. **Given** the complete generated output, **When** verification runs, **Then** glyph validation, kit verification, WCAG 2.1 AA, raster, platform, PDF, link, responsive, encoding, and repository-hygiene gates pass at the available capability tier.
4. **Given** the public site consumes generated kits, **When** the proposed Cueson surfaces are built, **Then** they consume verified generated output and do not independently restate identity values.

---

### User Story 4 - Hand off an approved identity safely (Priority: P3)

As a Cueson maintainer, I can receive a hash-addressed manifest identifying the exact approved brand inputs and generated deliverables for a later consumer-integration slice without S026 modifying the Cueson repository or activating its dormant domain.

**Why this priority**: The brand is a v1 prerequisite, but consumer import and domain activation belong to separate repositories, authorities, and release phases.

**Independent Test**: Inspect the handoff manifest and scope ledger. The exact approved sources and intended consumer assets are identified, while the Cueson working tree, `cueson.io`, DNS, and Cloudflare state remain unchanged.

**Acceptance Scenarios**:

1. **Given** the final approved kit, **When** the handoff record is produced, **Then** it identifies exact source and artifact hashes, intended Cueson destinations, licenses, and the later workflow required for import.
2. **Given** S026 completes, **When** both repositories and domain state are inspected, **Then** no Cueson source commit, consumer import, DNS change, redirect, domain activation, or Cloudflare mutation was performed by this slice.

### Edge Cases

- Cueson or Shruggie Brand advances after a proposal is rendered. Re-synchronize, compare relevant evidence and hashes, and invalidate only the approvals affected by material drift.
- Two proposed glyphs are visually distinct at large size but collapse to the same generic caption shape at 16 pixels. Reject or revise the weaker directions before owner review.
- A concept communicates captions but not preservation or interchange. Record the shortfall rather than stretching the rationale after the fact.
- A palette passes individual contrast pairs but loses state distinction under common color-vision deficiencies. Revise semantic roles before Gate 1 approval.
- The preferred description line break creates poor balance in a narrow or wide format. Use the permitted exact one-line form rather than rewriting the copy.
- The approved glyph requires a reduced master at small sizes. Treat that reduced geometry as a Gate 2 derivative requiring explicit approval, not as an automatic optimization.
- A platform mask clips the mark or makes its clear space visibly uneven. Revise the platform treatment without moving the approved core master.
- A requested improvement conflicts with a previously approved invariant. Surface the conflict and return the affected gate to a new explicitly identified revision.
- A font candidate has incomplete license evidence or mismatched internal metadata. Reject it before controlled ingestion.
- Optional native rendering capability is unavailable. Record the explicit skip, retain every non-optional measurement, and require hosted capability coverage before readiness.
- A third-party review asks for an identity change after Gate 2 approval. Do not alter approved geometry automatically; report the conflict to the owner and reopen the affected approval gate if the finding is valid.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: S026 MUST trace GitHub issue #184 and record the synchronized Shruggie Brand and Cueson default-branch revisions used for every approval packet.
- **FR-002**: Research MUST treat the three supplied explainer images as textual product-context evidence only and MUST exclude their visual styling from identity criteria.
- **FR-003**: Identity criteria MUST account for timed cues, universal subtitle and caption interchange, structured machine-readable content, lossless source preservation, native-format fidelity, text and bitmap sources, derived OCR, and explicit loss diagnostics.
- **FR-004**: The required verbal identity MUST use the exact name `Cueson`, slogan `Universal captions and subtitles`, and description `A lossless, structured interchange layer for subtitle and caption content.`
- **FR-005**: Image and graphic compositions MUST prefer the exact description split after `layer` when space permits and MAY use the exact one-line form when that produces a clearer composition.
- **FR-006**: Cueson MUST be modeled as a publicly showcaseable ShruggieTech-owned project with governed parent-brand inheritance and a distinct product identity.
- **FR-007**: Gate 1 MUST present three to five materially distinct glyph directions with concept rationale, represented product ideas, silhouette and negative-space analysis, size behavior at 256, 64, 32, and 16 pixels, light/dark and single-ink behavior, likely wordmark relationship, accessibility risks, resemblance or cliché risks, and tradeoffs.
- **FR-008**: Gate 1 concepts MUST avoid generic AI sparkles, an unmodified speech bubble, a play button, a closed-caption badge imitation, and a literal file-conversion-arrow diagram unless a proposal develops a distinctive Cueson-specific treatment with a defensible rationale.
- **FR-009**: Gate 1 MUST include one clearly recommended best-fit color system derived from Cueson's product meaning rather than the explainer images, with semantic roles, light and dark behavior, measured contrast, color-blind robustness, single-ink behavior, and its relationship to ShruggieTech house colors.
- **FR-010**: Gate 1 MUST support repeated owner critique and revision until one exact glyph and palette revision receives explicit approval.
- **FR-011**: Before Gate 1 approval, S026 MUST NOT commit a production glyph master or canonical palette, create final derivatives, or enable any public or consumer surface.
- **FR-012**: Gate 1 approval MUST record candidate identifiers, relevant hashes, displayed evidence, exact owner wording, approved scope, and timestamp.
- **FR-013**: Gate 2 MUST derive all identity work from the approved Gate 1 revision and MUST include primary horizontal, stacked, mark-only, wordmark-only, slogan, description, full-color, reversed, light, dark, single-ink, reduced-size where required, favicon, web-app, Android, iOS, macOS, Windows, social, repository, outlined specimen, and representative raster treatments.
- **FR-014**: Gate 2 MUST present size and surface comparisons, alignment and clear-space measurements, crop and mask previews, and a manifest naming the source relationship and hash of every proposed derivative.
- **FR-015**: Gate 2 MUST support repeated owner critique and revision until the exact final spread receives explicit approval.
- **FR-016**: Gate 1 approval MUST NOT be interpreted as approval of typography, wordmark construction, icon crops, reduced geometry, or final applications.
- **FR-017**: Before Gate 2 approval, S026 MUST NOT enable a public Cueson kit, registry entry, downloadable archive, publication surface, or Cueson consumer integration.
- **FR-018**: Gate 2 approval MUST record every approved master and derivative family, their hashes, displayed evidence, exact owner wording, scope, and timestamp.
- **FR-019**: Any governed geometry, palette, typography, or product-evidence drift MUST invalidate the affected approval and return S026 to the applicable gate.
- **FR-020**: Approved source-only Cueson definitions MUST live under `brands/cueson/`; any approved reusable font sources MUST live under `assets/fonts/` with complete license and provenance evidence.
- **FR-021**: The generated kit MUST contain every current required human and agent entry point, source contract, manifest, verification record, migration note, token, style, component, binding, registry, logo variant, platform asset, font record, specimen, guideline, UI specimen, and brand-guide PDF.
- **FR-022**: The UI specimen MUST express source preservation, cue timing, structured content, format coverage, diagnostics, and derived OCR without becoming a duplicate Cueson product specification.
- **FR-023**: Generated kits, approval renders, PDFs, raster exports, registries, site exports, archives, and other artifacts MUST remain under ignored generated-output paths and MUST NOT be committed.
- **FR-024**: Every approved constructed derivative MUST report zero glyph-validation failures, the Cueson kit MUST report zero verification problems, and all declared roles MUST meet WCAG 2.1 AA without waivers.
- **FR-025**: Font sources MUST be license-compatible, locally deliverable, metadata-verified, provenance-recorded, and usable without network access during routine generation.
- **FR-026**: Verification MUST cover required size behavior, platform masks, raster dimensions, icon entries, light/dark contrast, single-ink output, PDF behavior, pagination, UI rendering, link integrity, responsive behavior, repository hygiene, and mojibake at the available capability tier.
- **FR-027**: The site and registry proposal MUST consume the verified generated Cueson kit and MUST NOT independently author brand values.
- **FR-028**: S026 MUST produce a hash-addressed handoff manifest for later import into `shruggietech/cueson`, including intended consumer destinations, licenses, and required follow-up workflow.
- **FR-029**: S026 MUST NOT modify or commit to the Cueson repository, activate or configure `cueson.io`, change DNS or Cloudflare state, merge its own pull request, tag, or publish a release.
- **FR-030**: After both identity gates and local verification pass, S026 MUST push its feature branch and open an official pull request that closes #184 without a separate pre-push halt, as explicitly authorized by the owner.
- **FR-031**: S026 MUST process every actionable continuous-integration, Codex, security-bot, and human-review finding, MUST answer and resolve every review thread appropriately, MAY request exactly one second Codex review round, and MUST NOT request a third round.
- **FR-032**: S026 MUST halt for the owner merge ritual only after required continuous-integration checks are green and all received reviews are satisfied or accurately documented as non-actionable.

### Key Entities

- **Product Evidence Snapshot**: The exact Shruggie Brand and Cueson revisions, source paths, factual product claims, and excluded visual references used to define the identity brief.
- **Identity Criterion**: A testable product meaning or visual-performance constraint against which concepts are evaluated.
- **Glyph Candidate**: One proposed mark direction with an identifier, rationale, geometry source, measured proofs, risks, tradeoffs, and disposition.
- **Color-System Candidate**: The proposed semantic palette, surface modes, contrast evidence, color-vision evidence, single-ink behavior, and relationship to the parent identity.
- **Approval Ledger Entry**: An explicit owner decision bound to a gate, candidate revision, source and output hashes, displayed evidence, wording, scope, and timestamp.
- **Derivative Asset**: A wordmark, lockup, reduced master, icon crop, platform asset, monochrome treatment, or copy composition that depends on approved Gate 1 sources.
- **Cueson Brand Source**: The committed source-only definition from which all generated deliverables are rebuilt.
- **Cueson Brand Kit**: The complete verified generated deliverable consumed by people, tools, registries, and the public brand site.
- **Consumer Handoff Manifest**: A hash-addressed map from approved sources and generated deliverables to proposed future Cueson repository destinations and licenses.
- **Review Ledger**: The bounded record of continuous-integration results, received reviews, responses, corrections, resolutions, and at most two Codex review rounds.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Gate 1 presents between three and five materially distinct, product-grounded glyph directions and exactly one recommended accessible color system, with 100% of the required rationale and proof fields present.
- **SC-002**: The owner can request any number of bounded Gate 1 improvements, and no production identity source or canonical palette becomes eligible until one exact revision has explicit recorded approval.
- **SC-003**: Gate 2 accounts for 100% of the current required lockup, wordmark, copy, monochrome, reduced, web, desktop, mobile, social, repository, and specimen families, each with source traceability and a recorded hash.
- **SC-004**: The owner can request any number of bounded Gate 2 improvements, and no public or consumer surface becomes eligible until the complete exact spread has explicit recorded approval.
- **SC-005**: All approved identity assets remain distinguishable, unclipped, and compositionally balanced in the declared proofs at 256, 64, 32, and 16 pixels on light and dark surfaces.
- **SC-006**: Every text-bearing and declared fill role meets WCAG 2.1 AA, every approved constructed derivative reports zero glyph-validation failures, and the complete kit reports zero verification problems.
- **SC-007**: A clean offline build produces 100% of the current required Cueson kit layers from committed sources, while repository inspection finds zero committed generated artifacts.
- **SC-008**: The final public-surface proposal uses the exact approved name, slogan, description, ownership relationship, identity sources, and generated kit values with zero independent restatements.
- **SC-009**: The consumer handoff manifest maps 100% of intended future Cueson assets to an approved hash, license basis, and destination without modifying the Cueson repository or dormant domain.
- **SC-010**: The official pull request closes #184, all required checks pass, every received review thread is answered and resolved appropriately, no more than two Codex review rounds occur, and final merge remains solely with the owner.

## Assumptions

- The Cueson repository and operator-provided explainer images are evidence sources, not destinations for S026 edits.
- Cueson remains a ShruggieTech-owned public project and should inherit governance and affiliation rules without copying parent identity geometry or house colors automatically.
- The complete current generator contract at implementation time defines the required artifact families; S026 records any discovered contract change before relying on it.
- Concept and approval renders may be produced under ignored `dist/` paths before production sources exist, provided they are clearly identified as proposals and cannot enter normal discovery or publication.
- The owner may approve or reject recommendations at either gate; autopilot resumes only after explicit approval bound to the displayed proposal revision.
- Automatic push and official pull-request creation are authorized after both approval gates and verification, but merge, release, deployment, Cueson consumer import, and `cueson.io` activation remain outside that authorization.

## Scope Boundaries

### In Scope

- Product research, identity criteria, three to five glyph proposals, and one recommended color system.
- Iterative Gate 1 and Gate 2 human review with hash-bound evidence.
- Approved source identity, complete generated kit, public brand-site proposal, and consumer handoff manifest.
- Automated verification, official pull request, bounded review processing, and final owner handoff.

### Out of Scope

- Cueson application, schema, CLI, documentation, or repository modifications.
- Importing the approved kit into Cueson before a later Cueson issue and Spec Kit slice.
- `cueson.io`, DNS, Cloudflare, post-v1 website, schema publication, product release, or domain activation work.
- Final pull-request merge, brandbuilder release, tag, or release publication.

## Traceability

- GitHub issue #184 is the complete feature intake for S026.
- The three operator-supplied explainer images provide factual product context only and are excluded as visual precedent.
- The Cueson roadmap's externally produced brand-kit boundary is preserved by the source-only handoff and separate consumer-integration requirement.
- The owner's 2026-09-09 kickoff authorizes automatic push and official pull-request creation after both identity gates, but neither gate nor the final merge ritual is waived.
