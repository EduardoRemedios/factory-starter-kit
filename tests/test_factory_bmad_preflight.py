import json
import os
import subprocess
import sys
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path

from tests.test_factory_bmad_support import REPO_ROOT, runtime, seed_bmad, seed_factory


ADAPTER = REPO_ROOT / "plugin-src/factory-bmad/project-adapter"
RUN_ID = "RUN_20260810_2100_example"


class FactoryBmadPreflightTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(); self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name); seed_factory(self.root); seed_bmad(self.root, capabilities=True)
        preview = runtime.intake(self.root, "claude", None)
        self.assertEqual("PLAN_READY", preview["state"])
        self.assertEqual("APPLIED", runtime.intake(self.root, "claude", preview["plan"]["plan_id"])["state"])
        source = self.root / "_bmad-output/product/brief.md"; source.parent.mkdir(parents=True); source.write_text("# approved\n", encoding="utf-8")
        args = Namespace(source="_bmad-output/product/brief.md", snapshot_id="example-v1", workflow="product-brief", reviewer="PO", review_ref="BR-1", review_qualifier=None, approve_plan=None)
        preview = runtime.promote(self.root, args); args.approve_plan = preview["plan"]["plan_id"]
        applied = runtime.promote(self.root, args)
        self.digest = applied["aggregate_sha256"]
        run = self.root / "docs/Factory/runs" / RUN_ID; run.mkdir(parents=True)
        self.brief = run / "raw_brief.md"
        self.write_brief()

    def write_brief(self, snapshot="example-v1", digest=None, authority="EVIDENCE_ONLY", freeze="Brief Purple PASS", qualifier=None, extra=""):
        qualifier_line = f"- BMAD Review Qualifier: `{qualifier}`\n" if qualifier else ""
        self.brief.write_text(
            "# Brief\n\n## BMAD upstream evidence\n\n"
            f"- BMAD Snapshot ID: `{snapshot}`\n"
            f"- BMAD Snapshot SHA-256: `{digest or self.digest}`\n"
            f"- BMAD Authority: `{authority}`\n"
            f"- BMAD Context Freeze: `{freeze}`\n{qualifier_line}{extra}", encoding="utf-8")

    def run_preflight(self):
        completed = subprocess.run(["python3", str(ADAPTER / "factory_project_preflight"), "--run", RUN_ID, "--json"], cwd=self.root, text=True, capture_output=True)
        self.assertEqual(0, completed.returncode, completed.stderr)
        return json.loads(completed.stdout)

    def test_valid_snapshot_passes(self):
        payload = self.run_preflight()
        self.assertEqual("PASS", payload["status"])
        self.assertEqual("FACTORY_BMAD_PREFLIGHT_PASS", payload["reason_code"])

    def test_prefixed_workflow_alias_promotes_to_preflight_pass(self):
        source = self.root / "_bmad-output/product/prefixed.md"
        source.write_text("# prefixed\n", encoding="utf-8")
        args = Namespace(
            source="_bmad-output/product/prefixed.md",
            snapshot_id="prefixed-v1",
            workflow="bmad-product-brief",
            reviewer="PO",
            review_ref="BR-2",
            review_qualifier=None,
            approve_plan=None,
        )
        preview = runtime.promote(self.root, args)
        self.assertEqual("product-brief", preview["plan"]["workflow"])
        args.approve_plan = preview["plan"]["plan_id"]
        applied = runtime.promote(self.root, args)
        self.digest = applied["aggregate_sha256"]
        self.write_brief(snapshot="prefixed-v1")
        manifest = json.loads(
            (
                self.root
                / "docs/upstream/bmad/prefixed-v1/SNAPSHOT_MANIFEST.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual("product-brief", manifest["provenance"]["workflow"])
        self.assertEqual("FACTORY_BMAD_PREFLIGHT_PASS", self.run_preflight()["reason_code"])

    def test_legacy_prefixed_manifest_workflow_still_passes_preflight(self):
        manifest_path = self.root / "docs/upstream/bmad/example-v1/SNAPSHOT_MANIFEST.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["provenance"]["workflow"] = "bmad-product-brief"
        manifest["aggregate_sha256"] = runtime.digest_bytes(
            runtime.canonical(
                {key: value for key, value in manifest.items() if key != "aggregate_sha256"}
            )
        )
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.digest = manifest["aggregate_sha256"]
        self.write_brief()
        self.assertEqual("FACTORY_BMAD_PREFLIGHT_PASS", self.run_preflight()["reason_code"])

    def test_seeded_project_preflight_does_not_write_bytecode(self):
        environment = os.environ.copy()
        environment.pop("PYTHONDONTWRITEBYTECODE", None)
        environment.pop("PYTHONPYCACHEPREFIX", None)
        completed = subprocess.run(
            [sys.executable, "scripts/factory_project_preflight", "--run", RUN_ID, "--json"],
            cwd=self.root, env=environment, text=True, capture_output=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        payload = json.loads(completed.stdout)
        self.assertEqual("FACTORY_BMAD_PREFLIGHT_PASS", payload["reason_code"])
        self.assertEqual([], list(self.root.rglob("*.pyc")))

    def test_review_qualifier_must_match_the_snapshot_manifest(self):
        qualifier = "unvalidated upstream evidence; not binding product intent"
        source = self.root / "_bmad-output/product/qualified.md"
        source.write_text("# qualified\n", encoding="utf-8")
        args = Namespace(
            source="_bmad-output/product/qualified.md",
            snapshot_id="qualified-v1",
            workflow="product-brief",
            reviewer="PO",
            review_ref="BR-2",
            review_qualifier=qualifier,
            approve_plan=None,
        )
        preview = runtime.promote(self.root, args)
        args.approve_plan = preview["plan"]["plan_id"]
        applied = runtime.promote(self.root, args)
        self.digest = applied["aggregate_sha256"]
        self.write_brief(snapshot="qualified-v1", qualifier=qualifier)
        self.assertEqual("FACTORY_BMAD_PREFLIGHT_PASS", self.run_preflight()["reason_code"])
        self.write_brief(snapshot="qualified-v1", qualifier="different")
        self.assertEqual(
            "FACTORY_BMAD_REVIEW_QUALIFIER_MISMATCH",
            self.run_preflight()["reason_code"],
        )

    def test_reserved_snapshot_id_fails_before_lookup(self):
        self.write_brief(snapshot="ReCeIpTs")
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_ID_RESERVED", self.run_preflight()["reason_code"])

    def test_snapshot_inventory_is_exact(self):
        snapshot = self.root / "docs/upstream/bmad/example-v1"
        (snapshot / "extra.txt").write_text("extra\n", encoding="utf-8")
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_INVENTORY_INVALID", self.run_preflight()["reason_code"])

    def test_snapshot_symlink_and_mode_drift_fail(self):
        snapshot = self.root / "docs/upstream/bmad/example-v1"
        artifact = snapshot / "artifact.md"
        artifact.chmod(0o600)
        self.assertEqual("FACTORY_BMAD_ARTIFACT_MODE_MISMATCH", self.run_preflight()["reason_code"])
        artifact.chmod(0o644)
        artifact.unlink()
        artifact.symlink_to(self.root / "_bmad-output/product/brief.md")
        self.assertEqual("FACTORY_BMAD_SNAPSHOT_INVENTORY_INVALID", self.run_preflight()["reason_code"])

    def test_direct_draft_citation_fails(self):
        self.write_brief(extra="See `_bmad-output/product/brief.md`.\n")
        self.assertEqual("FACTORY_BMAD_DRAFT_CITATION", self.run_preflight()["reason_code"])

    def test_seeded_template_does_not_cite_the_forbidden_draft_directory(self):
        template = (self.root / "docs/adapters/bmad/RAW_BRIEF_TEMPLATE.md").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("_bmad-output/", template)

    def test_authority_and_freeze_fail_closed(self):
        self.write_brief(authority="BINDING")
        self.assertEqual("FACTORY_BMAD_AUTHORITY_INVALID", self.run_preflight()["reason_code"])
        self.write_brief(freeze="OPEN")
        self.assertEqual("FACTORY_BMAD_CONTEXT_NOT_FROZEN", self.run_preflight()["reason_code"])

    def test_citation_and_artifact_hash_tamper_fail(self):
        self.write_brief(digest="0" * 64)
        self.assertEqual("FACTORY_BMAD_CITATION_HASH_MISMATCH", self.run_preflight()["reason_code"])
        self.write_brief()
        (self.root / "docs/upstream/bmad/example-v1/artifact.md").write_text("tampered\n", encoding="utf-8")
        self.assertEqual("FACTORY_BMAD_ARTIFACT_HASH_MISMATCH", self.run_preflight()["reason_code"])

    def test_intake_is_seed_only_and_uses_existing_preflight_seam(self):
        declaration = json.loads((self.root / "docs/Factory/PROJECT_PREFLIGHT.json").read_text(encoding="utf-8"))
        self.assertEqual({"schema_version": 1, "timeout_seconds": 60}, declaration)
        self.assertTrue((self.root / "docs/adapters/bmad/CAPABILITY_AUDIT.json").is_file())
        self.assertTrue((self.root / "docs/adapters/bmad/BMAD_RECONCILIATION.json").is_file())
        self.assertTrue((self.root / "scripts/factory_bmad_policy.py").is_file())
        self.assertTrue((self.root / "scripts/factory_bmad_policy_lint").is_file())
        current = runtime.intake(self.root, "claude", None)
        self.assertEqual("FACTORY_BMAD_INTAKE_CURRENT", current["reason_code"])

    def test_capability_and_policy_drift_fail_closed(self):
        audit = self.root / "docs/adapters/bmad/CAPABILITY_AUDIT.json"
        payload = json.loads(audit.read_text(encoding="utf-8")); payload["policy_version"] = "old"
        audit.write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual("FACTORY_BMAD_POLICY_VERSION_DRIFT", self.run_preflight()["reason_code"])

    def test_uncovered_capability_fails_with_ci_reason(self):
        skill = self.root / ".claude/skills/bmad-unknown/SKILL.md"
        skill.parent.mkdir(parents=True); skill.write_text("# unknown\n", encoding="utf-8")
        self.assertEqual("FACTORY_BMAD_CAPABILITY_UNRECOGNIZED", self.run_preflight()["reason_code"])

    def test_existing_different_adapter_file_conflicts(self):
        target = self.root / "docs/Factory/PROJECT_PREFLIGHT.json"
        target.write_text("{}\n", encoding="utf-8")
        payload = runtime.intake(self.root, "claude", None)
        self.assertEqual("FACTORY_BMAD_INTAKE_CONFLICT", payload["reason_code"])


if __name__ == "__main__":
    unittest.main()
