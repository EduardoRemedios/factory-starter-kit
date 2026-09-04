import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import runtime, seed_bmad, seed_factory, seed_git, seed_nested_bmad


class FactoryBmadCapabilityTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); seed_git(root); seed_factory(root)
        return root

    def test_complete_supported_inventory_passes(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("READY", payload["state"])
        self.assertEqual("CONDUCTOR_BMAD_POLICY_OK", payload["reason_code"])
        self.assertEqual("6.10.0", payload["installation_version"])
        self.assertTrue(payload["coverage_sha256"])
        self.assertEqual([], payload["uncovered_capabilities"])
        self.assertIn("skills", payload["capabilities"])
        self.assertIn("commands", payload["capabilities"])
        self.assertIn("agents", payload["capabilities"])
        self.assertIn("hooks", payload["capabilities"])
        self.assertIn("configuration", payload["capabilities"])

    def test_missing_supported_skill_blocks_incomplete_coverage(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        skill = root / ".claude/skills/bmad-architecture/SKILL.md"
        skill.unlink(); skill.parent.rmdir()
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("CONDUCTOR_BMAD_CAPABILITY_INCOMPLETE", payload["reason_code"])

    def test_unknown_capability_blocks(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        skill = root / ".claude/skills/bmad-future-autonomous/SKILL.md"
        skill.parent.mkdir(parents=True); skill.write_text("# future\n", encoding="utf-8")
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("CONDUCTOR_BMAD_CAPABILITY_UNRECOGNIZED", payload["reason_code"])

    def test_symlinked_bmad_skill_blocks_without_following(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        outside = root.parent / f"{root.name}-outside-skill"
        outside.mkdir(); self.addCleanup(lambda: outside.rmdir())
        link = root / ".claude/skills/bmad-linked"
        link.symlink_to(outside, target_is_directory=True)
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("CONDUCTOR_BMAD_CAPABILITY_UNRECOGNIZED", payload["reason_code"])

    def test_unsupported_core_version_is_quarantined(self):
        root = self.root(); seed_bmad(root, {"core": "6.11.0", "bmm": "6.11.0"}, capabilities=True)
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("CONDUCTOR_BMAD_VERSION_QUARANTINED", payload["reason_code"])
        self.assertEqual([], payload["mutations"])

    def test_loop_blocks_and_tea_is_evidence_only(self):
        loop_root = self.root(); seed_bmad(loop_root, {"core": "6.10.0", "bmm": "6.10.0", "bmad-loop": "v0.9.1"}, capabilities=True)
        self.assertEqual("CONDUCTOR_BMAD_LOOP_INSTALLED", runtime.capability_audit(loop_root, "claude")["reason_code"])
        tea_root = self.root(); seed_bmad(tea_root, {"core": "6.10.0", "bmm": "6.10.0", "tea": "v1.21.1"}, capabilities=True)
        payload = runtime.capability_audit(tea_root, "claude")
        self.assertEqual("READY", payload["state"])
        self.assertEqual("OPTIONAL_STAGE_F_EVIDENCE_ONLY", payload["module_classifications"]["tea"])
        tea_capabilities = [item for item in payload["capabilities"]["skills"] if item["name"] in runtime.SUPPORTED_TEA_SKILLS]
        self.assertEqual(len(runtime.SUPPORTED_TEA_SKILLS), len(tea_capabilities))
        self.assertTrue(all(item["classification"] == "OPTIONAL_STAGE_F_EVIDENCE_ONLY" for item in tea_capabilities))

    def test_nested_bmad_audit_reports_loop_before_activation(self):
        root = self.root()
        seed_nested_bmad(root, {"core": "6.10.0", "bmm": "6.10.0", "bmad-loop": "v0.9.1"}, capabilities=True)
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("BLOCKED", payload["state"])
        self.assertEqual("CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT", payload["reason_code"])
        self.assertEqual("CONDUCTOR_BMAD_NESTED_LAYOUT", payload["layout_reason_code"])
        layout = payload["non_canonical_bmad_layouts"][0]
        self.assertEqual("bmad", layout["path"])
        self.assertIn("bmad/_bmad/_config/manifest.yaml", layout["manifests"])
        self.assertEqual("PROHIBITED_BLOCKER", layout["module_classifications"]["bmad-loop"])
        self.assertEqual("POLICY_COVERED", layout["module_classifications"]["core"])

    def test_unsafe_layouts_fail_closed_with_stable_reasons(self):
        cases = []

        nested = self.root(); seed_bmad(nested / "bmad", capabilities=True)
        cases.append((nested, "nested_active", "CONDUCTOR_BMAD_NESTED_LAYOUT"))

        combined = self.root(); seed_bmad(combined, capabilities=True); seed_bmad(combined / "bmad", capabilities=True)
        cases.append((combined, "canonical_and_nested", "CONDUCTOR_BMAD_MULTIPLE_ACTIVE_ROOTS"))

        ambiguous = self.root(); seed_bmad(ambiguous, capabilities=True)
        source_manifest = ambiguous / "_bmad/_config/manifest.yaml"
        source_manifest.with_suffix(".yml").write_bytes(source_manifest.read_bytes())
        cases.append((ambiguous, "ambiguous", "CONDUCTOR_BMAD_MANIFEST_AMBIGUOUS"))

        partial = self.root(); (partial / "_bmad").mkdir()
        cases.append((partial, "partial", "CONDUCTOR_BMAD_PARTIAL_STATE"))

        linked = self.root(); seed_bmad(linked / "canonical-source")
        (linked / "_bmad").symlink_to(linked / "canonical-source/_bmad", target_is_directory=True)
        cases.append((linked, "active_root_symlink", "CONDUCTOR_BMAD_ACTIVE_ROOT_SYMLINK"))

        for root, expected_state, expected_reason in cases:
            with self.subTest(expected_state):
                layout = runtime.assess_bmad_layout(root)
                self.assertEqual(expected_state, layout["state"])
                self.assertFalse(layout["safe"])
                self.assertEqual(expected_reason, layout["reason_code"])
                doctor = runtime.doctor(root, "claude")
                self.assertEqual("CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT", doctor["reason_code"])
                self.assertEqual(expected_reason, doctor["evidence"]["layout_reason_code"])
                audit = runtime.capability_audit(root, "claude")
                self.assertEqual("CONDUCTOR_BMAD_NON_CANONICAL_LAYOUT", audit["reason_code"])
                self.assertEqual(expected_reason, audit["layout_reason_code"])
                activation = runtime.enforcement_activation(root)
                self.assertTrue(activation["active"])
                self.assertEqual("CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE_UNSAFE_LAYOUT", activation["reason_code"])

    def test_fixed_legacy_archive_is_inert_beside_canonical_root(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        archive_root = root / runtime.policy.LEGACY_EVIDENCE_ROOT / "bmad-legacy-spike-1"
        seed_bmad(archive_root)
        layout = runtime.assess_bmad_layout(root)
        self.assertEqual("canonical_root", layout["state"])
        self.assertTrue(layout["legacy_archive_present"])
        self.assertEqual([], layout["nested_installations"])
        self.assertEqual("READY", runtime.capability_audit(root, "claude")["state"])

        archive_only = self.root()
        seed_bmad(archive_only / runtime.policy.LEGACY_EVIDENCE_ROOT / "historical")
        inert = runtime.assess_bmad_layout(archive_only)
        self.assertEqual("legacy_archive_outside_index", inert["state"])
        self.assertTrue(inert["safe"])
        self.assertFalse(inert["active_marker_present"])
        self.assertEqual("CONDUCTOR_ONLY", runtime.doctor(archive_only, "claude")["state"])
        self.assertFalse(runtime.enforcement_activation(archive_only)["active"])

if __name__ == "__main__":
    unittest.main()
