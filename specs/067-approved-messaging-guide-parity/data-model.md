# Data Model

## Message decision

messaging.<role> is independent for slogan, short_description, long_description, introductory_statement, positioning, mission, vision, values, and brand_promise. Each declares status approved, absent, or unresolved. Approved records contain exact nonempty text, nonempty uses, source, approved_by, and approved_on. Absent records contain only status and optional reason. Unresolved records may retain private candidate evidence but cannot project publicly. No role supplies another.

## Social composition

Existing social_copy remains independently approved. If messaging.slogan lists social-image, its text must exactly match social_copy.slogan. Social approval alone does not grant visual-guide use.

## Legacy inventory

Each item identifies brand slug, original path, exact value, current role, evidence, and disposition. Unresolved means owner decision is missing. Inventory is review evidence, never a public copy source.

## Guide projection

Each output has a source path, role, and use. The renderer selects only approved decisions for that use. Missing roles omit the section. Assets resolve to manifest deliveries and retain identity.
