"""End-to-end test of the Conductor contract core (migration steps 4 and 5).

Builds a temporary repository with a run in the Conductor layout and drives it
through G1 -> G2 -> G3 using the real modules, then attacks it: tampered
receipts, agent-authored results, stale countersigns, unproven claims, wrong
derived state, and a protected-root write.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import conductor_contract_lint as cl  # noqa: E402
import conductor_postimage as pi  # noqa: E402
import conductor_receipts as rc  # noqa: E402

RUN_ID = "RUN_20260904_2100_contract_core_fixture"
ZERO = "0" * 64


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def countersign(run_root: Path, kind: str, subject: str, decision: str = "GO") -> None:
    write_json(run_root / "countersign" / f"{kind}.json", {
        "schema_version": 1, "kind": kind, "subject_path": subject, "subject_sha256": sha(run_root / subject),
        "decision": decision, "signer": "Test Human", "utc": "2026-09-04T21:00:00Z",
    })


class Fixture:
    """A temporary repo with contracts, a brief, and one run."""

    def __init__(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="conductor-contract-"))
        self.root = self.tmp / "repo"
        shutil.copytree(REPO_ROOT / "docs" / "Conductor" / "contracts", self.root / "docs" / "Conductor" / "contracts")
        (self.root / "docs" / "PROJECT_STATE.md").parent.mkdir(parents=True, exist_ok=True)
        (self.root / "docs" / "PROJECT_STATE.md").write_text("# state\n", encoding="utf-8")
        (self.root / "docs" / "Conductor" / "INVARIANTS.md").write_text("# invariants\n", encoding="utf-8")
        (self.root / "scripts").mkdir()
        (self.root / "scripts" / "protected.py").write_text("print('protected')\n", encoding="utf-8")
        # Project Config declares managed_block mode, so the fixture carries the kit's real managed block.
        shutil.copy(REPO_ROOT / "AGENTS.md", self.root / "AGENTS.md")
        self.run_root = self.root / "docs" / "Conductor" / "runs" / RUN_ID
        (self.run_root / "notes").mkdir(parents=True)
        (self.run_root / "notes" / "brief.md").write_text("Build the thing.\n", encoding="utf-8")
        (self.run_root / "EXECUTION_MODE.txt").write_text("PLANNING_ONLY\n", encoding="utf-8")
        write_json(self.root / "docs" / "Conductor" / "PROJECT_CONFIG.json", {
            "schema_version": 1, "product_name": "Conductor", "protected_roots": ["scripts", "docs/Conductor/INVARIANTS.md"],
            "allowed_harnesses": ["claude-code"], "default_budget": {"model": "claude-fable-5-1", "effort_g2": "high", "effort_g3": "high"},
            "agents_md": {"mode": "managed_block"}, "required_docs": ["docs/PROJECT_STATE.md", "docs/Conductor/INVARIANTS.md"],
            "recall": {"trigger": "when_index_nonempty"}, "adapters": {},
        })
        self.write_intent()

    def write_intent(self, **overrides: Any) -> None:
        intent = {
            "schema_version": 1, "run_id": RUN_ID,
            "goal": "Prove the contract core end to end on a fixture repository.",
            "requirements": [
                {"id": "R-001", "statement": "Python says hello.", "acceptance": "Command exits 0.", "severity": "blocking"},
                {"id": "R-002", "statement": "A fixture file exists.", "acceptance": "Target present and non-empty.", "severity": "normal"},
                {"id": "R-003", "statement": "Human reviews the output.", "acceptance": "Attestation recorded.", "severity": "normal"},
            ],
            "constraints": [{"id": "C-001", "statement": "SIMPLE-CODE-GATE v2 applies.", "source": "docs/Conductor/INVARIANTS.md"}],
            "scope_in": ["fixture"], "scope_out": ["everything else"],
            "sources": [{"kind": "human_brief", "ref": f"docs/Conductor/runs/{RUN_ID}/notes/brief.md", "sha256": sha(self.run_root / "notes" / "brief.md")}],
            "verification_requirements": [
                {"id": "VM-001", "requirement_ids": ["R-001"], "tier": "V2", "description": "hello command"},
                {"id": "VM-002", "requirement_ids": ["R-002"], "tier": "V1", "description": "fixture present"},
                {"id": "VM-003", "requirement_ids": ["R-003"], "tier": "V4", "description": "human review"},
            ],
            "budget": {"model": "claude-fable-5-1", "effort_g2": "high", "effort_g3": "high"},
            "execution_mode": "PLANNING_ONLY",
            "done_definition": "Every row verified or decided.",
        }
        intent.update(overrides)
        write_json(self.run_root / "intent_pack.json", intent)

    def write_manifest(self, hello_cmd: list[str] | None = None) -> None:
        (self.run_root / "notes" / "fixture.txt").write_text("fixture\n", encoding="utf-8")
        manifest = {
            "schema_version": 2, "run_id": RUN_ID, "execution_mode": "PLANNING_ONLY",
            "execution_order": ["VM-001", "VM-002", "VM-003"],
            "checks": [
                {"id": "VM-001", "tier": "V2", "type": "command", "requirement_ids": ["R-001"], "description": "hello",
                 "command": hello_cmd or [sys.executable, "-c", "print('hello')"], "halt_on_failure": True, "evidence_path": "receipts/VM-001.json"},
                {"id": "VM-002", "tier": "V1", "type": "artifact", "requirement_ids": ["R-002"], "description": "fixture",
                 "target": f"docs/Conductor/runs/{RUN_ID}/notes/fixture.txt", "halt_on_failure": True, "evidence_path": "receipts/VM-002.json"},
                {"id": "VM-003", "tier": "V4", "type": "manual", "requirement_ids": ["R-003"], "description": "human review",
                 "expected": "Reviewer attests.", "halt_on_failure": True, "evidence_path": "receipts/VM-003.json"},
            ],
        }
        (self.run_root / "verification_manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

    def receipt_ref(self, check_id: str) -> dict[str, str]:
        path = self.run_root / "receipts" / f"{check_id}.json"
        return {"check_id": check_id, "receipt_path": f"receipts/{check_id}.json", "receipt_sha256": sha(path)}

    def write_statement(self, rows: list[dict[str, Any]], derived: str, handoff: str = "REVIEW_READY") -> None:
        report = self.run_root / "notes" / "verifier.md"
        report.write_text("# verifier\nAll rows audited against receipts.\n", encoding="utf-8")
        write_json(self.run_root / "statement_of_completion.json", {
            "schema_version": 1, "run_id": RUN_ID, "intent_pack_sha256": sha(self.run_root / "intent_pack.json"),
            "rows": rows, "verifier": {"report_path": "notes/verifier.md", "report_sha256": sha(report), "fresh_context": True},
            "derived_state": derived, "handoff_state": handoff,
        })

    def cleanup(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class ContractCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)

    # ---- G1
    def test_g1_draft_then_locked(self) -> None:
        r = cl.lint_intent(self.fx.root, RUN_ID)
        self.assertEqual((r["status"], r["state"]), ("PASS", "INTENT_DRAFT"), r)
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        r = cl.lint_intent(self.fx.root, RUN_ID)
        self.assertEqual((r["status"], r["state"]), ("PASS", "INTENT_LOCKED"), r)

    def test_g1_rejects_placeholders_unknown_requirements_and_bad_source_digest(self) -> None:
        self.fx.write_intent(goal="Prove the core for RUN_YYYYMMDD_HHMM_TAG.")
        self.assertIn("CONDUCTOR_CONTRACT_PLACEHOLDER", " ".join(cl.lint_intent(self.fx.root, RUN_ID)["errors"]))
        self.fx.write_intent(goal="TBD")
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["status"], "FAIL", "schema itself rejects bare TBD")
        self.fx.write_intent(verification_requirements=[{"id": "VM-001", "requirement_ids": ["R-999"], "tier": "V1", "description": "x"}])
        self.assertIn("CONDUCTOR_CONTRACT_UNKNOWN_REQUIREMENT", " ".join(cl.lint_intent(self.fx.root, RUN_ID)["errors"]))
        self.fx.write_intent(sources=[{"kind": "human_brief", "ref": f"docs/Conductor/runs/{RUN_ID}/notes/brief.md", "sha256": "a" * 64}])
        self.assertIn("CONDUCTOR_CONTRACT_SOURCE_DIGEST_MISMATCH", " ".join(cl.lint_intent(self.fx.root, RUN_ID)["errors"]))

    def test_g1_stale_countersign_is_an_error(self) -> None:
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_intent(goal="Prove the contract core end to end, edited after lock.")
        r = cl.lint_intent(self.fx.root, RUN_ID)
        self.assertEqual(r["status"], "FAIL")
        self.assertIn("CONDUCTOR_CONTRACT_COUNTERSIGN_STALE", " ".join(r["errors"]))

    def test_g1_project_config_adapter_block_needs_adapter_schema(self) -> None:
        cfg_path = self.fx.root / "docs" / "Conductor" / "PROJECT_CONFIG.json"
        cfg = json.loads(cfg_path.read_text())
        cfg["adapters"] = {"widget": {"anything": 1}}
        write_json(cfg_path, cfg)
        self.assertIn("CONDUCTOR_CONTRACT_ADAPTER_SCHEMA_MISSING", " ".join(cl.lint_intent(self.fx.root, RUN_ID)["errors"]))
        # with the real BMAD adapter schema present, a valid block passes and an invalid one fails
        shutil.copytree(REPO_ROOT / "docs" / "adapters" / "bmad" / "contracts", self.fx.root / "docs" / "adapters" / "bmad" / "contracts")
        cfg["adapters"] = {"bmad": {"declared_root": "_bmad", "legacy_evidence_root": "docs/adapters/bmad/legacy-evidence"}}
        write_json(cfg_path, cfg)
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["status"], "PASS")
        cfg["adapters"] = {"bmad": {"declared_root": "docs/x/_bmad", "legacy_evidence_root": "docs/adapters/bmad/legacy-evidence"}}
        write_json(cfg_path, cfg)
        self.assertIn("CONDUCTOR_CONTRACT_ADAPTER_CONFIG_INVALID", " ".join(cl.lint_intent(self.fx.root, RUN_ID)["errors"]))

    # ---- G2
    def lock_and_manifest(self) -> None:
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest()

    def test_g2_requires_lock_then_runs_receipts_to_completion(self) -> None:
        self.fx.write_manifest()
        r = cl.lint_execution(self.fx.root, RUN_ID)
        self.assertEqual(r["state"], "INTENT_NOT_LOCKED")
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        pi.capture(self.fx.root, RUN_ID)
        r = cl.lint_execution(self.fx.root, RUN_ID)
        self.assertEqual((r["status"], r["state"]), ("PASS", "EXECUTION_IN_PROGRESS"), r)
        self.assertEqual(r["checks"], {"VM-001": "NOT_RUN", "VM-002": "NOT_RUN", "VM-003": "NOT_RUN"})
        self.assertEqual(cl.lint_execution(self.fx.root, RUN_ID, require_complete=True)["status"], "FAIL")

        out = rc.run_receipts(self.fx.root, RUN_ID)
        self.assertEqual(out["outcomes"], {"VM-001": "PASS", "VM-002": "PASS", "VM-003": "NOT_RUN"})
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human", "looked fine")
        pi.compare(self.fx.root, RUN_ID)
        r = cl.lint_execution(self.fx.root, RUN_ID, require_complete=True)
        self.assertEqual((r["status"], r["state"], r["postimage"]), ("PASS", "EXECUTION_COMPLETE", "PASS"), r)

    def test_g2_execution_enabled_needs_execution_go(self) -> None:
        (self.fx.run_root / "EXECUTION_MODE.txt").write_text("EXECUTION_ENABLED\n", encoding="utf-8")
        self.fx.write_intent(execution_mode="EXECUTION_ENABLED")
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.assertEqual(cl.lint_execution(self.fx.root, RUN_ID)["state"], "EXECUTION_NOT_AUTHORIZED")
        countersign(self.fx.run_root, "EXECUTION_GO", "intent_pack.json", decision="NO_GO")
        self.assertIn("CONDUCTOR_CONTRACT_COUNTERSIGN_NO_GO", " ".join(cl.lint_execution(self.fx.root, RUN_ID)["errors"]))
        countersign(self.fx.run_root, "EXECUTION_GO", "intent_pack.json")
        self.assertIn("CONDUCTOR_CONTRACT_MANIFEST_MISSING", " ".join(cl.lint_execution(self.fx.root, RUN_ID)["errors"]))

    def test_g2_agent_authored_result_and_tampered_receipt_are_rejected(self) -> None:
        self.lock_and_manifest()
        rc.run_receipts(self.fx.root, RUN_ID, check_ids=["VM-001"])
        # agent edits the receipt to hide a failure
        receipt_path = self.fx.run_root / "receipts" / "VM-001.json"
        receipt = json.loads(receipt_path.read_text())
        receipt["exit_code"] = 0
        receipt["stdout_sha256"] = "b" * 64
        write_json(receipt_path, receipt)
        r = cl.lint_execution(self.fx.root, RUN_ID)
        self.assertIn("CONDUCTOR_CONTRACT_RECEIPT_TAMPERED", " ".join(r["errors"]))
        # agent writes a result block with no receipt behind it
        manifest_path = self.fx.run_root / "verification_manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text())
        manifest["checks"][1]["result"] = {"status": "PASS", "receipt_path": "receipts/VM-002.json"}
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
        r = cl.lint_execution(self.fx.root, RUN_ID)
        self.assertIn("CONDUCTOR_CONTRACT_FILE_MISSING", " ".join(r["errors"]))

    def test_g2_failing_halt_check_and_protected_write_are_errors(self) -> None:
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest(hello_cmd=[sys.executable, "-c", "import sys; sys.exit(3)"])
        pi.capture(self.fx.root, RUN_ID)
        out = rc.run_receipts(self.fx.root, RUN_ID)
        self.assertEqual(out["outcomes"], {"VM-001": "FAIL"}, "halt_on_failure must stop the run")
        r = cl.lint_execution(self.fx.root, RUN_ID)
        self.assertIn("CONDUCTOR_CONTRACT_HALT_ON_FAILURE", " ".join(r["errors"]))
        (self.fx.root / "scripts" / "protected.py").write_text("print('changed')\n", encoding="utf-8")
        cmp = pi.compare(self.fx.root, RUN_ID)
        self.assertEqual((cmp["status"], cmp["changed"]), ("FAIL", ["scripts/protected.py"]))
        self.assertIn("CONDUCTOR_CONTRACT_POSTIMAGE_FAILED", " ".join(cl.lint_execution(self.fx.root, RUN_ID)["errors"]))

    def test_receipts_attest_refuses_non_manual_checks(self) -> None:
        self.lock_and_manifest()
        with self.assertRaises(cl.ContractLintError) as ctx:
            rc.attest(self.fx.root, RUN_ID, "VM-001", "Test Human")
        self.assertEqual(ctx.exception.reason_code, "CONDUCTOR_RECEIPT_ATTEST_NOT_MANUAL")

    # ---- G3
    def complete_g2(self) -> None:
        self.lock_and_manifest()
        pi.capture(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        pi.compare(self.fx.root, RUN_ID)

    def all_verified_rows(self) -> list[dict[str, Any]]:
        return [
            {"requirement_id": "R-001", "status": "verified", "evidence": [self.fx.receipt_ref("VM-001")]},
            {"requirement_id": "R-002", "status": "verified", "evidence": [self.fx.receipt_ref("VM-002")]},
            {"requirement_id": "R-003", "status": "verified", "evidence": [self.fx.receipt_ref("VM-003")]},
        ]

    def test_g3_ready_then_countersigned(self) -> None:
        self.complete_g2()
        self.fx.write_statement(self.all_verified_rows(), "READY")
        r = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertEqual((r["status"], r["state"], r["derived_state"]), ("PASS", "COMPLETION_DRAFT", "READY"), r)
        countersign(self.fx.run_root, "COMPLETION", "statement_of_completion.json")
        r = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertEqual(r["state"], "COMPLETION_COUNTERSIGNED")

    def test_g3_derived_state_is_computed_not_asserted(self) -> None:
        self.complete_g2()
        rows = self.all_verified_rows()
        rows[1] = {"requirement_id": "R-002", "status": "not_done", "evidence": []}
        self.fx.write_statement(rows, "READY")
        r = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertIn("CONDUCTOR_CONTRACT_DERIVED_STATE_MISMATCH", " ".join(r["errors"]))
        self.fx.write_statement(rows, "BLOCKED")
        self.assertEqual(cl.lint_completion(self.fx.root, RUN_ID)["status"], "PASS")

    def test_g3_out_of_scope_needs_a_human_decision_file(self) -> None:
        self.complete_g2()
        rows = self.all_verified_rows()
        rows[2] = {"requirement_id": "R-003", "status": "out_of_scope", "evidence": [], "decision_ref": "notes/verifier.md"}
        self.fx.write_statement(rows, "NEEDS_HUMAN_DECISION")
        self.assertIn("CONDUCTOR_CONTRACT_DECISION_NOT_HUMAN", " ".join(cl.lint_completion(self.fx.root, RUN_ID)["errors"]))
        rows[2]["decision_ref"] = "countersign/INTENT_LOCK.json"
        self.fx.write_statement(rows, "NEEDS_HUMAN_DECISION")
        self.assertEqual(cl.lint_completion(self.fx.root, RUN_ID)["status"], "PASS")

    def test_g3_verified_claim_without_passing_receipt_is_rejected(self) -> None:
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest(hello_cmd=[sys.executable, "-c", "import sys; sys.exit(1)"])
        (self.fx.run_root / "verification_manifest.yaml").write_text(
            yaml.safe_dump({**yaml.safe_load((self.fx.run_root / "verification_manifest.yaml").read_text()), "execution_order": ["VM-002", "VM-003", "VM-001"]}, sort_keys=False))
        manifest = yaml.safe_load((self.fx.run_root / "verification_manifest.yaml").read_text())
        manifest["checks"][0]["halt_on_failure"] = False
        (self.fx.run_root / "verification_manifest.yaml").write_text(yaml.safe_dump(manifest, sort_keys=False))
        pi.capture(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        pi.compare(self.fx.root, RUN_ID)
        self.fx.write_statement(self.all_verified_rows(), "READY")
        r = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertIn("CONDUCTOR_CONTRACT_EVIDENCE_NOT_PASSING", " ".join(r["errors"]))

    def test_g3_row_set_must_match_intent_and_digest_must_match(self) -> None:
        self.complete_g2()
        self.fx.write_statement(self.all_verified_rows()[:2], "READY")
        self.assertIn("CONDUCTOR_CONTRACT_ROW_SET_MISMATCH", " ".join(cl.lint_completion(self.fx.root, RUN_ID)["errors"]))
        self.fx.write_statement(self.all_verified_rows(), "READY")
        statement = json.loads((self.fx.run_root / "statement_of_completion.json").read_text())
        statement["intent_pack_sha256"] = "c" * 64
        write_json(self.fx.run_root / "statement_of_completion.json", statement)
        self.assertIn("CONDUCTOR_CONTRACT_INTENT_DIGEST_MISMATCH", " ".join(cl.lint_completion(self.fx.root, RUN_ID)["errors"]))

    def test_g3_active_scope_gap_with_new_snapshot_reopens_g1(self) -> None:
        self.complete_g2()
        self.fx.write_statement(self.all_verified_rows(), "READY")
        write_json(self.fx.run_root / "gap_requests" / "GAP-001.json", {
            "schema_version": 1, "gap_id": "GAP-001", "run_id": RUN_ID, "intent_pack_sha256": sha(self.fx.run_root / "intent_pack.json"),
            "requirement_id": "R-002", "gap_type": "product_context", "question": "Is the fixture still wanted?",
            "supersession_impact": "active_scope",
            "resolution": {"decided_by": "Test Human", "utc": "2026-09-04T21:30:00Z", "decision": "replace", "new_snapshot_id": "SNAP-2", "new_snapshot_sha256": "d" * 64},
        })
        r = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertIn("CONDUCTOR_CONTRACT_G1_REOPEN_REQUIRED", " ".join(r["errors"]))

    def test_g3_merge_ready_requires_merge_preflight_summary(self) -> None:
        self.complete_g2()
        self.fx.write_statement(self.all_verified_rows(), "READY", handoff="MERGE_READY")
        self.assertEqual(cl.lint_completion(self.fx.root, RUN_ID)["status"], "FAIL", "schema requires merge_preflight_summary")
        statement_path = self.fx.run_root / "statement_of_completion.json"
        statement = json.loads(statement_path.read_text())
        summary = self.fx.root / "artifacts" / "merge_preflight" / "SUMMARY.md"
        summary.parent.mkdir(parents=True)
        summary.write_text("- Verdict: NOT_MERGE_READY\n", encoding="utf-8")
        statement["merge_preflight_summary"] = "artifacts/merge_preflight/SUMMARY.md"
        write_json(statement_path, statement)
        self.assertIn("CONDUCTOR_CONTRACT_MERGE_READY_UNPROVEN", " ".join(cl.lint_completion(self.fx.root, RUN_ID)["errors"]))
        summary.write_text("- Verdict: MERGE_READY\n", encoding="utf-8")
        self.assertEqual(cl.lint_completion(self.fx.root, RUN_ID)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
