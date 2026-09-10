#!/usr/bin/env python3
"""Contract tests for the non-publishing S026 Cueson identity study."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import cueson_identity_study as study


class CuesonIdentityStudyTests(unittest.TestCase):
    def test_gate_one_has_four_unique_complete_concepts_and_one_recommendation(self):
        self.assertEqual(4, len(study.CANDIDATES))
        self.assertEqual({"cueframe-r1"}, {key for key, value in study.CANDIDATES.items() if value["status"] == "recommended"})
        fingerprints = set()
        for key, candidate in study.CANDIDATES.items():
            study.validate_candidate(key, candidate)
            self.assertEqual(set(study.CRITERIA), set(candidate["criteria"]))
            self.assertTrue(candidate["rationale"])
            self.assertTrue(candidate["risks"])
            self.assertTrue(candidate["tradeoffs"])
            fingerprints.add(study.geometry_fingerprint(candidate))
        self.assertEqual(4, len(fingerprints))

    def test_product_copy_and_visual_exclusion_are_exact(self):
        self.assertEqual("Cueson", study.VERBAL_IDENTITY["name"])
        self.assertEqual("Universal captions and subtitles", study.VERBAL_IDENTITY["slogan"])
        self.assertEqual("A lossless, structured interchange layer for subtitle and caption content.", study.VERBAL_IDENTITY["description"])
        self.assertEqual(["A lossless, structured interchange layer", "for subtitle and caption content."], study.VERBAL_IDENTITY["preferred_description_lines"])
        excluded = set(study.EVIDENCE["excluded_visual_precedent"])
        self.assertEqual({"color", "typography", "layout", "composition", "formatting"}, excluded)
        self.assertIn("ocr-is-derived", study.CRITERIA)
        self.assertIn("source-remains-authoritative", study.CRITERIA)

    def test_palette_relationships_pass_and_color_vision_evidence_is_complete(self):
        observations = study.contrast_observations()
        self.assertTrue(observations)
        self.assertTrue(all(item["passes"] for item in observations))
        self.assertEqual({"protanopia", "deuteranopia", "tritanopia"}, set(study.color_vision_observations()))
        for mode, records in study.color_vision_observations().items():
            self.assertTrue(records, mode)
            self.assertTrue(all(item["passes"] for item in records), mode)

    def test_svg_output_is_passive_and_uses_no_external_references(self):
        for candidate in study.CANDIDATES.values():
            for variant in ("full", "reduced"):
                for surface in ("dark", "light", "mono-dark", "mono-light"):
                    svg = study.concept_svg(candidate, variant, surface)
                    lowered = svg.lower().replace('xmlns="http://www.w3.org/2000/svg"', "")
                    for prohibited in ("<script", "<style", "<text", "<foreignobject", "http:", "https:", "@import", "href="):
                        self.assertNotIn(prohibited, lowered)
                    self.assertIn('viewBox="0 0 512 512"', svg)

    def test_generate_writes_complete_deterministic_non_publishing_packet(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_output = study.generate(Path(first) / "gate-1")
            second_output = study.generate(Path(second) / "gate-1")
            first_manifest = json.loads((first_output / "manifest.json").read_text(encoding="utf-8"))
            second_manifest = json.loads((second_output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(first_manifest, second_manifest)
            self.assertEqual(1, first_manifest["gate"])
            self.assertEqual("pending", first_manifest["approval_status"])
            self.assertFalse(first_manifest["production_identity_created"])
            self.assertFalse(first_manifest["public_eligible"])
            self.assertEqual(list(study.SIZES), first_manifest["sizes_px"])
            self.assertEqual(list(study.SURFACES), first_manifest["surfaces"])
            self.assertEqual(4, len(first_manifest["candidates"]))
            paths = [item["path"] for item in first_manifest["files"]]
            self.assertEqual(len(paths), len(set(paths)))
            self.assertTrue(all(not Path(path).is_absolute() and ".." not in Path(path).parts for path in paths))
            required = {"overview.png", "palette.png", "proposal.json", "manifest.json", "index.html"}
            self.assertTrue(required.issubset({path.name for path in first_output.iterdir()}))
            for key in study.CANDIDATES:
                self.assertTrue((first_output / ("concept-%s.png" % key)).is_file())
                for size in study.SIZES:
                    for surface in study.SURFACES:
                        self.assertTrue((first_output / "proofs" / ("%s-full-%s-%d.png" % (key, surface, size))).is_file())
                        self.assertTrue((first_output / "proofs" / ("%s-reduced-%s-%d.png" % (key, surface, size))).is_file())
                        self.assertTrue((first_output / "proofs" / ("%s-full-mono-%s-%d.png" % (key, surface, size))).is_file())

    def test_invalid_candidate_and_palette_fail_closed(self):
        candidate = dict(study.CANDIDATES["cueframe-r1"])
        candidate["risks"] = []
        with self.assertRaises(ValueError):
            study.validate_candidate("broken", candidate)
        palette = json.loads(json.dumps(study.PALETTE))
        palette["dark"]["accent"] = palette["dark"]["surface"]
        with self.assertRaises(ValueError):
            study.validate_palette(palette)

    def test_gate_two_packet_covers_every_approved_derivative_and_stays_private(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = study.generate_gate_two(Path(temporary) / "gate-2")
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            proposal = json.loads((output / "proposal.json").read_text(encoding="utf-8"))
            self.assertEqual(2, manifest["gate"])
            self.assertEqual("cueframe-r1", manifest["approved_candidate"])
            self.assertEqual("cue-teal-r1", manifest["approved_palette"])
            self.assertEqual("pending", manifest["approval_status"])
            self.assertFalse(manifest["public_eligible"])
            self.assertEqual(
                {"mark", "mark-reduced", "horizontal", "stacked", "wordmark", "single-ink"},
                set(manifest["families"]),
            )
            self.assertEqual(
                {"web", "windows", "apple", "android", "social", "repository"},
                set(manifest["platforms"]),
            )
            self.assertEqual(
                ["Cueson", "Universal captions and subtitles",
                 "A lossless, structured interchange layer",
                 "for subtitle and caption content."],
                proposal["copy_lines"],
            )
            self.assertTrue((output / "overview.png").is_file())
            self.assertTrue((output / "lockups.png").is_file())
            self.assertTrue((output / "applications.png").is_file())
            self.assertTrue((output / "copy-compositions.png").is_file())
            self.assertTrue((output / "public-surfaces.png").is_file())
            self.assertTrue((output / "construction-continuity.png").is_file())
            continuity = json.loads((output / "construction-continuity.json").read_text(encoding="utf-8"))
            self.assertTrue(continuity["passes"])
            self.assertTrue(continuity["coordinate_contract_matches"])
            self.assertEqual(5, len(continuity["comparisons"]))
            self.assertTrue(all(record["silhouette_iou"] >= 0.90 for record in continuity["comparisons"] if record["size_px"] == 512))
            self.assertTrue(all(record["bbox_delta_max_px"] <= 1 for record in continuity["comparisons"]))
            self.assertTrue((output / "index.html").is_file())
            paths = [item["path"] for item in manifest["files"]]
            self.assertEqual(len(paths), len(set(paths)))
            self.assertTrue(all(not Path(path).is_absolute() and ".." not in Path(path).parts for path in paths))

            second = study.generate_gate_two(Path(temporary) / "gate-2-repeat")
            repeat = json.loads((second / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest, repeat)

    def test_consumer_handoff_is_hash_addressed_and_preserves_external_boundaries(self):
        output = study.generate_consumer_handoff(study.ROOT / "dist" / "cueson")
        handoff = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual("cueson", handoff["brand"])
        self.assertEqual(study.canonical_digest({key: value for key, value in handoff.items() if key != "sha256"}), handoff["sha256"])
        self.assertEqual("cueframe-r1", handoff["approval_ids"]["gate_1"]["candidate"])
        self.assertEqual(2, handoff["approval_ids"]["gate_2"]["attempt"])
        self.assertEqual(len(study.CONSUMER_ASSETS), len(handoff["generated_assets"]))
        for asset in handoff["generated_assets"]:
            self.assertEqual(study.file_digest(study.ROOT / "dist" / "cueson" / asset["source"]), asset["sha256"])
            self.assertTrue(asset["destination"])
        self.assertEqual(["LICENSE", "NOTICE", "LICENSE-BRAND.md"], handoff["licenses"]["required_files"])
        self.assertTrue(handoff["integration_issue"]["required"])
        self.assertTrue(handoff["integration_slice"]["required"])
        self.assertEqual({
            "working_tree_modified_by_s026": False,
            "remote_modified_by_s026": False,
            "integration_commit_created": False,
        }, handoff["repository_boundary"])
        self.assertFalse(any(value for key, value in handoff["domain_boundary"].items() if key.endswith("changed_by_s026")))
        kit_manifest = json.loads((study.ROOT / "dist" / "cueson" / "manifest.json").read_text(encoding="utf-8"))
        recorded = next(item for item in kit_manifest["files"] if item["path"] == "consumer-handoff.json")
        self.assertEqual(study.file_digest(output), recorded["sha256"])


if __name__ == "__main__":
    unittest.main()
