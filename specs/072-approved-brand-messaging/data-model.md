# S072 Data Model

Canonical records remain messaging.slogan, messaging.short_description, and messaging.long_description. Approved records contain status, exact text, uses, source, approved_by, and approved_on. Absent/unresolved records contain only status. No schema change.

The slice's decisions.md stores owner provenance for absence as well as approved text. inventory.md tracks all thirteen brands and pending editorial review. Suggestions remain separate from canonical JSON. A per-role approval changes only that role; explicit absence is not a fallback opportunity.
