from __future__ import annotations

import json
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from factory_project_preflight import (  # noqa: E402
    MAX_STREAM_BYTES,
    ProjectPreflightError,
    run_project_preflight,
    write_project_preflight_evidence,
)
from factory_stage_lint import lint_stage  # noqa: E402


RUN_ID = "RUN_20260805_0000_preflight_test"


class FactoryProjectPreflightTests(unittest.TestCase):
    def test_absent_declaration_preserves_existing_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = run_project_preflight(Path(temp_dir), RUN_ID)
        self.assertEqual("pass", result["outcome"])
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_NOT_DECLARED", result["reason_code"])
        self.assertFalse(result["result_required"])

    def test_valid_pass_records_separate_bounded_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root)
            self._write(root / "artifacts/project-preflight.json", "{}\n")
            self._command(
                root,
                """
                import json, sys
                assert sys.argv[1:] == ["--run", "RUN_20260805_0000_preflight_test", "--json"]
                print(json.dumps({"schema_version": 1, "status": "PASS", "reason_code": "PROJECT_READY", "evidence_paths": ["artifacts/project-preflight.json"]}))
                """,
            )
            self._run_root(root)

            result = run_project_preflight(root, RUN_ID)
            evidence = write_project_preflight_evidence(root, RUN_ID, result).read_text()

        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_PASS", result["reason_code"])
        self.assertLessEqual(result["stdout_bytes_retained"], MAX_STREAM_BYTES)
        self.assertIn("stdout_sha256:", evidence)
        self.assertIn("stderr_sha256:", evidence)
        self.assertNotIn("{\"schema_version\"", evidence)

    def test_malformed_declaration_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write(root / "docs/Factory/PROJECT_PREFLIGHT.json", "not json\n")
            result = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID", result["reason_code"])

    def test_missing_and_non_executable_commands_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root)
            missing = run_project_preflight(root, RUN_ID)
            self._command(root, "print('unused')", executable=False)
            invalid = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_COMMAND_MISSING", missing["reason_code"])
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_COMMAND_INVALID", invalid["reason_code"])

    def test_timeout_and_nonzero_exit_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root, timeout_seconds=1)
            self._command(root, "import time; time.sleep(2)")
            timeout = run_project_preflight(root, RUN_ID)
            self._command(root, "raise SystemExit(7)")
            nonzero = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_TIMEOUT", timeout["reason_code"])
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_EXIT_NONZERO", nonzero["reason_code"])
        self.assertEqual(7, nonzero["return_code"])

    def test_oversized_output_fails_without_retaining_excess(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root)
            self._command(root, f"import sys; sys.stdout.write('x' * {MAX_STREAM_BYTES + 1})")
            result = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_OUTPUT_TOO_LARGE", result["reason_code"])
        self.assertEqual(MAX_STREAM_BYTES, result["stdout_bytes_retained"])

    def test_oversized_stderr_is_bounded_independently(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root)
            self._command(root, f"import sys; sys.stderr.write('x' * {MAX_STREAM_BYTES + 1})")
            result = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_OUTPUT_TOO_LARGE", result["reason_code"])
        self.assertEqual(MAX_STREAM_BYTES, result["stderr_bytes_retained"])

    def test_malformed_ambiguous_and_explicit_fail_outputs_are_distinct(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root)
            self._command(root, "print('not json')")
            malformed = run_project_preflight(root, RUN_ID)
            self._command(root, "import json; print(json.dumps({'status': 'PASS'}))")
            ambiguous = run_project_preflight(root, RUN_ID)
            self._command(
                root,
                "import json; print(json.dumps({'schema_version': 1, 'status': 'FAIL', 'reason_code': 'PROJECT_BLOCKED', 'evidence_paths': []}))",
            )
            failed = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_OUTPUT_MALFORMED", malformed["reason_code"])
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_OUTPUT_AMBIGUOUS", ambiguous["reason_code"])
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_FAILED", failed["reason_code"])

    def test_absolute_evidence_path_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._declaration(root)
            absolute = (root / "evidence.json").resolve()
            self._write(absolute, "{}\n")
            self._command(
                root,
                f"import json; print(json.dumps({{'schema_version': 1, 'status': 'PASS', 'reason_code': 'PROJECT_READY', 'evidence_paths': [{str(absolute)!r}]}}))",
            )
            result = run_project_preflight(root, RUN_ID)
        self.assertEqual("FACTORY_PROJECT_PREFLIGHT_EVIDENCE_PATH_INVALID", result["reason_code"])

    def test_stage_a_requires_pass_evidence_only_when_declared(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = self._run_root(root)
            undeclared = lint_stage(root=root, run=RUN_ID, stage="A")
            self._declaration(root)
            missing = lint_stage(root=root, run=RUN_ID, stage="A")
            self._write(
                run_root / "PROJECT_PREFLIGHT.txt",
                "project_preflight: PASS\nreason_code: FACTORY_PROJECT_PREFLIGHT_PASS\n",
            )
            passed = lint_stage(root=root, run=RUN_ID, stage="A")
        self.assertEqual("PASS", undeclared["status"])
        self.assertEqual("FAIL", missing["status"])
        self.assertEqual("PASS", passed["status"])

    def test_symlinked_run_root_ancestors_block_evidence_write(self) -> None:
        result = {
            "outcome": "pass",
            "reason_code": "FACTORY_PROJECT_PREFLIGHT_PASS",
        }
        for ancestor in ("docs", "docs/Factory", "docs/Factory/runs"):
            with self.subTest(ancestor=ancestor), tempfile.TemporaryDirectory() as temp_dir:
                base = Path(temp_dir)
                root = base / "repo"
                root.mkdir()
                run_root = self._run_root(root)
                linked_ancestor = root / ancestor
                outside_ancestor = base / "outside" / Path(ancestor).name
                outside_ancestor.parent.mkdir(parents=True)
                run_below_ancestor = run_root.relative_to(linked_ancestor)
                linked_ancestor.rename(outside_ancestor)
                linked_ancestor.symlink_to(outside_ancestor, target_is_directory=True)
                outside_evidence = (
                    outside_ancestor / run_below_ancestor / "PROJECT_PREFLIGHT.txt"
                )

                with self.assertRaises(ProjectPreflightError):
                    write_project_preflight_evidence(root, RUN_ID, result)
                self.assertFalse(outside_evidence.exists())

    def test_root_operator_contract_has_exact_order(self) -> None:
        agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        planner = (REPO_ROOT / ".agents/skills/factory-root-planner/SKILL.md").read_text(
            encoding="utf-8"
        )
        for text in (agents, planner):
            knowledge = text.index("knowledge_lint.sh")
            preflight = text.index("project-preflight")
            recall = text.index("context-index")
            self.assertLess(knowledge, preflight)
            self.assertLess(preflight, recall)

    def _declaration(self, root: Path, *, timeout_seconds: int = 60) -> None:
        self._write(
            root / "docs/Factory/PROJECT_PREFLIGHT.json",
            json.dumps({"schema_version": 1, "timeout_seconds": timeout_seconds}) + "\n",
        )

    def _command(self, root: Path, body: str, *, executable: bool = True) -> None:
        path = root / "scripts/factory_project_preflight"
        self._write(
            path,
            "#!/usr/bin/env python3\n" + textwrap.dedent(body).strip() + "\n",
        )
        path.chmod(0o755 if executable else 0o644)

    def _run_root(self, root: Path) -> Path:
        run_root = root / "docs/Factory/runs" / RUN_ID
        self._write(run_root / "CONTEXT_RECALL_REPORT.md", "Coverage Verdict: SUFFICIENT\n")
        self._write(run_root / "pack/intent.md", "# Intent\n")
        self._write(
            run_root / "pack/HANDOFF/HANDOFF_STAGE_A.md",
            """# Stage A Handoff

## Version
- v1
## Change Log
- v1 (2026-08-05): Test.
## Stage
- Stage ID: STAGE_A
## Inputs (LOAD)
- raw
## Inputs (DISK)
- lint
## Skill Routing Contract
- Skill used: NONE
## Outputs Produced (paths)
- pack/intent.md
## Verification Steps Recommended
- lint
## Exit Criteria Status
- PASS
""",
        )
        return run_root

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
