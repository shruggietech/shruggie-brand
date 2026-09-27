#!/usr/bin/env python3
"""Generate a native WordPress adapter and installable block-theme starter."""

import hashlib
import html
import json
import copy
import re
import shutil
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from brand_contract import font_faces
from component_contract import load_component_catalog
from interface_contract import resolve_interface_contract, skill_metadata


ADAPTER_VERSION = "1.0.0"
TESTED_PAIRS = [
    {"wordpress": "6.9.9", "php": "8.2"},
    {"wordpress": "7.1.2", "php": "8.3"},
]
SLUG = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")


class WordPressError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise WordPressError(message)


def write_text(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def write_json(path, value):
    write_text(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def digest(path):
    payload = path.read_bytes()
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def css_value(value):
    if isinstance(value, (int, float)):
        return "%gpx" % value
    return str(value)


def font_records(kit, theme, brand):
    declared = font_faces(brand)
    require(declared, "WordPress font source has no approved local faces")
    assets = []
    result = []
    for role in ("display", "body", "mono"):
        declaration = brand["typography"]["families"][role]
        family = declaration["name"]
        available = []
        for weight in declaration["weights"]:
            options = [face for face in declared if face["role"] == role and face["weight"] == weight
                       and face["format"] in ("woff2", "ttf", "otf")]
            options.sort(key=lambda face: (0 if face["format"] == "woff2" else 1, face["path"]))
            require(options, "WordPress font weights are unavailable: %s %s" % (family, weight))
            face = options[0]
            source_relative = Path(face["path"])
            require(source_relative.parts[0] == "fonts" and ".." not in source_relative.parts
                    and not source_relative.is_absolute(), "WordPress font source path is unsafe")
            source = kit / source_relative
            require(source.is_file() and source.stat().st_size > 0 and not source.is_symlink(),
                    "WordPress font asset is missing: %s" % face["path"])
            if face.get("sha256"):
                require(digest(source)["sha256"] == face["sha256"], "WordPress font source checksum disagrees")
            destination = theme / "assets" / "fonts" / Path(*source_relative.parts[1:])
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            asset = {"source": source.relative_to(kit).as_posix(), "path": destination.relative_to(theme).as_posix(), **digest(destination)}
            if asset not in assets:
                assets.append(asset)
            available.append({"fontFamily": family, "fontStyle": face["style"],
                              "fontWeight": str(weight), "src": ["file:./" + destination.relative_to(theme).as_posix()]})
        license_key = next((name for name in ("Space-Grotesk", "Source-Sans-3", "Poppins", "Geist", "Courier-Prime")
                            if name.lower().replace("-", "") in family.lower().replace(" ", "")), None)
        choices = ([kit / "fonts" / "licenses" / ("OFL-%s.txt" % license_key)] if license_key else []) + [
            kit / "fonts" / ("OFL-%s.txt" % family.replace(" ", "-")), kit / "fonts" / "OFL.txt"]
        license_source = next((path for path in choices if path.is_file() and family.lower().split()[0] in path.read_text(encoding="utf-8").lower()), None)
        require(license_source is not None, "WordPress font license is missing: %s" % family)
        license_target = theme / "assets" / "licenses" / license_source.name
        license_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(license_source, license_target)
        license_asset = {"source": license_source.relative_to(kit).as_posix(),
                         "path": license_target.relative_to(theme).as_posix(), **digest(license_target)}
        if license_asset not in assets:
            assets.append(license_asset)
        result.append({"fontFamily": family, "name": family, "slug": "stbb-%s" % role, "fontFace": available})
    return result, assets


def theme_settings(brand, interface, color_roles, fonts):
    slug = brand["slug"]
    prefix = "stbb-%s" % slug
    identity = color_roles["identity"]
    cues = color_roles["interface"]["light"]
    require(identity and cues, "WordPress requires resolved identity and cue colors")
    palette = ([{"name": "Identity: %s" % item["label"], "slug": "%s-identity-%s" % (prefix, item["id"]), "color": item["hex"]} for item in identity] +
               [{"name": "Interface: %s" % item["label"], "slug": "%s-cue-%s" % (prefix, item["id"]), "color": item["hex"]} for item in cues])
    roles = interface["roles_by_theme"]["light"]
    for key, label in (("surface.background", "Background"), ("surface.card", "Card"),
                       ("text.primary", "Text"), ("text.muted", "Muted text"),
                       ("focus.ring", "Focus")):
        palette.append({"name": "Interface: %s" % label, "slug": "%s-%s" % (prefix, key.replace(".", "-")), "color": roles[key]})
    names = {entry["slug"] for entry in palette}
    require(len(names) == len(palette), "WordPress palette slugs collide")
    def preset(name):
        return "var:preset|color|%s-%s" % (prefix, name)
    spacing = [{"name": "Space %s" % value, "slug": "%s-space-%s" % (prefix, value), "size": "%spx" % size}
               for value, size in (("1", 4), ("2", 8), ("3", 12), ("4", 16), ("6", 24), ("8", 32), ("12", 48), ("16", 64))]
    return {
        "$schema": "https://schemas.wp.org/wp/6.9/theme.json",
        "version": 3,
        "settings": {
            "appearanceTools": True,
            "color": {"palette": palette, "defaultPalette": False},
            "typography": {"fontFamilies": fonts},
            "spacing": {"spacingSizes": spacing},
            "layout": {"contentSize": "%spx" % roles["layout.narrow.max"],
                       "wideSize": "%spx" % roles["layout.content.max"]},
            "custom": {"stbb": {"brand": slug, "adapterVersion": ADAPTER_VERSION}},
        },
        "styles": {
            "color": {"background": preset("surface-background"), "text": preset("text-primary")},
            "typography": {"fontFamily": "var:preset|font-family|stbb-body"},
            "spacing": {"blockGap": "%spx" % roles["spacing.component"]},
            "elements": {
                "link": {"color": {"text": preset("cue-action")}},
                "button": {"color": {"background": preset("cue-action"),
                                      "text": next(item["foreground"] for item in cues if item["id"] == "action")},
                           "border": {"radius": "%spx" % roles["spacing.control.inline"]}},
                "heading": {"typography": {"fontFamily": "var:preset|font-family|stbb-display"}},
            },
            "blocks": {
                "core/group": {"spacing": {"blockGap": "%spx" % roles["spacing.component"]}},
                "core/columns": {"spacing": {"blockGap": "%spx" % roles["spacing.component"]}},
            },
        },
    }


def dark_variation(base, brand, interface, color_roles):
    """Use the same semantic slugs with the approved dark interface values."""
    dark = copy.deepcopy(base)
    dark["title"] = "Dark interface"
    slug = brand["slug"]
    prefix = "stbb-%s" % slug
    roles = interface["roles_by_theme"]["dark"]
    cues = color_roles["interface"]["dark"]
    for item in dark["settings"]["color"]["palette"]:
        name = item["slug"]
        for cue in cues:
            if name == "%s-cue-%s" % (prefix, cue["id"]):
                item["color"] = cue["hex"]
        for role in ("surface.background", "surface.card", "text.primary", "text.muted", "focus.ring"):
            if name == "%s-%s" % (prefix, role.replace(".", "-")):
                item["color"] = roles[role]
    dark["styles"]["elements"]["button"]["color"]["text"] = next(
        item["foreground"] for item in cues if item["id"] == "action")
    return dark


def content_css(brand, interface):
    slug = brand["slug"]
    roles = interface["roles_by_theme"]["light"]
    focus = "var(--wp--preset--color--stbb-%s-focus-ring)" % slug
    width = css_value(roles["focus.width"])
    offset = css_value(roles["focus.offset"])
    return ("/* Generated content-only supplement. Theme defaults live in theme.json. */\n"
            ":is(.wp-site-blocks, .editor-styles-wrapper) :is(a, button, .wp-element-button, input, select, textarea):focus-visible {\n"
            "  outline: %s solid %s; outline-offset: %s;\n}\n" % (width, focus, offset) +
            ":where(.wp-site-blocks, .editor-styles-wrapper) :where(.wp-block-image img, .wp-block-site-logo img) { max-inline-size: 100%; block-size: auto; }\n" +
            ":where(.wp-site-blocks, .editor-styles-wrapper) .stbb-%s-sample-media img { inline-size: min(28rem, 100%%); }\n" % slug +
            ":where(.wp-site-blocks, .editor-styles-wrapper) .stbb-%s-sample-mark { background: #fff; padding: var(--wp--preset--spacing--stbb-%s-space-4); }\n" % (slug, slug) +
            ":where(.wp-site-blocks, .editor-styles-wrapper) .stbb-%s-sample-mark img { inline-size: min(12rem, 100%%); }\n" % slug +
            ":where(.wp-site-blocks, .editor-styles-wrapper) :where(.wp-element-caption) { color: var(--wp--preset--color--stbb-%s-text-muted); }\n" % slug +
            ":where(.wp-site-blocks, .editor-styles-wrapper) .wp-block-group.is-style-stbb-%s-card { background: var(--wp--preset--color--stbb-%s-surface-card); color: var(--wp--preset--color--stbb-%s-text-primary); border: %spx solid var(--wp--preset--color--stbb-%s-text-muted); border-radius: var(--wp--preset--spacing--stbb-%s-space-2); padding: var(--wp--preset--spacing--stbb-%s-space-6); }\n" % (slug, slug, slug, roles["border.default"], slug, slug, slug) +
            ":where(.wp-site-blocks, .editor-styles-wrapper) :where(.wp-block-navigation, .wp-block-columns, .wp-block-group, .wp-block-post-content) { min-inline-size: 0; overflow-wrap: anywhere; }\n"
            ":where(.wp-site-blocks, .editor-styles-wrapper) :where(.wp-block-button__link) { min-block-size: 44px; display: inline-flex; align-items: center; }\n"
            "@media (prefers-reduced-motion: reduce) { :where(.wp-site-blocks, .editor-styles-wrapper) * { scroll-behavior: auto; animation-duration: 0.01ms; transition-duration: 0.01ms; } }\n")


def block(text):
    return "<!-- wp:paragraph --><p>%s</p><!-- /wp:paragraph -->" % html.escape(text)


def templates(theme):
    header = ('<!-- wp:group {"tagName":"header","layout":{"type":"constrained"}} -->'
              '<header class="wp-block-group"><!-- wp:site-logo {"width":64} /-->'
              '<!-- wp:site-title /--><!-- wp:navigation {"overlayMenu":"mobile"} --><!-- wp:home-link {"label":"Home"} /--><!-- /wp:navigation --></header><!-- /wp:group -->\n')
    footer = ('<!-- wp:group {"tagName":"footer","layout":{"type":"constrained"}} -->'
              '<footer class="wp-block-group"><!-- wp:site-title /--></footer><!-- /wp:group -->\n')
    write_text(theme / "parts" / "header.html", header)
    write_text(theme / "parts" / "footer.html", footer)
    top = '<!-- wp:template-part {"slug":"header"} /-->\n'
    bottom = '<!-- wp:template-part {"slug":"footer"} /-->\n'
    def layout(body):
        return top + '<!-- wp:group {"tagName":"main","layout":{"type":"constrained"}} --><main class="wp-block-group">' + body + '</main><!-- /wp:group -->\n' + bottom
    entries = {
        "index": '<!-- wp:query {"query":{"perPage":10,"postType":"post"}} --><div class="wp-block-query"><!-- wp:post-template --><!-- wp:post-title {"isLink":true} /--><!-- wp:post-excerpt /--><!-- /wp:post-template --><!-- wp:query-no-results -->' + block("No posts found.") + '<!-- /wp:query-no-results --></div><!-- /wp:query -->',
        "page": '<!-- wp:post-title {"level":1} /--><!-- wp:post-content /-->',
        "single": '<!-- wp:post-title {"level":1} /--><!-- wp:post-date /--><!-- wp:post-content /-->',
        "archive": '<!-- wp:query-title {"type":"archive"} /--><!-- wp:query {"query":{"inherit":true}} --><div class="wp-block-query"><!-- wp:post-template --><!-- wp:post-title {"isLink":true} /--><!-- wp:post-excerpt /--><!-- /wp:post-template --><!-- wp:query-no-results -->' + block("No posts found in this archive.") + '<!-- /wp:query-no-results --></div><!-- /wp:query -->',
        "search": '<!-- wp:query-title {"type":"search"} /--><!-- wp:search {"label":"Search","showLabel":false} /--><!-- wp:query {"query":{"inherit":true}} --><div class="wp-block-query"><!-- wp:post-template --><!-- wp:post-title {"isLink":true} /--><!-- wp:post-excerpt /--><!-- /wp:post-template --><!-- wp:query-no-results -->' + block("No matching results. Try another search.") + '<!-- /wp:query-no-results --></div><!-- /wp:query -->',
        "404": '<!-- wp:heading {"level":1} --><h1>Page not found</h1><!-- /wp:heading -->' + block("The requested page could not be found.") + '<!-- wp:search {"label":"Search","showLabel":false} /-->',
    }
    for name, body in entries.items():
        write_text(theme / "templates" / (name + ".html"), layout(body) + "\n")


def patterns(theme, brand, sample_image):
    title = html.escape(brand["title"])
    description = html.escape(brand.get("descriptor") or brand.get("functional_descriptor") or "Explore our work.")
    image_class = "stbb-%s-%s" % (brand["slug"], "sample-media" if "social-preview" in sample_image else "sample-mark")
    image_alt = "%s brand preview" if "social-preview" in sample_image else "%s mark"
    approved_image = ('<!-- wp:image {"sizeSlug":"full","linkDestination":"none","className":"%s"} -->'
                      '<figure class="wp-block-image size-full %s"><img src="<?php echo esc_url( get_theme_file_uri( \'assets/images/%s\' ) ); ?>" alt="%s"/></figure><!-- /wp:image -->'
                      % (image_class, image_class, sample_image, image_alt % title))
    records = {
        "hero": ("Hero with action", "Lead with a clear introduction and action.",
                 '<!-- wp:group {"layout":{"type":"constrained"}} --><div class="wp-block-group"><!-- wp:heading --><h2>%s</h2><!-- /wp:heading --><!-- wp:paragraph --><p>%s</p><!-- /wp:paragraph --><!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button --><div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="mailto:hello@example.com">Get in touch</a></div><!-- /wp:button --></div><!-- /wp:buttons --></div><!-- /wp:group -->' % (title, description)),
        "text-media": ("Text and media", "Pair editable text with an image.",
                       '<!-- wp:columns --><div class="wp-block-columns"><!-- wp:column --><div class="wp-block-column"><!-- wp:heading --><h2>Tell your story</h2><!-- /wp:heading -->' + block("Replace this text with your own message.") + '</div><!-- /wp:column --><!-- wp:column --><div class="wp-block-column">' + approved_image + '</div><!-- /wp:column --></div><!-- /wp:columns -->'),
        "features": ("Feature or service grid", "Describe three useful offerings.",
                     '<!-- wp:columns --><div class="wp-block-columns">' + ''.join('<!-- wp:column --><div class="wp-block-column"><!-- wp:heading {"level":3} --><h3>Service %d</h3><!-- /wp:heading -->%s</div><!-- /wp:column -->' % (i, block("Describe a benefit.")) for i in (1, 2, 3)) + '</div><!-- /wp:columns -->'),
        "contact": ("Contact action", "Invite a clear next step without assuming a forms plugin.",
                    '<!-- wp:group {"layout":{"type":"constrained"}} --><div class="wp-block-group"><!-- wp:heading --><h2>Get in touch</h2><!-- /wp:heading -->' + block("Use your published contact details here.") + '<!-- wp:buttons --><div class="wp-block-buttons"><!-- wp:button --><div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="mailto:hello@example.com">Email us</a></div><!-- /wp:button --></div><!-- /wp:buttons --></div><!-- /wp:group -->'),
    }
    for name, (label, description, markup) in records.items():
        source = "<?php\n/**\n * Title: %s\n * Slug: stbb-%s/%s\n * Description: %s\n * Categories: featured\n */\n?>\n%s\n" % (label, brand["slug"], name, description, markup)
        write_text(theme / "patterns" / (name + ".php"), source)


def zip_theme(theme, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    records = []
    with zipfile.ZipFile(str(target), "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(theme.rglob("*")):
            if path.is_dir():
                continue
            require(path.is_file() and not path.is_symlink(), "WordPress theme contains an unsafe entry")
            relative = path.relative_to(theme).as_posix()
            require(relative and ".." not in relative.split("/"), "WordPress theme contains an unsafe path")
            data = path.read_bytes()
            require(data, "WordPress theme contains an empty file: %s" % relative)
            info = zipfile.ZipInfo(theme.name + "/" + relative, (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            records.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    return records


def generate_wordpress(brand_source, kit_path):
    kit = Path(kit_path)
    brand = json.loads(Path(brand_source).read_text(encoding="utf-8"))
    slug = brand["slug"]
    require(SLUG.fullmatch(slug), "WordPress brand slug is invalid")
    color_roles = json.loads((kit / "color-roles.json").read_text(encoding="utf-8"))
    interface = resolve_interface_contract(brand)
    root = kit / "wordpress"
    if root.exists() or root.is_symlink():
        require(root.is_dir() and not root.is_symlink(), "WordPress output root is unsafe")
        shutil.rmtree(root)
    theme = root / "theme" / ("stbb-" + slug)
    theme.mkdir(parents=True, exist_ok=True)
    fonts, font_assets = font_records(kit, theme, brand)
    image_assets = []
    probe_path = kit / "qc" / "probe.json"
    raster_available = (json.loads(probe_path.read_text(encoding="utf-8")).get("svg_raster", True)
                        if probe_path.is_file() else True)
    extension = "png" if raster_available else "svg"
    mark_image = "%s-mark-black-1024.png" % slug if raster_available else "%s-mark-black.svg" % slug
    sample_image = "%s-social-preview-1280.png" % slug if raster_available else "%s-social-preview.svg" % slug
    logo_source = kit / "logos" / extension
    has_social_preview = (logo_source / sample_image).is_file()
    names = (["%s-horizontal-black-1024.png" % slug, mark_image] if raster_available
             else ["%s-horizontal-black.svg" % slug, mark_image])
    if has_social_preview:
        names.append(sample_image)
    for filename in names:
        source = logo_source / filename
        require(source.is_file() and not source.is_symlink(),
                "WordPress approved %s asset is missing: %s" % ("raster" if raster_available else "vector", filename))
        if raster_available:
            require(source.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"),
                    "WordPress approved raster asset is missing: %s" % filename)
        else:
            try:
                root_element = ElementTree.parse(str(source)).getroot()
            except ElementTree.ParseError as error:
                raise WordPressError("WordPress generated vector asset is invalid: %s" % filename) from error
            require(root_element.tag == "{http://www.w3.org/2000/svg}svg",
                    "WordPress generated vector asset is invalid: %s" % filename)
        destination = theme / "assets" / "images" / filename
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        image_assets.append({"source": source.relative_to(kit).as_posix(),
                             "path": destination.relative_to(theme).as_posix(), **digest(destination)})
    settings = theme_settings(brand, interface, color_roles, fonts)
    write_json(theme / "theme.json", settings)
    write_json(theme / "styles" / "dark.json", dark_variation(settings, brand, interface, color_roles))
    write_text(theme / "style.css", "/*\nTheme Name: %s Brand Starter\nTheme URI: https://brand.shruggie.tech/%s/\nAuthor: ShruggieTech\nDescription: Generated native block-theme foundation for %s.\nVersion: %s\nRequires at least: 6.9\nRequires PHP: 8.2\nLicense: Apache-2.0\nText Domain: stbb-%s\n*/\n" % (brand["title"], slug, brand["title"], ADAPTER_VERSION, slug))
    stylesheet = theme / "assets" / "css" / "stbb-content.css"
    write_text(stylesheet, content_css(brand, interface))
    stylesheet_version = digest(stylesheet)["sha256"]
    write_text(theme / "functions.php", "<?php\n/** Generated content-only stylesheet hooks. */\nadd_action( 'after_setup_theme', function () { add_theme_support( 'editor-styles' ); add_editor_style( 'assets/css/stbb-content.css' ); } );\nadd_action( 'init', function () { register_block_style( 'core/group', array( 'name' => 'stbb-%s-card', 'label' => 'Brand card' ) ); } );\nadd_action( 'wp_enqueue_scripts', function () { wp_enqueue_style( 'stbb-%s-content', get_theme_file_uri( 'assets/css/stbb-content.css' ), array(), '%s' ); } );\n" % (slug, slug, stylesheet_version))
    templates(theme)
    patterns(theme, brand, sample_image if has_social_preview else mark_image)
    write_text(theme / "README.md", "# %s WordPress starter\n\nGenerated by BrandBuilder. Install this ZIP through Appearance > Themes, activate, upload an approved PNG for Site Logo, choose navigation, and replace demonstration copy. Source SVG logo geometry remains in the parent brand kit; do not enable unrestricted SVG uploads merely for this theme. Before updating, back up the database and export Site Editor customizations, then compare saved overrides with the new theme defaults on staging. Keep the previous ZIP and its checksum for rollback. See https://brand.shruggie.tech/docs/wordpress/ and the parent kit's `wordpress/README.md` for the supported versions and complete handoff.\n" % brand["title"])
    inventory = zip_theme(theme, root / (slug + "-stbb-theme.zip"))
    write_json(root / "theme-inventory.json", {"schema_version": 1, "theme_root": theme.name, "files": inventory})
    catalog = load_component_catalog()
    supported = {"Button": "core/button", "Card": "core/group", "EmptyState": "core/query-no-results"}
    support = {"schema_version": 1, "adapter_version": ADAPTER_VERSION,
               "test_targets": TESTED_PAIRS,
               "style_variations": [{"id": "dark", "path": "styles/dark.json", "selection": "Site Editor", "visitor_toggle": False}],
               "components": [{"id": name, "status": "adapted" if name in supported else "unsupported",
                               "core_block": supported.get(name),
                               "reason": ("Implemented with native core block markup and theme styles" if name in supported
                                          else "No equivalent core block behavior is implemented in this starter")}
                              for name in sorted(catalog["components"])],
               "core_blocks": {name: "native" for name in ("core/paragraph", "core/heading", "core/button", "core/group", "core/columns", "core/image", "core/navigation", "core/query", "core/search")},
               "scope": ["front-end-content", "block-editor-content"],
               "unverified": ["classic themes", "page builders", "forms", "commerce", "multilingual plugins", "caching plugins"]}
    write_json(root / "support-matrix.json", support)
    metadata = skill_metadata()
    manifest = {"schema_version": 1, "adapter_version": ADAPTER_VERSION, "brand": slug,
                "brand_version": brand.get("version", "1.0.0"), "compiler_version": metadata["version"],
                "interface_canon_version": interface["interface_canon_version"],
                "component_recipe_version": catalog["version"],
                "theme_json_version": 3, "tested_pairs": TESTED_PAIRS,
                "namespace": "stbb-%s" % slug,
                "entries": {"theme": "wordpress/theme/%s" % theme.name,
                            "zip": "wordpress/%s-stbb-theme.zip" % slug,
                            "inventory": "wordpress/theme-inventory.json",
                            "support": "wordpress/support-matrix.json",
                            "theme_json": "wordpress/theme/%s/theme.json" % theme.name},
                "zip": digest(root / (slug + "-stbb-theme.zip")),
                "assets": font_assets + image_assets}
    write_json(root / "adapter.json", manifest)
    logo_guidance = ("Set Site Logo with `theme/%s/assets/images/%s` or another approved PNG variant in the parent kit." % (theme.name, mark_image)
                     if raster_available else "This core-tier kit contains vector theme assets only; export an approved PNG before uploading a Site Logo to the media library.")
    write_text(root / "README.md", "# %s WordPress delivery\n\nInstall `%s-stbb-theme.zip` on the exact WordPress/PHP pairs listed in `adapter.json`. Use native Site Editor blocks and the four patterns. %s The theme uses native settings for defaults and a content-scoped CSS supplement. It does not style the WordPress admin chrome. The optional Dark interface style variation is selected by an editor and does not switch with a visitor preference.\n\nBefore updating, back up the database and export saved Global Styles, templates, template parts, navigation, pages, and posts. Pin the current ZIP and its checksum. Install the new ZIP in a staging site, compare its `theme.json` against saved Site Editor overrides, and reconcile intentionally. Saved database styles and templates can mask regenerated file defaults; replacing a ZIP does not delete client content or force those defaults. Roll back with the pinned ZIP plus database backup if necessary. Use a child theme or maintained source overlay for client code changes, rather than editing generated files. Classic themes and third-party builders, forms, commerce, multilingual, and caching plugins are unverified until tested for a client.\n" % (brand["title"], slug, logo_guidance))
    return manifest


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: gen_wordpress.py <brand.json> <kit-dir>")
    generate_wordpress(sys.argv[1], sys.argv[2])
    print("generated WordPress theme in %s" % (Path(sys.argv[2]) / "wordpress"))


if __name__ == "__main__":
    main()
