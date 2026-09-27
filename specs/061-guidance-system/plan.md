# Implementation Plan: Durable Guidance System

**Branch**: `codex/061-guidance-system` | **Date**: 2026-09-27 | **Spec**: [spec.md](spec.md)

## Summary

Complete #270, #271, and #272 in one source-led change. Add a curated reference library to the canonical manual, validate stable local citations, apply sources to practical authoring and integration instructions, replace opaque guideline presentation with reader guidance, and expose exact kit documentation facts as static JSON. Keep hosted, packaged, portable, and PDF authority consistent while leaving generated outputs outside Git.

## Technical Context

**Language/Version**: Python 3.8 minimum for skill and generator; TypeScript/React with Node.js 20 minimum for the static Next.js site.

**Primary Dependencies**: Existing Python standard-library pipeline, Next.js App Router, Fumadocs MDX/search, Playwright site verification, current JSON contracts.

**Storage**: Git-tracked Markdown, JSON, Python, and TypeScript sources. Build-generated kits, site export, and release archives are ignored artifacts.

**Testing**: Python contract/publication tests, eight production kit `verify.py` and `validate_glyph.py`, site lint/build and browser tests, publication audit, qualitative reader tasks.

**Target Platform**: Static hosted documentation and downloadable skill/kit consumed offline; current supported web and egui adapters. Android and WordPress content describes guidance and boundaries, not a new adapter.

**Project Type**: Brand system generator plus static documentation site.

**Performance Goals**: Static build and search only; no new runtime fetch or dependency on external reference hosts. Guideline topics must remain usable at narrow width and 200% zoom.

**Constraints**: Preserve exact logo geometry, current brand data, current adapter behavior, WCAG 2.1 AA, all production kit gates, and source/artifact boundary. Maintain public facts as exact verified kit bytes.

**Scale/Scope**: Eight production brands; all nine topic classes including conditional expressions; 16 current main manual pages plus a References page; three connected GitHub issues.

## Constitution Check

| Principle | Design response |
| --- | --- |
| P1 source/artifact boundary | Change only tracked sources. Build kits and site output under ignored paths. |
| P2 identity geometry | No SVG path or brand identity mutation. |
| P3 accessibility | Keep AA floor; test semantics, focus, reflow, and 200% zoom. |
| P4 verification | Rebuild and verify every production kit; retain temporary synthetic test inputs. |
| P5 kit authority | Public facts copy exact certified kit bytes; hosted content derives from the portal in that kit. |
| P6 Spec Kit/release | Keep spec, plan, tasks, and verification evidence in this slice. PR only, no public release. |

No exception or complexity waiver is required. Rechecked after design in [research.md](research.md).

## Project Structure

### Documentation for S061

```text
specs/061-guidance-system/
  spec.md
  checklists/requirements.md
  plan.md
  research.md
  data-model.md
  contracts/
  quickstart.md
  tasks.md
  verification.md
```

### Source code and content

```text
skill/references/                    # Canonical manual, catalog, reference library
skill/templates/                     # Generated kit, portable guide, and PDF templates
scripts/                             # Manual transform, site preparation, publication audits
site/components/guidelines/          # Hosted topic presentation
site/lib/                            # Topic TOC and portal types
site/app/                             # Shared layout styles
site/scripts/                          # Browser reader and accessibility scenarios
```

**Structure Decision**: Use existing manual and generator ownership. Reference annotations live in canonical Markdown, facts in the certified kit, and site code renders or copies those sources. No new service or database.
