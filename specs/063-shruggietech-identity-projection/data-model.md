# Data Model: S063 Identity Projection

## Authoritative mark

Existing `authoritative_inputs` bind the full and reduced paid rasters by path and SHA-256. Bytes remain unchanged. The reduced source's mask record identifies source digest, derivation method, approval authority, and approval date.

## Delivery role

Each generated asset has role, platform, dimensions, appearance, `source_variant`, destination, and digest. Standalone square roles resolve to `reduced`; paired and approved contextual roles may resolve to `full`. The family, source master, manifest, filename, and preview agree. Platform framing stays inside its safe area.

## Message role

`social_copy.slogan` is exact public slogan text. `brand_idea`, `guide.idea`, and retained introductory headlines are distinct and do not become slogan fallbacks. `social_copy.approval` identifies the superseding correction. `social_image_approval` binds final SVG and PNG bytes after Gate 2.

## Review state

Existing source and creative ledgers carry Gate 1 and Gate 2 decisions. A proposed transformation or assembled image is pending until its exact candidate, source hash, derivative manifest, and rendered proof are reviewed. Changed bytes invalidate approval. Pending state blocks final compilation and publication.
