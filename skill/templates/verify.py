#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify.py: assert a contracted brand kit against its selected canon rules.

Every number this emits is measured from the shipped files at run time. Nothing
is transcribed from a previous run. A check whose inputs are absent is reported
as SKIP with the reason, never silently passed.

    python3 build/verify.py [kit-dir] [--canon PATH] [--out VERIFY.md]

Exit code is the number of problems found, capped at 125.
"""
import argparse, base64, copy, hashlib, json, os, re, struct, sys, tempfile, unicodedata, zlib
from io import BytesIO
from pathlib import Path
import xml.etree.ElementTree as ET
from coloraide import Color
from capabilities import load_capabilities
from brand_contract import affiliation, application_icon_profile, logo_source_contract, sha256_file
from iconkit import ANDROID_DENSITIES, GENERATION_MARKER, ICO_SIZES, MAC_ROLES, WINDOWS_TARGETS, inspect_png

# ------------------------------------------------------------------ utilities
def R(a, b): return round(Color(a).contrast(b, method="wcag21"), 2)
def hue(h):
    c = Color(h).convert("oklch")
    return None if c["chroma"] < 0.02 else round(c["hue"], 1)
def hue_gap(a, b):
    x, y = hue(a), hue(b)
    if x is None or y is None: return None
    d = abs(x - y); return round(min(d, 360 - d), 1)

class Report:
    def __init__(self): self.rows, self.problems, self.skips = [], [], []
    def ok(self, cid, detail=""):   self.rows.append((cid, "pass", detail))
    def bad(self, cid, detail):
        self.rows.append((cid, "FAIL", detail)); self.problems.append("%s: %s" % (cid, detail))
    def skip(self, cid, why):
        self.rows.append((cid, "skip", why)); self.skips.append("%s: %s" % (cid, why))

TEXT_EXT = {".md", ".json", ".css", ".js", ".jsx", ".ts", ".tsx", ".mjs",
            ".html", ".svg", ".xml", ".txt", ".py", ".webmanifest", ".snippet"}
SRC_EXT  = {".js", ".jsx", ".ts", ".tsx", ".mjs"}

def walk(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in {"node_modules", "concepts", ".git", ".next", "dist"}]
        for f in fn: yield os.path.join(dp, f)

# -------------------------------------------------------------------- checks
def c_encoding(kit, rep):
    bad = []
    for p in walk(kit):
        if os.path.splitext(p)[1].lower() not in TEXT_EXT: continue
        b = open(p, "rb").read()
        if b[:3] == b"\xef\xbb\xbf": bad.append("%s: BOM" % os.path.relpath(p, kit)); continue
        try: t = b.decode("utf-8")
        except UnicodeDecodeError as e: bad.append("%s: not UTF-8 (%s)" % (os.path.relpath(p, kit), e)); continue
        # Escaped, never literal: this file ships inside every kit as
        # build/verify.py, and a literal sentinel makes the checker flag itself.
        for m in ("\u00c3\u00a2", "\u00c3\u00a9", "\u00e2\u20ac\u2122",
                  "\u00e2\u20ac\u009c", "\ufffd"):
            if m in t: bad.append("%s: mojibake %r" % (os.path.relpath(p, kit), m)); break
    rep.bad("encoding", "; ".join(bad)) if bad else rep.ok("encoding", "all text files UTF-8, no BOM, no mojibake")

def c_contrast(kit, brand, rep):
    """Re-derive every contrast number the kit states about itself."""
    claims, mism = 0, []
    def visit(node, path=""):
        nonlocal claims
        if isinstance(node, dict):
            if "hex" in node and isinstance(node.get("contrast"), dict):
                for k, stated in node["contrast"].items():
                    bg = brand.get("surfaces", {}).get("base", "#000000") if "dark" in k else "#F8F8F6"
                    got = R(node["hex"], bg); claims += 1
                    if abs(got - float(stated)) > 0.02:
                        mism.append("%s %s: states %s, measures %s" % (path, k, stated, got))
            if "legal_foreground_when_used_as_fill" in node and "hex" in node:
                lf = node["legal_foreground_when_used_as_fill"]; claims += 1
                got = R(lf["color"], node["hex"])
                b, w = R("#000000", node["hex"]), R("#FFFFFF", node["hex"])
                best = "#000000" if b >= w else "#FFFFFF"
                if abs(got - float(lf["ratio"])) > 0.01 or best != lf["color"]:
                    mism.append("%s foreground: states %s@%s, correct is %s@%s"
                                % (path, lf["color"], lf["ratio"], best, max(b, w)))
            for k, v in node.items(): visit(v, path + "/" + k if path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node): visit(v, "%s[%d]" % (path, i))
    visit(brand)
    if mism: rep.bad("contrast-rederived", "; ".join(mism))
    elif claims == 0: rep.skip("contrast-rederived", "brand.json states no contrast claims")
    else: rep.ok("contrast-rederived", "%d claims re-derived, all match" % claims)

def c_accent(canon, brand, rep):
    acc = brand.get("accent") or {}
    if not acc.get("bright"): return rep.skip("accent-rule", "brand.json declares no accent")
    a, al = acc["bright"], acc.get("accessible")
    base = brand.get("surfaces", {}).get("base", "#000000")
    sibs = canon["color"]["constrained_rules"]["identity_accent"]["checks"][0]["current_siblings"]
    fails = []
    # Fixtures exercise the pipeline and do not claim a sibling identity slot.
    # They still have to pass every contrast and accessibility requirement.
    inherits_house = affiliation(brand)["inheritance"] == "shruggietech-house"
    if brand.get("kind") != "fixture" and inherits_house:
        for name, s in sibs.items():
            if name == brand.get("slug"): continue
            g = hue_gap(a, s["hex"])
            if g is not None and g < 30: fails.append("hue %s from %s (needs 30)" % (g, name))
        g = hue_gap(a, canon["color"]["immutable"]["orange"]["hex"])
        if g is not None and g < 30: fails.append("hue %s from inherited orange (needs 30)" % g)
    r = R(a, base)
    if r < 4.5: fails.append("accent %s on base = %s (needs 4.5)" % (a, r))
    if not al: fails.append("no accessible light-surface variant declared")
    else:
        rl = R(al, "#F8F8F6")
        if rl < 4.5: fails.append("light variant %s = %s on #F8F8F6 (needs 4.5)" % (al, rl))
    rep.bad("accent-rule", "; ".join(fails)) if fails else \
        rep.ok("accent-rule", "%s%s:1 on base, light variant %s at %s:1"
               % (("fixture hue exempt, " if brand.get("kind") == "fixture" else "hue %s, " % hue(a)),
                  r, al, R(al, "#F8F8F6")))

def c_immutables(canon, brand, rep):
    drift = []
    inherits_house = affiliation(brand)["inheritance"] == "shruggietech-house"
    for k, tok in canon["color"]["immutable"].items():
        if not inherits_house and k in {"orange", "orange-cta"}:
            continue
        got = (brand.get("color", {}) or {}).get(k)
        if got and got.get("hex", "").upper() != tok["hex"].upper():
            drift.append("%s: kit has %s, canon has %s" % (k, got["hex"], tok["hex"]))
    ct = canon["typography"]["families"]
    typography = brand.get("typography") or {}
    bt = typography.get("families")
    if bt and typography.get("mode") == "house":
        for role, fam in ct.items():
            if bt.get(role, {}).get("name") and bt[role]["name"] != fam["name"]:
                drift.append("typography.%s: kit has %s, canon has %s" % (role, bt[role]["name"], fam["name"]))
    rep.bad("immutables-verbatim", "; ".join(drift)) if drift else \
        rep.ok("immutables-verbatim", "no drift from canon immutables")

def c_radius(kit, canon, rep):
    css = os.path.join(kit, "nextjs", "globals.css")
    if not os.path.exists(css): return rep.skip("radius-pegs", "nextjs/globals.css not present")
    t = open(css, encoding="utf-8").read(); miss = []
    for peg, val in canon["shadcn"]["radius_pegs"]["values"].items():
        if not re.search(r"%s:\s*%s\s*;" % (re.escape(peg), re.escape(val)), t):
            miss.append("%s should be %s" % (peg, val))
    rep.bad("radius-pegs", "; ".join(miss)) if miss else \
        rep.ok("radius-pegs", "all %d pegs exact" % len(canon["shadcn"]["radius_pegs"]["values"]))

def c_globals(kit, rep):
    css = os.path.join(kit, "nextjs", "globals.css")
    if not os.path.exists(css): return rep.skip("globals-slots", "nextjs/globals.css not present")
    t = open(css, encoding="utf-8").read()
    def blk(n):
        m = re.search(r"^%s \{(.*?)^\}" % n, t, re.S | re.M)
        return {} if not m else dict((k, h) for k, _, h in re.findall(
            r"--([a-z0-9-]+):\s*(oklch\([^)]*\));\s*/\* (#[0-9A-Fa-f]{6}) \*/", m.group(1)))
    dark, light = blk(r"\.dark"), blk(":root")
    if not dark or not light: return rep.skip("globals-slots", "could not parse :root / .dark")
    fails = []
    for k, v in list(dark.items()) + list(light.items()):
        rt = Color(v[0] if isinstance(v, tuple) else v)
    for scope, tbl in (("dark", dark), ("light", light)):
        for k, hx in tbl.items():
            pass
    # round-trip
    for scope, tbl in (("dark", blk(r"\.dark")), ("light", blk(":root"))):
        m = re.search(r"^%s \{(.*?)^\}" % (r"\.dark" if scope == "dark" else ":root"), t, re.S | re.M)
        for k, ok_, hx in re.findall(r"--([a-z0-9-]+):\s*(oklch\([^)]*\));\s*/\* (#[0-9A-Fa-f]{6}) \*/", m.group(1)):
            back = Color(ok_).convert("srgb").to_string(hex=True).upper()
            if back != hx.upper(): fails.append("%s/%s oklch->%s != %s" % (scope, k, back, hx))
    pairs = [("foreground","background"),("card-foreground","card"),("popover-foreground","popover"),
             ("primary-foreground","primary"),("secondary-foreground","secondary"),
             ("muted-foreground","muted"),("accent-foreground","accent")]
    for scope, tbl in (("dark", dark), ("light", light)):
        for fg, bg in pairs:
            if fg in tbl and bg in tbl:
                r = R(tbl[fg], tbl[bg])
                if r < 4.5: fails.append("%s %s on %s = %s" % (scope, fg, bg, r))
        for i in range(1, 6):
            k = "chart-%d" % i
            if k in tbl and "background" in tbl:
                r = R(tbl[k], tbl["background"])
                if r < 4.5: fails.append("%s %s = %s on background" % (scope, k, r))
        for k in ("destructive", "ring"):
            if k in tbl and "background" in tbl:
                r = R(tbl[k], tbl["background"])
                if r < 4.5: fails.append("%s %s = %s on background" % (scope, k, r))
    rep.bad("globals-slots", "; ".join(fails)) if fails else \
        rep.ok("globals-slots", "%d values round-trip; every pair, chart and state meets AA"
               % (len(dark) + len(light)))

BANNED = [
    (r"\b(\w[\w\- ]{2,30}), not (\w[\w\- ]{2,30})\b", "the X, not Y contrast"),
    (r"\brather than merely\b", "rather than merely"),
    (r"\b(?:synergy|best-in-class|game-changing|revolutionary|effortless|seamless)\b", "corporate filler"),
    (r"\bsupercharg(?:e|es|ed|ing)\b", "corporate filler"),
]
COPY_FILES = ("README.md", "SKILL.md", "readme.md")

# A document that DEFINES the banned patterns will always contain them. It opts
# out with an explicit, reasoned marker, and verify reports every exemption so
# the escape hatch stays visible instead of becoming a silent hole.
EXEMPT = re.compile(r'<!--\s*verify:allow-rhetoric\s+reason="([^"]{6,120})"\s*-->')

def c_rhetoric(kit, rep):
    hits, scanned, dashes, exempt = [], 0, 0, []
    for p in walk(kit):
        rel = os.path.relpath(p, kit)
        if os.path.basename(p) not in COPY_FILES and not rel.startswith("guidelines"): continue
        if os.path.splitext(p)[1].lower() not in {".md", ".html"}: continue
        t = open(p, encoding="utf-8", errors="replace").read(); scanned += 1
        dashes += t.count("\u2014")
        m = EXEMPT.search(t)
        if m:
            exempt.append("%s (%s)" % (rel, m.group(1))); continue
        for pat, label in BANNED:
            for mm in re.finditer(pat, t, re.I):
                hits.append("%s: %s -> %r" % (rel, label, mm.group(0)[:60]))
    if not scanned: return rep.skip("banned-rhetoric", "no brand-copy files found")
    tail = "; %d exempt: %s" % (len(exempt), ", ".join(exempt)) if exempt else ""
    if hits: rep.bad("banned-rhetoric", "; ".join(hits[:8]) + tail)
    else: rep.ok("banned-rhetoric", "%d copy files clean; %d em-dashes (reported, not failed)%s"
                 % (scanned, dashes, tail))

def c_raw_values(kit, rep):
    hits, scanned = [], 0
    for p in walk(kit):
        rel = os.path.relpath(p, kit)
        if os.path.splitext(p)[1].lower() not in SRC_EXT: continue
        if rel.startswith(("tokens", "build", "templates")) or "enforcement" in rel: continue
        t = open(p, encoding="utf-8", errors="replace").read(); scanned += 1
        for pat, label in ((r"[\"']#[0-9a-fA-F]{3,8}[\"']", "raw hex"),
                           (r"[\"']\d+px[\"']", "raw px"),
                           (r"\b(?:bg|text|border)-(?:slate|gray|zinc|neutral|stone)-\d{2,3}\b", "stock palette class")):
            for m in re.finditer(pat, t):
                hits.append("%s: %s %s" % (rel, label, m.group(0)))
    if not scanned: return rep.skip("no-raw-values", "no component source found")
    rep.bad("no-raw-values", "; ".join(hits[:8])) if hits else \
        rep.ok("no-raw-values", "%d source files, no raw hex, px or stock palette classes" % scanned)

def c_font_weights(kit, brand, rep):
    shipped = {}
    for role, fam in (brand.get("typography", {}).get("families") or {}).items():
        shipped[fam["name"].lower()] = set(fam["weights"])
    allowed = set().union(*shipped.values()) if shipped else set()
    hits, scanned = [], 0
    for p in walk(kit):
        if os.path.splitext(p)[1].lower() not in ({".css"} | SRC_EXT): continue
        rel = os.path.relpath(p, kit)
        if "enforcement" in rel or rel.startswith("templates"): continue
        t = open(p, encoding="utf-8", errors="replace").read(); scanned += 1
        for m in re.finditer(r"font-weight\s*:\s*(\d{3})", t):
            w = int(m.group(1))
            if w not in allowed: hits.append("%s: font-weight %d" % (rel, w))
        for m in re.finditer(r"fontWeight\s*:\s*(\d{3})", t):
            w = int(m.group(1))
            if w not in allowed: hits.append("%s: fontWeight %d" % (rel, w))
    if not scanned: return rep.skip("font-weights-exist", "no stylesheets or source found")
    rep.bad("font-weights-exist", "; ".join(hits[:8])) if hits else \
        rep.ok("font-weights-exist", "%d files, no weight requested that the faces lack" % scanned)

def c_svg(kit, rep):
    svgs = [p for p in walk(kit) if p.lower().endswith(".svg")]
    if not svgs: return (rep.skip("svg-no-live-text", "no SVGs in kit"),
                         rep.skip("svg-viewbox", "no SVGs in kit"))
    text_hits, vb_hits, raster_wrappers = [], [], []
    for p in svgs:
        rel = os.path.relpath(p, kit); t = open(p, encoding="utf-8", errors="replace").read()
        if re.search(r"<text\b", t) or re.search(r"font-family\s*=", t):
            text_hits.append(rel)
    # viewBox containment needs resolved transforms. A regex over raw path data
    # reports every glyph inside a translated <g> as clipped: false positives.
    try:
        from svgelements import SVG
    except ImportError:
        rep.skip("svg-viewbox", "svgelements not installed (regex cannot resolve transforms)")
        vb_hits = None
    authoritative_sources = set()
    try:
        brand = json.load(open(os.path.join(kit, "brand.json"), encoding="utf-8"))
        authoritative_sources = {
            os.path.normcase(os.path.normpath(record["path"]))
            for record in brand.get("authoritative_inputs", [])
            if record.get("format") == "svg"
        }
    except Exception:
        authoritative_sources = set()
    if vb_hits is not None:
        for p in svgs:
            rel = os.path.relpath(p, kit)
            if os.path.normcase(os.path.normpath(rel)) in authoritative_sources:
                raster_wrappers.append(rel)
                continue
            if "<image " in open(p, encoding="utf-8", errors="replace").read():
                raster_wrappers.append(rel)
                continue
            try:
                doc = SVG.parse(p); vb = doc.viewbox
                xs, ys = [], []
                for e in doc.elements():
                    try: bb = e.bbox()
                    except Exception: bb = None
                    if bb: xs += [bb[0], bb[2]]; ys += [bb[1], bb[3]]
                if not xs or vb is None: continue
                if (min(xs) < vb.x - 0.5 or min(ys) < vb.y - 0.5
                        or max(xs) > vb.x + vb.width + 0.5 or max(ys) > vb.y + vb.height + 0.5):
                    vb_hits.append("%s: ink (%.1f,%.1f)-(%.1f,%.1f) outside viewBox (%g,%g,%g,%g)"
                                   % (rel, min(xs), min(ys), max(xs), max(ys),
                                      vb.x, vb.y, vb.width, vb.height))
            except Exception as e:
                vb_hits.append("%s: could not parse (%s)" % (rel, e))
    rep.bad("svg-no-live-text", "; ".join(text_hits[:6])) if text_hits else \
        rep.ok("svg-no-live-text", "%d SVGs, all type outlined" % len(svgs))
    if vb_hits is not None:
        rep.bad("svg-viewbox", "; ".join(vb_hits[:6])) if vb_hits else \
            rep.ok("svg-viewbox", "%d vector SVGs resolved inside viewBox; %d lossless raster wrappers use generator-checked bounds"
                   % (len(svgs) - len(raster_wrappers), len(raster_wrappers)))

def c_ico(kit, rep):
    icos = [p for p in walk(kit) if p.lower().endswith(".ico")]
    if not icos: return rep.skip("ico-entries", "no .ico in kit")
    out = []
    for p in icos:
        b = open(p, "rb").read()
        if len(b) < 6 or b[:4] != b"\x00\x00\x01\x00":
            out.append("%s: not a valid ICO" % os.path.relpath(p, kit)); continue
        n = struct.unpack("<H", b[4:6])[0]
        sizes = []
        for i in range(n):
            off = 6 + i * 16
            if off + 2 > len(b): break
            w, h = b[off] or 256, b[off + 1] or 256
            sizes.append("%dx%d" % (w, h))
        if n < 5: out.append("%s: only %d entries (%s)" % (os.path.relpath(p, kit), n, ",".join(sizes)))
        else: rep.ok("ico-entries", "%s: %d entries (%s)" % (os.path.relpath(p, kit), n, ",".join(sizes)))
    if out: rep.bad("ico-entries", "; ".join(out))


def _container_sizes(path, kind):
    with open(path, "rb") as handle:
        payload = handle.read()
    if kind == "ico":
        if len(payload) < 6 or payload[:4] != b"\x00\x00\x01\x00":
            raise ValueError("not a valid ICO")
        count = struct.unpack("<H", payload[4:6])[0]
        if len(payload) < 6 + count * 16:
            raise ValueError("truncated ICO directory")
        sizes = []
        for index in range(count):
            offset = 6 + index * 16
            width = payload[offset] or 256
            height = payload[offset + 1] or 256
            length, start = struct.unpack("<II", payload[offset + 8:offset + 16])
            if width != height or start + length > len(payload):
                raise ValueError("invalid ICO entry %d" % index)
            sizes.append(width)
        return sizes
    if len(payload) < 8 or payload[:4] != b"icns":
        raise ValueError("not a valid ICNS")
    declared = struct.unpack(">I", payload[4:8])[0]
    if declared != len(payload):
        raise ValueError("ICNS length mismatch")
    mapping = {b"icp4": 16, b"icp5": 32, b"icp6": 64, b"ic07": 128,
               b"ic08": 256, b"ic09": 512, b"ic10": 1024}
    sizes, offset = [], 8
    while offset < len(payload):
        if offset + 8 > len(payload):
            raise ValueError("truncated ICNS entry")
        code = payload[offset:offset + 4]
        length = struct.unpack(">I", payload[offset + 4:offset + 8])[0]
        if length < 8 or offset + length > len(payload):
            raise ValueError("invalid ICNS entry length")
        if code in mapping:
            sizes.append(mapping[code])
        offset += length
    return sizes


def _expected_icon_paths(raster):
    """Return the independent minimum inventory for the selected capability tier."""
    required = {
        "icons/README.md",
        "icons/%s" % GENERATION_MARKER,
        "icons/web/README.md",
        "icons/web/favicon.svg",
        "icons/web/favicon-full.svg",
        "icons/web/manifest.json",
        "icons/android/README.md",
        "icons/android/manifest.json",
        "icons/apple/ios/README.md",
        "icons/apple/ios/manifest.json",
        "icons/apple/macos/README.md",
        "icons/apple/macos/manifest.json",
        "icons/windows/README.md",
        "icons/windows/manifest.json",
    }
    if not raster:
        return required
    for size in (16, 24, 32, 48, 64, 128, 180, 192, 256, 512):
        required.add("icons/web/favicon-%dx%d.png" % (size, size))
    required.update({
        "icons/web/apple-touch-icon.png",
        "icons/web/android-chrome-192x192.png",
        "icons/web/android-chrome-512x512.png",
        "icons/web/favicon.ico",
        "icons/web/site.webmanifest",
        "icons/android/app/src/main/res/drawable-nodpi/ic_launcher_foreground.png",
        "icons/android/app/src/main/res/drawable-nodpi/ic_launcher_monochrome.png",
        "icons/android/app/src/main/res/drawable/ic_launcher_background.xml",
        "icons/android/app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml",
        "icons/android/app/src/main/res/values/ic_launcher_colors.xml",
        "icons/android/play-store/google-play-512.png",
        "icons/apple/ios/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png",
        "icons/apple/ios/Assets.xcassets/AppIcon.appiconset/AppIcon-1024-dark.png",
        "icons/apple/ios/Assets.xcassets/AppIcon.appiconset/AppIcon-1024-tinted.png",
        "icons/apple/ios/Assets.xcassets/AppIcon.appiconset/Contents.json",
        "icons/apple/macos/Assets.xcassets/AppIcon.appiconset/Contents.json",
        "icons/apple/macos/AppIcon.icns",
        "icons/windows/classic/app.ico",
        "icons/windows/msix/ApplicationVisualElements.fragment.xml",
        "icons/windows/msix/PackageProperties.fragment.xml",
    })
    for density in ANDROID_DENSITIES:
        required.add("icons/android/app/src/main/res/mipmap-%s/ic_launcher.png" % density)
    for points, scale in MAC_ROLES:
        suffix = "@2x" if scale == 2 else ""
        name = "icon_%dx%d%s.png" % (points, points, suffix)
        required.add("icons/apple/macos/Assets.xcassets/AppIcon.appiconset/%s" % name)
        required.add("icons/apple/macos/AppIcon.iconset/%s" % name)
    for scale in (100, 200, 400):
        required.add("icons/windows/msix/Assets/Square44x44Logo.scale-%d.png" % scale)
        required.add("icons/windows/msix/Assets/Square150x150Logo.scale-%d.png" % scale)
        required.add("icons/windows/msix/Assets/StoreLogo.scale-%d.png" % scale)
    for size in WINDOWS_TARGETS:
        required.add("icons/windows/msix/Assets/Square44x44Logo.targetsize-%d.png" % size)
        required.add("icons/windows/msix/Assets/Square44x44Logo.targetsize-%d_altform-unplated.png" % size)
        required.add("icons/windows/msix/Assets/Square44x44Logo.targetsize-%d_altform-lightunplated.png" % size)
    return required


def _validate_apple_catalogs(kit, problems):
    ios_root = os.path.join(kit, "icons", "apple", "ios", "Assets.xcassets", "AppIcon.appiconset")
    ios_rows = [
        {"filename": "AppIcon-1024.png", "idiom": "universal", "platform": "ios", "size": "1024x1024"},
        {"filename": "AppIcon-1024-dark.png", "idiom": "universal", "platform": "ios", "size": "1024x1024",
         "appearances": [{"appearance": "luminosity", "value": "dark"}]},
        {"filename": "AppIcon-1024-tinted.png", "idiom": "universal", "platform": "ios", "size": "1024x1024",
         "appearances": [{"appearance": "luminosity", "value": "tinted"}]},
    ]
    mac_root = os.path.join(kit, "icons", "apple", "macos", "Assets.xcassets", "AppIcon.appiconset")
    mac_rows = []
    for points, scale in MAC_ROLES:
        suffix = "@2x" if scale == 2 else ""
        mac_rows.append({"filename": "icon_%dx%d%s.png" % (points, points, suffix), "idiom": "mac",
                         "scale": "%dx" % scale, "size": "%dx%d" % (points, points)})
    for label, root, rows in (("iOS", ios_root, ios_rows), ("macOS", mac_root, mac_rows)):
        path = os.path.join(root, "Contents.json")
        try:
            with open(path, encoding="utf-8") as handle:
                catalog = json.load(handle)
            expected = {"images": rows, "info": {"author": "xcode", "version": 1}}
            if catalog != expected:
                problems.append("%s Contents.json does not match the required file, size, scale, platform, and appearance relationships" % label)
            for row in rows:
                icon = os.path.join(root, row["filename"])
                if os.path.isfile(icon):
                    size = 1024 if label == "iOS" else int(row["size"].split("x")[0]) * int(row["scale"][0])
                    if inspect_png(icon)["size"] != (size, size):
                        problems.append("%s catalog entry %s has dimensions that disagree with its size and scale" % (label, row["filename"]))
        except Exception as error:
            problems.append("%s Contents.json cannot be validated: %s" % (label, error))


def _validate_windows_manifest_fragments(kit, brand, profile, problems):
    msix = os.path.join(kit, "icons", "windows", "msix")
    visual_path = os.path.join(msix, "ApplicationVisualElements.fragment.xml")
    properties_path = os.path.join(msix, "PackageProperties.fragment.xml")
    title = str(brand.get("title", ""))
    try:
        visual = ET.parse(visual_path).getroot()
        expected_tag = "{http://schemas.microsoft.com/appx/manifest/uap/windows10}VisualElements"
        expected_attributes = {
            "DisplayName": title,
            "Description": "%s application" % title,
            "BackgroundColor": profile["background"],
            "Square44x44Logo": "Assets\\Square44x44Logo.png",
            "Square150x150Logo": "Assets\\Square150x150Logo.png",
            "AppListEntry": "default",
        }
        if visual.tag != expected_tag or visual.attrib != expected_attributes or list(visual):
            problems.append("ApplicationVisualElements.fragment.xml does not match the required uap:VisualElements schema relationship")
    except Exception as error:
        problems.append("ApplicationVisualElements.fragment.xml cannot be validated: %s" % error)
    try:
        properties = ET.parse(properties_path).getroot()
        namespace = "{http://schemas.microsoft.com/appx/manifest/foundation/windows10}"
        expected_children = [
            (namespace + "DisplayName", title),
            (namespace + "PublisherDisplayName", title),
            (namespace + "Description", "%s application" % title),
            (namespace + "Logo", "Assets\\StoreLogo.png"),
        ]
        actual_children = [(child.tag, child.text) for child in properties]
        if properties.tag != namespace + "Properties" or properties.attrib or actual_children != expected_children:
            problems.append("PackageProperties.fragment.xml does not match the required Properties and StoreLogo schema relationship")
    except Exception as error:
        problems.append("PackageProperties.fragment.xml cannot be validated: %s" % error)


def _same_rgba(expected, actual):
    expected_rgba = expected.convert("RGBA")
    actual_rgba = actual.convert("RGBA")
    return expected_rgba.size == actual_rgba.size and expected_rgba.tobytes() == actual_rgba.tobytes()


def _expected_authoritative_icon(item, masters, profile):
    from iconkit import _plated, contain_visible
    variant = item.get("source_variant")
    if variant not in masters:
        return None
    mark = masters[variant]
    size = int(item["width"])
    role = item.get("role")
    appearance = item.get("appearance")
    if role == "adaptive-foreground":
        return contain_visible(mark, size, 66.0 / 108.0)
    if role == "adaptive-monochrome":
        return contain_visible(mark, size, 66.0 / 108.0, "#FFFFFF")
    if appearance in {"dark-unplated", "light-unplated"}:
        return contain_visible(mark, size, 0.72)
    background = ("#000000" if appearance == "dark" else
                  "#FFFFFF" if appearance == "tinted" else profile["background"])
    colour = "#000000" if appearance == "tinted" else None
    return _plated(mark, size, background, 0.75 if role == "play-store" else 0.72, colour)


def _render_icon_master(kit, relative, brand):
    from PIL import Image
    from gen_logo import raster
    source = os.path.join(kit, relative.replace("/", os.sep))
    logo = brand.get("logo") or {}
    canvas_width = float(logo.get("canvas_width", logo.get("grid", 1000)))
    canvas_height = float(logo.get("canvas_height", logo.get("grid", 1000)))
    with tempfile.TemporaryDirectory(prefix="icon-authority-") as temporary:
        rendered = os.path.join(temporary, "rendered.png")
        raster((["-w", "1024"] if canvas_width >= canvas_height else ["-h", "1024"])
               + [source, "-o", rendered])
        with Image.open(rendered) as source_image:
            rgba = source_image.convert("RGBA")
            rgba.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            square = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
            square.alpha_composite(rgba, ((1024 - rgba.width) // 2, (1024 - rgba.height) // 2))
            return square


def _container_png_payloads(path, kind):
    payload = Path(path).read_bytes()
    results = []
    if kind == "ico":
        count = struct.unpack("<H", payload[4:6])[0]
        for index in range(count):
            offset = 6 + index * 16
            size = payload[offset] or 256
            length, start = struct.unpack("<II", payload[offset + 8:offset + 16])
            image = payload[start:start + length]
            if not image.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("ICO identity frame is not PNG encoded")
            results.append((size, image))
        return results
    offset = 8
    mapping = {b"icp4": 16, b"icp5": 32, b"icp6": 64, b"ic07": 128,
               b"ic08": 256, b"ic09": 512, b"ic10": 1024}
    while offset < len(payload):
        code = payload[offset:offset + 4]
        length = struct.unpack(">I", payload[offset + 4:offset + 8])[0]
        if code in mapping:
            image = payload[offset + 8:offset + length]
            if not image.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("ICNS identity frame is not PNG encoded")
            results.append((mapping[code], image))
        offset += length
    return results


def c_icon_suites(kit, brand, rep):
    manifest_path = os.path.join(kit, "icons", "manifest.json")
    try:
        capabilities = load_capabilities(kit)
    except Exception as error:
        return rep.bad("icon-suites", "capability record unavailable: %s" % error)
    if not os.path.isfile(manifest_path):
        return rep.bad("icon-suites", "icons/manifest.json is missing")
    problems = []
    try:
        with open(manifest_path, encoding="utf-8") as handle:
            manifest = json.load(handle)
    except Exception as error:
        return rep.bad("icon-suites", "icons/manifest.json cannot be parsed: %s" % error)
    if manifest.get("schema_version") != "1.0.0":
        problems.append("manifest schema_version must be 1.0.0")
    if manifest.get("brand") != brand.get("slug"):
        problems.append("manifest brand does not match brand.json")
    expected_profile = application_icon_profile(brand)
    if manifest.get("profile") != expected_profile:
        problems.append("manifest profile does not match the effective brand contract")
    expected_masters = {
        "full": "logos/svg/%s-mark-color.svg" % brand.get("slug"),
        "reduced": "logos/svg/%s-mark-reduced-color.svg" % brand.get("slug"),
        "monochrome": "logos/svg/%s-mark-white.svg" % brand.get("slug"),
    }
    if manifest.get("source_masters") != expected_masters:
        problems.append("manifest source_masters do not match generated logo masters")
    else:
        try:
            with open(os.path.join(kit, "logos", "provenance.json"), encoding="utf-8") as handle:
                logo_paths = {item["path"] for item in json.load(handle).get("derivatives", [])}
            if not set(expected_masters.values()).issubset(logo_paths):
                problems.append("icon source_masters are absent from verified logo provenance")
        except Exception as error:
            problems.append("icon source_masters cannot be matched to logo provenance: %s" % error)
    authoritative = (brand.get("logo") or {}).get("source_mode") == "authoritative"
    identity_masters = {}
    if authoritative and capabilities.get("svg_raster"):
        try:
            for variant, master in expected_masters.items():
                identity_masters[variant] = _render_icon_master(kit, master, brand)
        except Exception as error:
            problems.append("authoritative icon masters cannot be loaded: %s" % error)
    expected_suites = {"web", "android", "apple-ios", "apple-macos", "windows"}
    suites = manifest.get("suites")
    if not isinstance(suites, list) or {row.get("id") for row in suites if isinstance(row, dict)} != expected_suites:
        problems.append("manifest must declare exactly the five platform suites")
        suites = []
    raster = bool(capabilities.get("svg_raster"))
    for suite in suites:
        if raster and suite.get("status") != "generated":
            problems.append("%s suite is not generated at raster tier" % suite.get("id"))
        if not raster and suite.get("id") != "web" and suite.get("status") != "skipped":
            problems.append("%s suite must record a core-tier skip" % suite.get("id"))
        for field in ("root", "readme", "manifest"):
            value = suite.get(field)
            if not isinstance(value, str) or not value:
                problems.append("%s suite lacks %s" % (suite.get("id"), field))
            elif not os.path.isfile(os.path.join(kit, value.replace("/", os.sep))) and field != "root":
                problems.append("%s suite %s is missing: %s" % (suite.get("id"), field, value))
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        problems.append("manifest artifacts must be a list")
        artifacts = []
    seen = set()
    declared = set()
    for index, item in enumerate(artifacts):
        if not isinstance(item, dict):
            problems.append("artifact %d is not an object" % index)
            continue
        relative = item.get("path")
        if not isinstance(relative, str) or not relative or "\\" in relative or os.path.isabs(relative):
            problems.append("artifact %d has an unsafe path" % index)
            continue
        normalized = os.path.normpath(relative).replace("\\", "/")
        if normalized.startswith("../") or normalized != relative or not relative.startswith("icons/"):
            problems.append("artifact has an unsafe path or non-normalized path: %s" % relative)
            continue
        if relative in seen:
            problems.append("duplicate artifact path: %s" % relative)
            continue
        seen.add(relative)
        declared.add(relative)
        path = os.path.join(kit, relative.replace("/", os.sep))
        if not os.path.isfile(path):
            problems.append("missing artifact: %s" % relative)
            continue
        fmt = item.get("format")
        if fmt == "png":
            try:
                info = inspect_png(path)
                expected = (item.get("width"), item.get("height"))
                if info["size"] != expected:
                    problems.append("%s dimensions %s, expected %s" % (relative, info["size"], expected))
                if info["mode"] != "RGBA":
                    problems.append("%s color mode %s, expected RGBA" % (relative, info["mode"]))
                if not info["srgb"]:
                    problems.append("%s lacks an sRGB declaration" % relative)
                if info["visible_bbox"] is None:
                    problems.append("%s has no visible pixels" % relative)
                if item.get("alpha") == "opaque" and info["has_transparency"]:
                    problems.append("%s must be opaque" % relative)
                if item.get("alpha") == "transparent" and not info["has_transparency"]:
                    problems.append("%s must preserve transparency" % relative)
                plated_roles = {"favicon", "apple-touch", "installable", "legacy-launcher", "play-store", "app-icon", "asset-catalog-icon", "iconset-icon", "msix-scale", "store-logo"}
                if item.get("role") == "target-size" and item.get("appearance") == "default":
                    plated_roles.add("target-size")
                if item.get("role") in plated_roles and item.get("alpha") == "opaque":
                    plate = "#000000" if item.get("appearance") == "dark" else "#FFFFFF" if item.get("appearance") == "tinted" else expected_profile["background"]
                    content = inspect_png(path, plate)["content_bbox"]
                    ratio = 0.75 if item.get("role") == "play-store" else 0.72
                    inset = max(0, int(item.get("width") * (1.0 - ratio) / 2.0) - 2)
                    if content is None or content[0] < inset or content[1] < inset or content[2] > item.get("width") - inset or content[3] > item.get("height") - inset:
                        problems.append("%s artwork exceeds its declared safe area: %s" % (relative, content))
                if authoritative and identity_masters:
                    from PIL import Image
                    expected_identity = _expected_authoritative_icon(item, identity_masters, expected_profile)
                    if expected_identity is not None:
                        with Image.open(path) as actual_identity:
                            if not _same_rgba(expected_identity, actual_identity):
                                problems.append("%s identity pixels disagree with declared %s master" %
                                                (relative, item.get("source_variant")))
            except Exception as error:
                problems.append("%s cannot be decoded as PNG: %s" % (relative, error))
        elif fmt == "json":
            try:
                with open(path, encoding="utf-8") as handle:
                    json.load(handle)
            except Exception as error:
                problems.append("%s cannot be parsed as JSON: %s" % (relative, error))
        elif fmt == "xml":
            try:
                ET.parse(path)
            except Exception as error:
                problems.append("%s cannot be parsed as XML: %s" % (relative, error))
        elif fmt == "svg":
            try:
                with open(path, encoding="utf-8") as handle:
                    text = handle.read()
                svg_root = ET.fromstring(text)
                for reference in re.findall(r'(?:href|xlink:href)=["\']([^"\']+)', text):
                    if not reference.startswith("data:") and not reference.startswith("#"):
                        problems.append("%s has a non-contained SVG dependency: %s" % (relative, reference))
                if authoritative and item.get("source_variant") in expected_masters:
                    images = [node for node in svg_root.iter() if node.tag.rsplit("}", 1)[-1] == "image"]
                    href = None if len(images) != 1 else images[0].get("href")
                    master = os.path.join(kit, expected_masters[item["source_variant"]].replace("/", os.sep))
                    expected_href = "data:image/svg+xml;base64," + base64.b64encode(Path(master).read_bytes()).decode("ascii")
                    if href != expected_href:
                        problems.append("%s does not embed its declared authoritative SVG master" % relative)
            except Exception as error:
                problems.append("%s cannot be parsed as SVG: %s" % (relative, error))
        elif fmt in {"ico", "icns"} and authoritative and identity_masters:
            try:
                from PIL import Image
                kind = fmt
                for size, payload in _container_png_payloads(path, kind):
                    variant = "full" if kind == "icns" or size > expected_profile["reduced_below_px"] else "reduced"
                    expected_identity = _expected_authoritative_icon(
                        {"source_variant": variant, "width": size, "role": "favicon", "appearance": "default"},
                        identity_masters, expected_profile)
                    with Image.open(BytesIO(payload)) as actual_identity:
                        if not _same_rgba(expected_identity, actual_identity):
                            problems.append("%s %d px frame disagrees with declared %s master" %
                                            (relative, size, variant))
            except Exception as error:
                problems.append("%s identity frames cannot be verified: %s" % (relative, error))
    for suite in suites:
        suite_id = suite.get("id")
        platform_path = os.path.join(kit, str(suite.get("manifest", "")).replace("/", os.sep))
        try:
            with open(platform_path, encoding="utf-8") as handle:
                platform_manifest = json.load(handle)
            expected_entries = [item for item in artifacts if item.get("platform") == suite_id and item.get("role") not in {"icon-index", "platform-manifest"}]
            if platform_manifest.get("schema_version") != manifest.get("schema_version") or platform_manifest.get("brand") != manifest.get("brand") or platform_manifest.get("platform") != suite_id or platform_manifest.get("status") != suite.get("status") or platform_manifest.get("reason") != suite.get("reason") or platform_manifest.get("source_masters") != manifest.get("source_masters") or platform_manifest.get("artifacts") != expected_entries:
                problems.append("%s does not agree with the top-level icon manifest" % suite.get("manifest"))
        except Exception as error:
            problems.append("%s cannot be validated against the top-level manifest: %s" % (suite.get("manifest"), error))
    actual = set()
    icons_root = os.path.join(kit, "icons")
    for path in walk(icons_root):
        relative = os.path.relpath(path, kit).replace(os.sep, "/")
        if relative != "icons/manifest.json":
            actual.add(relative)
    if declared != actual:
        missing = sorted(declared - actual)
        extra = sorted(actual - declared)
        if missing:
            problems.append("manifest declares missing icon files: %s" % ", ".join(missing[:6]))
        if extra:
            problems.append("undeclared icon files: %s" % ", ".join(extra[:6]))
    aliases = manifest.get("aliases")
    if not isinstance(aliases, dict):
        problems.append("manifest aliases must be an object")
        aliases = {}
    expected_aliases = {}
    for path in _expected_icon_paths(raster):
        if path.startswith("icons/web/") and path.count("/") == 2 and os.path.basename(path) not in {"README.md", "manifest.json"}:
            expected_aliases["favicons/%s" % os.path.basename(path)] = path
    if aliases != expected_aliases:
        problems.append("required favicon aliases do not match the authoritative web suite")
    actual_aliases = set()
    legacy_root = os.path.join(kit, "favicons")
    if os.path.isdir(legacy_root):
        actual_aliases = {os.path.relpath(path, kit).replace(os.sep, "/") for path in walk(legacy_root)}
    if actual_aliases != set(aliases):
        problems.append("favicons compatibility inventory does not match aliases")
    for alias, target in aliases.items():
        if not alias.startswith("favicons/") or target not in declared:
            problems.append("unsafe or unknown alias mapping: %s -> %s" % (alias, target))
            continue
        alias_path = os.path.join(kit, alias.replace("/", os.sep))
        target_path = os.path.join(kit, target.replace("/", os.sep))
        if not os.path.isfile(alias_path):
            problems.append("compatibility alias differs from authoritative target: %s" % alias)
            continue
        with open(alias_path, "rb") as alias_handle, open(target_path, "rb") as target_handle:
            if alias_handle.read() != target_handle.read():
                problems.append("compatibility alias differs from authoritative target: %s" % alias)
    absent = sorted(_expected_icon_paths(raster) - declared)
    if absent:
        problems.append("required platform artifacts are absent: %s" % ", ".join(absent[:12]))
    if raster:
        try:
            for relative in ("icons/web/favicon.ico", "icons/windows/classic/app.ico"):
                sizes = _container_sizes(os.path.join(kit, relative.replace("/", os.sep)), "ico")
                if sizes != list(ICO_SIZES):
                    problems.append("%s entries %s, expected %s" % (relative, sizes, list(ICO_SIZES)))
            icns_sizes = _container_sizes(os.path.join(kit, "icons", "apple", "macos", "AppIcon.icns"), "icns")
            expected_icns = sorted({points * scale for points, scale in MAC_ROLES})
            if icns_sizes != expected_icns:
                problems.append("AppIcon.icns entries %s, expected %s" % (icns_sizes, expected_icns))
        except Exception as error:
            problems.append("native icon container is invalid: %s" % error)
        foreground = os.path.join(kit, "icons", "android", "app", "src", "main", "res", "drawable-nodpi", "ic_launcher_foreground.png")
        try:
            box = inspect_png(foreground)["visible_bbox"]
            if box is None or box[0] < 83 or box[1] < 83 or box[2] > 349 or box[3] > 349:
                problems.append("Android adaptive foreground exceeds the central 66-unit safe zone: %s" % (box,))
        except Exception as error:
            problems.append("Android adaptive foreground cannot be inspected: %s" % error)
        play = os.path.join(kit, "icons", "android", "play-store", "google-play-512.png")
        if os.path.isfile(play) and os.path.getsize(play) > 1024 * 1024:
            problems.append("Google Play artwork exceeds 1,024 KB")
        _validate_apple_catalogs(kit, problems)
        _validate_windows_manifest_fragments(kit, brand, expected_profile, problems)
    if problems:
        rep.bad("icon-suites", "; ".join(problems[:30]))
    else:
        generated = sum(1 for suite in suites if suite.get("status") == "generated")
        rep.ok("icon-suites", "%d platform suites, %d declared artifacts, %d compatibility aliases" %
               (generated, len(artifacts), len(aliases)))

def c_pdf(kit, rep):
    pdfs = [p for p in walk(kit) if p.lower().endswith(".pdf")]
    if not pdfs: return rep.skip("pdf-fonts-embedded", "no PDF in kit")
    try: import pikepdf
    except ImportError: return rep.skip("pdf-fonts-embedded", "pikepdf not installed")
    bad, type3 = [], 0
    for p in pdfs:
        with pikepdf.open(p) as pdf:
            for pno, page in enumerate(pdf.pages, 1):
                for _, f in (page.get("/Resources", {}) or {}).get("/Font", {}).items():
                    # A Type3 font carries its glyphs inline in /CharProcs and has no
                    # /FontFile by construction. It is embedded; treating it as a
                    # failure is a false positive. Its presence is still worth
                    # reporting, because Chromium emits Type3 when it falls back.
                    if str(f.get("/Subtype")) == "/Type3":
                        if "/CharProcs" in f: type3 += 1; continue
                        bad.append("%s p%d: Type3 with no /CharProcs" % (os.path.relpath(p, kit), pno))
                        continue
                    d = f.get("/FontDescriptor") or (f.get("/DescendantFonts", [{}])[0].get("/FontDescriptor")
                                                     if f.get("/DescendantFonts") else None)
                    if d is None:
                        bad.append("%s p%d: %s has no descriptor" % (os.path.relpath(p, kit), pno, f.get("/BaseFont")))
                    elif not any(k in d for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                        bad.append("%s p%d: %s not embedded" % (os.path.relpath(p, kit), pno, f.get("/BaseFont")))
    note = "" if not type3 else "; %d Type3 glyph fonts (inline CharProcs, embedded; usually a renderer fallback)" % type3
    rep.bad("pdf-fonts-embedded", "; ".join(sorted(set(bad))[:6]) + note) if bad else \
        rep.ok("pdf-fonts-embedded", "%d PDFs, all fonts embedded%s" % (len(pdfs), note))

def c_manifest(kit, rep):
    mp = os.path.join(kit, "manifest.json")
    if not os.path.exists(mp): return rep.skip("manifest-checksums", "manifest.json not present")
    man = json.load(open(mp, encoding="utf-8")); bad = []
    for e in man.get("files", []):
        fp = os.path.join(kit, e["path"])
        if not os.path.exists(fp): bad.append("%s: missing" % e["path"]); continue
        b = open(fp, "rb").read()
        if hashlib.sha256(b).hexdigest() != e.get("sha256"): bad.append("%s: sha256 mismatch" % e["path"])
        elif e.get("bytes") is not None and len(b) != e["bytes"]: bad.append("%s: size mismatch" % e["path"])
    rep.bad("manifest-checksums", "; ".join(bad[:8])) if bad else \
        rep.ok("manifest-checksums", "%d files match" % len(man.get("files", [])))


def c_capability_artifacts(kit, rep):
    try:
        capabilities = load_capabilities(kit)
    except Exception as error:
        return rep.bad("capability-tier", str(error))
    tier = capabilities["tier"]
    rep.ok("capability-tier", "%s tier recorded by probe.py" % tier)

    logo_png_dir = os.path.join(kit, "logos", "png")
    pngs = ([os.path.join(logo_png_dir, name) for name in os.listdir(logo_png_dir)
             if name.lower().endswith(".png")] if os.path.isdir(logo_png_dir) else [])
    ico = os.path.join(kit, "favicons", "favicon.ico")
    if capabilities.get("svg_raster"):
        if not pngs:
            rep.bad("raster-artifacts", "probe found a rasterizer but PNG exports are missing")
        else:
            rep.ok("raster-artifacts", "%d logo PNGs produced" % len(pngs))
    else:
        rep.skip("raster-artifacts", "core tier: %s; PNG outputs skipped"
                 % capabilities.get("raster_reason", "required raster capability unavailable"))

    if not capabilities.get("svg_raster"):
        rep.skip("ico-artifact", "%s tier: source PNGs unavailable; ICO skipped" % tier)
    elif os.path.isfile(ico):
        rep.ok("ico-artifact", "favicon.ico produced by the deterministic icon writer")
    else:
        rep.bad("ico-artifact", "raster capability is available but favicon.ico is missing")

    pdf = os.path.join(kit, "brand-guide.pdf")
    if tier == "full":
        if os.path.isfile(pdf):
            rep.ok("brand-guide-artifact", "PDF produced after successful Chromium probe")
        else:
            rep.bad("brand-guide-artifact", "Chromium probe passed but brand-guide.pdf is missing")
    else:
        rep.skip("brand-guide-artifact", "%s tier: headless Chromium unavailable; PDF skipped" % tier)


def _paeth(left, above, upper_left):
    estimate = left + above - upper_left
    distances = (abs(estimate - left), abs(estimate - above), abs(estimate - upper_left))
    return (left, above, upper_left)[distances.index(min(distances))]


def _png_mask(payload, method):
    """Return (width, height, binary mask) for a non-interlaced RGBA8 PNG."""
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("authoritative mask source is not a PNG")
    position, header, compressed = 8, None, []
    while position < len(payload):
        length = struct.unpack(">I", payload[position:position + 4])[0]
        kind = payload[position + 4:position + 8]
        data = payload[position + 8:position + 8 + length]
        if kind == b"IHDR":
            header = data
        elif kind == b"IDAT":
            compressed.append(data)
        elif kind == b"IEND":
            break
        position += 12 + length
    if header is None or not compressed:
        raise ValueError("authoritative PNG is incomplete")
    width, height, depth, colour_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", header)
    if (depth, colour_type, compression, filtering, interlace) != (8, 6, 0, 0, 0):
        raise ValueError("authoritative PNG must be non-interlaced RGBA8")
    stride = width * 4
    raw = zlib.decompress(b"".join(compressed))
    if len(raw) != height * (stride + 1):
        raise ValueError("authoritative PNG has an unexpected data length")
    previous, offset, mask = bytearray(stride), 0, bytearray()
    for _row in range(height):
        filter_type = raw[offset]
        scanline = bytearray(raw[offset + 1:offset + stride + 1])
        offset += stride + 1
        for index in range(stride):
            left = scanline[index - 4] if index >= 4 else 0
            above = previous[index]
            upper_left = previous[index - 4] if index >= 4 else 0
            if filter_type == 1:
                scanline[index] = (scanline[index] + left) & 0xff
            elif filter_type == 2:
                scanline[index] = (scanline[index] + above) & 0xff
            elif filter_type == 3:
                scanline[index] = (scanline[index] + ((left + above) // 2)) & 0xff
            elif filter_type == 4:
                scanline[index] = (scanline[index] + _paeth(left, above, upper_left)) & 0xff
            elif filter_type != 0:
                raise ValueError("authoritative PNG uses an unknown filter")
        for index in range(0, stride, 4):
            red, green, blue, alpha = scanline[index:index + 4]
            if method == "luminance":
                alpha = round(alpha * max(red, green, blue) / 255)
            mask.append(255 if alpha else 0)
        previous = scanline
    return width, height, bytes(mask)


def _png_matches_svg(kit, relative, brand):
    """Independently rerender a logo PNG from its verified SVG master."""
    match = re.fullmatch(r"logos/png/(.+)-(1024|1280)\.png", relative)
    if not match:
        raise ValueError("logo PNG name does not identify its SVG master")
    svg_path = os.path.join(kit, "logos", "svg", match.group(1) + ".svg")
    if not os.path.isfile(svg_path):
        raise ValueError("corresponding SVG master is missing")
    width = int(match.group(2))
    from PIL import Image
    from gen_logo import raster, standalone_mark_ratio
    from iconkit import contain_visible
    with tempfile.TemporaryDirectory(prefix="logo-provenance-") as temporary:
        rendered = os.path.join(temporary, "rendered.png")
        expected_path = os.path.join(temporary, "expected.png")
        standalone = match.group(1).startswith(brand["slug"] + "-mark-")
        raster((["-h", str(width)] if standalone else ["-w", str(width)])
               + [svg_path, "-o", rendered])
        with Image.open(rendered) as source:
            expected = (contain_visible(source.convert("RGBA"), width, standalone_mark_ratio(brand))
                        if standalone else source.convert("RGBA"))
            expected.save(expected_path)
        with Image.open(expected_path) as expected, Image.open(os.path.join(kit, relative.replace("/", os.sep))) as actual:
            return _same_rgba(expected, actual)


def _square_knockout_problems(root, enclosure):
    """Return structural failures for a locally bounded square knockout."""
    local_name = lambda node: node.tag.rsplit("}", 1)[-1]
    masks = [node for node in root.iter()
             if local_name(node) == "mask" and node.get("id", "").endswith("-square-knockout")]
    if len(masks) != 1:
        return ["square-knockout mask count must be exactly one"]
    mask = masks[0]
    canvas = float(enclosure["canvas_size"])
    required = {
        "maskUnits": "userSpaceOnUse",
        "maskContentUnits": "userSpaceOnUse",
        "x": 0.0,
        "y": 0.0,
        "width": canvas,
        "height": canvas,
    }
    failures = []
    for name, expected in required.items():
        actual = mask.get(name)
        try:
            matches = actual == expected if isinstance(expected, str) else float(actual) == expected
        except (TypeError, ValueError):
            matches = False
        if not matches:
            failures.append("square-knockout mask %s must be %s" % (name, expected))
    reference = "url(#%s)" % mask.get("id")
    targets = [node for node in root.iter()
               if local_name(node) == "rect" and node.get("mask") == reference]
    if len(targets) != 1:
        failures.append("square-knockout mask must be referenced by exactly one enclosure rectangle")
    elif all(mask.get(name) is not None for name in ("x", "y", "width", "height")):
        target = targets[0]
        try:
            mask_box = (float(mask.get("x")), float(mask.get("y")),
                        float(mask.get("x")) + float(mask.get("width")),
                        float(mask.get("y")) + float(mask.get("height")))
            target_box = (float(target.get("x", 0)), float(target.get("y", 0)),
                          float(target.get("x", 0)) + float(target.get("width")),
                          float(target.get("y", 0)) + float(target.get("height")))
            if (target_box[0] < mask_box[0] or target_box[1] < mask_box[1]
                    or target_box[2] > mask_box[2] or target_box[3] > mask_box[3]):
                failures.append("square-knockout mask does not cover its enclosure rectangle")
        except (TypeError, ValueError):
            failures.append("square-knockout mask or enclosure rectangle has invalid bounds")
    return failures


def _monochrome_lockup_geometry_problems(kit, root, brand, item):
    """Compare a square monochrome lockup with its declared mark and wordmark geometry."""
    local_name = lambda node: node.tag.rsplit("}", 1)[-1]
    components = {name: [node for node in root.iter()
                         if node.get("data-lockup-component") == name]
                  for name in ("mark", "wordmark")}
    failures = []
    for name in components:
        if len(components[name]) != 1:
            failures.append("lockup must contain exactly one declared %s component" % name)
    if failures:
        return failures

    logo = brand.get("logo") or {}
    paths = logo.get("paths") or {}
    contextual = logo.get("contextual_variants") or {}
    selected = contextual.get(item["colourway"])
    variant = "single-ink" if selected == "single-ink" else item.get("variant") or "full"
    expected_items = paths.get(variant) or paths.get("full") or []
    enclosure = logo.get("square_enclosure") or {}
    if enclosure.get("monochrome_knockout"):
        knockout_role = enclosure.get("knockout_role")
        knockout = [entry for entry in expected_items
                    if entry.get("role", "accent") == knockout_role]
        expected_items = knockout or expected_items
    expected_mark = sorted(entry.get("d") for entry in expected_items
                           if entry.get("element", "path") == "path" and entry.get("d"))
    actual_mark = sorted(node.get("d") for node in components["mark"][0].iter()
                         if local_name(node) == "path" and node.get("d"))
    if not expected_mark or actual_mark != expected_mark:
        failures.append("lockup mark paths disagree with the declared %s geometry" % variant)

    wordmark_path = os.path.join(kit, "logos", "svg", "%s-wordmark-%s.svg" %
                                 (brand["slug"], item["colourway"]))
    try:
        wordmark_root = ET.parse(wordmark_path).getroot()
        wordmark_components = [node for node in wordmark_root.iter()
                               if node.get("data-lockup-component") == "wordmark"]
        expected_wordmark = sorted(node.get("d") for node in wordmark_components[0].iter()
                                   if local_name(node) == "path" and node.get("d"))
    except (IndexError, OSError, ET.ParseError):
        expected_wordmark = []
    actual_wordmark = sorted(node.get("d") for node in components["wordmark"][0].iter()
                             if local_name(node) == "path" and node.get("d"))
    if not expected_wordmark or actual_wordmark != expected_wordmark:
        failures.append("lockup wordmark paths disagree with its generated wordmark master")
    return failures


def _transformed_rect_bounds(root, rect):
    """Resolve the generator's translate and scale ancestors for a rectangle."""
    parent = {child: node for node in root.iter() for child in node}
    chain, node = [], rect
    while node in parent:
        node = parent[node]
        chain.append(node)
    x = float(rect.get("x", 0))
    y = float(rect.get("y", 0))
    points = [(x, y), (x + float(rect.get("width")), y + float(rect.get("height")))]
    for ancestor in chain:
        transform = ancestor.get("transform")
        if not transform:
            continue
        operations = re.findall(r"(translate|scale)\(([^)]+)\)", transform)
        if "".join("%s(%s)" % item for item in operations).replace(" ", "") != transform.replace(" ", ""):
            raise ValueError("square enclosure has an unsupported ancestor transform")
        for operation, arguments in reversed(operations):
            values = [float(value) for value in re.split(r"[ ,]+", arguments.strip())]
            if operation == "translate":
                dx, dy = values[0], values[1] if len(values) > 1 else 0.0
                points = [(px + dx, py + dy) for px, py in points]
            else:
                sx, sy = values[0], values[1] if len(values) > 1 else values[0]
                points = [(px * sx, py * sy) for px, py in points]
    return points


