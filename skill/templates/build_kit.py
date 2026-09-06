#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_kit.py: run the whole pipeline in order, then refuse to call it done.

    python3 build/build_kit.py <kit-dir>

Order matters. Tokens come first because everything downstream reads them; the
manifest comes last because it checksums everything else; QC comes after that
because it inspects the finished artifacts.

The final step is a message rather than a check: open the contact sheets. Every
automated gate in this kit can pass on a document that looks wrong.
"""
import json, os, subprocess, sys

from brand_contract import affiliation
from process_utils import hidden_process_kwargs

# Contract validation runs before any publishable output. The capability probe
# then routes later work, and the glyph gate stops broken constructed marks
# before export. See references/09-portability.md.
PRE = [
    ("validate explicit brand contract",            ["validate_brand.py", "{brand}"]),
    ("probe the toolchain",                     ["probe.py", "{kit}"]),
    ("glyph geometry gate",                     ["validate_glyph.py", "{brand}"]),
]
STEPS = [
    ("authoritative input evidence",            ["analyze_inputs.py", "{brand}", "{kit}"]),
    ("enrich brand.json with measured values", ["enrich_brand.py", "{brand}"]),
    ("outlined type specimen",                      ["build_specimen.py", "{brand}"]),
    ("vanilla tokens, styles.css, components",     ["gen_vanilla.py", "{brand}", "{kit}"]),
    ("tokens, shadcn registry, fonts, provider", ["gen_nextjs.py", "{brand}", "{kit}"]),
    ("agent contract and lint configs",         ["gen_enforcement.py", "{brand}", "{kit}"]),
    ("logo colourways, lockups, categorized application icons", ["gen_logo.py", "{brand}", "{kit}"]),
    ("guidelines page",                         ["gen_guidelines.py", "{brand}", "{kit}"]),
    ("brand guide PDF",                         ["gen_guide_pdf.py", "{brand}", "{kit}"]),
]
POST = [
    ("verify",   ["verify.py", "{kit}", "--out", "{kit}/VERIFY.md"]),
    ("affiliation output scan", ["scan_affiliation.py", "{brand}", "{kit}"]),
    ("image QC", ["qc_images.py", "{kit}"]),
]

def run(script, args, here):
    r = subprocess.run([sys.executable, os.path.join(here, script)] + args,
                       capture_output=True, text=True, **hidden_process_kwargs())
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def manifest(kit, complete=False):
    import hashlib
    files = []
    for dp, dn, fn in os.walk(kit):
        excluded = {"node_modules", "concepts", ".git", "__pycache__"}
        if not complete:
            excluded.add("qc")
        dn[:] = sorted(d for d in dn if d not in excluded)
        for f in sorted(fn):
            p = os.path.join(dp, f)
            relative = os.path.relpath(p, kit).replace(os.sep, "/")
            omitted = {"manifest.json"} if complete else {"manifest.json", "VERIFY.md"}
            if relative in omitted: continue
            with open(p, "rb") as source:
                b = source.read()
            files.append({"path": relative,
                          "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    bj = os.path.join(kit, "brand.json")
    if os.path.exists(bj):
        with open(bj, encoding="utf-8") as source:
            B = json.load(source)
    else:
        B = {}
    aff = affiliation(B) if B else {}
    with open(os.path.join(kit, "manifest.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"name": "%s-brand-kit" % B.get("slug", "brand"),
                   "version": B.get("version", "1.0.0"),
                   "parent": aff.get("parent"), "affiliation": aff,
                   "canon": B.get("canon", "1.0.0"),
                   "files": files}, f, indent=2)
        f.write("\n")
    return len(files)

def main():
    kit = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
    here = os.path.dirname(os.path.abspath(__file__))
    brand = os.path.join(kit, "brand.json")
    if not os.path.exists(brand):
        sys.exit("no brand.json in %s. Run the interview first; see references/03-interview.md." % kit)
    fail = 0
    for label, argv in PRE:
        script = argv[0]; args = [a.format(brand=brand, kit=kit) for a in argv[1:]]
        if not os.path.exists(os.path.join(here, script)):
            print("SKIP  %-42s (%s absent)" % (label, script)); continue
        rc, out = run(script, args, here)
        last = out.strip().splitlines()[-1] if out.strip() else ""
        print("%-5s %-42s %s" % ("ok" if rc == 0 else "FAIL", label, last[:70]))
        if rc:
            fail += rc
            print(out)
            if script in {"validate_brand.py", "validate_glyph.py"}:
                if script == "validate_brand.py":
                    print("\nThe brand contract is invalid. Correct brand.json or its declared local inputs before generating anything.")
                    return min(fail, 125)
                print("\nThe mark is wrong. Fix build/mk_paths.py and regenerate "
                      "logo.paths before building anything else.")
                return min(fail, 125)
    for label, argv in STEPS:
        script = argv[0]; args = [a.format(brand=brand, kit=kit) for a in argv[1:]]
        if not os.path.exists(os.path.join(here, script)):
            print("SKIP  %-42s (%s absent)" % (label, script)); continue
        rc, out = run(script, args, here)
        last = out.strip().splitlines()[-1] if out.strip() else ""
        print("%-5s %-42s %s" % ("ok" if rc == 0 else "FAIL", label, last[:70]))
        if rc: fail += 1; print(out)
    print("%-5s %-42s %d files" % ("ok", "verification manifest", manifest(kit)))
    for label, argv in POST:
        script = argv[0]; args = [a.format(brand=brand, kit=kit) for a in argv[1:]]
        if not os.path.exists(os.path.join(here, script)): continue
        rc, out = run(script, args, here)
        print("%-5s %-42s %s" % ("ok" if rc == 0 else "FAIL", label,
                                 "0 problems" if rc == 0 else "%d problems" % rc))
        if rc or script == "qc_images.py":
            print(out)
        fail += rc
    pdf = os.path.join(kit, "brand-guide.pdf")
    if os.path.exists(pdf):
        rc, out = run("qc_render.py", [pdf, "--out", os.path.join(kit, "qc"),
                                       "--expect-ground", "dark"], here)
        print("%-5s %-42s %s" % ("ok" if rc == 0 else "FAIL", "PDF QC",
                                 "0 problems" if rc == 0 else "%d problems" % rc))
        if rc:
            print(out)
        fail += rc
    ph = os.path.join(kit, "build", "brand-guide.print.html")
    if os.path.exists(ph):
        rc, out = run("qc_paginate.py", [ph], here)
        print("%-5s %-42s %s" % ("ok" if rc == 0 else "FAIL", "pagination",
                                 "0 split elements" if rc == 0 else "%d split" % rc))
        if rc:
            print(out)
        fail += rc
    print("%-5s %-42s %d files" % ("ok", "final release manifest",
                                          manifest(kit, complete=True)))
    print("\n%s" % ("BUILD CLEAN" if not fail else "BUILD HAS %d PROBLEMS" % fail))
    try:
        display_kit = os.path.relpath(kit)
    except ValueError:
        display_kit = kit
    print("Not finished. Open every sheet in %s and look at it. The gates above "
          "measure correctness; none can tell you it looks right."
          % os.path.join(display_kit, "qc"))
    return min(fail, 125)

if __name__ == "__main__":
    sys.exit(main())
