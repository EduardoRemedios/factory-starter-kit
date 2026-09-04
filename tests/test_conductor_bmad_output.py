import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import runtime, seed_factory
from tests.test_conductor_plugin_cli import runtime_for


REPO_ROOT = Path(__file__).resolve().parents[1]


class FactoryBmadOutputTests(unittest.TestCase):
    def test_default_summary_is_concise_and_has_one_next_action(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); seed_factory(root)
        text = runtime.concise(runtime.bootstrap(root, "claude", None))
        self.assertLessEqual(len(text.splitlines()), 7)
        self.assertEqual(1, text.count("Next:"))
        self.assertNotIn("{", text)
        self.assertNotIn("settings.local.json", text)
        self.assertIn("Target:", text)
        self.assertIn("Approval Plan ID:", text)
        self.assertIn("Pre-inventory SHA-256:", text)
        self.assertIn("Changes:", text)

    def test_bootstrap_summary_distinguishes_plan_id_from_inventory_hash(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); seed_factory(root)
        payload = runtime.bootstrap(root, "claude", None)
        text = runtime.concise(payload)
        self.assertIn(f"Approval Plan ID: {payload['plan']['plan_id']}", text)
        self.assertIn(
            f"Pre-inventory SHA-256: {payload['plan']['pre_inventory_sha256']}",
            text,
        )
        self.assertNotIn("Plan:", text)

    def test_bootstrap_apply_requires_a_fresh_claude_session_before_intake(self):
        payload = runtime.result(
            "APPLIED",
            "CONDUCTOR_BMAD_BOOTSTRAP_APPLIED",
            "restart_claude_then_run_factory_bmad_doctor",
            target="/tmp/project",
            mutations=["_bmad"],
        )
        text = runtime.concise(payload)
        self.assertIn("restart_claude_then_run_factory_bmad_doctor", text)

    def test_json_is_deterministic_opt_in_surface(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        payload = runtime.doctor(Path(temporary.name), "codex")
        self.assertEqual("NEITHER_GREENFIELD", payload["state"])
        self.assertEqual([], payload["mutations"])

    def test_conductor_authored_cli_is_concise_by_default_and_json_on_request(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            root = base / "new-project"
            root.mkdir()
            authored_runtime = runtime_for("authored", base)
            command = [
                sys.executable,
                str(authored_runtime),
                "--root",
                str(root),
            ]
            environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
            summary = subprocess.run(
                [*command, "greenfield", "--harness", "claude"],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertLessEqual(len(summary.stdout.splitlines()), 7)
            self.assertIn("Target:", summary.stdout)
            self.assertIn("Approval Plan ID:", summary.stdout)
            self.assertIn("Changes:", summary.stdout)
            self.assertNotIn("Plan:", summary.stdout)
            self.assertNotIn('"planned_files"', summary.stdout)
            structured = subprocess.run(
                [*command, "--json", "greenfield", "--harness", "claude"],
                check=True,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual("PLAN_READY", json.loads(structured.stdout)["state"])


if __name__ == "__main__":
    unittest.main()
