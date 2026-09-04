from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts/merge_preflight.sh"


def run_git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def write(path: Path, text: str, *, executable: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if executable:
        path.chmod(0o755)


def make_repo(root: Path) -> Path:
    repo = root / "repo"
    repo.mkdir()
    run_git(repo, "init", "-q", "-b", "main")
    run_git(repo, "config", "user.email", "test@example.com")
    run_git(repo, "config", "user.name", "Test")
    write(repo / "scripts/merge_preflight.sh", SCRIPT.read_text(encoding="utf-8"), executable=True)
    write(
        repo / "scripts/knowledge_lint.sh",
        "#!/usr/bin/env bash\necho 'knowledge_lint: PASS'\n",
        executable=True,
    )
    write(
        repo / "scripts/conductor-python",
        '#!/usr/bin/env bash\nexec python3 "$@"\n',
        executable=True,
    )
    write(
        repo / "tests/test_trivial.py",
        "import unittest\n\n\nclass TrivialTests(unittest.TestCase):\n"
        "    def test_passes(self):\n        self.assertTrue(True)\n",
    )
    run_git(repo, "add", "-A")
    run_git(repo, "commit", "-q", "-m", "seed")
    bare = root / "origin.git"
    run_git(root, "clone", "-q", "--bare", str(repo), str(bare))
    run_git(repo, "remote", "add", "origin", str(bare))
    run_git(repo, "fetch", "-q", "origin")
    return repo


def run_preflight(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["bash", "scripts/merge_preflight.sh"],
        cwd=repo,
        capture_output=True,
        text=True,
    )


def summary_text(repo: Path) -> str:
    summaries = sorted((repo / "artifacts/merge_preflight").rglob("SUMMARY.md"))
    assert summaries, "no SUMMARY.md written"
    return summaries[-1].read_text(encoding="utf-8")


class MergePreflightTests(unittest.TestCase):
    def test_clean_synced_repo_is_merge_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = make_repo(Path(temp_dir))
            completed = run_preflight(repo)
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            text = summary_text(repo)
            self.assertIn("Verdict: MERGE_READY", text)
            self.assertNotIn("| FAIL |", text)

    def test_dirty_tracked_tree_is_not_merge_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = make_repo(Path(temp_dir))
            (repo / "tests/test_trivial.py").write_text(
                "import unittest\n\n\nclass TrivialTests(unittest.TestCase):\n"
                "    def test_passes(self):\n        self.assertTrue(True)\n\n# dirty\n",
                encoding="utf-8",
            )
            completed = run_preflight(repo)
            self.assertNotEqual(0, completed.returncode)
            text = summary_text(repo)
            self.assertIn("Verdict: NOT_MERGE_READY", text)
            self.assertIn("| clean_worktree | FAIL", text)

    def test_unsynced_base_is_not_merge_ready(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = make_repo(Path(temp_dir))
            bare = Path(temp_dir) / "origin.git"
            mover = Path(temp_dir) / "mover"
            run_git(Path(temp_dir), "clone", "-q", str(bare), str(mover))
            run_git(mover, "config", "user.email", "test@example.com")
            run_git(mover, "config", "user.name", "Test")
            (mover / "moved.txt").write_text("base moved\n", encoding="utf-8")
            run_git(mover, "add", "-A")
            run_git(mover, "commit", "-q", "-m", "base moves ahead")
            run_git(mover, "push", "-q", "origin", "main")
            completed = run_preflight(repo)
            self.assertNotEqual(0, completed.returncode)
            text = summary_text(repo)
            self.assertIn("Verdict: NOT_MERGE_READY", text)
            self.assertIn("| base_sync | FAIL", text)


if __name__ == "__main__":
    unittest.main()
