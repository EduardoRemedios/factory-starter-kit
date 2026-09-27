"""Doctor distinguishes project instructions from evidence of Factory adoption."""
import json
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_plugin_status import RUNTIME, inventory, write


class DoctorAdoptionTests(unittest.TestCase):
    def diagnose(self, root, expected):
        before = inventory(root)
        for harness in ("codex", "claude"):
            with self.subTest(harness=harness):
                result = RUNTIME.evaluate_doctor(
                    root, harness=harness, platform_name="darwin", python_version=(3, 11, 0)
                )
                self.assertEqual(expected, result["reason_code"])
                self.assertEqual([], result["mutations"])
                self.assertEqual(before, inventory(root))
        return result

    def test_plain_project_instructions_are_not_an_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write(root / "AGENTS.md", "# Notes\nRead docs/ENGINEERING_STANDARDS.md.\n")
            result = self.diagnose(root, "CONDUCTOR_PROJECT_NOT_CONFIGURED")
            self.assertEqual("NOT_CONFIGURED", result["project_compatibility"])
            self.assertEqual("preview_greenfield_or_brownfield_setup", result["next_legal_action"])

    def test_no_instructions_are_not_an_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            self.diagnose(Path(directory), "CONDUCTOR_PROJECT_NOT_CONFIGURED")

    def test_each_partial_core_file_blocks_with_or_without_agents(self):
        for relative in ("docs/Conductor/ARCHITECTURE.md", "docs/Conductor/ORCHESTRATION.md", "docs/Conductor/INVARIANTS.md", "docs/Factory/ARCHITECTURE.md", "scripts/conductorctl", "scripts/conductor-python"):
            for agents in (False, True):
                with self.subTest(relative=relative, agents=agents), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write(root / relative, "Factory fixture\n")
                    if agents:
                        write(root / "AGENTS.md", "# Project\n")
                    self.diagnose(root, "CONDUCTOR_PROJECT_INCOMPLETE")

    def test_managed_marker_alone_blocks_including_incomplete_marker(self):
        for marker in ("<!-- conductor:managed:start v=0.3.10 sha256=" + "a" * 64 + " -->", "<!-- conductor:managed:start", "<!-- conductor:managed:end -->"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write(root / "AGENTS.md", "# Project\n" + marker + "\n")
                self.diagnose(root, "CONDUCTOR_PROJECT_INCOMPLETE")

    def test_valid_current_and_legacy_state_without_payload_blocks(self):
        for relative, version_key in ((RUNTIME.INSTALLATION_STATE_PATH, "conductor_version"), (RUNTIME.LEGACY_INSTALLATION_STATE_PATH, "factory_version")):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write(root / relative, json.dumps({"schema_version": 1, version_key: "0.3.10", "source_revision": "fixture", "managed_files": [], "adapter_state": {}, "last_successful_transaction": {}}))
                self.diagnose(root, "CONDUCTOR_PROJECT_INCOMPLETE")

    def test_malformed_state_keeps_existing_failure_precedence(self):
        for relative in (RUNTIME.INSTALLATION_STATE_PATH, RUNTIME.LEGACY_INSTALLATION_STATE_PATH):
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write(root / relative, "not json")
                self.diagnose(root, "CONDUCTOR_INSTALLATION_STATE_INVALID")

    def test_complete_core_remains_compatible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("AGENTS.md", "docs/Conductor/ARCHITECTURE.md", "docs/Conductor/ORCHESTRATION.md", "scripts/conductorctl"):
                write(root / relative, "Fixture\n")
            self.diagnose(root, "CONDUCTOR_DOCTOR_OK")

    def test_core_path_directory_or_broken_link_is_not_a_fresh_project(self):
        for broken_link in (False, True):
            with self.subTest(broken_link=broken_link), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = root / "scripts/conductorctl"
                path.parent.mkdir()
                if broken_link:
                    path.symlink_to("absent")
                else:
                    path.mkdir()
                self.diagnose(root, "CONDUCTOR_PROJECT_INCOMPLETE")
