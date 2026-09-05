import hashlib
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_plugin_status import inventory, write


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_PATH = REPO_ROOT / "plugin-src/conductor/runtime/conductor_plugin.py"
PAYLOAD_ROOT = REPO_ROOT / "plugins/conductor/payload"
SPEC = importlib.util.spec_from_file_location("conductor_plugin_setup_runtime", RUNTIME_PATH)
RUNTIME = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(RUNTIME)


def preview(root: Path, mode: str, harness: str = "codex"):
    return RUNTIME.evaluate_setup_plan(
        root,
        mode=mode,
        harness=harness,
        payload_root=PAYLOAD_ROOT,
        platform_name="darwin",
        python_version=(3, 11, 0),
    )


class FactoryPluginSetupPlanTests(unittest.TestCase):
    def test_claude_greenfield_preserves_exact_local_settings_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            settings = root / ".claude/settings.local.json"
            write(settings, '{"permissions":{"allow":[]}}\n')
            settings.chmod(0o640)
            settings.parent.chmod(0o750)
            before = inventory(root)
            output = preview(root, "greenfield", harness="claude")
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual([], output["mutations"])
            self.assertFalse((root / ".git").exists())
            self.assertEqual(before, inventory(root))
            preserved = output["bootstrap_plan"]["preserved_paths"]
            self.assertEqual(1, len(preserved))
            self.assertEqual(".claude/settings.local.json", preserved[0]["path"])
            self.assertEqual(hashlib.sha256(settings.read_bytes()).hexdigest(), preserved[0]["sha256"])
            self.assertEqual(0o640, preserved[0]["mode"])
            self.assertEqual(0o750, preserved[0]["directory_mode"])
            self.assertEqual(["settings.local.json"], preserved[0]["directory_entries"])
            self.assertNotIn(
                ".claude/settings.local.json",
                {item["path"] for item in output["planned_files"]},
            )
            self.assertNotIn(".claude/settings.local.json", output["allowed_paths"])

    def test_claude_hook_state_does_not_make_greenfield_nonempty(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / ".claude/hooks/.state/hook-errors.log", "harness\n")
            before = inventory(root)
            output = preview(root, "greenfield", harness="claude")
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual([], output["bootstrap_plan"]["preserved_paths"])
            self.assertEqual(before, inventory(root))

    def test_codex_rejects_claude_local_settings_shape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / ".claude/settings.local.json", "{}\n")
            before = inventory(root)
            output = preview(root, "greenfield", harness="codex")
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_GREENFIELD_NOT_EMPTY", output["reason_code"])
            self.assertEqual(
                "choose_an_empty_target_or_remove_non_project_harness_content",
                output["next_legal_action"],
            )
            self.assertEqual(before, inventory(root))

    def test_claude_greenfield_rejects_expanded_or_unsafe_local_state(self):
        cases = (
            "empty_claude_directory",
            "extra_claude_file",
            "extra_top_level_file",
            "claude_directory_symlink",
            "settings_symlink",
            "settings_directory",
        )
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                root = base / "repo"
                root.mkdir()
                claude = root / ".claude"
                claude.mkdir()
                if case not in {"empty_claude_directory", "claude_directory_symlink"}:
                    write(claude / "settings.local.json", "{}\n")
                if case == "extra_claude_file":
                    write(claude / "commands.md", "project command\n")
                elif case == "extra_top_level_file":
                    write(root / "README.md", "project\n")
                elif case == "claude_directory_symlink":
                    claude.rmdir()
                    outside = base / "outside"
                    outside.mkdir()
                    claude.symlink_to(outside, target_is_directory=True)
                elif case == "settings_symlink":
                    (claude / "settings.local.json").unlink()
                    outside = base / "settings.json"
                    write(outside, "{}\n")
                    (claude / "settings.local.json").symlink_to(outside)
                elif case == "settings_directory":
                    (claude / "settings.local.json").unlink()
                    (claude / "settings.local.json").mkdir()
                before = inventory(base)
                output = preview(root, "greenfield", harness="claude")
                self.assertEqual("BLOCKED", output["state"])
                expected_reason = (
                    "CONDUCTOR_UNSAFE_PATH"
                    if case
                    in {
                        "claude_directory_symlink",
                        "settings_symlink",
                        "settings_directory",
                    }
                    else "CONDUCTOR_GREENFIELD_NOT_EMPTY"
                )
                self.assertEqual(expected_reason, output["reason_code"])
                self.assertEqual([], output["mutations"])
                self.assertEqual(before, inventory(base))
                self.assertFalse((root / ".git").exists())

    def test_greenfield_existing_git_content_recommends_brownfield(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            write(root / "README.md", "existing project\n")
            before = inventory(root)
            output = preview(root, "greenfield", harness="claude")
            self.assertEqual("CONDUCTOR_GREENFIELD_NOT_EMPTY", output["reason_code"])
            self.assertEqual("use_brownfield_preview", output["next_legal_action"])
            self.assertEqual(before, inventory(root))

    def test_greenfield_plan_contains_required_factory_paths_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            before = inventory(root)
            output = preview(root, "greenfield")
            actions = {
                item["path"]: item["action"] for item in output["planned_files"]
            }
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual("CONDUCTOR_PLAN_READY", output["reason_code"])
            self.assertEqual("create", actions["AGENTS.md"])
            self.assertEqual("create", actions["docs/Conductor/ARCHITECTURE.md"])
            self.assertEqual("create", actions["scripts/conductorctl"])
            change_plan = output["change_plan"]
            self.assertEqual(output["plan_id"], change_plan["transaction_id"])
            self.assertEqual("greenfield", change_plan["operation"])
            self.assertIsNone(change_plan["source_version"])
            self.assertEqual("0.3.4", change_plan["target_version"])
            self.assertEqual("REVIEW_REQUIRED", change_plan["approval_state"])
            self.assertEqual(
                ["root", "git"],
                [
                    step["kind"]
                    for step in change_plan["ordered_transaction_steps"][:2]
                ],
            )
            self.assertEqual(
                ["no_change", "create"],
                [
                    step["action"]
                    for step in change_plan["ordered_transaction_steps"][:2]
                ],
            )
            self.assertEqual(
                "validation",
                change_plan["ordered_transaction_steps"][-1]["kind"],
            )
            self.assertTrue(
                any(
                    step["kind"] == "payload"
                    for step in change_plan["ordered_transaction_steps"]
                )
            )
            self.assertTrue(
                any(
                    step["kind"] == "metadata"
                    for step in change_plan["ordered_transaction_steps"]
                )
            )
            self.assertEqual(
                {item["path"] for item in change_plan["ordered_file_actions"]},
                set(change_plan["pre_digests"]),
            )
            self.assertEqual([], output["mutations"])
            self.assertEqual(before, inventory(root))

    def test_absent_greenfield_root_preview_is_read_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root = base / "new-project"
            before = inventory(base)
            output = preview(root, "greenfield")
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual(
                ["create", "create"],
                [step["action"] for step in output["bootstrap_plan"]["steps"]],
            )
            self.assertEqual(before, inventory(base))
            self.assertFalse(root.exists())

    def test_brownfield_preserves_unrelated_project_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative in ("README.md", "src/app.py", "tests/test_app.py", "package.json"):
                write(root / relative, "project-owned\n")
            before = inventory(root)
            output = preview(root, "brownfield")
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual([], output["conflicts"])
            self.assertEqual(before, inventory(root))

    def test_brownfield_preview_summary_counts_planned_files_not_mutations(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative in ("README.md", "src/app.py", "tests/test_app.py"):
                write(root / relative, "project-owned\n")
            output = preview(root, "brownfield")
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual([], output["mutations"])
            expected = sum(
                1
                for step in output["change_plan"]["ordered_transaction_steps"]
                if step["action"] in {"create", "modify", "delete"}
            )
            self.assertGreater(expected, 0)
            summary = RUNTIME.concise(output)
            self.assertIn(f"Changes: {expected} planned", summary)
            self.assertNotIn("Changes: 0", summary)

    def test_brownfield_conflict_halts_before_any_write(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "AGENTS.md", "project-specific instructions\n")
            write(root / "docs/Conductor/ORCHESTRATION.md", "different factory\n")
            before = inventory(root)
            output = preview(root, "brownfield")
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_CONFLICT_USER_OWNED", output["reason_code"])
            # An existing project AGENTS.md is composed (managed block inserted), never a conflict.
            self.assertNotIn("AGENTS.md", output["conflicts"])
            actions = {item["path"]: item["action"] for item in output["planned_files"]}
            self.assertEqual("compose", actions["AGENTS.md"])
            self.assertIn("docs/Conductor/ORCHESTRATION.md", output["conflicts"])
            self.assertEqual(before, inventory(root))

    def test_symlinked_target_ancestor_halts_before_any_write(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root = base / "repo"
            outside = base / "outside"
            root.mkdir()
            outside.mkdir()
            (root / "docs").symlink_to(outside, target_is_directory=True)
            before = inventory(base)
            output = preview(root, "brownfield")
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_UNSAFE_PATH", output["reason_code"])
            self.assertEqual(before, inventory(base))

    def test_greenfield_rejects_nonempty_repository(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "README.md", "existing\n")
            before = inventory(root)
            output = preview(root, "greenfield")
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_GREENFIELD_NOT_EMPTY", output["reason_code"])
            self.assertEqual(
                "choose_an_empty_target_or_remove_non_project_harness_content",
                output["next_legal_action"],
            )
            self.assertEqual(before, inventory(root))

    def test_payload_classifies_every_file_and_is_identical_between_packages(self):
        codex_version, codex_entries = RUNTIME.load_payload(
            REPO_ROOT / "plugins/conductor/payload"
        )
        claude_version, claude_entries = RUNTIME.load_payload(
            REPO_ROOT / "plugins/conductor-claude/payload"
        )
        self.assertEqual("0.3.4", codex_version)
        self.assertEqual(codex_entries, claude_entries)
        self.assertTrue(codex_entries)
        self.assertTrue(
            all(
                entry["classification"] in {"release-owned", "project-owned"}
                for entry in codex_entries
            )
        )


if __name__ == "__main__":
    unittest.main()
