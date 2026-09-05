# Feature Specification: Guarded Staging Disposition and Program Closure

**Feature Branch**: `codex/005-guarded-staging-disposition`

**Created**: 2026-09-04

**Status**: In progress

**Input**: Complete the verified, recoverable disposition of every legacy staging item; close the remaining Phase 1 and Phase 10 work with sanitized evidence; publish an official reviewed pull request; process the automatic Codex review and exactly one requested second round; and stop at the owner merge gate.

## User Scenarios & Testing

### User Story 1 - Prove every source is recoverable before retirement (Priority: P1)

As the repository owner, I can trust that every authoritative, historical, provenance, private-session, and unrelated-project item has been classified and preserved in an appropriate governed destination before its staging copy is moved.

**Why this priority**: Cleanup is irreversible in practice unless the backup and destination evidence are verified first. No staging item may be retired on assumption alone.

**Independent Test**: Compare the complete staging inventory with the pre-disposition archive, repository sources, published release, owning projects, and governed cold-storage destinations, then confirm that every top-level item has exactly one verified disposition.

**Acceptance Scenarios**:

1. **Given** the legacy staging workspace and its pre-disposition archive, **When** the integrity audit runs, **Then** every non-transient file is present byte-for-byte in the archive and any transient cache exception is identified as regenerated content.
2. **Given** an authoritative or provenance-bearing item, **When** its destination is assessed, **Then** equivalent governed source or an explicitly preserved copy is verified before the staging copy moves.
3. **Given** an item unrelated to this repository or retained only for history, **When** it is classified, **Then** it moves to an owning project only when that destination is unambiguous and collision-free, otherwise it moves to governed cold storage.

---

### User Story 2 - Retire staging without permanent deletion (Priority: P1)

As the operator, I can complete the cleanup while keeping every moved item recoverable and without publishing private workstation details.

**Why this priority**: The work order requires the staging workspace to become safely removable, but uncertainty must not cause data loss or sensitive-data disclosure.

**Independent Test**: Validate exact source and destination roots, execute the approved moves, then verify the original staging workspace is empty and the private recovery ledger accounts for every moved item without exposing those locations publicly.

**Acceptance Scenarios**:

1. **Given** a source that has verified governed coverage, **When** it is retired, **Then** it moves to recoverable deletion staging rather than being permanently deleted.
2. **Given** historical, unrelated, or private material, **When** it is relocated, **Then** it remains intact in governed cold storage and only its sanitized classification appears in the repository.
3. **Given** all planned moves are complete, **When** the staging workspace is inspected, **Then** it is empty or every deliberate retention is explicitly documented with rationale.

---

### User Story 3 - Close the public program with auditable evidence (Priority: P2)

As a project stakeholder, I can inspect GitHub and the repository to understand how every remaining work-order issue was satisfied, how review feedback was handled, and why each parent or milestone becomes eligible for closure.

**Why this priority**: The cleanup is not complete until public project management accurately reflects the evidence while sensitive operational data remains private.

**Independent Test**: Inspect the S005 artifacts, disposition ledger, issue comments, review ledger, open pull request, and milestone relationships. Every child is traced to evidence, no sensitive path or identifier is present, all review comments are dispositioned, and the pull request remains unmerged for the owner.

**Acceptance Scenarios**:

1. **Given** the S005 pull request, **When** automatic Codex feedback arrives, **Then** every negative finding is filed as a linked GitHub issue before the originating comment is substantively answered and resolved.
2. **Given** round 1 is complete, **When** round 2 is requested, **Then** exactly one explicit `@Codex` comment is posted and no third review request is made.
3. **Given** all permitted review feedback and required checks are complete, **When** readiness is reported, **Then** the pull request remains open and the owner is asked to perform the final review and merge ritual.
4. **Given** the owner later merges S005, **When** post-merge housekeeping runs, **Then** eligible children close before parents, zero-open-issue milestones close, and the program ledger reflects the final state.

### Edge Cases

