# Verification: Immutable Kit Publication

**Branch**: `codex/043-immutable-kit-publication`

**Local verification date**: 2026-09-21

**Hosted status**: Pull request [#238](https://github.com/shruggietech/shruggie-brand/pull/238) is open. The first Codex review completed on `412acf9` with two actionable release-integrity findings. Both are resolved locally and await verification on the corrective head. No tag or release has been created.

## Contract and regression evidence

- `python skill/templates/test_interface_contract.py`: 16 passed.
- `python skill/templates/test_documentation_contract.py`: 4 passed.
- `python skill/templates/test_conformance.py`: 11 passed.
- `python scripts/test_release_contract.py`: 23 passed.
- `python scripts/test_package_release.py`: 8 passed.
- `python scripts/test_prepare_site.py`: 36 passed.
- `python scripts/test_publication_workflow.py`: 17 passed.
- `python skill/templates/test_pipeline.py` with `GP_NODE` bound to exact Node.js 24.11.0: 68 passed.
- Exact-tag publication state is covered by the interface-contract, release-contract, preparation, and workflow suites. Candidate, wrong-tag, exact-tag, stale-link, and release-only deployment cases fail or pass as specified without creating a real tag.

## Aggregate build and release evidence

- `python scripts/build_all.py` with exact Node.js 24.11.0 completed twice after the final generator correction. Both runs built all eight kits with zero reported problems.
- Every production kit reported zero `verify.py` problems and zero `validate_glyph.py` failures.
- `python scripts/package_release.py --version 2.0.0` produced the canonical BrandBuilder and production-brand assets. A byte-parity defect between delivered and recovery impact records was caught, fixed in the generator, regression-tested, and then repackaged successfully.
- `python scripts/release_contract.py notes --version 2.0.0 --output release/release-notes.md` produced validated notes.
- `python scripts/release_contract.py verify --version 2.0.0 --release-dir release --notes release/release-notes.md` verified nine v2.0.0 candidate release assets and their generated notes.
- Post-review regression verification proves that `SHA256SUMS` covers only the `.skill` and `.zip` assets uploaded to the formal release, and the workflow uploads the checksum manifest itself.
- The publication record now requires an exact, ordered match to the seven release-authorized package identities verified by release metadata and archives. The independent third-party I Heart PR Tours showcase remains on the public site but is not misrepresented as a ShruggieTech release asset.
- A synthetic exact-tag rebuild bound every bundle to the exact committed source revision with publication status `release`, without creating a Git tag or changing remote state.
- `python scripts/release_contract.py publication --version 2.0.0 --record site/generated/publication.json --revision <committed-source-revision> --require-release` verified the exact release publication record.
- `python scripts/release_contract.py verify --version 2.0.0 --release-dir release --notes release/release-notes.md --revision <committed-source-revision> --require-release` verified all nine release assets, notes, bundle states, and source revisions.

## Hosted-site evidence

- `npx --yes pnpm@10.28.2 --dir site lint`: passed using the project-pinned package manager.
- `npx --yes pnpm@10.28.2 --dir site build`: passed, producing 95 static routes.
- `npx --yes pnpm@10.28.2 --dir site test`: 12 Node contract tests passed, followed by production-browser verification of 90 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- The generated publication record is a candidate, names exact v2.0.0 release destinations, contains the source revision, and contains no moving `releases/latest` destination.
- After review remediation, all eight site kits built together with zero reported problems using the approved portable proof artifact and exact Node.js 24.11.0 renderer. The prior corrective head also produced the 95-page export and passed all 90 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.

## Visual and identity evidence

- Reviewed all six generated QC PNGs for each of the eight brands, 48 sheets total. Logo sheets, PDF contact sheets, browser specimens, public guideline pages, product specimens, and generic web specimens showed no new clipping, contrast, responsive-layout, or identity defects.
- `git diff --name-only -- brands assets` returned no paths. No approved logo geometry, authoritative identity source, brand metadata, affiliation, ownership, or shared asset changed.
- Existing brand versions remain unchanged. Canonical package identities add BrandBuilder `2.0.0`, for example `eso-weave-brand-1.0.0-bb2.0.0.zip`.

## Source and artifact integrity

- `git diff --check`: passed.
- Strict byte inspection covered all 47 changed and added source files: valid UTF-8, no BOM, LF-only line endings, and no mojibake markers.
- `git ls-files dist release site/generated site/out` returned no paths. Generated kits, archives, site staging, site exports, PDFs, rasters, registries, and release outputs remain ignored and uncommitted.
- Current source and generated contracts contain no downstream adoption-status or utility-measurement fields. Historical rationale and negative regression assertions are retained where needed.

## GitHub delivery traceability

- Parent program: #209.
- Slice: #222, recorded as `S043`.
- Release/site parity: #233.
- Identity versus implementation guidance: #234.
- Immutable kit identity: #235.
- All five issues are in the `shruggie-brand Delivery` project under the Phase 16 milestone. The program and slice issues are `In progress`; #222, #233, #234, and #235 carry `Slice: S043`.
- Pull request #238 references all five issues. The first bounded Codex review reported that `SHA256SUMS` was declared but not uploaded and that the publication package inventory was not checked against the release-authorized set. Both findings now have fail-closed regression coverage and implementation fixes.
- The second bounded review found that a public showcase outside the formal release set could still claim release checksum coverage and that publication URL validation accepted non-authoritative lookalike hosts. Bundle generation now derives release status from the shared release-authorized brand set, leaving other showcases in candidate state with no external release-checksum claim, and preflight requires exact canonical GitHub release and skill URLs.

## Pending hosted completion

- Push the corrective review commit.
- Wait for every required hosted check to pass on the corrective head.
- Re-run bounded Codex review and resolve any further actionable finding.
- Record the final green run and completed review in this file.
- Do not create a tag or release as part of the pull request.
