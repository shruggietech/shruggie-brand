#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_glyph.py: decide whether a mark is correct without looking at it.

    python3 templates/validate_glyph.py <brand.json>
    python3 templates/validate_glyph.py <kit>/build/mk_paths.py --module

Every check here is a number, so this gate reads the same on a provider that
can view a rendered PNG and on one that cannot. `qc_images.py` still writes a
contact sheet and an agent that can see it still should, but a build is never
blocked on somebody having eyes.

The rasteriser is a scanline polygon fill written in plain Python. It exists so
this gate has no dependency on rsvg-convert, resvg, Inkscape, ImageMagick,
Pillow or a browser. On a locked-down sandbox those are the first things
missing, and a geometry check that silently skips is worse than no check.

WHAT IT MEASURES, AND WHY EACH ONE IS HERE
------------------------------------------
ink-inside-grid      Geometry outside its own viewBox is clipped at render
                     time. fragcap 1.0.0 shipped a wordmark whose crossbar sat
                     at x = -1 in a viewBox starting at 0.
optical-centring     A mark with an aperture or any asymmetry is not centred by
                     putting its construction centre at grid/2. Measured on the
                     flattened ink bbox, not on control points.
coverage             A mark under about 8 percent ink reads as thin and washed
                     out at small sizes; over about 60 percent it fills in.
ink-thickness        Mean stroke thickness in grid units. Strokes below the
                     floor break up at 16 px whatever else is true.
smallest-piece       Pixel area of the smallest surviving element at 16 px. An
                     element under two pixels is not there.
components           How many separate pieces of ink there are, at master size
                     and at 32 and 16 px. A piece that vanishes at 16 was a
                     detail that should have been dropped from the reduced
                     master. Two pieces that merge at 16 were too close.
counters             Enclosed holes, same three sizes. A counter that fills in
                     turns a G into a blob and an aperture C into an O.
reduced-master       The reduced master must actually be simpler than the full
                     one, and must survive 16 px on its own.

EXIT CODE
---------
Zero when there are no failures. Warnings do not block; failures do.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glyphkit as G                                          # noqa: E402


# ---------------------------------------------------------------- raster

def rasterise(paths, grid, size, fill_rules=None):
    """Scanline-fill a list of path-data strings into a size x size bitmap.

    Returns a list of bytearrays, one per row, 1 for ink. Sampling is at pixel
    centres, which is what a real rasteriser does, so the small-size component
    counts below behave the way the shipped PNG will.
    """
    fill_rules = fill_rules or {}
    grid = float(grid)
    scale = size / grid
    rows = [bytearray(size) for _ in range(size)]

    for idx, entry in enumerate(paths):
        d = entry["d"] if isinstance(entry, dict) else entry
        rule = (entry.get("fill_rule") if isinstance(entry, dict) else None) \
            or fill_rules.get(idx) or "nonzero"
        polys = G.flatten(d, steps=12)
        edges = []
        for poly in polys:
            for i in range(len(poly) - 1):
                x0, y0 = poly[i][0] * scale, poly[i][1] * scale
                x1, y1 = poly[i + 1][0] * scale, poly[i + 1][1] * scale
                if y0 == y1:
                    continue
                edges.append((x0, y0, x1, y1))
        if not edges:
            continue
        ylo = max(0, int(math.floor(min(min(e[1], e[3]) for e in edges))))
        yhi = min(size - 1, int(math.ceil(max(max(e[1], e[3]) for e in edges))))
        for py in range(ylo, yhi + 1):
            yc = py + 0.5
            xs = []
            for x0, y0, x1, y1 in edges:
                if (y0 <= yc < y1) or (y1 <= yc < y0):
                    t = (yc - y0) / (y1 - y0)
                    xs.append((x0 + t * (x1 - x0), 1 if y1 > y0 else -1))
            if not xs:
                continue
            xs.sort()
            row = rows[py]
            if rule == "evenodd":
                for i in range(0, len(xs) - 1, 2):
                    _span(row, xs[i][0], xs[i + 1][0], size)
            else:
                wind = 0
                for i in range(len(xs) - 1):
                    wind += xs[i][1]
                    if wind != 0:
                        _span(row, xs[i][0], xs[i + 1][0], size)
    return rows


