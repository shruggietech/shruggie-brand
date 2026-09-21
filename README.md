# Shruggie Brand

This repository is the source of the ShruggieTech brand system. It contains the `shruggie-brandbuilder` skill, source-only definitions for eight production brand kits, the regression pipeline that rebuilds every kit, and the release-backed static site published at [brand.shruggie.tech](https://brand.shruggie.tech).

| You are | Take |
| --- | --- |
| Working in Claude, uploading to the Customize pipeline | `shruggie-brandbuilder-2.0.0.skill` |
| Working in Codex, or vendoring into a repository | `shruggie-brandbuilder-2.0.0-portable.zip`, entry point `AGENTS.md` |

## Brand kits

- [ShruggieTech](https://brand.shruggie.tech/shruggietech/)
- [Fragcap](https://brand.shruggie.tech/fragcap/)
- [Go Schedule](https://brand.shruggie.tech/go-schedule/)
- [Glitchpad](https://brand.shruggie.tech/glitchpad/)
- [Covarity](https://brand.shruggie.tech/covarity/)
- [ESO Weave](https://brand.shruggie.tech/eso-weave/)
- [Cueson](https://brand.shruggie.tech/cueson/)
- [I Heart PR Tours](https://brand.shruggie.tech/i-heart-pr-tours/)

Each brand page links to a generated multi-page guideline portal with focused voice, logo, color, typography, component, asset, and platform-integration topics. The downloads page also carries a standalone HTML guideline for offline use.

## Build

Install Python 3.8 or newer and the dependencies documented in [CONTRIBUTING.md](CONTRIBUTING.md), then build every production kit:

```powershell
python scripts/build_all.py
```

Build one kit by slug:

```powershell
python scripts/build_all.py covarity
```

Generated output is written to `dist/` and is intentionally ignored by Git.

Every canonical archive is named `<brand-slug>-brand-<brand-version>-bb<brandbuilder-version>.zip`. Production Pages advances only with an exact formal release; verified `main` output remains a reviewable CI candidate.

## Add a brand

Read `skill/references/00-variance-contract.md`, then add source files only under `brands/<slug>/`. Register the kit in the site and build script, then run the complete validation. New production accents must satisfy the system hue-separation rule and every text-bearing color must clear WCAG 2.1 AA. Tests that require synthetic brand data must create it in a temporary directory.

## Licensing

Code, templates, reference documentation, and site source are licensed under [Apache License 2.0](LICENSE). Attribution is in [NOTICE](NOTICE). Names, wordmarks, logos, endorsement lockups, and logo path geometry remain reserved as described in [LICENSE-BRAND.md](LICENSE-BRAND.md). Bundled fonts retain the SIL Open Font License 1.1 terms included with the font sources.
