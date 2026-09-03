#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
glyphkit.py: parametric mark geometry, and a way to measure it without eyes.

WHY THIS EXISTS
---------------
Every logo failure this house has recorded came from one habit: an agent typing
SVG path data directly, then having no mechanical way to tell whether the result
was correct. That habit produced a wordmark clipped by its own viewBox, a mark
whose stroke geometry did not survive expand-to-outlines, an arc drawn with the
wrong Bezier constant, and a mark that looked centred in the file and off-centre
on the page. On a provider that cannot look at a rendered PNG, none of these are
detectable at all, so the run either ships something broken or flails.

So the agent does not type path data. It composes primitives from this module,
which can only emit well-formed geometry, and then measures the result with
`validate_glyph.py`, which rasterises the paths in pure Python and reports
numbers. Nothing here imports anything outside the standard library, nothing
shells out, and nothing needs a renderer, a browser, or a font.

WHAT THE AGENT WRITES
---------------------
A short script at `build/mk_paths.py` in the kit, which imports this module,
declares the mark's parameters as named constants, and exposes `full` and
`reduced` as lists of {"role": ..., "d": ...}. That script is the master. The
path data in brand.json is generated from it and is never edited by hand.

    import glyphkit as G
    GRID = 1000
    full = [
        {"role": "accent",   "d": G.ring_band(cx, cy, 420, 252, 88, 318)},
        {"role": "emphasis", "d": G.ring_band(cx, cy, 420, 252, 42, 78)},
    ]

THE COMMAND RULE
----------------
Everything emitted here is absolute `M`, `L`, `C`, `Z` with explicit x y pairs
and nothing else. That is not stylistic. Several tools in this kit, and every
naive bbox reader ever written, parse path data by pulling numbers out in order
and pairing them as coordinates. An `A` command carries three non-coordinate
numbers in the middle of its argument list, and `H` and `V` carry one number
where a pair is expected, so both silently corrupt any such reader. Relative
commands corrupt it differently and worse. Absolute M/L/C/Z is the subset where
positional parsing is exactly right, and it is enough to draw anything.

