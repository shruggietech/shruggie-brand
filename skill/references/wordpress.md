# WordPress delivery and client handoff

Each verified kit includes `wordpress/adapter.json`, `support-matrix.json`, an installable `*-stbb-theme.zip`, an exact `theme-inventory.json`, and the unpacked theme source in `wordpress/theme/`. The adapter is generated from `brand.json`, resolved interface roles, color roles, the component catalog, and approved kit assets. `theme.json` holds native color, typography, spacing, layout, element, and block defaults. `assets/css/stbb-content.css` covers content focus and media behavior that needs CSS. It is scoped to the rendered site and editor content area.

## Discover the site brief

Ask who the site serves, what visitors need to do, what pages and navigation are required, and who will edit each content type. Record hosting, domain and subdirectory needs, existing content and migration, asset rights, localization, accessibility and performance targets, and whether forms, commerce, a specific builder, or other plugins are actually required. Those answers define client implementation work; the starter does not silently select a plugin stack or lock editing controls.

## Select the package

Pin a complete kit archive and its release checksum first. Within it, confirm the WordPress theme ZIP checksum in `wordpress/adapter.json`. The kit and theme ZIP must come from the same build. Do not use `wordpress/theme/` files from a different kit version or substitute a generated asset by filename. The adapter and compiler have independent versions in `enforcement/consumer-contract.json`; the brand source has its own version. The support matrix lists exact WordPress/PHP fixture pairs and recipe coverage. It does not imply support for every core version, classic theme, builder, plugin, or PHP combination.

## Install a new site

1. Back up the database and WordPress files. On a staging site running a declared core/PHP pair, choose Appearance > Themes > Add New > Upload Theme and install the kit's `wordpress/*-stbb-theme.zip`.
2. Activate the new theme. Open Appearance > Editor and inspect styles, header, footer, navigation, and templates. Upload an approved raster from the kit's `logos/png/` directory into the WordPress Media Library, then select it as Site Logo for a background on which it remains readable. Set the WordPress Site Icon from an approved square raster in the kit's `favicons/` tree. The starter does not turn on unrestricted SVG uploads.
3. Insert the four native patterns (hero, text/media, feature grid, contact action) in pages as needed. The Group block offers a brand-specific Card style. The optional Dark interface variation changes Site Editor theme defaults when selected; it is not a visitor preference switch. Replace demonstration copy, sample email links, and the approved social preview image when client content is ready. When no approved social preview exists, the media pattern uses the approved black mark on a light backing. Save, reopen, and preview each page at narrow and wide widths, with keyboard focus and reduced motion.
4. Test navigation, archive/search/404 pages, images and fonts at the site's actual path, including a subdirectory installation when used. Configure forms, commerce, multilingual support, and other plugins under their own client requirements.

## Ownership and update precedence

The generated theme owns its files: `theme.json`, templates, template parts, patterns, CSS, fonts, licenses, and image assets. The client owns database content: pages, posts, menus/navigation, uploaded media, saved Global Styles, and Site Editor template/part overrides. Effective styling combines WordPress core defaults, parent and optional child theme settings, saved Global Styles, per-block choices, plugin filters, and the theme's scoped supplement. Later or more specific layers can mask a regenerated default; inspect the actual editor and published page before reporting a value as effective. An installed ZIP update therefore changes generated defaults, but does not reset saved edits. Site-specific code belongs in a maintained child theme or other source overlay, not edits to generated files. Approved identity changes return to `brands/<slug>/brand.json` and regenerate the kit; patching the exported theme is not a generator fix.

Before an update, pin the old kit and theme ZIP with checksums, back up the database, export Site Editor customizations where available, and record the current WordPress/PHP versions. The database backup is the recovery authority for styles, templates, parts, navigation, and content. Install the new ZIP on staging, compare its `theme.json` and changed template/pattern files to both the old ZIP and saved database overrides, then record each conflict with its generated default, saved value, decision, and owner. Reconcile deliberately, review edited pages and published output, and only then promote. Update content and media separately from theme files. To roll back, reinstall the pinned old ZIP and restore the matching database backup if saved overrides or content were changed. A ZIP rollback alone cannot revert database edits.

## Support boundaries

The generated starter uses core block-theme facilities and no required plugin, external font service, React runtime, or remote image host. The support matrix classifies each component recipe as adapted or unsupported and names the native core blocks used. Core `wp:group`, `wp:columns`, `wp:button`, `wp:query`, navigation, and image markup is editable in the Site Editor. The generated stylesheet does not style WordPress admin chrome.

| Target | Status | Next step |
| --- | --- | --- |
| Native block theme and Site Editor | Tested only on the exact WordPress/PHP pairs in `adapter.json` | Install the generated ZIP and validate the client's actual URL, content, and hosting. |
| Existing compatible block theme | Manual integration guidance, unverified as an automatic install | Merge selected `theme.json` settings and scoped CSS in maintained source, then test override precedence. |
| Classic themes and page builders | Unverified | Scope and implement a separate integration when the client requires one. |
| Forms, WooCommerce, multilingual, caching, or optimization plugins | Unverified | Choose the client-required plugin and test its templates, assets, and editor interaction before claiming support. |
