#!/usr/bin/env python3
"""Shared plain-English asset semantics and post-approval publication aliases."""

import hashlib
import json
import re
from pathlib import Path


AXES = ("purpose", "form", "layout", "treatment", "background", "surface", "ink",
        "platform", "platform_role", "source_variant")
ALIAS_INDEX = "logos/asset-aliases.json"


def _word(value):
    return str(value or "").replace("-", " ").replace("_", " ").strip()


def _safe_path(root, relative):
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("invalid asset path")
    parts = Path(relative).parts
    if Path(relative).is_absolute() or any(part in {"", ".", ".."} for part in parts):
        raise ValueError("unsafe asset path: %s" % relative)
    base = Path(root).resolve()
    current = base
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("asset path contains symlink: %s" % relative)
    if base not in current.resolve().parents:
        raise ValueError("asset path escapes kit: %s" % relative)
    return current


def describe(item):
    """Return one semantic design description without size or file format."""
    family = item.get("family") or ("logo" if str(item.get("path", "")).startswith("logos/") else "icon")
    path = str(item.get("path") or "")
    kind = str(item.get("kind") or "")
    colourway = str(item.get("colourway") or "")
    variant = str(item.get("variant") or "")
    if family == "logo":
        if kind not in {"lockup", "mark", "wordmark", "social-image"}:
            raise ValueError("unsupported logo kind: %s" % kind)
        layout = ("wide" if "-horizontal-" in path or "-lockup-wide-" in path
                  else "stacked" if "-stacked-" in path or "-lockup-stacked-" in path else "none")
        if kind == "lockup" and layout == "none":
            raise ValueError("lockup lacks wide or stacked layout: %s" % path)
        if kind == "social-image":
            purpose, form, layout = "social-share", "social-image", "none"
            treatment, background, surface, ink = "full-color", "dark", "none", "none"
            title = "Social share image, full color, dark background"
        else:
            purpose = "brand-identity"
            form = kind
            if colourway not in {"color", "light", "black", "white"}:
                raise ValueError("unsupported logo colourway: %s" % colourway)
            treatment = "monochrome" if colourway in {"black", "white"} else "full-color"
            background = "clear"
            surface = "light" if colourway in {"light", "black"} else "dark"
            ink = colourway if colourway in {"black", "white"} else "none"
            if kind == "lockup":
                name = "%s%s logo lockup" % ("Reduced " if variant == "reduced" else "", layout.lower())
                name = name[0].upper() + name[1:]
            elif kind == "mark":
                name = "%s brand mark" % ("Reduced" if variant == "reduced" else "Full")
            else:
                name = "Wordmark"
            description = "monochrome %s ink" % ink if ink != "none" else "full color"
            title = "%s, %s, for %s backgrounds" % (name, description, surface)
        platform, platform_role = "identity", "none"
        source_variant = variant if kind in {"mark", "lockup"} else "none"
    else:
        platform = str(item.get("platform") or "integration")
        raw_role = str(item.get("role") or "asset")
        platform_role = ("app-icon" if platform == "apple-macos" and raw_role in {"asset-catalog-icon", "iconset-icon", "icns"}
                         else "web-icon" if platform == "web" and raw_role in {"favicon", "apple-touch", "installable"}
                         else raw_role)
        purpose = "platform-icon"
        form = "icon"
        layout = "none"
        appearance = str(item.get("appearance") or "default")
        treatment = "monochrome" if appearance in {"black", "white", "monochrome"} else "full-color"
        alpha = item.get("alpha")
        background = "clear" if alpha == "transparent" else "opaque" if alpha == "opaque" else "none"
        surface = ("light" if appearance in {"light", "tinted", "light-unplated"}
                   else "dark" if appearance in {"dark", "dark-unplated"} else "none")
        ink = appearance if appearance in {"black", "white"} else "none"
        source_variant = str(item.get("source_variant") or "none")
        title = "%s %s" % ({"web": "Web", "android": "Android", "apple-ios": "iOS",
                             "apple-macos": "macOS", "windows": "Windows"}.get(platform, _word(platform).title()),
                            "icon" if platform_role == "web-icon" else _word(platform_role))
        if platform_role == "web-icon" and source_variant in {"full", "reduced"}:
            title += ", %s detail" % source_variant
        elif platform_role == "web-icon" and source_variant == "source-preserved":
            title += ", supplied artwork"
        title = title.strip()
        if background == "opaque":
            title += ", %s background" % background
        if surface != "none":
            title += ", for %s backgrounds" % surface
        if ink != "none":
            title += ", %s ink" % ink
    return {"purpose": purpose, "form": form, "layout": layout, "treatment": treatment,
            "background": background, "surface": surface, "ink": ink, "platform": platform,
            "platform_role": platform_role, "source_variant": source_variant, "title": title,
            "usage": str(item.get("destination") or ("Social sharing" if purpose == "social-share" else "Brand identity"))}


def design_key(item):
    description = describe(item)
    return tuple(description[axis] for axis in AXES)


def design_id(item):
    return "asset-" + re.sub(r"[^a-z0-9]+", "-", "-".join(design_key(item)).lower()).strip("-")


