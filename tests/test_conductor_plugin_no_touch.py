from __future__ import annotations

import unittest

from tests.conductor_plugin_test_support import BASELINE_PATH, REPO_ROOT, load_json, sha256_file


CURRENT_SPRINT_ALLOWED_LEGACY_PATHS = {
    "docs/Conductor/Spec/STAGE_CONTRACTS.md",
    "scripts/conductor_stage_lint.py",
    # Lifecycle-closeout contract fix: manifest presence is now enforced for
    # execution-enabled runs whose plan declares runnable VM checks.
    "scripts/conductor_pack_lint.py",
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
