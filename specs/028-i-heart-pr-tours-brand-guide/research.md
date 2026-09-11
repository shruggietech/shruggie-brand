# Research: Identity-Locked I Heart PR Tours Brand Guide

## Intake authority

**Decision**: Treat the supplied Brand Assets ZIP as the intake container and its one-page Canva PDF as `reference-art` and `brand-guide` evidence only. Do not promote either PDF, their embedded image streams, their vector/text objects, or crops of rendered pages as Full, Reduced, wordmark, or lockup masters.

**Rationale**: The ZIP contains 68 safe relative entries: the guide, an eight-page logo PDF, seven SVG identity files, matching large and normal PNG exports, a complete favicon family, and Courier Prime, Poppins, and Source Sans 3 font bundles. The dedicated SVG files establish stronger standalone authority than PDF crops or extracted page objects.

**Alternatives considered**: Cropping the lockups from the PDF preserves the visible page but invents crop and resolution authority. Extracting embedded JPEG streams preserves their compressed bytes but detaches them from the document and does not supply the lockup lettering. Reconstructing lockups from embedded fonts directly violates issue #188.

## Source authority hierarchy

**Decision**: Propose the exact supplied SVGs as production identity sources. `vertical_lightbg.svg` is the primary light-surface lockup, `vertical_darkbg.svg` is its dark-surface alternate, `horizontal_lightbg.svg` and `horizontal_darkbg.svg` are secondary lockups, and `heart.svg` is the reduced mark and scalable colored app-icon source. Preserve `vertical_sand.svg` and `horizontal_sand.svg` as supplied promotional compositions. Treat ordinary redundant PNG and PDF files as lower-authority comparison evidence. Treat the supplied favicon and platform-icon family as exact per-target compatibility authority after live-site verification.

**Rationale**: The SVGs are exact standalone Canva exports with safe relative structure and no scripts, live text, event handlers, or network references. They contain outlined lettering plus embedded PNG heart artwork, local masks, and filters. The light/dark files alter lettering color on transparent canvases; the sand files include their decorative square background. The large and normal PNGs use differing crops and canvases, so silently choosing a PNG would create weaker framing authority.

**Alternatives considered**: Using only the heart as Full and Reduced would discard supplied lockups. Retyping Courier Prime and Poppins would replace artwork. Promoting every redundant PNG would bloat the repository and preserve conflicting crops as peers. Flattening the hybrid SVGs would change source structure and weaken scale behavior.

### Live favicon and platform-icon authority

**Decision**: Copy exact supplied colored-heart favicon and platform targets at their declared sizes. For modern app sizes absent from the supplied family, derive from unchanged `heart.svg`, suppress its soft raster shadow, and fit the colored mark to the safe area measured from supplied 192 and 310 pixel platform masters. Never substitute a monochrome mark for favicon or app-icon roles.

**Rationale**: The live page declares one 32 × 32 PNG for favicon, nominal 192 × 192 favicon, and Apple touch roles. The original live asset is 32 × 32 with visible bounds `(2, 3, 30, 30)`. The supplied `favicon-32x32.png` has visible bounds `(1, 3, 31, 30)` and differs by only 0.6764 mean RGB levels after white compositing, consistent with CDN optimization. The rejected Gate 2 generated favicon differs by 37.7393 and fills the complete alpha canvas. Supplied 192 and 310 pixel masters converge on approximately 89.6 percent visible width, 82.3 percent visible height, 10.9 percent top space, and 6.8 percent bottom space.

**Alternatives considered**: Reusing the rejected current generator enlarges the heart to the canvas edges. Upscaling the 310 pixel raster to every modern size loses available detail. Treating the live CDN bytes as source would replace the owner-supplied package with an optimized derivative.

## Passive SVG compatibility

