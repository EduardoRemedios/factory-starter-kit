import importlib.util
import tempfile
import unittest
from pathlib import Path

from tests.test_factory_plugin_status import inventory, write


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_PATH = REPO_ROOT / "plugin-src/factory/runtime/factory_plugin.py"
PAYLOAD_ROOT = REPO_ROOT / "plugins/factory/payload"
SPEC = importlib.util.spec_from_file_location("factory_plugin_adapter_runtime", RUNTIME_PATH)
RUNTIME = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(RUNTIME)


def claude_plan(root: Path):
    return RUNTIME.evaluate_setup_plan(
        root,
        mode="brownfield",
        harness="claude",
        payload_root=PAYLOAD_ROOT,
        platform_name="darwin",
        python_version=(3, 11, 0),
    )


def write_skill(root: Path, directory: str, name: str) -> None:
    write(
        root / ".agents/skills" / directory / "SKILL.md",
        f"---\nname: {name}\ndescription: fixture\n---\n",
    )


class FactoryPluginAdapterTests(unittest.TestCase):
    def test_claude_bridge_is_previewed_then_created_as_one_line(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            plan = claude_plan(root)
            bridge = next(
                item for item in plan["planned_files"] if item["path"] == "CLAUDE.md"
            )
            self.assertEqual("create", bridge["action"])
            self.assertEqual("generated/pinned", bridge["classification"])
            before = inventory(root)
            self.assertEqual(before, inventory(root))
            applied = RUNTIME.apply_setup_plan(
                root,
                plan=plan,
                approved_plan_id=plan["plan_id"],
                payload_root=PAYLOAD_ROOT,
            )
            self.assertEqual("FACTORY_SETUP_APPLIED", applied["reason_code"])
            self.assertEqual("@AGENTS.md\n", (root / "CLAUDE.md").read_text())
            self.assertNotIn("##", (root / "CLAUDE.md").read_text())

    def test_existing_exact_claude_bridge_is_no_change(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "CLAUDE.md", "@AGENTS.md\n")
            before = inventory(root)
            plan = claude_plan(root)
            bridge = next(
                item for item in plan["planned_files"] if item["path"] == "CLAUDE.md"
            )
            self.assertEqual("no_change", bridge["action"])
            self.assertNotIn("CLAUDE.md", plan["conflicts"])
            self.assertEqual(before, inventory(root))

    def test_conflicting_claude_instructions_halt_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "CLAUDE.md", "project-specific Claude rules\n")
            before = inventory(root)
            plan = claude_plan(root)
            self.assertEqual("BLOCKED", plan["state"])
            self.assertEqual("FACTORY_CONFLICT_USER_OWNED", plan["reason_code"])
            self.assertIn("CLAUDE.md", plan["conflicts"])
            self.assertEqual(before, inventory(root))

    def test_existing_factory_role_skills_coexist(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_skill(root, "factory-root-planner", "factory-root-planner")
            write_skill(root, "factory-purple-gate", "factory-purple-gate")
            before = inventory(root)
            output = RUNTIME.evaluate_skill_coexistence(
                root,
                plugin_skill_names={"factory-doctor", "factory-progress"},
            )
            self.assertEqual("COMPATIBLE", output["state"])
            self.assertEqual("FACTORY_SKILLS_COMPATIBLE", output["reason_code"])
            self.assertEqual([], output["automatic_deletions"])
            self.assertEqual(before, inventory(root))

    def test_exact_skill_name_collision_halts_without_deletion(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_skill(root, "local-planner", "factory-root-planner")
            before = inventory(root)
            output = RUNTIME.evaluate_skill_coexistence(
                root,
                plugin_skill_names={"factory-root-planner"},
            )
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("FACTORY_SKILL_COLLISION", output["reason_code"])
            self.assertEqual([], output["automatic_deletions"])
            self.assertEqual(before, inventory(root))

    def test_doctor_discloses_selected_model_for_all_roles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative in (
                "AGENTS.md",
                "docs/Factory/ARCHITECTURE.md",
                "docs/Factory/ORCHESTRATION.md",
                "scripts/factoryctl",
            ):
                write(root / relative, "fixture\n")
            output = RUNTIME.evaluate_doctor(
                root,
                harness="codex",
                platform_name="darwin",
                python_version=(3, 11, 0),
            )
            self.assertEqual(
                "selected_session_model_serves_all_factory_roles",
                output["model_policy"]["default"],
            )
            self.assertEqual(["red", "blue", "purple"], output["model_policy"]["roles"])
            self.assertFalse(output["model_policy"]["separate_routing_configured"])


if __name__ == "__main__":
    unittest.main()
