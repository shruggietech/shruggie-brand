# S041 Verification Evidence

## Baseline

- Repository started from `main` at `454e7cc` on branch `codex/041-documentation-contract-boundaries`.
- The existing manual had 11 top-level Markdown pages, hard-coded site descriptions and navigation, generated `IMPLEMENTATION.md` prose, and no shared hosted/bundled documentation fact record.
- Documentation-related route kinds were `docs-index`, `docs-page`, `guidelines`, `guidelines-topic`, and `downloads`.
- `python scripts/test_prepare_site.py`: 35 passed.
- `python skill/templates/test_interface_contract.py`: 13 passed.
- `python skill/templates/test_pipeline.py`: 67 passed and 1 pre-existing environment-sensitive error in `test_i_heart_pr_tours_generation_preserves_exact_sources_and_approved_derivations` because the probed production proof renderer disagreed with the fixture record. The following Node command still returned the compound command exit code as zero, so this failure is recorded explicitly rather than masked.
- `node site/tests/site.test.mjs`: passed.
- `.gitignore` covers `dist/`, `site/out/`, generated site data, test results, dependency directories, caches, and machine-local Spec Kit state. No ignore change was required.

## Checkpoints

### Foundational contract

- `python skill/templates/test_documentation_contract.py`: 4 passed, covering schema, exact inventory, topic ownership, navigation uniqueness, route dispositions, fact equality, deterministic Markdown, and negative paths.
- The policy enumerates 15 top-level manual pages, all five documentation-related route kinds, all three authority surfaces, all ten required system topics, and all three overview graphics.

### Main manual

- Added four operational chapters for architecture and ownership, interface implementation, verification and versioning, and agent integration and extension.
- `python scripts/test_prepare_site.py`: 35 passed after navigation became contract-derived.
- `node site/tests/site.test.mjs`: passed with the 16-entry hierarchy including the generated index.

### Hosted and bundled projections

- `python skill/templates/test_interface_contract.py`: 13 passed.
- `python -m unittest skill.templates.test_pipeline.PipelineTests.test_enforcement_emits_deterministic_merge_safe_consumer_contract skill.templates.test_pipeline.PipelineTests.test_portal_payload_covers_every_delivery_once`: 2 passed.
- Generated consumer contracts now declare the documentation policy and exact fact record. Provenance covers the policy, schema, facts, rendered implementation guidance, adapters, recovery, and existing authorities.
- Site staging rejects missing or altered hosted facts and carries the fact record without mutation.

### Migration and accessibility

- Existing `docs-index`, `docs-page`, `guidelines`, `guidelines-topic`, and `downloads` routes remain preserved.
- The documentation index renders three server-side semantic ordered-list overviews with adjacent visible text equivalents and responsive, forced-color, and reduced-motion styling.
- No work from issues #193, #194, or #202 was absorbed.

### Full verification

- `python -m compileall -q scripts skill/templates`: passed.
- The complete documented Python contract suite passed, including 68 pipeline tests. Identity-continuity tests ran without a portable proof override, while I Heart PR Tours generation and the all-brand gate used pinned Node 24.11.0 and the SHA-bound approved proof artifact from successful main run `35295326759`.
- `python scripts/build_all.py`: seven kits passed directly. I Heart PR Tours initially reported the expected local Node 26 renderer mismatch, then passed with pinned Node 24.11.0 and the approved proof artifact. All eight kits completed with zero verifier, glyph, image, PDF, and pagination failures.
- `python scripts/test_package_release.py`: 7 passed. `python scripts/test_release_contract.py`: 20 passed. Release certification now requires canonical documentation policy, schema, facts, and recovery contents.
- Site staging prepared 8 kits and 15 reference documents. TypeScript passed, Next.js generated 95 static pages, Node payload and production-origin tests passed 12 of 12, and the source-level site contract passed.
- The first browser verification run found only stale pagination and no-script expectations, which were updated to the governed 16-page hierarchy. A later rerun encountered one transient iframe navigation context loss during the pre-existing S040 conformance sweep; the final browser result is recorded below.
- `node site/scripts/verify-site.mjs`: verified 90 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The documentation index also passed explicit server-rendered checks for all three overviews, ten ordered steps, and their visible text equivalents.
- `python scripts/audit_publication_artifacts.py --kits dist --site site/out`: confirmed publication markers for all 8 generated kits and all 8 hosted brand surfaces.
- `python -m unittest discover -s scripts -p 'test_*.py'`: 97 passed.
- The documentation, interface, pipeline, and icon-kit suite passed 102 tests under pinned Node 24.11.0 and the SHA-bound approved proof artifact.
- UTF-8, LF, mojibake, generated-output, task-completion, and repository-status checks are recorded in the final hygiene checkpoint before publication.