**Decision**: Narrowly extend passive-SVG validation to accept only self-contained `data:image/png;base64` references whose decoded media type, byte length, and SHA-256 are measured, while continuing to reject scripts, live text, event handlers, foreign objects, stylesheets, filesystem paths, and network references. Embed the approved source SVG bytes unchanged in generated outputs.

**Rationale**: All supplied SVGs use local embedded PNG data for the heart artwork. The current validator rejects every data URI even when it is self-contained and passive. Converting, stripping, tracing, or replacing those image nodes would violate source preservation. A bounded parser rule preserves the exact files while keeping external resource loading fail-closed.

**Alternatives considered**: Selecting large PNGs avoids the validator change but the current authoritative PNG path assumes recolorable masks and would mishandle the multicolor identity. Allowing arbitrary data URIs would be too broad. Rewriting the SVGs is prohibited.

## Palette measurements and use

**Decision**: Preserve all eight printed guide values as identity evidence: `#1C5B8D`, `#68A9DD`, `#A1CFF4`, `#E8C393`, `#F1D4AE`, `#F6E1C5`, `#F8EFE4`, and `#C5342C`. Do not recolor embedded or supplied artwork to match the swatches. Gate 1 must approve semantic roles separately from source-art color placement.

**Rationale**: Independent measurement shows `#1C5B8D` and `#C5342C` pass ordinary text on white at 7.17:1 and 5.38:1. The five light blue/tan/cream values pass strongly on black, from 8.31:1 to 18.46:1, but fail ordinary text on white. The dark blue fails on black at 2.93:1 and the red fails ordinary text on black at 3.90:1. Embedded heart imagery also contains textured/gradient blue and red values that do not exactly equal the flat guide swatches.

**Alternatives considered**: Shifting customer colors to make every pairing pass would alter the identity. Allowing failures as exceptions would violate constitution P3. The compliant approach preserves fixed colors and limits their semantic roles by measured surface.

### Revised live-site and brochure foundation

**Decision**: Revised Gate 1 uses the live site's exact `#C5342C` as action red, `#1C5B8D` as frequent support blue, `#68A9DD` and `#A1CFF4` as bounded light-blue supports, white `#FFFFFF` as the primary paper surface, `#111111` as ink, and `#555555` as muted ink. The two supplied brochure masters independently quantize to the same dominant blue and an earth cluster near `#5D4A46`; use `#5D4A46` as the occasional brown support. Earlier printed sand and cream values remain governed source evidence and native colors inside supplied sandy artwork, not the primary semantic UI palette.

**Rationale**: The live client surface establishes the actual action and support hierarchy the owner requested. Red, blue, brown, ink, and muted ink all pass ordinary text on white at 5.38:1, 7.17:1, 8.29:1, 18.88:1, and 7.46:1 respectively. The two lighter blues fail ordinary text on white at 2.53:1 and 1.65:1 and are therefore limited to decorative fields, large graphics, or combinations with a compliant dark foreground.

**Alternatives considered**: Keeping the first dark-neutral delivery would contradict the client's live and printed identity. Promoting pale sand values as the main support family would underweight the site's stronger blue system and would not supply a compliant brown text role.

## Typography identity and licensing

**Decision**: Propose the exact supplied Poppins Bold 4.004 file for display, Source Sans 3 3.052 Regular and Semibold files for body, and Courier Prime Regular 3.018 for the required mono role. Do not use any font to recreate logo lettering. Treat the Courier Prime Bold evidence in the logo PDFs as construction history only.

**Rationale**: The page label says `SOURCE SANS 3/PRO`, while its embedded subset names report SourceSansPro Regular and Italic. The supplied package resolves that ambiguity with an explicit Source Sans 3 archive and no Source Sans Pro archive. All three font ZIPs contain OFL text and exact static TTF binaries. Gate 1 binds only the minimum delivery set rather than all 40 supplied font files.

**Alternatives considered**: Selecting Source Sans Pro would require an unsupplied binary. Delivering every supplied weight would add unnecessary payload. Using Courier Prime to rebuild the mark would violate the artwork boundary. House mono is possible but less faithful than the supplied Courier Prime family.

