# Evidence: S011 v1.2.0 Publication and Production Certification

## Baseline

- Owner-merged main revision: `39b65b5daf9ea74c317132d26347566a9e4959d5`
- S010 pull request: [#127](https://github.com/shruggietech/shruggie-brand/pull/127)
- Merged-main Build workflow: [run 33990452781](https://github.com/shruggietech/shruggie-brand/actions/runs/33990452781), successful
- Merged-main Pages workflow: [run 33990452789](https://github.com/shruggietech/shruggie-brand/actions/runs/33990452789), successful
- Parent: [#116](https://github.com/shruggietech/shruggie-brand/issues/116)
- Publication: [#118](https://github.com/shruggietech/shruggie-brand/issues/118)
- Production: [#119](https://github.com/shruggietech/shruggie-brand/issues/119)
- S011 tracking: [#129](https://github.com/shruggietech/shruggie-brand/issues/129)
- Initial v1.2.0 tag and release state: absent

## Specification convergence

- Specification checklist: PASS
- Clarifications required: none
- Constitution pre-design and post-design checks: PASS
- Cross-artifact analysis: PASS. Every functional requirement maps to at least one task, all user stories have independent tests, task ordering respects publication and review gates, terminology is consistent, and the visual matrix was corrected to eight screenshots.

## Candidate revalidation

- Reviewed S010 head: `4e8a75f0f152ca09ed3fef682947f3af6840e97b`
- Owner-merged main: `39b65b5daf9ea74c317132d26347566a9e4959d5`
- Tree for both revisions: `8eeb12a546336083167dfc8f23396a8d56482f22`, exact match
- Current release discovery: `1.2.0`
- Local Python tests: 31 passed
- Local production build: five kits, zero reported problems, zero glyph failures, and zero `verify.py` problems. The local host ran at the supported core capability tier because no native SVG rasterizer was installed, so it did not substitute for full release packaging.
- Authoritative full candidate gate: [Build run 33990452781](https://github.com/shruggietech/shruggie-brand/actions/runs/33990452781), successful on exact merged main. Its jobs passed Python 3.8 compatibility, full native-renderer kit generation, release metadata and archive certification, generated agent synchronization, type checking, static export, browser checks, and WCAG verification.
- Generated agent synchronization: unchanged
- Markdown policy: passed

## Public release

- Annotated tag: `v1.2.0`, resolving to exact merged main `39b65b5daf9ea74c317132d26347566a9e4959d5`
- Tag conflict guard: no prior local tag, remote tag, or GitHub release existed
- Release workflow: [run 34001058553](https://github.com/shruggietech/shruggie-brand/actions/runs/34001058553), successful
- Public release: [shruggie-brandbuilder 1.2.0](https://github.com/shruggietech/shruggie-brand/releases/tag/v1.2.0), non-draft and non-prerelease
- Public inventory: exactly seven expected assets, two skill distributions and five production-kit archives
- Fresh public download contract: seven of seven assets and generated notes verified with zero failures
- Public notes comparison: exact after line-ending normalization, SHA-256 `5f5c52eb0619b6fa8a0e143e1452a6798b2794d74f3b89466a93022f84f8cc45`
- Issue evidence: [#118 comment](https://github.com/shruggietech/shruggie-brand/issues/118#issuecomment-5555803920)

## Production deployment

- Pages workflow: [run 33990452789](https://github.com/shruggietech/shruggie-brand/actions/runs/33990452789), successful for exact merged main `39b65b5daf9ea74c317132d26347566a9e4959d5`
- Pages configuration: workflow-based, public custom domain `brand.shruggie.tech`, enforced HTTPS, approved certificate
- Origin guard: seven regression tests passed for local fallback, exact HTTPS production selection, malformed origin rejection, host restriction, and safe canonical redirects
- Local site contract: 26 HTML routes at 360px and 1280px, zero WCAG 2.1 AA violations, zero failures
- Production site contract: 26 HTML routes at 360px and 1280px, zero WCAG 2.1 AA violations, zero failures
- Production redirect observation: GitHub Pages returns permanent HTTP 301 where the local server returns HTTP 308. The verifier accepts only 301 or 308 to the exact same-origin trailing-slash destination and rejects temporary, cross-origin, or incorrect redirects.
- Visual inspection: all eight screenshots across the documentation index and toolchain route, both widths, and both themes showed no new clipping, overlap, broken rendering, theme failure, or material regression
- Known future improvements: Phase 13 issues #120 through #126 remain open and do not contradict a v1.2.0 certification gate
- Issue evidence: [#119 comment](https://github.com/shruggietech/shruggie-brand/issues/119#issuecomment-5555804005)

## Repository gates

- Regression-first proof: production-origin tests failed because the module did not exist, then seven tests passed after implementation
- Python geometry and release suites: 113 tests and checks passed across glyph construction, packaging, release contract, site preparation, brand contract, icon generation, and pipeline behavior
- Site lint and generated content: passed
- Static site build: 26 pages generated successfully with webpack
- Local browser contract: 26 routes at both widths, zero failures and zero WCAG 2.1 AA violations
- Production browser contract: 26 routes at both widths, zero failures and zero WCAG 2.1 AA violations
- Markdown prose policy: passed
- Generated agent synchronization: unchanged
- Git diff whitespace check: passed
- UTF-8 without BOM and LF-only scan: 16 changed text files passed
- Mojibake, private-path, and common secret-marker scan: passed
- Generated output and dependency directories: ignored and absent from the change set

## Pull request and reviews

Pending.
