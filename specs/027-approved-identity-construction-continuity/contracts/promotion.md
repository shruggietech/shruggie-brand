# Promotion Contract

## Preconditions

Promotion accepts one complete `approved-canonical` bundle beneath the configured ignored approval root. Its source inventory, identity snapshot, construction provenance, palette qualification, proof matrix, approval decision, and record digest must validate before filesystem mutation.

The promotion envelope contains only the approval-root-relative source root, the fixed `identity-continuity.json` record path, that record file’s SHA-256, and the envelope digest. The continuity record is the complete authority. Its source inventory must govern `brand.json`, the exact construction helper or authoritative inputs, and every permanent file in the provisional source root. Proofs remain beneath the excluded `proofs/` subtree and are validated but never promoted.

## Filesystem boundary

- Source and destination paths are forward-slash relative paths.
- Absolute paths, traversal, backslashes, symlinks, duplicate destinations, undeclared files, generated proof paths, and destinations outside the named brand root are rejected.
- Renderer declarations are data only and are never executed.
- Ordinary build commands cannot invoke promotion.

## Transaction

1. Resolve and validate the approval root, source root, and intended brand destination.
2. Refuse an existing destination unless replacement is explicitly requested and every replaced file is governed by the same approved bundle.
3. Copy declared source files into a new sibling staging directory without transformation.
4. Recompute every staged hash and the staged identity snapshot.
5. Atomically install the staged tree.
6. Recompute every installed hash and identity snapshot.
7. Emit a promotion record only when approval, staged, and installed values are equal.
8. On any failure, remove only the validated staging directory and leave the prior destination unchanged.

## Postconditions

Successful promotion produces permanent source whose declared bytes and canonical identity snapshot exactly equal the approved candidate. It does not copy approval render output into source, enable publication, perform Gate 2, modify a consumer repository, or make an identity decision.
