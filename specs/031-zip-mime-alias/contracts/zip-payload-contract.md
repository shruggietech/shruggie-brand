# Contract: ZIP Download Payload

## Inputs

- A request path whose normalized extension is `.zip`.
- The response `Content-Type` header, which may be absent or include parameters.
- The complete response body as bytes.

## Media-type contract

Normalize the base media type by taking the value before the first semicolon, trimming whitespace, and lowercasing it. The normalized value must equal one of:

- `application/zip`
- `application/x-zip-compressed`

No wildcard, substring match, or generic binary fallback is permitted.

## Archive-body contract

Independently of the media-type result, a non-empty body must:

1. Meet the existing minimum ZIP record length.
2. Begin with the ZIP local-file signature `PK\x03\x04`.
3. Contain the end-of-central-directory signature `PK\x05\x06` inside the existing tail search window that accommodates the maximum ZIP comment.

The validator does not extract the archive or alter its bytes.

## Results

- Return no failures only when both the media-type and archive-body contracts pass.
- Return a media-type failure when the normalized type is unsupported or missing, listing the two supported values.
- Return an archive-body failure when the structural evidence is incomplete.
- Return both failures when both contracts fail.

## Compatibility boundary

This contract is origin-independent. The local static server and `https://brand.shruggie.tech` use the same validator. All contracts for non-ZIP extensions remain unchanged.
