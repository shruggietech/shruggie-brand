#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Overlay approved platform icon bytes after capability-routed generation."""

import json
import shutil
import sys
from pathlib import Path

from brand_contract import (_supplied_icon_target_dimensions, application_icon_profile,
                            contained_path, load_brand, sha256_file)


def write_json(path, value):
    with open(str(path), "w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, indent=2)
        handle.write("\n")


def platform_for(target):
    if target.startswith("icons/web/"):
        return "web"
    if target.startswith("icons/android/"):
        return "android"
    if target.startswith("icons/apple/ios/"):
        return "apple-ios"
    if target.startswith("icons/apple/macos/"):
        return "apple-macos"
    return "windows"


def apply_supplied_targets(brand, kit):
    """Copy source-preserved targets even when raster generation was skipped."""
    kit = Path(kit).resolve()
    manifest_path = contained_path(kit, "icons/manifest.json")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError("icons/manifest.json artifacts must be an array")
    by_path = {item.get("path"): item for item in artifacts if isinstance(item, dict)}
    suites = manifest.get("suites")
    if not isinstance(suites, list):
        raise ValueError("icons/manifest.json suites must be an array")

    for supplied in application_icon_profile(brand).get("supplied_targets", []):
        source = contained_path(kit, supplied["source"])
        target = contained_path(kit, supplied["target"], required=False)
        if sha256_file(source) != supplied["sha256"]:
            raise ValueError("supplied application icon hash drift: %s" % supplied["source"])
        if source.suffix.lower() != target.suffix.lower():
            raise ValueError("supplied application icon source and target formats differ")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(source), str(target))

        record = by_path.get(supplied["target"])
        if record is None:
            dimensions = _supplied_icon_target_dimensions(supplied["target"])
            width, height = dimensions if dimensions is not None else (None, None)
            record = {
                "path": supplied["target"],
                "platform": platform_for(supplied["target"]),
                "role": "supplied-target",
                "format": target.suffix.lower().lstrip("."),
                "width": width,
                "height": height,
                "appearance": None,
                "alpha": "either",
                "source_variant": "source-preserved",
                "destination": "Approved platform target",
            }
            artifacts.append(record)
            by_path[supplied["target"]] = record
        record["source_variant"] = "source-preserved"
        record["source"] = supplied["source"]
        record["source_sha256"] = supplied["sha256"]

        suite = next((row for row in suites
                      if supplied["target"].startswith(row.get("root", "").rstrip("/") + "/")), None)
        if suite is None:
            raise ValueError("supplied application icon target has no platform suite: %s" % supplied["target"])
        child_path = contained_path(kit, suite["manifest"])
        child = json.loads(child_path.read_text(encoding="utf-8"))
        child_artifacts = child.get("artifacts")
        if not isinstance(child_artifacts, list):
            raise ValueError("platform icon manifest artifacts must be an array")
        replaced = False
        for index, item in enumerate(child_artifacts):
            if item.get("path") == supplied["target"]:
                child_artifacts[index] = record
                replaced = True
                break
        if not replaced:
            child_artifacts.append(record)
        write_json(child_path, child)

        if supplied["target"].startswith("icons/web/"):
            alias = "favicons/%s" % target.name
            alias_path = contained_path(kit, alias, required=False)
            alias_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(source), str(alias_path))
            manifest.setdefault("aliases", {})[alias] = supplied["target"]

    write_json(manifest_path, manifest)
    return manifest


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: apply_supplied_icons.py <brand.json> <kit-dir>")
    brand = load_brand(sys.argv[1])
    manifest = apply_supplied_targets(brand, sys.argv[2])
    print("applied %d source-preserved platform icon targets" % len(
        application_icon_profile(brand).get("supplied_targets", [])))
    return 0 if manifest else 1


if __name__ == "__main__":
    sys.exit(main())
