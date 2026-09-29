# S067 verification evidence

## Source and contract checks

| Check | Result |
| --- | --- |
| `python -m unittest test_interface_contract test_documentation_contract test_component_contract test_web_react_adapter test_registry_contract test_messaging test_brand_contract` in `skill/templates` | 136 tests passed |
| `python skill/templates/test_glyphkit.py` | 34 checks, zero failures |
| `python scripts/test_prepare_site.py` | 40 tests passed |
| `python scripts/check_markdown.py` | Passed |
| `git diff --check` | Passed |
| `python skill/templates/probe.py` | Full local capability tier; Chromium and ImageMagick available; `pdffonts` unavailable |
| `python skill/templates/test_pipeline.py` | 96 of 97 passed initially; one Covarity fixture PDF overflow after voice copy was added |
| `python skill/templates/test_pipeline.py PipelineTests.test_third_party_fixed_font_pipeline_is_offline_and_ownership_safe` | Passed after limiting added voice content to name pages without a story or written-form block |
| `python skill/templates/test_pipeline.py` (final rerun) | 97 tests passed |
| `python scripts/test_identity_continuity_audit.py` | 7 tests passed |
| `python skill/templates/test_identity_continuity.py` | 25 tests passed |
| `python skill/templates/sync_agents_md.py skill` | Generated agent contract unchanged |
| Changed source and specification text | 52 files checked, UTF-8 without BOM, LF, and no detected mojibake |

The first aggregate PDF review found a blank run on ShruggieTech's sparse name page; revised layout passes PDF QC with zero problems. Contact-sheet review also found escaped inline markup on Covarity's name page; the canonical formatting was restored before final builds.

## Production builds and publication

The initial eleven-brand local build completed nine kits cleanly. I Heart PR Tours and Local Companion stopped at identity continuity because cached portable renderer attestations were bound to their prior record digests. Exact approved proofs were regenerated from the S067 source with pinned Node 24.11.0. The two affected kits and Covarity were rebuilt, and all eleven production kits now report zero `verify.py` problems, zero glyph failures, zero PDF QC problems, and zero split elements. All eleven PDF contact sheets were opened and reviewed. Identity snapshots and canonical source bindings were compared before and after the four approved-canonical brand.json continuity hash updates; neither was changed.

`pnpm --dir site lint` prepared eleven kits and eighteen reference documents and passed TypeScript checking. `pnpm --dir site build` produced the static site. `python scripts/check_readme_links.py`, `python scripts/test_registry_delivery.py`, `python scripts/test_registry_delivery.py --site site/out --inventory-only`, and `python scripts/audit_public_documentation.py --prepared` passed. `python scripts/package_release.py --version 2.8.0` and `python scripts/release_contract.py verify --version 2.8.0 --release-dir release --notes release/release-notes.md` passed. Browser site tests and publication audit remain in progress.
