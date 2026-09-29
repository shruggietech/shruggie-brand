# Research: Scruggs Tire & Alignment

**Observed**: 2026-09-28. This file records reference evidence and planning decisions, not creative approval.

## Authority and source inventory

| Source | Observation | Use and authority |
| --- | --- | --- |
| Owner request in this session | New client brand, eventual official ShruggieTech brand-site publication, separate branch and PR, ZIP as conceptual guidance, base assets plus current website preferred | Binding scope and ownership instruction |
| Supplied `Scruggs Tire & Alignment_Brand.zip` | SHA-256 `7b49270d6ce058682fadc64aff6507645eb0dc0187d8f719137c24c48be147d9`; root contains one `Brand/` directory | Reference package, not a schema or approval source |
| ZIP `Brand/brand-colors-hex.css` and `brand-colors-rgb.css` | Ten matching swatches: white, four grays, bright red `#ED1B24`, charcoal `#414141`, deep red `#7D0B13`, near-black red `#3E0400`, black | Candidate palette only; no automatic role assignment |
| ZIP `Brand/Scruggs-Logo-1200-x-630-px.png` | 1200x630 red tire plus black `SCRUGGS TIRE & ALIGNMENT` on white; SHA-256 `bbd93ca7ee0866218e0173b35c436a53287a0b361a6d7f36587297df8ce6438d` | Current-looking Full-mark concept, not approved production geometry |
| ZIP `Brand/Scruggs_Logo_LightBG.png` | 416x236 transparent red tire/black wordmark lockup; SHA-256 `b556a49f5c04f3afbe69114a4a7dbef4ef10ad01e2f3161849b652bca410621a` | Current Full-mark candidate, byte-identical to the live site's logo image; subject to source-format review |
| ZIP `Brand/cropped-favicon.png` | 180x180 red tire motif; SHA-256 `e5c3ced0ea3f829b97d4411a2a249b89c1e31dd6c4397b0d0bf22fe33eb62b36` | Candidate small-icon treatment, not a substitute for all platform roles |
| ZIP `Brand/image-palette.png` | Visual strip confirms the CSS swatches | Redundant reference; CSS values are easier to measure |
| ZIP `Brand/scruggscolored.jpg` | Older red tire and outlined wordmark with telephone number | Historical styling only; do not use as current lockup or contact authority |
| ZIP `Brand/old/greertires.com.7z` | Nested legacy site archive | Not opened; no demonstrated need |
| [Live client website](https://scruggstires.com/) | Current red tire/black wordmark on white; dark mechanic-photo hero; white heading, red action/underline; computed body `Roboto` and headings `Montserrat`; live logo is 416x236 and its 25,908 bytes have the same SHA-256 as the ZIP's `Scruggs_Logo_LightBG.png` | Dated current presentation evidence, not a local-font license or exact source approval |

The ZIP also contains a key image, car image, shop photo, and dark automotive hero. They are contextual photographs or decorations, not required brand-kit schema members. No supplied file is an instruction from the owner merely because its contents have a directive tone.

PNG IHDR inspection found that `Scruggs_Logo_LightBG.png` is non-interlaced RGBA8, the format accepted for an authoritative PNG source. The 180x180 favicon and 1200x630 social-style image are non-interlaced indexed-color PNGs, so neither can be bound directly as an authoritative PNG logo under the current Core contract. This is a source-format finding, not approval of the RGBA8 lockup or a decision to recreate the reduced mark.

## Client facts observed on the live site

The site currently calls Scruggs Tire & Alignment a family-owned tire and alignment shop serving Greer and nearby Greenville, South Carolina since 1989. It describes computerized alignments, tire sales and repair, steering and suspension, brakes, inspections, and truck lift and leveling work. These are claims from the client's own public site as of the observation date; any copied public fact must be refreshed at implementation or publication. The site's footer credits ShruggieTech with site design and management, which does not transfer ownership or create an endorsement lockup for the new brand kit.

## Measured color implications

The following WCAG relative-luminance ratios are planning measurements against pure white, before final rendered-size qualification. Ordinary text requires at least 4.5:1; relevant non-text fills require at least 3:1.

| Candidate | Against white | Planning implication |
| --- | --- | --- |
| `#ED1B24` bright red | 4.39:1 | Fails ordinary text on white; may remain an identity mark color or qualify for a non-text role where applicable. Do not waive the text failure. |
| `#7D0B13` deep red | 10.88:1 | Plausible accessible red text/action candidate on white, subject to full role checks. |
| `#414141` charcoal | 10.21:1 | Plausible body text candidate on white. |
| `#808080` medium gray | 3.95:1 | Fails ordinary text on white; do not assign it to that role. |
| `#A0A0A0` light gray | 2.61:1 | Fails ordinary text and 3:1 non-text on white. |
| `#C0C0C0` pale gray | 1.82:1 | Decorative or surface candidate only unless a different pairing qualifies. |

## Decisions and alternatives

1. **Reference precedence**: Use the owner's scope and constitution for requirements, the live site and ZIP base assets for current design evidence, and the old-site archive only if a later named decision truly needs it. This honors the explicit source hierarchy without discarding useful context.
2. **Logo source mode remains undecided**: The live-identical RGBA8 lockup is a plausible authoritative Full candidate if its topology and owner-approved role qualify. The indexed-color favicon is a Reduced concept but needs a supported production source or an explicitly approved construction. A constructed vector master is another option. The choice changes production identity, so Gate 1 must review exact candidates and evidence. A raster trace is not automatically canonical.
3. **Typography remains a proposal**: The live site uses Montserrat headings and Roboto body, but those faces are not presently in the shared font store. Existing locally licensed Poppins and Source Sans 3 are implementation candidates, not approved substitutes. Importing Montserrat or Roboto requires controlled source, hash, and license evidence if chosen.
4. **Third-party affiliation**: Use the existing independent-brand contract with client ownership and no inherited ShruggieTech tokens. The site's service credit is a separate optional choice; omit it from the new kit until explicitly selected.
5. **Publication authorization**: The owner has requested the official brand-site outcome. The repository's exact Gate 1 and Gate 2 creative decisions plus zero-problem verification remain prerequisites; no inferred approval is recorded.

## Open decisions for creative review

- Exact Full and Reduced production master bytes, source mode, and approved transformation set.
- Whether the current tire motif and wordmark are preserved as supplied or revised into a new, explicitly approved identity.
- Exact approved social share slogan, optional description lines, line breaks, and layout.
- Final font families, formal palette, interface cues, applications, and optional service credit.

These are owner decisions, not implementation defaults. Planning can proceed while they remain open; public kit compilation cannot.
