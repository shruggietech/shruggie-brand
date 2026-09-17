# Verification Evidence: Interface Contract Foundation

**Branch**: `codex/037-interface-contract-foundation`

**Baseline**: `main` and `origin/main` at `d4665c72b91c7966d87d336352742f0cfb99fba5` on 2026-09-17. S035 remains a separate unmerged branch.

**Versions**: Brand Canon `1.2.1`, Interface Canon `1.0.0`, BrandBuilder compiler `1.2.1`, and the existing per-brand source versions remain independently reported. This slice does not declare a release.

**Production inventory**: `covarity`, `cueson`, `eso-weave`, `fragcap`, `glitchpad`, `go-schedule`, `i-heart-pr-tours`, and `shruggietech`. Seven are release-certified locally. I Heart PR Tours retains its exact Node `24.11.0` approved-proof boundary and is rebuilt by CI on that canonical host.

**Slice issue**: [#223](https://github.com/shruggietech/shruggie-brand/issues/223), `[SLICE] S037: Establish the Interface Canon and consumer contract foundation`.

## Scope traceability

| Issue | S037 outcome | Evidence status |
| --- | --- | --- |
| #210 | Renderer-neutral Interface Canon, thirteen runtime capability inputs, logical-unit transforms, compatibility defaults, bounded overrides, accessibility pairs, source schema, and fail-closed validation | Complete in `skill/references/interface-canon.json`, `skill/references/interface-canon.schema.json`, and `skill/templates/interface_contract.py`; every production source resolves without identity mutation |
| #211 | Contextual Author, Implementation, and Audit routing synchronized across metadata-aware and ambient host surfaces with behavioral fixtures | Complete in `skill/references/operating-modes.md`, `skill/references/routing-fixtures.json`, `skill/SKILL.md`, and generated `skill/AGENTS.md`; all routing fixtures pass |
| #212 | Generated consumer manifest, governed block, exact offline recovery, deterministic merge, checksummed provenance, verification, release certification, and capability-gap record | Complete in `skill/templates/interface_contract.py`, `skill/templates/gen_enforcement.py`, `skill/templates/verify.py`, and `scripts/release_contract.py`; deterministic generation, mutation, archive, and offline recovery tests pass |

The implementation intentionally stops before #214 and later recipe, adapter, conformance-host, version-policy, consumer-adoption, and documentation-restructuring issues.

## Authority inventory

- Brand authority remains `skill/references/01-canon.json` plus each `brands/*/brand.json` source contract. The Interface Canon consumes those values and cannot reinterpret identity, artwork, affiliation, inheritance, or provenance.
- Skill and compiler versions remain authoritative in `skill/SKILL.md`; `skill/templates/sync_agents_md.py` projects the portable body into `skill/AGENTS.md`.
- Generated consumer authority originates in `skill/templates/gen_enforcement.py` and is checked by `skill/templates/verify.py`, the final kit manifest in `skill/templates/build_kit.py`, and release archive certification in `scripts/release_contract.py`.
- Generated kits under `dist/`, release archives under `release/`, site exports, and machine-local `.specify/feature.json` remain ignored. No generated artifact is part of the S037 commit.

## Test-first record

The focused Interface Canon, routing, consumer contract, and release archive assertions were added before their implementation. The first focused run failed at import because `interface_contract.py` did not exist, while the archive fixtures failed because no consumer contract or bundled exact distribution existed. Those expected failures established the missing behavior before source changes.

The initial Core-only icon regression also exposed an eager `coloraide` import in the new contract path. The implementation was corrected to import color measurement only during interface resolution, and the complete 17-test icon matrix now passes without importing optional raster or color dependencies during Core vector generation.

## Focused verification

- `python skill/templates/test_interface_contract.py`: 10 tests passed, including canonical shape, schema integrity, every production source, negative alias/role/target/cycle/compatibility/override/affiliation/accessibility cases, three mixed runtime profiles, operating-system-key rejection, all routing fixtures, host synchronization, deterministic merge, malformed markers, provenance mutations, and exact offline recovery.
- Independent JSON Schema validation with `jsonschema` passed for `interface-canon.json` and a freshly generated `consumer-contract.json`. The focused suite also walks both published schemas to ensure every closed required object defines its required properties.
- `python skill/templates/test_iconkit.py`: 17 tests passed, including the Core-only optional-dependency boundary.
- `python scripts/test_package_release.py`: 6 tests passed, including deterministic archive output, consumer handoff coverage, corrupt recovery rejection, and destination preservation on failure.
- `python scripts/test_release_contract.py`: 16 tests passed, including required consumer files, recorded manifest coverage, exact recovery integrity, coordinated recovery-version drift rejection, deterministic source/version behavior, and release-boundary rejection cases.
- `python skill/templates/test_pipeline.py`: 68 tests ran; 67 passed and the sole local error was the deliberate I Heart PR Tours renderer lock rejecting Node `26.5.0` in `test_i_heart_pr_tours_generation_preserves_exact_sources_and_approved_derivations`. The workflow installs Node `24.11.0` and exports that proof before the verified build, so CI is the authoritative result for this test.

## Complete local verification

- `python -m compileall -q skill scripts`: passed.
- `python skill/templates/test_glyphkit.py`: 34 checks, 0 failures.
- `python scripts/test_publication_workflow.py`: 17 tests passed.
- `python scripts/test_prepare_site.py`: 31 tests passed.
- `python scripts/test_identity_continuity_audit.py`: 4 tests passed.
- `python skill/templates/test_brand_contract.py`: 53 tests passed.
- `python skill/templates/test_identity_continuity.py`: 22 tests passed.
- `python scripts/check_markdown.py`: passed.
- `python scripts/build_all.py covarity cueson eso-weave fragcap glitchpad go-schedule shruggietech`: seven kits built cleanly. Every build reported zero verifier problems, zero glyph failures, zero image and PDF QC problems, and zero pagination splits.
- Fourteen final QC sheets were opened and inspected: the logo sheet and responsive guidelines sheet for each locally certified brand. No clipping, overlap, identity drift, unreadable mark, or mobile layout regression was observed.
- `python scripts/package_release.py` followed by generated notes and `release_contract.py verify`: nine deterministic release assets verified, including seven brand archives and both BrandBuilder distributions.
- `python skill/templates/sync_agents_md.py skill`: `skill/AGENTS.md` was unchanged after regeneration (20,831 bytes, portable body SHA-256 prefix `66c733af30e2`).
- The site payload and production-origin unit phase passed 12 tests. Fresh site preparation then failed closed on the intentionally stale local I Heart PR Tours kit because it lacks the new S037 contract and cannot be canonically regenerated on Node `26.5.0`; site export, full site verification, and publication audit therefore remain CI-authoritative on Node `24.11.0` with the approved proof artifact.

## Determinism, portability, and hygiene

- Repeated consumer generation produced byte-identical governed outputs and recovery archives. The verifier rejects altered provenance bytes, altered recovery bytes, unsafe paths, malformed markers, missing governed entry points, version drift, and unauthorized gap submission.
- Human text before and after a valid governed block is preserved exactly, including trailing blank lines. Missing blocks append deterministically; duplicate, missing-half, or reversed markers fail closed.
- The recovery archive contains exact `SKILL.md`, `AGENTS.md`, and Interface Canon authority, is selected before any network source, and is bound to the generated contract by SHA-256 and semantic versions.
- Final changed-file scan covered 38 source/specification files: zero UTF-8 BOMs, zero CRLF files, zero mojibake matches, and zero `git diff --check` findings.
- `.specify/feature.json`, representative `dist/`, `release/`, and `site/out/` paths are ignored. Final status contains only intended source, workflow, documentation, test, and S037 specification changes.

## Cross-artifact analysis

The final pass reconciled issue scope, specification requirements and success criteria, clarification decisions, plan scale, data model, three contracts, quickstart, task ordering, schemas, generator outputs, verification, release certification, and evidence. One medium consistency defect was found and corrected before publication: the plan described twelve runtime inputs while the implemented and specified contract contains thirteen. No CRITICAL or HIGH finding remains.

## CI and review rounds

Official pull request: [#224](https://github.com/shruggietech/shruggie-brand/pull/224), published from commit `52eed68` and configured to close slice issue #223 plus implementation issues #210, #211, and #212.

CI, review comments, reactions, thread resolution, and the single authorized second Codex review request remain in publication autopilot.
