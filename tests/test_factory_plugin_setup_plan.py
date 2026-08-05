import importlib.util
import tempfile
import unittest
from pathlib import Path

from tests.test_factory_plugin_status import inventory, write


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_PATH = REPO_ROOT / "plugin-src/factory/runtime/factory_plugin.py"
PAYLOAD_ROOT = REPO_ROOT / "plugins/factory/payload"
SPEC = importlib.util.spec_from_file_location("factory_plugin_setup_runtime", RUNTIME_PATH)
RUNTIME = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(RUNTIME)


def preview(root: Path, mode: str):
    return RUNTIME.evaluate_setup_plan(
        root,
        mode=mode,
        harness="codex",
        payload_root=PAYLOAD_ROOT,
        platform_name="darwin",
        python_version=(3, 11, 0),
    )


class FactoryPluginSetupPlanTests(unittest.TestCase):
    def test_greenfield_plan_contains_required_factory_paths_without_writing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            before = inventory(root)
            output = preview(root, "greenfield")
            actions = {
                item["path"]: item["action"] for item in output["planned_files"]
            }
            self.assertEqual("PLAN_READY", output["state"])
            self.assertEqual("FACTORY_PLAN_READY", output["reason_code"])
            self.assertEqual("create", actions["AGENTS.md"])
            self.assertEqual("create", actions["docs/Factory/ARCHITECTURE.md"])
            self.assertEqual("create", actions["scripts/factoryctl"])
            change_plan = output["change_plan"]
            self.assertEqual(output["plan_id"], change_plan["transaction_id"])
            self.assertEqual("greenfield", change_plan["operation"])
            self.assertIsNone(change_plan["source_version"])
            self.assertEqual("0.2.0", change_plan["target_version"])
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

    def test_brownfield_conflict_halts_before_any_write(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "AGENTS.md", "project-specific instructions\n")
            write(root / "docs/Factory/ORCHESTRATION.md", "different factory\n")
            before = inventory(root)
            output = preview(root, "brownfield")
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("FACTORY_CONFLICT_USER_OWNED", output["reason_code"])
            self.assertIn("AGENTS.md", output["conflicts"])
            self.assertIn("docs/Factory/ORCHESTRATION.md", output["conflicts"])
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
            self.assertEqual("FACTORY_UNSAFE_PATH", output["reason_code"])
            self.assertEqual(before, inventory(base))

    def test_greenfield_rejects_nonempty_repository(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "README.md", "existing\n")
            before = inventory(root)
            output = preview(root, "greenfield")
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("FACTORY_GREENFIELD_NOT_EMPTY", output["reason_code"])
            self.assertEqual(before, inventory(root))

    def test_payload_classifies_every_file_and_is_identical_between_packages(self):
        codex_version, codex_entries = RUNTIME.load_payload(
            REPO_ROOT / "plugins/factory/payload"
        )
        claude_version, claude_entries = RUNTIME.load_payload(
            REPO_ROOT / "plugins/factory-claude/payload"
        )
        self.assertEqual("0.2.0", codex_version)
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
