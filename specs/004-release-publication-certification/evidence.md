# Evidence: v1.1.2 Release and Publication Certification

## Baseline

| Item | Initial state |
| --- | --- |
| Verified base | `8553d7f8aba090962983b184cffa57f71389a808` on `origin/main` |
| v1.1.2 tag | Absent at slice start |
| v1.1.2 release | Absent at slice start |
| Open pull requests | None at slice start |
| Release children | #63, #72, and #73 open |
| Phase parents | #10 and #13 open |
| Program parent | #37 open |
| Phase milestones | 15 and 18 open |

## Discovered contradictions and corrections

| Finding | Ground truth | S004 decision |
| --- | --- | --- |
| Root 1.1.2 history was split | Three merged S003 corrections remained under Unreleased while the bundled skill already listed them under 1.1.2 | Fold the merged corrections into root 1.1.2 and keep Unreleased empty |
| Release body was not changelog-derived | The workflow hardcoded a summary and linked to the changelog | Generate and publish the exact version section plus validated metadata |
| Kit manifest version could disagree | Manifest generation hardcoded 1.0.0 while Fragcap declares 1.1.0 | Generate manifest version from `brand.json` and verify the three-way match |
| Workflow archive assertion was partial | Inline workflow logic checked only root licenses | Replace it with the reusable complete release contract |

## Local verification

| Gate | Result | Evidence |
| --- | --- | --- |
| Release-contract regressions | PASS | 6 tests passed, including metadata, notes, unsafe paths, bundle shape, checksum drift, and unexpected assets |
| Pipeline regressions | PASS | 18 tests passed, including the new declared manifest-version regression |
| Glyph construction | PASS | 31 checks and 0 failures |
| Full six-kit rebuild | PASS | Five production kits and the fixture built at full capability with 0 reported problems and 0 glyph failures |
| Visual contact sheets | PASS | Logo and page contact sheets for all six targets were reviewed as one generated montage; no new visual defect was observed |
| PDF and pagination QC | PASS | All six targets reported 0 PDF QC problems and 0 split elements |
| Release packaging | PASS | Exactly 7 expected archives were produced and the shared verifier accepted metadata, licenses, bundle shape, PDFs, versions, and recorded checksums |
| Release notes | PASS | Generated from root 1.1.2 history with skill 1.1.2, canon 1.1.2, and explicit rebuild migration guidance |
| Static site | PASS | TypeScript lint passed and Next.js exported 25 static pages |
| Generated agent contract | PASS | Sync reported unchanged output |
| Text and public-data hygiene | PASS | 19 changed files passed UTF-8 without BOM, LF, mojibake, private-path, secret, and provider-identifier scans |
| Clean-checkout repetition | PASS | Detached committed checkout passed 6 release tests, 18 pipeline tests, 31 glyph checks, Markdown policy, full six-kit build, exact seven-archive preflight, site lint, 25-page export, and remained clean |

## GitHub traceability

| Record | Link | State |
| --- | --- | --- |
| S004 slice issue | https://github.com/shruggietech/shruggie-brand/issues/90 | Open through publication |
| Issue #63 | https://github.com/shruggietech/shruggie-brand/issues/63 | Open pending publication |
| Issue #72 | https://github.com/shruggietech/shruggie-brand/issues/72 | Open pending publication |
| Issue #73 | https://github.com/shruggietech/shruggie-brand/issues/73 | Open pending publication |
| Pull request | Pending | Pending |

Pre-merge acceptance comments: [#63](https://github.com/shruggietech/shruggie-brand/issues/63#issuecomment-5536081006), [#72](https://github.com/shruggietech/shruggie-brand/issues/72#issuecomment-5536081269), [#73](https://github.com/shruggietech/shruggie-brand/issues/73#issuecomment-5536081492), and [#90](https://github.com/shruggietech/shruggie-brand/issues/90#issuecomment-5536081710).

## Codex review ledger

| Round | Trigger | Signal | Actionable comments | Finding issues | State |
| --- | --- | --- | ---: | --- | --- |
| 1 | Automatic on PR publication | Pending | Pending | Pending | Pending |
| 2 | One explicit `@Codex` comment after round 1 | Not requested | Pending | Pending | Pending |

Review request ceiling: 2 rounds. No third request is authorized.

## Hosted checks

Pending pull-request publication.

## Post-merge publication

Blocked on the owner merge ritual. No tag, release, issue closure, parent closure, or milestone closure is claimed by pre-merge evidence.