def _monochrome_lockup_mark_complete(kit, relative):
    """Measure that a rendered monochrome lockup spans its declared square mark."""
    match = re.fullmatch(r"logos/png/(.+)-(1024|1280)\.png", relative)
    if not match:
        raise ValueError("logo PNG name does not identify its SVG master")
    svg_path = os.path.join(kit, "logos", "svg", match.group(1) + ".svg")
    root = ET.parse(svg_path).getroot()
    rects = [node for node in root.iter()
             if node.tag.rsplit("}", 1)[-1] == "rect" and node.get("mask", "").startswith("url(#")]
    if len(rects) != 1:
        raise ValueError("SVG master lacks one measurable square-knockout target")
    points = _transformed_rect_bounds(root, rects[0])
    view_box = [float(value) for value in root.get("viewBox", "").split()]
    if len(view_box) != 4:
        raise ValueError("SVG master has an invalid viewBox")
    from PIL import Image
    with Image.open(os.path.join(kit, relative.replace("/", os.sep))) as image:
        alpha = image.convert("RGBA").getchannel("A")
        scale_x = image.width / view_box[2]
        scale_y = image.height / view_box[3]
        left = max(0, int((min(point[0] for point in points) - view_box[0]) * scale_x))
        top = max(0, int((min(point[1] for point in points) - view_box[1]) * scale_y))
        right = min(image.width, int((max(point[0] for point in points) - view_box[0]) * scale_x + 0.9999))
        bottom = min(image.height, int((max(point[1] for point in points) - view_box[1]) * scale_y + 0.9999))
        bounds = alpha.crop((left, top, right, bottom)).getbbox()
    return bool(bounds and (bounds[2] - bounds[0]) >= (right - left) * 0.8
                and (bounds[3] - bounds[1]) >= (bottom - top) * 0.8)


