# Verification Evidence: Approved Identity Construction Continuity

## Session 1: Specification and baseline (2026-09-09)

- Current `main` and `origin/main` were clean and synchronized at merged S026 revision `011f35303ef1d555dbbbcf6708447cc321df40db` before branch creation.
- GitHub issue #185 was open with P0, large-effort, brand, governance, generator, and Spec Kit labels. S026 issue #184 was already closed by merged PR #186, so Cueson is regression evidence rather than a pending identity.
- Work proceeds on `codex/027-approved-identity-construction-continuity`; machine-local `.specify/feature.json` selects `specs/027-approved-identity-construction-continuity/` and remains ignored.
- Spec Kit ran in order through specify, clarify, checklist, plan, tasks, and analyze. The requirements checklist passed 16/16. The identity-continuity requirements checklist passed 30/30 after analysis resolved the one-master exception, clarified Covarity’s provenance-only correction, and added runtime-measurement coverage. Cross-artifact analysis found zero critical issues.
- Constitution P1 through P6 pass before and after design. Source contracts and tests are committed; proof images, audit reports, kits, PDFs, rasters, registries, archives, site exports, and local Spec Kit state remain ignored.
- The pre-migration manifest at `dist/identity-continuity-preflight.json` binds all seven brand source files and governed identity snapshots to merged S026. It records source mode, geometry provenance, and showcase state before any migration edit.

## Pre-migration authoritative snapshot

| Brand | `brand.json` SHA-256 | Governed identity SHA-256 | Mode | Provenance | Showcase |
| --- | --- | --- | --- | --- | --- |
| Covarity | `248632525eabc5a763ef9b2fa9daeff5ff522dfd046fdef35a902069532afbb0` | `e08afbd58482a65e3e1b9d7403d3592738b7c01da1b58366fdd1332dcb2f6d00` | constructed | glyphkit (inaccurate legacy label) | public |
| Cueson | `c7ccf159094336d61ae7a4ff3db2b73f5d8b6e4adbfd20784fd4c8ce6c4df5ab` | `8f2dec61bc1e38fc469b116825819ebfefe5a9fc946055133b941b3e809cadf5` | constructed | glyphkit | public |
| ESO Weave | `851c60f86ded48b65ef7b86e255726c48ae8b81a745205a1118674238fd27d98` | `dc6adef1aef2f1f55e323eb48656351625b4315fe8476b4360d08ae5e8d70008` | authoritative | imported | public |
| Fragcap | `5db92d25db7b520e341ba2ef04827feebb041c33d000e693e3d6885f16d1a006` | `d321b43079e8fae2ffcdd37f0fcd7c37585253956edfabaf0e7f907322ea0049` | constructed | imported | public |
| Glitchpad | `3abbbd907a3060e5be66599dbfff71249387a98fcdcf563223c4c3070d593acd` | `43b83d4a90275ce05a7b3a09a1cfc91ff07621d83260939c7deab9b74967bfe8` | constructed | imported | public |
| Go Schedule | `4ce04c5456d342d19a8bd27c038bdb9c376ce5f0ff63f29ea14b852ade4b4e0d` | `29c086707119b323eadef51f72201d755c5af9af348e852ba109a99de3d5183d` | constructed | imported | public |
| ShruggieTech | `d3f98436b384ac2027c62bebc92cdf2ff7e1e8612f181f66b2841f4c59de37c7` | `15f40f029a2b6d90ed9c5c7b80954587b4e738acdc39afbfabb21c97b0e2e7cf` | authoritative | imported | public |

## Implementation evidence

### Session 2: Foundation and approval lifecycle (2026-09-09)

- The first focused identity test run failed with `ModuleNotFoundError: identity_continuity`, establishing the expected red baseline before the shared module existed. The implemented suite now passes 18/18 tests.
- Canonical serialization rejects duplicate JSON keys and malformed digests. Safe path resolution rejects absolute paths, parent traversal, backslashes, symbolic links, missing files, and root escapes.
- Identity snapshots bind source class, exact Full and Reduced path arrays or authoritative bindings, topology, framing, palette roles, and wordmark typography. Lifecycle tests prove that direction selection cannot jump to canonical approval and a historical baseline cannot be promoted.
- Approved-canonical records require complete human approval, renderer identity, bounded OKLCH palette qualification, and the exact 32-coordinate Full/Reduced, size, and surface proof matrix. Each proof is hash-bound and verified as a valid PNG with dimensions matching its declared coordinate. Same-renderer evidence requires exact file hashes. Cross-renderer evidence preserves topology and uses a one-pixel edge band plus bounds, centroid, changed-pixel, and interior Delta E measurements.
- The approval ledger now requires an approved continuity-record digest for prospective Gate 1 canonical source authority, while historical records reject that binding. Gate 2 remains derivative and publication authority only.

