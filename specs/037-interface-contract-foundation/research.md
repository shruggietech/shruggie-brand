# Research: Interface Contract Foundation

## R1. Existing authority surfaces

**Decision**: Extend the current Brand Canon instead of replacing it, and place the new Interface Canon beside `01-canon.json` under `skill/references/`.

**Rationale**: `01-canon.json` and `brand.json` already govern affiliation, identity, colors, typography, logo sources, approvals, and release versioning. Moving those concerns would create identity migration risk. Interface semantics need those values as inputs but need a separate lifecycle and explicit version.

**Alternatives considered**: Adding interface roles directly to every `brand.json` would duplicate defaults across production brands. Adding renderer-specific CSS or Rust structures to Brand Canon would make the source non-portable and pre-empt #215 and #216.

## R2. Backward-compatible production defaults

**Decision**: Resolve every existing brand through the shared Interface Canon and an empty optional `brand.interface.overrides` map.

**Rationale**: All production brands already provide the identity values needed by semantic interface aliases. Shared defaults prove compatibility without editing approved brand contracts or continuity records. Future explicit overrides remain narrow and validated.

**Alternatives considered**: Bulk-editing each brand with copied interface tokens would manufacture migration work and introduce drift. Treating absence as unknown would prevent current kits from generating.

## R3. Logical units and adapters

**Decision**: Define one logical UI unit and publish transform expectations for CSS pixels, egui points, and future native density-independent units, without emitting adapter code.

**Rationale**: A renderer-neutral measure remains stable while adapters own syntax and platform conversion. This closes the shared contract dependency and leaves actual Web and native adapters to their existing issues.

**Alternatives considered**: Storing CSS variables or egui structs in the canon would mix intent with renderer property bags. Using physical pixels would break text scaling and density independence.

## R4. Runtime environment model

**Decision**: Accept observed viewport, safe-area, input, accessibility, theme, IME, and titlebar capabilities, and reject operating-system names as routing inputs.

**Rationale**: Device stereotypes are unreliable. Mixed capability profiles are increasingly common and must remain valid. Adapters can report actual facts without the canon assuming a host.

**Alternatives considered**: `desktop`, `mobile`, or OS presets are convenient but silently conflate viewport, input, keyboard, and chrome behavior.

## R5. Contextual operating modes

**Decision**: Route from normalized intent and repository evidence, returning one mode plus a narrow clarification state when mutation authorities conflict.

**Rationale**: Natural-language keyword matching is brittle and magic wording is explicitly out of scope. Agents already interpret the request; the policy must tell them which observable facts control mode and what permissions remain unchanged.

**Alternatives considered**: Requiring `/author`, `/implement`, or `/audit` commands would fail ambient hosts. Allowing combined modes would obscure whether mutation is authorized.

## R6. Consumer manifest placement

**Decision**: Generate `enforcement/consumer-contract.json` and also list it in the kit-wide `manifest.json`.

**Rationale**: The focused manifest is discoverable beside agent instructions and can express authority and recovery without overloading the existing complete file inventory. The final kit manifest independently checksums it and every other output.

**Alternatives considered**: Replacing the existing manifest risks release compatibility. Encoding all consumer fields only in Markdown would not be machine-checkable.

## R7. Exact offline recovery

**Decision**: Bundle a deterministic exact-version `.skill` archive under `enforcement/distributions/`, record its SHA-256, and prefer it before any network recovery.

**Rationale**: A filename or version pin without delivered bytes cannot guarantee offline recovery. A nested deterministic archive supplies the exact implementation and can be verified before installation.

**Alternatives considered**: Pointing only at a latest release violates the issue. Pointing at an exact remote release still fails offline. Copying an unpacked tree is less atomic and harder to verify than one archive.

## R8. Governed instruction merging

**Decision**: Replace exactly one marker-bounded block, append it when absent, and reject malformed or duplicated markers before writing.

**Rationale**: This is deterministic, reviewable, and preserves all unrelated human text byte-for-byte except the single normalized separator used when appending a missing block.

**Alternatives considered**: Overwriting the file destroys local guidance. Heuristic heading replacement can consume unrelated sections. Repairing malformed markers automatically risks data loss.

## R9. Version semantics

**Decision**: Keep the current unreleased compiler and Brand Canon versions at `1.2.1`, introduce Interface Canon `1.0.0`, and report the existing per-brand version separately.

**Rationale**: This slice builds source changes but does not authorize a release tag or compatibility-policy expansion. The manifest still carries exact semantic identities. #218 owns the broader version matrix and adoption policy.

**Alternatives considered**: Bumping all release surfaces inside S037 would require release notes, site versioning, brand canon migration, and publication scope explicitly reserved for later work.

## R10. Security and integrity

**Decision**: Use contained relative paths, deterministic ZIP entries, SHA-256 for exact bytes, fail-closed marker parsing, no implicit network, and authorization-preserving gap records.

**Rationale**: There is no authentication or tenant boundary in this static compiler. The applicable risks are traversal, symlink escape, instruction clobbering, unverified recovery bytes, forged local authority, and unintended upstream mutation.

**Alternatives considered**: Signatures would require key management and release infrastructure outside this slice. Hashes plus the governed manifest are sufficient for exact delivered-byte integrity at this layer.
