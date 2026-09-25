"""Receipt consistency and v1 compatibility, without claiming writer authentication."""
from __future__ import annotations

import json
import shlex
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import yaml

from tests.test_contract_lint import Fixture, RUN_ID, cl, countersign, pi, rc, write_json


class ReceiptIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture()
        self.addCleanup(self.fx.cleanup)
        countersign(self.fx.run_root, "INTENT_LOCK", "intent_pack.json")
        self.fx.write_manifest()
        pi.capture(self.fx.root, RUN_ID)
        rc.run_receipts(self.fx.root, RUN_ID)
        rc.attest(self.fx.root, RUN_ID, "VM-003", "Test Human")
        pi.compare(self.fx.root, RUN_ID)

    def receipt(self, check_id="VM-001"):
        return json.loads((self.fx.run_root / "receipts" / f"{check_id}.json").read_text())

    def replace_receipt(self, receipt):
        receipt["payload_sha256"] = cl.receipt_payload_digest(receipt)
        write_json(self.fx.run_root / "receipts" / f"{receipt['check_id']}.json", receipt)

    def execution(self):
        return cl.lint_execution(self.fx.root, RUN_ID, require_complete=True)

    def assert_rejected(self, reason):
        result = self.execution()
        self.assertEqual("FAIL", result["status"], result)
        self.assertIn(reason, " ".join(result["errors"]), result)

    def test_existing_v1_command_artifact_and_manual_receipts_still_pass(self):
        self.assertEqual("EXECUTION_COMPLETE", self.execution()["state"])
        # expected_exit and result metadata were optional in the original schemas.
        receipt = self.receipt()
        del receipt["expected_exit"]
        self.replace_receipt(receipt)
        manifest_path = self.fx.run_root / "verification_manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text())
        for check in manifest["checks"]:
            check["result"].pop("exit_code")
            check["result"].pop("utc")
        manifest_path.write_text(yaml.safe_dump(manifest))
        self.assertEqual("EXECUTION_COMPLETE", self.execution()["state"])

    def test_changed_logs_are_rejected_even_without_a_receipt_edit(self):
        receipt = self.receipt()
        for stream, content in (("stdout", b"HELLO\n"), ("stdout", b""), ("stderr", b"error"), ("stdout", b"x" * 65537)):
            with self.subTest(stream=stream, size=len(content)):
                log = self.fx.run_root / receipt[f"{stream}_path"]
                original = log.read_bytes()
                log.write_bytes(content)
                self.assert_rejected("CONDUCTOR_CONTRACT_RECEIPT_LOG_MISMATCH")
                log.write_bytes(original)

    def test_recomputed_payload_does_not_hide_wrong_log_digest_or_size(self):
        original = self.receipt()
        for field, value in (("stdout_sha256", "b" * 64), ("stdout_bytes", 0), ("stderr_bytes", 1)):
            with self.subTest(field=field):
                self.replace_receipt({**original, field: value})
                self.assert_rejected("CONDUCTOR_CONTRACT_RECEIPT_LOG_MISMATCH")

    def test_missing_symlink_and_unreadable_logs_fail_closed(self):
        receipt = self.receipt()
        log = self.fx.run_root / receipt["stdout_path"]
        original = log.read_bytes()
        log.unlink()
        self.assert_rejected("CONDUCTOR_CONTRACT_FILE_MISSING")
        log.symlink_to(self.fx.run_root / "notes/fixture.txt")
        self.assert_rejected("CONDUCTOR_CONTRACT_UNSAFE_PATH")
        log.unlink()
        log.write_bytes(original)
        original_open = Path.open

        def deny_log(path, *args, **kwargs):
            if path.resolve() == log.resolve():
                raise PermissionError("fixture permission denied")
            return original_open(path, *args, **kwargs)

        with patch.object(Path, "open", deny_log):
            self.assert_rejected("CONDUCTOR_CONTRACT_RECEIPT_LOG_UNREADABLE")

    def test_recomputed_payload_does_not_hide_inconsistent_outcomes(self):
        original = self.receipt()
        for field, value in (("exit_code", 9), ("expected_exit", 9)):
            with self.subTest(field=field):
                self.replace_receipt({**original, field: value})
                self.assert_rejected("CONDUCTOR_CONTRACT_RECEIPT_OUTCOME_MISMATCH")

    def test_optional_manifest_metadata_must_agree_when_present(self):
        path = self.fx.run_root / "verification_manifest.yaml"
        original = path.read_text()
        for field, value in (("exit_code", 9), ("utc", "2026-09-01T00:00:00Z")):
            with self.subTest(field=field):
                manifest = yaml.safe_load(original)
                manifest["checks"][0]["result"][field] = value
                path.write_text(yaml.safe_dump(manifest))
                self.assert_rejected("CONDUCTOR_CONTRACT_RESULT_MISMATCH")

    def test_receipts_must_match_command_target_manual_kind_and_cwd(self):
        for check_id, field, value in (("VM-001", "command", ["different"]), ("VM-001", "cwd", "elsewhere"),
                                      ("VM-002", "command", ["conductor-receipts", "target-exists", "different"]),
                                      ("VM-003", "command", ["conductor-receipts", "human-attestation", ""])):
            with self.subTest(check_id=check_id, field=field):
                original = self.receipt(check_id)
                self.replace_receipt({**original, field: value})
                self.assert_rejected("CONDUCTOR_CONTRACT_RECEIPT_COMMAND_MISMATCH")
                self.replace_receipt(original)

    def test_quoted_command_and_nonzero_expected_exit_remain_supported(self):
        path = self.fx.run_root / "verification_manifest.yaml"
        manifest = yaml.safe_load(path.read_text())
        manifest["checks"][0]["command"] = shlex.join([sys.executable, "-c", "import sys; sys.exit(7)"])
        manifest["checks"][0]["expected_exit"] = 7
        path.write_text(yaml.safe_dump(manifest))
        rc.run_receipts(self.fx.root, RUN_ID, check_ids=["VM-001"])
        self.assertEqual("EXECUTION_COMPLETE", self.execution()["state"])

    def test_g3_rechecks_logs_after_statement_and_countersign(self):
        rows = [{"requirement_id": f"R-00{i}", "status": "verified", "evidence": [self.fx.receipt_ref(f"VM-00{i}")]}
                for i in range(1, 4)]
        self.fx.write_statement(rows, "READY")
        countersign(self.fx.run_root, "COMPLETION", "statement_of_completion.json")
        self.assertEqual("COMPLETION_COUNTERSIGNED", cl.lint_completion(self.fx.root, RUN_ID)["state"])
        (self.fx.run_root / self.receipt()["stdout_path"]).write_bytes(b"HELLO\n")
        result = cl.lint_completion(self.fx.root, RUN_ID)
        self.assertEqual("FAIL", result["status"])
        self.assertIn("CONDUCTOR_CONTRACT_RECEIPT_LOG_MISMATCH", " ".join(result["errors"]))

    def test_coordinated_rewrite_documents_checksum_authentication_limit(self):
        # A writer who controls both logs and digests can keep them consistent.
        # This deliberately passing case prevents calling a checksum a signature.
        receipt = self.receipt()
        content = b"coordinated replacement\n"
        (self.fx.run_root / receipt["stdout_path"]).write_bytes(content)
        receipt["stdout_sha256"] = cl.sha256_bytes(content)
        receipt["stdout_bytes"] = len(content)
        self.replace_receipt(receipt)
        self.assertEqual("EXECUTION_COMPLETE", self.execution()["state"])


if __name__ == "__main__":
    unittest.main()
