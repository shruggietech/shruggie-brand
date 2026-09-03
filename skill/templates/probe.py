#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
probe.py: find out what this machine can actually do, then say so.

    python3 templates/probe.py [<kit-dir>]

Prints a capability block and, when given a kit directory, writes
`<kit>/qc/probe.json` so the generators and VERIFY.md can route off measured
facts rather than assumptions.

The tiers are defined in references/09-portability.md:

    core    Python 3.8 and the standard library. Tokens, bindings, enforcement,
            guidelines, specimen, manifest, verify, and the whole glyph gate.
    raster  core plus an SVG rasteriser and an ICO writer. PNGs and favicons.
    full    raster plus headless Chromium. The brand guide PDF and QC sheets.

Core must always pass. If it does not, stop and say why; do not build half a kit
and describe it as complete.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile

from process_utils import hidden_process_kwargs

NODE = os.environ.get("GP_NODE") or shutil.which("node")
RESVG = os.environ.get("GP_RESVG_RENDERER") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "rsvg-convert.js"
)

CLI = [
    ("rsvg-convert", "SVG to PNG, first choice"),
    ("resvg", "SVG to PNG, second choice"),
    ("inkscape", "SVG to PNG and text-to-path, third choice"),
    ("magick", "multi-entry ICO (ImageMagick 7)"),
    ("convert", "multi-entry ICO (ImageMagick 6)"),
    ("oxipng", "PNG optimisation, optional"),
    ("pdftoppm", "PDF rasterisation for visual QC"),
    ("pdffonts", "PDF font embedding check"),
    ("node", "Node, for the bundled resvg fallback"),
    ("npx", "Node package runner"),
]

PY = [
    ("coloraide", "colour maths and contrast. The only hard dependency beyond stdlib."),
    ("fontTools", "wordmark and specimen outlining"),
    ("PIL", "raster compositing, contact sheets, ICO fallback"),
    ("playwright", "headless Chromium for the PDF and page screenshots"),
    ("pikepdf", "PDF verification"),
]


def which(name):
    return shutil.which(name)


def version(name):
    try:
        r = subprocess.run([name, "--version"], capture_output=True, text=True, timeout=8,
                           **hidden_process_kwargs())
        line = ((r.stdout or "") + (r.stderr or "")).strip().splitlines()
        return line[0][:60] if line else "present"
    except Exception:
        return "present"


def chromium_ok():
    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return False, "playwright not importable"
    try:
        p = sync_playwright().start()
        try:
            b = p.chromium.launch()
            b.close()
            return True, "chromium launches"
        finally:
            p.stop()
    except Exception as e:
        return False, str(e).strip().splitlines()[0][:70]


def node_resvg_ok():
    """Exercise the bundled fallback; file existence alone does not prove its module loads."""
    if not NODE or not os.path.isfile(RESVG):
        return False
    try:
        with tempfile.TemporaryDirectory() as directory:
            source = os.path.join(directory, "probe.svg")
            output = os.path.join(directory, "probe.png")
            with open(source, "w", encoding="utf-8", newline="\n") as handle:
                handle.write('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><rect width="1" height="1"/></svg>\n')
            result = subprocess.run(
                [NODE, RESVG, "-w", "1", source, "-o", output],
                cwd=os.path.dirname(os.path.abspath(RESVG)),
                capture_output=True,
                text=True,
                timeout=8,
                **hidden_process_kwargs()
            )
            return result.returncode == 0 and os.path.isfile(output)
    except Exception:
        return False


def main():
    kit = sys.argv[1] if len(sys.argv) > 1 else None
    found_cli, found_py = {}, {}

    print("python       %d.%d.%d  %s" % (sys.version_info[0], sys.version_info[1],
                                         sys.version_info[2], sys.executable))
    if sys.version_info < (3, 8):
        print("FAIL         this skill targets Python 3.8 or newer")
        return 2

    for name, why in CLI:
        p = which(name)
        found_cli[name] = bool(p)
        print("%-12s %s" % (name, version(name) if p else "MISSING     (%s)" % why))

    for mod, why in PY:
        try:
            __import__(mod)
            found_py[mod] = True
            print("%-12s present" % mod)
        except Exception:
            found_py[mod] = False
            print("%-12s MISSING     (%s)" % (mod, why))

    chrome, chrome_note = chromium_ok() if found_py.get("playwright") else (False, "playwright missing")
    print("%-12s %s" % ("chromium", chrome_note))

    node_resvg = node_resvg_ok()
    raster = (found_cli["rsvg-convert"] or found_cli["resvg"] or found_cli["inkscape"]
              or node_resvg)
    ico = found_cli["magick"] or found_cli["convert"] or found_py.get("PIL")
    tier = "full" if (raster and chrome) else ("raster" if raster else "core")

    caps = {
        "tier": tier,
        "python": "%d.%d.%d" % sys.version_info[:3],
        "cli": found_cli,
        "modules": found_py,
        "chromium": chrome,
        "svg_raster": raster,
        "node_resvg": node_resvg,
        "ico_writer": ico,
    }

    print("")
    print("tier         %s" % tier)
    if not found_py.get("coloraide"):
        print("BLOCKED      coloraide is missing. Contrast numbers are measured, never")
        print("             typed, so no colour work can proceed. Try:")
        print("               %s -m pip install --user coloraide" % os.path.basename(sys.executable))
    if tier == "core":
        print("NOTE         no SVG rasteriser. Vector masters, tokens, bindings, the")
        print("             guidelines page and the glyph gate all still run. PNGs,")
        print("             favicons and the ICO will be recorded as skips.")
    if tier != "full":
        print("NOTE         no headless Chromium. The brand guide PDF and the QC contact")
        print("             sheets will be recorded as skips with this reason.")
    if not (found_cli["magick"] or found_cli["convert"]) and found_py.get("PIL"):
        print("NOTE         no ImageMagick. The ICO falls back to Pillow, assembled from")
        print("             the per-size PNGs so the reduced master is still used below 32.")

    if kit:
        d = os.path.join(kit, "qc")
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "probe.json"), "w", encoding="utf-8", newline="\n") as f:
            json.dump(caps, f, indent=2)
            f.write("\n")
        print("")
        print("wrote        %s" % os.path.join(d, "probe.json"))

    return 0 if found_py.get("coloraide") else 1


if __name__ == "__main__":
    sys.exit(main())
