# S003 Evidence Ledger

## Baseline

- Verification base: `cbd96487dec1a19d93695910ec4337729acb1325`
- Base ref: `origin/main`
- Feature branch: `codex/003-reconcile-pr-reviews`
- Pull request: pending
- Public-content sensitive-data scan: pass across all 19 prospective files; no private path, credential, provider identifier, BOM, CRLF, invalid UTF-8, or mojibake finding

## Inherited Review Findings

| Task | Issue | Source thread | Focused evidence | Disposition | Reply | Thread |
|---|---:|---|---|---|---|---|
| 003-T001 | #17 | PR #16 `r3929374475` | Python 3.8-safe discovery regression and hosted minimum-version job | Fixed on main | Pending | Unresolved |
| 003-T002 | #18 | PR #16 `r3929374485` | Generated `next/font/local` binding, bundled font paths, and offline regression | Fixed on main | Pending | Unresolved |
| 003-T003 | #19 | PR #16 `r3929374492` | Lower-tier PDF skip regression, full-tier fatal behavior, and seven-archive dry run | Fixed on main | Pending | Unresolved |
| 003-T004 | #20 | PR #16 `r3929374496` | Named page-QC skip and full-tier fatal regressions plus six-kit build | Fixed on main | Pending | Unresolved |
| 003-T005 | #21 | PR #16 `r3929374502` | Route regression, live route fetches, and successful real shadcn install in a clean temporary project | Fixed on main | Pending | Unresolved |
| 003-T006 | #22 | PR #16 `r3929374508` | Existing runtime regression expanded to all kit scripts; remaining header nesting corrected | Fixed in S003 | Pending | Unresolved |
| 003-T007 | #23 | PR #16 `r3929374510` | Generated native required-state regression across input, textarea, and select | Fixed on main | Pending | Unresolved |
| 003-T008 | #24 | PR #16 `r3929374514` | Hidden non-interactive Windows subprocess regression | Fixed on main | Pending | Unresolved |
| 003-T009 | #25 | PR #16 `r3929374522` | Core-tier vector retention and raster-skip regression; ImageMagick measurement and QC fallback corrected | Fixed in S003 | Pending | Unresolved |
| 003-T010 | #27 | PR #26 `r3929603634` | Stale PDF removal regression | Fixed on main | Pending | Unresolved |
| 003-T011 | #28 | PR #26 `r3929603638` | Stale raster and favicon removal regression | Fixed on main | Pending | Unresolved |
| 003-T012 | #29 | PR #26 `r3929603642` | Independently measured ICO-writer regression | Fixed on main | Pending | Unresolved, outdated |
| 003-T013 | #30 | PR #26 `r3929603645` | Markdown physical-line policy check and regression | Fixed on main | Pending | Unresolved, outdated |
| 003-T014 | #31 | PR #26 `r3929696253` | Hosted Python 3.8 job executes the pipeline suite | Fixed on main | Pending | Unresolved, outdated |
| 003-T015 | #32 | PR #26 `r3929734673` | Pillow-inclusive raster regression; implemented renderer measurement aligned with generation and QC | Fixed in S003 | Pending | Unresolved |
| 003-T016 | #33 | PR #26 `r3929734677` | Stale page-QC removal regression | Fixed on main | Pending | Unresolved |
| 003-T017 | #34 | PR #26 `r3929778306` | Pillow-independent image-master regression | Fixed on main | Pending | Unresolved |
| 003-T018 | #35 | PR #26 `r3929778312` | Stale PDF contact-sheet and extracted-page removal regression | Fixed on main | Pending | Unresolved |
| 003-T019 | #36 | PR #26 `r3929848183` | Deferred Pillow import and named core-tier QC skip regression | Fixed on main | Pending | Unresolved |

## Work-Order Certification

| Phase | Candidate children | Deliberate exclusions | Decision |
|---|---|---|---|
| #6 Phase 1 | #39-#46 | None | #40, #43-#46 appear complete; #39, #41, and #42 require unavailable or private evidence, so parent remains open |
| #7 Phase 2 | #47-#49 | None | All children appear complete; parent is eligible after public evidence is posted |
| #8 Phase 3 | #50-#58 | None | #52, #55, and #58 depend on branch-only fixes; parent remains open |
| #9 Phase 4 | #59 | None | Child and parent appear complete after public evidence is posted |
| #10 Phase 5 | #60-#62 and #38 | #63 release publication | #60-#62 appear complete; #38 and #63 remain open, so parent remains open |
| #11 Phase 6 | #64-#67 | None | All children appear complete; parent is eligible after public evidence is posted |
| #12 Phase 7 | #68-#70 | None | All children appear complete subject to final sanitized public checks |
| #13 Phase 8 | #71-#72 | #73 published release inspection | #71 appears complete; #72 depends on the S003 changelog correction and remains open until merge; parent remains open |
| #14 Phase 9 | #74 | #75 unless current deployment is proven | #74 requires the clean S003 checkout result and remains open until merge; #75 and parent remain open |
| #15 Phase 10 | None | #76-#86 | Out of scope, parent remains open |
| #37 Program | All phases | Incomplete release, deployment, and staging work | Parent remains open |

## Verification Runs

| Check | Environment | Result | Evidence |
|---|---|---|---|
| Focused pipeline regressions | Local branch | Pass | 16 tests passed |
| Glyph tests | Local branch | Pass | 31 checks, 0 failures |
| Capability probe | Local branch | Pass | Full tier; ImageMagick and Chromium measured |
| Six-kit build and verification | Local branch | Pass | Six kits, 0 verification, image-QC, PDF-QC, or pagination problems |
| Site lint and static export | Local branch | Pass | ESLint clean; Next.js exported 25 routes |
| Seven-archive packaging dry run | Local branch | Pass | Exactly seven expected archives built |
| Clean repository-only rebuild | Separate checkout | Pending | Pending |
| Hosted pull-request checks | GitHub Actions | Pending | Pending |

Manual inspection covered all six logo sheets, all eleven desktop and 390-pixel page sheets, and all six PDF contact sheets. No clipping, overflow, blank page, unreadable type, or identity-art defect remained after the S003 fixture corrections.

## Codex Review Rounds

| Round | Trigger | Signal | Actionable comments | State |
|---|---|---|---:|---|
| 1 | Automatic on pull-request publication | Pending | Pending | Pending |
| 2 | One explicit `@Codex` comment after round 1 | Not requested | Pending | Pending |

Review request ceiling: 2 rounds. No third request is authorized.

## Final Gate

- All inherited review threads answered and resolved: pending
- Every candidate issue evaluated with public evidence: pending
- Eligible issue and parent closures completed: pending
- Local verification green: pending
- Hosted checks green: pending
- Both Codex rounds complete: pending
- Pull request remains open for owner merge: pending
