# Implementation plan: Brand system foundation

## Technical approach

1. Establish the public repository, community files, licensing split, GitHub taxonomy, and Spec Kit integration.
2. Import the canonical skill and fonts, then upgrade provenance and accessibility validation where ground truth requires it.
3. Migrate the five identities as source-only definitions and verify each generated kit visually and mechanically.
4. Add a synthetic glyphkit fixture to exercise the complete pipeline without consuming an identity hue slot.
5. Add Linux CI, deterministic release packaging, and a Next.js static site generated from `dist/`.
6. Publish through GitHub Pages, bind the DNS-only Cloudflare CNAME, verify HTTPS and registry installation, and issue the first release.
7. Repeat the build from a clean checkout, document every migration-source disposition, and clean the staging folder only after all external gates pass.

## Architecture boundaries

- `brands/` and `fixtures/` contain hand-authored sources only.
- `skill/` owns canon, generators, and gates.
- `dist/` is the rebuildable integration boundary.
- `site/` owns presentation chrome and consumes generated outputs verbatim.
- `release/` and `site/out/` are ephemeral publication artifacts.

## Known ground-truth adjustments

- The source skill started at 1.1.1 rather than the work order's stated 1.1.0, so this work releases 1.1.2.
- ShruggieTech has raster-only authoritative art. The build preserves those exact silhouettes through recolored mask wrappers instead of inventing vector geometry.
- The fixture is exempt from sibling hue allocation because it is not an identity, while all contrast gates remain mandatory.
