# S065 Restart Evidence

## 2026-09-29: new Gate 1 candidate

- Branch `codex/065-dancewithme865-restart` starts from `origin/main` in a separate managed worktree. The prior S065 worktree and its approvals were not reused.
- The owner image is direction. The selected supplied light stacked SVG uses the same angular DWM over upright DANCEWITHME and a red 865 block. Selected SVG bytes are unchanged from the supplied ZIP; the archive layout did not become a kit schema.
- Candidate `dwm865-s065-g1-r1` is recorded in [gate-1-proposal.json](gate-1-proposal.json), packet SHA-256 `19a7cd432831f0085f858a6b52c0a253accf3c60a10d91371f34fa2a25343a2d`. Its source inventory has 10 SVGs, 4 font binaries, and pending `brand.json`. The snapshot and renderer are bound to this candidate. No owner approval is recorded.
- Formal palette qualification passed all required role checks. The lowest measured text contrast is 4.503:1, including the off-white 865 numerals on the supplied red block.
- The production path rendered all 32 required Full and Reduced proofs at 256, 64, 32, and 16 pixels on dark, light, black, and white, plus four comparison artifacts per proof. The local review sheet is `dist/s065-gate1/gate1-32-proof-sheet.png`; the Natalie/source comparison is `dist/s065-gate1/natalie-vs-source.png`. These are ignored review artifacts, not repository sources.
- The 16 px light proof contains only a 14 by 4 px DWM ink area; at 32 px it is 25 by 8 px. The supplied Reduced artwork is still too wide for a clearly readable 16 px square icon. This is an explicit Gate 1 choice, not an unreported pass.
- Focused source-binding tests passed (2 contract tests and 1 production pipeline test). `git diff --check` passed. Final kit and site validation await both new creative approvals.

## Approval sequence

1. Gate 1 r1: the owner approved candidate `dwm865-s065-g1-r1` with the exact wording recorded in [gate-1-decision.json](gate-1-decision.json). That approval was superseded by the renderer and application icon changes described below.
2. Gate 1 r2: the owner approved candidate `dwm865-s065-g1-r2` with the exact wording recorded in [gate-1-decision-r2.json](gate-1-decision-r2.json). The approved source was promoted with canonical source binding `fb59ab31d5bfa0d5edda61e3c76cc4c84a517e96c11597848d2780640cf75f3c`.
3. Gate 2: the owner approved the exact derivative packet with wording recorded in [gate-2-decision.json](gate-2-decision.json). The approved packet SHA-256 is `a8f4283ce4986b8b8ca09ed02e11d6aeed4821b2c1676e66a236001798086b64`; its derivative manifest SHA-256 is `9b6d6ae94885dc4a0b14edc8d4ba854d3f212cce526e06d555aa6a3b5aabe727`. The owner separately selected `DanceWithMe865` as the only social image wording.

## 2026-09-29: private delivery check and revised Gate 1 candidate

- The first approved source was atomically promoted, and its 32 production proofs matched the approved hashes. The owner separately chose `DanceWithMe865` alone for the social share image.
- A private build with Gate 2 still pending exposed the too-small unplated Windows taskbar frames, a repeated brand name in the social image, and two independent generator defects: font license discovery missed new family names in `fonts/licenses/`, and specimen SVG placement rounded numbers beyond the verifier tolerance. The font resolver and numeric precision were corrected; the initial private build is not a final verification pass.
- Revised candidate [gate-1-proposal-r2.json](gate-1-proposal-r2.json) binds packet SHA-256 `5abca4ea8c0e238fb01d0b8f8aaea8feac20e6c5b9ada062fb64d7a2649ee5e8`. All 32 mark proof hashes remain identical to r1. The renderer settings digest changed, and the identity snapshot now includes a red plate and Reduced source for Windows application icons.
- The revised 16, 32, and 256 px icon previews are in ignored `dist/s065-gate1-r2/icon-preview/`. The Windows taskbar frame check passed with no problems. The 16 px DWM remains inherently small; no new glyph was invented.
- The generator now uses one lockup on a separate social canvas when the approved slogan is the brand title and no description is supplied. This revised social output was covered by renewed Gate 1 approval and is pending Gate 2 review.
- The generator update changes the whole-file renderer fingerprint for unrelated approved brands. A guarded legacy fingerprint applies only when the exact reviewed new generator bytes are present and a brand uses none of the new source or name-only social paths. Existing approved proof hashes remain mandatory. The I Heart PR Tours settings digest matched its recorded value under the same Pillow runtime, and a focused regression test passed. The local Node version differs from CI's pinned version, so cross-brand aggregate validation remains for the final gate.

## 2026-09-29: Gate 2 review packet

- The r2 Gate 1 promotion preserved the 10 selected SVG source bytes and produced a continuity record bound to the approved canonical source. The private derivative packet at `dist/s065-gate2/gate-2-packet.json` validated with 13 review surfaces; packet SHA-256 is `a8f4283ce4986b8b8ca09ed02e11d6aeed4821b2c1676e66a236001798086b64`.
- The packet includes the light stacked lockup matching the supplied direction, wide lockup, standalone wordmarks, Full and Reduced marks, a red plated Windows icon, palette, interface cues, support typography, a representative guidelines page, and a separate social share image. The social image uses one supplied horizontal lockup on a dark canvas and contains the brand name once, with no added slogan or description.
- A provisional private kit build completed generation, image checks, PDF checks, pagination, and affiliation checks. Its final verifier reported one expected problem: the assembled social SVG and PNG lack the distinct Gate 2 approval binding. This is not a final kit verification pass. Final aggregate and site validation remain pending Gate 2 approval.

