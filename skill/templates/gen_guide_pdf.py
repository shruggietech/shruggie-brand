#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_guide_pdf.py: the brand guide, built to the ShruggieTech house standard.

The default house standard remains full-bleed dark on every sheet. A brand may
explicitly declare ``guide.surface_mode: light`` when its approved identity is
light-first. The declared mode applies to every page rather than mixing a dark
cover with white body sheets.

Prose: every section reads brand.json `guide.<key>` when present and falls back
to a default generated from the measured values, so two operator inputs still
produce a complete document.

    python3 build/gen_guide_pdf.py <brand.json> <kit-dir> [--html-only]
"""
import argparse, base64, json, os, sys
from html import escape
from capabilities import load_capabilities
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _guidekit import tokens, faces, asset, copy_for, type_context
from brand_contract import affiliation, affiliation_text, custom_assets, guide_surface_mode, logo_metrics, vendor_boundary
from color_roles import load_color_roles

def chips(t, keys, light=False):
    o = ""
    for k in keys:
        if k not in t: continue
        o += ('<div class="sw"><div class="chip" style="background:%s;border-color:%s"></div>'
              '<div class="m">%s</div><div class="m dim">%s</div></div>'
              % (t[k], "#D6DAE2" if light else "#26304A", k, t[k]))
    return o

def _personality(B):
    rows = (B.get("guide") or {}).get("personality") or [
        ["Precise", "Exact units and observable outcomes", "Round numbers"],
        ["Bounded", "States what it does not cover", "Implied magic"],
        ["Competent", "Assumes a capable reader", "Condescending tutorials"]]
    prom = (B.get("guide") or {}).get("promises") or [
        "Every number shown is a measurement that happened.",
        "Unknowns are labelled as unknowns.",
        "Terminology stays identical across CLI, docs and interface."]
    # DEVIATION: this was a two-up, which squeezed a three-column table into half
    # the measure and wrapped every cell to four lines. The table takes the full
    # width now and the two short blocks share the row underneath it.
    return ('<div class="card" style="margin-top:4mm"><div class="ey">Personality</div>'
            '<table><tr><th style="width:22%%">Trait</th><th style="width:39%%">Expression</th>'
            '<th style="width:39%%">Avoid</th></tr>%s</table></div>'
            '<div class="two" style="margin-top:4mm"><div class="card"><div class="ey">Promises</div>'
            '<ul class="dim" style="line-height:1.7;margin-top:2mm">%s</ul></div>%s</div>'
            % ("".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(r) for r in rows),
               "".join("<li>%s</li>" % p for p in prom), _sharp_edge(B)))

def _sharp_edge(B):
    """The one place the brand could mislead somebody. Kept; the in-scope and
    out-of-scope lists that used to sit beside it were specification material."""
    edge = (B.get("guide") or {}).get("sharp_edge")
    if not edge:
        return ""
    return ('<div class="callout" style="margin:0"><div class="ey">The sharp edge</div>'
            '<p style="margin:0" class="dim">%s</p></div>' % edge)

def _semantics(B, A, CTA, CTA_FG, OR, FA):
    emphasis_name = "Orange" if affiliation(B)["inheritance"] == "shruggietech-house" else "Emphasis"
    i_heart_secondary = B.get("slug") == "i-heart-pr-tours"
    if not i_heart_secondary:
        return ('<div class="two"><div class="card"><div class="ey">Semantic use</div><table>'
                '<tr><th>Color</th><th>Means</th></tr>'
                '<tr><td style="color:%s">Accent</td><td>Primary value, selection, links, focus</td></tr>'
                '<tr><td style="color:%s">%s</td><td>Needs attention, threshold exceeded</td></tr>'
                '<tr><td style="color:%s">Destructive</td><td>Failed or timed out. Always with text.</td></tr>'
                '</table></div><div class="card"><div class="ey">Color vision</div>'
                '<p class="dim" style="margin:0">The emphasis and failure colors may not be reliably separable '
                'under deuteranopia. That is acceptable only because state '
                'is never carried by color alone: every state ships a written label.</p></div></div>'
                % (A, OR, emphasis_name, FA))
    secondary = ('<span class="cta-sample secondary"><b>Secondary action</b><small>Red outline</small></span>'
                 if i_heart_secondary else "")
    boundary = ("CTA red fills primary actions and outlines secondary ones. It does not replace identity, link, focus, chart, emphasis, or destructive colors."
                if i_heart_secondary else
                "The CTA color is reserved for the primary action. It does not replace identity, link, focus, chart, emphasis, or destructive colors.")
    return ('<div class="two"><div class="card"><div class="ey">Semantic use</div><table>'
            '<tr><th>Color</th><th>Means</th></tr>'
            '<tr><td style="color:%s">Accent</td><td>Primary value, selection, links, focus</td></tr>'
            '<tr><td style="color:%s">Primary CTA button</td><td>%s fill with %s text</td></tr>'
            '<tr><td style="color:%s">%s</td><td>Needs attention, threshold exceeded</td></tr>'
            '<tr><td style="color:%s">Destructive</td><td>Failed or timed out. Always with text.</td></tr>'
            '</table></div><div class="card"><div class="ey">CTA states</div>'
            '<div class="cta-states" style="--cta:%s;--cta-fg:%s">'
            '<span class="cta-sample">Default</span><span class="cta-sample hover">Hover</span>'
            '<span class="cta-sample active">Active</span><span class="cta-sample focus">Focus visible</span>'
            '%s</div>'
            '<div class="ey" style="margin-top:3mm">Color vision</div>'
            '<p class="m dim" style="margin:0">State is never carried by color alone. Every state keeps its written label and a shape, border, depth, or focus cue.</p>'
            '</div></div><div class="callout acc"><div class="ey">Role boundary</div>'
            '<p class="m dim" style="margin:0">%s</p></div>'
            % (A, CTA, CTA, CTA_FG, OR, emphasis_name, FA, CTA, CTA_FG, secondary, boundary))

def _scales():
    disp = [("display-xl", 72, "-0.030em"), ("display-lg", 56, "-0.025em"),
            ("display-md", 40, "-0.020em"), ("display-sm", 28, "-0.015em"),
            ("display-xs", 20, "-0.010em")]
    body = [("body-lg", 18.4, 1.60), ("body-md", 16, 1.70), ("body-sm", 14, 1.60),
            ("body-xs", 12, 1.50), ("eyebrow", 12, "0.12em caps")]
    return ('<div class="rule"></div><div class="two">'
            '<div class="card"><div class="ey">Scale, display</div><table>'
            '<tr><th>Token</th><th>Size</th><th>Tracking</th></tr>%s</table></div>'
            '<div class="card"><div class="ey">Scale, reading</div><table>'
            '<tr><th>Token</th><th>Size</th><th>Leading</th></tr>%s</table></div></div>'
            % ("".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in disp),
               "".join("<tr><td>%s</td><td>%s</td><td>%s</td></tr>" % r for r in body)))

def _ships(kit):
    """Read from the kit that actually exists rather than a hardcoded list."""
    want = [("logos/svg", "Vector masters, every lockup and colorway"),
            ("icons", "Web, Android, Apple, macOS, and Windows application suites"),
            ("favicons", "Compatibility aliases for the authoritative web suite"),
            ("fonts/woff2", "Web faces plus OFL licences"),
            ("tokens", "CSS and JSON with measured contrast"),
            ("nextjs", "globals.css, shadcn registry, fonts, provider"),
            ("enforcement", "AGENTS.md, ESLint, stylelint"),
            ("qc", "Contact sheets. Proof somebody looked."),
            ("guidelines", "The system rendered from itself")]
    rows = []
    for d, desc in want:
        p = os.path.join(kit, *d.split("/"))
        if os.path.isdir(p):
            n = sum(len(f) for _, _, f in os.walk(p))
            rows.append("<tr><td>%s/</td><td>%s</td><td>%d</td></tr>" % (d, desc, n))
    if not rows: return ""
    half = (len(rows) + 1) // 2
    tbl = lambda rs: ('<table><tr><th>Path</th><th>Contents</th><th>n</th></tr>%s</table>' % "".join(rs))
    return ('<div class="rule"></div><h3>What ships in the kit</h3>'
            '<div class="two"><div>%s</div><div>%s</div></div>'
            % (tbl(rows[:half]), tbl(rows[half:])))


def _variants(kit, slug, img):
    """Show the colourways that were actually produced, at the sizes they matter."""
    from _guidekit import b64 as _b64
    pngs = os.path.join(kit, "logos", "png")
    def has(n):
        p = os.path.join(pngs, n)
        return _b64(p) if os.path.exists(p) else None
    cells = []
    for fn, label, preview_class in (
        ("%s-horizontal-color-1024.png" % slug, "Horizontal, product surface", " dark-preview"),
        ("%s-mark-color-1024.png" % slug, "Mark", " dark-preview"),
        ("%s-horizontal-light-1024.png" % slug, "Light surface", " lite"),
        ("%s-mark-reduced-color-1024.png" % slug, "Reduced master", " lite")):
        b = has(fn)
        if not b: continue
        cells.append('<div class="card%s" style="text-align:center;padding:5mm 2mm">%s'
                     '<div class="m dim" style="margin-top:3mm">%s</div></div>'
                     % (preview_class,
                        img(b, "", "height:%dmm" % (7 if "horizontal" in fn else 9)), label))
    return "" if not cells else '<div class="grid4" style="margin-top:4mm">%s</div>' % "".join(cells)

def _charttable(D, L, B):
    rows = "".join("<tr><td>chart-%d</td><td>%s</td><td>%s</td></tr>"
                   % (i, D.get("chart-%d" % i, ""), L.get("chart-%d" % i, "")) for i in range(1, 6))
    return ('<div class="two" style="margin-top:4mm"><div class="card"><div class="ey">'
            'Derived values</div><table><tr><th>Series</th><th>Dark</th><th>Light</th></tr>%s</table>'
            '</div><div class="card"><div class="ey">Rules of use</div>'
            '<p class="m dim" style="margin:0">Series order is fixed: chart-1 is always the primary '
            'measurement. Never reorder to make a chart look better. Never introduce a sixth color; '
            'past five series, switch to a form that does not depend on hue. A series never uses the '
            'semantic emphasis or failure colors, because those carry state.</p></div></div>' % rows)


def build(B, kit):
    D, L = tokens(kit)
    slug, title = B["slug"], B["title"]
    light_first = guide_surface_mode(B) == "light"
    P, ALT = (L, D) if light_first else (D, L)
    A, AL = P["primary"], L["primary"]
    bright_accent = B["accent"]["bright"]
    AD = P.get("brand-accent-deep", A)
    OR, FA = P["brand-emphasis"], P["destructive"]
    CTA, CTA_FG = P["brand-cta"], P["brand-cta-foreground"]
    BG, CARD, LINE = P["background"], P["card"], P["border"]
    TX, MU = P["foreground"], P["muted-foreground"]
    CALLOUT, ACC_CALLOUT = P["secondary"], P["muted"]
    LG = B.get("logo", {})
    cs, canvas_width, canvas_height, artwork_width = logo_metrics(B)
    lockups = LG.get("lockups") or {}
    horizontal_lockup = lockups.get("horizontal") or {}
    stacked_lockup = lockups.get("stacked") or {}
    mono_logo = asset(kit, "%s-horizontal-light-1024.png" % slug) if light_first else asset(kit, "%s-horizontal-color-1024.png" % slug)
    mono_light = asset(kit, "%s-horizontal-light-1024.png" % slug)
    def img(b, cls="", st=""):
        return '' if not b else '<img class="%s" style="%s" src="data:image/png;base64,%s">' % (cls, st, b)

    type_ = type_context(B)
    aff = affiliation(B)
    inherits_house = aff["inheritance"] == "shruggietech-house"
    endorsement = affiliation_text(B)
    boundary = vendor_boundary(B)
    F = faces(kit, B)
    css = """
