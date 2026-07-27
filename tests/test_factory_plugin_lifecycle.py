import hashlib
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_factory_plugin_status import inventory, write


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_PATH = REPO_ROOT / "plugin-src/factory/runtime/factory_plugin.py"
SPEC = importlib.util.spec_from_file_location("factory_plugin_lifecycle_runtime", RUNTIME_PATH)
RUNTIME = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(RUNTIME)


def make_payload(
    root: Path, version: str, files: dict[str, tuple[str, str]]
) -> Path:
    payload = root / f"payload-{version}"
    entries = []
    for relative, (content, classification) in sorted(files.items()):
        write(payload / relative, content)
        entries.append(
            {
                "path": relative,
                "classification": classification,
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
            }
        )
    write(
        payload / "OWNERSHIP.json",
        json.dumps(
            {
                "schema_version": 1,
                "package": "factory",
                "version": version,
                "files": entries,
            },
            indent=2,
        )
        + "\n",
    )
    return payload


def setup_plan(root: Path, payload: Path):
    return RUNTIME.evaluate_setup_plan(
        root,
        mode="brownfield",
        harness="codex",
        payload_root=payload,
        platform_name="darwin",
        python_version=(3, 11, 0),
    )


def update_plan(root: Path, payload: Path):
    return RUNTIME.evaluate_update_plan(
        root,
        harness="codex",
        payload_root=payload,
        platform_name="darwin",
        python_version=(3, 11, 0),
    )


class FactoryPluginLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.v1 = make_payload(
            self.base,
            "0.1.0",
            {
                "AGENTS.md": ("starter instructions\n", "project-owned"),
                "docs/Factory/core.md": ("factory v1\n", "release-owned"),
            },
        )
        self.v2 = make_payload(
            self.base,
            "0.2.0",
            {
                "AGENTS.md": ("new starter instructions\n", "project-owned"),
                "docs/Factory/core.md": ("factory v2\n", "release-owned"),
                "scripts/factoryctl": ("#!/bin/sh\n", "release-owned"),
            },
        )

    def tearDown(self):
        self.temp.cleanup()

    def install_v1(self):
        plan = setup_plan(self.root, self.v1)
        output = RUNTIME.apply_setup_plan(
            self.root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=self.v1,
        )
        self.assertEqual("FACTORY_SETUP_APPLIED", output["reason_code"])

    def test_setup_requires_exact_plan_approval(self):
        plan = setup_plan(self.root, self.v1)
        before = inventory(self.root)
        output = RUNTIME.apply_setup_plan(
            self.root,
            plan=plan,
            approved_plan_id="wrong",
            payload_root=self.v1,
        )
        self.assertEqual("BLOCKED", output["state"])
        self.assertEqual("FACTORY_PLAN_APPROVAL_REQUIRED", output["reason_code"])
        self.assertEqual(before, inventory(self.root))

    def test_stale_setup_plan_halts_without_writing(self):
        plan = setup_plan(self.root, self.v1)
        write(self.root / "AGENTS.md", "appeared after preview\n")
        before = inventory(self.root)
        output = RUNTIME.apply_setup_plan(
            self.root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=self.v1,
        )
        self.assertEqual("BLOCKED", output["state"])
        self.assertEqual("FACTORY_PLAN_STALE", output["reason_code"])
        self.assertEqual(before, inventory(self.root))

    def test_setup_write_failure_restores_exact_prior_state(self):
        plan = setup_plan(self.root, self.v1)
        before = inventory(self.root)
        original = RUNTIME.atomic_write
        calls = {"count": 0}

        def fail_once(path, data, mode=0o644):
            calls["count"] += 1
            if calls["count"] == 2:
                raise OSError("fixture interruption")
            return original(path, data, mode)

        RUNTIME.atomic_write = fail_once
        try:
            output = RUNTIME.apply_setup_plan(
                self.root,
                plan=plan,
                approved_plan_id=plan["plan_id"],
                payload_root=self.v1,
            )
        finally:
            RUNTIME.atomic_write = original
        self.assertEqual("BLOCKED", output["state"])
        self.assertEqual("FACTORY_SETUP_ABORTED", output["reason_code"])
        self.assertIn("fixture interruption", output["blocker"])
        self.assertEqual(before, inventory(self.root))

    def test_setup_writes_receipt_and_second_run_is_idempotent(self):
        self.install_v1()
        self.assertEqual("factory v1\n", (self.root / "docs/Factory/core.md").read_text())
        state = json.loads(
            (
                self.root
                / "docs/Factory/installation/INSTALLATION_STATE.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("0.1.0", state["factory_version"])
        self.assertEqual("factory-plugin@0.1.0", state["source_revision"])
        self.assertTrue(state["managed_files"])
        self.assertTrue(
            all(
                {
                    "path",
                    "ownership_class",
                    "expected_digest",
                    "source_version",
                }
                <= set(item)
                for item in state["managed_files"]
            )
        )
        receipt_path = state["last_successful_transaction"]["receipt"]
        receipt = json.loads((self.root / receipt_path).read_text(encoding="utf-8"))
        self.assertEqual(state["last_successful_transaction"]["transaction_id"], receipt["transaction_id"])
        self.assertEqual("APPROVED", receipt["approval_state"])
        self.assertTrue(receipt["post_digests"])
        self.assertEqual("APPLIED", receipt["outcome"])
        self.assertEqual("NOT_REQUIRED", receipt["recovery_status"])
        before = inventory(self.root)
        plan = setup_plan(self.root, self.v1)
        output = RUNTIME.apply_setup_plan(
            self.root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=self.v1,
        )
        self.assertEqual("NO_CHANGE", output["state"])
        self.assertEqual("FACTORY_ALREADY_CURRENT", output["reason_code"])
        self.assertEqual([], output["mutations"])
        self.assertEqual(before, inventory(self.root))

    def test_update_preview_and_interruption_do_not_mutate(self):
        self.install_v1()
        plan = update_plan(self.root, self.v2)
        self.assertEqual("PLAN_READY", plan["state"])
        self.assertEqual("FACTORY_UPDATE_REVIEW_REQUIRED", plan["reason_code"])
        before = inventory(self.root)
        output = RUNTIME.apply_update_plan(
            self.root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=self.v2,
            interrupt_after_staging=True,
        )
        self.assertEqual("ROLLED_BACK", output["state"])
        self.assertEqual("FACTORY_UPDATE_ABORTED", output["reason_code"])
        self.assertEqual("0.1.0", output["final_version"])
        self.assertEqual(before, inventory(self.root))

    def test_update_preserves_project_owned_file_and_can_rollback_exactly(self):
        self.install_v1()
        write(self.root / "AGENTS.md", "team-owned instructions\n")
        before_update = inventory(self.root)
        plan = update_plan(self.root, self.v2)
        actions = {item["path"]: item["action"] for item in plan["planned_files"]}
        self.assertEqual("preserve", actions["AGENTS.md"])
        self.assertIn(
            "docs/Factory/installation/INSTALLATION_STATE.json",
            {item["path"] for item in plan["metadata_plan"]},
        )
        self.assertTrue(
            any(
                item["path"].startswith("docs/Factory/installation/receipts/")
                for item in plan["metadata_plan"]
            )
        )
        output = RUNTIME.apply_update_plan(
            self.root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=self.v2,
        )
        self.assertEqual("FACTORY_UPDATE_APPLIED", output["reason_code"])
        self.assertEqual(
            "team-owned instructions\n", (self.root / "AGENTS.md").read_text()
        )
        self.assertEqual("factory v2\n", (self.root / "docs/Factory/core.md").read_text())
        update_receipt_path = output["rollback_receipt"]
        approval = RUNTIME.apply_rollback(self.root, approved=False)
        self.assertEqual("BLOCKED", approval["state"])
        self.assertEqual(
            "FACTORY_ROLLBACK_APPROVAL_REQUIRED", approval["reason_code"]
        )
        rollback = RUNTIME.apply_rollback(self.root, approved=True)
        self.assertEqual("FACTORY_ROLLBACK_APPLIED", rollback["reason_code"])
        self.assertEqual("0.1.0", rollback["final_version"])
        after_rollback = inventory(self.root)
        before_without_receipts = {
            path: data
            for path, data in before_update.items()
            if "docs/Factory/installation/receipts/" not in path
        }
        after_without_receipts = {
            path: data
            for path, data in after_rollback.items()
            if "docs/Factory/installation/receipts/" not in path
        }
        self.assertEqual(before_without_receipts, after_without_receipts)
        update_receipt = json.loads(
            (self.root / update_receipt_path).read_text(encoding="utf-8")
        )
        self.assertEqual("ROLLED_BACK", update_receipt["recovery_status"])

    def test_modified_release_owned_file_blocks_update(self):
        self.install_v1()
        write(self.root / "docs/Factory/core.md", "local modification\n")
        before = inventory(self.root)
        output = update_plan(self.root, self.v2)
        self.assertEqual("BLOCKED", output["state"])
        self.assertEqual("FACTORY_CONFLICT_USER_OWNED", output["reason_code"])
        self.assertEqual(before, inventory(self.root))

    def test_downgrade_and_second_update_are_rejected_or_noop(self):
        self.install_v1()
        plan = update_plan(self.root, self.v2)
        applied = RUNTIME.apply_update_plan(
            self.root,
            plan=plan,
            approved_plan_id=plan["plan_id"],
            payload_root=self.v2,
        )
        self.assertEqual("APPLIED", applied["state"])
        before = inventory(self.root)
        second = update_plan(self.root, self.v2)
        self.assertEqual("NO_CHANGE", second["state"])
        self.assertEqual("FACTORY_ALREADY_CURRENT", second["reason_code"])
        downgrade = update_plan(self.root, self.v1)
        self.assertEqual("BLOCKED", downgrade["state"])
        self.assertEqual("FACTORY_DOWNGRADE_UNSUPPORTED", downgrade["reason_code"])
        self.assertEqual(before, inventory(self.root))


class FactoryPluginRealPayloadTests(unittest.TestCase):
    def test_real_payload_install_passes_knowledge_lint_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            payload = REPO_ROOT / "plugins/factory/payload"
            plan = RUNTIME.evaluate_setup_plan(
                root,
                mode="greenfield",
                harness="codex",
                payload_root=payload,
                platform_name="darwin",
                python_version=(3, 11, 0),
            )
            applied = RUNTIME.apply_setup_plan(
                root,
                plan=plan,
                approved_plan_id=plan["plan_id"],
                payload_root=payload,
            )
            self.assertEqual("FACTORY_SETUP_APPLIED", applied["reason_code"])
            lint = subprocess.run(
                ["bash", "scripts/knowledge_lint.sh"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, lint.returncode, lint.stdout + lint.stderr)
            before = inventory(root)
            second = RUNTIME.evaluate_setup_plan(
                root,
                mode="greenfield",
                harness="codex",
                payload_root=payload,
                platform_name="darwin",
                python_version=(3, 11, 0),
            )
            second_apply = RUNTIME.apply_setup_plan(
                root,
                plan=second,
                approved_plan_id=second["plan_id"],
                payload_root=payload,
            )
            self.assertEqual("NO_CHANGE", second_apply["state"])
            self.assertEqual(before, inventory(root))


if __name__ == "__main__":
    unittest.main()