def _transformed_image_bounds(root, image):
    """Resolve the generator's translate and uniform-scale ancestors."""
    parent = {child: node for node in root.iter() for child in node}
    chain, node = [], image
    while node in parent:
        node = parent[node]
        chain.append(node)
    points = [
        (float(image.get("x", 0)), float(image.get("y", 0))),
        (float(image.get("x", 0)) + float(image.get("width")), float(image.get("y", 0)) + float(image.get("height"))),
    ]
    for ancestor in chain:
        transform = ancestor.get("transform")
        if not transform:
            continue
        operations = re.findall(r"(translate|scale)\(([^)]+)\)", transform)
        if "".join("%s(%s)" % item for item in operations).replace(" ", "") != transform.replace(" ", ""):
            raise ValueError("authoritative image has an unsupported ancestor transform")
        for operation, arguments in reversed(operations):
            values = [float(value) for value in re.split(r"[ ,]+", arguments.strip())]
            if operation == "translate":
                dx, dy = values[0], values[1] if len(values) > 1 else 0.0
                points = [(x + dx, y + dy) for x, y in points]
            else:
                sx, sy = values[0], values[1] if len(values) > 1 else values[0]
                if abs(sx - sy) > 1e-9 or sx <= 0:
                    raise ValueError("authoritative image has a non-uniform or non-positive scale")
                points = [(x * sx, y * sy) for x, y in points]
    return points


