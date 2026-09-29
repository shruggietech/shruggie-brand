# Guide field-to-kit-source map

This map applies to all eleven production brands. The [migration inventory](migration-inventory.md) lists each brand's exact legacy text and classification. PDF and portable HTML are generated from the kit's brand.json and assets; the hosted guide consumes the kit's guidelines/portal.json.

| Output and role | Canonical source | Empty behavior and verification |
| --- | --- | --- |
| Cover and introduction title | brand.json.title | Required factual identity; same title in PDF, portable, and hosted |
| Cover/portable/hosted slogan | brand.json.messaging.slogan with visual-guide use | Omit if absent or unresolved; exact text and Slogan label checked |
| Short and long descriptions | Matching brand.json.messaging role with visual-guide use | Independent states; never use descriptor or idea; exact text and role checked |
| Introduction and optional strategy roles | Matching brand.json.messaging role with visual-guide use | Omit unless explicitly approved for the surface |
| Social share image | brand.json.social_copy and social_image_approval | Existing separate approval; exact slogan equality if messaging grants social-image use |
| Site metadata and consumer brand list | brand.json.messaging filtered by site-metadata or consumer-data use | Emit exact text in separate approvedMessaging and consumerMessaging records; unresolved roles omitted |
| PDF cover lockup | Kit logos/png horizontal delivery, from approved Full/Reduced source | Manifest path and digest, identity continuity, and approval checks |
| PDF name section | brand.json.title, affiliation, register, guidance.name_story/written_form/named | Missing optional guidance omitted; no synthesized name story or written form |
| Personality, promises, boundaries | brand.json.guidance.personality/promises/sharp_edge and source affiliation | Missing items omitted, never generic brand promises |
| Logo usage | brand.json.guidance.logo, brand.json.logo metrics/prohibitions, shipped logo assets | No guide-only override; source and manifest checks |
| Palette and semantic use | brand.json.guidance.palette, color_roles, measured token outputs | Kit values and contrast checks, with shared template explanation |
| Typography and specimen | brand.json.typography, approved visual-guide messages or neutral type sample | Missing messages use brand title or neutral sample, never legacy idea or descriptor |
| Components | brand.json.domain_components and generated component recipes | Exact source field names; kit bindings checked |
| Portable and hosted integration | Kit enforcement/documentation-facts.json, delivery manifests, generated instructions | Portal and hosted page use pinned kit facts and paths |
| Shared system explanations | Shipped build templates and system manual/reference files | One common maintained source, no per-brand fallback claim |

## Per-brand decision state at S067 intake

| Brand | General visual-guide slogan | Short description | Long description | Legacy guidance source |
| --- | --- | --- | --- | --- |
| covarity | unresolved | unresolved | unresolved | historical source |
| cueson | unresolved | unresolved | unresolved | Gate 2 guide surface |
| dancewithme865 | unresolved | unresolved | unresolved | Gate 2 guide surface |
| eso-weave | unresolved | unresolved | unresolved | Gate 2 guide surface |
| fragcap | unresolved | unresolved | unresolved | historical source |
| glitchpad | unresolved | unresolved | unresolved | historical source |
| go-schedule | unresolved | unresolved | unresolved | historical source |
| i-heart-pr-tours | unresolved | unresolved | unresolved | Gate 2 guide surface |
| local-companion | unresolved | unresolved | unresolved | Gate 2 guide surface |
| scruggs-tire-alignment | unresolved | unresolved | unresolved | Gate 2 guide surface |
| shruggietech | approved exact text per #295 | unresolved | unresolved | historical source |

An unresolved role is intentionally absent from public guide message sections. This is an honest classification of existing evidence, not a new owner decision. Root descriptor and brand_idea fields remain in source for legacy consumers until those consumers can migrate; guides do not display them as approved slogan or description.
