#!/usr/bin/env python3
"""Resolve authored identity colors and measured interface cues from one source model."""

import re
import json
from pathlib import Path

from coloraide import Color

from brand_contract import semantic_colors


HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
SEGMENT = re.compile(r"^[a-z][a-z0-9_-]*$")
IDENTITY_SOURCE = re.compile(r"^(?:brand\.accent\.(?:bright|deep|accessible|dim)|brand\.logo\.role_colors\.color\.[a-z][a-z0-9_]*|brand\.legacy_palette\.[0-9]+|semantic\.(?:action|emphasis))$")
CUES = ("action", "warning", "error", "success", "information", "focus", "selection", "disabled")


class ColorRoleError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise ColorRoleError(message)


def _source_value(source, brand, canon):
    _require(isinstance(source, str) and source and all(SEGMENT.fullmatch(part) or part.isdecimal() for part in source.split(".")),
             "unsupported color source reference: %r" % source)
    parts = source.split(".")
    if parts[0] == "brand":
        node = brand
        parts = parts[1:]
    elif parts[0] == "canon":
        node = canon
        parts = parts[1:]
    elif parts[0] == "semantic":
        node = semantic_colors(brand, canon)
        parts = parts[1:]
    else:
        raise ColorRoleError("unsupported color source reference: %s" % source)
    for part in parts:
        if isinstance(node, list) and part.isdecimal():
            index = int(part)
            _require(index < len(node), "unknown color source reference: %s" % source)
            node = node[index]
        else:
            _require(isinstance(node, dict) and part in node, "unknown color source reference: %s" % source)
            node = node[part]
    _require(isinstance(node, str) and HEX.fullmatch(node), "color source is not a hex value: %s" % source)
    return node.upper()


def _ratio(first, second):
    return round(Color(first).contrast(second, method="wcag21"), 2)


def _foreground(fill):
    black, white = _ratio("#000000", fill), _ratio("#FFFFFF", fill)
    return ("#000000", black) if black >= white else ("#FFFFFF", white)


def resolve_color_roles(brand, canon):
    """Return JSON-ready role records without changing any approved input color."""
    declaration = brand.get("color_roles")
    _require(isinstance(declaration, dict) and set(declaration).issubset({"identity", "combinations", "interface_overrides"}),
             "color_roles must declare identity and combinations with optional interface_overrides")
    identity = declaration.get("identity")
    _require(isinstance(identity, list) and identity, "color_roles.identity requires at least one formal color")
    formal, seen = [], set()
    for entry in identity:
        _require(isinstance(entry, dict) and set(entry) == {"id", "label", "source", "use"},
                 "formal color requires id, label, source, and use")
        identifier, label, source, use = (entry[key] for key in ("id", "label", "source", "use"))
        _require(isinstance(identifier, str) and SEGMENT.fullmatch(identifier) and identifier not in seen,
                 "duplicate or invalid formal color id: %r" % identifier)
        _require(isinstance(label, str) and label.strip() and isinstance(use, str) and use.strip(),
                 "formal color label and use must be nonempty")
        _require(isinstance(source, str) and IDENTITY_SOURCE.fullmatch(source),
                 "unsupported formal color source: %r" % source)
        formal.append({"id": identifier, "label": label, "source": source,
                       "hex": _source_value(source, brand, canon), "use": use})
        seen.add(identifier)

    declarations = declaration.get("combinations")
    _require(isinstance(declarations, list) and declarations,
             "color_roles.combinations requires at least one approved use")
    combinations, combination_ids = [], set()
    for entry in declarations:
        _require(isinstance(entry, dict) and set(entry) == {"id", "label", "colors", "artwork", "use"},
                 "identity combination requires id, label, colors, artwork, and use")
        identifier, label, colors, artwork, use = (entry[key] for key in ("id", "label", "colors", "artwork", "use"))
        _require(isinstance(identifier, str) and SEGMENT.fullmatch(identifier) and identifier not in combination_ids,
                 "duplicate or invalid identity combination id: %r" % identifier)
        _require(isinstance(label, str) and label.strip() and isinstance(use, str) and use.strip(),
                 "identity combination label and use must be nonempty")
        _require(isinstance(colors, list) and colors and all(isinstance(color, str) and color in seen for color in colors)
                 and len(colors) == len(set(colors)), "identity combination must reference distinct formal colors")
        _require(artwork in {"logo.full", "logo.reduced", "brand.applications"},
                 "unsupported identity combination artwork reference: %r" % artwork)
        combinations.append({"id": identifier, "label": label, "colors": colors,
                             "artwork": artwork, "use": use})
        combination_ids.add(identifier)

    model = ((canon.get("color") or {}).get("role_model") or {}).get("interface_cues")
    _require(isinstance(model, dict) and set(model) == set(CUES), "canon interface cue model must define eight roles")
    overrides = declaration.get("interface_overrides") or {}
    _require(isinstance(overrides, dict) and set(overrides).issubset(set(CUES)),
             "unsupported interface cue override")
    surfaces = {"dark": (brand.get("surfaces") or {}).get("base", "#000000"),
                "light": (brand.get("light_surfaces") or {}).get("base", "#F8F8F6")}
    interface = {"dark": [], "light": []}
    for cue in CUES:
        definition = model[cue]
        _require(isinstance(definition, dict) and set(definition) == {"label", "use", "non_color_cue", "dark", "light"},
                 "incomplete interface cue model: %s" % cue)
        _require(all(isinstance(definition[key], str) and definition[key].strip()
                     for key in ("label", "use", "non_color_cue")),
                 "interface cue needs meaning and non-color cue: %s" % cue)
        override = overrides.get(cue) or {}
        if cue in overrides:
            _require(isinstance(override, dict) and set(override) == {"dark", "light"},
                     "interface cue override needs dark and light sources: %s" % cue)
        for theme in ("dark", "light"):
            source = override.get(theme, definition[theme])
            value = _source_value(source, brand, canon)
            surface = surfaces[theme]
            _require(isinstance(surface, str) and HEX.fullmatch(surface), "invalid %s surface" % theme)
            foreground, foreground_ratio = _foreground(value)
            _require(foreground_ratio >= 4.5, "%s %s foreground contrast below 4.5" % (theme, cue))
            surface_ratio = _ratio(value, surface)
            if cue in {"focus", "selection"}:
                _require(surface_ratio >= 3.0, "%s %s surface contrast below 3.0" % (theme, cue))
            interface[theme].append({"id": cue, "label": definition["label"], "source": source,
                                     "hex": value, "use": definition["use"],
                                     "non_color_cue": definition["non_color_cue"],
                                     "foreground": foreground, "foreground_contrast": foreground_ratio,
                                     "surface": surface.upper(), "surface_contrast": surface_ratio,
                                     "theme": theme})
    return {"schema_version": 1, "identity": formal, "identity_combinations": combinations, "interface": interface}


def load_color_roles(brand, kit):
    """Read the generated authority, with source fallback for isolated guide tests."""
    path = Path(kit) / "color-roles.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    if "color_roles" not in brand:
        return None
    from interface_contract import load_brand_canon
    return resolve_color_roles(brand, load_brand_canon())
