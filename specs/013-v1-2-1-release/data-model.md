# Data Model: v1.2.1 Release and Production Certification

## Release Candidate

- **Version**: `1.2.1`
- **Source revision**: Reviewed pull-request head, then verified merged main
- **Metadata**: Skill version, canon version, site version, production-source canon references
- **History**: Root and skill changelog sections dated 2026-09-06
- **State**: Draft -> locally verified -> review-complete -> merged-main verified

## Release Asset Set

- **Skill assets**: Installable `.skill` file and portable `.zip`
- **Brand assets**: One archive for each of five production brands
- **Cardinality**: Exactly seven
- **State**: Candidate-built -> contract-verified -> CI-built -> freshly downloaded -> publicly verified

## Review Record

- **Round**: Automatic review only
- **Finding**: Source comment, severity, risk, disposition, correction, verification, and linked issue when negative
- **State**: Pending -> received -> dispositioned -> resolved

## Production Certification

- **Revision**: Merged main Pages deployment
- **Origin**: `https://brand.shruggie.tech`
- **Coverage**: Complete route inventory at 360px and 1280px, representative payloads, both themes, metadata, and WCAG 2.1 AA
- **State**: Pending -> deployed -> verified

## GitHub Tracking

- **Issue**: #140
- **Milestone**: #24
- **Closure rule**: Both remain open until public release assets and production deployment pass their contracts
