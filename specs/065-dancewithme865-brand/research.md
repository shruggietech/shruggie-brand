# Research: DanceWithMe865 Brand Restart

## Decision 1: Reference and source authority

**Decision**: Treat the owner-provided Natalie image as the selected visual direction and the supplied SVGs as candidate authoritative production sources. Do not inherit the earlier S065 design or approvals.

**Rationale**: The 1024 x 505 Natalie image closely matches the archive's `stacked-light` raster; its SVG presents the same DWM, upright outlined DANCEWITHME, and white 865 in a red rectangle. The supplied SVGs pass the repository passive SVG validator and match archive bytes. That is more faithful than reconstructing the lockup from a display font.

**Alternatives considered**: Recreate a new DWM glyph or generate an italic wordmark. Both change recognizable geometry and conflict with the pictured direction.

## Decision 2: Full, Reduced, and lockup roles

**Decision**: Propose the supplied DWM `mark-color.svg` as Full and the distinct supplied DWM `mark-reduced-color.svg` as Reduced, with source-faithful light and single-ink colorways. Propose the supplied stacked and horizontal SVG lockups for their intended surfaces. The stacked light source is the primary comparison to Natalie's image.

**Rationale**: Both marks use the established three-letter silhouette. Their distinct path data supports the repository's Full/Reduced requirement. Supplied outlined lockups retain the upright wordmark and boxed 865 without font substitution.

**Alternatives considered**: A new single-D Reduced mark and generated live or outlined font wordmark. These are rejected as visual deviations. Small DWM legibility remains an explicit 16 and 32 pixel Gate 1 review item.

## Decision 3: Color and accessibility

**Decision**: Keep the source artwork colors as a candidate palette only. Qualify all declared roles under the repository's sRGB, OKLCH, contrast, rendered-size, color-vision, semantic, and single-ink checks before requesting Gate 1.

**Rationale**: The light lockup uses near-black `#08090A`, red `#DF221E`, and off-white `#F8F8F6`; the off-white 865 on red measures 4.503:1, just above the ordinary text threshold. Antialiasing and application size require separate proof. The dark candidate uses brighter red `#FF493D`. The complete role map and rendered checks are bound in the Gate 1 proposal.

**Alternatives considered**: Assume the red passes because its source SVG is supplied. That would bypass the non-exemptable accessibility floor.

## Decision 4: Deliverable contract

**Decision**: Use the repository schema, governed brand sources, production renderer, generated kit, and site registry. Import only reviewed source assets and licensed fonts as needed. The ZIP tree, manifest, and prose are not output templates or public facts.

**Rationale**: The repository's canon and constitution define required content and source boundaries. ZIP folder shape has no authority over generated paths.

**Alternatives considered**: Copy the archive as a finished kit or adapt the generator to its paths. Both violate the owner's explicit instruction.

## Decision 5: Typography and copy

**Decision**: Preserve the supplied outlined wordmark independent of body typography. Use the four supplied font binaries as candidate support typography, with recorded metadata, exact hashes, and complete OFL license texts. Keep public service claims and the social slogan unresolved until supported by owner wording.

**Rationale**: The ZIP font name tables indicate OFL 1.1, but the archive does not contain full license text. Complete Kanit, Rubik, and Source Code Pro OFL texts were retrieved from the upstream font repositories. The lockup does not require font recreation. Brand prose in the ZIP is not an owner-approved claim. Support typography remains a Gate 2 review item.

**Alternatives considered**: Import all ZIP fonts and copy its descriptive prose immediately. That would conflate concept material with governed approval.

## Decision 6: Source binding support

**Decision**: Extend the general authoritative-source contract only where needed to bind supplied Reduced colorways and a supplied standalone outlined wordmark, while preserving existing output names and kit inventory.

**Rationale**: The current contract supports alternative Full colorways and supplied horizontal and stacked lockups, but not alternative Reduced colorways or a standalone supplied wordmark. Without those bindings, the light Reduced mark can disappear on white and the generator either invents a font wordmark or omits a supplied standard derivative. A derived single-ink wordmark also needs its own source binding, since the supplied black and white lockup files include a second cutout fill. The extension addresses a general contract gap without adopting any archive path or schema.

**Alternatives considered**: Recolor an authoritative SVG silently, accept an invisible light Reduced mark, or declare wordmark-only unavailable despite an exact supplied wordmark. Each loses source fidelity or a required deliverable.

## Decision 7: Small platform icons and social composition

**Decision**: Keep the supplied Reduced DWM paths unchanged. Use a signature red plate for small Windows taskbar frames, and render the owner-approved name once in the social image when the supplied lockup already contains it. Reopen Gate 1 because the icon setting changes the governed source snapshot and the social renderer change alters the renderer digest.

**Rationale**: The first private build reported unplated 16, 24, 32, and 48 px taskbar frames too short for the standard validator. The revised plated frames pass that check without inventing a new mark. The first social image repeated DanceWithMe865 beneath a lockup already containing the name, which obscured the owner's `DanceWithMe865 only` direction.

**Alternatives considered**: Invent a new single-D submark or waive the icon gate. The first changes identity geometry without an owner decision; the second conflicts with required verification.