### Session 3: Promotion, migration, and integration (2026-09-09)

- Promotion validates the complete approved continuity record, owner wording and scope, source snapshot, glyphkit helper, palette qualification, renderer, and proof matrix before mutation. It rejects executable sources, generated proof destinations, undeclared source files, duplicates, stale hashes, traversal, symlinks, and external roots.
- Exact source and continuity-record bytes are copied into a bounded sibling staging directory. Tests prove refusal of an existing destination without explicit replacement and restoration of the last-known-good destination after a simulated partial-install failure.
- The migration audit first failed because all seven committed records were absent. After migration, all seven validate with zero audit problems and preservation `passed` against baseline revision `011f35303ef1d555dbbbcf6708447cc321df40db`.
- Cueson is `glyphkit-constructed`; ESO Weave and ShruggieTech are `authoritative`; Covarity, Fragcap, Glitchpad, and Go Schedule are truthful `legacy-constructed` baselines. Historical evidence explicitly denies retrospective canonical approval.
- Covarity’s only allowed source change is its provenance label and reason. The custom helper and every shipped path value remain unchanged. All other brands differ only by the continuity reference.
- Build validation now runs before any derivative step and emits `identity-continuity-report.json`. Final verification independently regenerates and checks that report. Pipeline regressions reject Cueson helper, source, method, geometry, framing, palette, and generated-report drift.

### Session 4: Workflow and visual evidence (2026-09-09)

- `identity-continuity.md`, the interview, logo protocol, glyph construction guidance, schema, skill routing, and generated `AGENTS.md` now share one lifecycle. Direction selection is nonbinding, production construction and palette qualification precede canonical approval, and Gate 2 cannot reconstruct or first reveal master geometry.
- The unchanged Cueson production mark passed cross-renderer policy with topology `{components: 5, holes: 0}`, silhouette IoU `1.0`, changed-outside-edge fraction `0.0`, bounds delta `0`, centroid delta `0.0`, and interior Delta E `0.0`. Side-by-side, overlay, silhouette-XOR, and color-difference evidence was emitted under ignored `dist/` and visually inspected.
- All seven logo contact sheets were visually inspected after clean builds. No geometry, holes, clipping, framing, palette, or reduced-master regressions were observed.

## Final local validation

- Focused and regression matrix: 34 glyphkit checks, 5 package-release tests, 14 release-contract tests, 29 site-preparation tests, 40 brand-contract tests, 18 identity-continuity tests, 4 migration-audit tests, 14 iconkit tests, 51 pipeline tests, and Markdown policy all passed. The final pipeline rerun completed in 172.827 seconds on Python 3.12.9.
- Migration audit: 7/7 production records valid, 7/7 preservation comparisons passed, zero problems.
- Production build: 7/7 kits built clean with zero verification problems and zero glyph failures. Continuity validation ran before derivatives for every kit. The aggregate run completed in approximately four minutes, under the planned baseline plus 60-second continuity budget.
- Release certification: nine version 1.2.1 assets and generated notes verified without publishing a tag or release.
- Generated-agent synchronization: `skill/AGENTS.md` regenerated from `skill/SKILL.md`; the generated diff check passes.
- Site: content preparation and TypeScript lint passed, the static build generated 73 pages, and browser verification covered 68 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- Two expected integration failures were resolved during validation: the new reference initially lacked a navigation assignment, then Portability’s pagination expectation omitted its new Continuity neighbor. The final lint, build, and browser rerun is green.
- Generated kits, proofs, audit reports, release archives, site output, browser artifacts, and local Spec Kit state remain ignored. The final 51-file source scan found no UTF-8 BOM, mojibake, private workstation paths, CRLF or mixed tracked endings, whitespace errors, or em dashes in authored changes.

## Hosted CI and review ledger

Pending publication. The authorized PR review and hosted-check ledger will be appended after push.
