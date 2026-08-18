import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = REPO_ROOT / "plugin-src/factory-bmad/runtime"


class FactoryBmadRuntimeNoBytecodeTests(unittest.TestCase):
    def run_candidate(self, label: str) -> tuple[subprocess.CompletedProcess[str], list[Path]]:
        with tempfile.TemporaryDirectory() as temporary:
            scripts = Path(temporary) / label / "scripts"
            scripts.mkdir(parents=True)
            for name in ("factory_bmad.py", "factory_bmad_policy.py"):
                shutil.copy2(RUNTIME_ROOT / name, scripts / name)
            environment = os.environ.copy()
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
            environment.pop("PYTHONPYCACHEPREFIX", None)
            completed = subprocess.run(
                [sys.executable, str(scripts / "factory_bmad.py"), "--help"],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            bytecode = [path.relative_to(scripts) for path in scripts.rglob("*.pyc")]
            return completed, bytecode

    def test_runtime_candidate_is_self_protecting_before_policy_import(self):
        for label in ("authored", "factory-bmad-package", "factory-bmad-claude-package"):
            with self.subTest(label=label):
                completed, bytecode = self.run_candidate(label)
                self.assertEqual(0, completed.returncode, completed.stderr)
                self.assertEqual([], bytecode)

    def test_unprotected_dynamic_import_control_creates_bytecode(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            policy = root / "policy.py"
            policy.write_text("VALUE = 1\n", encoding="utf-8")
            loader = root / "loader.py"
            loader.write_text(
                "import importlib.util, pathlib\n"
                "p = pathlib.Path(__file__).with_name('policy.py')\n"
                "s = importlib.util.spec_from_file_location('policy', p)\n"
                "m = importlib.util.module_from_spec(s)\n"
                "s.loader.exec_module(m)\n",
                encoding="utf-8",
            )
            environment = os.environ.copy()
            environment.pop("PYTHONDONTWRITEBYTECODE", None)
            environment.pop("PYTHONPYCACHEPREFIX", None)
            completed = subprocess.run(
                [sys.executable, str(loader)],
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertTrue(list(root.rglob("*.pyc")))


if __name__ == "__main__":
    unittest.main()
