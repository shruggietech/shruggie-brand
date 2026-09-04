# Implementation plan: Publication completion

## Technical approach

1. Convert the full private directive into detailed, sanitized phase issues and file one reproducible issue for each PR review finding.
2. Add shared capability and Windows subprocess helpers to the skill templates.
3. Make generation route from the measured tier and distinguish unavailable tools from failures after successful probes.
4. Generate bundled local fonts, consistent registry paths, and accessible native UI semantics from source.
5. Extend minimum-version and pipeline regression coverage in CI.
6. Rebuild all kits, the site, and release archives locally, then repeat through protected hosted checks.
7. Merge, deploy, validate the real registry CLI path, tag v1.1.2, and perform guarded staging disposition.

## Architecture decisions

- `probe.py` remains the only capability authority. Generators read its JSON rather than reinterpreting environment state independently.
- `process_utils.py` centralizes Windows console suppression for every direct project-owned subprocess launcher.
- `fonts.ts` is the deterministic offline binding. The upstream `registry:font` item remains schema-compliant and documents that distinction.
- Release packaging independently asserts required PDFs, even though the build pipeline also checks them. Publication integrity does not rely on one gate.
- Generated artifact directories are path-guarded and cleared before a lower-tier skip so previous higher-tier output cannot survive a downgrade build.
- The original operator directive remains private. Public requirements live in GitHub issues and these sanitized Spec Kit artifacts.
