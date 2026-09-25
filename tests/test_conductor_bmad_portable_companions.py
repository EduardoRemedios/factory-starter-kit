"""Git-bound repository companions: approve content and Git context once, verify each checkout locally (synthetic only)."""
import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_repository_companions import external_source, validate_snapshot, runtime
from tests.test_conductor_bmad_governed_automation import real_git


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def commit_all(root: Path, message: str) -> str:
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", message)
    return git(root, "rev-parse", "HEAD")


class PortableCompanionTests(unittest.TestCase):
    def grooming(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        base = Path(temporary.name).resolve()
        root = base / "grooming"
        root.mkdir()
        directory, args = external_source(root)
        real_git(root)
        args.git_binding = True
        return base, root, directory, args

    def approve(self, root, args):
        preview = runtime.promote(root, args)
        self.assertEqual("PLAN_READY", preview["state"], preview)
        args.approve_plan = preview["plan"]["plan_id"]
        applied = runtime.promote(root, args)
        self.assertEqual("APPLIED", applied["state"], applied)
        return preview["plan"], applied

    def feature(self, base, root, name="feature", ref="HEAD"):
        other = base / name
        subprocess.run(["git", "clone", "-q", str(root), str(other)], check=True, capture_output=True)
        git(other, "checkout", "-q", "-b", name, ref)
        for key, value in (("user.email", "fixture@example.invalid"), ("user.name", "Fixture")):
            git(other, "config", key, value)
        return other

    def test_plan_has_git_context_and_no_absolute_root(self):
        base, root, _, args = self.grooming()
        plan = runtime.promote(root, args)["plan"]
        companions = plan["repository_companions"]
        self.assertEqual("git", companions["binding"])
        self.assertNotIn("target_root", companions)
        self.assertNotIn(str(root), json.dumps(plan))
        self.assertEqual(git(root, "rev-parse", "HEAD"), companions["approval_commit"])
        self.assertEqual(sorted(a["source_path"] for a in plan["source_artifacts"].values()), sorted(companions["git_blobs"]))
        # Same commit in another folder: the same approval identity, so no second content approval.
        other = self.feature(base, root, "same-commit")
        self.assertEqual(plan["plan_id"], runtime.promote(other, args)["plan"]["plan_id"])

    def test_grooming_to_feature_checkout_verifies_without_reapproval(self):
        base, root, _, args = self.grooming()
        plan, applied = self.approve(root, args)
        commit_all(root, "record reviewed snapshot on main")
        feature = self.feature(base, root)
        (feature / "apps").mkdir()
        (feature / "apps/change.ts").write_text("export const x = 1;\n")
        commit_all(feature, "implementation on the feature branch")
        verdict = runtime.verify_checkout(feature, args.snapshot_id)
        self.assertEqual("VERIFIED", verdict["state"], verdict)
        self.assertEqual("git", verdict["binding"])
        self.assertEqual(applied["aggregate_sha256"], verdict["aggregate_sha256"])
        manifest = json.loads((feature / plan["destination"] / "SNAPSHOT_MANIFEST.json").read_text())
        self.assertIsNone(validate_snapshot(feature, plan, manifest))
        self.assertEqual([], [m for m in verdict["mutations"]])

    def test_changed_inputs_tampered_snapshot_and_incompatible_bases_are_rejected(self):
        base, root, _, args = self.grooming()
        plan, _ = self.approve(root, args)
        commit_all(root, "record reviewed snapshot on main")
        cases = {}
        changed = self.feature(base, root, "changed-input")
        (changed / "docs/standards.md").write_text("# Standards v2\n")
        commit_all(changed, "newer main changed an approved input")
        cases["changed-input"] = (changed, "CONDUCTOR_BMAD_CHECKOUT_INPUTS_CHANGED")
        tampered = self.feature(base, root, "tampered")
        frozen = next((tampered / plan["destination"] / "content").rglob("standards.md"))
        frozen.write_text("tampered\n")
        cases["tampered"] = (tampered, "CONDUCTOR_BMAD_SNAPSHOT_INVENTORY_INVALID")
        unrelated = self.feature(base, root, "unrelated")
        git(unrelated, "checkout", "-q", "--orphan", "rewritten")
        commit_all(unrelated, "same files on unrelated history")
        cases["unrelated"] = (unrelated, "CONDUCTOR_BMAD_CHECKOUT_BASE_INCOMPATIBLE")
        for name, (checkout, code) in cases.items():
            with self.subTest(case=name):
                verdict = runtime.verify_checkout(checkout, args.snapshot_id)
                self.assertEqual(code, verdict["reason_code"], verdict)
                if name == "changed-input":
                    self.assertEqual(["docs/standards.md"], verdict["changed"])
                    self.assertIn("+# Standards v2", verdict["diff"]["docs/standards.md"])

    def test_feature_checkout_with_uncommitted_approved_bytes_is_not_verified(self):
        # G3 finding F-3: matching working-tree bytes over a different committed version must not verify.
        base, root, _, args = self.grooming()
        self.approve(root, args)
        commit_all(root, "record reviewed snapshot on main")
        feature = self.feature(base, root)
        standards = feature / "docs/standards.md"
        approved = standards.read_bytes()
        standards.write_text("# Different committed standards\n")
        commit_all(feature, "a different version is committed")
        standards.write_bytes(approved)
        verdict = runtime.verify_checkout(feature, args.snapshot_id)
        self.assertEqual("CONDUCTOR_BMAD_CHECKOUT_INPUT_UNCOMMITTED", verdict["reason_code"], verdict)
        self.assertEqual(["docs/standards.md"], verdict["uncommitted"])

    def test_uncommitted_untracked_and_misused_inputs_cannot_be_approved(self):
        for defect in ("dirty", "staged", "untracked", "no-companion"):
            with self.subTest(defect=defect):
                base, root, directory, args = self.grooming()
                if defect in ("dirty", "staged"):
                    (root / "docs/standards.md").write_text("# Unreviewed edit\n")
                    if defect == "staged":
                        git(root, "add", "docs/standards.md")
                elif defect == "untracked":
                    (root / "docs/new.md").write_text("# New\n")
                    spec = directory / "SPEC.md"
                    spec.write_text(spec.read_text().replace('"details.md",', '"details.md", "../../../../docs/new.md",'))
                    git(root, "add", str(spec.relative_to(root))); git(root, "commit", "-q", "-m", "cite new")
                    args.repo_companion.append("docs/new.md")
                else:
                    args.repo_companion = []
                verdict = runtime.promote(root, args)
                self.assertEqual("BLOCKED", verdict["state"], verdict)
                expected = "CONDUCTOR_BMAD_PROMOTION_ARGUMENTS_INVALID" if defect == "no-companion" else "CONDUCTOR_BMAD_GIT_INPUT_UNCOMMITTED"
                self.assertEqual(expected, verdict["reason_code"])
                self.assertFalse((root / "docs/upstream").exists())

    def test_moving_commit_between_preview_and_approval_is_stale(self):
        base, root, _, args = self.grooming()
        preview = runtime.promote(root, args)
        commit_all(root, "unrelated commit after review")
        args.approve_plan = preview["plan"]["plan_id"]
        self.assertEqual("CONDUCTOR_BMAD_PLAN_APPROVAL_MISMATCH", runtime.promote(root, args)["reason_code"])

    def test_run_citation_and_changed_execution_boundary(self):
        base, root, _, args = self.grooming()
        plan, _ = self.approve(root, args)
        manifest_path = root / plan["destination"] / "SNAPSHOT_MANIFEST.json"
        run = root / "docs/Conductor/runs/RUN_20260925_1000_portable"
        (run / "countersign").mkdir(parents=True)
        cite = {"kind": "upstream_snapshot", "ref": manifest_path.relative_to(root).as_posix(),
                "sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest()}
        (run / "intent_pack.json").write_text(json.dumps({"sources": [cite], "scope_in": ["apps/**"]}))

        def lock():
            digest = hashlib.sha256((run / "intent_pack.json").read_bytes()).hexdigest()
            (run / "countersign/INTENT_LOCK.json").write_text(json.dumps({"decision": "GO", "subject_sha256": digest}))
        lock()
        commit_all(root, "snapshot and locked run")
        feature = self.feature(base, root)
        self.assertEqual("VERIFIED", runtime.verify_checkout(feature, args.snapshot_id, run.name)["state"])
        widened = json.loads((feature / run.relative_to(root) / "intent_pack.json").read_text())
        widened["scope_in"].append("infra/**")
        (feature / run.relative_to(root) / "intent_pack.json").write_text(json.dumps(widened))
        self.assertEqual("CONDUCTOR_BMAD_CHECKOUT_INTENT_STALE", runtime.verify_checkout(feature, args.snapshot_id, run.name)["reason_code"])
        (feature / run.relative_to(root) / "intent_pack.json").write_text(json.dumps({"sources": []}))
        self.assertEqual("CONDUCTOR_BMAD_CHECKOUT_SNAPSHOT_NOT_CITED", runtime.verify_checkout(feature, args.snapshot_id, run.name)["reason_code"])

    def test_root_bound_snapshots_keep_their_contract(self):
        base, root, _, args = self.grooming()
        args.git_binding = False
        plan, _ = self.approve(root, args)
        manifest_path = root / plan["destination"] / "SNAPSHOT_MANIFEST.json"
        before = manifest_path.read_bytes()
        self.assertEqual("root", runtime.verify_checkout(root, args.snapshot_id)["binding"])
        manifest = json.loads(before)
        self.assertIsNone(validate_snapshot(root, plan, manifest))
        commit_all(root, "root-bound snapshot")
        other = self.feature(base, root)
        self.assertEqual("CONDUCTOR_BMAD_SNAPSHOT_ROOT_BOUND_ELSEWHERE", runtime.verify_checkout(other, args.snapshot_id)["reason_code"])
        self.assertIsNotNone(validate_snapshot(other, plan, manifest), "root-bound intake still refuses another root")
        self.assertEqual(before, manifest_path.read_bytes())

    def test_consumer_rejects_git_provenance_tampering(self):
        base, root, _, args = self.grooming()
        plan, _ = self.approve(root, args)
        original = runtime.snapshot_manifest(plan)
        self.assertIsNone(validate_snapshot(root, plan, original))
        other_commit = commit_all(root, "later commit")
        for field, value in (("approval_commit", "0" * 40), ("binding", "path"), ("git_blobs", {}), ("target_root", str(root))):
            with self.subTest(field=field, value=value):
                manifest = json.loads(json.dumps(original))
                manifest["provenance"]["repository_companions"][field] = value
                self.assertIsNotNone(validate_snapshot(root, plan, manifest))
        # A consistent-looking rewrite on disk still breaks the manifest's own aggregate digest.
        path = root / plan["destination"] / "SNAPSHOT_MANIFEST.json"
        manifest = json.loads(path.read_text())
        manifest["provenance"]["repository_companions"]["approval_commit"] = other_commit
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        self.assertEqual("CONDUCTOR_BMAD_MANIFEST_HASH_MISMATCH", runtime.verify_checkout(root, args.snapshot_id)["reason_code"])


if __name__ == "__main__":
    unittest.main()
