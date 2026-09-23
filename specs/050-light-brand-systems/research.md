# Research: First-Class Light Brand Systems

## Existing support and gaps

- **Decision**: Complete existing mode support instead of introducing a new theme preference. **Rationale**: I Heart PR Tours already declares `guide.surface_mode: light`; PDF and portable generators partially honor it, while hosted routes and portfolio do not. **Alternative considered**: Root-level user theme switching would leak into unrelated site routes and change the brand's governed identity.
- **Decision**: Validate the declaration in the source contract before generation. **Rationale**: Current `build_kit.py` enum validation occurs late and can be bypassed in a no-PDF capability tier. **Alternative considered**: Keep late-only QC, rejected because an invalid source would still produce portable output.
- **Decision**: Carry mode and semantic colors through the generated portal and site brand record. **Rationale**: The portal contains both palettes but no authoritative selection. Hosted UI otherwise guesses from the browser theme or color luminance. **Alternative considered**: Hardcoded slug rules, rejected as non-reusable and non-governed.
- **Decision**: Use a route-local token scope for Fumadocs and a card-local token scope for portfolio. **Rationale**: Root `<html class="dark">` and persisted host theme remain useful for the broader site. Fumadocs aliases must be overridden locally along with raw semantic variables, including nav/sidebar/mobile/toc. **Alternative considered**: Toggle root class or localStorage, rejected due to cross-route leakage and no-script mismatch.
- **Decision**: Retain per-asset dark/light wells. **Rationale**: `gen_guidelines.py` already classifies asset previews from approved colorway/appearance metadata; a light outer document does not make every asset a light-surface asset. **Alternative considered**: Force all wells light, rejected because white logos disappear.
- **Decision**: Correct PDF palette prose and selected-versus-comparison accent variables. **Rationale**: Existing light mode reverses `A` and `AL` while copy still labels them as dark/light, producing incorrect claims despite a light page.
- **Decision**: Extend measured QC and existing browser verifier rather than add a screenshot-byte golden test. **Rationale**: Constitution requires behavior and declared gates, and browser tests already cover narrow widths, zoom, no-script, reduced motion, and print. **Alternative considered**: Byte-compare PNG/PDF, prohibited by project guidance.

## Technical findings

- Source: `brands/i-heart-pr-tours/brand.json` has light mode, explicit `light_surfaces`, and immutable authoritative artwork. Its current portfolio record has `showcaseSurface: #FFFFFF`, but the UI rejects it because foreground is black.
- PDF: `gen_guide_pdf.py` selects light tokens for page CSS; `qc_render.py --expect-ground` can detect opposite outer page grounds. The palette narrative remains dark-first in places.
- Portable: `gen_guidelines.py` sets light `:root` and conditional `body.dark`, but the portal payload omits mode and standalone interactive focus uses fixed white/black cues.
- Hosted: `site/app/layout.tsx` fixes the initial root dark class; guide layouts inherit it. Portal types and CSS need a declared local scope.
- Portfolio: `site/components/brand-portfolio.tsx` and related CSS/tests deliberately accept only white-foreground governed surfaces. This is the behavior S050 intentionally changes.
- Validation: Existing Python and browser suites have light-brand source and white-well fixtures but do not prove full light route invariance or wrong-ground failure.

## Resolved questions

- **Does a missing declaration change old brands?** No. It means dark and is tested as such.
- **Does brand mode follow a visitor's site theme?** No. Brand presentation is declared source state. The broader site theme remains independent.
- **Does this publish or verify downstream consumers?** No. Source, generated kits, and this site's owned presentation are in scope; consumer adoption is not.