def _authoritative_identity_unobscured(svg_path, root):
    """Render the identity layer alone and prove later SVG content does not cover it."""
    isolated = copy.deepcopy(root)
    isolated_image = next(node for node in isolated.iter()
                          if node.tag.rsplit("}", 1)[-1] == "image")
    parents = {child: node for node in isolated.iter() for child in node}
    keep, node = {isolated, isolated_image}, isolated_image
    while node in parents:
        node = parents[node]
        keep.add(node)
    for parent in list(isolated.iter()):
        for child in list(parent):
            if child not in keep:
                parent.remove(child)

    from PIL import Image
    from gen_logo import raster
    with tempfile.TemporaryDirectory(prefix="logo-visibility-") as temporary:
        identity_svg = os.path.join(temporary, "identity.svg")
        identity_png = os.path.join(temporary, "identity.png")
        complete_png = os.path.join(temporary, "complete.png")
        ET.ElementTree(isolated).write(identity_svg, encoding="utf-8", xml_declaration=True)
        raster(["-w", "512", identity_svg, "-o", identity_png])
        raster(["-w", "512", svg_path, "-o", complete_png])
        with Image.open(identity_png) as identity_file, Image.open(complete_png) as complete_file:
            identity = identity_file.convert("RGBA")
            complete = complete_file.convert("RGBA")
            if identity.size != complete.size:
                return False
            identity_pixels = identity.load()
            complete_pixels = complete.load()
            opaque = 0
            for y in range(identity.height):
                for x in range(identity.width):
                    expected = identity_pixels[x, y]
                    if expected[3] == 255:
                        opaque += 1
                        actual = complete_pixels[x, y]
                        if actual[3] != 255 or actual[:3] != expected[:3]:
                            return False
            if opaque:
                return True
            return _same_rgba(identity, complete)


