import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts/verify_factory_bmad_cli_rollout.py"


class FactoryBmadCliRolloutTests(unittest.TestCase):
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

    def test_repo_preflight_accepts_current_marketplace_surface_offline(self):
        code, payload = self.run_preflight()
        self.assertEqual(0, code, payload)
        checks = {item["id"]: item for item in payload["checks"]}
        self.assertEqual("WARN", payload["state"])
        self.assertEqual("PASS", checks["marketplace_manifest"]["status"])
        self.assertEqual("PASS", checks["package_versions"]["status"])
        self.assertEqual("PASS", checks["bmad_pin"]["status"])
        self.assertEqual("PASS", checks["hook_command"]["status"])
        self.assertEqual("PASS", checks["claude_cache_factory"]["status"])
        self.assertEqual("PASS", checks["claude_cache_factory-bmad"]["status"])
        self.assertEqual("WARN", checks["external_binaries"]["status"])

    def test_invalid_companion_dependency_blocks_rollout(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / ".claude-plugin").mkdir()
            (root / "plugins/factory-claude/.claude-plugin").mkdir(parents=True)
            (root / "plugins/factory-bmad-claude/.claude-plugin").mkdir(parents=True)
            (root / "plugins/factory-bmad-claude/hooks").mkdir(parents=True)
            (root / "plugin-src/factory-bmad").mkdir(parents=True)
            (root / ".claude-plugin/marketplace.json").write_text(
                json.dumps({"plugins": [{"name": "factory"}, {"name": "factory-bmad"}]}),
                encoding="utf-8",
            )
            (root / "plugins/factory-claude/.claude-plugin/plugin.json").write_text(
                json.dumps({"version": "0.2.4"}),
                encoding="utf-8",
            )
            (root / "plugins/factory-bmad-claude/.claude-plugin/plugin.json").write_text(
                json.dumps({"version": "0.2.4", "dependencies": [{"name": "factory", "version": "~0.2.3"}]}),
                encoding="utf-8",
            )
            (root / "plugin-src/factory-bmad/manifest.json").write_text(
                json.dumps({"version": "0.2.4", "bmad_version": "6.10.0"}),
                encoding="utf-8",
            )
            (root / "plugins/factory-bmad-claude/hooks/hooks.json").write_text(
                json.dumps(
                    {
                        "hooks": {
                            "UserPromptExpansion": [{"hooks": [{"command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py\" hook"}]}],
                            "PreToolUse": [{"hooks": [{"command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py\" hook"}]}],
                        }
                    }
                ),
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

    def test_matching_candidate_version_with_stale_cache_blocks_rollout(self):
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            root = base / "candidate"
            cache = base / "cache"
            source = root / "plugins/factory-claude"
            cached = cache / "factory-starter-kit/factory/0.2.4"
            (root / ".claude-plugin").mkdir(parents=True)
            (root / "plugins/factory-bmad-claude/.claude-plugin").mkdir(parents=True)
            (root / "plugins/factory-bmad-claude/hooks").mkdir(parents=True)
            (root / "plugin-src/factory-bmad").mkdir(parents=True)
            (source / ".claude-plugin").mkdir(parents=True)
            cached.mkdir(parents=True)
            (root / ".claude-plugin/marketplace.json").write_text(
                json.dumps({"plugins": [{"name": "factory"}, {"name": "factory-bmad"}]}),
                encoding="utf-8",
            )
            (source / ".claude-plugin/plugin.json").write_text(
                json.dumps({"version": "0.2.4"}),
                encoding="utf-8",
            )
            (source / "sentinel.txt").write_text("current\n", encoding="utf-8")
            (cached / ".claude-plugin").mkdir()
            (cached / ".claude-plugin/plugin.json").write_text(
                json.dumps({"version": "0.2.4"}),
                encoding="utf-8",
            )
            (cached / "sentinel.txt").write_text("stale\n", encoding="utf-8")
            (root / "plugins/factory-bmad-claude/.claude-plugin/plugin.json").write_text(
                json.dumps({"version": "0.2.4", "dependencies": [{"name": "factory", "version": "~0.2.4"}]}),
                encoding="utf-8",
            )
            (root / "plugin-src/factory-bmad/manifest.json").write_text(
                json.dumps({"version": "0.2.4", "bmad_version": "6.10.0"}),
                encoding="utf-8",
            )
            (root / "plugins/factory-bmad-claude/hooks/hooks.json").write_text(
                json.dumps(
                    {
                        "hooks": {
                            "UserPromptExpansion": [{"hooks": [{"command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py\" hook"}]}],
                            "PreToolUse": [{"hooks": [{"command": "python3 \"${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py\" hook"}]}],
                        }
                    }
                ),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--marketplace-root",
                    str(root),
                    "--claude-cache-root",
                    str(cache),
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
        self.assertEqual("BLOCKED", checks["claude_cache_factory"]["status"])
        self.assertIn("differs from marketplace source", checks["claude_cache_factory"]["detail"])


if __name__ == "__main__":
    unittest.main()
