import hashlib
import json
import os
import re
import subprocess
import unittest
from pathlib import Path

from tests import test_conductor_plugin_composition as composition
from tests.test_conductor_plugin_status import inventory


LIVE_REQUESTED = os.environ.get("CONDUCTOR_PLUGIN_COMPOSITION_LIVE") == "1"


def normalized_file_bytes(path: Path) -> bytes:
    data = path.read_bytes()
    if path != Path.home() / ".claude.json":
        return data
    value = json.loads(data)
    inline = value.get("pluginUsage", {}).get("factory@inline")
    if isinstance(inline, dict):
        inline.pop("lastUsedAt", None)
        inline.pop("usageCount", None)
    skill_usage = value.get("skillUsage", {})
    if isinstance(skill_usage, dict):
        for name, usage in skill_usage.items():
            if name.startswith("factory:") and isinstance(usage, dict):
                usage.pop("lastUsedAt", None)
                usage.pop("usageCount", None)
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def state_digest(paths: tuple[Path, ...]) -> str:
    digest = hashlib.sha256()
    for root in paths:
        digest.update(str(root).encode())
        digest.update(b"\0")
        if root.is_symlink():
            digest.update(b"symlink\0")
            digest.update(os.readlink(root).encode())
            continue
        if root.is_file():
            digest.update(b"file\0")
            digest.update(normalized_file_bytes(root))
            continue
        if not root.is_dir():
            digest.update(b"absent\0")
            continue
        digest.update(b"dir\0")
        for path in sorted(root.rglob("*")):
            relative = path.relative_to(root).as_posix()
            digest.update(relative.encode())
            digest.update(b"\0")
            if path.is_symlink():
                digest.update(b"symlink\0")
                digest.update(os.readlink(path).encode())
            elif path.is_file():
                digest.update(b"file\0")
                digest.update(normalized_file_bytes(path))
            elif path.is_dir():
                digest.update(b"dir\0")
    return digest.hexdigest()


def default_claude_paths() -> tuple[Path, ...]:
    user_root = Path.home()
    return (
        user_root / ".claude.json",
        user_root / ".claude/settings.json",
        user_root / ".claude/plugins",
        user_root / ".claude/cache",
    )


