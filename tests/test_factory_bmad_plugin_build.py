import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "plugin-src/factory-bmad"
PACKAGES = {"codex": REPO_ROOT / "plugins/factory-bmad", "claude": REPO_ROOT / "plugins/factory-bmad-claude"}


class FactoryBmadPluginBuildTests(unittest.TestCase):
    def test_packages_are_current(self):
        completed = subprocess.run([sys.executable, "scripts/build_factory_bmad_plugins.py", "--check"], cwd=REPO_ROOT, text=True, capture_output=True)
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_manifest_and_skill_contract(self):
        source = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
        expected = {"doctor", "bootstrap", "audit", "promote", "intake"}
        self.assertEqual(expected, {item["id"] for item in source["skills"]})
        codex = json.loads((PACKAGES["codex"] / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        claude = json.loads((PACKAGES["claude"] / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("factory-bmad", codex["name"])
        self.assertEqual([{"name": "factory", "version": "~0.2.4"}], claude["dependencies"])
        self.assertEqual("0.2.4", claude["version"])
        self.assertEqual({f"factory-bmad-{name}" for name in expected}, {path.name for path in (PACKAGES["codex"] / "skills").iterdir()})
        self.assertEqual(expected, {path.name for path in (PACKAGES["claude"] / "skills").iterdir()})

    def test_claude_package_has_both_hook_paths_without_manifest_hook_field(self):
        package = PACKAGES["claude"]
        plugin = json.loads((package / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertNotIn("hooks", plugin)
        hooks = json.loads((package / "hooks/hooks.json").read_text(encoding="utf-8"))["hooks"]
        self.assertEqual("", hooks["UserPromptExpansion"][0]["matcher"])
        self.assertEqual("Skill", hooks["PreToolUse"][0]["matcher"])
        for event in ("UserPromptExpansion", "PreToolUse"):
            command = hooks[event][0]["hooks"][0]["command"]
            self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py", command)
            self.assertTrue(command.endswith(" hook"))
        self.assertFalse((PACKAGES["codex"] / "hooks").exists())

    def test_no_factory_core_or_bmad_runtime_is_vendored(self):
        for package in PACKAGES.values():
            self.assertFalse((package / "payload").exists())
            self.assertFalse((package / "_bmad").exists())
            self.assertFalse((package / "docs/Factory").exists())
            self.assertNotIn("[TODO:", "\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in package.rglob("*") if path.is_file()))

    def test_generic_factory_payload_excludes_companion_scripts(self):
        prohibited = {
            "build_factory_bmad_plugins.py",
            "verify_factory_bmad_claude_composition.sh",
            "verify_factory_bmad_live_pilot.sh",
            "verify_factory_bmad_release.sh",
        }
        for package in (REPO_ROOT / "plugins/factory", REPO_ROOT / "plugins/factory-claude"):
            scripts = package / "payload/scripts"
            self.assertTrue(prohibited.isdisjoint({path.name for path in scripts.iterdir()}))

    def test_marketplaces_expose_separate_companion(self):
        agents = json.loads((REPO_ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
        claude = json.loads((REPO_ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        self.assertEqual({"factory", "factory-bmad"}, {item["name"] for item in agents["plugins"]})
        self.assertEqual({"factory", "factory-bmad"}, {item["name"] for item in claude["plugins"]})


if __name__ == "__main__":
    unittest.main()
