# S074 Research

- The current release is v3.1.0; main includes S072 messaging, S073 site layout and dependency fixes after that tag.
- `.github/workflows/build.yml` deploys Pages only from a successful version-tag run after build and release publication. `CONTRIBUTING.md` requires CI-built release assets.
- `scripts/release_contract.py` validates coordinated site, skill, impact and dated changelog metadata and generates migration notes. The release policy classifies compatible output and correction work as patch changes.
- S072's plan and root changelog explicitly defer the seven brand and BrandBuilder patch versions to the next release slice.
- The published artifact boundary is ten owned brand archives, one skill, one portable bundle and SHA256SUMS; all thirteen production kits feed the site.
