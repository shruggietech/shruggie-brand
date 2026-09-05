# Evidence: v1.2.0 Release and Production Certification

## Baseline

| Item | Initial state |
| --- | --- |
| Verified base | `864eff349927d39caed3405e5f15c3c710d2dd71` on synchronized `main` and `origin/main` |
| Latest release | v1.1.2, published 2026-09-04 |
| v1.2.0 tag | Absent at slice start |
| v1.2.0 release | Absent at slice start |
| Current skill and canon | 1.1.2 |
| Production brands | Five, with independent versions and canon 1.1.2 |
| Root and skill changelogs | S006 through S009 changes under Unreleased |
| Open repository issues | None before S010 tracking creation |
| Phase 12 tracking | Milestone 22; parent #116; candidate #117; publication #118; production #119 |

## Decision record

| Decision | Outcome |
| --- | --- |
| Semantic version | 1.2.0 minor release for additive backward-compatible capabilities |
| Brand versions | Preserve all five independent brand versions; advance canon references only |
| Version authority | Validate skill and canon agreement; derive current workflow and packaging input from that path |
| PR closure | Close #117 only; track #116, #118, and #119 |
| Publication | Owner merge first, then annotated tag and CI-built release |
| Review ceiling | Automatic round one plus at most one explicit round two |

## Local verification

| Gate | Result |
| --- | --- |
| Regression-first release authority | Intended pre-implementation failures observed; final packaging tests 2/2 and release-contract tests 11/11 passed |
| Python compatibility surface | `compileall`, kit discovery, focused suites, and Markdown policy passed locally; hosted CI retains the Python 3.8 gate |
| Five production kits | Full-tier build completed with zero reported problems; every glyph gate had zero failures, every verifier had zero problems, and all image, PDF, and pagination gates passed |
| Visual inspection | All 20 generated sheets inspected at desktop and mobile sizes; the documented CDN-backed ShruggieTech UI kit was rerendered with network access and accepted |
| Release candidate | Exactly two v1.2.0 skill distributions and five independently versioned brand archives passed the shared release contract with generated notes |
| Site | Content preparation and TypeScript lint passed; the supported webpack production builder generated 26 static routes; browser verification completed successfully |
| Turbopack note | Local Windows denied Turbopack's pooled Node child process; the generated MDX source existed and webpack completed, while hosted Linux CI remains the authoritative normal-command gate |
| Generated agent contract | Synchronization reported unchanged output and `git diff --exit-code -- skill/AGENTS.md` passed |
| Repository hygiene | Markdown, diff whitespace, ignored generated outputs, UTF-8 without BOM, LF, mojibake, sensitive-data, and private-path checks passed across 26 changed files |

## Pull request and review ledger

Pending publication.

## Hosted checks

Pending publication.

## Post-merge release and production certification

Pending owner merge.