def c_logo_provenance(kit, brand, rep):
    """Verify the generated logo inventory against the source authority contract."""
    path = os.path.join(kit, "logos", "provenance.json")
    if not os.path.isfile(path):
        return rep.bad("logo-provenance", "logos/provenance.json is missing")
    try:
        with open(path, encoding="utf-8") as handle:
            provenance = json.load(handle)
        authority = logo_source_contract(brand, kit)
    except Exception as error:
        return rep.bad("logo-provenance", str(error))

    problems = []
    capabilities = load_capabilities(kit)
    if provenance.get("schema_version") != 1 or provenance.get("brand") != brand.get("slug"):
        problems.append("index identity or schema version is invalid")
    if provenance.get("source_mode") != authority["source_mode"]:
        problems.append("index source mode disagrees with brand contract")
    records = provenance.get("derivatives")
    if not isinstance(records, list):
        return rep.bad("logo-provenance", "derivatives must be an array")
    paths = [item.get("path") for item in records if isinstance(item, dict)]
    if len(paths) != len(records) or paths != sorted(paths) or len(paths) != len(set(paths)):
        problems.append("derivative paths must be complete, unique, and sorted")
    actual = []
    for directory, suffix in (("logos/svg", ".svg"), ("logos/png", ".png")):
        root = os.path.join(kit, directory.replace("/", os.sep))
        if os.path.isdir(root):
            actual.extend("%s/%s" % (directory, name) for name in os.listdir(root)
                          if name.lower().endswith(suffix))
    if set(paths) != set(actual):
        missing = sorted(set(actual) - set(paths))
        extra = sorted(set(paths) - set(actual))
        if missing:
            problems.append("unindexed logo derivatives: %s" % ", ".join(missing[:6]))
        if extra:
            problems.append("provenance names absent derivatives: %s" % ", ".join(extra[:6]))

    expected_keys = {"path", "kind", "variant", "colourway", "source_mode", "input_id",
                     "source_sha256", "sha256", "transformations", "embedded_metadata"}
    checked_sources = set()
    for item in records:
        if not isinstance(item, dict) or set(item) != expected_keys:
            problems.append("derivative record has invalid fields")
            continue
        relative = item["path"]
        variant = item["variant"]
        source = authority.get(variant) if variant in {"full", "reduced"} else None
        if source:
            record = source["record"]
            base_transform = "embed-unchanged" if record["format"] == "svg" else "recolor-mask"
            expected = [base_transform, "resize"]
            if item["kind"] == "lockup":
                expected.append("place-in-lockup")
            if item["source_mode"] != "authoritative" or item["input_id"] != record["id"] or item["source_sha256"] != record["sha256"]:
                problems.append("%s has stale or conflicting source identity" % relative)
            if item["transformations"] != expected or not set(expected).issubset(set(record["approved_transformations"])):
                problems.append("%s has undeclared or misordered transformations" % relative)
        elif item["input_id"] is not None or item["source_sha256"] is not None or item["transformations"]:
            problems.append("%s claims source lineage without a bound logo variant" % relative)

        output = os.path.join(kit, relative.replace("/", os.sep))
        if not os.path.isfile(output):
            continue
        if not re.fullmatch(r"[0-9a-f]{64}", item["sha256"] or ""):
            problems.append("%s has an invalid derivative SHA-256" % relative)
        elif sha256_file(output) != item["sha256"]:
            problems.append("%s derivative bytes disagree with provenance" % relative)
        if relative.endswith(".png"):
            if capabilities.get("svg_raster"):
                try:
                    if not _png_matches_svg(kit, relative, brand):
                        problems.append("%s pixels disagree with its verified SVG master" % relative)
                except Exception as error:
                    problems.append("%s cannot be compared with its SVG master: %s" % (relative, error))
            enclosure = (brand.get("logo") or {}).get("square_enclosure")
            if (enclosure and enclosure.get("monochrome_knockout") and item["kind"] == "lockup"
                    and item["colourway"] in {"black", "white"} and capabilities.get("pillow_composite")):
                try:
                    if not _monochrome_lockup_mark_complete(kit, relative):
                        problems.append("%s rendered square-knockout mark is clipped or incomplete" % relative)
                except Exception as error:
                    problems.append("%s rendered square-knockout mark cannot be measured: %s" % (relative, error))
            continue
        if not relative.endswith(".svg"):
            continue
        try:
            root = ET.parse(output).getroot()
            if root.get("data-logo-source-mode") != item["source_mode"]:
                problems.append("%s source-mode metadata disagrees with index" % relative)
            expected_variant = item["variant"]
            if root.get("data-logo-variant") != expected_variant:
                problems.append("%s variant metadata disagrees with index" % relative)
            enclosure = (brand.get("logo") or {}).get("square_enclosure")
            if (enclosure and enclosure.get("monochrome_knockout")
                    and item["kind"] in {"mark", "lockup"}
                    and item["colourway"] in {"black", "white"}):
                problems.extend("%s %s" % (relative, failure)
                                for failure in _square_knockout_problems(root, enclosure))
                if item["kind"] == "lockup":
                    problems.extend("%s %s" % (relative, failure)
                                    for failure in _monochrome_lockup_geometry_problems(
                                        kit, root, brand, item))
            if source:
                if root.get("data-authoritative-input-id") != source["record"]["id"] or root.get("data-authoritative-source-sha256") != source["record"]["sha256"]:
                    problems.append("%s authoritative metadata disagrees with index" % relative)
                images = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "image"]
                if len(images) != 1:
                    problems.append("%s must contain exactly one authoritative image" % relative)
                else:
                    image = images[0]
                    href = image.get("href") or image.get("{http://www.w3.org/1999/xlink}href")
                    element = source["element"]
                    expected_geometry = (float(element.get("x", 0)), float(element.get("y", 0)),
                                         float(element["width"]), float(element["height"]))
                    actual_geometry = (float(image.get("x", 0)), float(image.get("y", 0)),
                                       float(image.get("width")), float(image.get("height")))
                    if actual_geometry != expected_geometry or image.get("preserveAspectRatio") != "xMidYMid meet":
                        problems.append("%s changes the authoritative image placement" % relative)
                    forbidden = {"opacity", "display", "visibility", "style", "filter", "mask", "clip-path", "transform"}
                    if forbidden & set(image.attrib):
                        problems.append("%s hides or modifies the authoritative image presentation" % relative)
                    bounds = _transformed_image_bounds(root, image)
                    view_box = [float(value) for value in root.get("viewBox", "").split()]
                    if len(view_box) != 4 or min(x for x, _y in bounds) < view_box[0] or min(y for _x, y in bounds) < view_box[1] or max(x for x, _y in bounds) > view_box[0] + view_box[2] or max(y for _x, y in bounds) > view_box[1] + view_box[3]:
                        problems.append("%s moves authoritative identity content outside its canvas" % relative)
                    if item["kind"] == "mark":
                        visible_shapes = [node for node in root.iter() if node.tag.rsplit("}", 1)[-1] in {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}]
                        if visible_shapes:
                            problems.append("%s adds substitute geometry to an authoritative mark" % relative)
                    if capabilities.get("svg_raster") and not _authoritative_identity_unobscured(output, root):
                        problems.append("%s obscures authoritative identity pixels" % relative)
                    if source["record"]["format"] == "svg":
                        if not href or not href.startswith("data:image/svg+xml;base64,"):
                            problems.append("%s lacks embedded authoritative SVG bytes" % relative)
                        else:
                            with open(source["path"], "rb") as handle:
                                if base64.b64decode(href.split(",", 1)[1]) != handle.read():
                                    problems.append("%s changes authoritative SVG source bytes" % relative)
                    else:
                        if not href or not href.startswith("data:image/png;base64,"):
                            problems.append("%s lacks an embedded authoritative raster mask" % relative)
                        else:
                            with open(source["path"], "rb") as handle:
                                original = _png_mask(handle.read(), source["mask"])
                            derived = _png_mask(base64.b64decode(href.split(",", 1)[1]), "alpha")
                            if original != derived:
                                problems.append("%s changes authoritative %s mask topology" % (relative, variant))
                    checked_sources.add(variant)
        except Exception as error:
            problems.append("%s provenance metadata cannot be verified: %s" % (relative, error))
    approval_path = os.path.join(kit, "logos", "approval.json")
    expected_approval_records = []
    by_path = {item.get("path"): item for item in records if isinstance(item, dict)}
    for item in sorted((item for item in records if isinstance(item, dict)), key=lambda record: record.get("path", "")):
        relative = item.get("path", "")
        if relative.endswith(".svg"):
            expected_approval_records.append({"path": relative, "sha256": item.get("sha256")})
            continue
        match = re.match(r"logos/png/(.+)-[0-9]+\.png$", relative)
        source_path = "logos/svg/%s.svg" % match.group(1) if match else ""
        source = by_path.get(source_path)
        if not match or source is None:
            problems.append("%s lacks a deterministic SVG approval source" % relative)
            continue
        expected_approval_records.append({
            "path": relative,
            "rendered_from": source_path,
            "rendered_from_sha256": source.get("sha256"),
        })
    expected_approval = {"schema_version": 1, "brand": brand.get("slug"), "derivatives": expected_approval_records}
    try:
        with open(approval_path, encoding="utf-8") as handle:
            approval = json.load(handle)
        if approval != expected_approval:
            problems.append("approval manifest does not cover the verified derivative set")
    except Exception as error:
        problems.append("logos/approval.json cannot be verified: %s" % error)
    if authority["source_mode"] == "authoritative" and checked_sources != {"full", "reduced"}:
        problems.append("authoritative Full and Reduced sources were not both verified")
    if problems:
        rep.bad("logo-provenance", "; ".join(problems[:20]))
    else:
        rep.ok("logo-provenance", "%d derivatives agree with %s source contract" %
               (len(records), authority["source_mode"]))

