from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import factory_pack_lint as pack_lint  # noqa: E402


class FactoryPackLintCoreTests(unittest.TestCase):
    def test_current_mode_reaches_text_contract_without_unbound_local(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, pack_dir = self.make_run(Path(temporary))
            observed: list[str] = []

            def check_text_contracts(**kwargs: object) -> str:
                mode = str(kwargs["execution_mode"])
                observed.append(mode)
                return mode

            with self.patched_checks(check_text_contracts):
                result = pack_lint.lint_pack(root=root, pack_path=pack_dir)

            self.assertEqual("PASS", result["status"])
            self.assertEqual(["PLANNING_ONLY"], observed)

    def test_invalid_contract_returns_structured_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, pack_dir = self.make_run(Path(temporary))
            def check_text_contracts(**kwargs: object) -> str:
                errors = kwargs["errors"]
                self.assertIsInstance(errors, list)
                errors.append("invalid audit fixture")
                return str(kwargs["execution_mode"])

            with self.patched_checks(check_text_contracts):
                result = pack_lint.lint_pack(root=root, pack_path=pack_dir)

            self.assertEqual("FAIL", result["status"])
            self.assertEqual(["invalid audit fixture"], result["errors"])

    def test_cross_mode_activation_validates_manifest_against_audited_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root, pack_dir = self.make_run(Path(temporary))
            run_root = pack_dir.parent
            (run_root / "EXECUTION_MODE.txt").write_text(
                "EXECUTION_ENABLED\n", encoding="utf-8"
            )
            observed: list[str] = []

            def check_verification_manifest(**kwargs: object) -> None:
                observed.append(str(kwargs["execution_mode"]))

            with (
                patch.object(pack_lint, "_check_required_files"),
                patch.object(
                    pack_lint,
                    "_check_text_contracts",
                    return_value="PLANNING_ONLY",
                ),
                patch.object(pack_lint, "_check_artifact_shapes"),
                patch.object(
                    pack_lint,
                    "_check_verification_manifest",
                    side_effect=check_verification_manifest,
                ),
                patch.object(pack_lint, "check_host_capability_contract"),
            ):
                result = pack_lint.lint_pack(root=root, pack_path=pack_dir)

            self.assertEqual("PASS", result["status"])
            self.assertEqual(["PLANNING_ONLY"], observed)

    @staticmethod
    def make_run(root: Path) -> tuple[Path, Path]:
        run_root = root / "RUN_TEST"
        pack_dir = run_root / "pack"
        (pack_dir / "fixtures" / "cases").mkdir(parents=True)
        (run_root / "EXECUTION_MODE.txt").write_text(
            "PLANNING_ONLY\n", encoding="utf-8"
        )
        (run_root / "SPRINT_ID.txt").write_text(
            "SPRINT_TEST\n", encoding="utf-8"
        )
        return root, pack_dir

    @staticmethod
    @contextmanager
    def patched_checks(check_text_contracts: object) -> Iterator[None]:
        with (
            patch.object(pack_lint, "_check_required_files"),
            patch.object(
                pack_lint, "_check_text_contracts", side_effect=check_text_contracts
            ),
            patch.object(pack_lint, "_check_artifact_shapes"),
            patch.object(pack_lint, "_check_verification_manifest"),
            patch.object(pack_lint, "check_host_capability_contract"),
        ):
            yield


if __name__ == "__main__":
    unittest.main()