def _span(row, xa, xb, size):
    a = max(0, int(math.ceil(xa - 0.5)))
    b = min(size - 1, int(math.floor(xb - 0.5)))
    for x in range(a, b + 1):
        row[x] = 1


# ---------------------------------------------------------------- topology

def components(rows, size, want=1):
    """Count 4-connected regions of `want`, and return their pixel sizes."""
    seen = [bytearray(size) for _ in range(size)]
    sizes = []
    for y in range(size):
        for x in range(size):
            if rows[y][x] != want or seen[y][x]:
                continue
            n, stack = 0, [(x, y)]
            seen[y][x] = 1
            while stack:
                cx, cy = stack.pop()
                n += 1
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if 0 <= nx < size and 0 <= ny < size \
                            and not seen[ny][nx] and rows[ny][nx] == want:
                        seen[ny][nx] = 1
                        stack.append((nx, ny))
            sizes.append(n)
    return sorted(sizes, reverse=True)


def counters(rows, size):
    """Enclosed background regions: the holes a reader sees as counters."""
    seen = [bytearray(size) for _ in range(size)]
    stack = []
    for i in range(size):
        for x, y in ((i, 0), (i, size - 1), (0, i), (size - 1, i)):
            if rows[y][x] == 0 and not seen[y][x]:
                seen[y][x] = 1
                stack.append((x, y))
    while stack:                                              # flood the outside
        cx, cy = stack.pop()
        for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
            if 0 <= nx < size and 0 <= ny < size \
                    and not seen[ny][nx] and rows[ny][nx] == 0:
                seen[ny][nx] = 1
                stack.append((nx, ny))
    holes, total = 0, 0
    for y in range(size):
        for x in range(size):
            if rows[y][x] == 0 and not seen[y][x]:
                holes += 1
                n, st = 0, [(x, y)]
                seen[y][x] = 1
                while st:
                    cx, cy = st.pop()
                    n += 1
                    for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                        if 0 <= nx < size and 0 <= ny < size \
                                and not seen[ny][nx] and rows[ny][nx] == 0:
                            seen[ny][nx] = 1
                            st.append((nx, ny))
                total += n
    return holes, total


def ink_thickness(rows, size, grid):
    """Mean ink thickness in grid units, as 2 * area / boundary length.

    A band of thickness t and length L has area tL and roughly 2L of boundary,
    so this returns t. It is deliberately not a ridge-following medial-axis
    measurement: on a discrete grid those produce spurious local maxima at every
    flat terminal and report a stem width an order of magnitude too small. This
    estimator has no free parameters and no failure mode of that kind.

    For a solid blob it reports the radius rather than the diameter, which is
    fine: the number exists to catch marks built from strokes that are too thin,
    and a blob is never that.
    """
    area = 0
    boundary = 0
    for y in range(size):
        row = rows[y]
        for x in range(size):
            if not row[x]:
                continue
            area += 1
            if (x == 0 or not row[x - 1] or x == size - 1 or not row[x + 1]
                    or y == 0 or not rows[y - 1][x]
                    or y == size - 1 or not rows[y + 1][x]):
                boundary += 1
    if not boundary:
        return 0.0
    return 2.0 * area / boundary * grid / size


# ---------------------------------------------------------------- report

