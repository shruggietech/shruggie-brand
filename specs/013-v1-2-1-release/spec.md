# Feature Specification: v1.2.1 Release and Production Certification

**Feature Branch**: `codex/013-v1-2-1-release`

**Created**: 2026-09-06

**Status**: Ready for Implementation

**Input**: Publish the completed S012 brand-site polish and merged Dependabot security update as a fully verified v1.2.1 patch release.

## User Scenarios & Testing

### User Story 1 - Review a coherent patch candidate (Priority: P1)

As the release owner, I can review one source revision whose release histories, skill version, canon version, production-brand canon references, site metadata, release notes, packaging behavior, and CI preflight all agree on v1.2.1.

**Why this priority**: The release tag is immutable, so stale metadata or incomplete history must fail before publication.

**Independent Test**: Rebuild every production kit and all candidate archives, generate v1.2.1 notes, and pass the repository release contract for exactly seven assets.

**Acceptance Scenarios**:

1. **Given** the completed S012 and Dependabot changes under Unreleased, **When** the candidate is prepared, **Then** both changelogs preserve the applicable history under one dated v1.2.1 section and retain an empty Unreleased section.
2. **Given** v1.2.1 metadata, **When** release preflight runs, **Then** skill, canon, site, production sources, notes, and packaging agree without changing independent production-brand versions.
3. **Given** freshly rebuilt output, **When** release verification runs, **Then** exactly two skill distributions and five production-kit archives pass every metadata, license, safety, manifest, PDF, and checksum rule.

---

### User Story 2 - Publish reviewed source and official assets (Priority: P1)

As a release consumer, I can obtain an official v1.2.1 release created by CI from reviewed and verified main, with every pull-request review comment dispositioned before merge.

**Why this priority**: Public assets must come from the reviewed source revision and must remain reproducibly certifiable after publication.

**Independent Test**: Inspect the merged pull request, tag target, release workflow, public release inventory, notes, and seven freshly downloaded assets.

**Acceptance Scenarios**:

1. **Given** the S013 pull request, **When** automatic review and required checks complete, **Then** every actionable comment is answered, corrected when warranted, and resolved before merge.
2. **Given** satisfied review and green checks, **When** publication begins, **Then** the pull request is merged, actual main is synchronized and revalidated, and annotated tag v1.2.1 is created exactly once at that verified revision.
3. **Given** the successful tag workflow, **When** the GitHub release is inspected, **Then** it is public, non-draft, non-prerelease, and contains exactly seven verified assets plus generated notes.

---

### User Story 3 - Use the certified production site (Priority: P2)

As a visitor or internal brand operator, I can use the deployed brand site after v1.2.1 publication with its complete routes, downloads, discovery metadata, responsive layouts, themes, and accessibility behavior intact.

**Why this priority**: A successful archive release does not prove that the production site serves the same qualified revision.

**Independent Test**: Run the fail-closed production verifier against the completed Pages deployment for merged main and confirm every discovered route at mobile and desktop widths has zero WCAG 2.1 AA violations.

**Acceptance Scenarios**:

1. **Given** merged main and a successful Pages deployment, **When** production is inspected, **Then** it serves the release revision over HTTPS with the complete expected route inventory.
2. **Given** every public route and representative downloadable resource, **When** the production contract runs, **Then** canonical metadata, structured data, media types, payload signatures, responsive behavior, both themes, and accessibility checks pass.
3. **Given** successful public release and production evidence, **When** housekeeping runs, **Then** issue #140 and milestone 24 close with evidence and no unrelated issue is closed.

### Edge Cases

- If v1.2.1 already exists locally, remotely, or as a GitHub release, publication halts unless every target and public artifact exactly matches the intended verified release.
- If the merge result differs from the reviewed head, the complete candidate gate reruns against actual main before tagging.
- If an automatic Codex review yields only a thumbs-up reaction or explicit no-findings result, the round is complete only after review records and unresolved threads are checked.
- No manual second Codex review round is requested because this instruction authorizes release completion but does not authorize an extra review trigger.
- If release or Pages automation fails, issue #140 and milestone 24 remain open until the defect is corrected and the affected contract passes.
- Generated kits, exports, archives, downloaded public assets, screenshots, and generated notes remain ignored and uncommitted.

## Requirements

### Functional Requirements

