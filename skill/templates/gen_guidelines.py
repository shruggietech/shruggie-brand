#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_guidelines.py: the guidelines page, rendered from the system it documents.

Reads the SAME tokens the product ships (nextjs/globals.css), so the page and
the interface cannot drift apart. Dark by default with a light reading mode,
matching the product rather than the print guide.

Writes guidelines/index.html and, if a ui_kits directory is wanted, a demo
surface alongside it.

    python3 build/gen_guidelines.py <brand.json> <kit-dir>
"""
import argparse, base64, json, math, os, re, sys
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET
from coloraide import Color
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _guidekit import tokens, faces, asset, copy_for, type_context
from brand_contract import affiliation_text, logo_metrics

def color_reference(token, value):
    color = Color(value).convert("srgb")
    red, green, blue = [round(channel * 255) for channel in color.coords()]
    hsl = color.convert("hsl")
    oklch = color.convert("oklch")
    lab = color.convert("lab")
    hsl_hue = hsl["hue"] if math.isfinite(hsl["hue"]) else 0.0
    oklch_hue = oklch["hue"] if math.isfinite(oklch["hue"]) else 0.0
    return {
        "token": token,
        "hex": value.upper(),
        "rgb": "rgb(%d %d %d)" % (red, green, blue),
        "hsl": "hsl(%.1f %.1f%% %.1f%%)" % (hsl_hue, hsl["saturation"] * 100, hsl["lightness"] * 100),
        "oklch": "oklch(%.4f %.4f %.1f)" % (oklch["lightness"], oklch["chroma"], oklch_hue),
        "lab": "lab(%.2f%% %.2f %.2f) (D50)" % (lab["lightness"], lab["a"], lab["b"]),
        "print": "CMYK: output profile required",
    }

def group_asset_deliveries(deliveries):
    grouped = {}
    for item in deliveries:
        visual_role = item.get("role")
        if item.get("platform") == "apple-macos" and visual_role in {"asset-catalog-icon", "iconset-icon"}:
            visual_role = "app-icon"
        normalized = dict(item); normalized["role"] = visual_role
        key = tuple(item.get(field) or "default" for field in
                    ("family", "platform", "kind", "variant", "colourway")) + (
                        normalized.get("role") or "default", item.get("appearance") or "default",
                        item.get("source_variant") or "default")
        grouped.setdefault(key, []).append(item)
    result = []
    for key, rows in grouped.items():
        rows.sort(key=lambda item: item["path"])
        previews = [item for item in rows if item.get("format") in {"svg", "png"}]
        representative = max(previews or rows, key=lambda item: (
            item.get("format") == "svg", int(item.get("width") or 0) * int(item.get("height") or 0), item["path"]))
        result.append({"id": "asset-" + re.sub(r"[^a-z0-9]+", "-", "-".join(key).lower()).strip("-"),
                       "key": key, "representative": representative, "deliveries": rows})
    return sorted(result, key=lambda item: item["id"])

def _dimensions(path):
    suffix = path.suffix.lower()
    if suffix == ".png":
        from PIL import Image
        with Image.open(str(path)) as image:
            return image.size
    if suffix == ".svg":
        root = ET.parse(str(path)).getroot()
        box = root.get("viewBox", "").replace(",", " ").split()
        return (round(float(box[2])), round(float(box[3]))) if len(box) == 4 else (None, None)
    return (None, None)

def _container_sizes(path, format_):
    payload = path.read_bytes()
    if format_ == "ico" and len(payload) >= 6 and payload[:4] == b"\x00\x00\x01\x00":
        count = int.from_bytes(payload[4:6], "little")
        return sorted({payload[6 + index * 16] or 256 for index in range(count) if 6 + (index + 1) * 16 <= len(payload)})
    if format_ == "icns" and len(payload) >= 8 and payload[:4] == b"icns":
        types = {b"icp4": 16, b"icp5": 32, b"icp6": 64, b"ic07": 128, b"ic08": 256, b"ic09": 512, b"ic10": 1024}
        sizes, offset = set(), 8
        while offset + 8 <= len(payload):
            length = int.from_bytes(payload[offset + 4:offset + 8], "big")
            if length < 8 or offset + length > len(payload):
                raise ValueError("invalid ICNS container: %s" % path)
            if payload[offset:offset + 4] in types:
                sizes.add(types[payload[offset:offset + 4]])
            offset += length
        return sorted(sizes)
    return []

def asset_deliveries(kit):
    rows = []
    provenance = json.loads(Path(kit, "logos", "provenance.json").read_text(encoding="utf-8"))
    for item in provenance["derivatives"]:
        path = Path(kit, item["path"])
        if not path.is_file():
            raise ValueError("guideline logo inventory references missing file: %s" % item["path"])
        width, height = _dimensions(path)
        rows.append({"family": "logo", "platform": "identity", "kind": item["kind"], "variant": item["variant"],
                     "colourway": item["colourway"], "role": item["kind"], "appearance": item["colourway"],
                     "source_variant": item["variant"], "format": path.suffix[1:], "width": width, "height": height,
                     "destination": "Brand identity", "path": item["path"]})
    icons = json.loads(Path(kit, "icons", "manifest.json").read_text(encoding="utf-8"))
    icon_rows = {}
    for item in icons["artifacts"]:
        if item.get("format") not in {"png", "svg", "ico", "icns", "json", "xml"}:
            continue
        path = Path(kit, item["path"])
        if not path.is_file():
            raise ValueError("guideline icon inventory references missing file: %s" % item["path"])
        row = dict(item); row["family"] = "icon"
        if row["format"] in {"png", "svg"}:
            width, height = _dimensions(path)
            if ((row.get("width") and row["width"] != width)
                    or (row.get("height") and row["height"] != height)):
                raise ValueError("guideline icon inventory dimensions disagree with file: %s" % item["path"])
            row["width"], row["height"] = width, height
        elif row["format"] in {"ico", "icns"}:
            row["embedded_sizes"] = _container_sizes(path, row["format"])
        rows.append(row); icon_rows[item["path"]] = row
    for alias, target in icons.get("aliases", {}).items():
        path = Path(kit, alias)
        if not path.is_file():
            raise ValueError("guideline icon alias references missing file: %s" % alias)
        if target not in icon_rows:
            raise ValueError("guideline icon alias references uncatalogued target: %s" % target)
        row = dict(icon_rows[target]); row["path"] = alias; row["destination"] = "Compatibility alias for %s" % target
        rows.append(row)
    return rows, icons.get("suites", []), icons.get("aliases", {})

def _preview(kit, item, title):
    path = Path(kit, item["path"])
    if item.get("format") not in {"png", "svg"}:
        return '<div class="no-preview">Container asset</div>'
    mime = "image/svg+xml" if item["format"] == "svg" else "image/png"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return '<img src="data:%s;base64,%s" alt="%s preview">' % (mime, payload, escape(title, quote=True))

def _asset_catalog(kit, title):
    deliveries, suites, aliases = asset_deliveries(kit)
    groups = group_asset_deliveries(deliveries)
    cards = []
    for group in groups:
        row = group["representative"]
        label = " ".join(str(value) for value in group["key"] if value != "default").replace("-", " ").title()
        entries = []
        for item in group["deliveries"]:
            if item.get("width") and item.get("height"):
                size = "%s × %s" % (item["width"], item["height"])
            elif item.get("embedded_sizes"):
                size = "embedded: " + ", ".join("%d × %d" % (value, value) for value in item["embedded_sizes"])
            else:
                size = "container or metadata"
            entries.append('<li><a data-kit-asset href="../%s">%s</a><span>%s · %s · %s · %s</span></li>' %
                           (escape(item["path"], quote=True), escape(item["path"]), escape(str(item.get("role") or "asset")),
                            size, item["format"].upper(),
                            escape(str(item.get("destination") or "Kit delivery"))))
        light_surface = row.get("colourway") in {"light", "black"} or row.get("appearance") in {"light", "tinted", "light-unplated"}
        surface_class = "light-well" if light_surface else "dark-well"
        surface_label = "Light surface" if light_surface else "Dark surface"
        raster_widths = [int(item["width"]) for item in group["deliveries"] if item.get("format") == "png" and item.get("width")]
        sizing = ("Smallest delivered raster: %d px. Do not synthesize missing sizes." % min(raster_widths)
                  if raster_widths else "Use the declared container or vector at its listed destination.")
        handling = ("Follow the clear-space and reduction threshold above."
                    if row["family"] == "logo" else "Preserve declared plate and transparency behavior.")
        cards.append('<article class="asset-card" id="%s"><h3>%s</h3><div class="preview %s"><span class="surface-label">%s</span>%s</div>'
                     '<p class="dim">Use the declared %s form on compatible backgrounds. %s %s</p>'
                     '<ul class="deliveries">%s</ul></article>' %
                     (group["id"], escape(label), surface_class, surface_label, _preview(kit, row, "%s %s" % (title, label)),
                      escape(str(row.get("role") or row.get("kind") or "identity")), sizing, handling, "".join(entries)))
    skipped = [suite["id"] for suite in suites if suite.get("status") == "skipped"]
    note = ("<p class=\"notice\">Unavailable at this capability tier: %s.</p>" % escape(", ".join(skipped))) if skipped else ""
    alias_note = "" if not aliases else '<p class="lead">Compatibility aliases are listed with their canonical delivery group; byte-identical aliases do not create duplicate previews.</p>'
    return note + alias_note + '<div class="asset-grid">' + "".join(cards) + "</div>"

def _swatches(title, values, brand_title):
    cards = []
    grouped = {}
    for key, value in values:
        grouped.setdefault(value.upper(), []).append(key)
    for value, keys in grouped.items():
        roles = ", ".join(keys)
        ref = color_reference(roles, value)
        detail = []
        for fmt in ("hex", "rgb", "hsl", "oklch", "lab"):
            label = "%s %s" % (roles, fmt.upper())
            detail.append('<div class="color-value"><code>%s</code><button class="copy" type="button" data-copy="%s" aria-label="Copy %s %s">Copy</button></div>' %
                          (escape(ref[fmt]), escape(ref[fmt], quote=True), escape(brand_title, quote=True), escape(label, quote=True)))
        cards.append('<article class="color-card"><div class="chip" style="background:%s"></div><h3>%s</h3>'
                     '<details><summary>Color values</summary>%s<p class="dim">%s</p></details></article>' %
                     (value, escape(roles), "".join(detail), ref["print"]))
    return '<h3>%s</h3><div class="color-grid">%s</div>' % (escape(title), "".join(cards))

def clear_space_guidance(brand, clear_space):
    logo = brand.get("logo") or {}
    if logo.get("square_enclosure"):
        channel = logo.get("g_thickness_units")
        internal = (" The protected inner page retains its %g-unit G channel; that internal measurement is not the external clear-space requirement." % channel
                    if isinstance(channel, (int, float)) and not isinstance(channel, bool) else "")
        return ("The delivered square keeps %g units of external clear space on every side.%s Never resize the mark and wordmark independently."
                % (clear_space, internal))
    return "The horizontal row records its approved master composition. C is the outlined wordmark cap height used by the stacked lockup. X is the 70-unit G channel. Keep one X clear around every master. Never resize the mark and wordmark independently."

def build(B, kit):
    D, L = tokens(kit)
    slug, title = B["slug"], B["title"]
    A, AL = D["primary"], L["primary"]
    logo = asset(kit, "%s-horizontal-color-1024.png" % slug)
    lockups = (B.get("logo") or {}).get("lockups") or {}
    horizontal_lockup = lockups.get("horizontal") or {}
    stacked_lockup = lockups.get("stacked") or {}
    M = B.get("measured", {}); sep = M.get("hue_separation_deg", {})
    near = min(sep.values()) if sep else None
    cb = (B.get("color", {}).get("accent-bright", {}) or {})
    ca = (B.get("color", {}).get("accent-accessible", {}) or {})
    on_light = (cb.get("contrast") or {}).get("on_light_base", "?")
    acc_light = (ca.get("contrast") or {}).get("on_light_base", "?")
    fg = (cb.get("legal_foreground_when_used_as_fill") or {})
    dv = "".join("  --%s: %s;\n" % (k, v) for k, v in D.items())
    lv = "".join("  --%s: %s;\n" % (k, v) for k, v in L.items())
    def im(b, cls, alt):
        return "" if not b else '<img class="%s" src="data:image/png;base64,%s" alt="%s">' % (cls, b, escape(alt, quote=True))
    type_ = type_context(B)
    endorsement = affiliation_text(B)
    cs, canvas_width, canvas_height, artwork_width = logo_metrics(B)
    color_reference_html = (_swatches("Dark palette", list(D.items()), title)
                            + _swatches("Light palette", list(L.items()), title))
    catalog = _asset_catalog(kit, title)

    return """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s brand guidelines</title><style>
