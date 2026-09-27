# Verification: S060 Generated Artifact Semantics

## Classified findings and resolution

| Finding | Classification | Resolution |
|---|---|---|
| A portable kit manifest with an empty `files` list passed the generic verifier. | Reproducible required-inventory defect | `verify.py` now requires a populated, unique, root-contained inventory with byte, size, version, identity, and deliverable checks. Negative and valid-absence fixtures cover the rule. |
| A generated kit could be correct while a copied registry endpoint, download, conformance fixture, site projection, or staged archive drifted. | Cross-surface publication integrity gap | Semantic audit compares the exact kit and public tree, release files, staged records, SHA256SUMS, and source revision before upload. |
| Archive packaging adds three canonical license files after the kit manifest is generated. | First-round Codex review finding | The bundled verifier exempts those three package-level files from inventory closure; the release archive contract still validates their presence and canonical bytes. An extracted release archive passes the manifest gate. |
| The independently owned I Heart PR Tours archive is hosted without being a formal release asset. | First-round Codex review finding | Audit regenerates its deterministic archive from the certified kit in temporary storage and compares exact hosted bytes. A changed hosted archive fails a regression test. |
| Registry rows marked `capability-gap`, conditional approved custom assets, and human-only conformance baselines can be legitimately absent. | Declared optional or unsupported state | Matrix records the state; audit requires every advertised artifact while retaining valid absence. |
| Reader-facing guideline content in #270 needs separate design and copy work. | Follow-up outside S060 | #270 remains open; this slice checks that generated guideline facts agree with the kit authority. |

## Local verification on 2026-09-27

| Layer | Evidence |
|---|---|
| Source and schema | Spec Kit prerequisites and analysis passed. Coverage matrix classifies artifact families and their producer, consumer, schema/version, population, publication, and use test. `git diff --check`, Markdown check, public documentation source/prepared audits, and README links passed. |
| Negative semantic regressions | `scripts/test_publication_workflow.py`: 25 tests passed, including missing/changed public files, mismatched facts/version, bad checksum, unsafe optional reference, wrong staged source commit, and changed hosted non-release archive. `skill/templates/test_pipeline.py`: 90 tests passed before the review repair; its changed manifest case passed again after the canonical license exemption. |
| Kit and glyph candidate | Full-tier `scripts/build_all.py` built eight production kits with `BUILD CLEAN`, zero verifier problems, and zero glyph failures. |
| Archive and candidate | `package_release.py --version 2.6.0` produced nine local candidate assets; `release_contract.py verify` certified all nine with generated notes. Exact staged publication audit passed after the review repair: 8 brands, 8 kit markers, 8 packages, 1,914 public files, 8 site markers. The candidate revision matched the pre-commit local source revision; CI repeats it on the PR commit. An extracted Covarity release archive passed `c_manifest` with all three packaging licenses. |
| Consumer and accessibility | Site lint, build, and 12 Node tests passed. Browser validation checked 92 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. Registry delivery inventory passed for eight catalogs, and pinned shadcn CLI installation and local-font consumer build passed. |

Generated kits, site exports, release archives, and the staged candidate remain ignored local outputs. The local candidate is a validation build, not a formal public release. PR CI will rebuild and recheck from the final commit. Third-party reviews and required PR checks remain pending until the PR is opened.
