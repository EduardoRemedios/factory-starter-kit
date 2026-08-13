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

import factory_pack_lint as pack_lint  # noqa: E402


class FactoryPackLintVerificationContractTests(unittest.TestCase):
    def test_valid_contract_has_exact_vm_sets_and_pinned_no_touch_preimages(self) -> None:
        with self.fixture() as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertEqual([], errors)

    def test_plan_vm_missing_from_manifest_is_rejected(self) -> None:
        with self.fixture(plan_ids=("VM-001", "VM-002")) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("verification VM ID sets differ" in item for item in errors))

    def test_manifest_vm_missing_from_plan_is_rejected(self) -> None:
        with self.fixture(manifest_ids=("VM-001", "VM-002")) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("verification VM ID sets differ" in item for item in errors))

    def test_traceability_vm_missing_is_rejected(self) -> None:
        with self.fixture(trace_ids=()) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("verification VM ID sets differ" in item for item in errors))

    def test_canonical_traceability_verification_column_is_used(self) -> None:
        with self.fixture(canonical_traceability=True) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertEqual([], errors)

    def test_duplicate_plan_vm_is_rejected(self) -> None:
        with self.fixture(plan_ids=("VM-001", "VM-001")) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("verification_plan.md duplicates VM-001" in item for item in errors))

    def test_no_touch_requires_preimage_manifest_and_hash(self) -> None:
        with self.fixture(include_preimage_fields=False) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("preimage_manifest is required" in item for item in errors))
            self.assertTrue(any("preimage_manifest_sha256 is required" in item for item in errors))

    def test_stale_preimage_manifest_hash_is_rejected(self) -> None:
        with self.fixture(preimage_sha="0" * 64) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("preimage manifest SHA-256 mismatch" in item for item in errors))

    def test_historical_preimages_do_not_become_postimplementation_postimages(self) -> None:
        with self.fixture() as (run_root, pack_dir):
            (run_root.parent / "protected.txt").write_text("intentional implementation\n", encoding="utf-8")
            errors = self.check(run_root, pack_dir)
            self.assertEqual([], errors)

    def test_unsafe_preimage_manifest_path_is_rejected(self) -> None:
        with self.fixture(preimage_path="../outside.json") as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("preimage_manifest must be a safe run-relative path" in item for item in errors))

    def test_unsafe_exact_root_inside_preimage_manifest_is_rejected(self) -> None:
        with self.fixture() as (run_root, pack_dir):
            preimages = pack_dir / "fixtures/preimages.json"
            loaded = json.loads(preimages.read_text(encoding="utf-8"))
            loaded["exact_roots"] = ["../outside"]
            preimages.write_text(json.dumps(loaded), encoding="utf-8")
            manifest = yaml.safe_load((pack_dir / "verification_manifest.yaml").read_text(encoding="utf-8"))
            manifest["checks"][0]["preimage_manifest_sha256"] = hashlib.sha256(preimages.read_bytes()).hexdigest()
            (pack_dir / "verification_manifest.yaml").write_text(
                yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
            )
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("unsafe exact root" in item for item in errors))

    def test_symlinked_preimage_manifest_is_rejected(self) -> None:
        with self.fixture(preimage_path="pack/fixtures/link.json") as (run_root, pack_dir):
            preimages = pack_dir / "fixtures/preimages.json"
            (pack_dir / "fixtures/link.json").symlink_to(preimages.name)
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("regular non-symlink file" in item for item in errors))

    def test_execution_order_must_cover_each_vm_once(self) -> None:
        with self.fixture(execution_order=("VM-001", "VM-001")) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("execution_order duplicates" in item for item in errors))

        with self.fixture(
            manifest_ids=("VM-001", "VM-002"),
            plan_ids=("VM-001", "VM-002"),
            trace_ids=("VM-001", "VM-002"),
            execution_order=("VM-001", "BUILDER-001"),
        ) as (run_root, pack_dir):
            errors = self.check(run_root, pack_dir)
            self.assertTrue(any("execution_order VM IDs differ" in item for item in errors))

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
            plan_ids: tuple[str, ...] = ("VM-001",),
            manifest_ids: tuple[str, ...] = ("VM-001",),
            trace_ids: tuple[str, ...] = ("VM-001",),
            include_preimage_fields: bool = True,
            preimage_sha: str | None = None,
            preimage_path: str = "pack/fixtures/preimages.json",
            canonical_traceability: bool = False,
            execution_order: tuple[str, ...] | None = None,
        ) -> None:
            self.plan_ids = plan_ids
            self.manifest_ids = manifest_ids
            self.trace_ids = trace_ids
            self.include_preimage_fields = include_preimage_fields
            self.preimage_sha = preimage_sha
            self.preimage_path = preimage_path
            self.canonical_traceability = canonical_traceability
            self.execution_order = execution_order
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
            (pack_dir / "verification_plan.md").write_text(
                "# Plan\n\n## Checks\n\n"
                + "".join(f"- {item} — check\n" for item in self.plan_ids),
                encoding="utf-8",
            )
            coverage = ", ".join(self.trace_ids) if self.trace_ids else "None"
            if self.canonical_traceability:
                traceability = (
                    "| Constraint ID | Severity | Statement | Source | Scope Tag | Verification Tier | Verification (fixture/test/check) | Artifact Path |\n"
                    "|---|---|---|---|---|---|---|---|\n"
                    f"| C-01 | Critical | Protect bytes | RAW | OK | V1 | {coverage} | artifacts/check.txt |\n"
                )
            else:
                traceability = (
                    "| Constraint | Verification coverage |\n|---|---|\n"
                    f"| C-01 | {coverage} |\n"
                )
            (pack_dir / "traceability_matrix.md").write_text(traceability, encoding="utf-8")
            checks = []
            for check_id in self.manifest_ids:
                check = {
                    "id": check_id,
                    "tier": "V1",
                    "type": "no_touch",
                    "constraint_ids": ["C-01"],
                    "description": "Protect exact bytes.",
                    "command": "verify-preimages",
                    "expected": "PASS",
                    "halt_on_failure": True,
                    "evidence_path": f"artifacts/{check_id}.txt",
                }
                if self.include_preimage_fields:
                    check["preimage_manifest"] = self.preimage_path
                    check["preimage_manifest_sha256"] = self.preimage_sha or hashlib.sha256(
                        preimages.read_bytes()
                    ).hexdigest()
                checks.append(check)
            manifest = {
                "schema_version": 1,
                "run_id": "RUN_TEST",
                "sprint_id": "SPRINT_TEST",
                "execution_mode": "PLANNING_ONLY",
                "checks": checks,
            }
            if self.execution_order is not None:
                manifest["execution_order"] = list(self.execution_order)
            (pack_dir / "verification_manifest.yaml").write_text(
                yaml.safe_dump(
                    manifest,
                    sort_keys=False,
                ),
                encoding="utf-8",
            )
            return run_root, pack_dir

        def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
            self.temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
