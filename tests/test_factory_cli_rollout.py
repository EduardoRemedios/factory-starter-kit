import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts/verify_factory_cli_rollout.py"


class FactoryCliRolloutTests(unittest.TestCase):
    def run_preflight(self, *args: str) -> tuple[int, dict]:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--marketplace-root",
                str(REPO_ROOT),
                "--skip-external",
                "--json",
                *args,
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        return completed.returncode, json.loads(completed.stdout)

    def test_repo_preflight_accepts_current_factory_marketplace_offline(self):
        code, payload = self.run_preflight()
        self.assertEqual(0, code, payload)
        checks = {item["id"]: item for item in payload["checks"]}
        self.assertEqual("WARN", payload["state"])
        self.assertEqual("PASS", checks["marketplace_manifest"]["status"])
        self.assertEqual("PASS", checks["package_versions"]["status"])
        self.assertEqual("WARN", checks["external_binaries"]["status"])

    def test_mismatched_package_version_blocks_rollout(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".claude-plugin").mkdir()
            (root / "plugins/factory-claude/.claude-plugin").mkdir(parents=True)
            (root / "plugin-src/factory/runtime").mkdir(parents=True)
            (root / ".claude-plugin/marketplace.json").write_text(
                json.dumps({"plugins": [{"name": "factory"}]}),
                encoding="utf-8",
            )
            (root / "plugin-src/factory/manifest.json").write_text(
                json.dumps({"version": "0.2.0"}),
                encoding="utf-8",
            )
            (root / "plugin-src/factory/runtime/factory_plugin.py").write_text(
                'PLUGIN_VERSION = "0.2.0"\n',
                encoding="utf-8",
            )
            (root / "plugins/factory-claude/.claude-plugin/plugin.json").write_text(
                json.dumps({"version": "0.1.0"}),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--marketplace-root",
                    str(root),
                    "--skip-external",
                    "--json",
                ],
                cwd=REPO_ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
        payload = json.loads(completed.stdout)
        checks = {item["id"]: item for item in payload["checks"]}
        self.assertEqual(1, completed.returncode)
        self.assertEqual("BLOCKED", payload["state"])
        self.assertEqual("BLOCKED", checks["package_versions"]["status"])


if __name__ == "__main__":
    unittest.main()
