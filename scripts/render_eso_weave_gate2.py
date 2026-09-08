#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble the ignored S020 Gate 2 review packet from a verified private kit."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "dist" / "eso-weave"
OUTPUT = ROOT / "dist" / "eso-weave-approval" / "gate-2"
SPEC = ROOT / "specs" / "020-eso-weave-provenance-kit"
sys.path.insert(0, str(ROOT / "skill" / "templates"))
from brand_contract import validate_source_inventory
SURFACES = [
    "showcase-card",
    "brand-landing-page",
    "guideline-topics",
    "downloads",
    "registry-endpoints",
    "public-metadata",
    "structured-data",
    "social-preview",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    validate_source_inventory(SPEC / "source-inventory.json", ROOT)
    brand = json.loads((KIT / "brand.json").read_text(encoding="utf-8"))
    if brand["approval_ledger"]["gate_1"]["status"] != "approved":
        raise SystemExit("Gate 1 is not approved")
    if brand["approval_ledger"]["gate_2"]["status"] != "pending":
        raise SystemExit("Gate 2 packet generation requires a pending publication decision")
    verification = (KIT / "VERIFY.md").read_text(encoding="utf-8")
    if "| **Problems found** | **0** |" not in verification:
        raise SystemExit("private kit verification is not clean")

    resolved = OUTPUT.resolve()
    resolved.relative_to((ROOT / "dist").resolve())
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    OUTPUT.mkdir(parents=True)
    files = {
        KIT / "qc" / "logo-sheet.png": OUTPUT / "derivative-comparison.png",
        KIT / "qc" / "pages-guidelines-index.png": OUTPUT / "rendered-guidelines.png",
        KIT / "qc" / "pages-eso-weave-desktop-index.png": OUTPUT / "rendered-ui-specimen.png",
        KIT / "qc" / "contact-sheet.png": OUTPUT / "brand-guide-contact-sheet.png",
        KIT / "guidelines" / "index.html": OUTPUT / "portable-guidelines.html",
        KIT / "brand-guide.pdf": OUTPUT / "eso-weave-brand-guide.pdf",
        KIT / "VERIFY.md": OUTPUT / "VERIFY.md",
        KIT / "manifest.json": OUTPUT / "kit-manifest.json",
        KIT / "logos" / "provenance.json": OUTPUT / "derivative-provenance.json",
        SPEC / "source-inventory.json": OUTPUT / "source-inventory.json",
        SPEC / "gate-1-proposal.json": OUTPUT / "approval-ledger.json",
    }
    for source, target in files.items():
        if not source.is_file():
            raise SystemExit("Gate 2 input is missing: %s" % source)
        shutil.copy2(source, target)

    surface_path = OUTPUT / "publication-surfaces.json"
    surface_path.write_text(json.dumps({"release_publication": False, "surfaces": SURFACES}, indent=2) + "\n", encoding="utf-8", newline="\n")
    records = []
    for path in sorted(OUTPUT.iterdir()):
        if path.name == "packet.json":
            continue
        records.append({"path": path.name, "bytes": path.stat().st_size, "sha256": digest(path)})
    packet = {
        "schema_version": 1,
        "brand": "eso-weave",
        "source_hashes": brand["approval_ledger"]["source_hashes"],
        "derivative_manifest_sha256": digest(KIT / "logos" / "provenance.json"),
        "kit_manifest_sha256": digest(KIT / "manifest.json"),
        "verification_problems": 0,
        "public_projection_enabled": False,
        "publication_surfaces": SURFACES,
        "files": records,
    }
    packet_path = OUTPUT / "packet.json"
    packet_path.write_text(json.dumps(packet, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(packet_path)
    print("Gate 2 packet contains %d review files and no public projection" % len(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
