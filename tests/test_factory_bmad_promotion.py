import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from tests.test_factory_bmad_support import runtime


class FactoryBmadPromotionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.source = self.root / "_bmad-output/product/brief.md"
        self.source.parent.mkdir(parents=True)
        self.source.write_text("# Reviewed idea\n", encoding="utf-8")

    def args(self, **overrides):
        values = {"source": "_bmad-output/product/brief.md", "snapshot_id": "product-brief-v1", "workflow": "product-brief", "reviewer": "Product Owner", "review_ref": "BR-42", "review_qualifier": None, "approve_plan": None}
        values.update(overrides)
        return Namespace(**values)

    def test_preview_apply_and_reuse(self):
        before = runtime.tree_inventory(self.root)
        preview = runtime.promote(self.root, self.args())
        self.assertEqual("PLAN_READY", preview["state"])
        self.assertEqual(before, runtime.tree_inventory(self.root))
        applied = runtime.promote(self.root, self.args(approve_plan=preview["plan"]["plan_id"]))
        self.assertEqual("APPLIED", applied["state"])
        snapshot = self.root / "docs/upstream/bmad/product-brief-v1"
        self.assertTrue((snapshot / "SNAPSHOT_MANIFEST.json").is_file())
        reused = runtime.promote(self.root, self.args())
        self.assertEqual("REUSABLE", reused["state"])
        self.assertEqual(applied["aggregate_sha256"], reused["aggregate_sha256"])

    def test_stale_source_blocks(self):
        preview = runtime.promote(self.root, self.args())
        self.source.write_text("changed\n", encoding="utf-8")
        payload = runtime.promote(self.root, self.args(approve_plan=preview["plan"]["plan_id"]))
        self.assertEqual("FACTORY_BMAD_PLAN_APPROVAL_MISMATCH", payload["reason_code"])

    def test_optional_review_qualifier_is_plan_bound_and_immutable(self):
        qualifier = "unvalidated upstream evidence; not binding product intent"
        preview = runtime.promote(self.root, self.args(review_qualifier=qualifier))
        self.assertEqual(qualifier, preview["plan"]["review_qualifier"])
        stale = runtime.promote(
            self.root,
            self.args(
                review_qualifier="different qualifier",
                approve_plan=preview["plan"]["plan_id"],
            ),
        )
        self.assertEqual("FACTORY_BMAD_PLAN_APPROVAL_MISMATCH", stale["reason_code"])
        applied = runtime.promote(
            self.root,
            self.args(review_qualifier=qualifier, approve_plan=preview["plan"]["plan_id"]),
        )
        manifest = __import__("json").loads(
            (self.root / "docs/upstream/bmad/product-brief-v1/SNAPSHOT_MANIFEST.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual("APPLIED", applied["state"])
        self.assertEqual(qualifier, manifest["review"]["qualifier"])

    def test_traversal_symlink_and_downstream_workflow_block(self):
        traversal = runtime.promote(self.root, self.args(source="../brief.md"))
        self.assertEqual("FACTORY_BMAD_PATH_INVALID", traversal["reason_code"])
        target = self.root / "outside.md"; target.write_text("x\n", encoding="utf-8")
        link = self.root / "_bmad-output/link.md"; link.symlink_to(target)
        symlink = runtime.promote(self.root, self.args(source="_bmad-output/link.md"))
        self.assertEqual("FACTORY_BMAD_SYMLINK_REJECTED", symlink["reason_code"])
        prohibited = runtime.promote(self.root, self.args(workflow="architecture"))
        self.assertEqual("FACTORY_BMAD_WORKFLOW_PROHIBITED", prohibited["reason_code"])
        obsolete = runtime.promote(self.root, self.args(workflow="project-context"))
        self.assertEqual("FACTORY_BMAD_WORKFLOW_PROHIBITED", obsolete["reason_code"])
        allowed = runtime.promote(self.root, self.args(workflow="document-project"))
        self.assertEqual("PLAN_READY", allowed["state"])

    def test_prefixed_allowed_workflow_alias_is_accepted(self):
        payload = runtime.promote(
            self.root, self.args(workflow="bmad-product-brief")
        )
        self.assertEqual("PLAN_READY", payload["state"])
        self.assertEqual("product-brief", payload["plan"]["workflow"])

    def test_immutable_conflict_blocks(self):
        destination = self.root / "docs/upstream/bmad/product-brief-v1"
        destination.mkdir(parents=True)
        (destination / "user.md").write_text("mine\n", encoding="utf-8")
        payload = runtime.promote(self.root, self.args())
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_IMMUTABLE_CONFLICT", payload["reason_code"])

    def test_reserved_snapshot_ids_are_casefolded(self):
        for snapshot_id in ("receipts", "RECEIPTS", "Install-Receipts", "INSTALL-RECEIPTS"):
            with self.subTest(snapshot_id=snapshot_id):
                payload = runtime.promote(self.root, self.args(snapshot_id=snapshot_id))
                self.assertEqual("FACTORY_BMAD_SNAPSHOT_ID_RESERVED", payload["reason_code"])

    def test_snapshot_reuse_requires_exact_inventory_and_modes(self):
        preview = runtime.promote(self.root, self.args())
        runtime.promote(self.root, self.args(approve_plan=preview["plan"]["plan_id"]))
        snapshot = self.root / "docs/upstream/bmad/product-brief-v1"
        (snapshot / "extra.txt").write_text("extra\n", encoding="utf-8")
        payload = runtime.promote(self.root, self.args())
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_IMMUTABLE_CONFLICT", payload["reason_code"])

    def test_snapshot_mode_drift_blocks_reuse_and_rollback(self):
        preview = runtime.promote(self.root, self.args())
        applied = runtime.promote(self.root, self.args(approve_plan=preview["plan"]["plan_id"]))
        artifact = self.root / "docs/upstream/bmad/product-brief-v1/artifact.md"
        artifact.chmod(0o600)
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_IMMUTABLE_CONFLICT", runtime.promote(self.root, self.args())["reason_code"])
        self.assertEqual("FACTORY_BMAD_ROLLBACK_DIGEST_MISMATCH", runtime.rollback(self.root, applied["receipt"], None)["reason_code"])

    def test_guarded_rollback(self):
        preview = runtime.promote(self.root, self.args())
        applied = runtime.promote(self.root, self.args(approve_plan=preview["plan"]["plan_id"]))
        rollback_preview = runtime.rollback(self.root, applied["receipt"], None)
        self.assertEqual("PLAN_READY", rollback_preview["state"])
        rolled_back = runtime.rollback(self.root, applied["receipt"], rollback_preview["plan"]["plan_id"])
        self.assertEqual("APPLIED", rolled_back["state"])
        self.assertFalse((self.root / "docs/upstream/bmad/product-brief-v1").exists())

    def test_changed_snapshot_refuses_rollback(self):
        preview = runtime.promote(self.root, self.args())
        applied = runtime.promote(self.root, self.args(approve_plan=preview["plan"]["plan_id"]))
        (self.root / "docs/upstream/bmad/product-brief-v1/artifact.md").write_text("tampered\n", encoding="utf-8")
        payload = runtime.rollback(self.root, applied["receipt"], None)
        self.assertEqual("FACTORY_BMAD_ROLLBACK_DIGEST_MISMATCH", payload["reason_code"])


if __name__ == "__main__":
    unittest.main()