class Report(object):
    def __init__(self):
        self.rows = []
        self.fails = 0
        self.warns = 0

    def ok(self, name, detail):
        self.rows.append(("ok", name, detail))

    def warn(self, name, detail):
        self.rows.append(("WARN", name, detail))
        self.warns += 1

    def bad(self, name, detail):
        self.rows.append(("FAIL", name, detail))
        self.fails += 1

    def render(self):
        w = max(len(r[1]) for r in self.rows)
        out = []
        for state, name, detail in self.rows:
            out.append("%-4s %-*s %s" % (state, w, name, detail))
        out.append("")
        out.append("%d checks, %d warnings, %d failures"
                   % (len(self.rows), self.warns, self.fails))
        return "\n".join(out)


def measure(paths, grid, label, rep, reduced=False):
    """Run every check against one master and record the numbers."""
    prefix = "%s " % label

    for entry in paths:
        d = entry["d"] if isinstance(entry, dict) else entry
        if not G.path_commands_ok(d):
            rep.bad(prefix + "commands",
                    "path uses a command outside absolute M, L, C, Z. Compose it "
                    "with glyphkit rather than writing path data by hand.")
            return None

    x0, y0, x1, y1 = G.bbox(paths)
    w, h = x1 - x0, y1 - y0
    if x0 < -0.5 or y0 < -0.5 or x1 > grid + 0.5 or y1 > grid + 0.5:
        rep.bad(prefix + "ink-inside-grid",
                "ink bbox (%.1f %.1f %.1f %.1f) leaves the %g grid and will be clipped"
                % (x0, y0, x1, y1, grid))
    else:
        rep.ok(prefix + "ink-inside-grid",
               "bbox %.1f %.1f %.1f %.1f, %.0f x %.0f units" % (x0, y0, x1, y1, w, h))

    off_x = ((x0 + x1) / 2.0 - grid / 2.0) / grid * 100.0
    off_y = ((y0 + y1) / 2.0 - grid / 2.0) / grid * 100.0
    worst = max(abs(off_x), abs(off_y))
    detail = "offset %+.2f%% x, %+.2f%% y from grid centre" % (off_x, off_y)
    if worst > 1.5:
        rep.warn(prefix + "optical-centring",
                 detail + ". Finish the mark with glyphkit.center_ink().")
    else:
        rep.ok(prefix + "optical-centring", detail)

    N = 256
    rows = rasterise(paths, grid, N)
    ink = sum(sum(r) for r in rows)
    cov = 100.0 * ink / (N * N)
    if ink == 0:
        rep.bad(prefix + "coverage", "no ink rasterised: the geometry is degenerate")
        return None
    if cov < 6.0:
        rep.warn(prefix + "coverage", "%.1f%% ink, thin enough to wash out at small sizes" % cov)
    elif cov > 62.0:
        rep.warn(prefix + "coverage", "%.1f%% ink, heavy enough to fill in at small sizes" % cov)
    else:
        rep.ok(prefix + "coverage", "%.1f%% ink at 256 px" % cov)

    stem = ink_thickness(rows, N, grid)
    floor = grid * (0.060 if reduced else 0.035)
    detail = "%.0f units, %.1f%% of the grid" % (stem, 100.0 * stem / grid)
    if stem < floor:
        rep.warn(prefix + "ink-thickness",
                 detail + " (below the %.1f%% floor for a %s master; strokes this "
                 "thin break up at 16 px)" % (100.0 * floor / grid,
                                              "reduced" if reduced else "full"))
    else:
        rep.ok(prefix + "ink-thickness", detail)

    comp_master = components(rows, N)
    hole_master, _ = counters(rows, N)
    small = {}
    for s in (32, 16):
        r = rasterise(paths, grid, s)
        small[s] = (components(r, s), counters(r, s)[0], sum(sum(x) for x in r))

    n16, n32, nm = len(small[16][0]), len(small[32][0]), len(comp_master)
    detail = "%d at 256, %d at 32, %d at 16" % (nm, n32, n16)
    if small[16][2] == 0:
        rep.bad(prefix + "components", "nothing survives rasterisation at 16 px")
    elif n16 != nm or n32 != nm:
        # Check BOTH small sizes. A gap can close at 32 and reopen at 16 purely
        # from where the pixel centres fall, so testing only 16 misses it.
        worst = n32 if n32 != nm else n16
        rep.warn(prefix + "components",
                 detail + ". Pieces %s below master size; separate them further or "
                 "merge them deliberately."
                 % ("merge" if worst < nm else "fragment"))
    else:
        rep.ok(prefix + "components", detail)

    smallest = min(small[16][0]) if small[16][0] else 0
    detail = "smallest piece is %d px of 256 at 16 px" % smallest
    if smallest < 2:
        rep.bad(prefix + "smallest-piece", detail + ". That element is invisible "
                "at favicon size; drop it from the reduced master.")
    elif smallest < 6:
        rep.warn(prefix + "smallest-piece", detail + ". Barely resolvable.")
    else:
        rep.ok(prefix + "smallest-piece", detail)

    detail = "%d at 256, %d at 32, %d at 16" % (
        hole_master, small[32][1], small[16][1])
    if small[16][1] < hole_master or small[32][1] < hole_master:
        (rep.bad if reduced else rep.warn)(
            prefix + "counters", detail + ". A counter closes at 16 px, so the "
            "silhouette changes shape at favicon size.")
    else:
        rep.ok(prefix + "counters", detail)

    return {"bbox": (x0, y0, x1, y1), "coverage": cov, "thickness": stem,
            "components": len(comp_master), "counters": hole_master,
            "components_16": len(small[16][0]), "counters_16": small[16][1]}


