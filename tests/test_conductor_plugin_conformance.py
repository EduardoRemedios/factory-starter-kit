import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_plugin_status import complete_i2_pack, create_run, write


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
FIXTURE = json.loads(
    (
        REPO_ROOT
        / "tests/plugin_fixtures/harness_parity/golden.json"
    ).read_text(encoding="utf-8")
)


def load_runtime(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


CODEX_RUNTIME = load_runtime(
    "conductor_codex_runtime", REPO_ROOT / "plugins/conductor/scripts/conductor_plugin.py"
)
CLAUDE_RUNTIME = load_runtime(
    "conductor_claude_runtime",
    REPO_ROOT / "plugins/conductor-claude/scripts/conductor_plugin.py",
)


class FactoryPluginConformanceTests(unittest.TestCase):
    def test_progress_semantics_match_harness_parity_fixture(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            write(run_root / "EXECUTION_MODE.txt", "PLANNING_ONLY\n")
            complete_i2_pack(run_root)
            codex = CODEX_RUNTIME.evaluate_progress(root)
            claude = CLAUDE_RUNTIME.evaluate_progress(root)
            self.assertEqual(codex, claude)
            expected = FIXTURE["expected_normalized_result"]
            self.assertEqual(expected["stage_order"], codex["completed_stages"])
            self.assertEqual(expected["final_state"], codex["state"])
            self.assertFalse((run_root / "EXECUTION_PROMPT.md").exists())

    def test_setup_semantics_differ_only_by_documented_claude_bridge(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            codex_root = base / "codex"
            claude_root = base / "claude"
            codex_root.mkdir()
            claude_root.mkdir()
            codex = CODEX_RUNTIME.evaluate_setup_plan(
                codex_root,
                mode="brownfield",
                harness="codex",
                payload_root=REPO_ROOT / "plugins/conductor/payload",
                platform_name="darwin",
                python_version=(3, 11, 0),
            )
            claude = CLAUDE_RUNTIME.evaluate_setup_plan(
                claude_root,
                mode="brownfield",
                harness="claude",
                payload_root=REPO_ROOT / "plugins/conductor-claude/payload",
                platform_name="darwin",
                python_version=(3, 11, 0),
            )
            codex_files = codex["planned_files"]
            claude_files = [
                item for item in claude["planned_files"] if item["path"] != "CLAUDE.md"
            ]
            self.assertEqual(codex_files, claude_files)
            self.assertEqual(
                ["CLAUDE.md"],
                [
                    item["path"]
                    for item in claude["planned_files"]
                    if item["path"] == "CLAUDE.md"
                ],
            )

    def test_git_root_resolution_handles_spaces_and_nested_invocation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir) / "project with spaces"
            nested = root / "src/deep"
            nested.mkdir(parents=True)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            self.assertEqual(root.resolve(), CODEX_RUNTIME.resolve_git_root(nested))
            self.assertEqual(root.resolve(), CLAUDE_RUNTIME.resolve_git_root(nested))

    def test_git_worktree_resolution_returns_worktree_root(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            main = base / "main repo"
            worktree = base / "feature worktree"
            subprocess.run(["git", "init", "-q", str(main)], check=True)
            write(main / "README.md", "fixture\n")
            env = {
                **os.environ,
                "GIT_AUTHOR_NAME": "Factory Fixture",
                "GIT_AUTHOR_EMAIL": "factory@example.invalid",
                "GIT_COMMITTER_NAME": "Factory Fixture",
                "GIT_COMMITTER_EMAIL": "factory@example.invalid",
            }
            subprocess.run(["git", "-C", str(main), "add", "README.md"], check=True)
            subprocess.run(
                ["git", "-C", str(main), "commit", "-q", "-m", "fixture"],
                check=True,
                env=env,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(main),
                    "worktree",
                    "add",
                    "-q",
                    "-b",
                    "fixture-worktree",
                    str(worktree),
                ],
                check=True,
            )
            nested = worktree / "nested"
            nested.mkdir()
            self.assertEqual(worktree.resolve(), CODEX_RUNTIME.resolve_git_root(nested))
            self.assertEqual(worktree.resolve(), CLAUDE_RUNTIME.resolve_git_root(nested))

    def test_unverified_environment_has_stable_reason_on_both_packages(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            outputs = [
                runtime.evaluate_doctor(
                    root,
                    harness=harness,
                    platform_name="linux",
                    python_version=(3, 11, 0),
                )
                for runtime, harness in (
                    (CODEX_RUNTIME, "codex"),
                    (CLAUDE_RUNTIME, "claude"),
                )
            ]
            self.assertTrue(all(item["state"] == "BLOCKED" for item in outputs))
            self.assertTrue(
                all(
                    item["reason_code"] == "CONDUCTOR_ENVIRONMENT_UNVERIFIED"
                    for item in outputs
                )
            )


if __name__ == "__main__":
    unittest.main()
