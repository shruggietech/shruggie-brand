# covarity-web UI kit

A single-page specimen of the Covarity evidence workspace, rendered from the shipped
tokens and components rather than from a mockup. Open `index.html` directly; it links
`../../styles.css` and `../../components/components.css`, so any token change shows up
here on reload.

What the page is demonstrating, and why each part is here:

- The scope bar names the vault and the entity, because a screen that does not say
  which vault it is reading is the failure the previous system shipped.
- The evidence table uses `EvidenceRow` at compact density with Geist Mono, so a span
  offset and a confidence figure line up column to column.
- The no-answer block is a first-class state with the same visual weight as an answer.
- The review queue shows a provisional reference held back from canonical publication.
- Purple carries identity, links, focus and selection. Orange appears once, on a
  warning badge in the footer, and never as a second accent.
