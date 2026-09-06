# Icon Manifest Contract

## Location and encoding

- Authoritative manifest: `icons/manifest.json`
- Encoding: UTF-8 without BOM and LF line endings
- Schema version: `1.0.0`
- Relative paths use forward slashes and are resolved from the kit root.

## Required top-level shape

```json
{
  "schema_version": "1.0.0",
  "brand": "example",
  "profile": {
    "background": "#FFFFFF",
    "reduced_below_px": 32
  },
  "capability": {
    "tier": "full"
  },
  "suites": [],
  "artifacts": [],
  "aliases": {}
}
```

## Invariants

1. `brand` equals the kit's validated `brand.json` slug.
2. `suites` contains exactly one entry for each required platform identifier.
3. A generated suite has a present README, native or generated metadata, and at least one image artifact.
4. A skipped suite has no stale image or binary artifacts and records a non-empty capability reason.
5. Every artifact path exists exactly once, remains inside the kit, and matches its declared format.
6. Every raster artifact decodes to the declared dimensions and satisfies its alpha rule.
7. Every compatibility alias exists and is byte-identical to its authoritative target.
8. Every file below `icons/`, except the manifest itself, is declared as an artifact or suite document.
9. No `favicons/` file exists unless declared as an alias.
10. Source-owned product symbols below `icons/domain/` are declared as preserved domain artifacts and remain byte-identical across repeated generation.

## Failure contract

Verification reports the normalized relative file path, violated field, expected value, and observed value. Unsafe paths, duplicate paths, missing suites, undeclared files, stale aliases, and malformed native metadata are hard failures in raster-capable production builds.
