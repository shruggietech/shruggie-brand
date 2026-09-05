# Feature Specification: v1.2.0 Release and Production Certification

**Feature Branch**: `codex/010-v1-2-release-certification`

**Created**: 2026-09-05

**Status**: Ready for Review

**Input**: Prepare the completed S006 through S009 work as v1.2.0, certify the release candidate, publish an official pull request, process no more than two Codex review rounds, stop for the owner merge ritual, then publish and independently verify the tagged release and deployed production site.

## User Scenarios & Testing

### User Story 1 - Coherent release candidate (Priority: P1)

As the release owner, I can review one source revision whose histories, brandbuilder version, canon version, production-brand canon references, site package metadata, packaging behavior, release notes, and continuous-integration release preflight all agree on v1.2.0.

**Why this priority**: A tag publishes immutable assets. Version drift or incomplete history must fail before the owner considers the release pull request.

**Independent Test**: Build every production kit and all release archives from a clean source checkout, generate the v1.2.0 notes, and run one repository-owned verifier that accepts exactly seven assets while rejecting stale or contradictory version metadata.

**Acceptance Scenarios**:

1. **Given** the completed S006 through S009 work under Unreleased, **When** the v1.2.0 candidate is prepared, **Then** both changelogs preserve that history under one dated v1.2.0 section and retain a clean Unreleased heading for future changes.
2. **Given** the v1.2.0 candidate metadata, **When** preflight runs, **Then** skill, canon, production-brand canon references, site package, generated notes, packaging, and workflow inputs agree without changing independent production-brand versions.
3. **Given** freshly rebuilt distribution output, **When** packaging and verification run, **Then** exactly two skill distributions and five production-kit archives pass the complete release contract.
4. **Given** a stale version literal, incomplete history, missing asset, unsafe archive entry, missing license, invalid PDF, incomplete manifest, or checksum mismatch, **When** preflight runs, **Then** it exits nonzero and identifies the failed rule.

---

### User Story 2 - Bounded reviewed handoff (Priority: P1)

As the repository owner, I receive an open S010 pull request with successful required checks and every Codex review comment dispositioned after no more than the automatic review and one explicit second round.

**Why this priority**: Release readiness includes complete review handling while merge authority remains exclusively with the owner.

**Independent Test**: Inspect the pull request review ledger, review threads, issue links, comment history, head revision, and required checks. There are no unresolved actionable findings, no more than one explicit `@Codex` request, no merge, and no v1.2.0 tag.

**Acceptance Scenarios**:

1. **Given** the official S010 pull request, **When** automatic Codex feedback arrives, **Then** every comment receives a substantive disposition and every warranted correction is implemented and verified.
2. **Given** a negative review finding, **When** it is accepted for correction, **Then** a linked GitHub issue records the source comment, risk, acceptance criteria, labels, and milestone before its review thread is resolved.
3. **Given** round one is complete, **When** the authorized second round is requested, **Then** exactly one explicit `@Codex review` comment is posted and no later event requests another round.
4. **Given** all authorized review feedback is resolved and required checks are successful, **When** handoff occurs, **Then** the pull request remains open and the owner is asked to perform the final review and merge ritual.

---

### User Story 3 - Evidence-backed public release (Priority: P2)

As a release consumer, I can obtain v1.2.0 from GitHub and see exactly seven CI-built assets whose release notes, licenses, versions, required documents, manifests, and checksums pass the same contract used before merge.

**Why this priority**: Public release evidence can exist only after the owner merges the reviewed source revision.

**Independent Test**: From the verified merged main revision, create the v1.2.0 tag once, wait for the release workflow, download the release body and assets into an empty directory, and pass the repository release verifier without substituting local artifacts.

**Acceptance Scenarios**:

1. **Given** the owner has merged S010, **When** post-merge publication starts, **Then** actual `origin/main` is synchronized and revalidated before tag creation.
2. **Given** a successful tag workflow, **When** the GitHub release is inspected, **Then** it is public, non-draft, non-prerelease, targets verified main, and contains exactly seven assets plus generated release notes.
3. **Given** freshly downloaded public assets, **When** verification runs, **Then** seven of seven pass the complete release contract.

---

### User Story 4 - Qualified production deployment (Priority: P2)

As a brand-site visitor or internal brand operator, I can use the deployed site after v1.2.0 publication and obtain working skill, brand, registry, and native-icon resources while the route discovery, accessibility, responsive layout, and both visual themes remain intact.

