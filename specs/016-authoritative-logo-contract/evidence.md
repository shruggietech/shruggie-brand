# S016 Verification Evidence

## Scope and Baseline

- GitHub issue: #151, authoritative logo source locking and reconstruction prohibition.
- Feature branch: `codex/016-authoritative-logo-contract`, created from `efcd664` after S015 merged.
- Spec Kit selection: `.specify/feature.json` points to `specs\\016-authoritative-logo-contract` and remains ignored.
- Artifact boundary: `dist/`, `release/`, generated site output, caches, and local environments remain ignored.
- Identity boundary: no logo path, approved source byte, color, site presentation, or release version changed.

### Constructed path fingerprints

| Brand | Pre-S016 and current SHA-256 |
| --- | --- |
| Covarity | `b9846d9b00e393092678164a7d5f1c24cfd4186e2d2490b3d8a87be8e3b8e40c` |
| Fragcap | `47877d1667ac44ab6c81ed41ab675cf8831b7644e4926c4df93eeca024805e3b` |
| Glitchpad | `3115a137763ff75ab64a036282f9bc5bf683a3b4d68ffda6d0d5839da030c95e` |
| Go Schedule | `95ce6d68210a79672af6d639a4610070e61269842d414de63194fd0ed25fb5a6` |

ShruggieTech's retained imported path record remains `da15b5819b777ff3c1323d801b52333b0fd8015bbe08443bd7bc53085616cad7`; authoritative mode rejects its use as generated logo geometry.

### Authoritative source fingerprints

| Variant | Bound input | Pre-S016 and current SHA-256 |
| --- | --- | --- |
| Full | `full-mark-master` | `d500c3eadf049d36ce094bf7e35e37902a4ab49a66bcd6a9b40696961208a5c8` |
| Reduced | `reduced-mark-master` | `dc84170f164277ee4289240405aec1b35170937da0d4afe8f096ecd6d893c324` |

## Focused Verification

Run on 2026-09-07 from the repository virtual environment:

- `test_brand_contract.py`: 26 passed.
- `test_pipeline.py`: 29 passed.
- `test_iconkit.py`: 14 passed.
- `test_glyphkit.py`: 31 checks, 0 failures.
- `test_release_contract.py`: 13 passed.
- `test_prepare_site.py`: 20 passed.
- `test_package_release.py`: 2 passed.
- `check_markdown.py`: passed.

The tests cover explicit modes, separate role-correct bindings, stale or reference-only inputs, construction-helper conflicts, unrelated geometry, reduced substitution, deterministic provenance, SVG metadata, valid recolors and lockups, incomplete or stale lineage, undeclared operations, topology tampering, and platform master handoff.

## Production Verification

`scripts/build_all.py` rebuilt all five production kits. Every kit reported `BUILD CLEAN`; aggregate output reported five kits and zero problems. Each `verify.py` report had zero problems and each glyph report had zero failures. ShruggieTech generated 21 SVG logo derivatives plus raster and platform suites from its bound sources, with complete provenance and exact mask-topology agreement.

The five logo sheets, five PDF contact sheets, five responsive guideline sheets, and five responsive product sheets were inspected. Marks, lockups, Full and Reduced variants, colors, typography, desktop layouts, and 390 px layouts were intact with no visible substitution, clipping, overflow, or presentation drift.

Release packaging produced and verified all seven version 1.2.1 assets without publication. Site lint and local verifier tests passed, including 11 payload and production-origin tests. The normal Windows Turbopack launcher twice failed to spawn its pooled Node child with operating-system error 5 and misleadingly named an existing generated MDX file as missing. The same prepared source completed a production build with Next.js's supported webpack builder, including TypeScript, all 26 static pages, and build traces. Hosted Linux CI remains the authoritative Turbopack result.

## Spec Kit Analysis

Initial cross-artifact analysis identified two material omissions, both resolved before implementation completion:

- Fresh owner approval is now required for a changed binding, hash, source artwork, mask method, or visible geometry (FR-021).
- Raster silhouette acceptance now requires exact binary topology after deterministic nearest-neighbor normalization (SC-004).

Final analysis result: zero material consistency, coverage, ambiguity, constitution, or underspecification findings across 21 functional requirements, 6 success criteria, and 37 chronological tasks.

## Publication

- Pull request: https://github.com/shruggietech/shruggie-brand/pull/154
- Automatic Codex review: pending.
- Optional second review round: not requested.
- Hosted CI: pending.
