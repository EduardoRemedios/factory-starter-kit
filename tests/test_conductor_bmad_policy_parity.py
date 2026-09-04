import tempfile
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, runtime, seed_bmad, seed_factory, seed_git


class FactoryBmadPolicyParityTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); seed_git(root); seed_factory(root); seed_bmad(root, capabilities=True)
        return root

    def test_runtime_and_ci_lint_share_verdict(self):
        root = self.root()
        audit = runtime.capability_audit(root, "claude")
        lint = runtime.policy_lint(root, "claude")
        self.assertEqual(audit["reason_code"], lint["reason_code"])
        self.assertEqual(audit["policy_version"], lint["policy_version"])
        self.assertEqual(audit["coverage_sha256"], lint["coverage_sha256"])

    def test_unknown_returns_same_stable_reason(self):
        root = self.root()
        path = root / ".claude/commands/bmad-unknown.md"; path.parent.mkdir(parents=True); path.write_text("# unknown\n", encoding="utf-8")
        audit = runtime.capability_audit(root, "claude")
        lint = runtime.policy_lint(root, "claude")
        self.assertEqual("CONDUCTOR_BMAD_CAPABILITY_UNRECOGNIZED", audit["reason_code"])
        self.assertEqual(audit["reason_code"], lint["reason_code"])

    def test_ci_callable_policy_lint_cli(self):
        root = self.root()
        completed = subprocess.run(
            [sys.executable, str(REPO_ROOT / "plugin-src/conductor-bmad/runtime/conductor_bmad.py"), "--root", str(root), "--json", "policy-lint", "--harness", "claude"],
            text=True, capture_output=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("CONDUCTOR_BMAD_POLICY_OK", payload["reason_code"])
        self.assertEqual(runtime.policy.POLICY_VERSION, payload["policy_version"])

    def test_seeded_project_lint_uses_same_reason(self):
        root = self.root()
        preview = runtime.intake(root, "claude", None)
        self.assertEqual("PLAN_READY", preview["state"])
        runtime.intake(root, "claude", preview["plan"]["plan_id"])
        completed = subprocess.run(
            [sys.executable, "scripts/conductor_bmad_policy_lint"],
            cwd=root, text=True, capture_output=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual(runtime.policy_lint(root, "claude")["reason_code"], payload["reason_code"])

    def test_seeded_project_lint_does_not_write_bytecode(self):
        root = self.root()
        preview = runtime.intake(root, "claude", None)
        self.assertEqual("PLAN_READY", preview["state"])
        runtime.intake(root, "claude", preview["plan"]["plan_id"])
        environment = os.environ.copy()
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        environment.pop("PYTHONPYCACHEPREFIX", None)
        completed = subprocess.run(
            [sys.executable, "scripts/conductor_bmad_policy_lint"],
            cwd=root, env=environment, text=True, capture_output=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual([], list(root.rglob("*.pyc")))

    def test_generated_policy_copies_match_authored_source(self):
        authored = REPO_ROOT / "plugin-src/conductor-bmad/runtime/conductor_bmad_policy.py"
        self.assertEqual(authored.read_bytes(), (REPO_ROOT / "plugins/conductor-bmad/scripts/conductor_bmad_policy.py").read_bytes())
        self.assertEqual(authored.read_bytes(), (REPO_ROOT / "plugins/conductor-bmad-claude/scripts/conductor_bmad_policy.py").read_bytes())
        self.assertEqual(authored.read_bytes(), (REPO_ROOT / "plugins/conductor-bmad/assets/project-adapter/conductor_bmad_policy.py").read_bytes())
        self.assertEqual(authored.read_bytes(), (REPO_ROOT / "plugins/conductor-bmad-claude/assets/project-adapter/conductor_bmad_policy.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