# ---------------------------------------------------------------------- main
def c_glyph(kit, brand, rep):
    """The measured geometry gate, folded into VERIFY.md.

    `svg-viewbox` needs svgelements to resolve transforms and skips without it,
    which leaves a Core-tier build with no geometry verdict at all. This check
    has no dependency beyond the standard library, so every provider gets the
    same answer about the mark. See references/08-glyph-construction.md.
    """
    lg = (brand.get("logo") or {})
    paths = (lg.get("paths") or {}).get("full")
    if not paths:
        return rep.skip("glyph-geometry", "no logo.paths.full in brand.json")
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        sys.path.insert(0, here)
        import glyphkit as GK
        import validate_glyph as VG
    except Exception as e:
        return rep.skip("glyph-geometry", "glyphkit unavailable (%s)" % e)

    provenance = lg.get("geometry_provenance", "glyphkit")
    reason = lg.get("geometry_provenance_reason", "")
    if provenance not in {"glyphkit", "imported"}:
        return rep.bad("glyph-geometry",
                       "logo.geometry_provenance must be glyphkit or imported")
    if provenance == "imported" and not reason.strip():
        return rep.bad("glyph-geometry",
                       "imported geometry requires logo.geometry_provenance_reason")

    bad = [i for i, e in enumerate(paths)
           if e.get("element", "path") != "path"
           or not GK.path_commands_ok(e["d"])]
    if bad and provenance == "glyphkit":
        return rep.bad("glyph-geometry",
                       "path %s uses a command outside absolute M, L, C, Z; "
                       "compose the mark with glyphkit" % ", ".join(str(i) for i in bad))
    sub = VG.Report()
    grid = float(lg.get("grid", 1000))
    VG.measure(paths, grid, "full", sub, provenance=provenance,
               provenance_reason=reason)
    if (lg.get("paths") or {}).get("reduced"):
        VG.measure(lg["paths"]["reduced"], grid, "reduced", sub, reduced=True,
                   provenance=provenance, provenance_reason=reason)
    if (lg.get("paths") or {}).get("single-ink"):
        VG.measure_strokes(lg["paths"]["single-ink"], grid, "single-ink", sub)
    if sub.fails:
        rep.bad("glyph-geometry", "; ".join(
            "%s %s" % (n, d) for st, n, d in sub.rows if st == "FAIL")[:280])
    else:
        note = "%d checks clean" % len(sub.rows)
        if provenance == "imported":
            note = "imported geometry (%s); %s" % (reason, note)
        if sub.warns:
            note += ", %d warning(s): %s" % (sub.warns, "; ".join(
                n for st, n, _ in sub.rows if st == "WARN")[:120])
        rep.ok("glyph-geometry", note)


