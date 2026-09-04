import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import runtime, seed_bmad, seed_factory


class FactoryBmadPolicyTests(unittest.TestCase):
    def audit(self, modules):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); seed_factory(root); seed_bmad(root, modules, capabilities=True)
        return runtime.module_audit(root, "claude")

    def test_core_bmm_is_upstream_only(self):
        payload = self.audit({"core": "6.10.0", "bmm": "6.10.0"})
        self.assertEqual("READY", payload["state"])
        self.assertEqual("UPSTREAM_CAPABILITY_ONLY", payload["classifications"]["bmm"])

    def test_loop_blocks(self):
        payload = self.audit({"core": "6.10.0", "bmm": "6.10.0", "bmad-loop": "v0.9.1"})
        self.assertEqual("CONDUCTOR_BMAD_LOOP_INSTALLED", payload["reason_code"])
        self.assertEqual("PROHIBITED_BLOCKER", payload["classifications"]["bmad-loop"])

    def test_tea_is_evidence_only_not_governance(self):
        payload = self.audit({"core": "6.10.0", "bmm": "6.10.0", "tea": "v1.21.1"})
        self.assertEqual("READY", payload["state"])
        self.assertEqual("OPTIONAL_STAGE_F_EVIDENCE_ONLY", payload["classifications"]["tea"])

    def test_unknown_module_requires_review(self):
        payload = self.audit({"core": "6.10.0", "bmm": "6.10.0", "mystery": "1.0"})
        self.assertEqual("CONDUCTOR_BMAD_MODULE_REVIEW_REQUIRED", payload["reason_code"])


if __name__ == "__main__":
    unittest.main()
