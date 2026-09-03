import json
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
        values = {"source": "_bmad-output/product/brief.md", "snapshot_id": "product-brief-v1", "workflow": "product-brief", "reviewer": "Product Owner", "review_ref": "BR-42", "review_qualifier": None, "evidence_type": None, "authority": None, "plan_identity": None, "supersedes_snapshot_id": None, "supersedes_sha256": None, "approve_plan": None}
        values.update(overrides)
        return Namespace(**values)

    def solution_args(self, **overrides):
        package = self.root / "_bmad-output/solution"
        package.mkdir(parents=True, exist_ok=True)
        if not (package / "ux.md").exists():
            (package / "ux.md").write_text("# UX\n", encoding="utf-8")
        (package / "decisions/ADR-1.md").parent.mkdir(parents=True, exist_ok=True)
        if not (package / "decisions/ADR-1.md").exists():
            (package / "decisions/ADR-1.md").write_text("# Candidate decision\n", encoding="utf-8")
        values = {
            "source": "_bmad-output/solution", "snapshot_id": "solution-v1", "workflow": "ux",
            "reviewer": "Product Owner", "review_ref": "BR-43", "review_qualifier": None,
            "evidence_type": "SOLUTION_CONTEXT", "authority": "EVIDENCE_ONLY",
            "plan_identity": "solution-review-43", "supersedes_snapshot_id": None,
            "supersedes_sha256": None, "approve_plan": None,
        }
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
        legacy_solution = runtime.promote(self.root, self.args(workflow="architecture"))
        self.assertEqual("FACTORY_BMAD_SOLUTION_CONTEXT_REQUIRED", legacy_solution["reason_code"])
        prohibited = runtime.promote(self.root, self.args(workflow="create-architecture"))
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
        for snapshot_id in ("latest", "LATEST", "receipts", "RECEIPTS", "Install-Receipts", "INSTALL-RECEIPTS"):
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

    def test_solution_context_directory_preview_apply_reuse_and_rollback(self):
        preview = runtime.promote(self.root, self.solution_args())
        self.assertEqual("PLAN_READY", preview["state"])
        self.assertEqual(2, preview["plan"]["schema_version"])
        self.assertEqual("SOLUTION_CONTEXT", preview["plan"]["evidence_type"])
        self.assertEqual("EVIDENCE_ONLY", preview["plan"]["authority"])
        self.assertEqual("1.1.0", preview["plan"]["policy_version"])
        applied = runtime.promote(self.root, self.solution_args(approve_plan=preview["plan"]["plan_id"]))
        self.assertEqual("APPLIED", applied["state"])
        snapshot = self.root / "docs/upstream/bmad/solution-v1"
        manifest = json.loads((snapshot / "SNAPSHOT_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual({"content/decisions/ADR-1.md", "content/ux.md"}, set(manifest["artifacts"]))
        self.assertEqual("solution-review-43", manifest["provenance"]["plan_identity"])
        self.assertEqual("REUSABLE", runtime.promote(self.root, self.solution_args())["state"])
        rollback_preview = runtime.rollback(self.root, applied["receipt"], None)
        self.assertEqual("PLAN_READY", rollback_preview["state"])
        self.assertEqual("APPLIED", runtime.rollback(self.root, applied["receipt"], rollback_preview["plan"]["plan_id"])["state"])

    def test_solution_context_is_immutable_when_draft_changes(self):
        preview = runtime.promote(self.root, self.solution_args())
        applied = runtime.promote(self.root, self.solution_args(approve_plan=preview["plan"]["plan_id"]))
        snapshot_file = self.root / "docs/upstream/bmad/solution-v1/content/ux.md"
        frozen = snapshot_file.read_bytes()
        (self.root / "_bmad-output/solution/ux.md").write_text("# changed draft\n", encoding="utf-8")
        self.assertEqual(frozen, snapshot_file.read_bytes())
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_IMMUTABLE_CONFLICT", runtime.promote(self.root, self.solution_args())["reason_code"])
        manifest = json.loads((self.root / "docs/upstream/bmad/solution-v1/SNAPSHOT_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual(applied["aggregate_sha256"], manifest["aggregate_sha256"])

    def test_solution_context_requires_typed_evidence_only_plan_identity(self):
        self.assertEqual("FACTORY_BMAD_AUTHORITY_INVALID", runtime.promote(self.root, self.solution_args(authority="BINDING"))["reason_code"])
        self.assertEqual("FACTORY_BMAD_EVIDENCE_TYPE_INVALID", runtime.promote(self.root, self.solution_args(evidence_type="SPEC"))["reason_code"])
        self.assertEqual("FACTORY_BMAD_PLAN_IDENTITY_INVALID", runtime.promote(self.root, self.solution_args(plan_identity=""))["reason_code"])
        self.assertEqual("PLAN_READY", runtime.promote(self.root, self.solution_args(workflow="architecture"))["state"])
        self.assertEqual("PLAN_READY", runtime.promote(self.root, self.solution_args(workflow="spec"))["state"])
        self.assertEqual("FACTORY_BMAD_WORKFLOW_PROHIBITED", runtime.promote(self.root, self.solution_args(workflow="create-architecture"))["reason_code"])

    def test_solution_context_rejects_empty_or_symlinked_content(self):
        empty = self.root / "_bmad-output/empty"
        empty.mkdir()
        self.assertEqual("FACTORY_BMAD_SOURCE_EMPTY", runtime.promote(self.root, self.solution_args(source="_bmad-output/empty"))["reason_code"])
        outside = self.root / "outside.md"
        outside.write_text("outside\n", encoding="utf-8")
        (self.root / "_bmad-output/solution/link.md").symlink_to(outside)
        self.assertEqual("FACTORY_BMAD_SYMLINK_REJECTED", runtime.promote(self.root, self.solution_args())["reason_code"])

    def test_solution_context_supersession_is_exact_and_preserves_prior_snapshot(self):
        first_preview = runtime.promote(self.root, self.solution_args())
        first = runtime.promote(self.root, self.solution_args(approve_plan=first_preview["plan"]["plan_id"]))
        prior_manifest = self.root / "docs/upstream/bmad/solution-v1/SNAPSHOT_MANIFEST.json"
        prior_bytes = prior_manifest.read_bytes()
        (self.root / "_bmad-output/solution/ux.md").write_text("# UX v2\n", encoding="utf-8")
        second_args = self.solution_args(
            snapshot_id="solution-v2", plan_identity="solution-review-44",
            supersedes_snapshot_id="solution-v1", supersedes_sha256=first["aggregate_sha256"],
        )
        second_preview = runtime.promote(self.root, second_args)
        self.assertEqual("PLAN_READY", second_preview["state"])
        second_args.approve_plan = second_preview["plan"]["plan_id"]
        self.assertEqual("APPLIED", runtime.promote(self.root, second_args)["state"])
        self.assertEqual(prior_bytes, prior_manifest.read_bytes())
        invalid = runtime.promote(self.root, self.solution_args(snapshot_id="solution-v3", supersedes_snapshot_id="solution-v1"))
        self.assertEqual("FACTORY_BMAD_SUPERSESSION_INVALID", invalid["reason_code"])


if __name__ == "__main__":
    unittest.main()
