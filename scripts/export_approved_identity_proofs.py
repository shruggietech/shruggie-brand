#!/usr/bin/env python3
"""Export an exact, validated canonical-host proof matrix for cross-platform CI."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "skill" / "templates"
if str(TEMPLATES) not in sys.path:
    sys.path.insert(0, str(TEMPLATES))

from identity_continuity import (  # noqa: E402
    generate_current_proofs,
    load_json,
    safe_path,
    validate_brand_continuity,
    validate_current_proof_matrix,
)


def confined(path, root, label):
    resolved = Path(path).resolve()
    try:
        resolved.relative_to(Path(root).resolve())
    except ValueError as error:
        raise ValueError("%s must stay inside %s" % (label, root)) from error
    return resolved


def export_proofs(source, destination):
    source = confined(source, ROOT / "brands", "brand source")
    destination = confined(destination, ROOT / "dist" / "ci-approved-proofs", "proof destination")
    if destination.exists():
        shutil.rmtree(str(destination))
    shutil.copytree(str(source), str(destination))
    (destination / "qc").mkdir()
    brand = load_json(destination / "brand.json")
    result = validate_brand_continuity(brand, destination)
    if result["status"] != "approved-canonical":
        raise ValueError("canonical-host proof export requires an approved-canonical brand")
    record = load_json(safe_path(destination, brand["identity_continuity"]["record"]))
    generate_current_proofs(brand, destination)
    validation = validate_current_proof_matrix(record, destination, brand=brand)
    return destination / "qc" / "identity-continuity-proofs", len(validation["proofs"])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()
    proof_dir, count = export_proofs(args.source, args.destination)
    print("exported %d exact approved proofs to %s" % (count, proof_dir))


if __name__ == "__main__":
    main()
