# S054 Evidence and Manual Disposition

## Baseline and scope

The branch started from merged S053 `main` at `92e876aacffae23a7b838d3b802abd58372bd4b5`. The v2.2.0 source version is a candidate; no v2.2.0 tag or public release existed at kickoff. The 15-page catalog in `skill/references/documentation-contract.json` is the route authority. Individual brand guideline pages are outside #264's content scope, though the existing publication audit still checks their internal-process language.

## Main-manual page-by-page disposition

| Public route | Source | Disposition and operative cross-check |
| --- | --- | --- |
| `/docs/00-variance-contract/` | `00-variance-contract.md` | Removed obsolete page version, fixed kit-count/development stories, corrected constructed versus authoritative logo source and optional asset delivery. Checked against source-mode verifier and kit manifest behavior. |
| `/docs/02-kit-anatomy/` | `02-kit-anatomy.md` | Replaced migration-era file tree and portfolio counts with current package layers and inventory authority. Checked representative generated kits and source-mode rules; `mk_paths.py` is conditional. |
| `/docs/03-interview/` | `03-interview.md` | No portfolio count or work-slice code. Its broader adaptive-brief redesign is tracked separately by open #266; S054 does not silently close that issue. |
| `/docs/06-logo-protocol/` | `06-logo-protocol.md` | Replaced dated 1.1.0 defect-story heading with current preflight checklist and corrected constructed/authoritative verifier distinction against `08-glyph-construction.md`. |
| `/docs/08-glyph-construction/` | `08-glyph-construction.md` | Current source-mode, legacy-provenance, and approval distinctions remain operative; no portfolio-size claim. |
| `/docs/identity-continuity/` | `identity-continuity.md` | Current source approval and derivative boundaries remain operative; no portfolio-size claim. |
| `/docs/07-voice/` | `07-voice.md` | Voice and rhetorical rules remain current; no portfolio-size claim. |
| `/docs/04-toolchain/` | `04-toolchain.md` | Capability probing and explicit skip behavior remain current; no portfolio-size claim. |
| `/docs/05-shadcn-binding/` | `05-shadcn-binding.md` | Removed false live-site link-color and early palette-history claims. Kept exact registry and local-font guidance consistent with generated adapter output. |
| `/docs/09-portability/` | `09-portability.md` | Core/extended/visual capability boundaries remain current; no portfolio-size claim. |
| `/docs/operating-modes/` | `operating-modes.md` | Retained the narrowly necessary Spec Kit instruction for governed authoring; no portfolio-size claim. |
| `/docs/10-system-architecture/` | `10-system-architecture.md` | Main/hosted/bundled ownership remains aligned with `documentation-contract.json`; no portfolio-size claim. |
| `/docs/11-interface-implementation/` | `11-interface-implementation.md` | Exact version tuple, adapter, and consumer-contract instructions remain current; no portfolio-size claim. |
| `/docs/12-verification-versioning/` | `12-verification-versioning.md` | Independent version domains, candidate/release state, and exact archive naming remain current; no portfolio-size claim. |
| `/docs/13-agent-integration/` | `13-agent-integration.md` | Recovery, version pinning, and local gap-record instructions remain current; no portfolio-size claim. |
| `/docs/` | Generated overview | Now displays candidate or official identity from the same publication authority as every page. |

The audit also scans the catalog's titles/descriptions, generated navigation and route records, prepared MDX, exported HTML, and individual brand sources for previously governed internal-process phrases. Count rules are scoped to the main manual so measured technical and brand-specific facts are not rejected as portfolio totals.

## Verification ledger

| Gate | Result |
| --- | --- |
| `python scripts/test_check_readme_links.py` | PASS, 9 isolated cases; also passed in the 22-suite non-build run. |
| `python scripts/test_public_documentation.py`, `python scripts/audit_public_documentation.py --sources`, and `python scripts/audit_public_documentation.py --prepared` | PASS, 9 isolated cases and zero source/prepared audit problems. |
| `python scripts/test_documentation_publication.py` | PASS, 5 candidate/release and mutation fixtures. |
| `python dist/s053_pinned_node.py python scripts/build_all.py` | PASS, 8 kits with zero verifier, glyph, image, PDF, and pagination problems. The ignored launcher pins Node 24.11.0 and hides console children. |
| `python dist/s053_pinned_node.py python dist/s053_validation.py` and `python dist/s053_pinned_node.py python skill/templates/test_pipeline.py` | PASS, 22 non-build suites and the full pipeline regression. |
| `python scripts/test_registry_delivery.py` and `python scripts/test_registry_delivery.py --site site/out --inventory-only` | PASS, clean consumer installation and eight exported production catalogs. |
| `python scripts/package_release.py --version 2.2.0` and `python scripts/release_contract.py notes --version 2.2.0 --output release/release-notes.md` | PASS, 9 candidate assets and generated notes. |
| `python dist/s053_pinned_node.py pnpm --dir site lint` and `python dist/s053_pinned_node.py pnpm --dir site build` | PASS, MDX generation, TypeScript, and 96 static pages. |
| `python scripts/release_contract.py verify --version 2.2.0 --release-dir release --notes release/release-notes.md` | PASS, 9 candidate assets. |
| `python scripts/release_contract.py documentation --version 2.2.0 --record site/generated/documentation-publication.json --publication site/generated/publication.json --docs site/generated/docs --exported site/out/docs/publication.json --release-dir release --revision 92e876aacffae23a7b838d3b802abd58372bd4b5` | PASS, exact source, prepared page, export, and skill archive binding. |
| `python scripts/audit_publication_artifacts.py --kits dist/s054_audit_kits --site site/out` | PASS, eight markers in a clean staging copy of the production kits and eight in the site export. The local `dist/` root contains unrelated ignored tools from earlier slices, so a root-level audit there is not representative; clean CI will use its fresh `dist/`. |
| `python scripts/check_readme_links.py`, `python scripts/check_markdown.py`, `git diff --check`, `python -m compileall -q scripts` | PASS, zero link, Markdown, whitespace, or compile problems. |
| `python dist/s053_pinned_node.py pnpm --dir site test` | PASS, 12 payload/origin tests and 91 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations. The first run exposed a stale test expectation for a fixed color table intentionally removed from `05-shadcn-binding.md`; the table-route list was corrected and the complete test rerun passed. |
| Changed text encoding and corruption scan | PASS, no UTF-8 BOM, carriage returns, or common mojibake markers in changed text and S054 Spec Kit records. |

## First PR review correction

Codex review on PR #279 identified an empty-alt gap for reference-style Markdown images such as `![][logo]`. The README audit now rejects empty and whitespace-only reference labels, and its isolated image test covers both failures and a descriptive reference label. The affected tests, live README audit, Markdown policy, and diff hygiene checks passed before the correction was pushed.
| Live deployed routes and formal release asset comparison | Pending authorized post-merge v2.2.0 publication. No live pass is claimed in the PR. |
