# End-to-end validation guide

1. Run focused documentation contract, citation, generator, and site-preparation tests. Confirm a missing reference ID or altered facts byte is rejected.
2. Build all eight production kits in an ignored output directory. Run `verify.py` and `validate_glyph.py` on every kit; both must report zero failures.
3. Prepare and export the site from those verified kits. Confirm `/docs/references/` participates in navigation and static search and each `/{brand}/facts/documentation.json` equals the corresponding kit source.
4. Run browser tests for topic navigation, descriptive links, heading order, keyboard focus, 200% zoom, and narrow reflow. Walk representative reader tasks for a default interface, override, registry, asset download, package authority, and future platform guidance.
5. Run the full documented CI-equivalent validation and publication audit. Record exact commands, results, skips, and any live external link review in `verification.md`.

Generated files remain under ignored build directories. The PR is ready for owner review only after required CI and external review dispositions are complete.
