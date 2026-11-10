# S075 Messaging Presentation Contract

S075 supersedes S067's visible role-label requirement only for cover presentation. Approval state, authorized uses, exact wording and independent role identity remain mandatory.

- Cover slogan: approved text, 23pt declared display face/weight, no visible role key.
- Supporting roles: 13.5pt body face, 1.5 leading, foreground on declared ground with measured AA contrast.
- Each role uses `data-message-role`; explicit `data-message-value` content contains only approved copy. Optional reference labels remain separate.
- Missing roles emit no wrapper, placeholder or orphan decoration; legacy brand_idea/descriptor cannot substitute.
- Canonical print HTML retains one exact wrapper per role. Rendering may split that value into ordered DOM continuation fragments; their concatenated text remains exactly equal to the canonical source. Canonical HTML verification rejects duplicate/nested role wrappers; rendered regression checks verify reconstruction and measured bounds.
- Measured layout prevents overlap with logo, footer, other roles and page bounds; overflow uses identified continuation sheets at unchanged readable sizes.
- Portable/hosted reference sections retain useful labels. Opening surfaces are inventoried and any changed responsive surface receives enlargement/reflow checks.
- PDF verification checks exact role content within opening/continuation pages, without requiring visible schema labels. HTML and portal checks independently bind roles to approved source.

Identity geometry, social-image wording/composition and unapproved copy remain outside the presentation change.
