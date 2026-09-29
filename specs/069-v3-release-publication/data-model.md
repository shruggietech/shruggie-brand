# S069 Release Data Model

| Entity | Identity | Required relationships |
| --- | --- | --- |
| Source revision | Full Git commit SHA | Exact `main` ancestor and `v3.0.0` tag target |
| Version tuple | BrandBuilder 3.0.0, Brand Canon 2.0.0, adapter versions | Equal across source metadata, notes, kit bundles, publication records, and site |
| Release candidate | Source revision plus verified outputs | Eleven kits and site, ten distribution files, checksum record, documentation record |
| Formal release asset | Canonical immutable file name and SHA-256 | Eight brand archives, skill, portable bundle; all derive from one candidate |
| Hosted brand package | One of eleven verified kit identities | Site copy and generated guide; eight also have a formal release archive |
| Official release | `v3.0.0` tag and GitHub release | Tag SHA equals candidate SHA; eleven uploaded assets include `SHA256SUMS` |
| Published site | Exact tag artifact | Publication status `release`, all eleven brands, exact release link |

State sequence: source candidate -> PR reviewed and green -> merged candidate -> exact tag -> release preflight -> official release -> Pages deployment -> post-publication verification. A failure leaves the last completed state intact for inventory-based recovery.
