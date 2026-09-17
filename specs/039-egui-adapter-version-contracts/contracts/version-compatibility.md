# Contract: Independent Version and Compatibility Policy

## Independent domains

Brand Canon, Interface Canon, component recipes, Web/React adapter, egui adapter, compiler, and every brand each carry an independent semantic version. A change bumps only the domain whose meaning changed, except when a compatibility rule requires a dependent domain release.

## Bump rules

- Patch identifies backward-compatible corrections that do not add or remove public contract surface.
- Minor identifies backward-compatible additions, new optional fields, or expanded adapter support.
- Major identifies removals, renamed meanings, incompatible defaults, required-field shape changes, or behavior changes that invalidate conforming consumers.

Domain-specific examples in `version-policy.json` refine these rules and are authoritative when they are stricter.

## Compatibility and lifecycle

Compatibility is a validated relationship among exact versions. A candidate has generated and verified bytes but is not yet an immutable publication. Publication means immutable artifacts for one domain exist. An unadopted record makes no downstream-use claim, while adoption means a specific consumer pins and uses those artifacts. None of these states implies either of the others.

## Pinning and recovery

A consumer handoff pins every domain version, authority path, and checksum needed to verify the kit. Delivered offline BrandBuilder bytes are the primary recovery source. Guidance must never substitute `latest`, a range-selected version, or a newer compiler for the exact pinned distribution.

## Failure behavior

Generation, kit verification, and release certification reject an incompatible domain combination with the dependent domain, actual version, required compatibility, and remediation direction. They also reject missing policy, mismatched authority copies, checksum drift, schema drift, and manifests that omit a version domain.
