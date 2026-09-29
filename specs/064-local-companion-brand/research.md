# Research: Local Companion Brand Kit

## Identity authority and approval

**Decision:** Use a constructed `glyphkit` Full and Reduced mark, promote only the exact approved source bytes, and bind palette, framing, topology, renderer, and 32 proofs through `identity_continuity.py`.

**Production binding:** The owner approved the original mark and a corrected Gate 1 binding to CI-pinned Node v24.11.0 and the opt-in single-line social composition generator. The Full and Reduced source bytes and all 32 proof PNG hashes remained identical. The corrected proposal SHA-256 is `5c9c2c49398e8ae1e230579cd3aa96a712f2886a5684450920d8fd4c18f75aca`.

**Rationale:** The owner rejected the existing LC monogram, selected the lower-right calm-orbit concept, and needs a new abstract production mark. `gen_logo.py --proof-stage-only` and `generate_current_proofs` produce the same mark SVG path and raster engine used for production. The private candidate reports zero glyph failures; its Full master has a 16-pixel component warning, so the Reduced master is used at and below 32 pixels.

**Alternatives considered:** Reusing the LC SVG conflicts with the owner's identity direction. Tracing the concept image would not yield governed, parametric source. Using the current W placeholder is invalid product artwork.

## Palette and typography

**Decision:** Keep graphite `#090B10` / `#11151D` and indigo `#8B9CFF`, with accessible `#4B5CC0` on light surfaces. Use the existing house font bundle, Space Grotesk 500/700, Geist 400/500, and Geist Mono 400, under its local OFL-1.1 source license.

**Rationale:** The original indigo clears 4.5:1 on all five planned dark surfaces, minimum 5.35:1. The darker light-surface indigo clears all five planned light surfaces, minimum 4.69:1. The current app's `#7184EB` variant is too light for small text on near-white. House typography is legal and portable for this kit, even when the brand's palette inheritance is independent. The app's Segoe UI Variable and Cascadia Mono stack remains implementation context; the kit does not imply those proprietary/system faces are bundled.

**Alternatives considered:** Bundling Segoe UI Variable would require redistribution rights not established by the app source. Fixed custom typography would require complete licensed face, hash, and provenance records without improving this slice.

## Interface cues and app parity

**Decision:** Treat formal product identity colors and functional interface cues as separate, measured systems. The owner selected app parity at Gate 2, so the kit binds amber `#F2BD68`, pink `#FF7B91`, green `#63D6AD`, and blue `#70B8FF` on dark surfaces with separately measured darker light-surface companions.

**Rationale:** `color_roles.py` derives eight cues from canonical roles. Its optional `functional_colors` binding now maps the four app state cues without changing formal identity colors or existing brands. The generated color-role manifest measures each selected cue against dark and light surfaces and records a text or icon signal.

**Alternatives considered:** The default kit mappings would have used indigo for warning and success, red for error, and indigo for information. The owner chose app parity. The representative Gate 2 application is synthetic and does not claim that the installed UI has adopted the portable kit fonts.

## Kit and site projection

**Decision:** Build the Local Companion kit from `brands/local-companion/brand.json` with `scripts/build_all.py`, then let `scripts/prepare_site.py` project all public pages, registries, images, and downloads from verified `dist/` output. Add the slug to release, publication-audit, workflow, and site-test inventories.

**Rationale:** `prepare_site.py` requires a generated kit per source brand and only includes public brands whose Gate 2 ledger authorizes the required surfaces. `interface_contract.py` separately governs which kit archives are release-authorized; omission there would leave a visible site entry without the requested released download. `scripts/audit_publication_artifacts.py`, `.github/workflows/build.yml`, and `site/tests/site.test.mjs` have explicit production lists.

**Alternatives considered:** Hand-authoring static site assets would violate the site's verified-kit source boundary and lose source-to-output traceability.

## Release and deployment

**Decision:** Bump the BrandBuilder release metadata, state skill/canon/migration impact accurately, and publish the exact CI-built asset on a `vMAJOR.MINOR.PATCH` tag reachable from `main` after both approvals and all gates pass.

**Rationale:** `scripts/release_contract.py` requires version agreement across `skill/SKILL.md`, `site/package.json`, `release-impact.json`, changelogs, and migration records. `scripts/package_release.py` produces a per-brand archive only for release-authorized slugs. The tag workflow validates source SHA, release inventory, and checksums, publishes the GitHub release, then deploys the exact Pages artifact. Source on `main` alone does not guarantee a live hosted kit.

**Alternatives considered:** An untagged site export or a hand-uploaded ZIP would bypass the required release and provenance checks.

**Additional release inventory evidence:** The local `v2.7.0` tag already exists, so this work requires a new version. `scripts/test_release_contract.py` fixes 2.7.0 metadata and seven exact archive names, `scripts/test_publication_workflow.py` fixes the eight hosted slugs, and `site/tests/site.test.mjs` fixes the same hosted inventory. `scripts/check_readme_links.py` and `scripts/audit_public_documentation.py` detect stale public counts. All of these must advance with the new release; `main` and a passing local build alone do not deploy Pages.
