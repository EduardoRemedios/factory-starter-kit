import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.test_factory_plugin_status import inventory, write


REPO_ROOT = Path(__file__).resolve().parent.parent
FACTORY_PACKAGE = REPO_ROOT / "plugins/factory-claude"
FACTORY_SKILLS = {
    "factory:doctor",
    "factory:greenfield",
    "factory:brownfield",
    "factory:progress",
    "factory:run",
    "factory:validate",
    "factory:update",
}
RUNTIME_SPEC = importlib.util.spec_from_file_location(
    "factory_plugin_composition_runtime",
    FACTORY_PACKAGE / "scripts/factory_plugin.py",
)
RUNTIME = importlib.util.module_from_spec(RUNTIME_SPEC)
assert RUNTIME_SPEC.loader
RUNTIME_SPEC.loader.exec_module(RUNTIME)


def claude_with_plugin_cli() -> str:
    candidates = [
        os.environ.get("FACTORY_CLAUDE_BIN"),
        shutil.which("claude"),
        str(Path.home() / ".local/bin/claude"),
    ]
    for candidate in dict.fromkeys(item for item in candidates if item):
        completed = subprocess.run(
            [candidate, "plugin", "validate", "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        if (
            completed.returncode == 0
            and "Usage: claude plugin validate" in completed.stdout
            and "--strict" in completed.stdout
        ):
            return candidate
    raise AssertionError(
        "No Claude Code executable with the plugin validation interface was found"
    )


def dependency_result(
    *, factory_version: str | None, enabled: bool, required: str = "=0.2.0"
) -> dict[str, object]:
    if factory_version is None or not enabled:
        return {"outcome": "halt", "reason": "dependency-unsatisfied"}
    if required != f"={factory_version}":
        return {
            "outcome": "halt",
            "reason": "dependency-version-unsatisfied",
        }
    return {"outcome": "pass", "dependency_resolved": True, "enabled": True}


def plugin_skills(plugin_root: Path) -> set[str]:
    manifest = json.loads(
        (plugin_root / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
    )
    namespace = manifest["name"]
    return {
        f"{namespace}:{path.parent.name}"
        for path in (plugin_root / "skills").glob("*/SKILL.md")
    }


def make_marketplace(base: Path) -> tuple[Path, Path, Path]:
    marketplace = base / "marketplace"
    factory = marketplace / "plugins/factory"
    companion = marketplace / "plugins/companion-fixture"
    shutil.copytree(FACTORY_PACKAGE, factory)
    write(
        companion / ".claude-plugin/plugin.json",
        json.dumps(
            {
                "name": "companion-fixture",
                "version": "1.0.0",
                "description": "Adapter-neutral composition fixture.",
                "author": {"name": "Factory Test"},
                "dependencies": [{"name": "factory", "version": "=0.2.0"}],
            },
            indent=2,
        )
        + "\n",
    )
    write(
        companion / "skills/doctor/SKILL.md",
        "---\nname: doctor\ndescription: Delegate diagnosis.\n---\n\n"
        "Invoke `/factory:doctor` and preserve its result.\n",
    )
    write(
        marketplace / ".claude-plugin/marketplace.json",
        json.dumps(
            {
                "name": "composition-fixture",
                "owner": {"name": "Factory Test"},
                "description": "Temporary adapter-neutral composition proof.",
                "plugins": [
                    {
                        "name": "factory",
                        "source": "./plugins/factory",
                        "version": "0.2.0",
                    },
                    {
                        "name": "companion-fixture",
                        "source": "./plugins/companion-fixture",
                        "version": "1.0.0",
                    },
                ],
            },
            indent=2,
        )
        + "\n",
    )
    subprocess.run(["git", "init", "-q", str(marketplace)], check=True)
    subprocess.run(["git", "-C", str(marketplace), "add", "."], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(marketplace),
            "-c",
            "user.name=Factory Test",
            "-c",
            "user.email=factory-test@example.invalid",
            "commit",
            "-q",
            "-m",
            "composition fixture",
        ],
        check=True,
    )
    for tag in ("factory--v0.2.0", "companion-fixture--v1.0.0"):
        subprocess.run(["git", "-C", str(marketplace), "tag", tag], check=True)
    return marketplace, factory, companion


class FactoryPluginCompositionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.marketplace, self.factory, self.companion = make_marketplace(
            self.base
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_cp01_exact_dependency_and_local_release_tag(self):
        manifest = json.loads(
            (self.companion / ".claude-plugin/plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            [{"name": "factory", "version": "=0.2.0"}],
            manifest["dependencies"],
        )
        tags = subprocess.run(
            ["git", "-C", str(self.marketplace), "tag", "--list"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        self.assertIn("factory--v0.2.0", tags)
        self.assertEqual(
            {"outcome": "pass", "dependency_resolved": True, "enabled": True},
            dependency_result(factory_version="0.2.0", enabled=True),
        )

    def test_cp02_cp03_cp04_dependency_failures_halt(self):
        self.assertEqual(
            "dependency-unsatisfied",
            dependency_result(factory_version=None, enabled=True)["reason"],
        )
        self.assertEqual(
            "dependency-unsatisfied",
            dependency_result(factory_version="0.2.0", enabled=False)["reason"],
        )
        self.assertEqual(
            "dependency-version-unsatisfied",
            dependency_result(factory_version="0.1.0", enabled=True)["reason"],
        )

    def test_cp05_exact_namespaced_skill_inventory(self):
        self.assertEqual(FACTORY_SKILLS, plugin_skills(self.factory))
        self.assertEqual(
            {"companion-fixture:doctor"}, plugin_skills(self.companion)
        )
        self.assertFalse(FACTORY_SKILLS & plugin_skills(self.companion))

    def test_cp06_doctor_is_read_only_and_preserves_base_reason(self):
        root = self.base / "doctor-project"
        root.mkdir()
        before = inventory(root)
        output = RUNTIME.evaluate_doctor(
            root,
            harness="claude",
            platform_name="darwin",
            python_version=(3, 11, 0),
        )
        self.assertEqual("FACTORY_PROJECT_NOT_CONFIGURED", output["reason_code"])
        self.assertEqual([], output["mutations"])
        self.assertEqual(before, inventory(root))

    def test_cp07_greenfield_preview_is_read_only_with_exact_plan(self):
        root = self.base / "preview-project"
        before = inventory(self.base)
        output = RUNTIME.evaluate_setup_plan(
            root,
            mode="greenfield",
            harness="claude",
            payload_root=self.factory / "payload",
            platform_name="darwin",
            python_version=(3, 11, 0),
        )
        self.assertEqual("FACTORY_PLAN_READY", output["reason_code"])
        self.assertEqual(64, len(output["plan_id"]))
        self.assertEqual([], output["mutations"])
        self.assertEqual(before, inventory(self.base))

    def test_cp08_generic_approval_halts_without_mutation(self):
        root = self.base / "approval-project"
        plan = RUNTIME.evaluate_setup_plan(
            root,
            mode="greenfield",
            harness="claude",
            payload_root=self.factory / "payload",
            platform_name="darwin",
            python_version=(3, 11, 0),
        )
        before = inventory(self.base)
        output = RUNTIME.apply_setup_plan(
            root,
            plan=plan,
            approved_plan_id="approve",
            payload_root=self.factory / "payload",
        )
        self.assertEqual("FACTORY_PLAN_APPROVAL_REQUIRED", output["reason_code"])
        self.assertEqual([], output["mutations"])
        self.assertEqual(before, inventory(self.base))

    def test_fixture_passes_strict_claude_validation(self):
        claude = claude_with_plugin_cli()
        for target in (self.factory, self.companion, self.marketplace):
            completed = subprocess.run(
                [claude, "plugin", "validate", "--strict", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
