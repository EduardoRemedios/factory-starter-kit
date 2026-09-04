from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import conductor_pack_lint as pack_lint  # noqa: E402


class FactoryPackLintActivationTests(unittest.TestCase):
    def test_missing_audited_mode_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root, pack_dir = self.make_run(Path(temporary), audit="- Verdict: PASS\n")
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertIn(
                "PACK_AUDIT_REPORT.md must record exactly one audited execution mode",
                errors,
            )

    def test_valid_cross_mode_activation_pins_immutable_pack(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root, pack_dir = self.make_run(
                Path(temporary),
                audit="- Verdict: PASS\n- Audited Execution Mode: `PLANNING_ONLY`\n",
            )
            manifest = pack_dir / "PACK_MANIFEST.md"
            audit = pack_dir / "PACK_AUDIT_REPORT.md"
            (run_root / "EXECUTION_AUTHORIZATION.md").write_text(
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
            errors: list[str] = []

            audited_mode = pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertEqual("PLANNING_ONLY", audited_mode)
            self.assertEqual([], errors)

    def test_stale_activation_pin_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            run_root, pack_dir = self.make_run(
                Path(temporary),
                audit="- Verdict: PASS\n- Audited Execution Mode: `PLANNING_ONLY`\n",
            )
            manifest = pack_dir / "PACK_MANIFEST.md"
            audit = pack_dir / "PACK_AUDIT_REPORT.md"
            (run_root / "EXECUTION_AUTHORIZATION.md").write_text(
                "\n".join(
                    (
                        "- Human Go: RECORDED",
                        "- Prior Execution Mode: `PLANNING_ONLY`",
                        "- Activated Execution Mode: `EXECUTION_ENABLED`",
                        f"- Authorized Pack Manifest SHA-256: `{'0' * 64}`",
                        f"- Authorized Pack Audit SHA-256: `{self.sha256(audit)}`",
                        "",
                    )
                ),
                encoding="utf-8",
            )
            errors: list[str] = []

            pack_lint.check_execution_mode_contract(
                run_root, pack_dir, "EXECUTION_ENABLED", errors
            )

            self.assertIn("EXECUTION_AUTHORIZATION.md manifest SHA-256 mismatch", errors)
            self.assertTrue(manifest.is_file())

    @staticmethod
    def make_run(root: Path, *, audit: str) -> tuple[Path, Path]:
        run_root = root / "RUN_TEST"
        pack_dir = run_root / "pack"
        pack_dir.mkdir(parents=True)
        (pack_dir / "PACK_MANIFEST.md").write_text("manifest\n", encoding="utf-8")
        (pack_dir / "PACK_AUDIT_REPORT.md").write_text(audit, encoding="utf-8")
        return run_root, pack_dir

    @staticmethod
    def sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()


class FactoryPackLintManifestPresenceTests(unittest.TestCase):
    def test_execution_enabled_with_planned_vm_checks_requires_manifest(self) -> None:
        with self.pack(plan_ids=("VM-001", "VM-002")) as pack_dir:
            errors, warnings = self.check(pack_dir, "EXECUTION_ENABLED")
            self.assertTrue(
                any("cannot record a canonical execution closeout" in item for item in errors),
                errors,
            )
            self.assertEqual([], warnings)

    def test_execution_enabled_without_planned_vm_checks_keeps_legacy_warning(self) -> None:
        with self.pack(plan_ids=()) as pack_dir:
            errors, warnings = self.check(pack_dir, "EXECUTION_ENABLED")
            self.assertEqual([], errors)
            self.assertTrue(
                any("allowed for legacy packs" in item for item in warnings),
                warnings,
            )

    def test_planning_only_with_planned_vm_checks_warns_of_uncloseable_pack(self) -> None:
        with self.pack(plan_ids=("VM-001",)) as pack_dir:
            errors, warnings = self.check(pack_dir, "PLANNING_ONLY")
            self.assertEqual([], errors)
            self.assertTrue(
                any("cannot record a canonical execution closeout" in item for item in warnings),
                warnings,
            )

    def test_present_manifest_emits_no_presence_diagnostics(self) -> None:
        with self.pack(plan_ids=("VM-001",), manifest=True) as pack_dir:
            for mode in ("PLANNING_ONLY", "EXECUTION_ENABLED"):
                errors, warnings = self.check(pack_dir, mode)
                self.assertEqual([], errors)
                self.assertEqual([], warnings)

    @staticmethod
    def check(pack_dir: Path, execution_mode: str) -> tuple[list[str], list[str]]:
        errors: list[str] = []
        warnings: list[str] = []
        pack_lint.check_verification_manifest_presence(
            pack_dir=pack_dir,
            execution_mode=execution_mode,
            errors=errors,
            warnings=warnings,
        )
        return errors, warnings

    class pack:
        def __init__(self, *, plan_ids: tuple[str, ...], manifest: bool = False) -> None:
            self.plan_ids = plan_ids
            self.manifest = manifest
            self.temporary = tempfile.TemporaryDirectory()

        def __enter__(self) -> Path:
            pack_dir = Path(self.temporary.name) / "RUN_TEST" / "pack"
            pack_dir.mkdir(parents=True)
            checks = "".join(f"- {item} — check\n" for item in self.plan_ids)
            (pack_dir / "verification_plan.md").write_text(
                f"# Plan\n\n## Checks\n\n{checks}", encoding="utf-8"
            )
            if self.manifest:
                (pack_dir / "verification_manifest.yaml").write_text(
                    "schema_version: 1\n", encoding="utf-8"
                )
            return pack_dir

        def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
            self.temporary.cleanup()


class FactoryPackLintVerificationContractTests(unittest.TestCase):
    def test_canonical_traceability_column_is_used(self) -> None:
        with self.fixture(canonical_traceability=True) as (run_root, pack_dir):
            self.assertEqual([], self.check(run_root, pack_dir))

    def test_symlinked_preimage_manifest_is_rejected(self) -> None:
        with self.fixture(symlink_preimages=True) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("regular non-symlink file" in item for item in errors))

    def test_execution_order_covers_every_vm_exactly_once(self) -> None:
        with self.fixture(execution_order=("VM-001", "VM-001")) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("execution_order duplicates" in item for item in errors))

        with self.fixture(
            ids=("VM-001", "VM-002"),
            execution_order=("VM-001", "BUILDER-001"),
        ) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("execution_order VM IDs differ" in item for item in errors))

    def test_historical_target_drift_does_not_rewrite_preimages(self) -> None:
        with self.fixture() as (run_root, pack_dir):
            (run_root.parent / "protected.txt").write_text(
                "intentional implementation\n", encoding="utf-8"
            )
            self.assertEqual([], self.check(run_root, pack_dir))

    @staticmethod
    def check(run_root: Path, pack_dir: Path) -> list[str]:
        errors: list[str] = []
        pack_lint._check_verification_manifest(
            run_root=run_root,
            pack_dir=pack_dir,
            sprint_id="SPRINT_TEST",
            execution_mode="PLANNING_ONLY",
            checked_files=[],
            errors=errors,
            warnings=[],
        )
        return errors

    class fixture:
        def __init__(
            self,
            *,
            ids: tuple[str, ...] = ("VM-001",),
            execution_order: tuple[str, ...] | None = None,
            canonical_traceability: bool = False,
            symlink_preimages: bool = False,
        ) -> None:
            self.ids = ids
            self.execution_order = execution_order
            self.canonical_traceability = canonical_traceability
            self.symlink_preimages = symlink_preimages
            self.temporary = tempfile.TemporaryDirectory()

        def __enter__(self) -> tuple[Path, Path]:
            root = Path(self.temporary.name)
            run_root = root / "RUN_TEST"
            pack_dir = run_root / "pack"
            fixtures = pack_dir / "fixtures"
            fixtures.mkdir(parents=True)
            target = root / "protected.txt"
            target.write_text("protected\n", encoding="utf-8")
            preimages = fixtures / "preimages.json"
            preimages.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "exact_roots": [],
                        "files": {
                            "protected.txt": {
                                "type": "file",
                                "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            manifest_name = "preimages.json"
            if self.symlink_preimages:
                manifest_name = "link.json"
                (fixtures / manifest_name).symlink_to(preimages.name)

            (pack_dir / "verification_plan.md").write_text(
                "# Plan\n\n## Checks\n\n"
                + "".join(f"- {item} — check\n" for item in self.ids),
                encoding="utf-8",
            )
            coverage = ", ".join(self.ids)
            if self.canonical_traceability:
                traceability = (
                    "| Constraint ID | Severity | Statement | Source | Scope Tag | Verification Tier | Verification (fixture/test/check) | Artifact Path |\n"
                    "|---|---|---|---|---|---|---|---|\n"
                    f"| C-001 | Critical | Protect | RAW | OK | V1 | {coverage} | artifacts/check.txt |\n"
                )
            else:
                traceability = (
                    "| Constraint | Verification coverage |\n|---|---|\n"
                    f"| C-001 | {coverage} |\n"
                )
            (pack_dir / "traceability_matrix.md").write_text(
                traceability, encoding="utf-8"
            )

            checks = []
            for check_id in self.ids:
                checks.append(
                    {
                        "id": check_id,
                        "tier": "V1",
                        "type": "no_touch",
                        "constraint_ids": ["C-001"],
                        "description": "Protect exact bytes.",
                        "command": "verify-preimages",
                        "expected": "PASS",
                        "halt_on_failure": True,
                        "preimage_manifest": f"pack/fixtures/{manifest_name}",
                        "preimage_manifest_sha256": hashlib.sha256(preimages.read_bytes()).hexdigest(),
                        "evidence_path": f"artifacts/{check_id}.txt",
                    }
                )
            manifest: dict[str, object] = {
                "schema_version": 1,
                "run_id": "RUN_TEST",
                "sprint_id": "SPRINT_TEST",
                "execution_mode": "PLANNING_ONLY",
                "checks": checks,
            }
            if self.execution_order is not None:
                manifest["execution_order"] = list(self.execution_order)
            (pack_dir / "verification_manifest.yaml").write_text(
                yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
            )
            return run_root, pack_dir

        def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
            self.temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
