from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from factory_pack_lint import check_context_recall_report  # noqa: E402


class ContextRecallRepairTests(unittest.TestCase):
    def test_unrepaired_weak_recall_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            errors: list[str] = []

            check_context_recall_report(
                root=root,
                report_path=root / "docs/Factory/runs/RUN_TEST/CONTEXT_RECALL_REPORT.md",
                text="# Context Recall Report\n\n## Report Metadata\n- Coverage Verdict: WEAK\n",
                errors=errors,
            )

            self.assertTrue(any("without a Direct-Source Repair section" in error for error in errors))

    def test_repaired_direct_source_report_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_source(root, "docs/product_readiness.md")
            errors: list[str] = []

            check_context_recall_report(
                root=root,
                report_path=root / "docs/Factory/runs/RUN_TEST/CONTEXT_RECALL_REPORT.md",
                text=self._report(source="docs/product_readiness.md"),
                errors=errors,
            )

            self.assertEqual(errors, [])

    def test_repair_with_missing_direct_source_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            errors: list[str] = []

            check_context_recall_report(
                root=root,
                report_path=root / "docs/Factory/runs/RUN_TEST/CONTEXT_RECALL_REPORT.md",
                text=self._report(source="docs/missing.md"),
                errors=errors,
            )

            self.assertTrue(any("direct source does not exist" in error for error in errors))

    def test_repair_with_material_unresolved_refs_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write_source(root, "docs/product_readiness.md")
            errors: list[str] = []

            check_context_recall_report(
                root=root,
                report_path=root / "docs/Factory/runs/RUN_TEST/CONTEXT_RECALL_REPORT.md",
                text=self._report(
                    source="docs/product_readiness.md",
                    material_refs="`approval_record.md`",
                    materiality="FAIL",
                ),
                errors=errors,
            )

            self.assertTrue(any("Remaining Material Unresolved Refs must be None" in error for error in errors))
            self.assertTrue(any("Materiality Check must be PASS" in error for error in errors))

    def _write_source(self, root: Path, rel_path: str) -> None:
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# Product Readiness\n\nThis local source records the readiness facts needed for Stage A.\n",
            encoding="utf-8",
        )

    def _report(
        self,
        *,
        source: str,
        material_refs: str = "None",
        materiality: str = "PASS",
    ) -> str:
        return f"""# Context Recall Report

## Report Metadata
- Coverage Verdict: WEAK

## Required Reference Checks
### R1. `{source}`
- Status: UNRESOLVED
- Resolution Type: path
- Evidence: None

## Direct-Source Repair
- Original Generated Verdict: WEAK
- Unresolved Generated Refs: `{source}`
- Direct-Source Repair Status: APPLIED
- Context Index Refreshed: YES
- Fallback Scopes Attempted: YES
- Remaining Unresolved Generated Refs: None
- Remaining Material Unresolved Refs: {material_refs}
- Materiality Check: {materiality}
- Final Repaired Verdict: REPAIRED_DIRECT_SOURCE_CHECK

## Direct Sources Read
- `{source}`

## Source Summaries
### `{source}`
- Summary: This source directly confirms the Stage A readiness context needed to repair the unresolved generated ref.
- Covers refs: `{source}`
- Remaining unresolved refs: None
"""


if __name__ == "__main__":
    unittest.main()