%s
:root { --font-display:'%s'; --font-body:'%s'; --font-mono:'%s'; --font-label-weight:%d; }
@page { size:A4; margin:0; }
* { box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact; }
html,body { margin:0; padding:0; background:%s; color:%s;
  font-family:var(--font-body),system-ui,sans-serif; font-size:9.2pt; line-height:1.62; }
h1,h2,h3 { font-family:var(--font-display); margin:0; }
h2 { font-weight:%d; font-size:16pt; letter-spacing:-.02em; line-height:1.12; margin-bottom:4mm; }
h3 { font-weight:%d; font-size:10.6pt; margin:5mm 0 2mm; }
p { margin:0 0 2.6mm; }
.dim { color:%s; }
.m { font-family:var(--font-body); font-size:7.5pt; letter-spacing:0; }
.code-block { font-family:var(--font-mono); font-size:7.2pt; letter-spacing:.02em; }
.ey { font-family:var(--font-body); font-weight:var(--font-label-weight); font-size:7.8pt; letter-spacing:.08em; text-transform:uppercase;
  color:%s; margin-bottom:2mm; }
.pg { position:relative; width:210mm; height:297mm; background:%s;
  padding:16mm 16mm 18mm 16mm; overflow:hidden; break-after:page; }
.pg:last-child { break-after:auto; }
.pg::after { content:""; position:absolute; left:16mm; right:16mm; bottom:11mm;
  height:.25mm; background:%s; }
