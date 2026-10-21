#!/usr/bin/env python3
"""Resolve omitted horizontal-layout settings before the explicit source renderer."""
import copy

from brand_contract import horizontal_wordmark_lines
from lockup_typography import horizontal_lockup as explicit_horizontal_lockup


def required(brand):
    logo = brand.get("logo") or {}
    horizontal = (logo.get("lockups") or {}).get("horizontal") or {}
    return ("canvas_height_units" not in horizontal
            or any("wordmark" not in ((logo.get("role_colors") or {}).get(mode) or {})
                   for mode in ("color", "light")))


def horizontal_lockup(brand, font_path, colourway, roles, *args):
    profile = horizontal_wordmark_lines(brand)
    if profile is None:
        raise ValueError("horizontal wordmark lines require an explicit row configuration")
    resolved = brand
    horizontal = (brand.get("logo") or {}).get("lockups", {}).get("horizontal", {})
    if "canvas_height_units" not in horizontal:
        resolved = copy.deepcopy(brand)
        resolved["logo"]["lockups"]["horizontal"]["canvas_height_units"] = max(
            profile["canvas_height_units"], profile["mark_height_units"] + 2 * profile["padding_units"])
    inks = dict(roles)
    inks.setdefault("wordmark", "#F2F5FA" if colourway == "color" else "#0A0A0A")
    return explicit_horizontal_lockup(resolved, font_path, colourway, inks, *args)
