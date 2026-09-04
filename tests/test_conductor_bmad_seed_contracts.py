"""seed-contracts (0.3.1, finding F-6): inert adapter contracts seeded independently of intake."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, runtime, seed_factory, seed_git

CLAUDE_PACKAGE = REPO_ROOT / "plugins/conductor-bmad-claude"


class SeedContractsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        seed_git(self.root)
        seed_factory(self.root)

    def test_packaged_assets_carry_the_published_contracts(self) -> None:
        for rel in ("assets/project-adapter/contracts/bmad_adapter_config.schema.json",
                    "assets/project-adapter/contracts/lane_policy.schema.json",
                    "assets/project-adapter/lane_policy.json",
                    "assets/project-adapter/BMAD_POLICY.md"):
            with self.subTest(asset=rel):
                self.assertTrue((CLAUDE_PACKAGE / rel).is_file(), rel)
        shipped = json.loads((CLAUDE_PACKAGE / "assets/project-adapter/lane_policy.json").read_text())
        published = json.loads((REPO_ROOT / "docs/adapters/bmad/lane_policy.json").read_text())
        self.assertEqual(shipped, published)

    def test_preview_apply_idempotent_and_conflict(self) -> None:
        preview = runtime.seed_contracts(self.root, None)
        self.assertEqual(("PLAN_READY", "CONDUCTOR_BMAD_SEED_PLAN_READY"), (preview["state"], preview["reason_code"]))
        self.assertEqual({"create"}, {item["action"] for item in preview["plan"]["files"]})
        self.assertFalse((self.root / "docs/adapters/bmad").exists(), "preview must not write")
        wrong = runtime.seed_contracts(self.root, "not-the-plan")
        self.assertEqual("CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", wrong["reason_code"])
        applied = runtime.seed_contracts(self.root, preview["plan"]["plan_id"])
        self.assertEqual(("APPLIED", "CONDUCTOR_BMAD_SEED_APPLIED"), (applied["state"], applied["reason_code"]))
        for rel in ("docs/adapters/bmad/contracts/bmad_adapter_config.schema.json", "docs/adapters/bmad/lane_policy.json", "docs/adapters/bmad/BMAD_POLICY.md"):
            self.assertTrue((self.root / rel).is_file(), rel)
        self.assertTrue((self.root / applied["receipt"]).is_file())
        again = runtime.seed_contracts(self.root, None)
        self.assertEqual(("READY", "CONDUCTOR_BMAD_SEED_CURRENT"), (again["state"], again["reason_code"]))
        (self.root / "docs/adapters/bmad/lane_policy.json").write_text("{}", encoding="utf-8")
        conflict = runtime.seed_contracts(self.root, None)
        self.assertEqual("CONDUCTOR_BMAD_SEED_CONFLICT", conflict["reason_code"])
        self.assertEqual(["docs/adapters/bmad/lane_policy.json"], conflict["conflicts"])

    def test_seed_makes_a_declared_adapter_lintable_before_intake(self) -> None:
        """The F-6 scenario: adapters.bmad declared, intake impossible, G1 lint must still validate."""
        import shutil  # noqa: PLC0415
        # a minimal Conductor-adopted repo: contracts, INVARIANTS, AGENTS.md with managed block, project config, a run
        shutil.copytree(REPO_ROOT / "docs/Conductor/contracts", self.root / "docs/Conductor/contracts")
        shutil.copy(REPO_ROOT / "AGENTS.md", self.root / "AGENTS.md")
        (self.root / "docs/Conductor/INVARIANTS.md").write_text("# inv\n", encoding="utf-8")
        (self.root / "docs/PROJECT_STATE.md").write_text("# state\n", encoding="utf-8")
        config = json.loads((REPO_ROOT / "docs/Conductor/templates/project_config.template.json").read_text())
        config["adapters"] = {"bmad": {"declared_root": "tools/bmad/_bmad", "legacy_evidence_root": "docs/adapters/bmad/legacy-evidence"}}
        (self.root / "docs/Conductor/PROJECT_CONFIG.json").write_text(json.dumps(config), encoding="utf-8")
        run = self.root / "docs/Conductor/runs/RUN_20260904_2200_seed_fixture"
        (run / "notes").mkdir(parents=True)
        (run / "EXECUTION_MODE.txt").write_text("PLANNING_ONLY\n", encoding="utf-8")
        (run / "notes/brief.md").write_text("brief\n", encoding="utf-8")
        import hashlib  # noqa: PLC0415
        intent = json.loads((REPO_ROOT / "docs/Conductor/templates/intent_pack.template.json").read_text())
        intent.update({"run_id": run.name, "goal": "Seed fixture goal statement.", "scope_in": ["fixture"], "scope_out": [], "risks": []})
        intent["sources"] = [{"kind": "human_brief", "ref": f"docs/Conductor/runs/{run.name}/notes/brief.md",
                              "sha256": hashlib.sha256(b"brief\n").hexdigest()}]
        intent["requirements"][0]["statement"] = "One requirement."
        intent["requirements"][0]["acceptance"] = "Acceptance is stated."
        intent["verification_requirements"][0]["description"] = "One check."
        intent["constraints"][0]["statement"] = "One constraint."
        (run / "intent_pack.json").write_text(json.dumps(intent), encoding="utf-8")
        scripts = REPO_ROOT / "scripts"
        env = {"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"}

        def lint() -> dict:
            out = subprocess.run([sys.executable, str(scripts / "conductorctl"), "contract-lint", "intent", "--run", run.name, "--json"],
                                 cwd=self.root, capture_output=True, text=True, env=env)
            return json.loads(out.stdout)

        # conductorctl resolves the repo from its own location; run the lint module against self.root directly instead
        sys.path.insert(0, str(scripts))
        import conductor_contract_lint as cl  # noqa: PLC0415
        before = cl.lint_intent(self.root, run.name)
        self.assertIn("CONDUCTOR_CONTRACT_ADAPTER_SCHEMA_MISSING", " ".join(before["errors"]))
        preview = runtime.seed_contracts(self.root, None)
        runtime.seed_contracts(self.root, preview["plan"]["plan_id"])
        after = cl.lint_intent(self.root, run.name)
        self.assertEqual(after["status"], "PASS", after)


if __name__ == "__main__":
    unittest.main()
