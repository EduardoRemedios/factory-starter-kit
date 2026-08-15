import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
LAUNCHER = REPO_ROOT / "scripts/factory-python"


class FactoryPythonLauncherTests(unittest.TestCase):
    def test_launcher_is_exact_and_executable(self):
        self.assertEqual(
            '#!/bin/sh\nset -eu\nexport PYTHONDONTWRITEBYTECODE=1\nexec python3 "$@"\n',
            LAUNCHER.read_text(encoding="utf-8"),
        )
        self.assertTrue(LAUNCHER.stat().st_mode & stat.S_IXUSR)

    def test_launcher_exports_guard_and_forwards_arguments(self):
        result = subprocess.run(
            [
                str(LAUNCHER),
                "-c",
                "import os,sys; print(os.environ['PYTHONDONTWRITEBYTECODE']); print('|'.join(sys.argv[1:]))",
                "alpha",
                "two words",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual("1\nalpha|two words\n", result.stdout)

    def test_launcher_preserves_exit_status(self):
        result = subprocess.run(
            [str(LAUNCHER), "-c", "raise SystemExit(23)"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(23, result.returncode)

    def test_launcher_prevents_bytecode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "probe_module.py").write_text("VALUE = 7\n", encoding="utf-8")
            (root / "runner.py").write_text(
                "import probe_module\nassert probe_module.VALUE == 7\n",
                encoding="utf-8",
            )
            subprocess.run([str(LAUNCHER), "runner.py"], cwd=root, check=True)
            self.assertFalse((root / "__pycache__").exists())
            self.assertEqual([], list(root.rglob("*.pyc")))

    def test_missing_interpreter_fails_visibly(self):
        environment = os.environ.copy()
        environment["PATH"] = "/nonexistent"
        result = subprocess.run(
            [str(LAUNCHER), "-c", "pass"],
            env=environment,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(0, result.returncode)
        self.assertIn("python3", result.stderr)

    def test_factory_control_surfaces_use_launcher(self):
        surfaces = (
            "AGENTS.md",
            ".agents/skills/factory-root-planner/SKILL.md",
            ".agents/skills/factory-execution-closeout/SKILL.md",
            "docs/Factory/ORCHESTRATION.md",
            "docs/Factory/Spec/STAGE_CONTRACTS.md",
            "docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md",
            "plugin-src/factory/skills/validate.md",
        )
        for relative in surfaces:
            with self.subTest(path=relative):
                text = (REPO_ROOT / relative).read_text(encoding="utf-8")
                self.assertNotIn("`python3 ", text)
                self.assertNotIn("`python ", text)
        self.assertIn("- Human Go: RECORDED", (REPO_ROOT / surfaces[5]).read_text(encoding="utf-8"))

    def test_factoryctl_self_routes_through_launcher_without_bytecode(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            scripts = root / "scripts"
            scripts.mkdir()
            for source in (REPO_ROOT / "scripts").iterdir():
                if source.is_file() and (source.suffix == ".py" or source.name in {"factoryctl", "factory-python"}):
                    shutil.copy2(source, scripts / source.name)
            environment = os.environ.copy()
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
            completed = subprocess.run(
                [str(scripts / "factoryctl"), "--help"],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                env=environment,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual([], list(root.rglob("*.pyc")))
            self.assertEqual([], list(root.rglob("__pycache__")))


if __name__ == "__main__":
    unittest.main()
