# S073 Presentation Model

No persistent domain schema changes in this slice.

## Portfolio section

One section identified by `portfolio`, labeled by the unchanged `portfolio-heading`. Its ordered visible introduction is Selected work, Our Portfolio, and the exact approved identity-spectrum sentence, followed by the brand grid.

## Portfolio title

A title comprises the exact brand name and, for third-party brands, an affiliation marker that links to the shared third-party explanation. The display state is normal size, measured reduced size, or contained wrap. The title may change display state on font availability or width change without changing source text or semantic association.

## Reference entry

Each entry has a stable `REF-*` identifier and heading, followed by Source, Class, Use, and Limit fields in that order. Field values and links are source content. The site may style the unit but must not copy or edit values during publication.

## Invariants

- Names, approved portfolio sentence, reference IDs, field values, and link targets remain byte-for-byte equivalent to the source baseline except Markdown structure needed to separate fields.
- A missing vendor marker stays missing; a present marker retains its accessible explanation.
- The References page is the only documentation page receiving reference-entry styling.