ANGLES
------
Degrees, counter-clockwise, zero pointing right, in the ordinary mathematical
sense. The y axis is flipped on the way into SVG coordinates, so 90 is the top
of the canvas and 270 is the bottom. Say what you mean in maths and let the
module handle the flip; an agent doing that conversion by hand gets it wrong.
"""

import math

__all__ = [
    "fmt", "pt", "Path",
    "arc_points", "arc", "ring_band", "wedge", "disc", "ring",
    "rounded_rect", "rect", "polygon", "capsule",
    "flatten", "bbox", "translate", "scale", "center_ink",
    "path_commands_ok", "MAX_ARC_SEGMENT_DEGREES",
]

# A cubic approximates a circular arc well below roughly 90 degrees and poorly
# above it. 45 keeps the maximum radial error near one part in 40,000 of the
# radius, which is invisible at any size a logo is ever reproduced at.
MAX_ARC_SEGMENT_DEGREES = 45.0

_EPS = 1e-9


# ---------------------------------------------------------------- formatting

def fmt(v):
    """Two decimals, trailing zeros stripped, negative zero normalised.

    Path data is compared byte for byte by the manifest checksum, so the
    formatter has to be deterministic. Python's repr of a float is not.
    """
    if abs(v) < 0.005:
        v = 0.0
    s = "%.2f" % v
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


def pt(x, y):
    return "%s %s" % (fmt(x), fmt(y))


# ---------------------------------------------------------------- path builder

class Path(object):
    """An absolute-only path builder.

    Use it when a primitive does not cover the shape. It refuses relative and
    shorthand commands by simply not offering them, and it tracks whether the
    current subpath was closed so `d()` can complain rather than emit an open
    filled region.
    """

    def __init__(self):
        self._parts = []
        self._open = False
        self._start = None
        self._cur = None

    def move(self, x, y):
        if self._open:
            raise ValueError("move() with an unclosed subpath: call close() first")
        self._parts.append("M%s" % pt(x, y))
        self._open = True
        self._start = (x, y)
        self._cur = (x, y)
        return self

    def line(self, x, y):
        self._require_open("line")
        self._parts.append("L%s" % pt(x, y))
        self._cur = (x, y)
        return self

    def curve(self, x1, y1, x2, y2, x, y):
        self._require_open("curve")
        self._parts.append("C%s %s %s" % (pt(x1, y1), pt(x2, y2), pt(x, y)))
        self._cur = (x, y)
        return self

    def arc(self, cx, cy, r, a0, a1):
        """Append a circular arc, moving to its start if the subpath is empty."""
        segs = arc_points(cx, cy, r, a0, a1)
        if not self._open:
            self.move(*segs[0][0])
        else:
            sx, sy = segs[0][0]
            if abs(sx - self._cur[0]) > 1e-6 or abs(sy - self._cur[1]) > 1e-6:
                self.line(sx, sy)
        for _, c1, c2, end in segs:
            self.curve(c1[0], c1[1], c2[0], c2[1], end[0], end[1])
        return self

    def close(self):
        self._require_open("close")
        self._parts.append("Z")
        self._open = False
        self._cur = self._start
        return self

    def d(self):
        if self._open:
            raise ValueError("d() with an unclosed subpath: a filled region must be closed")
        if not self._parts:
            raise ValueError("d() on an empty path")
        return " ".join(self._parts)

    def _require_open(self, what):
        if not self._open:
            raise ValueError("%s() before move(): a path must start with move()" % what)

    def __str__(self):
        return self.d()


# ---------------------------------------------------------------- arcs

def _polar(cx, cy, r, deg):
    t = math.radians(deg)
    return (cx + r * math.cos(t), cy - r * math.sin(t))


def _tangent(deg):
    """Unit tangent in the direction of increasing angle, in SVG coordinates."""
    t = math.radians(deg)
    return (-math.sin(t), -math.cos(t))


def arc_points(cx, cy, r, a0, a1):
    """Cubic segments approximating the arc from a0 to a1 along radius r.

    Signed: a1 below a0 sweeps clockwise on screen. Returns a list of
    (start, control1, control2, end) tuples so callers can decide how to join
    them. Segments are split so none exceeds MAX_ARC_SEGMENT_DEGREES.
    """
    if r <= 0:
        raise ValueError("arc radius must be positive, got %r" % (r,))
    span = float(a1) - float(a0)
    if abs(span) < _EPS:
        raise ValueError("arc from %r to %r has zero span" % (a0, a1))
    n = max(1, int(math.ceil(abs(span) / MAX_ARC_SEGMENT_DEGREES)))
    step = span / n
    # The magic constant. k = 4/3 * tan(theta/4) is the control-point distance,
    # as a fraction of the radius, that makes a cubic touch the arc at its
    # midpoint. Getting this wrong by using a fixed 0.5523 (which is only
    # correct for a 90 degree quadrant) is the classic hand-drawn arc bug.
    k = (4.0 / 3.0) * math.tan(math.radians(step) / 4.0)
    out = []
    a = float(a0)
    for _ in range(n):
        b = a + step
        p0, p1 = _polar(cx, cy, r, a), _polar(cx, cy, r, b)
        t0, t1 = _tangent(a), _tangent(b)
        c1 = (p0[0] + k * r * t0[0], p0[1] + k * r * t0[1])
        c2 = (p1[0] - k * r * t1[0], p1[1] - k * r * t1[1])
        out.append((p0, c1, c2, p1))
        a = b
    return out


def arc(cx, cy, r, a0, a1):
    """An open arc as path data, starting with M. Rarely what you want on its
    own: a logo is filled regions, so reach for ring_band or wedge first."""
    segs = arc_points(cx, cy, r, a0, a1)
    p = Path().move(*segs[0][0])
    for _, c1, c2, end in segs:
        p.curve(c1[0], c1[1], c2[0], c2[1], end[0], end[1])
    return " ".join(p._parts)


# ---------------------------------------------------------------- primitives

def ring_band(cx, cy, r_out, r_in, a0, a1, cap="radial"):
    """A closed annular segment: the workhorse for aperture and ring marks.

    cap "radial" cuts both ends along a radius, which is what almost every
    geometric mark wants. cap "round" finishes each end with a semicircle of
    diameter (r_out - r_in), which reads softer and holds up better at 16 px
    because it removes two sharp corners.
    """
    if r_in >= r_out:
        raise ValueError("r_in (%r) must be smaller than r_out (%r)" % (r_in, r_out))
    if r_in < 0:
        raise ValueError("r_in must not be negative")
    if cap not in ("radial", "round"):
        raise ValueError("cap must be 'radial' or 'round', got %r" % (cap,))

    mid = (r_out + r_in) / 2.0
    half = (r_out - r_in) / 2.0
    # Which way the caps bulge depends on which way the band sweeps. Getting
    # this backwards makes the cap fold into the band, and the result renders as
    # a bar with a bite out of it or as several disconnected pieces. The cap arc
    # must START where the previous arc ENDED, at the outer radius, which is
    # angle a1 on the cap circle, and run 180 degrees in the sweep direction.
    sgn = 1.0 if a1 >= a0 else -1.0
    p = Path()
    p.arc(cx, cy, r_out, a0, a1)
    if cap == "round":
        ex, ey = _polar(cx, cy, mid, a1)
        p.arc(ex, ey, half, a1, a1 + 180.0 * sgn)
    p.arc(cx, cy, r_in, a1, a0)
    if cap == "round":
        sx, sy = _polar(cx, cy, mid, a0)
        p.arc(sx, sy, half, a0 - 180.0 * sgn, a0)
    return p.close().d()


def ring(cx, cy, r_out, r_in):
    """A complete annulus as two subpaths.

    The inner circle is wound in the OPPOSITE direction to the outer one, so the
    hole appears under fill-rule nonzero as well as evenodd. Two subpaths wound
    the same way are a classic silent failure: the file looks right in an editor
    that defaults to evenodd and renders as a solid disc everywhere else, and
    nothing in a text diff shows why.
    """
    if r_in >= r_out:
        raise ValueError("r_in (%r) must be smaller than r_out (%r)" % (r_in, r_out))
    outer = Path().arc(cx, cy, r_out, 0, 360).close().d()
    inner = Path().arc(cx, cy, r_in, 360, 0).close().d()
    return outer + " " + inner


def wedge(cx, cy, r, a0, a1):
    """A pie slice from the centre."""
    p = Path().move(cx, cy)
    p.arc(cx, cy, r, a0, a1)
    return p.close().d()


def disc(cx, cy, r):
    return Path().arc(cx, cy, r, 0, 360).close().d()


def rect(x, y, w, h):
    if w <= 0 or h <= 0:
        raise ValueError("rect needs positive width and height")
    return (Path().move(x, y).line(x + w, y).line(x + w, y + h)
            .line(x, y + h).close().d())


def rounded_rect(x, y, w, h, r):
    """Corners as quarter-circle cubics. r is clamped to half the short side."""
    if w <= 0 or h <= 0:
        raise ValueError("rounded_rect needs positive width and height")
    r = max(0.0, min(float(r), min(w, h) / 2.0))
    if r < _EPS:
        return rect(x, y, w, h)
    k = (4.0 / 3.0) * math.tan(math.pi / 8.0) * r     # quarter circle
    p = Path().move(x + r, y)
    p.line(x + w - r, y)
    p.curve(x + w - r + k, y, x + w, y + r - k, x + w, y + r)
    p.line(x + w, y + h - r)
    p.curve(x + w, y + h - r + k, x + w - r + k, y + h, x + w - r, y + h)
    p.line(x + r, y + h)
    p.curve(x + r - k, y + h, x, y + h - r + k, x, y + h - r)
    p.line(x, y + r)
    p.curve(x, y + r - k, x + r - k, y, x + r, y)
    return p.close().d()


def capsule(x0, y0, x1, y1, thickness):
    """A round-ended bar between two points. Useful for abstract marks built
    from strokes, which must still ship as filled outlines."""
    dx, dy = x1 - x0, y1 - y0
    length = math.hypot(dx, dy)
    if length < _EPS:
        raise ValueError("capsule endpoints coincide")
    if thickness <= 0:
        raise ValueError("capsule thickness must be positive")
    half = thickness / 2.0
    ang = math.degrees(math.atan2(-dy, dx))           # SVG y is down
    # The offset normal must match where the end-cap arc STARTS, at ang+90.
    # Flip this sign and the two lines cross, the path becomes a bowtie, and the
    # shape rasterises into three disconnected pieces while still looking like a
    # bar in a vector editor. validate_glyph caught exactly that; a person
    # eyeballing the SVG would not have.
    nx, ny = dy / length * half, -dx / length * half
    p = Path().move(x0 + nx, y0 + ny).line(x1 + nx, y1 + ny)
    p.arc(x1, y1, half, ang + 90.0, ang - 90.0)
    p.line(x0 - nx, y0 - ny)
    p.arc(x0, y0, half, ang - 90.0, ang - 270.0)
    return p.close().d()


def polygon(points):
    if len(points) < 3:
        raise ValueError("polygon needs at least three points")
    p = Path().move(points[0][0], points[0][1])
    for x, y in points[1:]:
        p.line(x, y)
    return p.close().d()


# ---------------------------------------------------------------- measurement

def _tokenize(d):
    """Split path data into (command, [numbers]). Absolute M/L/C/Z only, by
    design: anything else is rejected loudly rather than mis-parsed quietly."""
    out, i, n = [], 0, len(d)
    num = ""
    cmd = None
    args = []

    def flush_num():
        nonlocal num
        if num:
            args.append(float(num))
            num = ""

    while i < n:
        ch = d[i]
        if ch in "MLCZ":
            flush_num()
            if cmd is not None:
                out.append((cmd, args))
            cmd, args = ch, []
        elif ch in "mlczHhVvAaSsQqTt":
            raise ValueError(
                "path uses command %r. glyphkit emits absolute M, L, C and Z only; "
                "relative, shorthand and arc commands break positional coordinate "
                "readers used elsewhere in this kit" % ch)
        elif ch in "-+":
            if num and num[-1] not in "eE":
                flush_num()
            num += ch
        elif ch.isdigit() or ch == ".":
            num += ch
        elif ch in "eE":
            num += ch
        elif ch in " ,\t\r\n":
            flush_num()
        else:
            raise ValueError("unexpected character %r in path data" % ch)
        i += 1
    flush_num()
    if cmd is not None:
        out.append((cmd, args))
    return out


def path_commands_ok(d):
    """True when the path parses under the absolute-only rule. Used by verify."""
    try:
        _tokenize(d)
        return True
    except ValueError:
        return False


def _cubic(p0, p1, p2, p3, steps):
    for i in range(1, steps + 1):
        t = i / float(steps)
        u = 1.0 - t
        x = (u * u * u * p0[0] + 3 * u * u * t * p1[0]
             + 3 * u * t * t * p2[0] + t * t * t * p3[0])
        y = (u * u * u * p0[1] + 3 * u * u * t * p1[1]
             + 3 * u * t * t * p2[1] + t * t * t * p3[1])
        yield (x, y)


def flatten(d, steps=16):
    """Path data to a list of closed polygons in device order.

    Curves are sampled rather than bounded, so the bbox this feeds is the real
    ink extent. The naive alternative, running a regex over the numbers, reads
    Bezier CONTROL points as if they were on the curve and reports a box that
    can be several percent too large. That is what makes a mark look wrongly
    centred after an automated fit.
    """
    polys, cur, start = [], [], None
    for cmd, args in _tokenize(d):
        if cmd == "M":
            if len(args) != 2:
                raise ValueError("M takes exactly one coordinate pair")
            if cur:
                polys.append(cur)
            start = (args[0], args[1])
            cur = [start]
        elif cmd == "L":
            if len(args) % 2 or not args:
                raise ValueError("L takes whole coordinate pairs")
            for i in range(0, len(args), 2):
                cur.append((args[i], args[i + 1]))
        elif cmd == "C":
            if len(args) % 6 or not args:
                raise ValueError("C takes groups of three coordinate pairs")
            for i in range(0, len(args), 6):
                p0 = cur[-1]
                cur.extend(_cubic(p0, (args[i], args[i + 1]),
                                  (args[i + 2], args[i + 3]),
                                  (args[i + 4], args[i + 5]), steps))
        elif cmd == "Z":
            if cur:
                if cur[0] != cur[-1]:
                    cur.append(cur[0])
                polys.append(cur)
                cur = [start] if start else []
                cur = []
    if cur and len(cur) > 2:
        polys.append(cur)
    return [p for p in polys if len(p) > 2]


def bbox(paths, steps=16):
    """Exact ink bounding box of a list of {"d": ...} entries or raw strings."""
    xs, ys = [], []
    for entry in paths:
        d = entry["d"] if isinstance(entry, dict) else entry
        for poly in flatten(d, steps):
            for x, y in poly:
                xs.append(x)
                ys.append(y)
    if not xs:
        raise ValueError("no geometry to measure")
    return (min(xs), min(ys), max(xs), max(ys))


def _map_path(d, fn):
    out = []
    for cmd, args in _tokenize(d):
        if cmd == "Z":
            out.append("Z")
            continue
        pairs = []
        for i in range(0, len(args), 2):
            pairs.append(pt(*fn(args[i], args[i + 1])))
        out.append(cmd + " ".join(pairs))
    return " ".join(out)


def translate(paths, dx, dy):
    fn = lambda x, y: (x + dx, y + dy)
    return [dict(p, d=_map_path(p["d"], fn)) if isinstance(p, dict)
            else _map_path(p, fn) for p in paths]


def scale(paths, factor, origin=(0.0, 0.0)):
    ox, oy = origin
    fn = lambda x, y: (ox + (x - ox) * factor, oy + (y - oy) * factor)
    return [dict(p, d=_map_path(p["d"], fn)) if isinstance(p, dict)
            else _map_path(p, fn) for p in paths]


def center_ink(paths, grid, steps=16):
    """Translate so the real ink bbox is centred on the grid.

    A mark with an aperture, a descender, or any asymmetry is NOT centred by
    putting its construction centre at grid/2. Compose the mark wherever the
    maths is clearest, then finish with this. Doing it by eye, or by nudging a
    constant until a preview looks right, is how a mark ends up two percent off
    and nobody can say why.
    """
    x0, y0, x1, y1 = bbox(paths, steps)
    dx = (grid - (x1 - x0)) / 2.0 - x0
    dy = (grid - (y1 - y0)) / 2.0 - y0
    return translate(paths, dx, dy)
