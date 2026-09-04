import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("publication", ROOT / "scripts/verify_conductor_bmad_publication.py")
publication = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(publication)


def git(root, *args, input_text=None):
    return subprocess.run(
        ["git", *args], cwd=root, text=True, input=input_text,
        capture_output=True, check=True,
    ).stdout.strip()


class PublicationBoundaryTests(unittest.TestCase):
    def test_internal_evidence_is_never_public(self):
        self.assertFalse(publication.public_path("artifacts/verification/x.txt"))
        self.assertFalse(publication.public_path("docs/Conductor/runs/RUN_x/raw_brief.md"))

    def test_expected_product_paths_are_public(self):
        self.assertTrue(publication.public_path("plugin-src/conductor-bmad/manifest.json"))
        self.assertTrue(publication.public_path("tests/test_conductor_bmad_policy.py"))

    def test_privacy_scan_blocks_local_and_customer_values(self):
        self.assertIn("local_home", publication.scan_privacy("docs/example.md", b"/Users/person/project"))
        self.assertIn("customer", publication.scan_privacy("docs/example.md", b"AuditEdge"))

    def test_privacy_exceptions_are_literal_and_path_scoped(self):
        self.assertEqual([], publication.scan_privacy(__file__.removeprefix(str(ROOT) + "/"), b"AuditEdge"))
        self.assertIn("customer", publication.scan_privacy("tests/another_test.py", b"AuditEdge"))
        self.assertIn("customer", publication.scan_privacy(__file__.removeprefix(str(ROOT) + "/"), b"Sym" + b"phony"))


class RefClassifierTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="publication-ref-test-")
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Factory Test")
        git(self.root, "config", "user.email", "factory@example.invalid")
        (self.root / "seed.txt").write_text("seed\n")
        git(self.root, "add", "seed.txt")
        git(self.root, "commit", "-q", "-m", "seed")

    def tearDown(self):
        self.temp.cleanup()

    def baseline(self):
        return publication.source_identity_snapshot(self.root)

    def assert_stable_ref_failure(self, ref):
        baseline = self.baseline()
        git(self.root, "update-ref", ref, "HEAD")
        with self.assertRaisesRegex(RuntimeError, ref.replace("[", r"\[")):
            publication.validate_source_identity(self.root, baseline)

    def test_volatile_add_remove_and_change_are_disclosed(self):
        remove_ref = publication.VOLATILE_REF_PREFIX + "remove"
        change_ref = publication.VOLATILE_REF_PREFIX + "change"
        add_ref = publication.VOLATILE_REF_PREFIX + "add"
        git(self.root, "update-ref", remove_ref, "HEAD")
        git(self.root, "update-ref", change_ref, "HEAD")
        baseline = self.baseline()
        tree = git(self.root, "rev-parse", "HEAD^{tree}")
        git(self.root, "update-ref", "-d", remove_ref)
        git(self.root, "update-ref", change_ref, tree)
        git(self.root, "update-ref", add_ref, "HEAD")
        result = publication.validate_source_identity(self.root, baseline)["volatile_refs"]
        self.assertEqual([add_ref], [item["ref"] for item in result["added"]])
        self.assertEqual([remove_ref], [item["ref"] for item in result["removed"]])
        self.assertEqual([change_ref], [item["ref"] for item in result["changed"]])

    def test_branch_ref_change_blocks(self):
        self.assert_stable_ref_failure("refs/heads/extra")

    def test_tag_ref_change_blocks(self):
        self.assert_stable_ref_failure("refs/tags/review")

    def test_remote_tracking_ref_change_blocks(self):
        self.assert_stable_ref_failure("refs/remotes/origin/review")

    def test_other_codex_ref_change_blocks(self):
        self.assert_stable_ref_failure("refs/codex/other/review")

    def test_unexpected_ref_namespace_change_blocks(self):
        self.assert_stable_ref_failure("refs/notes/review")

    def test_head_change_blocks(self):
        baseline = self.baseline()
        git(self.root, "commit", "-q", "--allow-empty", "-m", "move head")
        with self.assertRaisesRegex(RuntimeError, "source head drift"):
            publication.validate_source_identity(self.root, baseline)

    def test_remote_change_blocks(self):
        baseline = self.baseline()
        git(self.root, "remote", "add", "review", "https://example.invalid/review.git")
        with self.assertRaisesRegex(RuntimeError, "source remote drift"):
            publication.validate_source_identity(self.root, baseline)

    def test_staged_index_change_blocks(self):
        baseline = self.baseline()
        (self.root / "staged.txt").write_text("staged\n")
        git(self.root, "add", "staged.txt")
        with self.assertRaisesRegex(RuntimeError, "source index is not empty"):
            publication.validate_source_identity(self.root, baseline)

    def test_malformed_and_duplicate_ref_records_block(self):
        with self.assertRaisesRegex(RuntimeError, "invalid ref record"):
            publication.parse_refs(["not-a-ref"])
        head = "0" * 40
        with self.assertRaisesRegex(RuntimeError, "duplicate ref record"):
            publication.parse_refs([f"{head} refs/heads/main", f"{head} refs/heads/main"])


class ProtectedInventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="publication-inventory-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tree = self.root / "protected"
        self.tree.mkdir()
        (self.tree / "file.txt").write_text("before\n", encoding="utf-8")
        (self.tree / "other.txt").write_text("other\n", encoding="utf-8")

    def inventory(self):
        return publication.protected_inventory(self.root, ("protected/",))

    def assert_drift(self, mutation):
        before = self.inventory()
        mutation()
        with self.assertRaisesRegex(RuntimeError, "protected inventory drift"):
            publication.require_inventory_equal(before, self.inventory())

    def test_add_delete_content_mode_and_symlink_mutations_fail(self):
        mutations = {
            "add": lambda: (self.tree / "added.txt").write_text("added\n", encoding="utf-8"),
            "delete": lambda: (self.tree / "other.txt").unlink(),
            "content": lambda: (self.tree / "file.txt").write_text("after\n", encoding="utf-8"),
            "mode": lambda: (self.tree / "file.txt").chmod(0o600),
            "symlink": self.replace_with_symlink,
        }
        for name, mutation in mutations.items():
            with self.subTest(name=name):
                self.tearDown()
                self.setUp()
                self.assert_drift(mutation)

    def replace_with_symlink(self):
        path = self.tree / "file.txt"
        path.unlink()
        path.symlink_to("other.txt")


class CloneVerificationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="publication-clone-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.name", "Factory Test")
        git(self.root, "config", "user.email", "factory@example.invalid")
        (self.root / "seed.txt").write_text("seed\n", encoding="utf-8")
        git(self.root, "add", "seed.txt")
        git(self.root, "commit", "-q", "-m", "seed")

    def candidate(self):
        commit = git(self.root, "rev-parse", "HEAD")
        return {
            "schema": "conductor.publication-candidate.v1",
            "worktree": str(self.root),
            "commit": commit,
            "base_commit": commit,
            "manifest_sha256": "0" * 64,
            "public_paths": ["docs/ROADMAP.md"],
            "source_identity": {},
            "authority_grants": [],
        }

    def test_schema_and_worktree_head_are_exact(self):
        candidate = self.candidate()
        candidate["schema"] = "wrong"
        with self.assertRaisesRegex(RuntimeError, "candidate schema invalid"):
            publication.validate_candidate(candidate)
        candidate = self.candidate()
        candidate["commit"] = "0" * 40
        with self.assertRaisesRegex(RuntimeError, "candidate worktree HEAD mismatch"):
            publication.validate_candidate(candidate)

    def test_tracked_and_untracked_residue_block(self):
        commit = self.candidate()["commit"]
        (self.root / "seed.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "clone worktree is not clean"):
            publication.require_clean_clone(self.root, commit)
        git(self.root, "checkout", "--", "seed.txt")
        (self.root / "untracked.txt").write_text("dirty\n", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "clone worktree is not clean"):
            publication.require_clean_clone(self.root, commit)

    def test_clean_clone_passes_at_exact_commit(self):
        result = publication.verify_clone(self.candidate(), commands=[])
        self.assertEqual("PASS", result["status"])
        self.assertEqual(self.candidate()["commit"], result["commit"])
        self.assertEqual("EMPTY_PORCELAIN_V1_Z", result["final_status"])


if __name__ == "__main__":
    unittest.main()