- A dated archive may predate execution by one day. It remains valid only when all archived files match byte-for-byte and every unarchived file is proven to be a regenerated transient cache.
- A local command-line client may be absent while an authenticated provider integration is available. The integration may satisfy read-only access preflight only when an actual account-scoped read succeeds and no credential or identifier is published.
- A staging source may differ from the governed repository because the repository contains later fixes. The staging source is not authoritative merely because it is older; unique content must be separated from superseded content before retirement.
- An owning project may be absent or its correct destination may be ambiguous. The item moves to governed cold storage instead of creating or overwriting project content.
- A source or destination may contain junctions, virtual environments, or dependency caches. The move must remain recoverable and use exact validated roots without traversing or deleting linked targets.
- Review feedback may arrive late after a correction push. It is processed within its originating authorized round and never causes a third review request.

## Requirements

### Functional Requirements

- **FR-001**: S005 MUST record a sanitized toolchain preflight covering authenticated Git and GitHub access, Python 3.8 or newer, Node.js 20 or newer, the package manager, authenticated Cloudflare account access, ImageMagick, Playwright, and optional SVG rasterizer capability.
- **FR-002**: S005 MUST verify the complete pre-disposition archive outside the staging workspace by path, byte count, and SHA-256 content comparison before any staging move.
- **FR-003**: A missing archive entry MAY be accepted only when it is a regenerated transient cache, all authoritative and historical files remain archive-covered, and the exception is recorded privately and summarized safely in public evidence.
- **FR-004**: S005 MUST inventory every top-level staging item at disposition time and assign exactly one classification, destination category, preservation proof, recoverability state, and final state.
- **FR-005**: S005 MUST publish `docs/disposition.md` as the sanitized, complete, top-level disposition ledger without private filesystem paths, secrets, raw session output, backup locations, or provider resource identifiers.
- **FR-006**: S005 MUST confirm the repository and published release retain every authoritative skill file and rebuild both supported skill distributions before retiring private skill trees and transport bundles.
- **FR-007**: S005 MUST confirm all five production brands retain their source configuration, notes, artwork, UI source, icons, provenance, verified generated output, and published release archives before retiring each legacy directory and snapshot separately.
- **FR-008**: S005 MUST verify Fragcap historical geometry and bespoke construction scripts exist in governed provenance before its legacy kit moves, without redrawing or normalizing shipped geometry.
- **FR-009**: S005 MUST compare the staged SVG runtime helper with the committed generator helper, preserve any unique authoritative behavior, and prove the remaining runtime can be regenerated from documented dependencies before moving it.
- **FR-010**: S005 MUST move historical bulk artifacts to governed cold storage and MUST NOT commit generated PDFs, raster images, screenshots, archives, or other historical bulk output.
- **FR-011**: S005 MUST relocate unrelated Go Schedule and Covarity research to an unambiguous collision-free owning-project destination or governed cold storage and record only sanitized destination classes publicly.
- **FR-012**: S005 MUST verify both parent-brand CSS sources are preserved in repository provenance and support the canon and accessibility record before their private originals move.
- **FR-013**: S005 MUST triage private session output and the operator directive into governed private storage, publish neither their content nor operational location, and represent both in the sanitized disposition ledger.
- **FR-014**: S005 MUST permanently delete nothing. Superseded copies and regenerable runtime content MUST move to recoverable deletion staging only after source and destination validation.
- **FR-015**: S005 MUST leave the original staging workspace empty or document every deliberate retention. An empty directory may remain as the verified terminal state.
- **FR-016**: S005 MUST add sanitized decisions and evidence explaining every discovered contradiction, deviation, preservation rule, move class, and validation result.
- **FR-017**: S005 MUST reconcile the completed S004 post-merge publication evidence in its repository Spec Kit records before claiming the release prerequisite.
- **FR-018**: S005 MUST link issues #39, #41, #42, and #76 through #86 to one public S005 slice issue and keep issue, parent, milestone, and program states consistent with evidence.
- **FR-019**: S005 MUST leave implementation-dependent child issues, parents #6 and #15, milestones 11 and 20, and program #37 open until the reviewed change is merged to main and post-merge evidence satisfies their state policies.
- **FR-020**: Every negative Codex review finding on the S005 pull request MUST be filed as a GitHub issue with appropriate labels, milestone, source-comment link, rationale or reproduction, and acceptance criteria before its source thread is resolved.
- **FR-021**: Every Codex review comment MUST receive a substantive response; warranted corrections MUST be verified and pushed before the corresponding thread is resolved.
- **FR-022**: S005 MUST allow only two review rounds: the automatic publication-triggered round and exactly one explicit `@Codex` request after round 1 completes. No transition or task may trigger a third round.
- **FR-023**: S005 MUST NOT merge its own pull request. Once both review rounds are satisfied and all required checks are green, it MUST halt at the owner merge gate.
- **FR-024**: All committed text MUST use UTF-8 without BOM and LF line endings, contain no mojibake, and exclude private workstation paths, secrets, raw session output, backup locations, and provider resource identifiers.
- **FR-025**: Full documented validation MUST pass, including all production kits and the fixture reporting zero verification problems and zero glyph failures, before owner handoff.

