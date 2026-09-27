#!/usr/bin/env python3
"""Verify the generated WordPress theme and its installable ZIP against source records."""

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from gen_wordpress import ADAPTER_VERSION, TESTED_PAIRS, WordPressError, dark_variation, require
from interface_contract import load_interface_canon, resolve_interface_contract, skill_metadata


def verify_wordpress(kit_path):
    kit = Path(kit_path)
    brand = json.loads((kit / "brand.json").read_text(encoding="utf-8"))
    slug = brand["slug"]
    root = kit / "wordpress"
    manifest = json.loads((root / "adapter.json").read_text(encoding="utf-8"))
    inventory = json.loads((root / "theme-inventory.json").read_text(encoding="utf-8"))
    support = json.loads((root / "support-matrix.json").read_text(encoding="utf-8"))
    theme = root / "theme" / ("stbb-" + slug)
    archive_path = root / (slug + "-stbb-theme.zip")
    require(manifest["brand"] == slug and manifest["brand_version"] == brand.get("version", "1.0.0"),
            "WordPress manifest brand version disagrees")
    require(manifest["compiler_version"] == skill_metadata()["version"], "WordPress compiler version disagrees")
    require(manifest["interface_canon_version"] == load_interface_canon()["version"], "WordPress interface canon version disagrees")
    require(manifest["adapter_version"] == ADAPTER_VERSION and support["adapter_version"] == ADAPTER_VERSION,
            "WordPress adapter versions disagree")
    require(manifest["tested_pairs"] == TESTED_PAIRS and support["test_targets"] == TESTED_PAIRS,
            "WordPress test target records disagree")
    require(manifest["namespace"] == "stbb-" + slug, "WordPress namespace disagrees")
    expected_entries = {"theme": "wordpress/theme/stbb-%s" % slug,
                        "zip": "wordpress/%s-stbb-theme.zip" % slug,
                        "inventory": "wordpress/theme-inventory.json",
                        "support": "wordpress/support-matrix.json",
                        "theme_json": "wordpress/theme/stbb-%s/theme.json" % slug}
    require(manifest["entries"] == expected_entries, "WordPress adapter entry paths disagree")
    settings = json.loads((theme / "theme.json").read_text(encoding="utf-8"))
    require(settings["version"] == 3 and settings["settings"]["custom"]["stbb"]["brand"] == slug,
            "WordPress theme.json identity or format disagrees")
    palette = settings["settings"]["color"]["palette"]
    names = [item["slug"] for item in palette]
    require(len(names) == len(set(names)) and all(name.startswith("stbb-" + slug + "-") for name in names),
            "WordPress palette contains duplicate or unscoped identifiers")
    roles = json.loads((kit / "color-roles.json").read_text(encoding="utf-8"))
    expected_colors = {"stbb-%s-identity-%s" % (slug, item["id"]): item["hex"] for item in roles["identity"]}
    expected_colors.update({"stbb-%s-cue-%s" % (slug, item["id"]): item["hex"]
                            for item in roles["interface"]["light"]})
    actual_colors = {item["slug"]: item["color"] for item in palette}
    require(all(actual_colors.get(name) == color for name, color in expected_colors.items()),
            "WordPress colors are not source-derived")
    dark = json.loads((theme / "styles" / "dark.json").read_text(encoding="utf-8"))
    require(dark == dark_variation(settings, brand, resolve_interface_contract(brand), roles),
            "WordPress dark variation is not source-derived")
    require(support.get("style_variations") == [{"id": "dark", "path": "styles/dark.json",
                                                  "selection": "Site Editor", "visitor_toggle": False}],
            "WordPress style variation support record disagrees")
    css = (theme / "assets" / "css" / "stbb-content.css").read_text(encoding="utf-8")
    require(".wp-site-blocks" in css and ".editor-styles-wrapper" in css,
            "WordPress supplement does not scope content roots")
    require(not re.search(r"(?:^|\})\s*(?:html|body|#wpadminbar|\.wp-admin)\b", css),
            "WordPress supplement contains an unscoped admin/global selector")
    require("!important" not in css, "WordPress supplement must not override with !important")
    required = {"style.css", "theme.json", "styles/dark.json", "functions.php", "templates/index.html",
                "templates/page.html", "templates/single.html", "templates/archive.html",
                "templates/search.html", "templates/404.html", "parts/header.html", "parts/footer.html",
                "patterns/hero.php", "patterns/text-media.php", "patterns/features.php", "patterns/contact.php"}
    files = {path.relative_to(theme).as_posix(): path for path in theme.rglob("*") if path.is_file()}
    require(required.issubset(files), "WordPress theme omits required templates or patterns")
    for path in files.values():
        require(not path.is_symlink(), "WordPress theme contains a symbolic link")
    recorded = inventory["files"]
    require(inventory["theme_root"] == theme.name, "WordPress inventory root disagrees")
    require(len(recorded) == len(files), "WordPress inventory file count disagrees")
    seen = set()
    for item in recorded:
        relative = item["path"]
        require(relative not in seen and relative in files and ".." not in relative.split("/")
                and not relative.startswith("/"), "WordPress inventory path is unsafe or duplicate")
        seen.add(relative)
        data = files[relative].read_bytes()
        require(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
                "WordPress inventory file hash disagrees: %s" % relative)
    require(seen == set(files), "WordPress inventory omits theme files")
    with zipfile.ZipFile(str(archive_path)) as archive:
        members = archive.infolist()
        names = [item.filename for item in members]
        require(all(name.startswith(theme.name + "/") and ".." not in name.split("/") for name in names),
                "WordPress archive contains an unsafe path")
        require(len(names) == len(set(names)) and len(names) == len(recorded),
                "WordPress archive has duplicate or missing entries")
        require(all(((member.external_attr >> 16) & 0o170000) == 0o100000 for member in members),
                "WordPress archive contains a nonregular entry")
        for item in recorded:
            name = theme.name + "/" + item["path"]
            require(name in names, "WordPress archive omits %s" % name)
            payload = archive.read(name)
            require(len(payload) == item["bytes"] and hashlib.sha256(payload).hexdigest() == item["sha256"],
                    "WordPress archive member disagrees: %s" % name)
    zip_bytes = archive_path.read_bytes()
    require(manifest["zip"] == {"bytes": len(zip_bytes), "sha256": hashlib.sha256(zip_bytes).hexdigest()},
            "WordPress ZIP checksum disagrees")
    for entry in manifest["assets"]:
        source = kit / entry["source"]
        destination = theme / entry["path"]
        require(source.is_file() and destination.is_file() and source.read_bytes() == destination.read_bytes(),
                "WordPress asset differs from kit authority: %s" % entry["path"])
        require(entry["bytes"] == destination.stat().st_size and
                entry["sha256"] == hashlib.sha256(destination.read_bytes()).hexdigest(),
                "WordPress asset checksum disagrees")
    for pattern in (theme / "patterns").glob("*.php"):
        contents = pattern.read_text(encoding="utf-8")
        require("Slug: stbb-%s/" % slug in contents and not re.search(r'\bid\s*=\s*["\']', contents),
                "WordPress pattern has unscoped slug or generated HTML ID: %s" % pattern.name)
    require({item["id"] for item in support["components"]}, "WordPress support matrix is empty")
    return len(files)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify_wordpress.py <kit-dir>")
    try:
        count = verify_wordpress(sys.argv[1])
    except (WordPressError, OSError, KeyError, ValueError, zipfile.BadZipFile) as error:
        print("WordPress verification failed: %s" % error)
        return 1
    print("WordPress verification passed: %d source and archive files" % count)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
