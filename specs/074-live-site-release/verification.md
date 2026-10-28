# S074 Verification

## Baseline

- 2026-10-28: fetched `origin/main` at `31b34611f92996061782c5bbe61ab148a02d63f4`; working tree clean before S074.
- Main Build run `40635751465` completed successfully at that source revision.
- Latest official release before S074: v3.1.0. Pages deployment is gated on a successful version-tag run.
- Before deployment, `https://brand.shruggie.tech/` returned HTTP 200 with v3.1.0 present and the new fragcap sentence absent.

## Focused candidate checks

- `python scripts/release_contract.py current`: 3.1.1.
- `python scripts/test_release_contract.py`: 27/27 passed; `python skill/templates/test_interface_contract.py`: 19/19 passed.
- Identity continuity audit passed after refreshing only the DanceWithMe865 source-file and record hashes; 7 identity audit regressions, 26 identity continuity regressions, and 83 brand contract regressions passed.
- Messaging 12/12, publication workflow 28/28, package release 11/11, documentation publication 5/5, prepared-site 42/42, public documentation 9/9, documentation references 3/3, README links 9/9 passed.
- `python -m compileall -q scripts skill/templates`, `python scripts/check_markdown.py`, public documentation source audit, and WordPress fixture `npm audit --audit-level=moderate` passed (zero vulnerabilities).
- WordPress fixture tests passed 11/11 after removing the command runner's inherited pager variables; the first attempt with `GIT_PAGER` present failed its explicit environment policy.
- Generated v3.1.1 release notes passed metadata validation and state Brand Canon 2.1.0, no required identity migration, exact changed-package repinning, and the existing thirteen-hosted/ten-archive boundary.
- All 26 edited/new text files scanned as UTF-8 without BOM, LF-only, and without known mojibake markers. `git diff --check` passed.
- A registry delivery attempt made while `build_all.py` was still replacing generated kits saw an incomplete ESO Weave registry item. This is an invalid concurrent check; rerun against the completed build is required.
- `python scripts/build_all.py`: all 13 production kits rebuilt with zero reported problems; each kit recorded zero verifier problems, zero glyph failures and zero PDF QC problems.
- The completed `python scripts/test_registry_delivery.py` passed: 13 catalogs and local font bundles, with the pinned shadcn CLI installing 27 UI items into a consumer build. `python scripts/test_brand_essentials_delivery.py` checked 13 portal, portable and PDF openings.
- `python scripts/package_release.py --version 3.1.1` and `python scripts/release_contract.py verify --version 3.1.1 --release-dir release --notes release/release-notes.md`: twelve release assets and generated notes verified. The local package predates the final commit; tagged CI must rebuild and verify the release-source identity.
- `pnpm@10.28.2 --dir site lint` and `build` passed using the repository-pinned pnpm version. The build generated 196 static pages. A first attempt with the command runner's pnpm 11.25.0 stopped at its interactive modules-purge guard, so no source change was made.
- The semantic publication audit passed for 13 brands, 13 kit markers, 13 packages, 13 site markers and 3,094 public files. Prepared public documentation and README link audits reported zero problems; the site registry inventory passed.
- The local static home contains the four approved descriptions for fragcap, Glitchpad, go-schedule and ShruggieTech, plus the portfolio introduction.
- WordPress 6.9.9/PHP 8.2 and WordPress 7.1.2/PHP 8.3 passed ZIP install, native patterns, update/rollback, non-root URL composition and live asset fetch.
- `pnpm@10.28.2 --dir site test` passed all 12 Node contract tests, 278 route/viewport checks, 99 visual route/viewport cases across both themes, and 139 HTML routes at desktop/mobile widths with zero WCAG 2.1 AA violations. The exported desktop homepage screenshot was inspected: portfolio text is beneath its heading, DanceWithMe865 has title clearance, and the approved descriptions appear on cards.
- Final source check: `git diff --check`, Markdown prose policy, and a UTF-8 without BOM/LF/mojibake scan of 26 edited/new text files passed. Only intended source and `specs/074-live-site-release/` appear in `git status --short`.

## 2026-10-28: Review, release and live publication

- Release preparation [PR #339](https://github.com/shruggietech/shruggie-brand/pull/339) was reviewed at head `2a2a9c0b16f34fa193547cb73a6c57b2911cdad6`. Codex code review found no issues. One additional requested Codex security review found no issues. No review threads or actionable comments remained. The [exact-head PR run](https://github.com/shruggietech/shruggie-brand/actions/runs/40769221504) passed every applicable job.
- PR #339 was squash merged into main at `65af667461798738b0cf381b7c8bc4487afd853a`. The reviewed head and merged commit have the same source tree, `798ea82e0b084df5c4bd926412c1dc83efd651d1`. The [post-merge main run](https://github.com/shruggietech/shruggie-brand/actions/runs/40775802048) passed every applicable job.
- Annotated tag `v3.1.1` (tag object `acd791920a245ca307d80b175db525bbd02a52bb`) points to the merged main commit. The [tag workflow](https://github.com/shruggietech/shruggie-brand/actions/runs/40775877208) passed all eight jobs, including full build, release preflight, official release publication and exact-artifact Pages deployment.
- The [official v3.1.1 release](https://github.com/shruggietech/shruggie-brand/releases/tag/v3.1.1) is public, non-prerelease and latest, with thirteen assets. All thirteen downloaded assets match their GitHub SHA-256 metadata. The twelve distribution assets match the downloaded `SHA256SUMS`; the exact-release contract verifies those twelve archives and generated release notes against the tagged source revision. No locally assembled artifact was uploaded.
- Public `https://brand.shruggie.tech/docs/publication.json` reports release status, v3.1.1 and the exact tagged revision. The public home has thirteen cards, nests the portfolio description beneath its heading, and contains the exact approved fragcap, Glitchpad, go-schedule and ShruggieTech sentences. Their four formal brand-essentials guides contain the same sentences. The public References page has all 68 labeled entries and released v3.1.1 language.
- All ten public brand archive downloads match their corresponding official release ZIPs byte-for-byte. A headless live browser campaign passed 24 checks across six routes, two viewport widths and both supported themes, with zero WCAG 2.1 AA violations and zero failed site assets. Desktop and mobile home screenshots were inspected: portfolio text is beneath the heading and the DanceWithMe865 title has visible card-edge clearance. The browser checks used the mobile accordion and desktop cards on their respective layouts.
- The temporary live HTTP/browser verifiers, downloaded assets and screenshots are ignored under `dist/private/s074-publication/`; released source and `dist/` remain out of the closeout commit.
