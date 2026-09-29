# S068 data model

## Essentials projection

An essentials projection is generated from a validated brand source and is copied into the kit portal. It contains `name` (canonical title), `relationship` (existing affiliation wording), `approved_words` (visual-guide-approved identity message roles), `strategy` (visual-guide-approved strategy roles only), `mark_guidance` and `palette_guidance` (existing canonical visual instructions), `type_families` (declared display/body/mono names), and `usage_limits` (literal `logo.prohibitions`). Empty optional values remain absent. The projection does not add an approval state or alter source identity.

## Guide navigation

Each guide renders a list of section descriptors with title and anchor. Optional Approved words and Brand strategy descriptors are present only when their respective source projection is nonempty. Hosted TOC entries are built from the same descriptors that choose rendered sections. Portable guide navigation is built from the actual section list. The PDF page sequence reflects the same concepts but keeps details on their existing dedicated sheets.

## Manual publication display

The docs sidebar presentation reads `publication.status`, `publication.version`, and `publication.releaseUrl` from the generated publication record. Status `release` permits a version label linked to the official release. Status `candidate` produces a compact theme control with no version link. No historical-version entity is created.
