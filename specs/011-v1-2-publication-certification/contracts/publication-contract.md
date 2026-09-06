# Contract: v1.2.0 Public Release

## Provenance

1. `origin/main` resolves to `39b65b5daf9ea74c317132d26347566a9e4959d5` before tagging.
2. The annotated tag object `v1.2.0^{}` resolves to that commit.
3. The successful Release workflow is triggered by the v1.2.0 tag.
4. The GitHub release is public, non-draft, non-prerelease, and targets v1.2.0.

## Expected public assets

| Kind | Filename |
| --- | --- |
| Installable skill | `shruggie-brandbuilder-1.2.0.skill` |
| Portable skill | `shruggie-brandbuilder-1.2.0-portable.zip` |
| ShruggieTech kit | `shruggietech-brand-1.0.0.zip` |
| Fragcap kit | `fragcap-brand-1.1.0.zip` |
| Go Schedule kit | `go-schedule-brand-1.0.0.zip` |
| Glitchpad kit | `glitchpad-brand-1.0.0.zip` |
| Covarity kit | `covarity-brand-1.0.0.zip` |

## Independent verification

The release body must match generated notes. The seven files must be downloaded from GitHub into a newly created ignored directory and pass `scripts/release_contract.py verify` with no local candidate file substituted. Universal licensing, archive safety, metadata, version, PDF, manifest, byte-count, and SHA-256 rules remain authoritative.

## Failure policy

A conflict, wrong target, failed workflow, unexpected release state, notes mismatch, asset mismatch, or verifier failure keeps #118 open. Never move or upload locally built candidate artifacts into the public-download directory.