.foot { position:absolute; left:16mm; right:16mm; bottom:6mm; display:flex;
  justify-content:space-between; font-family:var(--font-body); font-weight:var(--font-label-weight); font-size:7pt;
  letter-spacing:.02em; color:%s; }
.cover { padding:0; }
.cover .inner { position:absolute; inset:0; padding:24mm 20mm 20mm 20mm; }
.cover img.lockup { display:block; width:160mm; height:auto; margin-top:12mm; }
.cover .sys { margin:0; font-family:var(--font-body); font-weight:var(--font-label-weight); font-size:8pt;
  letter-spacing:.06em; text-transform:uppercase; color:%s; }
.cover .message { margin-top:20mm; padding:1mm 0 1mm 7mm; border-left:1mm solid; }
.cover .tag { margin:0; font-family:var(--font-display); font-weight:%d; font-size:23pt;
  letter-spacing:-.025em; line-height:1.08; max-width:145mm; }
.cover .idea { margin-top:4mm; font-size:11.5pt; color:%s; max-width:152mm; }
.cover .base { position:absolute; left:20mm; bottom:18mm; font-family:var(--font-body);
  font-size:7pt; letter-spacing:.02em; color:%s; }
.two { display:grid; grid-template-columns:1fr 1fr; gap:7mm; }
.three { display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; }
.grid4 { display:grid; grid-template-columns:repeat(4,1fr); gap:3.4mm; margin:3mm 0 4mm; }
.grid5 { display:grid; grid-template-columns:repeat(5,1fr); gap:2.8mm; margin:3mm 0 4mm; }
.sw .chip { height:13mm; border-radius:1.6mm; border:.25mm solid; }
.sw .m { margin-top:1mm; }
.card { background:%s; border:.25mm solid %s; border-radius:2.6mm; padding:4.5mm; }
.card.lite { background:#FFFFFF; border-color:#D6DAE2; color:#0A0A0A; }
.card.lite .dim { color:#6B6B6B; }
.card.dark-preview { background:#08131D; border-color:#27445A; color:#FFFFFF; }
.card.dark-preview .dim { color:#E8EDF2; }
.rule { height:.25mm; background:%s; margin:4.5mm 0; }
table { width:100%%; border-collapse:collapse; font-family:var(--font-body); font-size:7.8pt; }
th { text-align:left; font-weight:var(--font-label-weight); text-transform:uppercase; letter-spacing:.04em;
  font-size:7.3pt; color:%s; padding:1.7mm 2mm; border-bottom:.25mm solid %s; }
td { padding:1.7mm 2mm; border-bottom:.25mm solid %s; vertical-align:top; }
.role-cues-compact { font-size:7pt; }
.role-cues-compact td { padding:1mm 1.5mm; }
.kv { display:grid; grid-template-columns:30mm 1fr; gap:1.4mm 4mm; }
.kv .k { font-family:var(--font-body); font-weight:var(--font-label-weight); font-size:7.3pt; text-transform:uppercase;
  letter-spacing:.04em; color:%s; padding-top:.5mm; }
.callout { border:.25mm solid %s; border-left:1mm solid %s; border-radius:1.6mm;
  padding:3.4mm 4mm; margin:4mm 0; background:%s; }
.callout .ey { color:%s; }
.callout.acc { border-color:%s; border-left-color:%s; background:%s; }
.callout.acc .ey { color:%s; }
.badge { font-family:var(--font-body); font-weight:var(--font-label-weight); font-size:7pt; letter-spacing:.04em; text-transform:uppercase;
  border:.25mm solid currentColor; border-radius:9mm; padding:.5mm 2mm; }
.charts { display:flex; gap:1.6mm; align-items:flex-end; height:22mm; margin:3mm 0 1mm; }
.charts div { flex:1; border-radius:1.2mm 1.2mm 0 0; }
.cta-states { display:grid; grid-template-columns:1fr 1fr; gap:1mm; margin:1.4mm 0 0; }
.cta-sample { display:grid; place-items:center; min-height:7mm; border:.4mm solid var(--cta); border-radius:1.6mm; background:var(--cta); color:var(--cta-fg); font-weight:var(--font-label-weight); }
.cta-sample.hover { border-color:var(--cta-fg); transform:translateY(-.5mm); }
.cta-sample.active { box-shadow:inset 0 0 0 .6mm var(--cta-fg); }
.cta-sample.focus { outline:.6mm solid #FFFFFF; outline-offset:.6mm; box-shadow:0 0 0 1.2mm #000000; }
.cta-sample.secondary { grid-column:1 / -1; grid-template-columns:auto auto; gap:2mm; background:transparent; color:var(--cta); border-color:var(--cta); }
.cta-sample.secondary small { font-size:6.5pt; font-weight:var(--font-body-regular); text-transform:uppercase; letter-spacing:.04em; }
ul { margin:1mm 0 0; padding-left:4mm; } li { margin-bottom:1.8mm; }
.sw .m { font-size:6.6pt; }
""" % (F, type_["display"], type_["body"], type_["mono"], type_["body_medium"], BG, TX, type_["display_bold"], type_["display_regular"], MU, A, BG, LINE, MU, A, type_["display_regular"], MU, MU, CARD, LINE, LINE, TX, LINE, LINE, TX, LINE, OR, CALLOUT, A, A, A, ACC_CALLOUT, A)

    def foot(n):
        return '<div class="foot"><span>%s | Brand System</span><span>%02d</span></div>' % (title, n)
    def pg(ey, h2, body, n):
        return '<div class="pg"><div class="ey">%s</div><h2>%s</h2>%s%s</div>' % (ey, h2, body, foot(n))

    dark_bars = "".join('<div style="background:%s;height:%d%%"></div>' % (D["chart-%d" % i], 34 + i * 13)
                        for i in range(1, 6))
    light_bars = "".join('<div style="background:%s;height:%d%%"></div>' % (L["chart-%d" % i], 34 + i * 13)
                         for i in range(1, 6))

    pages = []
    pages.append('<div class="pg cover"><div class="inner">'
                 '<div class="sys">Brand &amp; design system</div>%s'
                 '<div class="message" style="border-color:%s"><div class="tag">%s</div><div class="idea">%s</div></div>'
                 '<div class="base">%sVersion %s &nbsp;·&nbsp; '
                 'Canon %s &nbsp;·&nbsp; %s</div>%s</div></div>'
                 % (img(mono_logo, "lockup"), A,
                    copy_for(B, "idea", B.get("brand_idea", B["title"])),
                    copy_for(B, "descriptor", B.get("descriptor", "")),
                    ((endorsement + " &nbsp;·&nbsp; ") if endorsement else ""),
                    B.get("version", "1.0.0"), B.get("canon", "1.0.0"),
                    B.get("homepage", "").replace("https://", ""), foot(1)))

    # DEVIATION: this sheet used to open with a product summary and an
    # in-scope / out-of-scope trio. A brand guide that pitches the product goes
    # stale the moment the specification moves, and it answers a question nobody
    # opened a brand book to ask. The sheet carries the name and the rules for
    # writing it now. Scope belongs to the specification.
    story = (B.get("guide") or {}).get("name_story") or [
        "State where the name came from and what its parts carry.",
    ]
    written = (B.get("guide") or {}).get("written_form") or (
        "Write %s in title case in prose and lowercase in technical identifiers." % title)
    pages.append(pg("Name", title,
        "".join('<p>%s</p>' % para for para in story)
        + '<div class="callout acc"><div class="ey">Written form</div>'
          '<p style="margin:0" class="dim">%s</p></div>'
          '<div class="kv" style="margin-top:5mm">%s</div>'
          '<h3>Product principle</h3><p style="font-family:var(--font-display);font-weight:%d;'
          'font-size:12.5pt;color:%s">%s</p>%s' % (
            written,
            "".join('<div class="k">%s</div><div>%s</div>' % (k, v) for k, v in [
                ("Named", (B.get("guide") or {}).get("named", "")),
                ("Parent", aff["parent"] or "None"),
                ("Register", B.get("register", "precise-dry")),
                ("Flourish", "Declined" if not B.get("shruggie_flourish")
                             else "Permitted, once per view"),
                ("Casing", "The product name is lowercase in prose and technical identifiers."
                 if B.get("wordmark_text", title).islower()
                 else "Title case in prose, lowercase in identifiers"),
            ] if v), type_["display_regular"], A, B.get("brand_idea", title), _personality(B)), 2))

    pages.append(pg("Logo system", "Marks and lockups",
        '<p>%s</p><div class="card" style="text-align:center;padding:9mm 4mm;margin:4mm 0">%s</div>'
        '<div class="two"><div><h3 style="margin-top:0">Clear space</h3>'
        '<p class="dim">One clear-space unit on every side: %d units on the %d × %d canvas, '
        '%.1f percent of artwork width. No text, border, icon or crop enters that band.</p></div>'
        '<div class="card"><div class="ey">Minimum size</div><table>%s</table>'
        '<p class="m dim" style="margin-top:3mm">Below %d px the reduced master takes over. '
        'It ships as its own file. Do not rasterize the full mark down at runtime.</p></div></div>'
        '<div class="rule"></div><h3>Fixed lockup proportions</h3>'
        '<table><tr><th>Lockup</th><th>Mark height</th><th>Gap</th><th>Alignment</th></tr>'
        '<tr><td>Horizontal</td><td>%.0f units</td><td>%.0f units</td><td>Optical center</td></tr>'
        '<tr><td>Stacked</td><td>%.2fC</td><td>%.2fC</td><td>Centered on wordmark ink width</td></tr></table>'
        '<p class="m dim">The horizontal row records its approved master composition. C is the outlined '
        'wordmark cap height used by the stacked lockup. X is the clear-space unit declared above. '
        'Keep one X clear around every master and never resize the mark and wordmark independently.</p>'
        '<div class="callout"><div class="ey">Prohibited</div><p style="margin:0" class="dim">'
        'No rotation, skew, stretch, outline, bevel or glow. Never recolor individual elements. '
        'Never set the wordmark in live text or a substitute typeface. %s</p></div>' % (
            copy_for(B, "logo", "The mark is built on a declared grid and ships as filled outlines, "
                                "never live text."),
            img(mono_logo, "", "height:17mm"), cs, canvas_width, canvas_height, 100.0 * cs / artwork_width,
            "".join("<tr><td>%s</td><td>%s px</td></tr>" % (k, v)
                    for k, v in (LG.get("min_px") or {}).items()),
            LG.get("reduced_below_px", 32),
            float(horizontal_lockup.get("mark_height_units", 160.0)),
            float(horizontal_lockup.get("gap_units", 34.0)),
            float(stacked_lockup.get("mark_height_c", 1.8)),
            float(stacked_lockup.get("gap_c", 0.45)),
            ("Never combine the %s and ShruggieTech marks into one lockup." % slug)
            if aff["parent"] else "Never combine this mark with another organization’s mark into one lockup.")
        + _variants(kit, slug, img), 3))

    i_heart_cta = slug == "i-heart-pr-tours"
    role_grid = "grid5" if i_heart_cta else "grid4"
    role_tokens = (["primary", "brand-accent-deep", "brand-emphasis", "brand-cta", "destructive"]
                   if i_heart_cta else ["primary", "brand-accent-deep", "brand-emphasis", "destructive"])
    cta_note = ((" The primary CTA button uses %s with %s text in both themes, and the generated verifier enforces AA for that pair." % (CTA, CTA_FG))
                if i_heart_cta else " Every fill token in brand.json carries its measured foreground.")
    pages.append(pg("Color", "Palette",
        '<p>%s</p><h3 style="margin-top:4mm">Role colors on dark surfaces</h3><div class="%s">%s</div>'
        '<h3>Neutrals, dark surfaces</h3><div class="grid4">%s</div>'
        '<div class="card lite" style="margin-top:4mm"><div class="ey" style="color:%s">'
        'Light reading surface</div><div class="grid4" style="margin-bottom:0">%s</div></div>'
        '<div class="callout"><div class="ey">Light surfaces</div><p style="margin:0" class="dim">'
        'The bright accent %s measures <b style="color:%s">%s:1</b> on the light reading surface and is '
        'never text there. The light token block substitutes %s at %s:1 automatically. The legal '
        'foreground on an accent fill is %s at %s:1.%s</p></div>' % (
            copy_for(B, "palette", ("White-paper first. The accessible accent structures the light "
                                    "surface; the brand-specific emphasis marks attention."
                                    if light_first else
                                    "Dark and close to monochrome. The accent is the signal; the "
                                    "inherited orange marks a state needing attention."
                                    if inherits_house else
                                    "Dark and close to monochrome. The accent is the signal; the "
                                    "brand-specific emphasis color marks a state needing attention.")),
            role_grid, chips(D, role_tokens),
            chips(D, ["background", "card", "secondary", "border"]),
            AL, chips(L, ["primary", "background", "muted", "muted-foreground"], True),
            bright_accent,
            TX,
            (B.get("color", {}).get("accent-bright", {}).get("contrast", {}) or {}).get("on_light_base", "?"),
            AL,
            (B.get("color", {}).get("accent-accessible", {}).get("contrast", {}) or {}).get("on_light_base", "?"),
            (B.get("color", {}).get("accent-bright", {}).get("legal_foreground_when_used_as_fill", {}) or {}).get("color", "?"),
            (B.get("color", {}).get("accent-bright", {}).get("legal_foreground_when_used_as_fill", {}) or {}).get("ratio", "?"),
            cta_note,
        ) + _semantics(B, A, CTA, CTA_FG, OR, FA), 4))

    pages.append(pg("Color", "Chart colors",
        '<p>Chart colors serve data visualization. Brand applications use the identity accent and the neutral surfaces. Each chart color is derived from the identity accent and measured against its surface so every entry clears 4.5:1.</p>'
        '<div class="charts">%s</div><div class="grid5">%s</div>'
        '<div class="callout acc"><div class="ey">Contrast checks</div>'
        '<p style="margin:0" class="dim">Lightness is calculated separately for dark and light surfaces. Data charts also use labels or shapes; hue alone does not carry meaning.</p></div><div class="card lite"><div class="ey" style="color:%s">The same palette on '
        'the light reading surface</div><div class="charts">%s</div><div class="grid5" '
        'style="margin-bottom:0">%s</div></div>' % (
            dark_bars, chips(D, ["chart-1", "chart-2", "chart-3", "chart-4", "chart-5"]),
            AL, light_bars, chips(L, ["chart-1", "chart-2", "chart-3", "chart-4", "chart-5"], True))
        + _charttable(D, L, B), 5))

    pages.append(pg("Typography", "Display, interface, code",
        '<p>%s uses three approved type families. %s handles display text, %s handles '
        'interface and reading text, and %s is reserved for literal command blocks.</p>'
        '<div class="card" style="margin:4mm 0"><div style="font-family:var(--font-display);'
        'font-weight:%d;font-size:22pt;letter-spacing:-.025em;line-height:1.08">%s</div>'
        '<div class="dim" style="margin-top:2mm">%s</div></div>'
        '<div class="two"><div class="card"><div class="ey">Roles</div><table>'
        '<tr><th>Function</th><th>Typeface</th><th>Weights</th></tr>'
        '<tr><td>Display, headings</td><td>%s</td><td>%s</td></tr>'
        '<tr><td>Body, interface</td><td>%s</td><td>%s</td></tr>'
        '<tr><td>Literal code blocks</td><td>%s</td><td>%s</td></tr></table></div>'
        '<div class="card"><div class="ey">Geometry</div><table>'
        '<tr><th>Axis</th><th>Value</th></tr>'
        '<tr><td>Radii</td><td>6 / 8 / 12 / 16 / pill</td></tr>'
        '<tr><td>Spacing</td><td>4 8 12 16 24 32 48 64 96 120</td></tr>'
        '<tr><td>Focus</td><td>2px ring at 2px offset</td></tr></table></div></div>'
        '<div class="callout"><div class="ey">Available weights</div><p style="margin:0" class="dim">'
        'Only the listed local faces are approved. Any other weight makes the renderer synthesize a faux bold, which prints badly and forces outlined glyphs into exported PDFs. Courier Prime is used only for literal command blocks.</p></div>' % (
            title, type_["display"], type_["body"], type_["mono"], type_["display_bold"],
            copy_for(B, "idea", B.get("brand_idea", title)),
            copy_for(B, "descriptor", B.get("descriptor", "")),
            type_["display"], type_["display_weights"], type_["body"], type_["body_weights"], type_["mono"], type_["mono_weights"]) + _scales(), 6))

    expressions = custom_assets(B, kit, public_only=True)
    if expressions:
        cards = []
        for item in expressions:
            source = os.path.join(kit, *item["source"]["path"].split("/"))
            mime = {"svg": "image/svg+xml", "png": "image/png", "jpeg": "image/jpeg", "webp": "image/webp"}[item["source"]["format"]]
            with open(source, "rb") as handle:
                encoded = base64.b64encode(handle.read()).decode("ascii")
            well = {"dark": "background:#121820", "light": "background:#FFFFFF", "grid": "background:repeating-conic-gradient(#D5D5D5 0 25%,#F5F5F5 0 50%) 0/20px 20px", "image": "background:#F5F5F5"}[item["preview"]["well"]]
            cards.append('<div class="card" style="text-align:center"><div style="%s;padding:3mm"><img style="height:75mm;max-width:100%%;object-fit:contain" src="data:%s;base64,%s" alt="%s"></div><h3>%s</h3><p class="dim">%s</p><p class="dim">Role: %s. Use: %s. Avoid: %s.</p><p class="dim">%s · %s</p><p class="dim">Source: %s</p></div>' % (
                well, mime, encoded, escape(item["accessibility"]["alt"], quote=True), escape(item["title"]),
                escape(item["description"]), escape(item["role"]), escape(item["usage"]["use"]), escape(item["usage"]["avoid"]),
                escape(item["credit"]["attribution"]), escape(item["credit"]["license"]), escape(item["source"]["path"])))
        for start in range(0, len(cards), 2):
            heading = "Expressions and atmosphere" if start == 0 else "Expressions and atmosphere (continued)"
            intro = ('<p>These approved treatments extend the identity for selected contexts. They are not substitutes for the core logo masters.</p>'
                     if start == 0 else "")
            pages.append(pg("Optional expressions", heading,
                            '%s<div class="two" style="margin-top:4mm">%s</div>' % (intro, "".join(cards[start:start + 2])),
                            len(pages) + 1))

    roles = load_color_roles(B, kit)
    affiliation_detail = ""
    formal_detail = ""
    if roles:
        ownership = "ShruggieTech owned" if aff["ownership"] == "shruggietech-owned" else "Third party"
        palette_choice = ("Shared house emphasis and action, explicitly selected" if inherits_house
                          else "Brand-specific emphasis and action")
        typography_choice = "House families" if B["typography"]["mode"] == "house" else "Declared local faces"
        decisions = (("Ownership", ownership), ("Parent", aff["parent"] or "None"),
                     ("Palette", palette_choice), ("Typography", typography_choice))
        decision_rows = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' %
                                (escape(label), escape(value)) for label, value in decisions)
        formal_rows = "".join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' %
                              (escape(row["label"]), escape(row["hex"]), escape(row["use"]))
                              for row in roles["identity"])
        combination_rows = "".join('<tr><th scope="row">%s</th><td>%s in %s</td><td>%s</td></tr>' %
                                   (escape(row["label"]), escape(", ".join(row["colors"])),
                                    escape(row["artwork"]), escape(row["use"]))
                                   for row in roles["identity_combinations"])
        formal_detail = ('<h3>Formal identity colors</h3>'
                         '<table><tr><th>Color</th><th>HEX</th><th>Use</th></tr>%s</table>'
                         '<h3>Approved combinations and artwork</h3>'
                         '<table><tr><th>Application</th><th>Colors and artwork</th><th>Use</th></tr>%s</table>'
                         % (formal_rows, combination_rows))
        affiliation_detail = ('<div class="rule"></div><h3>Independent decisions</h3>'
                              '<table><tr><th>Decision</th><th>Declaration</th></tr>%s</table>%s'
                              % (decision_rows, "" if boundary or len(roles["identity"]) > 1 else formal_detail))
    affiliation_page = len(pages) + 1
    if aff["parent"]:
        pages.append(pg("Parent", endorsement,
        '<p>%s declares ShruggieTech parentage. Palette sharing and typography are separate explicit choices. The approved mark and colors remain this brand\'s own source decisions.</p>'
        '<div class="card" style="text-align:center;padding:7mm;margin:4mm 0"><div class="m" '
        'style="letter-spacing:.2em;text-transform:uppercase;color:%s">%s</div></div>'
        '<p class="dim">The approved mono family, uppercase, positive tracking. Visually subordinate and outside the '
        'logo clear space. Never a combined parent-product lockup.</p><div class="rule"></div>'
        '<h3>Load the system</h3><div class="card"><div class="code-block" style="line-height:2">'
        'npx shadcn@4.21.0 registry add @%s=%s/r/{name}.json<br>'
        'npx shadcn@4.21.0 add @%s/theme<br>npm i next-themes</div></div>'
        '<p class="dim">The catalog lists installable theme and component items. For offline fonts, copy nextjs/fonts.ts and fonts/ together from the kit.</p>'
        '%s%s' % (
            title,
            MU, endorsement, slug, B.get("registry_base", B.get("homepage", "https://shruggie.tech").rstrip("/") + "/brand"), slug,
            _ships(kit), affiliation_detail), affiliation_page))
    else:
        pages.append(pg("Affiliation", "Independent identity",
            '<p>This brand has no ShruggieTech parent or ownership endorsement.</p>%s%s'
            '<div class="rule"></div><h3>Load the system</h3><div class="card"><div class="code-block" style="line-height:2">'
            'npx shadcn@4.21.0 registry add @%s=%s/r/{name}.json<br>'
            'npx shadcn@4.21.0 add @%s/theme<br>npm i next-themes</div></div>'
            '<p class="dim">The catalog lists installable theme and component items. For offline fonts, copy nextjs/fonts.ts and fonts/ together from the kit.</p>%s%s' % (
                (('<div class="card" style="text-align:center;padding:7mm;margin:4mm 0"><div class="m" '
                  'style="letter-spacing:.2em;text-transform:uppercase;color:%s">%s</div></div>' % (MU, endorsement)) if endorsement else ""),
                (('<div class="callout acc"><div class="ey">Vendor and trademark boundary</div><p style="margin:0" class="dim">%s</p></div>' % boundary["notice"]) if boundary else ""),
                slug, B.get("registry_base", B.get("homepage", "").rstrip("/") + "/brand"), slug,
                _ships(kit), affiliation_detail), affiliation_page))

    if roles:
        compact = bool(boundary or len(roles["identity"]) > 1)
        rows = []
        for dark, light in zip(roles["interface"]["dark"], roles["interface"]["light"]):
            pairing = ('Dark: %s, %s text %.2f:1; surface %.2f:1<br>Light: %s, %s text %.2f:1; surface %.2f:1' %
                       (escape(dark["hex"]), escape(dark["foreground"]), dark["foreground_contrast"], dark["surface_contrast"],
                        escape(light["hex"]), escape(light["foreground"]), light["foreground_contrast"], light["surface_contrast"]))
            if not compact:
                pairing += '<br>Source: %s / %s' % (escape(dark["source"]), escape(light["source"]))
            rows.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
                        (escape(dark["label"]), escape(dark["use"]), pairing,
                         escape(dark["non_color_cue"])))
        candidates = [(color, cue) for color in roles["identity"] for cue in roles["interface"]["dark"]
                      if cue["id"] in {"action", "warning"} and color["hex"] == cue["hex"]]
        sample, cue = candidates[0] if candidates else (roles["identity"][0], roles["interface"]["dark"][1])
        example = ('<p>Correct: use %s (%s) in approved identity work; pair the %s cue (%s) with %s. Misuse: a lone identity swatch as the only %s signal.</p>' %
                   (escape(sample["label"]), escape(sample["hex"]), escape(cue["label"]), escape(cue["hex"]),
                    escape(cue["non_color_cue"].lower()), escape(cue["label"].lower())))
        pages.append(pg("Color roles", "Interface color cues",
                        '<p>Colors for actions and states are distinct from formal identity artwork. A shared HEX is a deliberate choice; meaning also uses words, icons, outlines, or state attributes.</p>'
                        '%s%s'
                        '<table class="%s"><tr><th>Cue</th><th>Purpose</th><th>Dark and light pairing</th><th>Additional cue</th></tr>%s</table>'
                        % (formal_detail if compact else "", example,
                           "role-cues-compact" if compact else "", "".join(rows)), len(pages) + 1))

    html = ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><title>%s brand guide"
            "</title><style>%s</style></head><body>%s</body></html>"
            % (slug, css, "\n".join(pages)))
    return html

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brand"); ap.add_argument("kit"); ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()
    with open(a.brand, encoding="utf-8") as handle:
        B = json.load(handle)
    os.makedirs(os.path.join(a.kit, "build"), exist_ok=True)
    hp = os.path.join(a.kit, "build", "brand-guide.print.html")
    with open(hp, "w", encoding="utf-8", newline="\n") as f: f.write(build(B, a.kit))
    print("wrote", hp)
    if a.html_only: return 0
    pdf_path = os.path.join(a.kit, "brand-guide.pdf")
    if os.path.isfile(pdf_path):
        os.remove(pdf_path)
    contact_sheet = os.path.join(a.kit, "qc", "contact-sheet.png")
    pdf_pages = os.path.join(a.kit, "qc", "_pdf-pages")
    if os.path.isfile(contact_sheet):
        os.remove(contact_sheet)
    if os.path.isdir(pdf_pages):
        for name in os.listdir(pdf_pages):
            page = os.path.join(pdf_pages, name)
            if name.endswith(".png") and os.path.isfile(page):
                os.remove(page)
        if not os.listdir(pdf_pages):
            os.rmdir(pdf_pages)
    capabilities = load_capabilities(a.kit)
    if capabilities["tier"] != "full":
        print("SKIP brand guide PDF: headless Chromium unavailable at %s tier"
              % capabilities["tier"])
        return 0
    try:
        from playwright.sync_api import sync_playwright
        import pathlib
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page()
            pg.goto("file://" + str(pathlib.Path(hp).resolve())); pg.wait_for_timeout(1800)
            pg.emulate_media(media="print")
            pg.pdf(path=pdf_path, format="A4", print_background=True,
                   margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
            b.close()
        print("wrote", pdf_path)
        ground = guide_surface_mode(B)
        print("Now run qc_render.py --expect-ground %s AND OPEN THE CONTACT SHEET." % ground)
    except Exception as e:
        print("FAIL brand guide PDF: Chromium was probed successfully but export failed (%s)" % e)
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