def c_aa_floor(kit, canon, brand, rep):
    """WCAG AA as a floor, not as a claim.

    c_contrast checks that a stated number matches the measured one. It passes a
    token that honestly declares 3.2:1, which is exactly how an inaccessible
    value survives a build. This check reads canon's per-colour `aa` declaration
    and enforces the floor:

      as_text_on  the colour is used as text on that surface and must clear 4.5:1
      as_fill     the colour is used as a fill and must record a legal foreground
                  that clears 4.5:1 on top of it

    NON-EXEMPTABLE. See canon accessibility.exemptions. No conformance level and
    no operator override waives a failure here; the value changes instead.
    """
    LIGHT = "#F8F8F6"
    dark = (brand.get("surfaces") or {}).get("base") or "#000000"
    colors = brand.get("color") or {}
    if not colors:
        return rep.skip("aa-floor", "brand.json carries no measured color block; run enrich_brand.py")

    # canon owns the role declarations; the kit owns the values.
    decl = {}
    for group in ("immutable", "neutral_ramp", "parent_identity_accent"):
        for name, spec in (canon["color"].get(group) or {}).items():
            if isinstance(spec, dict) and isinstance(spec.get("aa"), dict):
                decl[name] = spec["aa"]
    # the accent trio is named per brand but inherits the parent's declarations
    for kit_name, canon_name in (("accent-bright", "bright"),
                                 ("accent-deep", "deep"),
                                 ("accent-accessible", "accessible")):
        a = ((canon["color"].get("parent_identity_accent") or {}).get(canon_name) or {}).get("aa")
        if a:
            decl[kit_name] = a
    if affiliation(brand)["inheritance"] == "independent":
        decl["emphasis"] = {"as_text_on": "dark", "as_fill": False}
        decl["action"] = {"as_text_on": "light", "as_fill": True}

    fails, checked = [], 0
    for name, spec in colors.items():
        rule = decl.get(name)
        if not rule or not isinstance(spec, dict) or "hex" not in spec:
            continue
        hexv = spec["hex"]
        for surface, label in ((dark, "dark base"), (LIGHT, "light base")):
            want = rule.get("as_text_on")
            if want in (None, False):
                continue
            if want != "both" and not ((want == "dark" and surface == dark)
                                       or (want == "light" and surface == LIGHT)):
                continue
            checked += 1
            r = R(hexv, surface)
            if r < 4.5:
                fails.append("%s %s as text on the %s = %s (needs 4.5)"
                             % (name, hexv, label, r))
        if rule.get("as_fill"):
            checked += 1
            b, w = R("#000000", hexv), R("#FFFFFF", hexv)
            if max(b, w) < 4.5:
                fails.append("%s %s as a fill has no legal foreground: black %s, white %s"
                             % (name, hexv, b, w))
    if not checked:
        return rep.skip("aa-floor", "no canon-declared text or fill colours found in the kit")
    if fails:
        rep.bad("aa-floor", "; ".join(fails[:8]) + " [NON-EXEMPTABLE]")
    else:
        rep.ok("aa-floor", "%d declared text and fill roles clear AA against the real surfaces"
               % checked)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kit", nargs="?", default=".")
    ap.add_argument("--canon", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    kit = os.path.abspath(a.kit)
    here = os.path.dirname(os.path.abspath(__file__))
    canon_path = a.canon or os.path.join(here, "..", "references", "01-canon.json")
    canon = json.load(open(canon_path, encoding="utf-8"))
    bp = os.path.join(kit, "brand.json")
    if not os.path.exists(bp): bp = os.path.join(kit, "brand.spec.json")
    brand = json.load(open(bp, encoding="utf-8")) if os.path.exists(bp) else {}

    rep = Report()
    c_encoding(kit, rep)
    c_contrast(kit, brand, rep)
    c_aa_floor(kit, canon, brand, rep)
    c_accent(canon, brand, rep)
    c_immutables(canon, brand, rep)
    c_radius(kit, canon, rep)
    c_globals(kit, rep)
    c_rhetoric(kit, rep)
    c_raw_values(kit, rep)
    c_font_weights(kit, brand, rep)
    c_glyph(kit, brand, rep)
    c_logo_provenance(kit, brand, rep)
    c_capability_artifacts(kit, rep)
    c_icon_suites(kit, brand, rep)
    c_svg(kit, rep)
    c_ico(kit, rep)
    c_pdf(kit, rep)
    c_manifest(kit, rep)

    lines = ["# Verification", "",
             "Generated by `build/verify.py` against canon `%s`." % canon["version"],
             "Every number below is measured from the shipped files at run time.", "",
             "| Check | Result | Detail |", "| --- | --- | --- |"]
    for cid, st, d in rep.rows:
        lines.append("| `%s` | %s | %s |" % (cid, {"pass": "pass", "FAIL": "**FAIL**", "skip": "skip"}[st],
                                             (d or "").replace("|", "\\|")[:300]))
    lines += ["", "| | |", "| --- | ---: |",
              "| Checks run | %d |" % len(rep.rows),
              "| Skipped (inputs absent) | %d |" % len(rep.skips),
              "| **Problems found** | **%d** |" % len(rep.problems), ""]
    if rep.skips:
        lines += ["## Skipped", "", "A skip means the input was absent, never that the check passed.", ""]
        lines += ["- %s" % s for s in rep.skips] + [""]
    if rep.problems:
        lines += ["## Problems", ""] + ["- %s" % p for p in rep.problems] + [""]
    md = "\n".join(lines)
    out = a.out or os.path.join(kit, "VERIFY.md")
    with open(out, "w", encoding="utf-8", newline="\n") as f: f.write(md)
    print(md)
    sys.exit(min(len(rep.problems), 125))

if __name__ == "__main__":
    main()
