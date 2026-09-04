"""Gap Requests (migration step 8): agent opens, human resolves, active-scope supersession reopens G1."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

import conductor_contract_lint as cl  # noqa: E402
import conductor_gap as gap  # noqa: E402
from tests.test_contract_lint import RUN_ID, Fixture, countersign  # noqa: E402


class GapRequestTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)

    def test_open_binds_to_intent_and_validates(self) -> None:
        out = gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-002", gap_type="product_context",
                           question="Is the fixture still wanted?", supersession_impact="future_only")
        self.assertEqual(out["gap_id"], "GAP-001")
        doc = json.loads((self.fx.run_root / "gap_requests" / "GAP-001.json").read_text())
        self.assertEqual(doc["intent_pack_sha256"], cl.sha256_file(self.fx.run_root / "intent_pack.json"))
        second = gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-001", gap_type="constraint", question="Which timeout?")
        self.assertEqual(second["gap_id"], "GAP-002")

    def test_open_rejects_unknown_requirement_and_bad_type(self) -> None:
        with self.assertRaises(cl.ContractLintError) as ctx:
            gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-999", gap_type="ux", question="?")
        self.assertEqual(ctx.exception.reason_code, "CONDUCTOR_GAP_UNKNOWN_REQUIREMENT")
        with self.assertRaises(cl.ContractLintError) as ctx:
            gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-001", gap_type="budget", question="?")
        self.assertEqual(ctx.exception.reason_code, "CONDUCTOR_GAP_SCHEMA_INVALID")

    def test_resolve_needs_a_human_and_happens_once(self) -> None:
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-002", gap_type="product_context", question="?")
        with self.assertRaises(cl.ContractLintError) as ctx:
            gap.resolve_gap(self.fx.root, RUN_ID, "GAP-001", decided_by="  ", decision="drop it")
        self.assertEqual(ctx.exception.reason_code, "CONDUCTOR_GAP_DECIDER_REQUIRED")
        out = gap.resolve_gap(self.fx.root, RUN_ID, "GAP-001", decided_by="Test Human", decision="drop it")
        self.assertFalse(out["g1_reopen_required"])
        with self.assertRaises(cl.ContractLintError) as ctx:
            gap.resolve_gap(self.fx.root, RUN_ID, "GAP-001", decided_by="Test Human", decision="again")
        self.assertEqual(ctx.exception.reason_code, "CONDUCTOR_GAP_ALREADY_RESOLVED")

    def test_active_scope_resolution_with_new_snapshot_reopens_g1_in_completion_lint(self) -> None:
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-002", gap_type="architecture", question="?", supersession_impact="active_scope")
        out = gap.resolve_gap(self.fx.root, RUN_ID, "GAP-001", decided_by="Test Human", decision="replace", new_snapshot_id="SNAP-2", new_snapshot_sha256="d" * 64)
        self.assertTrue(out["g1_reopen_required"])
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest()
        self.fx.write_statement([
            {"requirement_id": "R-001", "status": "not_done", "evidence": []},
            {"requirement_id": "R-002", "status": "not_done", "evidence": []},
            {"requirement_id": "R-003", "status": "not_done", "evidence": []},
        ], "BLOCKED")
        errors = " ".join(cl.lint_completion(self.fx.root, RUN_ID)["errors"])
        self.assertIn("CONDUCTOR_CONTRACT_G1_REOPEN_REQUIRED", errors)
        self.assertIn("GAP-001", errors)

    def test_resolved_gap_is_a_valid_decision_ref(self) -> None:
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-003", gap_type="requirement", question="?")
        gap.resolve_gap(self.fx.root, RUN_ID, "GAP-001", decided_by="Test Human", decision="out of scope for this run")
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest()
        import conductor_postimage as pi  # noqa: E402
        import conductor_receipts as rc  # noqa: E402
        pi.capture(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        pi.compare(self.fx.root, RUN_ID)
        self.fx.write_statement([
            {"requirement_id": "R-001", "status": "verified", "evidence": [self.fx.receipt_ref("VM-001")]},
            {"requirement_id": "R-002", "status": "verified", "evidence": [self.fx.receipt_ref("VM-002")]},
            {"requirement_id": "R-003", "status": "out_of_scope", "evidence": [], "decision_ref": "gap_requests/GAP-001.json"},
        ], "NEEDS_HUMAN_DECISION")
        result = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertEqual(result["status"], "PASS", result)


if __name__ == "__main__":
    unittest.main()
