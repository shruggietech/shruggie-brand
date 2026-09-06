# Evidence: S013 v1.2.1 Release and Production Certification

## Baseline

- Synchronized main revision: `17e685764c19a21e648d366250421fa2a5060860`
- Included S012 merge: PR #134 at `38bf264f1ffdbad0481795c3a7254d1f5bf095a0`
- Included Dependabot merge: PR #113 at `17e685764c19a21e648d366250421fa2a5060860`
- Dependabot alert GHSA-2qfp-q593-8484: fixed
- Baseline release: v1.2.0
- Initial v1.2.1 local tag, remote tag, and GitHub release: absent
- Tracking issue: [#140](https://github.com/shruggietech/shruggie-brand/issues/140)
- Milestone: [Phase 14](https://github.com/shruggietech/shruggie-brand/milestone/24)

## Specification convergence

- Specification checklist: PASS
- Clarifications required: none
- Constitution pre-design and post-design checks: PASS
- Cross-artifact analysis: PASS. All 21 functional requirements map to one or more of 26 tasks, all three user stories have independent tests, terminology and ordering are consistent, and there are zero critical, high, medium, or low findings.

## Candidate verification

- Regression-first proof: v1.2.1 tests failed on the absent changelog and metadata state, then 14 packaging and release-contract tests passed after implementation.
- Current release discovery: `1.2.1`
- Python source gates: 116 tests and geometry checks passed across glyph construction, packaging, release metadata, site preparation, brand contracts, application icons, and pipeline behavior.
- Production build: five kits, zero reported problems, zero glyph failures, zero image-QC problems, zero PDF-QC problems, and zero pagination failures at the full local capability tier.
- Candidate archive contract: exactly seven v1.2.1 assets plus generated notes passed metadata, licensing, archive-safety, PDF, manifest, and checksum verification.
- Generated agent synchronization: unchanged.
- Site type check: passed.
- Local static export: 26 pages generated with the repository's documented webpack fallback because the Windows host denied Turbopack's pooled child-process launch.
- Site browser contract: 11 origin and payload tests passed; 26 HTML routes passed at 360px and 1280px with zero WCAG 2.1 AA violations.
- Visual inspection: all 12 brand-site screenshots and the generated guide, logo, and source-UI sheets were inspected. The four non-ShruggieTech source-UI pages and all guides and logo sheets rendered correctly. The ShruggieTech source-UI sheet remained blank only because its unchanged CDN-hosted React runtime was denied by the local sandbox; the hosted full-tier build remains the authoritative rendering check for that unchanged fixture.

## Pull request and review

- Initial candidate commit: `26df279`
- Pending branch publication and automatic review.

## Public release

- Pending verified-main tag and GitHub Actions publication.

## Production deployment

- Pending Pages and production-origin verification.

## Repository gates

- Markdown prose policy: passed.
- Git diff whitespace check: passed.
- UTF-8 without BOM and LF-only scan: 24 changed and new text files passed.
- Mojibake, em-dash, private-path, and provider-identifier scans: passed.
- Generated output and dependency directories: ignored and absent from the change set.
