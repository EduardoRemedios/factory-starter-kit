import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLIC_ROOTS = [REPO_ROOT / "plugin-src/factory-bmad", REPO_ROOT / "plugins/factory-bmad", REPO_ROOT / "plugins/factory-bmad-claude", REPO_ROOT / "docs/adapters/bmad"]
PUBLIC_FILES = [
    REPO_ROOT / "scripts/build_factory_bmad_plugins.py",
    *sorted((REPO_ROOT / "scripts").glob("verify_factory_bmad_*.sh")),
]


class FactoryBmadDocsPrivacyTests(unittest.TestCase):
    def test_public_companion_is_customer_neutral_and_private_safe(self):
        prohibited = re.compile(r"Symphony|AuditEdge|/Users/|Claude Enterprise|website_sales", re.IGNORECASE)
        for root in PUBLIC_ROOTS:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file():
                    self.assertIsNone(prohibited.search(path.read_text(encoding="utf-8", errors="ignore")), str(path))
        for path in PUBLIC_FILES:
            self.assertIsNone(prohibited.search(path.read_text(encoding="utf-8", errors="ignore")), str(path))

    def test_policy_states_authority_and_tea_boundary(self):
        policy = (REPO_ROOT / "plugin-src/factory-bmad/project-adapter/BMAD_POLICY.md").read_text(encoding="utf-8")
        self.assertIn("Factory is the SDLC and sole downstream authority", policy)
        self.assertIn("optional Stage F evidence only", policy)
        self.assertIn("bmad-loop", policy)

    def test_required_enforcement_verifier_is_deterministic(self):
        verifier = (REPO_ROOT / "scripts/verify_factory_bmad_claude_enforcement.sh").read_text(encoding="utf-8")
        self.assertIn("DETERMINISTIC_PACKAGED_PRETOOLUSE", verifier)
        self.assertNotIn("FACTORY_BMAD_LIVE_CLAUDE", verifier)
        self.assertNotIn("test_factory_bmad_claude_live", verifier)
        self.assertFalse((REPO_ROOT / "scripts/verify_factory_bmad_claude_two_lane.py").exists())


if __name__ == "__main__":
    unittest.main()