### Live-site heading hierarchy

**Decision**: Use the supplied Poppins Bold for primary guide headings and the supplied Source Sans 3 Semibold for section labels, table headings, key labels, surface labels, and badges. Reserve Courier Prime for code, tokens, file paths, identifiers, and measured values. Use near-black `#111111` for primary headings and table labels, with `#1C5B8D` limited to the occasional uppercase section eyebrow already established by the live identity.

**Rationale**: Computed styles measured on the official site on 2026-09-11 use Poppins at weight 700 for most H2 and H3 headings, usually in `rgb(17, 17, 17)`. Supporting body and utility content uses Source Sans Pro, while one uppercase eyebrow uses `rgb(28, 91, 141)`. The supplied archive contains the delivery-safe equivalents already approved at Gate 1: Poppins Bold and Source Sans 3 Regular or Semibold. The prior generated guide incorrectly styled semantic labels and complete tables as Courier Prime, making them resemble low-resolution preformatted text.

**Alternatives considered**: Adding the site's unsupplied DM Sans or Outfit files would violate the approved archive boundary. Retaining Courier Prime with a larger size would preserve the wrong semantic role. Replacing all monospace use would make genuine implementation values less distinguishable.

### Small-text and surface-preview correction

**Decision**: Use Source Sans 3 for every footer, page number, cover metadata line, minor label, table value, measurement note, and portable-guide metadata role. Retain Courier Prime only for the literal installation command block at its existing 400 weight. Use the exact title-driven footer form `<brand title> | Brand System`. Present dark-surface source marks on bounded dark preview wells and light-surface source marks on light wells.

**Rationale**: Candidate `iheartpr-g2-r3` still inherited Courier Prime through generic `.m`, `.foot`, `.cover .sys`, `.cover .base`, portable `.mono`, delivery metadata, endorsement, and inline code selectors. That contradicted the owner's intended display-only character for the newspaper-like face, except where literal code convention requires monospace. Page 3 also placed the dark-surface horizontal and vertical masters on white cards. Their white lettering remained present but became invisible, leaving only the colored heart and creating the false appearance of a tiny off-center icon.

**Alternatives considered**: Recenter the visible heart would hide the actual surface mismatch and misrepresent the source asset. Recoloring or substituting the dark-surface sources would violate their approved authority. Removing the source variants would make the guide incomplete. Surface-correct wells preserve the unchanged files and show their intended use honestly.

## Transformations

**Decision**: Propose only byte-preserving source storage, unchanged SVG embedding, proportional resize, deterministic rasterization of the unchanged passive SVG, exact-alpha placement on approved solid surfaces, package-format conversion that preserves visible pixels, and non-cropping placement within declared bounds. Recoloring, tracing, retyping, outline generation, silhouette masks, geometry cleanup, crop changes, and invented wordmark-only or monochrome variants remain prohibited unless separately returned to Gate 1.

**Rationale**: These operations can be deterministic and source-bound without changing the customer's artwork. Exact allowed operations must be assigned per source rather than globally.

**Alternatives considered**: Automatic monochrome or recolor families make a visually complete kit but would reinterpret a multicolor Puerto Rico flag mark. A smaller honest delivery is preferable to an invented one.

### Revised single-ink derivation

**Decision**: Propose a deterministic single-ink derivation from the unchanged approved light-background master. Preserve source alpha, suppress the supplied soft raster shadow through an alpha-floor transition, turn near-white artwork into transparent knockouts through a narrow transition band, and recolor every remaining visible pixel to exact black or white. Bind the recipe, renderer, source hash, proof digest, and output digest. Do not infer approval from this proposal.

**Rationale**: A literal all-opaque-pixels recolor is technically possible but fills the white star and stripes and retains the source shadow as a dirty halo. The proposed transform preserves the mark's recognizable negative-space structure and yields a clean single ink without tracing, vectorization, retyping, or source mutation.

