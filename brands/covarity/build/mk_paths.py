#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Covarity mark geometry, hand-authored on a 1000-unit grid.

The mark is an aperture C split at its upper terminal. The long arc is the
identity accent (durable knowledge). The short terminal arc is the inherited
ShruggieTech orange (agent context). The radial slot between them is the
adjudication boundary, and it is a declared dimension, not a visual accident.

Only M, C, L and Z are emitted, with every coordinate written as an explicit
x y pair. gen_logo.py's bbox assertion reads coordinates positionally, so
arc, H and V commands would make it read garbage.
"""
import json, math

GRID   = 1000.0
CX, CY = 554.0, 500.0        # optically centred: see bbox print at the bottom
R_OUT  = 420.0
R_IN   = 252.0               # 168-unit ring
R_IN_R = 230.0               # reduced mark runs a 190-unit ring

APERTURE_START = 318.0       # lower terminal, measured counter-clockwise from east
APERTURE_END   =  42.0       # upper terminal
SLOT_FROM      =  78.0       # adjudication slot, 10 degrees of arc
SLOT_TO        =  88.0

def P(a, r):
    t = math.radians(a)
    return (CX + r * math.cos(t), CY - r * math.sin(t))

def T(a):
    t = math.radians(a)
    return (-math.sin(t), -math.cos(t))

def arc(a0, a1, r):
    """Cubic segments from a0 to a1 along radius r. Signed, so it runs either way."""
    total = a1 - a0
    n = max(1, int(math.ceil(abs(total) / 45.0)))
    step = total / n
    h = (4.0 / 3.0) * math.tan(math.radians(step) / 4.0)
    out, a = [], a0
    for _ in range(n):
        b = a + step
        p0, p1 = P(a, r), P(b, r)
        t0, t1 = T(a), T(b)
        c1 = (p0[0] + h * r * t0[0], p0[1] + h * r * t0[1])
        c2 = (p1[0] - h * r * t1[0], p1[1] - h * r * t1[1])
        out.append("C%s %s %s %s %s %s" % (f(c1[0]), f(c1[1]), f(c2[0]), f(c2[1]), f(p1[0]), f(p1[1])))
        a = b
    return " ".join(out)

def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")

def band(a0, a1, r_out, r_in):
    """One closed ring segment with flat radial cuts at both ends."""
    s_out, e_in = P(a0, r_out), P(a1, r_in)
    return ("M%s %s %s L%s %s %s Z"
            % (f(s_out[0]), f(s_out[1]), arc(a0, a1, r_out),
               f(e_in[0]), f(e_in[1]), arc(a1, a0, r_in)))

full = [
    {"role": "accent",   "d": band(SLOT_TO, APERTURE_START, R_OUT, R_IN)},
    {"role": "emphasis", "d": band(APERTURE_END, SLOT_FROM, R_OUT, R_IN)},
]
reduced = [
    {"role": "accent", "d": band(APERTURE_END, APERTURE_START, R_OUT, R_IN_R)},
]

def bbox(paths):
    import re
    xs, ys = [], []
    for p in paths:
        n = [float(v) for v in re.findall(r"-?\d+\.?\d*", p["d"])]
        xs += n[0::2]; ys += n[1::2]
    return min(xs), min(ys), max(xs), max(ys)

if __name__ == "__main__":
    for name, paths in (("full", full), ("reduced", reduced)):
        b = bbox(paths)
        print("%-8s bbox %.1f %.1f %.1f %.1f  (w %.1f h %.1f)  inside 1000: %s"
              % (name, b[0], b[1], b[2], b[3], b[2] - b[0], b[3] - b[1],
                 b[0] >= -0.5 and b[1] >= -0.5 and b[2] <= GRID + 0.5 and b[3] <= GRID + 0.5))
    print(json.dumps({"full": full, "reduced": reduced}, indent=2)[:400])
