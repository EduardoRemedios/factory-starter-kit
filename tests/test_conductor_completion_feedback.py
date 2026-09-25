"""Completion feedback to the product-context lane: only after countersigned G3, never merge/deployment approval (synthetic only)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

import conductor_contract_lint as cl  # noqa: E402
import conductor_postimage as pi  # noqa: E402
import conductor_receipts as rc  # noqa: E402
import conductor_run_records as records  # noqa: E402
from tests.test_contract_lint import RUN_ID, Fixture, countersign, sha, write_json  # noqa: E402


class CompletionFeedbackTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)
        snapshot = self.fx.root / "docs/upstream/bmad/spec042-v1/SNAPSHOT_MANIFEST.json"
        write_json(snapshot, {"snapshot_id": "spec042-v1", "aggregate_sha256": "a" * 64,
                              "provenance": {"repository_companions": {"binding": "git", "approval_commit": "c" * 40}},
                              "artifacts": {"content/SPEC.md": {"source_path": "bmad/_bmad-output/specs/x/SPEC.md", "sha256": "b" * 64}}})
        intent = json.loads((self.fx.run_root / "intent_pack.json").read_text())
        intent["sources"].append({"kind": "upstream_snapshot", "ref": snapshot.relative_to(self.fx.root).as_posix(), "sha256": sha(snapshot)})
        write_json(self.fx.run_root / "intent_pack.json", intent)
        write_json(self.fx.run_root / "gap_requests/GAP-001.json", {
            "schema_version": 1, "gap_id": "GAP-001", "run_id": RUN_ID, "intent_pack_sha256": sha(self.fx.run_root / "intent_pack.json"),
            "requirement_id": "R-002", "gap_type": "ux", "question": "Show breadcrumbs in a later slice?",
            "supersession_impact": "future_only", "owner": "PM (Test Owner)"})
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest()
        pi.capture(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        pi.compare(self.fx.root, RUN_ID)
        rows = [{"requirement_id": r, "status": "verified", "evidence": [self.fx.receipt_ref(c)]}
                for r, c in (("R-001", "VM-001"), ("R-002", "VM-002"), ("R-003", "VM-003"))]
        rows[1]["limitation"] = "Checked on the fixture only."
        rows[1]["residual_gap"] = "gap_requests/GAP-001.json"
        self.fx.write_statement(rows, "READY")

    def test_refused_before_completion_countersign(self) -> None:
        with self.assertRaises(cl.ContractLintError) as ctx:
            records.completion_feedback(self.fx.root, RUN_ID)
        self.assertEqual("CONDUCTOR_FEEDBACK_NOT_COUNTERSIGNED", ctx.exception.reason_code)
        self.assertFalse((self.fx.run_root / "UPSTREAM_FEEDBACK.md").exists())

    def test_feedback_names_sources_status_evidence_limitations_and_owned_deferrals(self) -> None:
        countersign(self.fx.run_root, "COMPLETION", "statement_of_completion.json")
        out = records.completion_feedback(self.fx.root, RUN_ID)
        data = json.loads((self.fx.root / out["paths"][1]).read_text())
        text = (self.fx.root / out["paths"][0]).read_text()
        self.assertEqual(["merge", "deployment", "backlog change", "release"], data["not_approved_by_this_record"])
        self.assertEqual("spec042-v1", data["source_snapshots"][0]["snapshot_id"])
        self.assertEqual("c" * 40, data["source_snapshots"][0]["approval_commit"])
        self.assertEqual(["VM-002"], data["requirements"][1]["evidence"])
        self.assertEqual("Checked on the fixture only.", data["requirements"][1]["limitation"])
        self.assertEqual([{"gap_id": "GAP-001", "requirement_id": "R-002", "question": "Show breadcrumbs in a later slice?",
                           "owner": "PM (Test Owner)", "decision": None,
                           "disposition": "backlog decision for PM/BA; not delivered by this run"}], data["deferred_findings"])
        self.assertEqual(sha(self.fx.run_root / "statement_of_completion.json"), data["statement_sha256"])
        self.assertIn("It is **not** merge, deployment, release or backlog approval", text)
        self.assertIn("does not mark any product capability as delivered upstream", text)
        self.assertEqual("REVIEW_READY", data["completion"]["handoff_state"])

    def test_stale_completion_countersign_refuses_feedback(self) -> None:
        countersign(self.fx.run_root, "COMPLETION", "statement_of_completion.json")
        statement = json.loads((self.fx.run_root / "statement_of_completion.json").read_text())
        statement["rows"][0]["limitation"] = "edited after signature"
        write_json(self.fx.run_root / "statement_of_completion.json", statement)
        with self.assertRaises(cl.ContractLintError):
            records.completion_feedback(self.fx.root, RUN_ID)


if __name__ == "__main__":
    unittest.main()
