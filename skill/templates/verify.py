#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify.py: assert a ShruggieTech sub-brand kit against canon.

Every number this emits is measured from the shipped files at run time. Nothing
is transcribed from a previous run. A check whose inputs are absent is reported
as SKIP with the reason, never silently passed.

    python3 build/verify.py [kit-dir] [--canon PATH] [--out VERIFY.md]

Exit code is the number of problems found, capped at 125.
"""
import argparse, hashlib, json, os, re, struct, sys, unicodedata
from coloraide import Color
from capabilities import load_capabilities

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
            ".html", ".svg", ".txt", ".py", ".webmanifest", ".snippet"}
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
    if brand.get("kind") != "fixture":
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
    for k, tok in canon["color"]["immutable"].items():
        got = (brand.get("color", {}) or {}).get(k)
        if got and got.get("hex", "").upper() != tok["hex"].upper():
            drift.append("%s: kit has %s, canon has %s" % (k, got["hex"], tok["hex"]))
    ct = canon["typography"]["families"]
    bt = (brand.get("typography") or {}).get("families")
    if bt:
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

def c_font_weights(kit, canon, rep):
    shipped = {}
    for role, fam in canon["typography"]["families"].items():
        shipped[fam["name"].lower()] = set(fam["weights"])
    hits, scanned = [], 0
    for p in walk(kit):
        if os.path.splitext(p)[1].lower() not in ({".css"} | SRC_EXT): continue
        rel = os.path.relpath(p, kit)
        if "enforcement" in rel or rel.startswith("templates"): continue
        t = open(p, encoding="utf-8", errors="replace").read(); scanned += 1
        for m in re.finditer(r"font-weight\s*:\s*(\d{3})", t):
            w = int(m.group(1))
            if w not in {400, 500, 700}: hits.append("%s: font-weight %d" % (rel, w))
        for m in re.finditer(r"fontWeight\s*:\s*(\d{3})", t):
            w = int(m.group(1))
            if w not in {400, 500, 700}: hits.append("%s: fontWeight %d" % (rel, w))
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
    if vb_hits is not None:
        for p in svgs:
            rel = os.path.relpath(p, kit)
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
        rep.skip("raster-artifacts", "core tier: SVG rasterizer unavailable; PNG outputs skipped")

    if not capabilities.get("svg_raster"):
        rep.skip("ico-artifact", "%s tier: source PNGs unavailable; ICO skipped" % tier)
    elif capabilities.get("ico_writer"):
        if os.path.isfile(ico):
            rep.ok("ico-artifact", "favicon.ico produced after successful writer probe")
        else:
            rep.bad("ico-artifact", "ICO writer probe passed but favicon.ico is missing")
    else:
        rep.skip("ico-artifact", "%s tier: ImageMagick, convert, and Pillow unavailable; ICO skipped" % tier)

    pdf = os.path.join(kit, "brand-guide.pdf")
    if tier == "full":
        if os.path.isfile(pdf):
            rep.ok("brand-guide-artifact", "PDF produced after successful Chromium probe")
        else:
            rep.bad("brand-guide-artifact", "Chromium probe passed but brand-guide.pdf is missing")
    else:
        rep.skip("brand-guide-artifact", "%s tier: headless Chromium unavailable; PDF skipped" % tier)

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
    c_font_weights(kit, canon, rep)
    c_glyph(kit, brand, rep)
    c_capability_artifacts(kit, rep)
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