%(faces)s
:root {
%(lv)s  --radius-sm:6px; --radius-md:8px; --radius-xl:12px;
  --font-display:'%(display)s'; --font-body:'%(body)s'; --font-mono:'%(mono)s';
}
.dark {
%(dv)s}
* { box-sizing:border-box; }
body { margin:0; background:var(--background); color:var(--foreground);
  font-family:var(--font-body),system-ui,sans-serif; font-size:16px; line-height:1.7;
  -webkit-font-smoothing:antialiased; }
.wrap { max-width:1200px; margin:0 auto; padding:0 24px; }
@media(min-width:768px){ .wrap{ padding:0 48px; } }
@media(min-width:1024px){ .wrap{ padding:0 80px; } }
header { padding:96px 0 48px; }
h1 { font-family:var(--font-display); font-weight:%(display_bold)d; font-size:clamp(2.25rem,6vw,3.5rem);
  line-height:1.1; letter-spacing:-.025em; margin:.2em 0; }
h2 { font-family:var(--font-display); font-weight:%(display_regular)d; font-size:1.75rem; line-height:1.2;
  letter-spacing:-.015em; margin:0 0 8px; }
h3 { font-family:var(--font-display); font-weight:%(display_regular)d; font-size:1.1rem; margin:32px 0 8px; }
.eyebrow { font-family:var(--font-mono); font-size:.75rem; letter-spacing:.12em;
  text-transform:uppercase; color:var(--primary); }
