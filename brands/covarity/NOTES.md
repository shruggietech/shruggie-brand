# Covarity migration notes

- Geometry provenance is `glyphkit`. `build/mk_paths.py` and both path masters were copied unchanged from the shipped kit.
- Generated `measured` and `color` blocks are intentionally absent from source `brand.json` and are restored in `dist/` by `enrich_brand.py`.
- The registry moved from `https://covarity.ai/brand` to `https://brand.shruggie.tech/covarity/brand`.
- No accessibility identity correction was required during source migration.

