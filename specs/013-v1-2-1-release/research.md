# Research: v1.2.1 Release and Production Certification

## Patch version

- **Decision**: Publish v1.2.1.
- **Rationale**: S012 corrected site presentation, accessibility verification, documentation language, and the ShruggieTech application-icon background without breaking public source contracts. Brotli 1.2.0 is a compatible security update.
- **Alternatives considered**: v1.3.0 would overstate the scope; retaining v1.2.0 would leave current main and public assets divergent.

## Version authority

- **Decision**: Advance the synchronized skill and canon metadata plus the site package and production-source canon references.
- **Rationale**: Existing release validation treats skill and canon as the shared compatibility baseline, and generated archives record that canon.
- **Alternatives considered**: Decoupling skill and canon versions is a separate architecture change with no benefit to this patch release.

## Migration statement

- **Decision**: Record conditional migration for v1.2.1.
- **Rationale**: The ShruggieTech kit and site should be rebuilt to receive the corrected black-background icon and presentation, while other brand assets have no behavior change beyond canon metadata parity.
- **Alternatives considered**: A blanket mandatory migration would misrepresent unaffected kits; declaring no migration would hide the ShruggieTech asset correction.

## Review boundary

- **Decision**: Inspect and fully resolve the automatic Codex review but do not manually trigger another round.
- **Rationale**: The user authorized release completion but did not authorize an additional review trigger, and the project's prior failures make a finite explicit boundary important.
- **Alternatives considered**: Triggering a second round without authorization would add delay and violate the stated boundary.

## Publication source

- **Decision**: GitHub Actions remains the only official asset publisher.
- **Rationale**: The release workflow rebuilds from the tag with native renderers and applies the same seven-asset contract used locally.
- **Alternatives considered**: Uploading local archives would weaken provenance and violate the constitution.
