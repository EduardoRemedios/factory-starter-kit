"""Review packets: what a human reviews at each gate, and the objective exit from grooming (synthetic only)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))

import conductor_gap as gap  # noqa: E402
import conductor_postimage as pi  # noqa: E402
import conductor_receipts as rc  # noqa: E402
import conductor_run_records as records  # noqa: E402
from tests.test_contract_lint import RUN_ID, Fixture, countersign, sha, write_json  # noqa: E402


class ReviewPacketTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)

    def packet(self) -> tuple[dict, str]:
        out = records.write_review_packet(self.fx.root, RUN_ID)
        return out, (self.fx.root / out["path"]).read_text()

    def cite_snapshot(self, snapshot_id: str, binding: dict) -> None:
        manifest = {"snapshot_id": snapshot_id, "aggregate_sha256": "a" * 64,
                    "provenance": {"repository_companions": binding},
                    "artifacts": {"content/docs/ENGINEERING_STANDARDS.md": {"source_path": "docs/ENGINEERING_STANDARDS.md", "sha256": "b" * 64}}}
        path = self.fx.root / "docs/upstream/bmad" / snapshot_id / "SNAPSHOT_MANIFEST.json"
        write_json(path, manifest)
        intent = json.loads((self.fx.run_root / "intent_pack.json").read_text())
        intent["sources"].append({"kind": "upstream_snapshot", "ref": path.relative_to(self.fx.root).as_posix(), "sha256": sha(path)})
        write_json(self.fx.run_root / "intent_pack.json", intent)

    def test_g1_packet_lists_inputs_intent_questions_and_digest_to_sign(self) -> None:
        self.cite_snapshot("spec042-v1", {"binding": "git", "approval_commit": "c" * 40})
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-001", gap_type="ux", question="Where do actions go?",
                     supersession_impact="active_scope", owner="UX")
        out, text = self.packet()
        self.assertEqual(("INTENT_DRAFT", False), (out["gate_state"], out["ready_for_g1"]))
        for expected in ("snapshot `spec042-v1`, binding git @ `cccccccccccc`", "`docs/ENGINEERING_STANDARDS.md`",
                         "| R-001 | Python says hello.", "SIMPLE-CODE-GATE v2 applies.", "GAP-001 is open with impact active_scope",
                         f"`intent_pack.json` SHA-256 `{sha(self.fx.run_root / 'intent_pack.json')}`",
                         "Completion is not merge, deployment or backlog approval"):
            self.assertIn(expected, text)

    def test_exit_conditions_future_only_needs_owner_and_new_snapshots_need_citation(self) -> None:
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-002", gap_type="product_context", question="Later?", supersession_impact="future_only")
        out, text = self.packet()
        self.assertFalse(out["ready_for_g1"])
        self.assertIn("GAP-001 is future_only but names no owner", text)
        (self.fx.run_root / "gap_requests/GAP-001.json").unlink()
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-002", gap_type="product_context", question="Later?",
                     supersession_impact="future_only", owner="PM")
        self.assertTrue(self.packet()[0]["ready_for_g1"], "an owned future-only finding never keeps a ready slice cycling")
        gap.open_gap(self.fx.root, RUN_ID, requirement_id="R-001", gap_type="ux", question="Now?", supersession_impact="active_scope")
        gap.resolve_gap(self.fx.root, RUN_ID, "GAP-002", decided_by="Test Human", decision="Reconciled in BMAD",
                        new_snapshot_id="spec042-v2", new_snapshot_sha256="d" * 64)
        out, text = self.packet()
        self.assertFalse(out["ready_for_g1"])
        self.assertIn("introduced snapshot spec042-v2, which the intent does not cite yet", text)
        self.cite_snapshot("spec042-v2", {"binding": "git", "approval_commit": "e" * 40})
        self.assertTrue(self.packet()[0]["ready_for_g1"])

    def test_g2_and_g3_packets_show_evidence_review_and_statement_digest(self) -> None:
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest()
        pi.capture(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        pi.compare(self.fx.root, RUN_ID)
        out, text = self.packet()
        self.assertEqual("EXECUTION_COMPLETE", out["gate_state"])
        self.assertIn("| VM-001 | R-001 |", text)
        self.assertIn("Write-boundary compare: PASS", text)
        rows = [{"requirement_id": r, "status": "verified", "evidence": [self.fx.receipt_ref(c)], "limitation": "fixture only"}
                for r, c in (("R-001", "VM-001"), ("R-002", "VM-002"), ("R-003", "VM-003"))]
        self.fx.write_statement(rows, "READY")
        out, text = self.packet()
        self.assertEqual("COMPLETION_DRAFT", out["gate_state"])
        self.assertIn("Independent review: `notes/verifier.md`", text)
        self.assertIn("| R-001 | verified | fixture only |", text)
        self.assertIn(f"`statement_of_completion.json` SHA-256 `{sha(self.fx.run_root / 'statement_of_completion.json')}`", text)
        self.assertFalse((self.fx.run_root / "countersign/COMPLETION.json").exists())


if __name__ == "__main__":
    unittest.main()