**Why this priority**: A successful source build does not prove that the deployed domain or its downloadable resources are usable.

**Independent Test**: Against the completed Pages deployment for merged main, inspect the full route inventory plus representative downloads, registry responses, metadata, both themes, desktop and mobile layouts, and accessibility results.

**Acceptance Scenarios**:

1. **Given** merged main and a successful Pages deployment, **When** the production domain is inspected, **Then** it serves the merged release state over HTTPS with no stale route inventory.
2. **Given** representative skill, brand, registry, and icon links, **When** they are requested from production, **Then** each returns the expected content type and a non-empty valid payload.
3. **Given** every public route, **When** discovery output is inspected, **Then** strict canonical URLs, route-specific metadata, social previews, structured data, sitemap membership, and robots policy remain consistent.
4. **Given** representative documentation and portfolio routes, **When** checked at desktop and mobile widths in both themes, **Then** there are zero WCAG 2.1 AA violations and no material visual regression.

### Edge Cases

- If v1.2.0 already exists locally or remotely, publication halts unless its tag target, release target, notes, and assets exactly match the intended verified release.
- If a squash or concurrent change makes merged main differ from the reviewed head, post-merge publication repeats the complete candidate verification against actual main before tagging.
- If a release or Pages workflow fails, issues #118 and #119 remain open and no milestone or slice parent closes.
- If an automatic Codex review yields only a thumbs-up reaction or explicit no-findings message, the round is complete only after pending review threads and review records are checked.
- Corrections made after round two never trigger a third review request. Late comments from either authorized round are still answered and resolved.
- Public release verification uses a newly created empty download directory so stale local assets cannot satisfy the contract.
- Production certification distinguishes a delayed deployment from a bad deployment and records the actual workflow and deployed revision before deciding issue state.
- Generated kits, site exports, archives, and generated release notes remain disposable ignored output and never enter the commit.

## Requirements

### Functional Requirements

- **FR-001**: S010 MUST publish its specification, plan, tasks, contracts, checklists, and sanitized verification evidence under `specs/010-v1-2-release-certification/`.
- **FR-002**: GitHub milestone 22 MUST track parent issue #116 and child issues #117, #118, and #119, with release-candidate work separated from post-merge publication and production evidence.
- **FR-003**: The next brandbuilder and canon version MUST be 1.2.0 because S006 through S009 add backward-compatible public capabilities and do not remove or incompatibly redefine the established brand-source contract.
- **FR-004**: Root and bundled skill changelogs MUST preserve all current Unreleased entries in a dated 1.2.0 section, preserve earlier release history, and leave a clean Unreleased section.
- **FR-005**: `skill/SKILL.md`, authoritative canon metadata, site package metadata, each production source's canon reference, generated release notes, packaging defaults, and continuous-integration release preflight MUST agree on 1.2.0.
- **FR-006**: Production brand versions MUST remain independently governed and MUST NOT be changed merely because the brandbuilder and canon advance to 1.2.0.
- **FR-007**: Release tooling MUST derive the current candidate version from one validated authoritative metadata path where practical instead of requiring duplicated workflow and packaging literals.
- **FR-008**: Release history validation MUST recognize 1.2.0 and retain explicit historical validation for earlier required releases without embedding 1.1.2 as the only current release.
- **FR-009**: Local candidate packaging MUST produce exactly seven files: the installable skill distribution, the portable skill archive, and one archive for each of the five production brands.
- **FR-010**: All seven release assets MUST pass the existing type-specific metadata, licensing, archive-safety, version, PDF, manifest coverage, and checksum rules.
- **FR-011**: Every production kit MUST report zero problems from `verify.py` and zero failures from `validate_glyph.py` before the release candidate is considered ready.
- **FR-012**: S010 MUST run the documented Python 3.8 compatibility tests, full Python tests, complete production build, release packaging and contract, generated agent synchronization, site lint, static export, site tests, Markdown policy, and repository hygiene gates.
- **FR-013**: The committed change MUST contain no generated kit, generated site export, release archive, generated release note, private workstation path, secret, provider identifier, BOM, CRLF text, or mojibake.
- **FR-014**: The pull request MUST close #117 only, and MUST track #116, #118, and #119 without closing them before public evidence exists.
- **FR-015**: Every Codex review comment MUST receive a substantive response, every warranted correction MUST be tested and pushed, and every addressed review thread MUST be resolved.
- **FR-016**: Every negative Codex finding MUST be filed as a GitHub issue with source linkage, appropriate labels and milestone, rationale or reproduction, and testable acceptance criteria before resolution.
- **FR-017**: S010 MUST permit no more than two Codex review rounds: the automatic round and at most one explicit `@Codex review` request after round one completes.
- **FR-018**: S010 MUST NOT merge its own pull request or create the v1.2.0 tag before the owner completes the final merge ritual.
- **FR-019**: After owner merge, the actual merged main revision MUST pass the complete candidate gate before one annotated v1.2.0 tag is pushed.
- **FR-020**: The tagged workflow MUST build release assets from tagged source and publish generated notes, and public verification MUST use a fresh download rather than local artifacts.
- **FR-021**: Production certification MUST record the Pages workflow result, deployed revision, route inventory, representative download and registry responses, metadata and discovery parity, both themes, responsive layouts, and WCAG 2.1 AA results.
- **FR-022**: Issue #117 MAY close on merge of the reviewed candidate. Issues #118 and #119 MUST remain open until their public evidence is attached. Parent #116 and milestone 22 MUST close only after all three children are evidence-complete.