**Alternatives considered**: Solid silhouette conversion destroys internal flag structure. Manual vector tracing creates new geometry. Keeping monochrome blocked leaves a deterministic current-kit capability unused after the owner explicitly requested reconsideration.

## Light-first guide and expressive assets

**Decision**: The I Heart PR Tours guide uses a white-paper light surface throughout, with dark examples confined to bounded demonstrations. Its brand discussion draws on the owner-supplied brochures: heartfelt local knowledge, thoughtful guidance, curated island experiences, history, culture, nature, and memorable photography. Add an optional `Expressions and atmosphere` section containing the exact supplied vertical and horizontal sandy treatments.

**Rationale**: The live site and both brochure masters are predominantly light or white-framed marketing systems, even when large photography and blue panels create contrast. The prior generator forced a dark root surface, preventing the requested result. The sandy treatments are already approved supplied compositions and need an honest guide role instead of disappearing from the delivery.

**Repository gaps**: `gen_guide_pdf.py` hard-codes full-bleed dark pages and dark tokens, `gen_guidelines.py` always renders a dark body, the site root forces dark theme, and hosted brand cards retain dark-biased descendant styles. These gaps are tracked in #193. The fixed generator, site-copy, and schema asset families have no optional expressive or mood-art category; that gap and future cross-brand digital artwork are tracked in #194.

## Affiliation and publication

**Decision**: Propose `third-party`, independent, parentless, private showcase, no inheritance, no endorsement, and no service credit at Gate 1. Repository pull-request review is permitted after Gate 2, while public registry, hosted guide, release, deployment, and showcase remain disabled unless explicitly approved.

**Rationale**: Issue #188 prohibits inferred ShruggieTech ownership, authorship, endorsement, maintenance, warranty, service credit, and public permission. A fail-closed private default is the only reversible starting point.

**Alternatives considered**: The current customer website credits ShruggieTech for site design and management, but that does not authorize brand-system authorship or reuse as a kit service credit.

## Product voice and imagery

**Decision**: Use the current official website only as retrieval-dated voice and use-context evidence. The resulting guide may describe locally rooted, small-group Puerto Rico experiences, expert local insight, history, culture, nature, flexibility, connection, and authentic team photography. Do not download or commit website media.

**Rationale**: The website currently presents the company as a family-style tour operator sharing Puerto Rico through small-group history, culture, and nature experiences, while the supplied guide calls for authentic photography and videography from real tours. These sources align on warmth, local knowledge, memorable discovery, and real island moments.

**Alternatives considered**: Copying current marketing text would make the guide brittle and blur identity guidance with site content. Downloading images would add unverified rights and source authority.

## S027 continuity state

**Decision**: I Heart PR Tours must enter as a new `approved-canonical` authoritative identity after Gate 1, not as a historical baseline. The approval bundle must bind exact sources, renderer settings, palette qualification, transformations, and full proof evidence.

**Rationale**: S027's historical mode exists only to preserve identities that predated the new process. S028 is the first new intake after that process merged and therefore must use its prospective approval lifecycle.

**Alternatives considered**: A historical record would falsely imply preexisting repository authority and evade the new proof and owner-binding requirements.

## Private-file boundary incident

**Decision**: Further discovery is restricted to explicitly named in-scope files or operator-provided paths. Generic neighboring files are never opened to infer that they belong to the logo package.

**Rationale**: During initial filename triage, three generically named nearby PNGs were briefly previewed to determine whether their timestamps connected them to the brand guide. They were unrelated, were not copied or hashed into evidence, and are excluded. This is stricter than the initial triage approach and directly enforces FR-025 going forward.

**Alternatives considered**: Continuing timestamp-based visual discovery risks exposing unrelated personal material and has no acceptable identity-authority benefit.
