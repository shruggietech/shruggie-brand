# Data Model: Site Shell and Homepage Stabilization

## SharedNavigationLink

| Field | Type | Rules |
|---|---|---|
| label | string | Exact public label |
| href | URL or site path | Canonical destination |
| external | boolean | True for destinations outside `brand.shruggie.tech` |
| placement | menu | Available to desktop and mobile shared navigation |
| scope | site, docs, or both | Documentation root may be omitted on docs pages |

Required shared external records are Company and Download Skill. The existing GitHub source record remains available.

## SharedFooterLink

| Field | Type | Rules |
|---|---|---|
| label | string | Documentation, Download Skill, Company, Source, or License |
| href | URL or site path | Canonical destination |
| kind | internal, same-tab, or new-tab | Controls anchor rendering and opener isolation |

The ordered set has five records. Brands is invalid. Download Skill, Source, and License are `new-tab`; Company is `same-tab`.

## HeroAction

| Field | Type | Rules |
|---|---|---|
| order | integer | 1 Documentation, 2 Download Skill, 3 Explore Our Portfolio |
| role | primary, secondary, or supporting | Maps to generated orange or green treatments |
| href | URL or fragment | `/docs`, canonical releases URL, or `#portfolio` |
| cue | optional character | Supporting action uses decorative `↓` |

## LayoutMeasurement

| Field | Type | Rules |
|---|---|---|
| route | path | Compared route |
| viewport | width and height | Identical within a comparison group |
| theme | light or dark | Both required |
| scale | 1 or 2 | Browser context device-scale emulation |
| selector | string | Shared header, logo/menu, shell, docs page, or TOC |
| box | left, right, width, center | CSS-pixel geometry |
| overflow | number | Document scroll width minus client width |

Two measurements are stable when each required dimension differs by no more than one CSS pixel and overflow is zero.

## State Transitions

- Shared navigation changes presentation between desktop and mobile without changing record order or destinations.
- The docs TOC changes between desktop rail and narrow popover while the article remains inside one stable shell.
- Root scrollbar reservation remains stable when route content changes from short to tall.
