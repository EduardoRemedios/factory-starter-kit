from __future__ import annotations

import json
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts.conductor_host_capability import (
    artifact_path,
    discover_artifact,
    host_identity,
    validate_artifact,
    validate_document,
)
from scripts.conductor_pack_lint import (
    check_host_capability_contract,
    evaluate_host_capability_contract,
    inspect_host_capability_requirements,
)


class HostCapabilityValidatorTests(unittest.TestCase):
    def document(self, path: str, *, kind: str = "executable_file") -> dict:
        return {
            "schema_version": 1,
            "run_id": "RUN_TEST",
            "posture": "VERIFIED_LOCAL",
            "host": host_identity(),
            "capabilities": [{"id": "shell_test", "path": path, "kind": kind}],
        }

    def test_missing_usr_bin_test_fails_on_current_macos_host(self) -> None:
        if host_identity()["system"] != "Darwin" or Path("/usr/bin/test").exists():
            self.skipTest("macOS path regression applies only when /usr/bin/test is absent")
        result = validate_document(self.document("/usr/bin/test"), run_id="RUN_TEST")
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITY_PATH_MISSING")

    def test_bin_test_is_valid_executable_on_current_macos_host(self) -> None:
        if host_identity()["system"] != "Darwin":
            self.skipTest("macOS path regression")
        result = validate_document(self.document("/bin/test"), run_id="RUN_TEST")
        self.assertEqual(result["status"], "PASS")

    def test_relative_duplicate_and_unknown_kind_fail_schema(self) -> None:
        document = self.document("relative/test")
        document["capabilities"] *= 2
        document["capabilities"][1] = {"id": "shell_test", "path": "/bin/test", "kind": "program"}
        result = validate_document(document, run_id="RUN_TEST")
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITY_SCHEMA_INVALID")
        self.assertTrue(any("PATH_INVALID" in item for item in result["errors"]))
        self.assertTrue(any("ID_DUPLICATE" in item for item in result["errors"]))
        self.assertTrue(any("KIND_INVALID" in item for item in result["errors"]))

    def test_host_mismatch_and_deferred_target_block(self) -> None:
        document = self.document("/bin/test")
        result = validate_document(document, run_id="RUN_TEST", current_host={"system": "Other", "machine": "x"})
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITY_HOST_MISMATCH")
        document["posture"] = "DEFERRED_TARGET"
        result = validate_document(document, run_id="RUN_TEST")
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITIES_DEFERRED_TARGET")

    def test_file_directory_and_executable_kinds(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            file_path = root / "tool"
            file_path.write_text("fixture", encoding="utf-8")
            file_result = validate_document(self.document(str(file_path), kind="file"), run_id="RUN_TEST")
            self.assertEqual(file_result["status"], "PASS")
            executable_result = validate_document(self.document(str(file_path)), run_id="RUN_TEST")
            self.assertEqual(executable_result["reason_code"], "CONDUCTOR_HOST_CAPABILITY_NOT_EXECUTABLE")
            file_path.chmod(file_path.stat().st_mode | stat.S_IXUSR)
            executable_result = validate_document(self.document(str(file_path)), run_id="RUN_TEST")
            self.assertEqual(executable_result["status"], "PASS")
            directory_result = validate_document(self.document(str(root), kind="directory"), run_id="RUN_TEST")
            self.assertEqual(directory_result["status"], "PASS")

    def test_validation_does_not_read_capability_contents(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            tool = Path(temp_dir) / "tool"
            tool.write_text("secret", encoding="utf-8")
            tool.chmod(tool.stat().st_mode | stat.S_IXUSR)
            with mock.patch.object(Path, "read_bytes", side_effect=AssertionError("target content read")):
                result = validate_document(self.document(str(tool)), run_id="RUN_TEST")
            self.assertEqual(result["status"], "PASS")

    def test_discovery_writes_only_exact_pack_artifact_after_validation(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            pack = root / "docs/Conductor/runs/RUN_TEST/pack"
            pack.mkdir(parents=True)
            tool = root / "tool"
            tool.write_text("fixture", encoding="utf-8")
            tool.chmod(tool.stat().st_mode | stat.S_IXUSR)
            result = discover_artifact(root, "RUN_TEST", [["tool", "executable_file", str(tool)]], "pack/host_capabilities.json")
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["mutations"], ["docs/Conductor/runs/RUN_TEST/pack/host_capabilities.json"])
            self.assertTrue(artifact_path(root, "RUN_TEST").is_file())
            before = artifact_path(root, "RUN_TEST").read_bytes()
            validated = validate_artifact(root, "RUN_TEST")
            self.assertEqual(validated["status"], "PASS")
            self.assertEqual(artifact_path(root, "RUN_TEST").read_bytes(), before)


class HostCapabilityPackLintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.run = self.root / "docs/Conductor/runs/RUN_TEST"
        self.pack = self.run / "pack"
        self.pack.mkdir(parents=True)
        (self.run / "EXECUTION_MODE.txt").write_text("PLANNING_ONLY\n", encoding="utf-8")
        (self.run / "SPRINT_ID.txt").write_text("SPRINT_TEST\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_manifest(self, *, command: str, capability_ids: list[str] | None) -> None:
        declaration = ""
        if capability_ids is not None:
            declaration = "    capability_ids: [" + ", ".join(capability_ids) + "]\n"
        (self.pack / "verification_manifest.yaml").write_text(
            "schema_version: 1\n"
            "run_id: RUN_TEST\n"
            "sprint_id: SPRINT_TEST\n"
            "execution_mode: PLANNING_ONLY\n"
            "checks:\n"
            "  - id: VM-001\n"
            "    tier: V2\n"
            "    type: command\n"
            "    constraint_ids: [C-01]\n"
            "    description: host check\n"
            f"    command: {command}\n"
            f"{declaration}"
            "    expected: pass\n"
            "    halt_on_failure: true\n"
            "    evidence_path: artifacts/VM-001.json\n",
            encoding="utf-8",
        )

    def write_artifact(self, path: str, *, posture: str = "VERIFIED_LOCAL", capability_id: str = "shell_test") -> None:
        document = {
            "schema_version": 1,
            "run_id": "RUN_TEST",
            "posture": posture,
            "host": host_identity(),
            "capabilities": [{"id": capability_id, "path": path, "kind": "executable_file"}],
        }
        (self.pack / "host_capabilities.json").write_text(json.dumps(document), encoding="utf-8")

    def test_absolute_command_without_declaration_fails(self) -> None:
        self.write_manifest(command="/bin/test -e fixture", capability_ids=None)
        result = evaluate_host_capability_contract(self.root, self.run)
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITY_DECLARATION_INVALID")

    def test_declared_absolute_command_requires_artifact(self) -> None:
        self.write_manifest(command="/bin/test -e fixture", capability_ids=["shell_test"])
        result = evaluate_host_capability_contract(self.root, self.run)
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITIES_MISSING")

    def test_matching_declared_capability_passes(self) -> None:
        self.write_manifest(command="/bin/test -e fixture", capability_ids=["shell_test"])
        self.write_artifact("/bin/test")
        result = evaluate_host_capability_contract(self.root, self.run)
        self.assertEqual(result["status"], "PASS")

    def test_unknown_id_and_path_mismatch_fail(self) -> None:
        self.write_manifest(command="/bin/test -e fixture", capability_ids=["other"])
        self.write_artifact("/bin/test")
        result = evaluate_host_capability_contract(self.root, self.run)
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITY_DECLARATION_MISMATCH")

    def test_relative_command_without_artifact_is_compatible(self) -> None:
        self.write_manifest(command="./scripts/conductor-python -V", capability_ids=None)
        result = evaluate_host_capability_contract(self.root, self.run)
        self.assertEqual(result["reason_code"], "CONDUCTOR_HOST_CAPABILITIES_NOT_REQUIRED")

    def test_deferred_target_is_allowed_only_for_planning_envelope(self) -> None:
        self.write_manifest(command="/bin/test -e fixture", capability_ids=["shell_test"])
        self.write_artifact("/bin/test", posture="DEFERRED_TARGET")
        (self.pack / "SPRINT_TEST_ENVELOPE.md").write_text("Host Capability Posture: DEFERRED_TARGET\n", encoding="utf-8")
        errors: list[str] = []
        checked: list[str] = []
        check_host_capability_contract(
            root=self.root,
            run_root=self.run,
            pack_dir=self.pack,
            execution_mode="PLANNING_ONLY",
            checked_files=checked,
            errors=errors,
        )
        self.assertEqual(errors, [])
        check_host_capability_contract(
            root=self.root,
            run_root=self.run,
            pack_dir=self.pack,
            execution_mode="EXECUTION_ENABLED",
            checked_files=checked,
            errors=errors,
        )
        self.assertTrue(any("DEFERRED_TARGET" in item for item in errors))

    def test_shell_fixture_tokens_are_inspected(self) -> None:
        fixture = self.pack / "fixtures/check.sh"
        fixture.parent.mkdir()
        fixture.write_text("/bin/test -e fixture\n", encoding="utf-8")
        (self.pack / "verification_manifest.yaml").write_text(
            "checks:\n"
            "  - id: VM-001\n"
            "    type: fixture\n"
            "    target: fixtures/check.sh\n"
            "    capability_ids: [shell_test]\n",
            encoding="utf-8",
        )
        result = inspect_host_capability_requirements(self.pack)
        self.assertEqual(result["absolute_paths"], ["/bin/test"])
        self.assertEqual(result["capability_ids"], ["shell_test"])


if __name__ == "__main__":
    unittest.main()