def preferred_path(slug, item):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("invalid brand slug for asset name")
    if item.get("family", "logo") != "logo":
        return str(item["path"])
    description = describe(item)
    path = Path(item["path"])
    stem = [slug, "social-share-image" if description["form"] == "social-image"
            else "logo-lockup" if description["form"] == "lockup"
            else "brand-mark" if description["form"] == "mark" else "wordmark"]
    if description["layout"] != "none":
        stem.append(description["layout"])
    if description["form"] == "mark":
        stem.append("reduced-detail" if description["source_variant"] == "reduced" else "full-detail")
    elif description["form"] == "lockup" and description["source_variant"] == "reduced":
        stem.append("reduced-detail")
    stem.append(description["treatment"])
    stem.append(description["background"])
    if description["ink"] != "none":
        stem.append(description["ink"])
    if description["surface"] != "none":
        stem.append("for-" + description["surface"])
    size = re.search(r"-(\d+)(?:x\d+)?$", path.stem)
    if size:
        stem.append(size.group(1))
    return "logos/named/%s%s" % ("-".join(stem), path.suffix)


def write_aliases(kit, slug, derivatives):
    """Reconcile generated public names without touching approved derivatives."""
    root = Path(kit).resolve()
    aliases = []
    by_preferred = {}
    for item in derivatives:
        source_path = item["path"]
        source = _safe_path(root, source_path)
        if not source.is_file() or source.suffix.lower() not in {".svg", ".png"}:
            raise ValueError("missing or unsupported approved asset: %s" % source_path)
        public_item = dict(item, family="logo", platform="identity", format=source.suffix[1:])
        preferred = preferred_path(slug, public_item)
        _safe_path(root, preferred)
        contents = source.read_bytes()
        digest = hashlib.sha256(contents).hexdigest()
        if preferred in by_preferred and by_preferred[preferred][0] != digest:
            raise ValueError("descriptive alias collision: %s" % preferred)
        by_preferred[preferred] = (digest, contents)
        description = describe(public_item)
        aliases.append({"source_path": source_path, "preferred_path": preferred, "sha256": digest,
                        "design_id": design_id(public_item),
                        "design": {key: description[key] for key in AXES},
                        "title": description["title"]})
    named_root = _safe_path(root, "logos/named")
    if named_root.exists() and not named_root.is_dir():
        raise ValueError("named delivery path is not a directory")
    existing = list(named_root.rglob("*")) if named_root.exists() else []
    if any(path.is_symlink() or not (path.is_file() or path.is_dir()) for path in existing):
        raise ValueError("named delivery tree contains an unsafe entry")
    for path in existing:
        if path.is_file() and path.relative_to(root).as_posix() not in by_preferred:
            path.unlink()
    for path in sorted((path for path in existing if path.is_dir()), key=lambda value: len(value.parts), reverse=True):
        if not any(path.iterdir()):
            path.rmdir()
    for preferred, (_, contents) in by_preferred.items():
        target = _safe_path(root, preferred)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not target.is_file():
            raise ValueError("descriptive alias path is not a file: %s" % preferred)
        if not target.exists() or target.read_bytes() != contents:
            target.write_bytes(contents)
    payload = {"schema_version": 1, "brand": slug, "aliases": sorted(aliases, key=lambda item: item["source_path"])}
    index = _safe_path(root, ALIAS_INDEX)
    with index.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    return payload


def validate_aliases(kit, derivatives, mapping=None):
    root = Path(kit)
    problems = []
    try:
        if mapping is None:
            mapping = json.loads(_safe_path(root, ALIAS_INDEX).read_text(encoding="utf-8"))
        approved = {item["path"] for item in derivatives}
        rows = mapping["aliases"]
        if mapping.get("schema_version") != 1 or not isinstance(rows, list):
            raise ValueError("invalid alias index header")
        if {row.get("source_path") for row in rows} != approved or len(rows) != len(approved):
            raise ValueError("alias index does not cover exact derivative inventory")
        expected_named = set()
        for row in rows:
            source_path, preferred = row["source_path"], row["preferred_path"]
            approved_item = next(item for item in derivatives if item["path"] == source_path)
            expected_path = preferred_path(mapping["brand"], dict(approved_item, family="logo"))
            expected_item = dict(approved_item, family="logo")
            description = describe(expected_item)
            if (preferred != expected_path or row.get("design_id") != design_id(expected_item)
                    or row.get("design") != {key: description[key] for key in AXES}
                    or row.get("title") != description["title"]):
                raise ValueError("alias semantics disagree with approved source: %s" % source_path)
            source, target = _safe_path(root, source_path), _safe_path(root, preferred)
            if not preferred.startswith("logos/named/") or not source.is_file() or not target.is_file():
                raise ValueError("alias path is missing or outside named delivery tree")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            if (approved_item.get("sha256", digest) != digest
                    or hashlib.sha256(target.read_bytes()).hexdigest() != digest or row["sha256"] != digest):
                raise ValueError("alias digest mismatch: %s" % preferred)
            expected_named.add(preferred)
        if any(path.is_symlink() for path in (root / "logos" / "named").rglob("*")):
            raise ValueError("named delivery tree contains a symlink")
        actual_named = {path.relative_to(root).as_posix() for path in (root / "logos" / "named").rglob("*") if path.is_file()}
        if actual_named != expected_named:
            raise ValueError("named delivery inventory differs from alias index")
    except (OSError, ValueError, KeyError, TypeError) as error:
        problems.append(str(error))
    return problems
