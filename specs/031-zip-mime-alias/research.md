# Research: Hosted ZIP MIME Compatibility

## Production behavior

**Decision**: Treat `application/x-zip-compressed` as a supported ZIP media-type alias alongside `application/zip`.

**Rationale**: The production GitHub Pages origin serves the valid brand archives with the alias while their ZIP opening signatures and end records pass the existing structural checks. Rejecting the response solely because of equivalent metadata produces a false deployment failure.

**Alternatives considered**: Change the hosting header, rejected because GitHub Pages controls it. Accept any `application/*zip*` value, rejected because pattern matching broadens the contract beyond observed and intended types. Accept `application/octet-stream`, rejected because it removes useful type evidence.

## Validation boundary

**Decision**: Add the alias to the existing extension-specific allowlist and make no change to ZIP body validation.

**Rationale**: Local and remote site verification already call the same payload contract. A declarative allowlist change fixes both paths while preserving the independent opening-signature and end-of-central-directory evidence that rejects HTML, empty, truncated, and mislabeled bodies.

**Alternatives considered**: Special-case the production hostname, rejected because payload semantics should not vary by origin. Rewrite response headers before validation, rejected because it hides the evidence being checked. Replace structure checks with media-type acceptance, rejected because headers alone are not trustworthy.

## Media-type normalization

**Decision**: Preserve the existing normalization that removes response parameters, trims whitespace, and compares the base media type case-insensitively.

**Rationale**: HTTP media types are case-insensitive and may carry parameters. Both supported ZIP values should participate in the same established behavior as every other payload type.

**Alternatives considered**: Match raw header strings exactly, rejected because harmless casing or parameters would recreate false failures. Add ZIP-only normalization, rejected because the shared normalization is already sufficient.

## Regression strategy

**Decision**: Cover both supported media types with valid and malformed ZIP fixtures, plus a structurally valid archive labeled with an unsupported media type. Retain the existing non-ZIP cases and run the complete site verifier.

**Rationale**: This matrix proves the compatibility addition and its fail-closed boundary independently. The broader suite demonstrates that the shared contract did not regress other extensions.

**Alternatives considered**: Add only one positive alias case, rejected because it would not prove malformed alias responses remain rejected. Depend only on a live production check, rejected because it is not deterministic and cannot exercise negative cases.
