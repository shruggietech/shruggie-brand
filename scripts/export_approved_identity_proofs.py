#!/usr/bin/env python3
"""Export exact canonical-host identity and Gate 2 evidence for cross-platform CI."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "skill" / "templates"
if str(TEMPLATES) not in sys.path:
    sys.path.insert(0, str(TEMPLATES))

from brand_contract import sha256_file  # noqa: E402
from identity_continuity import (  # noqa: E402
    load_json,
    safe_path,
    validate_brand_continuity,
    validate_current_proof_matrix,
)
from process_utils import hidden_process_kwargs  # noqa: E402


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
    for face in (brand.get("typography") or {}).get("faces", []):
        relative = Path(face["path"])
        try:
            font_relative = relative.relative_to("fonts")
        except ValueError as error:
            raise ValueError("fixed font path must remain under fonts") from error
        origin = confined(ROOT / "assets" / "fonts" / font_relative, ROOT / "assets" / "fonts", "fixed font")
        target = confined(destination / relative, destination, "staged fixed font")
        if not origin.is_file():
            raise ValueError("fixed font is missing: %s" % face["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(origin), str(target))
    commands = (
        [sys.executable, str(TEMPLATES / "probe.py"), str(destination)],
        [sys.executable, str(TEMPLATES / "gen_logo.py"), str(destination / "brand.json"), str(destination)],
    )
    for command in commands:
        completed = subprocess.run(command, capture_output=True, text=True, check=False,
                                   **hidden_process_kwargs())
        if completed.returncode:
            raise RuntimeError("canonical-host export failed: %s" % ((completed.stderr or completed.stdout).strip()))
    record = load_json(safe_path(destination, brand["identity_continuity"]["record"]))
    validation = validate_current_proof_matrix(record, destination, brand=brand)
    gate_2 = ((brand.get("approval_ledger") or {}).get("gate_2") or {})
    approval = destination / "logos" / "approval.json"
    if gate_2.get("status") == "approved" and sha256_file(approval) != gate_2.get("derivative_manifest_sha256"):
        raise ValueError("canonical-host Gate 2 derivative manifest drift")
    if (destination / "fonts").exists():
        shutil.rmtree(str(destination / "fonts"))
    for generated in (destination / "icons", destination / "favicons"):
        if generated.exists():
            shutil.rmtree(str(generated))
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
