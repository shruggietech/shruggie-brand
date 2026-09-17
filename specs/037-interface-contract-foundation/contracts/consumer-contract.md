# Contract: Generated Consumer Authority

## Delivered files

Every kit contains:

- `enforcement/AGENTS.md`, one concise merge-safe governed block.
- `enforcement/IMPLEMENTATION.md`, the complete brand-specific application contract.
- `enforcement/consumer-contract.json`, machine-readable identity, environment, authority, versions, provenance, verification, recovery, and gap metadata.
- `enforcement/interface-canon.json`, the exact Interface Canon used for generation.
- `enforcement/interface-canon.schema.json`, the authoring schema for the delivered canon.
- `enforcement/capability-gap.example.json`, a complete local draft record with `submission_authorized: false`.
- `enforcement/distributions/shruggie-brandbuilder-<compiler_version>.skill`, the exact deterministic offline distribution.

## Authority precedence

The pinned brand source, Brand Canon, Interface Canon, and generated consumer contract outrank screenshots, legacy stylesheets, local token guesses, and visual inference. Human-authored repository instructions remain in force where they do not contradict the governed brand contract. A contradiction is reported, not silently merged.

## Recovery order

1. Use an installed BrandBuilder only when its version exactly matches `compiler_version`.
2. Otherwise verify and install the bundled distribution at the declared contained path.
3. Only when delivered bytes are absent and network use is authorized may a consumer obtain the exact named version from an authoritative release location and verify its published SHA-256.
4. Never install an unspecified latest version.

## Verification

Run the declared verification entry point from the kit. Completion requires zero verifier problems and zero glyph failures. Missing optional renderers are named skips; missing contract or integrity prerequisites are failures.

## Determinism

Identical governed source bytes and identical preserved human instruction content produce byte-identical consumer-contract files, governed blocks, copied canon files, gap templates, and nested distributions. Malformed markers produce no output mutation.
