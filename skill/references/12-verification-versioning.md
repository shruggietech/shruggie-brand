# Verification, Versioning, and Release

BrandBuilder treats verification and publication as separate states. Passing local checks makes a kit a valid candidate. Publishing makes exact bytes available. BrandBuilder records compatibility and migration impact for its own output, but it does not track downstream adoption or utility.

Canonical kit archives use `<brand-slug>-brand-<brand-version>-bb<brandbuilder-version>.zip`. The older brand-only form is non-canonical and MUST NOT be updated as a mutable alias. Every governed output-contract change requires a BrandBuilder version advance.

## Verification layers

Source checks validate schema, identity boundaries, continuity, provenance, and declared tool capabilities. Generator tests exercise deterministic output and negative paths. Kit verification inspects manifests, hashes, assets, tokens, adapters, support matrices, accessibility contracts, recovery, and documentation agreement. `validate_glyph.py` separately measures permitted vector geometry. A shippable kit has zero verifier problems and zero glyph failures.

The full repository gate compiles Python, runs focused contract and pipeline suites, validates Markdown and encoding, builds every production brand, synchronizes ambient agent instructions, stages the site, runs lint and type checks, builds static output, exercises Node and browser accessibility checks, audits publication, and inspects the Git diff for generated artifacts.

## Independent version domains

Brand Canon, Interface Canon, component recipes, Web/React adapter, egui adapter, compiler, and each brand have independent semantic versions. `version-policy.json` defines bump meanings and compatibility edges. The consumer contract records the complete tuple and the compatibility rules evaluated for it. Never replace one member with an unspecified latest version.

A patch preserves the domain's contract while correcting or clarifying behavior. A minor release adds backward-compatible governed capability. A major release changes the domain contract and requires an explicit migration path. The precise rules for each domain live in the version policy rather than prose inference.

## Recovery and conformance

Each generated kit contains an exact `.skill` recovery archive and SHA-256 checksum. Verify the checksum before extracting to the declared empty directory. Prefer delivered offline bytes. Network recovery requires separate authorization and the same exact version.

Conformance evidence proves measured behavior for the declared adapter and fixtures. It is not a promise that every host behaves identically. Missing host capability must be reported as an adaptation or gap, never hidden by a screenshot.

## Release procedure

1. Regenerate from governed source in a clean candidate workspace.
2. Run all documented validation and retain the exact results.
3. Inspect identity-sensitive output without altering approved geometry.
4. Publish immutable versioned artifacts and checksums.
5. Update current hosted references from the verified generated kit.
6. Keep older bundled contracts authoritative for their delivered bytes.