section { padding:56px 0; border-top:1px solid var(--border); }
section { scroll-margin-top:24px; }
.contents { border-block:1px solid var(--border); padding:16px 0; }
.contents ul { display:flex; flex-wrap:wrap; gap:8px 20px; margin:8px 0 0; padding:0; list-style:none; }
.contents a,.utility a,.deliveries a { color:var(--foreground); text-underline-offset:4px; }
.lead { color:var(--muted-foreground); max-width:720px; }
.grid { display:grid; gap:16px; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); margin-top:24px; }
.sw .chip { height:64px; border-radius:var(--radius-md); border:1px solid var(--border); }
.color-grid,.asset-grid { display:grid; gap:16px; grid-template-columns:repeat(auto-fit,minmax(min(100%%,260px),1fr)); margin-top:20px; }
.color-card,.asset-card { min-width:0; background:var(--card); border:1px solid var(--border); border-radius:var(--radius-xl); padding:18px; }
.color-card .chip { height:72px; border:1px solid var(--border); border-radius:var(--radius-md); }
.color-card h3,.asset-card h3 { margin:12px 0; }
.color-value { display:grid; grid-template-columns:minmax(0,1fr) auto; align-items:center; gap:8px; border-top:1px solid var(--border); padding:8px 0; }
.color-value code,.deliveries a,.deliveries span { overflow-wrap:anywhere; }
.copy { min-width:44px; min-height:44px; border:1px solid var(--border); border-radius:var(--radius-sm); background:var(--secondary); color:var(--foreground); cursor:pointer; }
.preview { display:grid; place-items:center; min-height:180px; border:1px solid var(--border); border-radius:var(--radius-md); padding:20px; overflow:hidden; }
.preview img { max-height:180px; }
.dark-well { background:#090909; }
.light-well { background:#F5F5F5; color:#111111; }
.surface-label { align-self:start; justify-self:start; font: .65rem var(--font-mono); letter-spacing:.08em; text-transform:uppercase; }
.deliveries { list-style:none; padding:0; margin:12px 0 0; }
.deliveries li { display:grid; gap:2px; border-top:1px solid var(--border); padding:9px 0; }
.deliveries span { color:var(--muted-foreground); font: .7rem var(--font-mono); }
.theme-wells { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:24px; }
.theme-well { border:1px solid var(--border); border-radius:var(--radius-xl); padding:20px; background:var(--background); color:var(--foreground); }
.theme-well .mini-bars { display:flex; gap:5px; height:64px; align-items:flex-end; }
.theme-well .mini-bars span { flex:1; height:var(--height); background:var(--bar); border-radius:4px 4px 0 0; }
.notice { border:1px solid var(--border); border-radius:var(--radius-md); padding:12px; }
.back-top { position:fixed; right:16px; bottom:16px; min-width:44px; min-height:44px; opacity:0; pointer-events:none; transform:translateY(8px); }
.back-top.visible { opacity:1; pointer-events:auto; transform:none; }
.sr-only { position:absolute; width:1px; height:1px; overflow:hidden; clip:rect(0,0,0,0); }
.mono { font-family:var(--font-mono); font-size:.75rem; margin-top:6px; }
.dim { color:var(--muted-foreground); }
.card { background:var(--card); border:1px solid var(--border);
  border-radius:var(--radius-xl); padding:24px; }
.two { display:grid; gap:24px; grid-template-columns:1fr 1fr; }
@media(max-width:800px){ .two,.theme-wells{ grid-template-columns:1fr; } }
.row { display:flex; gap:16px; flex-wrap:wrap; align-items:center; margin-top:24px; }
.btn { font-family:var(--font-body); font-weight:%(body_medium)d; font-size:.875rem; border-radius:var(--radius-md);
  padding:10px 18px; border:1px solid transparent; cursor:pointer; }
.btn-primary { background:var(--primary); color:var(--primary-foreground); }
.btn-secondary { background:transparent; color:var(--foreground); border-color:var(--border); }
.badge { font-family:var(--font-mono); font-size:.7rem; letter-spacing:.08em; text-transform:uppercase;
  border-radius:999px; padding:4px 12px; border:1px solid currentColor; }
input { font-family:var(--font-body); font-size:.875rem; background:var(--card); color:var(--foreground);
  border:1px solid var(--input); border-radius:var(--radius-md); padding:10px 12px; width:100%%; }
:focus-visible { outline:2px solid var(--ring); outline-offset:2px; }
table { width:100%%; border-collapse:collapse; font-family:var(--font-mono); font-size:.8rem; margin-top:16px; }
th { text-align:left; color:var(--muted-foreground); font-weight:400; letter-spacing:.08em;
  text-transform:uppercase; font-size:.7rem; padding:8px 12px; border-bottom:1px solid var(--border); }
td { padding:8px 12px; border-bottom:1px solid var(--border); }
.endorse { font-family:var(--font-mono); font-size:.7rem; letter-spacing:.1em; text-transform:uppercase;
  color:var(--muted-foreground); padding:48px 0 96px; }
img { max-width:100%%; height:auto; object-fit:contain; }
img.logo { max-height:56px; } img.mark { max-height:40px; } img.stacked { max-height:160px; }
code { font-family:var(--font-mono); font-variant-ligatures:none; }
@media(prefers-reduced-motion:reduce){ *{ animation-duration:.01ms!important; transition-duration:.01ms!important; } }
</style></head><body class="dark"><div class="wrap">
<header id="top">%(logoimg)s
<div class="eyebrow" style="margin-top:32px">Brand guidelines</div>
<h1>%(idea)s</h1>
<p class="lead">%(descriptor)s</p>
</header>

<nav class="contents" aria-label="On this page"><strong>On this page</strong><ul>
<li><a href="#colors">Colors</a></li><li><a href="#themes">Theme examples</a></li>
<li><a href="#type-components">Type and components</a></li><li><a href="#assets">Asset catalog</a></li>
</ul></nav>

<main><section id="colors"><div class="eyebrow">Colour</div><h2>Identity accent</h2>
<p class="lead">%(sepline)s</p>
<p class="lead">HEX uses uppercase pairs; sRGB uses integer 0-255 channels; HSL uses degrees and percentages rounded to one decimal; OKLCH uses four decimals for lightness and chroma plus one for hue; CIELAB uses D50 with lightness as a percentage and two decimals per channel.</p>
%(color_reference_html)s
<div class="card" style="margin-top:24px"><div class="eyebrow">Light surfaces</div>
<p style="margin:8px 0 0">The bright accent <code>%(A)s</code> measures <b>%(on_light)s:1</b> on the light
reading surface and is never text there. The light block substitutes <code>%(AL)s</code> at
%(acc_light)s:1. The legal foreground on an accent fill is <code>%(fgc)s</code> at %(fgr)s:1.</p></div>
</section>

<section id="themes"><div class="eyebrow">Theme reference</div><h2>Dark and light examples</h2>
<p class="lead">Chart colors serve data visualization. Brand applications use the identity accent and the neutral surfaces. Each chart color is derived from the accent, clears 4.5:1 on its surface, and remains separate from warning and failure states.</p>
<div class="theme-wells"><div class="theme-well" style="%(dark_vars)s"><div class="eyebrow">Dark</div><h3>Heading and controls</h3><p>Body text on the generated dark surface.</p><div class="row"><button class="btn btn-primary">Primary</button><button class="btn btn-secondary">Secondary</button></div><div class="mini-bars">%(mini_bars)s</div></div>
<div class="theme-well" style="%(light_vars)s"><div class="eyebrow">Light</div><h3>Heading and controls</h3><p>Body text on the generated light surface.</p><div class="row"><button class="btn btn-primary">Primary</button><button class="btn btn-secondary">Secondary</button></div><div class="mini-bars">%(mini_bars_light)s</div></div></div>
</section>

<section id="type-components"><div class="eyebrow">Type and components</div><h2>%(display)s, %(body)s, %(mono)s</h2>
<div class="two" style="margin-top:24px">
<div class="card">
<div style="font-family:var(--font-display);font-weight:%(display_bold)d;font-size:3rem;letter-spacing:-.025em;line-height:1.1">Display</div>
<div style="font-family:var(--font-display);font-weight:%(display_regular)d;font-size:1.6rem;margin-top:12px">Heading</div>
<p style="margin-top:12px">Body in %(body)s at %(body_regular)d. Approved weights are display %(display_weights)s, body %(body_weights)s, and mono %(mono_weights)s. Undeclared weights are prohibited.</p>
<div class="mono" style="font-size:.8rem">0O 1lI 8B 5S 2Z</div></div>
<div class="card"><div class="eyebrow">Components</div>
<div class="row"><button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<span class="badge" style="color:var(--primary)">ok</span>
<span class="badge" style="color:var(--brand-emphasis)">warn</span>
<span class="badge" style="color:var(--destructive)">fail</span></div>
<div style="margin-top:16px"><input placeholder="input"></div>
<table><tr><th>token</th><th>value</th></tr>
<tr><td>radius</td><td>6 / 8 / 12 / 16</td></tr>
<tr><td>spacing</td><td>4 8 12 16 24 32 48 64</td></tr>
<tr><td>focus</td><td>2px ring, 2px offset</td></tr></table></div></div>
</section>

<section id="assets"><div class="eyebrow">Delivery</div><h2>Complete asset catalog</h2>
<p class="lead">Canvas %(canvas_width)d × %(canvas_height)d units, clear space %(cs)d units (%(cspct).1f percent of artwork width).
Below %(red)d px the reduced master takes over.</p>
<h3>Fixed lockup proportions</h3>
<table><tr><th>lockup</th><th>mark height</th><th>gap</th><th>alignment</th></tr>
<tr><td>horizontal</td><td>%(hmark).0f units</td><td>%(hgap).0f units</td><td>optical center</td></tr>
<tr><td>stacked</td><td>%(smark).2fC</td><td>%(sgap).2fC</td><td>centered on wordmark ink width</td></tr></table>
<p class="lead">%(clear_space_guidance)s</p>
%(catalog)s
</section></main>

%(endorsement)s
<footer class="utility"><a href="#top">Back to top</a><span data-host-exit></span></footer>
<div id="copy-status" class="sr-only" aria-live="polite"></div>
<button class="back-top btn btn-secondary" type="button" hidden aria-label="Back to top">Top</button>
</div><script>
const topTarget=document.querySelector('header');const topButton=document.querySelector('.back-top');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
for(const button of document.querySelectorAll('[data-copy]'))button.addEventListener('click',async()=>{const status=document.querySelector('#copy-status');try{if(!navigator.clipboard)throw new Error('unavailable');await navigator.clipboard.writeText(button.dataset.copy);status.textContent='Copied '+button.getAttribute('aria-label').replace(/^Copy /,'');}catch(error){status.textContent='Copy failed. Select the displayed value instead.';}});
if('IntersectionObserver' in window){topButton.hidden=false;new IntersectionObserver(([entry])=>{topButton.classList.toggle('visible',!entry.isIntersecting);topButton.tabIndex=entry.isIntersecting?-1:0;}).observe(topTarget);topButton.addEventListener('click',()=>{topTarget.scrollIntoView({behavior:reduced.matches?'auto':'smooth'});topTarget.setAttribute('tabindex','-1');topTarget.focus({preventScroll:true});});}
</script></body></html>""" % {
        "title": title, "faces": faces(kit, B), "lv": lv, "dv": dv,
        "logoimg": im(logo, "logo", "%s horizontal logo" % title),
        "idea": copy_for(B, "idea", B.get("brand_idea", title)),
        "descriptor": copy_for(B, "descriptor", B.get("descriptor", "")),
        "sepline": ("Hue %s in OKLCH." % M.get("identity_hue", "?")) + (
            "" if near is None else " %.1f degrees clear of the nearest sibling identity accent." % near),
        "A": A, "AL": AL, "on_light": on_light, "acc_light": acc_light,
        "fgc": fg.get("color", "?"), "fgr": fg.get("ratio", "?"),
        "canvas_width": canvas_width,
        "canvas_height": canvas_height,
        "hmark": float(horizontal_lockup.get("mark_height_units", 160.0)),
        "hgap": float(horizontal_lockup.get("gap_units", 34.0)),
        "smark": float(stacked_lockup.get("mark_height_c", 1.8)),
        "sgap": float(stacked_lockup.get("gap_c", 0.45)),
        "cs": cs,
        "cspct": 100.0 * cs / artwork_width,
        "clear_space_guidance": clear_space_guidance(B, cs),
        "color_reference_html": color_reference_html,
        "catalog": catalog,
        "dark_vars": escape(";".join("--%s:%s" % item for item in D.items()), quote=True),
        "light_vars": escape(";".join("--%s:%s" % item for item in L.items()), quote=True),
        "mini_bars": "".join('<span style="--bar:%s;--height:%d%%"></span>' % (D["chart-%d" % i], 36 + i * 10) for i in range(1, 6)),
        "mini_bars_light": "".join('<span style="--bar:%s;--height:%d%%"></span>' % (L["chart-%d" % i], 36 + i * 10) for i in range(1, 6)),
        "red": (B.get("logo") or {}).get("reduced_below_px", 32),
        "endorsement": "" if not endorsement else '<div class="endorse">%s</div>' % escape(endorsement),
        **type_,
    }

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("brand"); ap.add_argument("kit")
    a = ap.parse_args()
    B = json.load(open(a.brand, encoding="utf-8"))
    d = os.path.join(a.kit, "guidelines"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "index.html")
    with open(p, "w", encoding="utf-8", newline="\n") as f: f.write(build(B, a.kit))
    print("wrote", p)
    print("Now run qc_images.py and OPEN the page sheet. It renders at 390px too.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
