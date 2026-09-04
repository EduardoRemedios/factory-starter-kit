import hashlib
import os
import subprocess
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, seed_bmad, seed_factory, seed_git


REAL_STATE = (Path.home() / ".claude.json", Path.home() / ".claude")


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    if not path.exists() and not path.is_symlink():
        return "ABSENT"
    candidates = [path] if not path.is_dir() or path.is_symlink() else [path, *sorted(path.rglob("*"))]
    for candidate in candidates:
        relative = "." if candidate == path else candidate.relative_to(path).as_posix()
        digest.update(relative.encode())
        if candidate.is_symlink():
            digest.update(b"L")
            digest.update(os.readlink(candidate).encode())
        elif candidate.is_dir():
            digest.update(b"D")
        elif candidate.is_file():
            digest.update(b"F")
            with candidate.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
    return digest.hexdigest()


@unittest.skipUnless(os.environ.get("CONDUCTOR_BMAD_LIVE_CLAUDE") == "1", "isolated authenticated Claude proof not authorized")
class FactoryBmadClaudeLiveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        required = (
            "CONDUCTOR_CLAUDE_BIN",
            "CONDUCTOR_BMAD_LIVE_ROOT",
            "CONDUCTOR_BMAD_LIVE_CONFIG_DIR",
            "CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT",
            "CONDUCTOR_BMAD_LIVE_EVIDENCE_ROOT",
            "CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE",
            "CONDUCTOR_BMAD_PREFLIGHT_SHA256",
            "CONDUCTOR_BMAD_PERMISSION_RULE",
            "CONDUCTOR_RELEASE_VERSION",
        )
        missing = [name for name in required if not os.environ.get(name)]
        if missing:
            raise AssertionError(f"missing live inputs: {missing}")
        cls.claude = Path(os.environ["CONDUCTOR_CLAUDE_BIN"])
        if not cls.claude.is_file():
            raise AssertionError("explicit Claude Code binary unavailable")
        cls.candidate = Path(os.environ["CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT"])
        cls.base = Path(os.environ["CONDUCTOR_BMAD_LIVE_ROOT"])
        cls.config = Path(os.environ["CONDUCTOR_BMAD_LIVE_CONFIG_DIR"])
        if cls.base.exists() or cls.base.is_symlink():
            raise AssertionError("CONDUCTOR_BMAD_LIVE_ROOT must be absent")
        verified = subprocess.run(
            [
                str(REPO_ROOT / "scripts/conductor-python"),
                "scripts/verify_conductor_bmad_live_preflight.py",
                "--verify-verdict",
                os.environ["CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE"],
                "--expected-verdict-sha256",
                os.environ["CONDUCTOR_BMAD_PREFLIGHT_SHA256"],
                "--expected-claude-bin",
                os.environ["CONDUCTOR_CLAUDE_BIN"],
                "--expected-config-root",
                os.environ["CONDUCTOR_BMAD_LIVE_CONFIG_DIR"],
                "--expected-evidence-root",
                os.environ["CONDUCTOR_BMAD_LIVE_EVIDENCE_ROOT"],
                "--expected-candidate-root",
                os.environ["CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT"],
                "--expected-live-root",
                os.environ["CONDUCTOR_BMAD_LIVE_ROOT"],
                "--expected-permission-rule",
                os.environ["CONDUCTOR_BMAD_PERMISSION_RULE"],
                "--expected-release-version",
                os.environ["CONDUCTOR_RELEASE_VERSION"],
            ],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if verified.returncode != 0:
            raise AssertionError(verified.stdout + verified.stderr)
        cls.base.mkdir(parents=True)
        if cls.config.is_symlink():
            raise AssertionError("CONDUCTOR_BMAD_LIVE_CONFIG_DIR must not be a symlink")
        cls.config.mkdir(parents=True, exist_ok=True)
        cls.protected = (*REAL_STATE, cls.candidate)
        cls.real_before = {str(path): tree_digest(path) for path in cls.protected}
        cls.environment = {
            **os.environ,
            "CLAUDE_CONFIG_DIR": str(cls.config),
            "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
            "DISABLE_TELEMETRY": "1",
        }

    @classmethod
    def tearDownClass(cls):
        after = {str(path): tree_digest(path) for path in cls.protected}
        if after != cls.real_before:
            raise AssertionError("protected Claude or candidate state changed during isolated proof")

    def repository(self, *, factory: bool) -> Path:
        root = self.base / ("active" if factory else "inactive")
        if root.exists():
            return root
        root.mkdir(); seed_git(root); seed_bmad(root, capabilities=True)
        if factory:
            seed_factory(root)
        skills = {
            "bmad-architecture": "Architecture workflow fixture",
            "bmad-product-brief": "Product brief workflow fixture",
            "bmad-future-autonomous": "Unknown workflow fixture",
        }
        for name, description in skills.items():
            skill = root / ".claude/skills" / name / "SKILL.md"
            skill.parent.mkdir(parents=True, exist_ok=True)
            skill.write_text(
                f"---\nname: {name}\ndescription: {description}\n---\n\nReturn `{name}:EXPANDED` and do not use other tools.\n",
                encoding="utf-8",
            )
        return root

    def invoke(self, root: Path, prompt: str, *, tools: str = "") -> str:
        command = [
            str(self.claude),
            "--plugin-dir", str(self.candidate / "plugins/conductor-claude"),
            "--plugin-dir", str(self.candidate / "plugins/conductor-bmad-claude"),
            "--setting-sources", "project",
            "--no-session-persistence",
            "--permission-mode", "dontAsk",
            "--tools", tools,
            "--output-format", "stream-json",
            "--include-hook-events",
            "--verbose",
            "--print",
            prompt,
        ]
        completed = subprocess.run(
            command,
            cwd=root,
            env=self.environment,
            text=True,
            capture_output=True,
            timeout=180,
        )
        combined = completed.stdout + "\n" + completed.stderr
        authentication_failures = (
            "login required",
            "not logged in",
            '"error":"authentication_failed"',
        )
        for failure in authentication_failures:
            self.assertNotIn(failure, combined.lower(), combined[-2000:])
        return combined

    def test_direct_allowed_prohibited_unknown_and_inactive_paths(self):
        active = self.repository(factory=True)
        prohibited = self.invoke(active, "/bmad-architecture")
        self.assertIn("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", prohibited)
        unknown = self.invoke(active, "/bmad-future-autonomous")
        self.assertIn("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", unknown)
        allowed = self.invoke(active, "/bmad-product-brief")
        self.assertNotIn("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", allowed)
        inactive = self.invoke(self.repository(factory=False), "/bmad-architecture")
        self.assertNotIn("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", inactive)

    def test_model_initiated_skill_is_denied(self):
        output = self.invoke(
            self.repository(factory=True),
            "Use the bmad-architecture skill through the Skill tool now. Do not choose another skill.",
            tools="Skill",
        )
        self.assertIn("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", output)


if __name__ == "__main__":
    unittest.main()
