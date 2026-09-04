import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PREFLIGHT = REPO_ROOT / "scripts/verify_conductor_bmad_live_preflight.py"
CONTRACT = REPO_ROOT / "tests/plugin_fixtures/conductor_bmad_live_verifier_contract.json"
SOURCE_COUPLING = REPO_ROOT / "tests/plugin_fixtures/conductor_bmad_025_source_coupling.json"


class FactoryBmadLivePreflightTests(unittest.TestCase):
    def invoke(
        self,
        root: Path,
        *,
        permission_rule: str = "Bash(python3 *)",
        config_root: Path | None = None,
        omit_journey: str | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], Path, dict[str, Path]]:
        root = root.resolve(strict=True)
        candidate = root / "candidate"
        (candidate / "plugin-src/conductor").mkdir(parents=True)
        (candidate / "plugin-src/conductor-bmad").mkdir(parents=True)
        (candidate / ".claude-plugin").mkdir()
        (candidate / "plugin-src/conductor/manifest.json").write_text(
            json.dumps({"version": "0.3.1"}), encoding="utf-8"
        )
        (candidate / "plugin-src/conductor-bmad/manifest.json").write_text(
            json.dumps({"version": "0.3.1", "conductor_dependency": "~0.3.1"}),
            encoding="utf-8",
        )
        (candidate / ".claude-plugin/marketplace.json").write_text(
            json.dumps(
                {
                    "plugins": [
                        {"name": "conductor", "version": "0.3.1"},
                        {"name": "conductor-bmad", "version": "0.3.1"},
                    ]
                }
            ),
            encoding="utf-8",
        )
        binary = root / "claude"
        binary.write_text(
            "#!/bin/sh\n"
            "touch \"$(dirname \"$0\")/claude-invoked\"\n"
            "exit 99\n",
            encoding="utf-8",
        )
        binary.chmod(0o755)
        config = config_root or root / "config"
        evidence = root / "evidence"
        journeys = [root / name for name in ("greenfield", "brownfield-neither", "brownfield-bmad")]
        protected = root / "protected-preimages"
        protected.mkdir()
        protected_arguments: list[str] = []
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        for role in contract["protected_root_roles"]:
            manifest = protected / f"{role}.json"
            manifest.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "root": str(root / "protected" / role),
                        "entries": [],
                        "entry_count": 0,
                        "aggregate_sha256": "0" * 64,
                    }
                ),
                encoding="utf-8",
            )
            protected_arguments.extend(("--protected-preimage", f"{role}={manifest}"))
        output = evidence / "preflight.json"
        command = [
            str(REPO_ROOT / "scripts/conductor-python"),
            str(PREFLIGHT),
            "--contract",
            str(CONTRACT),
            "--claude-bin",
            str(binary),
            "--observed-version",
            "2.1.228",
            "--supported-version-prefix",
            "2.1.",
            "--permission-mode",
            "dontAsk",
            "--permission-rule",
            permission_rule,
            "--release-version",
            "0.3.1",
            "--bmad-version",
            "6.10.0",
            "--config-root",
            str(config),
            "--evidence-root",
            str(evidence),
            "--candidate-root",
            str(candidate),
            "--source-coupling",
            str(SOURCE_COUPLING),
            "--output",
            str(output),
            *protected_arguments,
        ]
        for name, path in zip(("greenfield", "brownfield-neither", "brownfield-bmad"), journeys):
            if name == omit_journey:
                continue
            command.extend(("--journey-root", f"{name}={path}"))
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        return completed, output, {
            "binary": binary,
            "candidate": candidate,
            "config": config,
            "evidence": evidence,
            "live_root": journeys[0],
        }

    def test_valid_contract_writes_digest_bound_pass_without_invoking_binary(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed, output, inputs = self.invoke(Path(temporary))
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
            verdict = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("PASS", verdict["state"])
            self.assertRegex(verdict["verdict_sha256"], r"^[0-9a-f]{64}$")
            self.assertFalse((Path(temporary) / "claude-invoked").exists())

            verified = subprocess.run(
                [
                    str(REPO_ROOT / "scripts/conductor-python"),
                    str(PREFLIGHT),
                    "--verify-verdict",
                    str(output),
                    "--expected-verdict-sha256",
                    verdict["verdict_sha256"],
                    "--expected-claude-bin",
                    str(inputs["binary"]),
                    "--expected-config-root",
                    str(inputs["config"]),
                    "--expected-evidence-root",
                    str(inputs["evidence"]),
                    "--expected-candidate-root",
                    str(inputs["candidate"]),
                    "--expected-live-root",
                    str(inputs["live_root"]),
                    "--expected-permission-rule",
                    "Bash(python3 *)",
                    "--expected-release-version",
                    "0.3.1",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, verified.returncode, verified.stdout + verified.stderr)

    def test_live_preflight_fixtures_are_release_owned(self):
        for path in (CONTRACT, SOURCE_COUPLING):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), path)
                relative = path.relative_to(REPO_ROOT).as_posix()
                self.assertTrue(relative.startswith("tests/plugin_fixtures/"))
                self.assertNotIn("docs/Conductor/runs/", relative)

    def test_legacy_permission_is_retained_as_blocked_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            for rule in ("Bash(python3:*)", "Bash(*)"):
                with self.subTest(rule=rule):
                    root = Path(temporary) / rule.replace("/", "_").replace("*", "all")
                    root.mkdir()
                    completed, output, _ = self.invoke(root, permission_rule=rule)
                    self.assertEqual(1, completed.returncode)
                    verdict = json.loads(output.read_text(encoding="utf-8"))
                    self.assertEqual("BLOCKED", verdict["state"])
                    self.assertIn("CONDUCTOR_BMAD_PERMISSION_RULE_INVALID", verdict["reason_codes"])

    def test_realpath_overlap_is_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            completed, output, _ = self.invoke(
                root, config_root=root / "candidate" / "config"
            )
            self.assertEqual(1, completed.returncode)
            verdict = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn("CONDUCTOR_BMAD_ROOT_OVERLAP", verdict["reason_codes"])

    def test_missing_journey_root_is_blocked_before_live_use(self):
        with tempfile.TemporaryDirectory() as temporary:
            completed, output, _ = self.invoke(
                Path(temporary), omit_journey="greenfield"
            )
            self.assertEqual(1, completed.returncode)
            verdict = json.loads(output.read_text(encoding="utf-8"))
            self.assertIn(
                "CONDUCTOR_BMAD_JOURNEY_ROOT_INVALID", verdict["reason_codes"]
            )

    def test_live_assets_have_no_stale_permission_cleanup_or_config_drop(self):
        composition = (REPO_ROOT / "tests/test_conductor_plugin_composition_live.py").read_text()
        bmad_live = (REPO_ROOT / "tests/test_conductor_bmad_claude_live.py").read_text()
        shell = (REPO_ROOT / "scripts/verify_conductor_bmad_claude_composition.sh").read_text()
        self.assertNotIn("Bash(python3:*)", composition)
        self.assertNotIn("2.1.218", composition)
        self.assertNotIn("routing_environment = os.environ.copy()", composition)
        self.assertIn('CONDUCTOR_PLUGIN_COMPOSITION_LIVE") == "1"', composition)
        self.assertNotIn("TemporaryDirectory", bmad_live)
        self.assertNotIn("trap 'rm -rf", shell)
        self.assertNotIn("mktemp -d", shell)
        self.assertIn("CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE", shell)
        self.assertIn("CONDUCTOR_BMAD_LIVE_ROOT", shell)
        self.assertLess(
            shell.index("export CLAUDE_CONFIG_DIR"),
            shell.index('"$CLAUDE_BIN" --version'),
        )


if __name__ == "__main__":
    unittest.main()
