# Data Model: Dependency Release Intake

- **Intake row**: Pull request number, package or action, previous version, target version, target immutable revision when applicable, and disposition.
- **Source contract**: One expected immutable revision and one accurate upstream version comment for each external workflow action; duplicate uses must agree.
- **Release candidate**: Combined dependency source revision with full kit, site, accessibility, and publication evidence.
- **Release outcome**: Exact merged main commit, `v2.0.1` tag, verified asset inventory and checksums, and Pages deployment.

No application schema or persisted runtime data changes.
