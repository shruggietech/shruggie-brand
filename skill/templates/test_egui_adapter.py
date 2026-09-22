#!/usr/bin/env python3
"""Generated Rust/egui adapter regression tests."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from component_contract import COMPONENT_IDS  # noqa: E402
from gen_egui import generate_egui, verify_egui_adapter  # noqa: E402
from process_utils import hidden_process_kwargs  # noqa: E402


class EguiAdapterTests(unittest.TestCase):
    def generate(self, root):
        kit = Path(root) / "shruggietech"
        kit.mkdir()
        shutil.copy2(ROOT / "brands" / "shruggietech" / "brand.json", kit / "brand.json")
        generate_egui(kit / "brand.json", kit)
        return kit

    def test_output_is_deterministic_complete_and_native(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            native = kit / "native" / "egui"
            first = {
                path.relative_to(native).as_posix(): path.read_bytes()
                for path in native.rglob("*") if path.is_file()
            }
            generate_egui(kit / "brand.json", kit)
            second = {
                path.relative_to(native).as_posix(): path.read_bytes()
                for path in native.rglob("*") if path.is_file()
            }
            self.assertEqual(first, second)
            manifest = json.loads((native / "adapter.json").read_text(encoding="utf-8"))
            support = json.loads((native / "support-matrix.json").read_text(encoding="utf-8"))
            self.assertEqual("1.0.1", manifest["adapter_version"])
            self.assertEqual("=0.36.1", manifest["crate"]["dependencies"]["egui"])
            self.assertEqual("=0.36.1", manifest["crate"]["dev_dependencies"]["egui_kittest"])
            self.assertEqual("1.95", manifest["crate"]["rust_version"])
            self.assertTrue((native / "Cargo.lock").is_file())
            self.assertEqual(set(COMPONENT_IDS), {item["component"] for item in support["components"]})
            self.assertEqual({"supported", "adapted", "unsupported"}, set(support["status_vocabulary"]))
            self.assertEqual({"passed", "pending"}, set(support["proof_vocabulary"]))
            self.assertTrue(all(item["proof"] == "passed" for item in support["components"]))
            source = "\n".join(
                (native / "src" / name).read_text(encoding="utf-8")
                for name in ("lib.rs", "tokens.rs", "components.rs")
            )
            self.assertIn("egui::", source)
            self.assertIn("RuntimeCapabilities", source)
            self.assertIn("Density", source)
            self.assertIn("fine_pointer_control_height", source)
            self.assertIn("requires_conservative_target", source)
            self.assertNotIn("React", source)
            self.assertNotIn("className", source)
            self.assertEqual([], verify_egui_adapter(kit))

    def test_tampered_versions_and_support_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            native = kit / "native" / "egui"
            manifest_path = native / "adapter.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["component_recipe_version"] = "9.9.9"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("component recipe" in problem for problem in verify_egui_adapter(kit)))

            generate_egui(kit / "brand.json", kit)
            support_path = native / "support-matrix.json"
            support = json.loads(support_path.read_text(encoding="utf-8"))
            support["components"].pop()
            support_path.write_text(json.dumps(support), encoding="utf-8")
            self.assertTrue(any("recipe coverage" in problem for problem in verify_egui_adapter(kit)))

            generate_egui(kit / "brand.json", kit)
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["compiler_version"] = "1.9.9"
            manifest["compatibility"]["validated_versions"]["compiler"] = "1.9.9"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertTrue(any("compiler version" in problem for problem in verify_egui_adapter(kit)))

            generate_egui(kit / "brand.json", kit)
            lockfile = native / "Cargo.lock"
            lockfile.write_text(lockfile.read_text(encoding="utf-8") + "# drift\n", encoding="utf-8")
            self.assertTrue(any("Cargo.lock" in problem for problem in verify_egui_adapter(kit)))

    @unittest.skipUnless(shutil.which("cargo"), "cargo is not installed")
    def test_generated_crate_compiles_and_runs_rendered_state_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            kit = self.generate(temporary)
            manifest = kit / "native" / "egui" / "Cargo.toml"
            result = subprocess.run(
                ["cargo", "test", "--manifest-path", str(manifest), "--locked"],
                check=False,
                capture_output=True,
                text=True,
                **hidden_process_kwargs()
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
