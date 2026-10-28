# S074 Release Data Model

- **Version tuple**: BrandBuilder and site 3.1.1; Brand Canon 2.1.0; seven edited brands at their next patch version; other brands and adapters retain their versions.
- **Candidate record**: Exact source SHA, thirteen verified kits, static site output, release notes, release asset names and SHA256SUMS.
- **Published record**: Annotated v3.1.1 tag, GitHub Release, uploaded assets and Pages deployment, all bound to the candidate SHA.
- **Recovery rule**: Existing v3.1.0 bytes remain immutable. A retry compares the same revision and checksums before any publication action.
