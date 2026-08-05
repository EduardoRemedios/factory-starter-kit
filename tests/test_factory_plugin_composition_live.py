import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tests.test_factory_plugin_composition import FACTORY_PACKAGE, make_marketplace
from tests.test_factory_plugin_status import inventory


LIVE_REQUESTED = any(
    "test_factory_plugin_composition_live" in argument for argument in sys.argv
)


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
    return subprocess.run(
        ["claude", *args],
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
        version = run_claude(
            ["--version"], cwd=Path.cwd(), environment=os.environ.copy()
        )
        self.assertEqual(0, version.returncode, version.stderr)
        self.assertIn("2.1.218", version.stdout)

        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            marketplace, _, companion = make_marketplace(base)
            config = base / "claude-config"
            project = base / "project"
            config.mkdir()
            project.mkdir()
            subprocess.run(["git", "init", "-q", str(project)], check=True)

            environment = os.environ.copy()
            environment.update(
                {
                    "CLAUDE_CONFIG_DIR": str(config),
                    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
                    "DISABLE_TELEMETRY": "1",
                }
            )
            user_before = state_digest(default_claude_paths())
            project_before = inventory(project)

            added = run_claude(
                ["plugin", "marketplace", "add", str(marketplace)],
                cwd=project,
                environment=environment,
            )
            self.assertEqual(0, added.returncode, added.stdout + added.stderr)
            installed = run_claude(
                [
                    "plugin",
                    "install",
                    "companion-fixture@composition-fixture",
                ],
                cwd=project,
                environment=environment,
            )
            self.assertEqual(
                0, installed.returncode, installed.stdout + installed.stderr
            )
            listed = run_claude(
                ["plugin", "list", "--json"],
                cwd=project,
                environment=environment,
            )
            self.assertEqual(0, listed.returncode, listed.stdout + listed.stderr)
            plugins = json.loads(listed.stdout)
            by_name = {
                item.get("id") or item.get("name"): item for item in plugins
            }
            factory = next(
                item
                for name, item in by_name.items()
                if isinstance(name, str) and name.startswith("factory@")
            )
            companion = next(
                item
                for name, item in by_name.items()
                if isinstance(name, str) and name.startswith("companion-fixture@")
            )
            self.assertRegex(factory["version"], r"^0\.2\.0-[0-9a-f]{12}$")
            self.assertTrue(factory["enabled"])
            self.assertTrue(companion["enabled"])
            self.assertNotIn("errors", factory)
            self.assertNotIn("errors", companion)

            self.assertEqual(project_before, inventory(project))
            self.assertEqual(user_before, state_digest(default_claude_paths()))

            routing_environment = os.environ.copy()
            routing_environment.update(
                {
                    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
                    "DISABLE_TELEMETRY": "1",
                }
            )
            session_only = [
                "--plugin-dir",
                str(FACTORY_PACKAGE),
                "--plugin-dir",
                str(companion),
                "--print",
                "--output-format",
                "json",
                "--no-session-persistence",
                "--setting-sources",
                "",
                "--tools",
                "Bash",
                "--allowedTools",
                "Bash(python3 *)",
                "--permission-mode",
                "dontAsk",
            ]

            doctor = run_claude(
                [
                    *session_only,
                    "/factory:doctor Return only state, reason_code, and mutations.",
                ],
                cwd=project,
                environment=routing_environment,
            )
            if doctor.returncode != 0:
                self.assertEqual(project_before, inventory(project))
                self.assertEqual(
                    user_before, state_digest(default_claude_paths())
                )
                try:
                    failure = json.loads(doctor.stdout).get("result", "unknown")
                except json.JSONDecodeError:
                    failure = "non-JSON Claude failure"
                self.fail(f"CLAUDE_ROUTING_AUTH_FAILED: {failure}")
            doctor_output = json.loads(doctor.stdout)["result"]
            self.assertIn("FACTORY_PROJECT_NOT_CONFIGURED", doctor_output)

            greenfield = run_claude(
                [
                    *session_only,
                    "/factory:greenfield Return only state, reason_code, plan_id, and mutations; do not enumerate planned files.",
                ],
                cwd=project,
                environment=routing_environment,
            )
            if greenfield.returncode != 0:
                self.assertEqual(project_before, inventory(project))
                self.assertEqual(
                    user_before, state_digest(default_claude_paths())
                )
                try:
                    failure = json.loads(greenfield.stdout).get(
                        "result", "unknown"
                    )
                except json.JSONDecodeError:
                    failure = "non-JSON Claude failure"
                self.fail(f"CLAUDE_ROUTING_FAILED: {failure}")
            greenfield_output = json.loads(greenfield.stdout)["result"]
            self.assertIn("FACTORY_PLAN_READY", greenfield_output)
            self.assertIsNotNone(re.search(r"\b[0-9a-f]{64}\b", greenfield_output))

            self.assertEqual(project_before, inventory(project))
            self.assertEqual(user_before, state_digest(default_claude_paths()))
            self.assertTrue((config / "plugins").is_dir())


if __name__ == "__main__":
    unittest.main()
