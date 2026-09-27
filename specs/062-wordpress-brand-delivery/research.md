# Research and decisions: WordPress brand delivery

## Sources reviewed on 2026-09-27

- [WordPress 7.1.2 release](https://wordpress.org/news/2026/09/wordpress-7-1-2-release/) identifies the current stable core release.
- [Theme structure](https://developer.wordpress.org/themes/core-concepts/theme-structure/) requires `style.css` and `templates/index.html` for a block theme; `theme.json` is the native settings/style contract.
- [theme.json version 3 reference](https://developer.wordpress.org/block-editor/reference-guides/theme-json-reference/theme-json-living/) identifies version 3 and version-specific schemas under `schemas.wp.org/wp/{version}/theme.json`. The moving trunk schema cannot certify a pinned core fixture.
- [Typography](https://developer.wordpress.org/themes/global-settings-and-styles/settings/typography/) specifies bundled font references as `file:./...`.
- [wp-env](https://developer.wordpress.org/block-editor/reference-guides/packages/packages-env/) supports pinned core and PHP versions, installed themes, and CLI commands in Docker fixtures.
- [Template hierarchy](https://developer.wordpress.org/themes/templates/template-hierarchy/) places saved database templates before child-theme and theme files.
- [Global Settings and Styles](https://developer.wordpress.org/themes/global-settings-and-styles/) explains native settings/styles and user override hierarchy.

## Decisions

| Question | Decision | Reason |
| --- | --- | --- |
| Native baseline | Core block theme, no required plugin | Matches the owner-approved baseline and lets editor and front end consume one `theme.json`. |
| Versions | Minimum fixture WordPress 6.9.9 with PHP 8.2; current fixture WordPress 7.1.2 with PHP 8.3 | Two pinned core/PHP pairs, including current stable, avoid claiming every intermediate combination. Support record stays evidence based. |
| Namespace | `stbb-<full-brand-slug>-` for adapter-owned identifiers, `stbb-` for shared symbols | The full slug avoids two-character collisions. CSS selectors remain scoped to content roots; prefix alone is not isolation. |
| Colors | Formal identity palette and interface cue palette use separate slug groups, both sourced from resolved contracts | Keeps approved identity and functional cues distinct and preserves independent palettes. |
| Supplement | Native settings/styles set site-wide defaults; only content-specific focus, responsive and block-state behavior goes in supplemental CSS | WordPress can merge file and saved styles. No global reset or admin-chrome selectors. |
| Assets | Copy license-qualified WOFF2 and approved raster logo alternatives from generated kit; retain SVG source in parent kit | WordPress media uploads do not require unrestricted SVG capability. Exact path data remains untouched. |
| Theme packaging | Deterministic `wordpress/<slug>-stbb-theme.zip` plus inspectable `wordpress/theme/` and SHA-256 inventory | Installable artifact and source map are independently verifiable; no generated output is committed. |
| Client changes | Keep posts/pages and saved Global Styles/template overrides in WordPress; document export and drift inspection before package replacement | Updating generated files must not silently delete database state or imply file defaults are effective. |
| Runtime evidence | A pinned Docker-backed `wp-env` CI job installs the ZIP, activates it, exercises WP-CLI and editor/front-end endpoints, and records versions | Static schema checks and CSS text inspection alone cannot establish installability or editor behavior. |

## Alternatives rejected

- Importing `gen_vanilla.py` CSS wholesale would bring global resets and unscoped element styles into WordPress.
- A standalone JSON fragment without a theme ZIP would leave issue #274 unfinished.
- A generic two-character namespace would collide for brands with matching initial letters.
- Theme style variations are editor selections; S062 does not present them as an automatic visitor toggle.
