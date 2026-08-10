from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


CLOSEOUT = load_module(
    "factory_execution_closeout",
    REPO_ROOT / "scripts/factory_execution_closeout.py",
)
RUNTIME = load_module(
    "factory_plugin_runtime_closeout",
    REPO_ROOT / "plugin-src/factory/runtime/factory_plugin.py",
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, value: dict) -> None:
    write(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


class ExecutionCloseoutTests(unittest.TestCase):
    def make_root(self) -> Path:
        root = Path(self.temp_dir.name)
        validator = root / "scripts/factory_execution_closeout.py"
        validator.parent.mkdir(parents=True)
        shutil.copyfile(REPO_ROOT / "scripts/factory_execution_closeout.py", validator)
        return root

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = self.make_root()

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def make_run(self, run_id: str = "RUN_20260805_0000_fixture") -> Path:
        run_root = self.root / "docs/Factory/runs" / run_id
        write(run_root / "KNOWLEDGE_LINT.txt", "knowledge_lint: PASS\n")
        write(run_root / "EXECUTION_MODE.txt", "EXECUTION_ENABLED\n")
        write(run_root / "EXECUTION_PROMPT.md", "- Human Go: RECORDED\n")
        write(run_root / "EXECUTION_AUTHORIZATION.md", "authorized\n")
        write(run_root / "SPRINT_ID.txt", "SPRINT_20260805_001\n")
        write(run_root / "pack/PACK_AUDIT_REPORT.md", "- Verdict: PASS\n")
        write(run_root / "pack/PACK_MANIFEST.md", "manifest\n")
        write(run_root / "pack/micro_sprints.md", "## MS-00 — Freeze\n## MS-01 — Build\n")
        write(
            run_root / "pack/verification_manifest.yaml",
            "checks:\n  - id: VM-001\n  - id: VM-002\n",
        )
        for stage in RUNTIME.STAGE_ORDER:
            write(
                run_root / "pack/HANDOFF" / f"HANDOFF_STAGE_{stage}.md",
                "## Outputs Produced (paths)\n\n## Exit Criteria Status\n- PASS\n",
            )
        evidence_root = self.root / "artifacts" / run_id
        write(evidence_root / "VM-001.txt", "pass one\n")
        write(evidence_root / "VM-002.txt", "pass two\n")
        write(evidence_root / "receipt.json", "receipt\n")
        return run_root

    def draft(self, run_root: Path, outcome: str = "REVIEW_READY") -> dict:
        rules = {
            "REVIEW_READY": (
                "FACTORY_EXECUTION_REVIEW_READY",
                "review_the_retained_clean_worktree",
                ["PASS", "PASS"],
            ),
            "NO_GO": (
                "FACTORY_EXECUTION_NO_GO",
                "review_failed_verification_evidence",
                ["PASS", "FAIL"],
            ),
            "BLOCKED": (
                "FACTORY_EXECUTION_BLOCKED",
                "resolve_the_recorded_blocker",
                ["PASS", "NOT_RUN"],
            ),
        }
        reason, action, statuses = rules[outcome]
        evidence_root = self.root / "artifacts" / run_root.name
        results = []
        for index, status in enumerate(statuses, start=1):
            path = evidence_root / f"VM-00{index}.txt"
            results.append(
                {
                    "id": f"VM-00{index}",
                    "status": status,
                    "evidence_path": path.relative_to(self.root).as_posix(),
                    "sha256": CLOSEOUT.sha256_file(path),
                    "blocker": None if status == "PASS" else "EXACT_TEST_BLOCKER",
                }
            )
        receipt = evidence_root / "receipt.json"
        return {
            "schema": CLOSEOUT.SCHEMA,
            "run_id": run_root.name,
            "sprint_id": "SPRINT_20260805_001",
            "execution_mode": "EXECUTION_ENABLED",
            "outcome": outcome,
            "reason_code": reason,
            "next_legal_action": action,
            "authority_grants": [],
            "pack_manifest": {
                "path": "pack/PACK_MANIFEST.md",
                "sha256": CLOSEOUT.sha256_file(run_root / "pack/PACK_MANIFEST.md"),
            },
            "execution_authorization": {
                "path": "EXECUTION_AUTHORIZATION.md",
                "sha256": CLOSEOUT.sha256_file(run_root / "EXECUTION_AUTHORIZATION.md"),
            },
            "micro_sprints": {
                "path": "pack/micro_sprints.md",
                "sha256": CLOSEOUT.sha256_file(run_root / "pack/micro_sprints.md"),
            },
            "verification_manifest": {
                "path": "pack/verification_manifest.yaml",
                "sha256": CLOSEOUT.sha256_file(run_root / "pack/verification_manifest.yaml"),
            },
            "completed_micro_sprints": ["MS-00", "MS-01"],
            "verification_results": results,
            "retained_evidence": [
                {
                    "id": "WORKTREE_RECEIPT",
                    "path": receipt.relative_to(self.root).as_posix(),
                    "sha256": CLOSEOUT.sha256_file(receipt),
                }
            ],
        }

    def record(self, run_root: Path, draft: dict) -> dict:
        input_path = self.root / f"{run_root.name}-draft.json"
        write_json(input_path, draft)
        return CLOSEOUT.record_closeout(self.root, run_root.name, input_path)

    def assert_invalid(self, run_root: Path, draft: dict, reason: str) -> None:
        with self.assertRaises(CLOSEOUT.ExecutionCloseoutError) as caught:
            CLOSEOUT.validate_closeout(self.root, run_root.name, draft)
        self.assertEqual(reason, caught.exception.reason_code)

    def test_ec01_valid_review_ready_and_idempotent_record(self):
        run = self.make_run()
        draft = self.draft(run)
        first = self.record(run, draft)
        second = self.record(run, draft)
        self.assertEqual([f"docs/Factory/runs/{run.name}/EXECUTION_CLOSEOUT.json"], first["mutations"])
        self.assertEqual([], second["mutations"])
        self.assertEqual("REVIEW_READY", RUNTIME.evaluate_progress(self.root, run_id=run.name)["state"])

    def test_ec02_valid_no_go(self):
        run = self.make_run()
        self.record(run, self.draft(run, "NO_GO"))
        output = RUNTIME.evaluate_progress(self.root, run_id=run.name)
        self.assertEqual("NO_GO", output["state"])
        self.assertEqual("FACTORY_EXECUTION_NO_GO", output["reason_code"])

    def test_ec03_valid_blocked(self):
        run = self.make_run()
        self.record(run, self.draft(run, "BLOCKED"))
        self.assertEqual("BLOCKED", RUNTIME.evaluate_progress(self.root, run_id=run.name)["state"])

    def test_ec04_legacy_absence_preserves_authorized_state(self):
        run = self.make_run()
        output = RUNTIME.evaluate_progress(self.root, run_id=run.name)
        self.assertEqual("AUTHORIZED_FOR_EXECUTION", output["state"])
        self.assertEqual("FACTORY_HUMAN_GO_RECORDED", output["reason_code"])

    def test_ec05_malformed_unknown_and_duplicate_ids_fail(self):
        run = self.make_run()
        malformed = run / CLOSEOUT.CLOSEOUT_NAME
        write(malformed, "{invalid")
        output = RUNTIME.evaluate_progress(self.root, run_id=run.name)
        self.assertEqual("FACTORY_EXECUTION_CLOSEOUT_INVALID", output["reason_code"])
        malformed.unlink()
        write(malformed, '{"schema":"one","schema":"two"}')
        output = RUNTIME.evaluate_progress(self.root, run_id=run.name)
        self.assertEqual(
            "FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID", output["blocker"]
        )
        malformed.unlink()
        unknown = self.draft(run)
        unknown["unknown"] = True
        self.assert_invalid(run, unknown, "FACTORY_EXECUTION_CLOSEOUT_SCHEMA_INVALID")
        duplicate = self.draft(run)
        duplicate["verification_results"][1]["id"] = "VM-001"
        self.assert_invalid(run, duplicate, "FACTORY_EXECUTION_CLOSEOUT_DUPLICATE_ID")

    def test_ec06_wrong_run_or_sprint_fails(self):
        run = self.make_run()
        wrong_run = self.draft(run)
        wrong_run["run_id"] = "RUN_20260805_9999_wrong"
        self.assert_invalid(run, wrong_run, "FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH")
        wrong_sprint = self.draft(run)
        wrong_sprint["sprint_id"] = "SPRINT_20260805_999"
        self.assert_invalid(run, wrong_sprint, "FACTORY_EXECUTION_CLOSEOUT_IDENTITY_MISMATCH")

    def test_ec07_wrong_pack_or_authorization_digest_fails(self):
        run = self.make_run()
        for field in ("pack_manifest", "execution_authorization"):
            draft = self.draft(run)
            draft[field]["sha256"] = "0" * 64
            self.assert_invalid(run, draft, "FACTORY_EXECUTION_CLOSEOUT_PIN_MISMATCH")

    def test_ec08_missing_or_unsafe_evidence_fails(self):
        run = self.make_run()
        missing = self.draft(run)
        missing["verification_results"][0]["evidence_path"] = "artifacts/missing.txt"
        self.assert_invalid(run, missing, "FACTORY_EXECUTION_CLOSEOUT_EVIDENCE_MISSING")
        unsafe = self.draft(run)
        unsafe["verification_results"][0]["evidence_path"] = "../outside.txt"
        self.assert_invalid(run, unsafe, "FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH")
        link = self.root / "artifacts" / run.name / "linked.txt"
        link.symlink_to(self.root / "artifacts" / run.name / "VM-001.txt")
        symlinked = self.draft(run)
        symlinked["verification_results"][0]["evidence_path"] = link.relative_to(self.root).as_posix()
        self.assert_invalid(run, symlinked, "FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH")

    def test_symlinked_run_root_ancestors_block_validation_and_recording(self):
        for ancestor in ("docs", "docs/Factory", "docs/Factory/runs"):
            with self.subTest(ancestor=ancestor), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                original_root = self.root
                try:
                    self.root = base / "repo"
                    self.root.mkdir()
                    run = self.make_run()
                    draft = self.draft(run)
                    input_path = self.root / "closeout-draft.json"
                    write_json(input_path, draft)

                    linked_ancestor = self.root / ancestor
                    outside_ancestor = base / "outside" / Path(ancestor).name
                    outside_ancestor.parent.mkdir(parents=True)
                    run_below_ancestor = run.relative_to(linked_ancestor)
                    linked_ancestor.rename(outside_ancestor)
                    linked_ancestor.symlink_to(outside_ancestor, target_is_directory=True)
                    outside_record = (
                        outside_ancestor / run_below_ancestor / CLOSEOUT.CLOSEOUT_NAME
                    )

                    with self.assertRaises(CLOSEOUT.ExecutionCloseoutError) as validate_error:
                        CLOSEOUT.validate_closeout(self.root, run.name, draft)
                    self.assertEqual(
                        "FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH",
                        validate_error.exception.reason_code,
                    )
                    self.assertFalse(outside_record.exists())

                    with self.assertRaises(CLOSEOUT.ExecutionCloseoutError) as record_error:
                        CLOSEOUT.record_closeout(self.root, run.name, input_path)
                    self.assertEqual(
                        "FACTORY_EXECUTION_CLOSEOUT_UNSAFE_PATH",
                        record_error.exception.reason_code,
                    )
                    self.assertFalse(outside_record.exists())
                finally:
                    self.root = original_root

    def test_ec09_evidence_drift_blocks_progress(self):
        run = self.make_run()
        self.record(run, self.draft(run))
        write(self.root / "artifacts" / run.name / "VM-001.txt", "drift\n")
        output = RUNTIME.evaluate_progress(self.root, run_id=run.name)
        self.assertEqual("BLOCKED", output["state"])
        self.assertEqual("FACTORY_EXECUTION_CLOSEOUT_EVIDENCE_DIGEST_MISMATCH", output["blocker"])

    def test_ec10_incomplete_or_duplicate_micro_sprints_fail(self):
        run = self.make_run()
        incomplete = self.draft(run)
        incomplete["completed_micro_sprints"] = ["MS-00"]
        self.assert_invalid(run, incomplete, "FACTORY_EXECUTION_CLOSEOUT_MICRO_SPRINT_MISMATCH")
        duplicate = self.draft(run)
        duplicate["completed_micro_sprints"] = ["MS-00", "MS-00"]
        self.assert_invalid(run, duplicate, "FACTORY_EXECUTION_CLOSEOUT_DUPLICATE_ID")

    def test_ec11_outcome_evidence_contradiction_fails(self):
        run = self.make_run()
        draft = self.draft(run)
        draft["verification_results"][1]["status"] = "FAIL"
        draft["verification_results"][1]["blocker"] = "FAILED"
        self.assert_invalid(run, draft, "FACTORY_EXECUTION_CLOSEOUT_OUTCOME_CONTRADICTION")

    def test_ec12_closeout_cannot_grant_authority(self):
        run = self.make_run()
        draft = self.draft(run)
        draft["authority_grants"] = ["release"]
        self.assert_invalid(run, draft, "FACTORY_EXECUTION_CLOSEOUT_AUTHORITY_VIOLATION")

    def test_explicit_and_default_run_selection_are_distinct(self):
        older = self.make_run("RUN_20260805_0001_closed")
        self.record(older, self.draft(older))
        newer = self.make_run("RUN_20260805_0002_active")
        explicit = RUNTIME.evaluate_progress(self.root, run_id=older.name)
        default = RUNTIME.evaluate_progress(self.root)
        self.assertEqual("REVIEW_READY", explicit["state"])
        self.assertEqual(older.name, explicit["run_id"])
        self.assertEqual("AUTHORIZED_FOR_EXECUTION", default["state"])
        self.assertEqual(newer.name, default["run_id"])


if __name__ == "__main__":
    unittest.main()
