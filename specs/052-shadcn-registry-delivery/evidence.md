# S052 Verification Evidence

## Scope and traceability

S052 implements issue #263. FR-001 to FR-005 map to generator, schema, and site projection checks. FR-006 maps to a pinned shadcn CLI install and clean Next.js consumer build. FR-007 maps to the generated README, skill, PDF, hosted downloads, and contribution guide. FR-008 maps to the production and publication gates below. FR-009 keeps issue #269's broader artifact audit and later release work separate.

## Local verification, 2026-09-25

- The official shadcn catalog and item schemas were pinned locally with upstream MIT license provenance. The contract suite passed 10 cases, including valid fileless themes and rejection of missing/empty UI content, duplicate or unsafe targets, broken dependencies, mismatched catalog and direct payloads, undeclared endpoints, and unsupported local-font items.
- `scripts/build_all.py` built all eight production kits with zero reported verifier problems. The glyph and PDF QC gates passed. The I Heart PR Tours identity proof matched its approved Node 24.11.0 renderer; an initial local run under Node 26 failed that environment-bound proof, so the final build and pipeline suite used Node 24.11.0 and the approved proof tree.
- `skill/templates/test_pipeline.py` passed 75 tests. The documented standalone Python contract, publication, identity, adapter, documentation, glyph, and registry test scripts passed. `scripts/check_markdown.py` passed.
- `scripts/test_registry_delivery.py` validated all eight generated catalogs and local face paths. The pinned `shadcn@4.21.0` CLI discovered the catalog and installed the theme plus all 24 UI items into a temporary clean consumer. TypeScript checked the installed components, and Next.js built a rendered representative row using bundled local fonts.
- `pnpm --dir site lint` and `pnpm --dir site build` passed with pinned pnpm 10.28.2 and Node 24.11.0. The static export contains 96 pages. `scripts/check_readme_links.py` and `scripts/audit_public_documentation.py --prepared` reported zero problems.
- `pnpm --dir site test` verified 91 HTML routes at desktop and mobile widths with zero WCAG 2.1 AA violations.
- The exported registry inventory exactly matched all generated kit JSON files. `scripts/audit_publication_artifacts.py` passed with eight kit markers and eight hosted markers when run against a clean copy of the production kits; the local `dist/` directory also held test tooling and proof fixtures that are absent from CI's clean artifact root.
- `scripts/package_release.py --version 2.0.3` generated nine local candidate assets; release notes and `release_contract.py verify` passed. These outputs remain ignored and are not part of the PR.
- Changed text files decoded as UTF-8, had no BOM or CRLF, and `git diff --check` passed. No source logo geometry changed.

## External and later checks

- [PR #275](https://github.com/shruggietech/shruggie-brand/pull/275) opened from commit `ce4585a`. The first Codex review found that the standalone capability probe did not require `jsonschema` even though the registry generator imports it. The follow-up blocks an unusable Core tier, stops `build_kit.py` before generation on probe failure, corrects portable guidance, and adds two negative tests. Required CI and final review disposition remain pending.
- Public HTTPS endpoint and release behavior: pending an authorized merge and deployment. No tag, release, or issue closure is claimed by this PR.

## Post-merge release preparation

The owner authorized a formal public release on 2026-09-25. PR #275 is merged as `1d9602be0b1cdb17b4a74ae1387566c51b608035`. Release preparation selects BrandBuilder 2.1.0, Brand Canon 1.4.0, and I Heart PR Tours 1.1.0 under the declared version policy. The S052 source fix remains the basis for issue #263. Final tagged CI, release assets, public site deployment, live endpoint inventory, and remote consumer installation are recorded in the issue after publication; this preparation does not claim those checks have passed.