### Key Entities

- **Disposition Entry**: One top-level staging item with a sanitized identifier, classification, destination class, preservation evidence, recoverability rule, and final state.
- **Private Recovery Record**: A non-public record of exact source and destination locations, archive hash, move completion, and recovery instructions.
- **Preservation Proof**: A byte comparison, governed source reference, release verification, provenance reference, or owner-project placement demonstrating that required material survives retirement.
- **Review Round**: One authorized Codex arrival signal, its findings, linked issues, responses, corrections, resolution state, and trigger URL when applicable.
- **Closure Set**: The child-first issue and milestone relationships that become eligible only after reviewed S005 evidence reaches main.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 2,479 archived files match the live staging workspace by relative path, byte count, and SHA-256, with exactly two unarchived files classified as regenerated Python bytecode caches and zero authoritative or historical mismatches.
- **SC-002**: Every top-level staging item present at execution has exactly one completed entry in `docs/disposition.md` and the private recovery record, with zero unclassified or multiply classified items.
- **SC-003**: Five of five production brand directories, five of five legacy snapshot archives, all private skill copies, the build runtime, historical archive, two unrelated research groups, two provenance CSS sources, private session output, and the operator directive reach verified recoverable destinations.
- **SC-004**: The original staging workspace contains zero files and zero undocumented retained directories after disposition.
- **SC-005**: Public-data scans report zero private paths, secrets, raw session content, backup locations, provider resource identifiers, BOMs, CRLF text files, or mojibake markers in the S005 change set.
- **SC-006**: Full repository validation reports six of six targets with zero verification problems and zero glyph failures, all focused tests and documentation checks pass, and hosted required checks are successful.
- **SC-007**: The official S005 pull request has zero unresolved actionable Codex comments after exactly two or fewer review rounds, exactly one explicit `@Codex` request, and all required checks successful.
- **SC-008**: Before owner merge, the S005 pull request remains open and no implementation-dependent child, phase parent, milestone, or program issue is closed prematurely.
- **SC-009**: After owner merge and post-merge verification, all fourteen direct child issues, parents #6 and #15, milestones 11 and 20, the S005 slice issue, and program #37 have states consistent with their evidence-backed acceptance policies.

## Assumptions

- The already-published v1.1.2 release and live site satisfy Phase 10 prerequisite gates only after they are rechecked and referenced in S005 evidence.
- The existing dated archive is preferable to a duplicate archive if byte-level comparison proves complete coverage of all non-transient content.
- Governed cold storage and recoverable deletion staging are private operational destinations whose exact locations belong only in the private recovery record.
- When an owning-project destination cannot be proven safe without interpretation, cold storage is the default.
- The external parent-site accessibility issue remains separately tracked in its owning repository and does not block the brand-repository work-order program definition of done.
- The owner will merge the reviewed S005 pull request before post-merge issue and milestone closure can occur.
