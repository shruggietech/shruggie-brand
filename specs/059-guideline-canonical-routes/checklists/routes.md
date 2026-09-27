# Route Contract Requirements Checklist

**Purpose**: Check whether S059 requirements fully describe canonical navigation, compatibility, and publication evidence before final implementation review.

## Canonical navigation

- [x] Does the spec state one rule for the final segment of every menu page, including optional topics and future brands? (FR-001 to FR-003)
- [x] Does it distinguish visible label slugs from stable semantic topic keys? (FR-001, route contract)
- [x] Does it require uniqueness and reject absent or duplicate destinations? (Edge Cases, FR-008)

## Existing links

- [x] Are all three changed legacy page paths named with direct canonical destinations? (US2, route contract)
- [x] Does it distinguish page navigation from direct downloadable files and archives? (FR-004, FR-005)
- [x] Does it state the GitHub Pages status-code limitation and required non-indexable fallback behavior? (Assumptions, research, route contract)

## Published references

- [x] Are menus, breadcrumbs, pagination, search, canonical/social metadata, structured data, robots, and sitemap covered? (FR-006)
- [x] Is the separate `/docs/` manual boundary explicit? (FR-007)
- [x] Are accessibility and full eight-brand validation mandatory? (FR-009, SC-004)

## Notes

All items have testable acceptance in the specification and are assigned implementation and validation tasks. No unresolved owner decision is required to proceed with the static GitHub Pages bridge design.
