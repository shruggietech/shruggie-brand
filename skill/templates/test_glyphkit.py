#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_glyphkit.py: self-test for the geometry layer.

    python3 templates/test_glyphkit.py

Standard library only, no test runner. Run it after touching glyphkit.py or
validate_glyph.py, and on any machine where the pipeline is behaving oddly: a
geometry bug that reaches a kit is expensive, and every case here is one that
actually happened.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glyphkit as G
import validate_glyph as V

GRID = 1000
fails = []


def check(name, cond, detail=""):
    print("%-4s %s%s" % ("ok" if cond else "FAIL", name, ("  " + detail) if detail else ""))
    if not cond:
        fails.append(name)


def comps(paths, size=256):
    return V.components(V.rasterise(paths, GRID, size), size)


# Every primitive must rasterise to exactly one connected region. A primitive
# that comes apart is self-intersecting, and the classic cause is an offset
# normal pointing the wrong way, which looks correct in a vector editor.
for name, d in [
    ("disc", G.disc(500, 500, 300)),
    ("rect", G.rect(200, 200, 600, 600)),
    ("rounded_rect", G.rounded_rect(150, 150, 700, 700, 180)),
    ("wedge", G.wedge(500, 500, 400, 20, 200)),
    ("ring_band radial", G.ring_band(500, 500, 420, 250, 30, 300)),
    ("ring_band round", G.ring_band(500, 500, 420, 250, 30, 300, cap="round")),
    ("polygon", G.polygon([(200, 200), (800, 300), (700, 820), (250, 700)])),
]:
    check("one piece: " + name, comps([{"d": d}]) == [comps([{"d": d}])[0]] and len(comps([{"d": d}])) == 1)

for ang in [(300, 700, 700, 300), (200, 500, 800, 500), (500, 200, 500, 800),
            (700, 300, 300, 700), (250, 250, 780, 760)]:
    d = G.capsule(ang[0], ang[1], ang[2], ang[3], 120)
    n = len(comps([{"d": d}]))
    check("one piece: capsule %s" % (ang,), n == 1, "got %d regions" % n)

# A ring must have a hole under BOTH fill rules, which means the inner contour
# is wound backwards. Two contours wound the same way fill solid under nonzero.
r = [{"d": G.ring(500, 500, 420, 240)}]
holes_nonzero = V.counters(V.rasterise(r, GRID, 256), 256)[0]
r_eo = [{"d": G.ring(500, 500, 420, 240), "fill_rule": "evenodd"}]
holes_evenodd = V.counters(V.rasterise(r_eo, GRID, 256), 256)[0]
check("ring hole under nonzero", holes_nonzero == 1, "got %d" % holes_nonzero)
check("ring hole under evenodd", holes_evenodd == 1, "got %d" % holes_evenodd)

# The bbox must follow the curve, not the control points. A regex over the
# numbers reads control points as if they were on the curve and over-reports.
d = G.disc(500, 500, 400)
x0, y0, x1, y1 = G.bbox([{"d": d}])
check("bbox follows the curve", abs((x1 - x0) - 800) < 6, "width %.1f, expected 800" % (x1 - x0))

# center_ink must centre the INK, not the construction.
off = G.center_ink([{"d": G.ring_band(500, 500, 420, 252, 42, 318)}], GRID)
bx0, by0, bx1, by1 = G.bbox(off)
check("center_ink centres the ink",
      abs((bx0 + bx1) / 2 - 500) < 1 and abs((by0 + by1) / 2 - 500) < 1,
      "centre %.1f %.1f" % ((bx0 + bx1) / 2, (by0 + by1) / 2))

# The command rule is enforced, not merely documented.
check("rejects an arc command", not G.path_commands_ok("M0 0A10 10 0 1 1 20 20Z"))
check("rejects relative commands", not G.path_commands_ok("m0 0 l10 10 z"))
check("rejects H and V", not G.path_commands_ok("M0 0H10V10Z"))
check("accepts absolute M L C Z", G.path_commands_ok(G.rect(0, 0, 10, 10)))

# Imported geometry preserves shipped path data. Unsupported commands remain
# visible, but they warn instead of forcing a redraw. Glyphkit-authored paths
# keep the strict failure because they can be regenerated safely.
legacy = [{"d": "M100 100H900V900H100Z"}]
imported_report = V.Report()
V.measure(legacy, GRID, "full", imported_report,
          provenance="imported", provenance_reason="shipped before glyphkit")
check("imported commands warn",
      imported_report.fails == 0 and imported_report.warns == 2,
      "%d warnings, %d failures" % (imported_report.warns, imported_report.fails))

glyphkit_report = V.Report()
V.measure(legacy, GRID, "full", glyphkit_report, provenance="glyphkit")
check("glyphkit commands fail",
      glyphkit_report.fails == 1 and glyphkit_report.warns == 0,
      "%d warnings, %d failures" % (glyphkit_report.warns, glyphkit_report.fails))

# Arc segmentation: a full circle must not be emitted as one cubic.
segs = G.arc_points(500, 500, 400, 0, 360)
check("arcs are split at 45 degrees", len(segs) == 8, "got %d segments" % len(segs))

# Deterministic formatting, because the manifest checksums path data.
check("formatting is deterministic", G.disc(500, 500, 300) == G.disc(500, 500, 300))
check("negative zero normalised", G.fmt(-0.0001) == "0")

# Unclosed subpaths must raise rather than emit an open filled region.
try:
    G.Path().move(0, 0).line(10, 10).d()
    check("unclosed subpath raises", False)
except ValueError:
    check("unclosed subpath raises", True)

print("")
print("%d checks, %d failures" % (16 + 7 + 5 + 2, len(fails)))
sys.exit(1 if fails else 0)
