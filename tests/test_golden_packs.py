"""Golden-pack regression guard (Conductor migration step 1).

The two archived Factory V2 runs under ``tests/golden_packs/`` are qualified
evidence: RUN_20260902_0725 (Factory-BMAD 0.2.5 solution-context integration,
human-accepted) and RUN_20260903_1750 (MS-06 disposable qualification planning
run, Purple PASS). Any change to pack-lint, stage contracts, or templates that
would stop these packs from linting is a compatibility break with qualified
evidence and must be made deliberately, with this test updated in the same
change. See docs/Conductor/DESIGN_PACK/06_MIGRATION_AND_QUALIFICATION.md.
"""
from __future__ import annotations

from pathlib import Path
import sys
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import factory_pack_lint as pack_lint  # noqa: E402

GOLDEN_ROOT = REPO_ROOT / "tests" / "golden_packs"
GOLDEN_RUNS: dict[str, int] = {
    # run id -> number of files pack-lint is expected to check
    "RUN_20260902_0725_factory_bmad_025_solution_context_integration": 35,
    "RUN_20260903_1750_factory_bmad_025_ms06_disposable_live_qualification": 32,
}


class GoldenPackTests(unittest.TestCase):
    def test_golden_runs_are_present_and_complete(self) -> None:
        present = sorted(path.name for path in GOLDEN_ROOT.iterdir() if path.is_dir())
        self.assertEqual(present, sorted(GOLDEN_RUNS))
        for run_id in GOLDEN_RUNS:
            run_root = GOLDEN_ROOT / run_id
            for required in ("EXECUTION_MODE.txt", "SPRINT_ID.txt", "pack/PACK_MANIFEST.md", "pack/PACK_AUDIT_REPORT.md"):
                self.assertTrue((run_root / required).is_file(), f"{run_id}: missing {required}")

    def test_golden_runs_pass_pack_lint(self) -> None:
        for run_id, expected_checked in GOLDEN_RUNS.items():
            with self.subTest(run=run_id):
                result = pack_lint.lint_pack(root=REPO_ROOT, run=f"tests/golden_packs/{run_id}")
                self.assertEqual(result["errors"], [], f"{run_id}: pack-lint errors: {result['errors']}")
                self.assertEqual(result["warnings"], [], f"{run_id}: pack-lint warnings: {result['warnings']}")
                self.assertEqual(
                    len(result["checked_files"]),
                    expected_checked,
                    f"{run_id}: checked-file count changed; update GOLDEN_RUNS deliberately if the contract changed",
                )

    def test_golden_runs_are_planning_only(self) -> None:
        # Both archived runs were qualification/planning runs; an EXECUTION_ENABLED
        # golden pack would need matching execution evidence and is out of scope here.
        for run_id in GOLDEN_RUNS:
            mode = (GOLDEN_ROOT / run_id / "EXECUTION_MODE.txt").read_text(encoding="utf-8").strip()
            self.assertEqual(mode, "PLANNING_ONLY", f"{run_id}: unexpected execution mode {mode!r}")


if __name__ == "__main__":
    unittest.main()
