from __future__ import annotations

import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import factory_pack_lint as pack_lint  # noqa: E402


class FactoryPackLintActivationTests(unittest.TestCase):
    def test_matching_planning_mode_needs_no_activation_record(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            errors: list[str] = []

            audited_mode = pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "PLANNING_ONLY", errors
            )

            self.assertEqual("PLANNING_ONLY", audited_mode)
            self.assertEqual([], errors)

    def test_matching_execution_mode_preserves_legacy_compatibility(self) -> None:
        with self.run_fixture(audited_mode="EXECUTION_ENABLED") as (run_root, pack_dir):
            errors: list[str] = []

            audited_mode = pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertEqual("EXECUTION_ENABLED", audited_mode)
            self.assertEqual([], errors)

    def test_valid_activation_preserves_and_pins_planning_artifacts(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            manifest = pack_dir / "PACK_MANIFEST.md"
            audit = pack_dir / "PACK_AUDIT_REPORT.md"
            before = (self.sha256(manifest), self.sha256(audit))
            self.write_authorization(run_root, manifest, audit)
            errors: list[str] = []

            audited_mode = pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertEqual("PLANNING_ONLY", audited_mode)
            self.assertEqual([], errors)
            self.assertEqual(before, (self.sha256(manifest), self.sha256(audit)))

    def test_cross_mode_activation_requires_authorization(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertIn("cross-mode activation requires EXECUTION_AUTHORIZATION.md", errors)

    def test_missing_audited_mode_fails_closed(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            (pack_dir / "PACK_AUDIT_REPORT.md").write_text(
                "- Verdict: PASS\n", encoding="utf-8"
            )
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertIn(
                "PACK_AUDIT_REPORT.md must record exactly one audited execution mode",
                errors,
            )

    def test_reverse_transition_is_rejected(self) -> None:
        with self.run_fixture(audited_mode="EXECUTION_ENABLED") as (run_root, pack_dir):
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "PLANNING_ONLY", errors
            )

            self.assertTrue(any("unsupported execution mode transition" in item for item in errors))

    def test_stale_manifest_and_audit_pins_are_rejected(self) -> None:
        for stale_target in ("manifest", "audit"):
            with self.subTest(stale_target=stale_target):
                with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
                    manifest = pack_dir / "PACK_MANIFEST.md"
                    audit = pack_dir / "PACK_AUDIT_REPORT.md"
                    self.write_authorization(run_root, manifest, audit)
                    target = manifest if stale_target == "manifest" else audit
                    target.write_text(target.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
                    errors: list[str] = []

                    pack_lint.check_execution_mode_contract(
                        run_root, pack_dir, "EXECUTION_ENABLED", errors
                    )

                    self.assertTrue(any(f"{stale_target} SHA-256 mismatch" in item for item in errors))

    def test_duplicate_authorization_field_is_rejected(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            manifest = pack_dir / "PACK_MANIFEST.md"
            audit = pack_dir / "PACK_AUDIT_REPORT.md"
            authorization = self.write_authorization(run_root, manifest, audit)
            authorization.write_text(
                authorization.read_text(encoding="utf-8")
                + "- Human Go: RECORDED\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertTrue(any("Human Go must occur exactly once" in item for item in errors))

    def test_symlinked_authorization_is_rejected(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            manifest = pack_dir / "PACK_MANIFEST.md"
            audit = pack_dir / "PACK_AUDIT_REPORT.md"
            external = run_root.parent / "authorization.md"
            self.write_authorization(run_root.parent, manifest, audit, target=external)
            (run_root / "EXECUTION_AUTHORIZATION.md").symlink_to(external)
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertIn("EXECUTION_AUTHORIZATION.md must be a regular non-symlink file", errors)

    def test_lint_uses_audited_mode_for_verification_manifest(self) -> None:
        with self.run_fixture(audited_mode="PLANNING_ONLY") as (run_root, pack_dir):
            self.write_authorization(
                run_root,
                pack_dir / "PACK_MANIFEST.md",
                pack_dir / "PACK_AUDIT_REPORT.md",
            )
            (run_root / "EXECUTION_MODE.txt").write_text("EXECUTION_ENABLED\n", encoding="utf-8")
            with patch.object(pack_lint, "_check_verification_manifest") as check_manifest:
                pack_lint.lint_pack(run_root.parent, run=str(run_root))

            self.assertEqual("PLANNING_ONLY", check_manifest.call_args.kwargs["execution_mode"])

    class run_fixture:
        def __init__(self, *, audited_mode: str) -> None:
            self.audited_mode = audited_mode
            self.temporary = tempfile.TemporaryDirectory()

        def __enter__(self) -> tuple[Path, Path]:
            root = Path(self.temporary.name)
            run_root = root / "RUN_TEST"
            pack_dir = run_root / "pack"
            pack_dir.mkdir(parents=True)
            (pack_dir / "PACK_MANIFEST.md").write_text("manifest\n", encoding="utf-8")
            (pack_dir / "PACK_AUDIT_REPORT.md").write_text(
                f"- Verdict: PASS\n- Audited Execution Mode: `{self.audited_mode}`\n",
                encoding="utf-8",
            )
            return run_root, pack_dir

        def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
            self.temporary.cleanup()

    @staticmethod
    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def write_authorization(
        self,
        run_root: Path,
        manifest: Path,
        audit: Path,
        *,
        target: Path | None = None,
    ) -> Path:
        authorization = target or run_root / "EXECUTION_AUTHORIZATION.md"
        authorization.write_text(
            "\n".join(
                (
                    "- Human Go: RECORDED",
                    "- Prior Execution Mode: `PLANNING_ONLY`",
                    "- Activated Execution Mode: `EXECUTION_ENABLED`",
                    f"- Authorized Pack Manifest SHA-256: `{self.sha256(manifest)}`",
                    f"- Authorized Pack Audit SHA-256: `{self.sha256(audit)}`",
                    "",
                )
            ),
            encoding="utf-8",
        )
        return authorization


if __name__ == "__main__":
    unittest.main()