def run_claude(
    args: list[str], *, cwd: Path, environment: dict[str, str], timeout: int = 120
) -> subprocess.CompletedProcess[str]:
    binary = environment.get("CONDUCTOR_CLAUDE_BIN")
    if not binary:
        raise AssertionError("CONDUCTOR_CLAUDE_BIN is required")
    return subprocess.run(
        [binary, *args],
        cwd=cwd,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


@unittest.skipUnless(
    LIVE_REQUESTED,
    "live Claude composition runs only through its dedicated verification command",
)
class FactoryPluginCompositionLiveTests(unittest.TestCase):
    def test_two_lane_dependency_and_namespaced_routing(self):
        environment = os.environ.copy()
        required = (
            "CONDUCTOR_CLAUDE_BIN",
            "CONDUCTOR_CLAUDE_VERSION_PREFIX",
            "CONDUCTOR_BMAD_LIVE_ROOT",
            "CONDUCTOR_BMAD_LIVE_CONFIG_DIR",
            "CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT",
            "CONDUCTOR_BMAD_LIVE_EVIDENCE_ROOT",
            "CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE",
            "CONDUCTOR_BMAD_PREFLIGHT_SHA256",
            "CONDUCTOR_BMAD_PERMISSION_RULE",
            "CONDUCTOR_RELEASE_VERSION",
        )
        missing = [name for name in required if not environment.get(name)]
        self.assertEqual([], missing, f"missing live inputs: {missing}")
        verified = subprocess.run(
            [
                str(composition.REPO_ROOT / "scripts/conductor-python"),
                "scripts/verify_conductor_bmad_live_preflight.py",
                "--verify-verdict",
                environment["CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE"],
                "--expected-verdict-sha256",
                environment["CONDUCTOR_BMAD_PREFLIGHT_SHA256"],
                "--expected-claude-bin",
                environment["CONDUCTOR_CLAUDE_BIN"],
                "--expected-config-root",
                environment["CONDUCTOR_BMAD_LIVE_CONFIG_DIR"],
                "--expected-evidence-root",
                environment["CONDUCTOR_BMAD_LIVE_EVIDENCE_ROOT"],
                "--expected-candidate-root",
                environment["CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT"],
                "--expected-live-root",
                environment["CONDUCTOR_BMAD_LIVE_ROOT"],
                "--expected-permission-rule",
                environment["CONDUCTOR_BMAD_PERMISSION_RULE"],
                "--expected-release-version",
                environment["CONDUCTOR_RELEASE_VERSION"],
            ],
            cwd=composition.REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, verified.returncode, verified.stdout + verified.stderr)

        version = run_claude(
            ["--version"], cwd=composition.REPO_ROOT, environment=environment
        )
        self.assertEqual(0, version.returncode, version.stderr)
        self.assertIn(environment["CONDUCTOR_CLAUDE_VERSION_PREFIX"], version.stdout)

        base = Path(environment["CONDUCTOR_BMAD_LIVE_ROOT"])
        config = Path(environment["CONDUCTOR_BMAD_LIVE_CONFIG_DIR"])
        candidate = Path(environment["CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT"])
        self.assertFalse(base.exists() or base.is_symlink())
        self.assertFalse(config.is_symlink())
        base.mkdir(parents=True)
        config.mkdir(parents=True, exist_ok=True)
        project = base / "project"
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)

        original_factory_package = composition.CONDUCTOR_PACKAGE
        composition.CONDUCTOR_PACKAGE = candidate / "plugins/conductor-claude"
        try:
            marketplace, _, companion = composition.make_marketplace(base)
        finally:
            composition.CONDUCTOR_PACKAGE = original_factory_package

        environment.update(
            {
                "CLAUDE_CONFIG_DIR": str(config),
                "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
                "DISABLE_TELEMETRY": "1",
            }
        )
        protected = (*default_claude_paths(), candidate)
        protected_before = state_digest(protected)
        project_before = inventory(project)

        added = run_claude(["plugin", "marketplace", "add", str(marketplace)], cwd=project, environment=environment)
        self.assertEqual(0, added.returncode, added.stdout + added.stderr)
        installed = run_claude(["plugin", "install", "companion-fixture@composition-fixture"], cwd=project, environment=environment)
        self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
        listed = run_claude(["plugin", "list", "--json"], cwd=project, environment=environment)
        self.assertEqual(0, listed.returncode, listed.stdout + listed.stderr)
        plugins = json.loads(listed.stdout)
        by_name = {item.get("id") or item.get("name"): item for item in plugins}
        factory = next(item for name, item in by_name.items() if isinstance(name, str) and name.startswith("factory@"))
        companion_item = next(item for name, item in by_name.items() if isinstance(name, str) and name.startswith("companion-fixture@"))
        self.assertTrue(factory["enabled"])
        self.assertTrue(companion_item["enabled"])
        self.assertNotIn("errors", factory)
        self.assertNotIn("errors", companion_item)
        self.assertEqual(project_before, inventory(project))
        self.assertEqual(protected_before, state_digest(protected))

        routing_environment = environment.copy()
        session_only = [
            "--plugin-dir", str(candidate / "plugins/conductor-claude"),
            "--plugin-dir", str(companion),
            "--print", "--output-format", "json", "--no-session-persistence",
            "--setting-sources", "", "--tools", "Bash",
            "--allowedTools", environment["CONDUCTOR_BMAD_PERMISSION_RULE"],
            "--permission-mode", "dontAsk",
        ]
        doctor = run_claude([*session_only, "/conductor:doctor Return only state, reason_code, and mutations."], cwd=project, environment=routing_environment)
        self.assertEqual(0, doctor.returncode, doctor.stdout + doctor.stderr)
        self.assertIn("CONDUCTOR_PROJECT_NOT_CONFIGURED", json.loads(doctor.stdout)["result"])
        greenfield = run_claude([*session_only, "/conductor:greenfield Return only state, reason_code, plan_id, and mutations; do not enumerate planned files."], cwd=project, environment=routing_environment)
        self.assertEqual(0, greenfield.returncode, greenfield.stdout + greenfield.stderr)
        greenfield_output = json.loads(greenfield.stdout)["result"]
        self.assertIn("CONDUCTOR_PLAN_READY", greenfield_output)
        self.assertIsNotNone(re.search(r"\b[0-9a-f]{64}\b", greenfield_output))
        self.assertEqual(project_before, inventory(project))
        self.assertEqual(protected_before, state_digest(protected))
        self.assertTrue((config / "plugins").is_dir())


if __name__ == "__main__":
    unittest.main()
