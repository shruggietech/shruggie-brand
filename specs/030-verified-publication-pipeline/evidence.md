# Verification Evidence: Verified Publication Pipeline

## 2026-09-11 - Incident and planning baseline

- Issue: [#196](https://github.com/shruggietech/shruggie-brand/issues/196)
- Branch: `codex/030-verified-publication-pipeline`
- Failed Pages run: `34633145579` at revision `920b95c`, rejected because the Pages-only rebuild selected native `rsvg-convert` and Node 24.20.0 instead of the approved `node-resvg` and Node 24.11.0 contract.
- Passing Build run: `34633145470` at the same revision, using the approved Windows proof export and portable comparison path.
- Last production deployment: `6382937945` at revision `6c858676396c1963ea2ea0403298aa1a830e13c0`.
- Active ruleset: `22231594`, strict required status context `build`, with no bypass.
- Identity impact: none authorized. The continuity gate behaved correctly and no proof hash, approval record, tolerance, identity source, or geometry value will change.
- Specification analysis: 16 of 16 functional requirements and all buildable success criteria map to tasks. One priority-label inconsistency in `tasks.md` was corrected before implementation. No constitutional conflict remains.
- Checklist gate: `requirements.md` 16/16 and `publication.md` 18/18.

## 2026-09-11 - Local implementation evidence

- Test-first baseline: `scripts/test_publication_workflow.py` initially stopped on the absent auditor, then reported nine expected workflow-contract failures against the old Build, Pages, and Release topology after the auditor was added.
- Focused green result: 17 publication and artifact-boundary tests plus 15 release-contract tests passed.
- Mutation coverage: symbolic links, hard links, paths outside the repository, unexpected hidden paths, and missing or extra governed icon manifests all fail closed.
- Workflow syntax: `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.7` passed after protecting the checksum glob from option-like filenames.
- Generator regression matrix: glyphkit 34 checks, package-release 5 tests, site preparation 30 tests, brand contract 53 tests, identity continuity 22 tests, iconkit 17 tests, pipeline 58 tests, identity-continuity audit 4 tests, and Markdown policy all passed. Documented capability skips and warnings remained explicit and unchanged.
- Production build: all eight kits rebuilt with zero reported problems; every final `verify.py` and glyph gate reported zero failures.
- Static site: TypeScript passed, 81 pages exported, 11 payload/origin tests passed, and 76 HTML routes passed desktop and mobile browser verification with zero WCAG 2.1 AA violations.
- Artifact audit: exactly eight kit markers and eight Pages markers were accepted, with no symbolic link, hard link, or unexpected hidden path. Two pre-existing ignored study folders were moved to a named temporary directory for this audit and restored unchanged afterward.
- Release dry-run: nine v1.2.1 assets and generated notes passed `release_contract.py verify`; no tag or release was created.
- Ruleset recheck: active ruleset `22231594` still requires exact context `build`, uses strict status checks, and has no bypass actors.
- Identity impact: `git status` contains no brand, approval, proof-hash, tolerance, or geometry source change.
- Final Spec Kit analysis: zero remaining consistency, ambiguity, coverage, or constitution findings across `spec.md`, `plan.md`, and `tasks.md`.

## 2026-09-11 - Hosted pull request evidence

- Official pull request: [#197](https://github.com/shruggietech/shruggie-brand/pull/197).
- First Codex review on `df8e4ab`: one actionable P1 finding. The checkout-free release publisher lacked an explicit repository selector for `gh release create`.
- Resolution on `9feae99`: added trusted `GH_REPO: ${{ github.repository }}` publisher environment binding and a source-contract regression, replied on the exact inline thread, and resolved it.
- Second and final Codex round on `9feae99`: completed with no major issues and a thumbs-up reaction. No third round was requested.
- Corrected-head CI: run `34651915401` passed Windows approved proofs in 1m45s, Python 3.8 compatibility in 5m24s, authoritative `verified-build` in 23m37s, and the exact required `build` context in 4s.
- Pull-request publication behavior: `deploy-pages`, `release-preflight`, and `publish-release` were all skipped as required.
- Artifact lineage: run SHA `e49c96d11b5ddab0fe907d90ae6744fdb2987013` produced `approved-identity-proofs-e49c96d11b5ddab0fe907d90ae6744fdb2987013`, `verified-brand-kits-e49c96d11b5ddab0fe907d90ae6744fdb2987013`, `github-pages-e49c96d11b5ddab0fe907d90ae6744fdb2987013`, and `verified-release-assets-e49c96d11b5ddab0fe907d90ae6744fdb2987013`. This is GitHub's tested pull-request merge revision for source head `9feae99134c656faa5424cbeabcda79b6ba5aca4`.
- Review closure: zero unresolved review threads; pull request state `CLEAN` and `MERGEABLE`.
- Security-review observation: no separate security-bot comment or check was emitted during the completed review window. The external Codex integration completed its final round with no further security or code finding and left the documented thumbs-up reaction.

## Post-merge owner verification

Pending by design. The owner merge ritual must occur before the production Pages revision can advance.