## 2026-09-29: approved derivative binding

- The exact Gate 2 decision binds the reviewed manifest and social SVG/PNG hashes in `brands/dancewithme865/brand.json`. The canonical Gate 1 source binding remains `fb59ab31d5bfa0d5edda61e3c76cc4c84a517e96c11597848d2780640cf75f3c` after updating the continuity record for the approved source metadata.
- Local Windows export regenerated all 32 approved source proofs and matched the reviewed derivative manifest. The CI proof job now exports this brand with the existing approved identity before Linux aggregate validation. Final build and site evidence follows below.
- The first approved build exposed a verifier logic error: supplied lockup and wordmark variants were included in its verified-source set, but the final condition required that set to equal only `full` and `reduced`. The condition now requires both canonical mark roles to be present; a direct verifier rerun reported zero problems. A fresh complete build is in progress to confirm the shipped verifier copy.

## 2026-09-29: final build and cross-brand checks

- The fresh DanceWithMe865 build reported zero `verify.py` problems and zero `validate_glyph.py` failures. Image QC and PDF QC reported zero problems. The logo sheet, desktop and 390 px guideline screenshot, and PDF contact sheet were opened for visual review.
- Full contract checks found two source bookkeeping omissions: `dancewithme865` was absent from the continuity audit inventory, and its canon version was implicit. Both are now explicit. Updating `brand.json` changed its source metadata hash, while the approved canonical artwork binding remained unchanged.
- Local regression checks need the reviewed Node runtime for each previously approved identity. The I Heart PR Tours approval is bound to Node 24.11.0; DanceWithMe865 is bound to Node 26.5.0. The CI Windows proof job exports each under its approved runtime. The Linux build uses both exports for its cross-runtime comparison.
- Fixed specimen numeric serialization only where legacy six-digit formatting would exceed the verifier's placement tolerance. Existing rounded values remain byte-identical, and the DanceWithMe865 specimen retains its measured source placement.

## 2026-09-29: standard delivery verification

- The final aggregate build generated nine kits and reported zero `verify.py` problems and zero `validate_glyph.py` failures. The DanceWithMe865 logo sheet, 390 px and desktop guidelines page, and PDF contact sheet were opened for visual review.
- Site lint and static export passed with nine prepared kits. The complete site browser suite verified 103 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The DanceWithMe865 overview and assets are present under the existing site route structure with an independent-client ownership notice.
- The public registry inventory validated nine catalogs and local font bundles. The prepared public documentation audit reported zero problems. The publication audit passed with nine kits, nine site markers, nine packages, and 2,161 copied public files. For this local audit only, two ignored private review kits were temporarily moved out of `dist/` and restored afterward; CI starts from a clean `dist/` tree.
- Release candidate metadata verification passed for the current `2.7.0` source version with nine generated release assets and notes. S065 is tracked by [issue #303](https://github.com/shruggietech/shruggie-brand/issues/303).
- The full Python contract suite passed all 26 checks when rerun with CI's environment scope. The first local wrapper run had applied `GP_APPROVED_PROOF_ROOT` to synthetic continuity tests outside that scope; the corrected run supersedes it. The clean registry consumer installed 24 UI items through the pinned shadcn CLI and built with local font bundles.
- The pinned WordPress runtime checks passed on 6.9.9/PHP 8.2 and 7.1.2/PHP 8.3, including ZIP install, native patterns, update and rollback, non-root URL composition, live asset fetch, and WCAG checks. `npm audit` found zero vulnerabilities. The agent contract sync made no change; the local capability probe reported full tier.
- Final source checks found zero UTF-8, BOM, CRLF, replacement-character, or likely mojibake problems across 52 changed text files. `git diff --check` and the Markdown prose check passed. `git ls-files dist` returned no tracked generated files. GitHub CI remains to run on the PR commit.

## 2026-09-29: consolidated PR review and proof replay

- S065's approved source commit is an ancestor of the consolidated S066 PR #304. A source-tree comparison found no changes to `brands/dancewithme865/assets/source/`. Superseded PR #305 was closed with its branch retained after both first-round Codex threads were answered and resolved.
- The combined generator rejects supplied black or white wordmarks when `single_ink.wordmark_input_id` would derive the same output path. Regressions cover both collisions. The verified CI artifact lists all eleven production kits, including DanceWithMe865 and Scruggs.
- The combined branch re-exported all 32 exact approved DanceWithMe865 proofs under Node 26.5.0, and the client kit build reported zero verifier problems and zero glyph failures. The logo sheet and PDF contact sheet were opened for visual inspection. The GitHub approved-identity-proofs job passed on the first consolidated push. The local nine-brand Node 24 build also reported zero problems; final CI remains pending.
- The complete local pipeline suite passed 97 tests. The first consolidated GitHub run found that the Python 3.8 job had no pinned SVG renderer installed; this CI setup was corrected and pushed for a fresh run.
