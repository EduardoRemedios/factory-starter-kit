import tempfile
import unittest
from pathlib import Path

from tests.test_factory_bmad_support import runtime, seed_bmad, seed_factory, seed_git


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
        self.assertEqual("FACTORY_BMAD_POLICY_OK", payload["reason_code"])
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
        self.assertEqual("FACTORY_BMAD_CAPABILITY_INCOMPLETE", payload["reason_code"])

    def test_unknown_capability_blocks(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        skill = root / ".claude/skills/bmad-future-autonomous/SKILL.md"
        skill.parent.mkdir(parents=True); skill.write_text("# future\n", encoding="utf-8")
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("FACTORY_BMAD_CAPABILITY_UNRECOGNIZED", payload["reason_code"])

    def test_symlinked_bmad_skill_blocks_without_following(self):
        root = self.root(); seed_bmad(root, capabilities=True)
        outside = root.parent / f"{root.name}-outside-skill"
        outside.mkdir(); self.addCleanup(lambda: outside.rmdir())
        link = root / ".claude/skills/bmad-linked"
        link.symlink_to(outside, target_is_directory=True)
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("FACTORY_BMAD_CAPABILITY_UNRECOGNIZED", payload["reason_code"])

    def test_unsupported_core_version_is_quarantined(self):
        root = self.root(); seed_bmad(root, {"core": "6.11.0", "bmm": "6.11.0"}, capabilities=True)
        payload = runtime.capability_audit(root, "claude")
        self.assertEqual("FACTORY_BMAD_VERSION_QUARANTINED", payload["reason_code"])
        self.assertEqual([], payload["mutations"])

    def test_loop_blocks_and_tea_is_evidence_only(self):
        loop_root = self.root(); seed_bmad(loop_root, {"core": "6.10.0", "bmm": "6.10.0", "bmad-loop": "v0.9.1"}, capabilities=True)
        self.assertEqual("FACTORY_BMAD_LOOP_INSTALLED", runtime.capability_audit(loop_root, "claude")["reason_code"])
        tea_root = self.root(); seed_bmad(tea_root, {"core": "6.10.0", "bmm": "6.10.0", "tea": "v1.21.1"}, capabilities=True)
        payload = runtime.capability_audit(tea_root, "claude")
        self.assertEqual("READY", payload["state"])
        self.assertEqual("OPTIONAL_STAGE_F_EVIDENCE_ONLY", payload["module_classifications"]["tea"])
        tea_capabilities = [item for item in payload["capabilities"]["skills"] if item["name"] in runtime.SUPPORTED_TEA_SKILLS]
        self.assertEqual(len(runtime.SUPPORTED_TEA_SKILLS), len(tea_capabilities))
        self.assertTrue(all(item["classification"] == "OPTIONAL_STAGE_F_EVIDENCE_ONLY" for item in tea_capabilities))


if __name__ == "__main__":
    unittest.main()
