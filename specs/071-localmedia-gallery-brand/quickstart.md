# S071 Validation Guide

Use the contributor prerequisites and hidden non-interactive Windows launcher policy in AGENTS.md. The private candidate is under dist/private/localmedia-gallery/gate-1 before promotion.

1. Run skill/templates/test_glyphkit.py and skill/templates/test_identity_continuity.py with the repository Python environment. Compound cutouts and source provenance must pass.
2. Run skill/templates/validate_brand.py and skill/templates/validate_glyph.py against the private candidate brand.json. Require zero glyph failures.
3. Prepare the private Gate 1 packet through the production proof-stage-only path, render both masters at 256/64/32/16 pixels on dark/light/black/white twice, and validate all hashes, palette evidence and review sheets.
4. After exact owner approval, promote source bytes to brands/localmedia-gallery and validate the canonical continuity record. Assemble and validate the private Gate 2 packet and exact social SVG/PNG.
5. After Gate 2 approval, build the final kit with scripts/build_all.py localmedia-gallery and require zero problems from verify.py and validate_glyph.py. Inspect generated logo/contact sheets and PDF/pagination evidence.
6. Run the full CONTRIBUTING.md and current CI aggregate checks, site/publication audits and source/encoding checks. Verify official deployed routes and downloaded checksums before claiming publication.

The source/derivative contract is defined in [contracts/delivery.md](contracts/delivery.md); states and authority are defined in [data-model.md](data-model.md).
