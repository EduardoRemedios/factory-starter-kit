"""run-init: generated RUN_ID, planning-only skeleton, collision refusal and resume (synthetic only)."""
from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

import conductor_contract_lint as cl  # noqa: E402
import conductor_run_records as records  # noqa: E402
from tests.test_contract_lint import Fixture, countersign  # noqa: E402

NOW = datetime(2026, 9, 25, 10, 5, tzinfo=timezone.utc)
LATER = datetime(2026, 9, 25, 10, 6, tzinfo=timezone.utc)


class RunInitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)
        self.root = self.fx.root

    def test_creates_unique_planning_only_run_with_packet(self) -> None:
        out = records.init_run(self.root, "spec042-header", now=NOW)
        self.assertEqual(("CREATED", "RUN_20260925_1005_spec042-header"), (out["state"], out["run_id"]))
        run_root = self.root / "docs/Conductor/runs" / out["run_id"]
        for name in ("countersign", "gap_requests", "receipts", "postimage", "notes"):
            self.assertTrue((run_root / name).is_dir(), name)
        self.assertEqual("PLANNING_ONLY\n", (run_root / "EXECUTION_MODE.txt").read_text())
        self.assertEqual(out["run_id"], json.loads((run_root / "intent_pack.json").read_text())["run_id"])
        self.assertEqual([], list((run_root / "countersign").iterdir()), "run-init never signs")
        # The template draft deliberately fails G1 until a person-reviewed intent replaces its placeholders.
        self.assertEqual("INTENT_INVALID", out["gate_state"])
        packet = (self.root / out["packet"]).read_text()
        self.assertIn("Ready for G1 review: **no**", packet)
        self.assertIn("CONDUCTOR_CONTRACT_PLACEHOLDER", packet)

    def test_repeat_resumes_the_open_run_instead_of_duplicating(self) -> None:
        first = records.init_run(self.root, "spec042-header", now=NOW)
        again = records.init_run(self.root, "spec042-header", now=LATER)
        self.assertEqual(("EXISTING", first["run_id"]), (again["state"], again["run_id"]))
        self.assertEqual(1, len(list((self.root / "docs/Conductor/runs").glob("RUN_*_spec042-header"))))

    def test_slug_matches_exactly_not_as_a_suffix(self) -> None:
        # G3 finding F-6: 'adoption' must not resume RUN_..._spec042_adoption.
        records.init_run(self.root, "spec042_adoption", now=NOW)
        other = records.init_run(self.root, "adoption", now=LATER)
        self.assertEqual(("CREATED", "RUN_20260925_1006_adoption"), (other["state"], other["run_id"]))

    def test_new_run_collision_and_next_minute(self) -> None:
        records.init_run(self.root, "spec042-header", now=NOW)
        with self.assertRaises(cl.ContractLintError) as ctx:
            records.init_run(self.root, "spec042-header", new=True, now=NOW)
        self.assertEqual("CONDUCTOR_RUN_ID_COLLISION", ctx.exception.reason_code)
        second = records.init_run(self.root, "spec042-header", new=True, now=LATER)
        self.assertEqual("RUN_20260925_1006_spec042-header", second["run_id"])

    def test_completed_runs_are_not_resumed(self) -> None:
        first = records.init_run(self.root, "spec042-header", now=NOW)
        (self.root / "docs/Conductor/runs" / first["run_id"] / "countersign/COMPLETION.json").write_text("{}")
        self.assertEqual("CREATED", records.init_run(self.root, "spec042-header", now=LATER)["state"])

    def test_invalid_slug_and_interrupted_init_fail_with_reasons(self) -> None:
        for slug in ("AUD", "a", "../x", "has space", "x" * 42):
            with self.subTest(slug=slug), self.assertRaises(cl.ContractLintError) as ctx:
                records.init_run(self.root, slug, now=NOW)
            self.assertEqual("CONDUCTOR_RUN_SLUG_INVALID", ctx.exception.reason_code)
        (self.root / "docs/Conductor/runs/.tmp-RUN_20260925_1005_spec042-header").mkdir(parents=True)
        with self.assertRaises(cl.ContractLintError) as ctx:
            records.init_run(self.root, "spec042-header", now=NOW)
        self.assertEqual("CONDUCTOR_RUN_PARTIAL_INIT", ctx.exception.reason_code)

    def test_generated_id_satisfies_the_bmad_adapter_run_pattern(self) -> None:
        import importlib.machinery
        import importlib.util
        loader = importlib.machinery.SourceFileLoader("adapter_preflight", str(REPO_ROOT / "plugin-src/conductor-bmad/project-adapter/conductor_project_preflight"))
        spec = importlib.util.spec_from_loader(loader.name, loader)
        module = importlib.util.module_from_spec(spec)
        loader.exec_module(module)
        self.assertTrue(module.RUN_RE.fullmatch(records.init_run(self.root, "spec042-header", now=NOW)["run_id"]))
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")  # existing fixture run is unaffected
        self.assertEqual("INTENT_LOCKED", cl.lint_intent(self.root, self.fx.run_root.name)["state"])


if __name__ == "__main__":
    unittest.main()
