# Integrity Checklist: Ownership-Neutral Authoritative Inputs

**Purpose**: Review whether S007 requirements are precise enough to prevent false affiliation, identity mutation, unsafe font ingestion, and unapproved palette publication.
**Created**: 2026-09-05
**Feature**: [spec.md](../spec.md)

**Note**: This is a reviewer-owned requirements-quality artifact. Mark an item `[x]` only when a reviewer determines the criterion is satisfied. Checkbox state does not represent implementation completion.

## Affiliation and Publication Safety

- [ ] CHK001 Are ownership, parentage, inheritance, endorsement, service credit, and showcase permission defined as separate decisions with closed values? [Spec FR-001 through FR-004]
- [ ] CHK001A Does independent inheritance explicitly replace ShruggieTech semantic orange with required brand-specific emphasis and action colors across generated outputs? [Spec FR-029]
- [ ] CHK002 Is the prohibited third-party output behavior stated across every generated text and metadata surface rather than only the public site? [Spec FR-007 through FR-008]
- [ ] CHK003 Is missing or contradictory affiliation data required to fail before publishable output exists? [Spec FR-006]
- [ ] CHK004 Is the existing owned-brand migration explicit enough to prevent a compatibility fallback from silently classifying future client brands? [Spec FR-009]
- [ ] CHK005 Is public showcase permission defined without requiring confidential contract content? [Spec FR-005 and FR-024]

## Supplied Identity Integrity

- [ ] CHK006 Are authoritative mark, reduced-mark, wordmark, and reference-art roles independently representable? [Spec FR-017 through FR-020]
- [ ] CHK007 Do source records require immutable identity evidence, including path, hash, format, color profile, usage status, and allowed transformations? [Spec FR-018 through FR-019]
- [ ] CHK008 Are active SVG content, external dependencies, path escape, role collision, and source drift all explicit rejection cases? [Spec edge cases and FR-019]
- [ ] CHK009 Does palette analysis remain evidence-only until a human approval binds an exact candidate to an exact source hash? [Spec FR-021 through FR-023]
- [ ] CHK010 Are transparent-pixel behavior, deterministic output, analysis limitations, and ordinary accessibility validation all stated? [Spec FR-021 through FR-022]

## Typography and Ingestion Safety

- [ ] CHK011 Does every brand explicitly select house or fixed typography, with no implicit default? [Spec FR-010]
- [ ] CHK012 Does a fixed face declaration contain enough measured and declared facts to detect wrong family, face, format, hash, license, or usage status? [Spec FR-011 through FR-012]
- [ ] CHK013 Is controlled ingestion separated from ordinary offline builds and limited to secure or controlled sources and the repository font boundary? [Spec FR-013 through FR-015]
- [ ] CHK014 Is atomic failure behavior defined so rejected or interrupted ingestion cannot leave a partially approved font? [Spec FR-015]
- [ ] CHK015 Are all generated typography surfaces required to consume the selected contract instead of retaining house-font assumptions? [Spec FR-016]

## System and Verification Coverage

- [ ] CHK016 Are production migration, temporary test isolation, Python 3.8 support, hidden-process behavior, encoding, identity, and accessibility gates preserved? [Spec FR-025 through FR-026]
- [ ] CHK017 Is issue scope explicit enough that only #104 and #105 can close from S007 while #106 remains open? [Spec FR-027]
- [ ] CHK018 Are the pull-request review ceiling and the requirement to answer and resolve every negative finding unambiguous? [Spec FR-028 and SC-009]

## Notes

- Leave unchecked criteria for an independent requirements-quality reviewer.
- `$speckit-implement` must not modify these markers.