def load(spec):
    """Accept a brand.json, or a mk_paths.py exposing `full` and `reduced`."""
    if spec.endswith(".py"):
        import importlib.util
        name = os.path.splitext(os.path.basename(spec))[0]
        s = importlib.util.spec_from_file_location(name, spec)
        m = importlib.util.module_from_spec(s)
        sys.path.insert(0, os.path.dirname(os.path.abspath(spec)))
        s.loader.exec_module(m)
        return {"grid": getattr(m, "GRID", 1000),
                "full": m.full,
                "reduced": getattr(m, "reduced", None)}
    B = json.load(open(spec, encoding="utf-8"))
    lg = B.get("logo") or {}
    paths = lg.get("paths") or {}
    return {"grid": lg.get("grid", 1000),
            "full": paths.get("full"),
            "reduced": paths.get("reduced")}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__.strip().splitlines()[2].strip())
        return 2
    data = load(args[0])
    if not data["full"]:
        print("no full master found in %s" % args[0])
        return 2

    rep = Report()
    grid = float(data["grid"])
    full = measure(data["full"], grid, "full", rep)

    if not data["reduced"]:
        rep.warn("reduced-master",
                 "absent. Below 32 px the full mark will be downscaled, which is "
                 "the defect this house keeps rediscovering.")
    else:
        red = measure(data["reduced"], grid, "reduced", rep, reduced=True)
        if full and red:
            same = json.dumps(data["reduced"], sort_keys=True) == \
                json.dumps(data["full"], sort_keys=True)
            if same:
                rep.bad("reduced-master",
                        "identical to the full master. It must drop whole elements.")
            elif red["thickness"] < full["thickness"] * 0.99 and red["components"] >= full["components"]:
                rep.warn("reduced-master",
                         "thinner and no simpler than the full master (%.0f vs %.0f "
                         "units, %d vs %d pieces). Remove elements rather than "
                         "shrinking them." % (red["thickness"], full["thickness"],
                                              red["components"], full["components"]))
            else:
                rep.ok("reduced-master",
                       "%d pieces at %.0f units thick, against %d at %.0f for the full"
                       % (red["components"], red["thickness"],
                          full["components"], full["thickness"]))

    print(rep.render())
    return min(rep.fails, 125)


if __name__ == "__main__":
    sys.exit(main())
