# Contract: v1.2.0 Candidate and Public Release

## Version discovery

```powershell
python scripts/release_contract.py current
```

The command prints only `1.2.0` and exits zero when skill metadata, canon metadata, requested changelog history, release dates, and all production source canon references agree. Any disagreement exits nonzero.

## Candidate commands

```powershell
python scripts/package_release.py
python scripts/release_contract.py notes --version 1.2.0 --output release/release-notes.md
python scripts/release_contract.py verify --version 1.2.0 --release-dir release --notes release/release-notes.md
```

An explicit `--version 1.2.0` remains accepted by packaging. Omitting it selects the validated current version.

## Expected assets

| Kind | Filename |
| --- | --- |
| Installable skill | `shruggie-brandbuilder-1.2.0.skill` |
| Portable skill | `shruggie-brandbuilder-1.2.0-portable.zip` |
| ShruggieTech kit | `shruggietech-brand-1.0.0.zip` |
| Fragcap kit | `fragcap-brand-1.1.0.zip` |
| Go Schedule kit | `go-schedule-brand-1.0.0.zip` |
| Glitchpad kit | `glitchpad-brand-1.0.0.zip` |
| Covarity kit | `covarity-brand-1.0.0.zip` |

## Invariants

1. Universal licensing, archive safety, canonical skill files, brand metadata, PDF signature, manifest coverage, byte counts, and SHA-256 rules remain those enforced by `scripts/release_contract.py`.
2. Skill and canon versions equal 1.2.0. Every production source and archive canon reference equals 1.2.0.
3. Production brand versions and corresponding archive filename versions remain unchanged.
4. Root and bundled 1.2.0 changelog sections use the same date and the generated notes contain the exact root section body.
5. Release notes explicitly require existing kits to rebuild for the v1.2.0 migration.
6. Candidate output contains no file outside the seven expected assets and the separately supplied generated notes file.

## Published verification

After owner merge, save the GitHub release body and download all seven assets into a newly created empty directory. Run the same verify command against those downloaded files. Local candidate output cannot substitute for a public download.

