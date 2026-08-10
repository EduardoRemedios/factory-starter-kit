from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_factory_plugin_status import inventory, write


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_NAMES = ("authored", "claude", "codex")


def runtime_for(name: str, fixture_root: Path) -> Path:
    if name == "claude":
        return REPO_ROOT / "plugins/factory-claude/scripts/factory_plugin.py"
    if name == "codex":
        return REPO_ROOT / "plugins/factory/scripts/factory_plugin.py"
    package = fixture_root / "authored-package"
    runtime = package / "scripts/factory_plugin.py"
    runtime.parent.mkdir(parents=True)
    shutil.copy2(REPO_ROOT / "plugin-src/factory/runtime/factory_plugin.py", runtime)
    shutil.copytree(REPO_ROOT / "plugins/factory/payload", package / "payload")
    return runtime


def run_cli(runtime: Path, cwd: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], dict]:
    completed = subprocess.run(
        [sys.executable, str(runtime), *args],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise AssertionError(
            f"{runtime} returned invalid JSON: {completed.stdout!r}; stderr={completed.stderr!r}"
        ) from error
    return completed, payload


class FactoryPluginCliTests(unittest.TestCase):
    def test_claude_greenfield_cli_preserves_local_settings_preview(self):
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                runtime = runtime_for(runtime_name, base)
                root = base / "claude initialized project"
                write(root / ".claude/settings.local.json", '{"permissions":{}}\n')
                before = inventory(root)
                completed, payload = run_cli(
                    runtime, root, "greenfield", "--harness", "claude"
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertEqual("PLAN_READY", payload["state"])
                self.assertEqual(
                    ".claude/settings.local.json",
                    payload["bootstrap_plan"]["preserved_paths"][0]["path"],
                )
                self.assertEqual([], payload["mutations"])
                self.assertEqual(before, inventory(root))
                self.assertFalse((root / ".git").exists())

    def test_codex_harness_cli_rejects_claude_local_settings(self):
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                runtime = runtime_for(runtime_name, base)
                root = base / "codex project"
                write(root / ".claude/settings.local.json", "{}\n")
                before = inventory(root)
                completed, payload = run_cli(
                    runtime, root, "greenfield", "--harness", "codex"
                )
                self.assertEqual(2, completed.returncode, completed.stderr)
                self.assertEqual(
                    "FACTORY_GREENFIELD_NOT_EMPTY", payload["reason_code"]
                )
                self.assertEqual(
                    "choose_an_empty_target_or_remove_non_project_harness_content",
                    payload["next_legal_action"],
                )
                self.assertEqual([], payload["mutations"])
                self.assertEqual(before, inventory(root))

    def test_greenfield_defaults_to_empty_current_directory(self):
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                runtime = runtime_for(runtime_name, base)
                root = base / "empty project"
                root.mkdir()
                before = inventory(root)
                completed, payload = run_cli(
                    runtime, root, "greenfield", "--harness", "claude"
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertEqual("PLAN_READY", payload["state"])
                self.assertEqual("FACTORY_PLAN_READY", payload["reason_code"])
                self.assertEqual(str(root.resolve()), payload["repository_root"])
                self.assertEqual([], payload["mutations"])
                self.assertEqual(before, inventory(root))
                self.assertFalse((root / ".git").exists())

    def test_greenfield_explicit_absent_spaced_target_is_preview_only(self):
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                runtime = runtime_for(runtime_name, base)
                workspace = base / "workspace"
                workspace.mkdir()
                target = workspace / "absent project with spaces"
                before = inventory(workspace)
                completed, payload = run_cli(
                    runtime,
                    workspace,
                    "--root",
                    str(target),
                    "greenfield",
                    "--harness",
                    "claude",
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertEqual("PLAN_READY", payload["state"])
                self.assertEqual("FACTORY_PLAN_READY", payload["reason_code"])
                self.assertEqual(str(target.resolve()), payload["repository_root"])
                self.assertEqual([], payload["mutations"])
                self.assertEqual(before, inventory(workspace))
                self.assertFalse(target.exists())

    def test_greenfield_rejects_nonempty_current_directory(self):
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                runtime = runtime_for(runtime_name, base)
                root = base / "existing project"
                write(root / "README.md", "existing project\n")
                before = inventory(root)
                completed, payload = run_cli(
                    runtime, root, "greenfield", "--harness", "claude"
                )
                self.assertEqual(2, completed.returncode, completed.stderr)
                self.assertEqual("BLOCKED", payload["state"])
                self.assertEqual("FACTORY_GREENFIELD_NOT_EMPTY", payload["reason_code"])
                self.assertEqual(
                    "choose_an_empty_target_or_remove_non_project_harness_content",
                    payload["next_legal_action"],
                )
                self.assertEqual([], payload["mutations"])
                self.assertEqual(before, inventory(root))

    def test_doctor_outside_git_still_requires_git_root(self):
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                runtime = runtime_for(runtime_name, base)
                root = base / "empty project"
                root.mkdir()
                before = inventory(root)
                completed, payload = run_cli(
                    runtime, root, "doctor", "--harness", "claude"
                )
                self.assertEqual(2, completed.returncode, completed.stderr)
                self.assertEqual("BLOCKED", payload["state"])
                self.assertEqual("FACTORY_GIT_ROOT_REQUIRED", payload["reason_code"])
                self.assertEqual([], payload["mutations"])
                self.assertEqual(before, inventory(root))

    def test_help_describes_greenfield_root_exception(self):
        expected = "current directory for greenfield; Git root otherwise"
        for runtime_name in RUNTIME_NAMES:
            with self.subTest(runtime=runtime_name), tempfile.TemporaryDirectory() as temp_dir:
                runtime = runtime_for(runtime_name, Path(temp_dir))
                completed = subprocess.run(
                    [sys.executable, str(runtime), "--help"],
                    cwd=REPO_ROOT,
                    check=False,
                    capture_output=True,
                    text=True,
                    env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertIn(expected, " ".join(completed.stdout.split()))


if __name__ == "__main__":
    unittest.main()
