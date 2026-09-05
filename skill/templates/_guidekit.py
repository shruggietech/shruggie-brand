# -*- coding: utf-8 -*-
"""Shared helpers for the two document generators. Both read the SAME tokens the
product ships, so a kit's documents and its interface cannot drift apart."""
import base64, json, os, re
from brand_contract import affiliation_text, font_faces, typography_families

def tokens(kit):
    css = open(os.path.join(kit, "nextjs", "globals.css"), encoding="utf-8").read()
    def blk(n):
        m = re.search(r"^%s \{(.*?)^\}" % n, css, re.S | re.M)
        if not m: return {}
        return dict((k, h) for k, _, h in re.findall(
            r"--([a-z0-9-]+):\s*(oklch\([^)]*\));\s*/\* (#[0-9A-Fa-f]{6}) \*/", m.group(1)))
    return blk(r"\.dark"), blk(":root")

def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()

def faces(kit, brand):
    out, families, selected = "", typography_families(brand), {}
    for face in font_faces(brand):
        key = (face["role"], face["weight"], face["style"])
        if key not in selected or face["format"] == "woff2":
            selected[key] = face
    for key in sorted(selected):
        face = selected[key]
        p = os.path.join(kit, face["path"].replace("/", os.sep))
        if os.path.exists(p):
            mime = "font/woff2" if face["format"] == "woff2" else "font/%s" % face["format"]
            fmt = {"woff2": "woff2", "ttf": "truetype", "otf": "opentype"}[face["format"]]
            out += ("@font-face{font-family:'%s';font-weight:%d;font-style:%s;font-display:block;"
                    "src:url(data:%s;base64,%s) format('%s')}\n" % (
                        families[face["role"]]["name"], face["weight"], face["style"], mime, b64(p), fmt))
    return out


def type_context(brand):
    families = typography_families(brand)
    return {
        "display": families["display"]["name"],
        "body": families["body"]["name"],
        "mono": families["mono"]["name"],
        "display_weights": ", ".join(str(value) for value in families["display"]["weights"]),
        "body_weights": ", ".join(str(value) for value in families["body"]["weights"]),
        "mono_weights": ", ".join(str(value) for value in families["mono"]["weights"]),
        "display_bold": max(families["display"]["weights"]),
        "display_regular": min(families["display"]["weights"]),
        "body_regular": min(families["body"]["weights"]),
        "body_medium": max(families["body"]["weights"]),
    }

def asset(kit, *cands):
    for c in cands:
        p = os.path.join(kit, "logos", "png", c)
        if os.path.exists(p): return b64(p)
    return None

def copy_for(B, key, default):
    """Prose comes from brand.json `guide` when the operator wrote it, and from a
    generated default otherwise. A kit is complete from two inputs; overriding
    any single section stays a one-line edit."""
    return ((B.get("guide") or {}).get(key)) or default
