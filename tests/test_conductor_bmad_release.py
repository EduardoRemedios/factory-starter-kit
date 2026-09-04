import hashlib
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT


RELEASE_SCRIPT = REPO_ROOT / "scripts/verify_conductor_bmad_single_repo_release.sh"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReleaseFunctionTestCase(unittest.TestCase):
    def run_bash(self, body, *args, evidence_root=None):
        environment = os.environ.copy()
        environment["CONDUCTOR_BMAD_EVIDENCE_ROOT"] = str(evidence_root)
        return subprocess.run(
            [
                "bash",
                "-c",
                'source "$1"\nshift\n' + body,
                "conductor-bmad-release-test",
                str(RELEASE_SCRIPT),
                *(str(arg) for arg in args),
            ],
            cwd=REPO_ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )


class FactoryBmadReleaseGateTests(ReleaseFunctionTestCase):
    def test_middle_failure_stops_direct_caller(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "VM-010.txt"
            result = self.run_bash(
                """
step_one() { echo step_one; }
step_fail() { echo step_fail; return 7; }
step_later() { echo later_release_marker; }
conductor_bmad_vm10_execute "$1" step_one step_fail step_later
""",
                output,
                evidence_root=root / "source-evidence",
            )
            self.assertEqual(7, result.returncode, result.stdout + result.stderr)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(["status=FAIL"], [line for line in lines if line.startswith("status=")])
            self.assertNotIn("status=PASS", lines)
            self.assertNotIn("later_release_marker", lines)
            self.assertEqual("status=FAIL", lines[-1])

    def test_middle_failure_stops_conditional_caller(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "VM-010.txt"
            result = self.run_bash(
                """
step_one() { echo step_one; }
step_fail() { echo step_fail; return 7; }
step_later() { echo later_release_marker; }
if conductor_bmad_vm10_execute "$1" step_one step_fail step_later; then
  exit 0
else
  status=$?
  exit "$status"
fi
""",
                output,
                evidence_root=root / "source-evidence",
            )
            self.assertEqual(7, result.returncode, result.stdout + result.stderr)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(["status=FAIL"], [line for line in lines if line.startswith("status=")])
            self.assertNotIn("status=PASS", lines)
            self.assertNotIn("later_release_marker", lines)
            self.assertEqual("status=FAIL", lines[-1])

    def test_success_writes_one_terminal_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "VM-010.txt"
            result = self.run_bash(
                """
step_one() { echo step_one; }
step_two() { echo step_two; }
conductor_bmad_vm10_execute "$1" step_one step_two
""",
                output,
                evidence_root=root / "source-evidence",
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(["status=PASS"], [line for line in lines if line.startswith("status=")])
            self.assertEqual("status=PASS", lines[-1])


class FactoryBmadAttemptPreservationTests(ReleaseFunctionTestCase):
    def test_source_only_load_has_no_side_effect(self):
        with tempfile.TemporaryDirectory() as temporary:
            evidence = Path(temporary) / "must-not-exist"
            result = self.run_bash(
                'type conductor_bmad_vm10_execute >/dev/null\n',
                evidence_root=evidence,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse(evidence.exists())

    def test_competing_owner_blocks_before_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir()
            result = self.run_bash(
                """
conductor_bmad_lock_acquire "$1" token-one || exit $?
before=$(shasum -a 256 "$1/.release-owner/token" | awk '{print $1}')
if conductor_bmad_lock_acquire "$1" token-two; then
  exit 40
fi
after=$(shasum -a 256 "$1/.release-owner/token" | awk '{print $1}')
[[ "$before" == "$after" ]] || exit 41
conductor_bmad_lock_release "$1" token-one
""",
                root,
                evidence_root=root / "unused-source-root",
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertFalse((root / ".release-owner").exists())

    def test_rapid_attempts_are_distinct_and_digest_equal(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir()
            original = root / "VM-001.txt"
            original.write_text("first-attempt\n", encoding="utf-8")
            first_digest = digest(original)
            result = self.run_bash(
                """
conductor_bmad_lock_acquire "$1" token-one || exit $?
conductor_bmad_archive_previous_attempt "$1" token-one || exit $?
printf 'second-attempt\n' > "$1/VM-001.txt"
conductor_bmad_archive_previous_attempt "$1" token-one || exit $?
conductor_bmad_lock_release "$1" token-one
""",
                root,
                evidence_root=root / "unused-source-root",
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            attempts = sorted(path for path in (root / "attempts").iterdir() if not path.name.startswith("."))
            self.assertEqual(2, len(attempts))
            self.assertNotEqual(attempts[0].name, attempts[1].name)
            snapshots = [attempt / "VM-001.txt" for attempt in attempts]
            self.assertIn(first_digest, {digest(path) for path in snapshots})
            self.assertIn(hashlib.sha256(b"second-attempt\n").hexdigest(), {digest(path) for path in snapshots})
            self.assertFalse(original.exists())

    def test_archive_failure_retains_prior_bytes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir()
            prior = root / "VM-001.txt"
            prior.write_text("retain-me\n", encoding="utf-8")
            before = digest(prior)
            (root / "attempts").write_text("blocks-directory-creation\n", encoding="utf-8")
            result = self.run_bash(
                """
conductor_bmad_lock_acquire "$1" token-one || exit $?
if conductor_bmad_archive_previous_attempt "$1" token-one; then
  exit 40
else
  status=$?
fi
conductor_bmad_lock_release "$1" token-one || exit $?
exit "$status"
""",
                root,
                evidence_root=root / "unused-source-root",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertTrue(prior.exists())
            self.assertEqual(before, digest(prior))

    def test_preexisting_owner_is_retained(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "evidence"
            owner = root / ".release-owner"
            owner.mkdir(parents=True)
            token = owner / "token"
            token.write_text("existing-owner\n", encoding="utf-8")
            before = digest(token)
            result = self.run_bash(
                'conductor_bmad_lock_acquire "$1" token-two\n',
                root,
                evidence_root=root / "unused-source-root",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual(before, digest(token))

    def test_token_mismatch_cannot_remove_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "evidence"
            root.mkdir()
            result = self.run_bash(
                """
conductor_bmad_lock_acquire "$1" token-one || exit $?
printf 'token-two\n' > "$1/.release-owner/token"
conductor_bmad_lock_release "$1" token-one
""",
                root,
                evidence_root=root / "unused-source-root",
            )
            self.assertNotEqual(0, result.returncode)
            self.assertEqual("token-two", (root / ".release-owner/token").read_text(encoding="utf-8").strip())


class FactoryBmadProtectedInventoryTests(ReleaseFunctionTestCase):
    def tree_digest(self, root):
        result = self.run_bash('conductor_bmad_tree_digest "$1"\n', root, evidence_root=root / "unused")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return result.stdout.strip()

    def test_add_delete_content_mode_and_symlink_mutations_change_digest(self):
        for mutation in ("add", "delete", "content", "mode", "symlink"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary) / "protected"
                root.mkdir()
                first = root / "first.txt"
                second = root / "second.txt"
                first.write_text("first\n", encoding="utf-8")
                second.write_text("second\n", encoding="utf-8")
                before = self.tree_digest(root)
                if mutation == "add":
                    (root / "added.txt").write_text("added\n", encoding="utf-8")
                elif mutation == "delete":
                    second.unlink()
                elif mutation == "content":
                    first.write_text("changed\n", encoding="utf-8")
                elif mutation == "mode":
                    first.chmod(0o600)
                else:
                    first.unlink()
                    first.symlink_to("second.txt")
                self.assertNotEqual(before, self.tree_digest(root))


if __name__ == "__main__":
    unittest.main()
