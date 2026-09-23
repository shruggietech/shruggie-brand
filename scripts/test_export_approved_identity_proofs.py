"""Regression checks for the canonical-host Gate 2 proof export."""

from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

import export_approved_identity_proofs as exporter


class ExportApprovedIdentityProofsTests(unittest.TestCase):
    def setUp(self):
        self.source = exporter.ROOT / "brands" / "i-heart-pr-tours"
        self.destination = exporter.ROOT / "dist" / "ci-approved-proofs" / "test-proof-retry"

    def test_retries_one_exact_manifest_mismatch(self):
        expected = (Path("proofs"), 32)
        mismatch = exporter.DerivativeManifestDrift("approved", "different")
        with mock.patch.object(exporter, "_export_once", side_effect=[mismatch, expected]) as run:
            with mock.patch("sys.stderr") as stderr:
                result = exporter.export_proofs(self.source, self.destination)
        self.assertEqual(result, expected)
        self.assertEqual(run.call_count, 2)
        self.assertIn("retrying once", "".join(call.args[0] for call in stderr.write.call_args_list))

    def test_fails_if_second_manifest_is_still_wrong(self):
        mismatch = exporter.DerivativeManifestDrift("approved", "different")
        with mock.patch.object(exporter, "_export_once", side_effect=mismatch) as run:
            with mock.patch("sys.stderr"):
                with self.assertRaisesRegex(exporter.DerivativeManifestDrift, "approved.*different"):
                    exporter.export_proofs(self.source, self.destination)
        self.assertEqual(run.call_count, 2)

    def test_other_export_failure_is_not_retried(self):
        with mock.patch.object(exporter, "_export_once", side_effect=RuntimeError("generator failed")) as run:
            with self.assertRaisesRegex(RuntimeError, "generator failed"):
                exporter.export_proofs(self.source, self.destination)
        run.assert_called_once()

    def test_destination_outside_generated_proof_root_is_rejected(self):
        with mock.patch.object(exporter, "_export_once") as run:
            with self.assertRaisesRegex(ValueError, "proof destination must stay inside"):
                exporter.export_proofs(self.source, exporter.ROOT / "outside-proofs")
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
