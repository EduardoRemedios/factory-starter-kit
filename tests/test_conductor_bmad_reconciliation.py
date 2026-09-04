import importlib.util
import sqlite3
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, runtime, seed_bmad, seed_factory, seed_git


CONTEXT_SPEC = importlib.util.spec_from_file_location(
    "conductor_bmad_layout_context_index",
    REPO_ROOT / "scripts/conductor_context_index.py",
)
context_index = importlib.util.module_from_spec(CONTEXT_SPEC)
assert CONTEXT_SPEC.loader is not None
CONTEXT_SPEC.loader.exec_module(context_index)


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

    def test_nested_remediation_preview_preserves_inventory_and_link_impact_without_writes(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name); seed_git(root); seed_factory(root); seed_bmad(root / "bmad")
        architecture = root / "bmad/_bmad-output/planning/architecture.md"
        architecture.parent.mkdir(parents=True)
        architecture.write_text("# Candidate architecture\n", encoding="utf-8")
        readme = root / "README.md"
        readme.write_text("See [legacy architecture](bmad/_bmad-output/planning/architecture.md).\n", encoding="utf-8")

        before = runtime.tree_inventory(root)
        report = runtime.reconcile_brownfield(root)
        self.assertEqual(before, runtime.tree_inventory(root))
        self.assertEqual("nested_active", report["layout"]["state"])
        self.assertEqual(1, len(report["remediation_previews"]))
        preview = report["remediation_previews"][0]
        self.assertEqual("RELOCATION_PREVIEW_ONLY", preview["operation"])
        self.assertEqual("bmad", preview["source"])
        self.assertEqual("docs/adapters/bmad/legacy-evidence/bmad", preview["target"])
        self.assertFalse(preview["target_collision"])
        self.assertEqual([], preview["mutations"])
        inventory = {item["path"]: item for item in preview["source_inventory"]}
        self.assertEqual(runtime.digest_file(architecture), inventory["bmad/_bmad-output/planning/architecture.md"]["sha256"])
        impacts = {(item["path"], item["line"]) for item in preview["link_impacts"]}
        self.assertIn(("README.md", 1), impacts)

    def test_fixed_archive_inventory_is_hash_preserving_and_inert(self):
        archive = self.root / runtime.policy.LEGACY_EVIDENCE_ROOT / "bmad-legacy-spike-1"
        source = archive / "_bmad/_config/manifest.yaml"
        source.parent.mkdir(parents=True)
        source.write_text("installation:\n  version: historical\n", encoding="utf-8")
        before = runtime.tree_inventory(self.root)
        report = runtime.reconcile_brownfield(self.root)
        self.assertEqual(before, runtime.tree_inventory(self.root))
        inventory = {item["path"]: item for item in report["legacy_archive_inventory"]}
        relative = source.relative_to(self.root).as_posix()
        self.assertEqual("file", inventory[relative]["kind"])
        self.assertEqual(runtime.digest_file(source), inventory[relative]["sha256"])
        self.assertEqual([], report["remediation_previews"])

    def test_legacy_archive_has_zero_index_and_stage_a_hits_while_promoted_context_is_recalled(self):
        temporary = tempfile.TemporaryDirectory(); self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        legacy_marker = "CONDUCTOR_BMAD_LEGACY_MUST_NOT_RECALL"
        promoted_marker = "CONDUCTOR_BMAD_SELECTED_SOLUTION_CONTEXT_MUST_RECALL"
        legacy = root / runtime.policy.LEGACY_EVIDENCE_ROOT / "bmad-legacy-spike-1/architecture.md"
        promoted = root / "docs/upstream/bmad/solution-v1/content/architecture.md"
        legacy.parent.mkdir(parents=True); promoted.parent.mkdir(parents=True)
        legacy.write_text(f"# Legacy\n{legacy_marker}\n", encoding="utf-8")
        promoted.write_text(f"# Selected\n{promoted_marker}\n", encoding="utf-8")
        database = root / "context.sqlite3"

        context_index.build_context_index(root, database)
        described = context_index.describe_context(root, database)
        self.assertNotIn(legacy.relative_to(root).as_posix(), described["sources"])
        self.assertIn(promoted.relative_to(root).as_posix(), described["sources"])
        self.assertEqual(0, context_index.recall_context(root, legacy_marker, database)["match_count"])
        self.assertGreater(context_index.recall_context(root, promoted_marker, database)["match_count"], 0)

        with sqlite3.connect(database) as connection:
            legacy_chunks = connection.execute(
                "SELECT COUNT(*) FROM chunks WHERE content LIKE ?", (f"%{legacy_marker}%",)
            ).fetchone()[0]
            legacy_facts = connection.execute(
                "SELECT COUNT(*) FROM facts WHERE source_path = ?", (legacy.relative_to(root).as_posix(),)
            ).fetchone()[0]
        self.assertEqual(0, legacy_chunks)
        self.assertEqual(0, legacy_facts)

        report_path = root / "stage-a-report.md"
        context_index.write_context_report(
            root=root,
            output_path=report_path,
            profile="stage-a",
            scope="RUN_20990101_0000_layout_fixture",
            focus_terms=[legacy_marker, promoted_marker],
            db_path=database,
        )
        report = report_path.read_text(encoding="utf-8")
        self.assertNotIn(f"`{legacy.relative_to(root).as_posix()}:", report)
        self.assertIn(f"`{promoted.relative_to(root).as_posix()}:", report)


if __name__ == "__main__":
    unittest.main()
