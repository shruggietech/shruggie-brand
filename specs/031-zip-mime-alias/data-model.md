# Data Model: Hosted ZIP MIME Compatibility

## ZIP payload contract

- **Identity**: A requested path whose normalized extension is `.zip`.
- **Attributes**: Declared response media type, normalized media type, response body, validation failures.
- **Relationships**: References the supported ZIP media-type set and ZIP structure evidence.
- **Validation**: Passes only when the normalized media type is supported and the body contains all required ZIP structure evidence.

## Supported ZIP media type

- **Identity**: One exact normalized base media-type string.
- **Allowed values**: `application/zip`, `application/x-zip-compressed`.
- **Excluded values**: Missing or empty types, `application/octet-stream`, `text/html`, and every value not explicitly listed.
- **Normalization**: Strip parameters after the first semicolon, trim surrounding whitespace, and convert to lowercase before comparison.

## ZIP structure evidence

- **Opening evidence**: The body begins with the ZIP local-file signature `PK\x03\x04`.
- **Closing evidence**: The end-of-central-directory signature `PK\x05\x06` occurs within the existing maximum-comment search window at the end of the body.
- **Minimum size**: The body is at least the existing minimum ZIP record length.
- **Failure behavior**: Missing any item adds an archive-structure failure regardless of the declared media type.

## Validation result

- **Identity**: Ordered collection of zero or more diagnostic strings for one path, media type, and body.
- **Valid state**: No diagnostics after both metadata and structure evaluation.
- **Invalid media-type state**: Diagnostic names the normalized or missing type and both supported ZIP values.
- **Invalid archive state**: Diagnostic identifies missing valid ZIP signature and end record.
- **Combined invalid state**: Both diagnostics may be present when both declaration and body evidence fail.

## Invariants

1. A supported media type cannot compensate for invalid ZIP structure.
2. Valid ZIP structure cannot compensate for an unsupported media type.
3. Production and local verification apply the same ZIP payload contract.
4. Adding the alias changes no non-ZIP allowlist or body rule.
