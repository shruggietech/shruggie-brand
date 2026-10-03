"""Exercise the approved insonic helper without changing its bound bytes."""

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / 'skill' / 'templates'
sys.path.insert(0, str(TEMPLATES))
from process_utils import hidden_process_kwargs


class InsonicConstructionTests(unittest.TestCase):
    def run_launcher(self, launcher, cwd, *arguments):
        environment = dict(os.environ)
        environment.pop('PYTHONPATH', None)
        return subprocess.run([sys.executable, str(launcher)] + list(arguments), cwd=str(cwd),
                              env=environment, capture_output=True, text=True, encoding='utf-8',
                              **hidden_process_kwargs())

    def assert_geometry(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        actual = json.loads(result.stdout)
        brand = json.loads((ROOT / 'brands/insonic/brand.json').read_text(encoding='utf-8'))
        self.assertEqual(actual, {'grid': brand['logo']['grid'], **brand['logo']['paths']})

    def test_repository_launcher_resolves_library_from_unrelated_working_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assert_geometry(self.run_launcher(ROOT / 'brands/insonic/build/run_paths.py', directory))

    def test_portable_kit_launcher_accepts_the_installed_library_explicitly(self):
        with tempfile.TemporaryDirectory() as directory:
            build = Path(directory) / 'kit' / 'build'
            build.mkdir(parents=True)
            for name in ('mk_paths.py', 'run_paths.py'):
                shutil.copyfile(ROOT / 'brands/insonic/build' / name, build / name)
            self.assert_geometry(self.run_launcher(build / 'run_paths.py', directory, '--templates', str(TEMPLATES)))

    def test_missing_explicit_library_reports_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_launcher(ROOT / 'brands/insonic/build/run_paths.py', directory,
                                       '--templates', directory)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Pass --templates', result.stderr)

    def test_canonical_helper_keeps_its_approved_bytes_and_passes_module_validation(self):
        helper = ROOT / 'brands/insonic/build/mk_paths.py'
        continuity = json.loads((ROOT / 'brands/insonic/identity-continuity.json').read_text(encoding='utf-8'))
        binding = next(item for item in continuity['source_files'] if item['path'] == 'build/mk_paths.py')
        self.assertEqual(hashlib.sha256(helper.read_bytes()).hexdigest(), binding['sha256'])
        result = self.run_launcher(TEMPLATES / 'validate_glyph.py', ROOT, str(helper), '--module')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
