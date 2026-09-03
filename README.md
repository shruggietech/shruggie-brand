# Shruggie Brand

This repository is the source of the ShruggieTech brand system. It contains the `shruggie-brandbuilder` skill, source-only definitions for five production brand kits, a synthetic fixture, the regression pipeline that rebuilds every kit, and the static site published at [brand.shruggie.tech](https://brand.shruggie.tech).

| You are | Take |
| --- | --- |
| Working in Claude, uploading to the Customize pipeline | `shruggie-brandbuilder-1.1.2.skill` |
| Working in Codex, or vendoring into a repository | `shruggie-brandbuilder-1.1.2-portable.zip`, entry point `AGENTS.md` |

## Brand kits

- [ShruggieTech](https://brand.shruggie.tech/shruggietech/)
- [Fragcap](https://brand.shruggie.tech/fragcap/)
- [Go Schedule](https://brand.shruggie.tech/go-schedule/)
- [Glitchpad](https://brand.shruggie.tech/glitchpad/)
- [Covarity](https://brand.shruggie.tech/covarity/)

## Build

Install Python 3.8 or newer and the dependencies documented in [CONTRIBUTING.md](CONTRIBUTING.md), then build every production kit and the fixture:

```powershell
python scripts/build_all.py
```

Build one kit by slug:

```powershell
python scripts/build_all.py covarity
```

Generated output is written to `dist/` and is intentionally ignored by Git.

## Add a brand

Start from `fixtures/example-brand/`, read `skill/references/00-variance-contract.md`, and add source files only under `brands/<slug>/`. Register the kit in the site and build script, then run the complete validation. New production accents must satisfy the canon hue-separation rule and every text-bearing color must clear WCAG 2.1 AA.

## Licensing

Code, templates, reference documentation, and site source are licensed under [Apache License 2.0](LICENSE). Attribution is in [NOTICE](NOTICE). Names, wordmarks, logos, endorsement lockups, and logo path geometry remain reserved as described in [LICENSE-BRAND.md](LICENSE-BRAND.md). Bundled fonts retain the SIL Open Font License 1.1 terms included with the font sources.