- **FR-001**: S013 MUST publish complete Spec Kit artifacts and sanitized evidence under `specs/013-v1-2-1-release/`.
- **FR-002**: GitHub milestone 24 and issue #140 MUST track candidate, review, publication, public-asset, and production evidence without closing before every acceptance criterion passes.
- **FR-003**: The release MUST use patch version 1.2.1 because it contains backward-compatible site and identity corrections plus a dependency security fix.
- **FR-004**: Root and skill changelogs MUST preserve applicable Unreleased history in dated v1.2.1 sections, retain prior history, and leave clean Unreleased sections.
- **FR-005**: Skill, canon, site, all production-brand canon references, notes, packaging, and workflow preflight MUST agree on v1.2.1.
- **FR-006**: Production-brand `version` values MUST remain independently governed and unchanged.
- **FR-007**: Release notes MUST state skill version, canon version, and the conditional migration impact of the ShruggieTech icon and site changes.
- **FR-008**: Release validation MUST recognize the v1.2.1 history and reject incomplete or contradictory metadata.
- **FR-009**: Candidate packaging MUST produce exactly seven assets: one installable skill, one portable skill archive, and one archive for each of five production brands.
- **FR-010**: All production kits MUST report zero `verify.py` problems and zero `validate_glyph.py` failures before publication.
- **FR-011**: The slice MUST pass Python 3.8 compatibility, all Python tests, the full production build, release packaging and verification, agent synchronization, site lint and export, browser verification, Markdown policy, and repository hygiene.
- **FR-012**: The committed change MUST contain no generated output, secret, private workstation path, provider identifier, BOM, CRLF text, or mojibake.
- **FR-013**: The pull request MUST track #140 without closing it at merge, because publication and production proof occur afterward.
- **FR-014**: Every automatic Codex review comment MUST receive a substantive disposition, every warranted correction MUST be verified, and every addressed thread MUST be resolved before merge.
- **FR-015**: S013 MUST NOT manually trigger Codex review or create a second review round.
- **FR-016**: After checks and review pass, the pull request MUST be merged, actual main synchronized, and the complete candidate gate rerun before tagging.
- **FR-017**: The annotated v1.2.1 tag MUST target verified main and GitHub Actions MUST remain the sole builder and publisher of official release assets.
- **FR-018**: The public release MUST be non-draft and non-prerelease, carry generated notes, and expose exactly seven expected assets.
- **FR-019**: Seven freshly downloaded public assets MUST pass the repository release contract without substituting local candidate output.
- **FR-020**: The production Pages deployment MUST pass the full route, resource, payload, metadata, responsive, theme, and WCAG 2.1 AA contract.
- **FR-021**: Issue #140 and milestone 24 MUST close only after public release and production evidence pass, and no unrelated issue may be closed.

### Key Entities

- **Release candidate**: The reviewed source revision and synchronized v1.2.1 metadata from which CI can rebuild the release.
- **Release asset set**: Exactly two skill distributions and five production-kit archives, each validated by the shared release contract.
- **Publication evidence**: Immutable tag, workflow, release, asset inventory, checksum, and fresh-download verification records.
- **Production certification**: Pages revision plus route, resource, discovery, responsive, theme, and accessibility results.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Skill, canon, site, five production canon references, both changelogs, generated notes, and packaging report one v1.2.1 candidate with zero version mismatches.
- **SC-002**: Five production kits complete with zero verification problems and zero glyph failures.
- **SC-003**: Exactly seven candidate assets pass the release contract with zero missing, unexpected, unsafe, malformed, or checksum-invalid files.
- **SC-004**: All required pull-request checks pass, every review comment is answered, and zero actionable review threads remain unresolved.
- **SC-005**: Tag v1.2.1 targets verified main and the public release exposes exactly seven CI-built assets.
- **SC-006**: Seven of seven freshly downloaded public assets pass the release contract.
- **SC-007**: Production verification covers every discovered HTML route at 360px and 1280px with zero failures and zero WCAG 2.1 AA violations.
- **SC-008**: Sanitized scans report zero committed generated outputs, private paths, secrets, provider identifiers, BOMs, CRLF text files, or mojibake markers.
- **SC-009**: GitHub reports #140 and milestone 24 closed only after SC-001 through SC-008 are evidenced.

## Assumptions

- v1.2.1 is the next available semantic version after v1.2.0.
- The S012 visual and wording corrections are backward-compatible, and Brotli 1.2.0 is a backward-compatible security update.
- Existing ShruggieTech kits and the site should be rebuilt for the corrected black-background icon source; other production kits need no consumer migration beyond optional canon-metadata parity.
- GitHub Actions remains the sole publisher of official release assets.
- The current production verifier and seven-asset release contract remain authoritative.
