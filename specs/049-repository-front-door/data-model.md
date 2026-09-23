# Data Model: README Publication Links

This slice introduces no persisted product data. It checks existing public-documentation references against an existing generated contract.

## README destination

- **Source**: Markdown link/image destination or HTML `href`, `src`, or `srcset` in the root README.
- **Class**: Repository-local target, canonical site route, official external destination, or badge image.
- **Validation**: Local targets resolve inside the repository and exist. Canonical site targets use HTTPS, exact host, and a pathname in the generated route contract. Untrusted lookalike hosts and unsafe local encodings fail.

## Brand route

- **Source**: A generated route record with `kind: guidelines`, `brandSlug`, `pathname`, and `canonical`.
- **Uniqueness**: One canonical overview destination per published brand.
- **Completeness**: Every generated brand overview route appears among README links.

## Release candidate

- **Source**: Existing release contract metadata and CI-generated candidate files.
- **States**: Merged source candidate, tagged verified revision, published release.
- **Invariant**: README latest-release guidance does not claim candidate bytes are already published; formal assets and checksums come from the exact tagged revision.
