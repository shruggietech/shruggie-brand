# S067 verification evidence

The results below describe the first PR commit at BrandBuilder 2.8.0. The first Codex review required a source and compiler version change, exact treatment of six Gate 2 approved portfolio descriptions, and a Python 3.8/3.9 PDF extractor fallback. All affected checks are being repeated against the review resolution commit before the final handoff.

## First review resolution

The required `guide` to `guidance` source rename now declares Brand Canon 2.0.0 and BrandBuilder 3.0.0. Each brand has a patch version because its approved identity geometry is unchanged. Four approved-canonical continuity records were refreshed for their new brand.json source digest without changing approved identity snapshots or approval facts, and their exact portable renderer proofs were regenerated. Six Gate 2 approved descriptors now have source-bound `short_description` records for site metadata only; portfolio cards omit descriptions for the other five brands. Public site records omit raw legacy `descriptor` and `idea`. Python 3.8/3.9 validation reports an explicit PDF messaging skip when PyMuPDF is unavailable while still checking portable HTML and portal JSON.

The review-resolution rerun passed `python skill/templates/test_pipeline.py` (97), the combined Python contract suite (136), `python scripts/test_prepare_site.py` (40), identity continuity tests (32), publication workflow tests (27), and glyphkit checks (34). `python scripts/check_markdown.py`, `python scripts/check_readme_links.py`, `git diff --check`, and `python skill/templates/sync_agents_md.py skill` passed. The generated agent contract was unchanged. Forty-two modified text files were checked as UTF-8 without BOM and LF, with no detected mojibake.

All eleven Brand Canon 2.0.0 and BrandBuilder 3.0.0 production kits rebuilt with zero verifier or glyph failures, zero PDF QC problems, and zero pagination splits. Their eleven new PDF contact sheets were opened and reviewed. `pnpm --dir site lint` and `pnpm --dir site build` passed; `pnpm --dir site test` passed twelve Node tests, 242 route and viewport checks, 84 visual checks across two themes, and 121 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The site verifier now checks exact approved descriptions on six portfolios and absent paragraphs on five, including contrast, keyboard, zoom, and mobile behavior.

`python scripts/test_registry_delivery.py`, `python scripts/test_registry_delivery.py --site site/out --inventory-only`, and `python scripts/audit_public_documentation.py --prepared` passed. `python scripts/package_release.py --version 3.0.0` built ten release assets; generated notes and `python scripts/release_contract.py verify --version 3.0.0 --release-dir release --notes release/release-notes.md` passed. `python scripts/audit_publication_artifacts.py --kits dist --site site/out --semantic --release release` passed for eleven brands and 2,616 public files. Unrelated ignored local scratch directories were temporarily parked outside `dist/` for that audit and restored afterward.

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

`pnpm --dir site lint` prepared eleven kits and eighteen reference documents and passed TypeScript checking. `pnpm --dir site build` produced the static site. `pnpm --dir site test` passed twelve Node tests, 242 route and viewport checks, 84 visual route and viewport checks across two themes, and 121 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. `python scripts/check_readme_links.py`, `python scripts/test_registry_delivery.py`, `python scripts/test_registry_delivery.py --site site/out --inventory-only`, and `python scripts/audit_public_documentation.py --prepared` passed. `python scripts/package_release.py --version 2.8.0` and `python scripts/release_contract.py verify --version 2.8.0 --release-dir release --notes release/release-notes.md` passed. `python scripts/audit_publication_artifacts.py --kits dist --site site/out --semantic --release release` passed with eleven brands and 2,616 public files after moving unrelated ignored local scratch directories aside for the audit. Those directories were restored afterward.
