# S054 Verification Scenarios

1. Run source/README mutation tests. Count words/digits, stale prose, slice codes, brand catalogs, specific build commands, malformed links, and absent alt text must fail; legitimate contract numbers pass.
2. Build production kits and site. Inspect every manual route for candidate identity and compare generated record with source and prepared bytes.
3. Package candidate assets. Independently mutate version, revision, inventory, source digest, page digest, skill URL, and packaged reference bytes; preflight must fail each.
4. After an authorized tagged release, check live manual routes and `/docs/publication.json` against exact release assets. Do not record a live pass before release.
