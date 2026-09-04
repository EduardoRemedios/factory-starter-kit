import hashlib
import importlib.util
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, runtime, seed_bmad, seed_git


CONDUCTOR_RUNTIME_PATH = REPO_ROOT / "plugin-src/conductor/runtime/conductor_plugin.py"
CONDUCTOR_SPEC = importlib.util.spec_from_file_location("conductor_bmad_pilot_factory_runtime", CONDUCTOR_RUNTIME_PATH)
conductor_runtime = importlib.util.module_from_spec(CONDUCTOR_SPEC)
assert CONDUCTOR_SPEC.loader is not None
CONDUCTOR_SPEC.loader.exec_module(conductor_runtime)
CONDUCTOR_PAYLOAD = REPO_ROOT / "plugins/conductor/payload"


class FactoryBmadSingleRepositoryPilotTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def adopt_factory(self, root: Path, mode: str):
        plan = conductor_runtime.evaluate_setup_plan(
            root,
            mode=mode,
            harness="claude",
            payload_root=CONDUCTOR_PAYLOAD,
            platform_name="darwin",
            python_version=(3, 12, 0),
        )
        self.assertEqual("PLAN_READY", plan["state"], plan)
        applied = conductor_runtime.apply_setup_plan(
            root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=CONDUCTOR_PAYLOAD,
        )
        self.assertEqual("CONDUCTOR_SETUP_APPLIED", applied["reason_code"], applied)

    def install_bmad_with_factory(self, root: Path):
        if os.environ.get("CONDUCTOR_BMAD_LIVE_INSTALLER") == "1":
            preview = runtime.bootstrap(root, "claude", None)
            self.assertEqual("PLAN_READY", preview["state"], preview)
            applied = runtime.bootstrap(root, "claude", preview["plan"]["plan_id"])
            self.assertEqual("APPLIED", applied["state"], applied)
        else:
            seed_bmad(root, capabilities=True)

    def install_bmad_only(self, root: Path):
        if os.environ.get("CONDUCTOR_BMAD_LIVE_INSTALLER") == "1":
            completed = subprocess.run(
                [
                    "npx", "--yes", "bmad-method@6.10.0", "install",
                    "--directory", str(root), "--modules", "bmm",
                    "--tools", "claude-code", "--yes",
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
        else:
            seed_bmad(root, capabilities=True)

    def finish_companion_intake(self, root: Path):
        audit = runtime.capability_audit(root, "claude")
        self.assertEqual("READY", audit["state"], audit)
        preview = runtime.intake(root, "claude", None)
        self.assertEqual("PLAN_READY", preview["state"], preview)
        applied = runtime.intake(root, "claude", preview["plan"]["plan_id"])
        self.assertEqual("APPLIED", applied["state"], applied)
        self.assertTrue((root / "docs/adapters/bmad/CAPABILITY_AUDIT.json").is_file())
        self.assertTrue(runtime.enforcement_activation(root)["active"])

    def test_greenfield_neither_journey(self):
        root = self.root()
        self.assertEqual("NEITHER_GREENFIELD", runtime.doctor(root, "claude")["state"])
        self.adopt_factory(root, "greenfield")
        self.assertEqual("CONDUCTOR_ONLY", runtime.doctor(root, "claude")["state"])
        self.install_bmad_with_factory(root)
        self.finish_companion_intake(root)

    def test_brownfield_neither_journey_preserves_source(self):
        root = self.root(); seed_git(root)
        source = root / "src/app.py"; source.parent.mkdir(); source.write_text("print('preserve')\n", encoding="utf-8")
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        self.assertEqual("NEITHER_BROWNFIELD", runtime.doctor(root, "claude")["state"])
        self.adopt_factory(root, "brownfield")
        self.install_bmad_with_factory(root)
        self.finish_companion_intake(root)
        self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())

    def test_brownfield_bmad_only_adopts_factory_before_intake(self):
        root = self.root(); seed_git(root)
        source = root / "app.py"; source.write_text("# existing\n", encoding="utf-8")
        before = hashlib.sha256(source.read_bytes()).hexdigest()
        self.install_bmad_only(root)
        doctor = runtime.doctor(root, "claude")
        self.assertEqual("BMAD_ONLY", doctor["state"])
        self.assertEqual("run_factory_brownfield_preview", doctor["next_legal_action"])
        self.assertFalse(runtime.enforcement_activation(root)["active"])
        self.adopt_factory(root, "brownfield")
        self.assertTrue(runtime.enforcement_activation(root)["active"])
        self.finish_companion_intake(root)
        self.assertEqual(before, hashlib.sha256(source.read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
