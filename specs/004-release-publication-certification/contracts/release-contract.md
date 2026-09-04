# Contract: v1.1.2 Release Metadata and Assets

## Commands

```powershell
python scripts/package_release.py --version 1.1.2
python scripts/release_contract.py notes --version 1.1.2 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.1.2 --release-dir release --notes release/release-notes.md
```

The notes command exits nonzero on metadata or changelog disagreement. The verify command includes the same metadata gate and exits nonzero on any missing, unexpected, malformed, unsafe, or inconsistent archive.

## Expected assets

| Kind | Filename |
| --- | --- |
| Claude skill | `shruggie-brandbuilder-1.1.2.skill` |
| Portable skill | `shruggie-brandbuilder-1.1.2-portable.zip` |
| ShruggieTech kit | `shruggietech-brand-1.0.0.zip` |
| Fragcap kit | `fragcap-brand-1.1.0.zip` |
| Go Schedule kit | `go-schedule-brand-1.0.0.zip` |
| Glitchpad kit | `glitchpad-brand-1.0.0.zip` |
| Covarity kit | `covarity-brand-1.0.0.zip` |

Brand filenames are computed from current source metadata. This table records the expected S004 baseline and must change with source versions.

## Universal archive rules

1. The archive opens as ZIP and contains no absolute or parent-traversal member.
2. `LICENSE`, `NOTICE`, and `LICENSE-BRAND.md` exist at archive root.
3. The release directory contains no file outside the expected seven asset names and the separately supplied generated notes file.

## Skill distribution rules

- The Claude skill contains `SKILL.md`, `AGENTS.md`, `CHANGELOG.md`, and the universal licenses.
- The portable archive omits `SKILL.md` and contains `AGENTS.md`, `CHANGELOG.md`, its portable `README.md`, and the universal licenses.

## Production-kit rules

- `brand.json`, `manifest.json`, `VERIFY.md`, and `brand-guide.pdf` exist.
- The filename slug and version equal the embedded `brand.json` slug and version.
- The manifest name, version, and canon equal the embedded brand values.
- Every file recorded by the manifest exists and matches its recorded byte count and SHA-256.

## Release-note rules

- The first-level title names `shruggie-brandbuilder v1.1.2`.
- Skill version and canon version are both explicit and equal authoritative source metadata.
- Migration is explicit: existing kits need migration and must rebuild to record provenance, accessibility corrections, and review remediations.
- The remainder is the exact 1.1.2 section body from root `CHANGELOG.md`.

## Published verification

After owner merge and successful tag workflow, write the GitHub release body to a temporary notes file and download all assets into the same fresh temporary directory. Run the verify command with those paths. Local build artifacts must never be substituted for downloaded assets.
