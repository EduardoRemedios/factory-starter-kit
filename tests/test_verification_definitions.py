"""Separate approved check definitions from runner-owned results before effects."""
from __future__ import annotations

import copy
import json
import os
import sys
import unittest
from pathlib import Path

import yaml

from tests.test_contract_lint import Fixture, RUN_ID, cl, countersign, pi, rc, sha, write_json


class VerificationDefinitionsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)
        self.fx.write_manifest(hello_cmd=[sys.executable, "-c", "from pathlib import Path; Path('executed').write_text('yes')"])
        self.manifest_path = self.fx.run_root / "verification_manifest.yaml"
        self.definitions_path = self.fx.run_root / "verification_definitions.json"
        self.intent_path = self.fx.run_root / "intent_pack.json"

    def pin(self, path: Path, ref: str | None = None, kind: str = "spec") -> None:
        intent = json.loads(self.intent_path.read_text())
        intent["sources"].append({"kind": kind, "ref": ref or path.relative_to(self.fx.root).as_posix(), "sha256": sha(path)})
        write_json(self.intent_path, intent)
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")

    def freeze(self) -> None:
        document = yaml.safe_load(self.manifest_path.read_text())
        for check in document["checks"]:
            check.pop("result", None)
        write_json(self.definitions_path, document)
        self.pin(self.definitions_path)

    def tree_bytes(self) -> dict[str, bytes]:
        return {path.relative_to(self.fx.root).as_posix(): path.read_bytes()
                for path in self.fx.root.rglob("*") if path.is_file()}

    def assert_blocked(self, reason: str) -> None:
        result = cl.lint_intent(self.fx.root, RUN_ID)
        self.assertEqual(result["status"], "FAIL", result)
        self.assertIn(reason, " ".join(result["errors"]))
        self.assert_effects_blocked(reason)

    def assert_effects_blocked(self, reason: str) -> None:
        before = self.tree_bytes()
        for invoke in (lambda: rc.run_receipts(self.fx.root, RUN_ID, ["VM-001"]),
                       lambda: rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")):
            with self.assertRaises(cl.ContractLintError) as ctx:
                invoke()
            self.assertIn(reason, str(ctx.exception))
            self.assertEqual(self.tree_bytes(), before, "rejected calls must not run the sentinel or mutate evidence")

    def test_current_manifest_pin_is_rejected_before_execution_and_attestation(self) -> None:
        self.pin(self.manifest_path)
        self.assert_blocked("CONDUCTOR_CONTRACT_MUTABLE_MANIFEST_SOURCE")

    def test_normalized_alias_cannot_pin_mutable_manifest(self) -> None:
        ref = self.manifest_path.relative_to(self.fx.root).as_posix().replace("/verification_", "/./verification_")
        self.pin(self.manifest_path, ref=ref)
        self.assert_blocked("CONDUCTOR_CONTRACT_MUTABLE_MANIFEST_SOURCE")

    def test_hardlink_alias_cannot_pin_mutable_manifest(self) -> None:
        alias = self.fx.run_root / "notes" / "looks-immutable.json"
        os.link(self.manifest_path, alias)
        self.pin(alias)
        self.assert_blocked("CONDUCTOR_CONTRACT_MUTABLE_MANIFEST_SOURCE")

    def test_historical_manifest_copy_is_allowed(self) -> None:
        archived = self.fx.root / "docs/Conductor/runs/RUN_prior/verification_manifest.yaml"
        archived.parent.mkdir()
        archived.write_bytes(self.manifest_path.read_bytes())
        self.pin(archived, kind="prior_run")
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["status"], "PASS")
        rc.run_receipts(self.fx.root, RUN_ID, ["VM-001"])
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["status"], "PASS")

    def test_results_rerun_attestation_and_reformatting_preserve_locked_intent(self) -> None:
        self.freeze()
        immutable = self.definitions_path.read_bytes()
        intent_digest = sha(self.intent_path)
        pi.capture(self.fx.root, RUN_ID)
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["state"], "INTENT_LOCKED")
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID, ["VM-001"])
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        document = yaml.safe_load(self.manifest_path.read_text())
        self.manifest_path.write_text(json.dumps(document, indent=4, sort_keys=True))
        pi.compare(self.fx.root, RUN_ID)
        result = cl.lint_execution(self.fx.root, RUN_ID, require_complete=True)
        self.assertEqual((result["status"], result["state"]), ("PASS", "EXECUTION_COMPLETE"), result)
        self.assertEqual(self.definitions_path.read_bytes(), immutable)
        self.assertEqual(sha(self.intent_path), intent_digest)

    def test_every_definition_change_is_rejected_before_effects(self) -> None:
        self.freeze()
        original = yaml.safe_load(self.manifest_path.read_text())
        changes = {
            "command": lambda m: m["checks"][0].update(command=[sys.executable, "-c", "print('different')"]),
            "expected_exit": lambda m: m["checks"][0].update(expected_exit=7),
            "requirements": lambda m: m["checks"][0].update(requirement_ids=["R-002"]),
            "halt": lambda m: m["checks"][0].update(halt_on_failure=False),
            "description": lambda m: m["checks"][0].update(description="Different acceptance intent"),
            "tier": lambda m: m["checks"][0].update(tier="V1"),
            "type": lambda m: m["checks"][0].update(type="test"),
            "target": lambda m: m["checks"][1].update(target="another.txt"),
            "evidence": lambda m: m["checks"][0].update(evidence_path="receipts/elsewhere.json"),
            "expected": lambda m: m["checks"][2].update(expected="No review required"),
            "order": lambda m: m["execution_order"].reverse(),
            "check_order": lambda m: m["checks"].reverse(),
            "remove": lambda m: m["checks"].pop(),
            "add": lambda m: m["checks"].append({**m["checks"][0], "id": "VM-004"}),
            "mode": lambda m: m.update(execution_mode="EXECUTION_ENABLED"),
            "run": lambda m: m.update(run_id="RUN_other"),
        }
        for name, mutate in changes.items():
            with self.subTest(name=name):
                document = copy.deepcopy(original)
                mutate(document)
                self.manifest_path.write_text(yaml.safe_dump(document))
                self.assert_blocked("CONDUCTOR_CONTRACT_DEFINITIONS_MISMATCH")

    def test_changed_snapshot_digest_is_rejected(self) -> None:
        self.freeze()
        document = json.loads(self.definitions_path.read_text())
        document["checks"][0]["description"] = "Different"
        write_json(self.definitions_path, document)
        self.assert_blocked("CONDUCTOR_CONTRACT_SOURCE_DIGEST_MISMATCH")

    def test_definition_changes_during_a_check_are_not_overwritten_or_executed_next(self) -> None:
        command = [sys.executable, "-c",
                   "import json, pathlib, yaml; p = pathlib.Path(" + repr(str(self.manifest_path)) + "); "
                   "m = yaml.safe_load(p.read_text()); m['checks'][1]['description'] = 'changed during check'; "
                   "p.write_text(json.dumps(m))"]
        self.fx.write_manifest(hello_cmd=command)
        self.freeze()
        original = self.manifest_path.read_bytes()
        for selected in (["VM-001"], None):
            with self.subTest(selected=selected):
                self.manifest_path.write_bytes(original)
                with self.assertRaises(cl.ContractLintError) as ctx:
                    rc.run_receipts(self.fx.root, RUN_ID, selected)
                self.assertIn("CONDUCTOR_CONTRACT_DEFINITIONS_MISMATCH", str(ctx.exception))
                current = json.loads(self.manifest_path.read_text())
                self.assertEqual(current["checks"][1]["description"], "changed during check")
                self.assertTrue((self.fx.run_root / "receipts/VM-001.json").exists(), "retain evidence of the already-run check")
                self.assertFalse((self.fx.run_root / "receipts/VM-002.json").exists(), "do not run the next check")

    def test_missing_snapshot_is_rejected(self) -> None:
        self.freeze()
        self.definitions_path.unlink()
        self.assert_blocked("CONDUCTOR_CONTRACT_SOURCE_MISSING")

    def test_missing_manifest_is_rejected(self) -> None:
        self.freeze()
        self.manifest_path.unlink()
        self.assert_blocked("CONDUCTOR_CONTRACT_FILE_MISSING")

    def test_unpinned_snapshot_is_rejected(self) -> None:
        write_json(self.definitions_path, yaml.safe_load(self.manifest_path.read_text()))
        self.assert_blocked("CONDUCTOR_CONTRACT_DEFINITIONS_UNPINNED")

    def test_wrong_source_kind_does_not_activate_snapshot(self) -> None:
        write_json(self.definitions_path, yaml.safe_load(self.manifest_path.read_text()))
        self.pin(self.definitions_path, kind="human_brief")
        self.assert_blocked("CONDUCTOR_CONTRACT_DEFINITIONS_UNPINNED")

    def test_symlink_snapshot_is_rejected(self) -> None:
        self.freeze()
        moved = self.fx.run_root / "notes" / "moved.json"
        self.definitions_path.rename(moved)
        self.definitions_path.symlink_to(moved)
        self.assert_blocked("CONDUCTOR_CONTRACT_UNSAFE_PATH")

    def test_invalid_or_result_bearing_snapshot_is_rejected(self) -> None:
        original = yaml.safe_load(self.manifest_path.read_text())
        for snapshot in (None, {}, {**original, "checks": [{**original["checks"][0], "result": {
                "status": "NOT_RUN", "receipt_path": "receipts/VM-001.json"}}, *original["checks"][1:]]}):
            with self.subTest(snapshot=snapshot):
                self.fx.write_intent()
                write_json(self.definitions_path, snapshot)
                self.pin(self.definitions_path)
                self.assert_blocked("CONDUCTOR_CONTRACT_DEFINITIONS_INVALID")

    def test_unpinned_legacy_run_retains_existing_result_behavior(self) -> None:
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["state"], "INTENT_LOCKED")

    def test_legacy_manifest_only_runner_and_attestation_remain_supported(self) -> None:
        self.intent_path.unlink()
        self.assertEqual(rc.run_receipts(self.fx.root, RUN_ID)["outcomes"]["VM-001"], "PASS")
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        self.assertEqual(yaml.safe_load(self.manifest_path.read_text())["checks"][2]["result"]["status"], "PASS")

    def test_orphan_snapshot_does_not_allow_manifest_only_execution(self) -> None:
        self.freeze()
        self.intent_path.unlink()
        self.assert_blocked("CONDUCTOR_CONTRACT_FILE_MISSING")

    def enable_execution(self) -> None:
        self.fx.write_intent(execution_mode="EXECUTION_ENABLED")
        (self.fx.run_root / "EXECUTION_MODE.txt").write_text("EXECUTION_ENABLED\n")
        manifest = yaml.safe_load(self.manifest_path.read_text())
        manifest["execution_mode"] = "EXECUTION_ENABLED"
        self.manifest_path.write_text(yaml.safe_dump(manifest))
        self.freeze()

    def test_repinning_changed_definitions_requires_renewed_approval(self) -> None:
        self.freeze()
        approved_lock = (self.fx.run_root / "countersign/INTENT_LOCK.json").read_bytes()
        manifest = yaml.safe_load(self.manifest_path.read_text())
        manifest["checks"][0]["command"] = [sys.executable, "-c", "from pathlib import Path; Path('unapproved').touch()"]
        self.manifest_path.write_text(yaml.safe_dump(manifest))
        write_json(self.definitions_path, manifest)
        intent = json.loads(self.intent_path.read_text())
        intent["sources"][-1]["sha256"] = sha(self.definitions_path)
        write_json(self.intent_path, intent)
        self.assertEqual((self.fx.run_root / "countersign/INTENT_LOCK.json").read_bytes(), approved_lock)
        self.assert_blocked("CONDUCTOR_CONTRACT_COUNTERSIGN_STALE")
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.assertEqual(rc.run_receipts(self.fx.root, RUN_ID, ["VM-001"])["outcomes"]["VM-001"], "PASS")
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")

    def test_frozen_definitions_require_intent_lock_before_effects(self) -> None:
        self.freeze()
        (self.fx.run_root / "countersign/INTENT_LOCK.json").unlink()
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["state"], "INTENT_DRAFT")
        self.assert_effects_blocked("CONDUCTOR_RECEIPT_APPROVAL_REQUIRED: INTENT_LOCK")

    def test_frozen_definitions_require_execution_go_when_enabled(self) -> None:
        self.enable_execution()
        self.assert_effects_blocked("CONDUCTOR_RECEIPT_APPROVAL_REQUIRED: EXECUTION_GO")
        countersign(self.fx.run_root, "EXECUTION_GO", "intent_pack.json")
        self.assertEqual(rc.run_receipts(self.fx.root, RUN_ID)["outcomes"]["VM-001"], "PASS")
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")

    def test_stale_execution_go_is_rejected_even_with_current_g1(self) -> None:
        self.enable_execution()
        countersign(self.fx.run_root, "EXECUTION_GO", "intent_pack.json")
        intent = json.loads(self.intent_path.read_text())
        intent["goal"] += " Revised scope."
        write_json(self.intent_path, intent)
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.assertEqual(cl.lint_intent(self.fx.root, RUN_ID)["state"], "INTENT_LOCKED")
        self.assert_effects_blocked("CONDUCTOR_CONTRACT_COUNTERSIGN_STALE")
        countersign(self.fx.run_root, "EXECUTION_GO", "intent_pack.json")
        self.assertEqual(rc.run_receipts(self.fx.root, RUN_ID, ["VM-001"])["outcomes"]["VM-001"], "PASS")
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")

    def test_rejected_execution_go_is_rejected_before_effects(self) -> None:
        self.enable_execution()
        countersign(self.fx.run_root, "EXECUTION_GO", "intent_pack.json", decision="NO_GO")
        self.assert_effects_blocked("CONDUCTOR_CONTRACT_COUNTERSIGN_NO_GO")

    def test_symlink_approval_is_rejected_for_frozen_definitions(self) -> None:
        self.freeze()
        approval = self.fx.run_root / "countersign/INTENT_LOCK.json"
        moved = self.fx.run_root / "notes/moved-approval.json"
        approval.rename(moved)
        approval.symlink_to(moved)
        self.assert_effects_blocked("CONDUCTOR_CONTRACT_UNSAFE_PATH")


if __name__ == "__main__":
    unittest.main()
