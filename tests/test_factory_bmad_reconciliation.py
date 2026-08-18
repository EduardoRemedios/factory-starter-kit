import tempfile
import unittest
from pathlib import Path

from tests.test_factory_bmad_support import runtime, seed_bmad, seed_factory, seed_git


class FactoryBmadReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name); seed_git(self.root); seed_factory(self.root); seed_bmad(self.root, capabilities=True)
        files = {
            "_bmad-output/planning/product-brief.md": "brief\n",
            "_bmad-output/planning/architecture.md": "legacy\n",
            "_bmad-output/implementation/sprint-status.yaml": "status: old\n",
            "_bmad-output/misc/notes.md": "unknown\n",
            "src/app.py": "print('preserve')\n",
        }
        for name, content in files.items():
            path = self.root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content, encoding="utf-8")

    def test_reconciliation_is_read_only_and_classifies_authority(self):
        before = runtime.tree_inventory(self.root)
        report = runtime.reconcile_brownfield(self.root)
        self.assertEqual(before, runtime.tree_inventory(self.root))
        classes = {item["path"]: item["classification"] for item in report["artifacts"]}
        self.assertEqual("UPSTREAM_REVIEW_CANDIDATE", classes["_bmad-output/planning/product-brief.md"])
        self.assertEqual("NON_BINDING_HISTORY", classes["_bmad-output/planning/architecture.md"])
        self.assertEqual("NON_BINDING_HISTORY", classes["_bmad-output/implementation/sprint-status.yaml"])
        self.assertEqual("REVIEW_REQUIRED", classes["_bmad-output/misc/notes.md"])
        self.assertNotIn("src/app.py", classes)

    def test_capability_audit_embeds_reconciliation_digest(self):
        payload = runtime.capability_audit(self.root, "claude")
        self.assertEqual("READY", payload["state"])
        self.assertEqual(runtime.reconcile_brownfield(self.root)["aggregate_sha256"], payload["reconciliation"]["aggregate_sha256"])


if __name__ == "__main__":
    unittest.main()