### Key Entities

- **Release Candidate**: The reviewed source revision, version metadata, history, generated notes, expected asset set, and complete local validation evidence.
- **Version Authority**: The validated relationship among skill version, canon version, site package version, production-brand canon references, packaging, and workflow preflight.
- **Release Asset Contract**: The exact seven expected filenames and their type-specific archive, licensing, metadata, PDF, manifest, and checksum requirements.
- **Review Round**: One authorized Codex arrival signal, its findings, responses, corrections, issue links, thread resolutions, and immutable trigger or signal link.
- **Publication Evidence**: The actual merged revision, annotated tag target, release workflow, release URL, generated notes, downloaded assets, and verifier output.
- **Production Evidence**: The Pages workflow, deployed revision, route inventory, resource responses, metadata and discovery results, accessibility audit, and visual checks.
- **Closure Set**: Child issues #117 through #119, parent #116, and milestone 22, whose state advances only when each record's evidence gate is fulfilled.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All version-authority surfaces agree on 1.2.0 while all five production brand versions remain unchanged.
- **SC-002**: The candidate build reports zero verification problems and zero glyph failures across five production kits.
- **SC-003**: Candidate packaging produces exactly seven expected release assets and seven of seven pass the shared contract with zero failures.
- **SC-004**: Python 3.8 compatibility, full Python tests, generated-agent synchronization, site lint, static export, site tests, Markdown policy, encoding, sensitive-data, and generated-artifact gates all pass.
- **SC-005**: The S010 pull request has zero unresolved actionable Codex comments after no more than two review rounds and no more than one explicit `@Codex review` request.
- **SC-006**: Before owner merge, the S010 pull request remains open and no S010-created v1.2.0 tag or release exists.
- **SC-007**: After owner merge, the v1.2.0 release targets verified main, is public and non-prerelease, contains exactly seven assets, and seven of seven freshly downloaded assets pass verification.
- **SC-008**: The production route inventory has zero missing routes, representative downloadable resources have zero invalid responses, and representative desktop and mobile pages in both themes have zero WCAG 2.1 AA violations.
- **SC-009**: GitHub reports issue and milestone states consistent with the evidence policy: #117 after merge, #118 and #119 after public proof, and #116 plus milestone 22 only after all children close.
- **SC-010**: Sanitized scans report zero committed generated artifacts, BOMs, CRLF text files, mojibake markers, private paths, secrets, or provider identifiers in the S010 change set.

## Assumptions

- The owner will merge the reviewed S010 pull request before post-merge publication and production certification continue.
- GitHub Actions remains the sole publisher of official release assets; local artifacts are disposable candidate evidence only.
- A minor version increment is appropriate because the accumulated work adds ownership-neutral inputs, authoritative supplied assets, native icon suites, portfolio and documentation behavior, and discovery coverage while retaining the existing source and archive contracts.
- Existing production-brand versions stay unchanged because no identity revision is included in S010; only their canon reference advances.
- The current release contract remains authoritative and is generalized only where its hardcoded current-version assumptions would otherwise make v1.2.0 unsafe or unnecessarily repetitive.
- The two post-merge issues intentionally remain open at the owner handoff and will be completed during standard post-merge housekeeping.
