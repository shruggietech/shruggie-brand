# Research: ESO Weave Provenance and Current-Spec Kit

## Decision 1: Use synchronized upstream `main` as the evidence snapshot

**Decision**: Use ESO Weave commit `a165091d93b687100dc7471bbf5b7dd5f9d4c1e9`, fetched from the repository default branch on 2026-09-07, as the initial S020 evidence snapshot. Re-fetch immediately before each owner gate.

**Rationale**: Issue #153 requires current evidence rather than a frozen intake checkout. The synchronized revision advanced from intake commit `1280dfec2cfac67f70be65a2aa806f18bf982588`, but the two authoritative SVG hashes and four fixed-font/OFL hashes remain identical to intake.

**Alternatives considered**: Use the intake commit (stale and contrary to the issue); switch the neighboring working checkout to `main` (would disturb unrelated user work); infer current content from GitHub pages (weaker than a synchronized Git object snapshot).

## Decision 2: Map reorganized documentation to current canonical paths

**Decision**: Map `docs/brand/ESO-Weave-Brand-v1.md` to `docs/src/development/brand-standard.md`. Use the current `docs/src/` corpus and `docs/project/` governance records in place of the removed monolithic `docs/ESO-Weave-Specification.md`, while retaining the historical path in S012 evidence.

**Rationale**: Upstream reorganized documentation without changing authoritative identity files. Recreating removed paths would misrepresent current provenance and copy stale product material.

**Alternatives considered**: Treat path movement as identity drift (incorrect); copy only the historical files from S012 (insufficient current product voice); duplicate the old paths into the brand source (creates false authority).

## Decision 3: Classify provenance statements by evidence type

**Decision**: Record the introducing commit, S012 specification, source masters, current brand standard, and reproduction recipe as public repository evidence. Record “originated through the ShruggieTech brand-building system” as an operator-supplied assertion from issue #153.

**Rationale**: The public history proves when and how the identity entered ESO Weave but does not independently prove the service relationship. Keeping these classes separate avoids laundering operator knowledge into a public-history claim.

**Alternatives considered**: Present all provenance as repository-proven (overclaim); omit the origin statement (fails the issue); place it only in prose with no classification (not auditable).

## Decision 4: Preserve supplied SVGs as opaque authoritative masters

**Decision**: Copy `eso-weave-mark.svg` and `eso-weave-glyph.svg` byte for byte under the ESO Weave source tree and refer to them through authoritative-input records. Do not convert strokes to paths, optimize XML, change metadata, re-key coordinates, or normalize whitespace.

**Rationale**: Their stroked interlocking-carets geometry, round line caps, color-role order, overlaid teal segment, and badged canvas are load-bearing identity characteristics. Byte preservation is stronger and simpler than attempting geometric equivalence.

**Alternatives considered**: Convert to the constructed-path schema (identity mutation); embed a raster copy (loses vector authority); recreate paths from screenshots (unacceptable approximation).

## Decision 5: Separate source approval, derivative approval, and publication approval

**Decision**: Use explicit approval ledger records keyed by source hashes and derivative-set hashes. Palette selection is part of Gate 1. Gate 1 enables derivative construction but not publication. Gate 2 enables the exact enumerated public surfaces but becomes stale if any bound source or derivative hash changes.

**Rationale**: One Boolean “approved” cannot distinguish evidence acceptance, creative transformation, and public release. Hash binding makes approval deterministic and fail-closed.

**Alternatives considered**: One broad approval flag (ambiguous and stale-prone); prose-only evidence (not machine-enforceable); publication permission inferred from `showcase: public` alone (violates issue gate).

## Decision 6: Propose the supplied badged mark as the reduced master

**Decision**: Recommend the unchanged `eso-weave-mark.svg` badged master for reduced and platform-icon use. Recommend the badge-less glyph only for approved ink-background lockups above its measured minimum. Do not create a simplified caret variant unless the first gate explicitly requests one.

**Rationale**: Upstream already documents the badged mark as the icon used everywhere and specifically states it stays legible at 16 pixels on arbitrary backgrounds. Reusing an unchanged authoritative master avoids unnecessary geometry.

**Alternatives considered**: Simplify the glyph (unapproved identity work); treat the badge-less glyph as universal (fails on light backgrounds); invent a third reduced symbol (no evidence).

## Decision 7: Construct missing lockups from approved composition, not altered mark geometry

**Decision**: Propose horizontal and stacked compositions that place an unchanged authoritative mark or glyph beside or above an outlined Inter SemiBold wordmark. Propose wordmark-only output from the same approved outline. Treat composition metrics and text outlines as constructed derivative geometry requiring Gate 1.

**Rationale**: The current kit requires reusable vector lockups and outlined type, while upstream supplies only mark and glyph masters plus rendered raster references. Source-driven composition preserves the mark and makes the only new geometry explicit.

**Alternatives considered**: Embed live fonts in SVG (not portable enough for current contract); trace rendered wordmark rasters (less faithful); hand-author letterforms (identity invention).

## Decision 8: Keep fixed Inter faces brand-local unless reuse is approved

**Decision**: Ingest the three exact upstream Inter TTF files and OFL into the ESO Weave source directory through the existing fixed-font contract. Do not add a mono face unless the generator contract proves it is mandatory and the owner approves a licensed candidate.

**Rationale**: These files are already approved upstream identity sources. Brand-local storage preserves provenance and avoids implying that Inter is a shared house-family decision.

**Alternatives considered**: Promote Inter to shared fonts (unnecessary cross-brand policy); substitute house typography (violates independent identity); fetch current Inter from the network (breaks hash and offline guarantees).

## Decision 9: Derive voice from current product and safety documentation

**Decision**: Define ESO Weave as direct, technical, cautious, and state-focused. Lead with observed state, configured behavior, safety gates, and user responsibility. Avoid official-game language, promises of undetectability or account safety, and volatile roadmap details. Use Weave Status, Resource Status, and Automation Gate as representative UI domain components.

**Rationale**: The current README, feature manual, interface documentation, and responsible-use page repeatedly emphasize observable state, bounded automation, safety gates, and user responsibility.

**Alternatives considered**: Copy the full product specification (would become a second product spec); lean into fantasy voice (conflicts with modern technical tool); describe it as a ShruggieTech product (false affiliation).

## Decision 10: Enforce the vendor boundary as structured source content

**Decision**: Store required vendor disclaimer and trademark text in the ESO Weave source contract, project it into relevant generated guidance and public metadata, and test for its presence alongside the existing forbidden-affiliation scan.

**Rationale**: Generic third-party affiliation validation protects the ShruggieTech relationship but cannot by itself protect the separate ZeniMax, Bethesda, Microsoft, and Elder Scrolls boundary.

**Alternatives considered**: Put the disclaimer only in README prose (easy for generators to omit); hard-code ESO-specific text in site source (violates generated-kit ownership); rely on upstream links (insufficient in standalone output).

## Decision 11: Publication remains derived and disabled through Gate 2

**Decision**: Allow private local generation after Gate 1 but keep the source record ineligible for public site projection until a current Gate 2 ledger entry enumerates the exact approved site, registry, metadata, guideline, and downloadable surfaces.

**Rationale**: This preserves the existing source-to-`dist/` architecture and makes premature publication mechanically impossible.

**Alternatives considered**: Add static site pages early and hide links (still public output); delay all kit generation until Gate 2 (prevents meaningful review); maintain a manual site allowlist unrelated to brand approval (duplicated truth).
