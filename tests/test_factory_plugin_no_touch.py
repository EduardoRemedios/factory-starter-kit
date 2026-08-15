from __future__ import annotations

import unittest

from tests.factory_plugin_test_support import BASELINE_PATH, REPO_ROOT, load_json, sha256_file


CURRENT_SPRINT_ALLOWED_LEGACY_PATHS = {
    "docs/Factory/Spec/STAGE_CONTRACTS.md",
    "scripts/factory_stage_lint.py",
}


class FactoryPluginProtectedPathTests(unittest.TestCase):
    def test_protected_paths_match_execution_baseline(self) -> None:
        baseline = load_json(BASELINE_PATH)
        for relative_path, expected_digest in baseline["files"].items():
            if relative_path in CURRENT_SPRINT_ALLOWED_LEGACY_PATHS:
                continue
            path = REPO_ROOT / relative_path
            self.assertTrue(path.is_file(), relative_path)
            self.assertEqual(sha256_file(path), expected_digest, relative_path)


if __name__ == "__main__":
    unittest.main()
