import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.dont_write_bytecode = True
RUNTIME_PATH = REPO_ROOT / "plugin-src/conductor/runtime/conductor_plugin.py"
SPEC = importlib.util.spec_from_file_location("conductor_plugin_runtime", RUNTIME_PATH)
RUNTIME = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(RUNTIME)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def inventory(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def create_run(root: Path, run_id: str = "RUN_20260724_0000_fixture") -> Path:
    run_root = root / "docs/Conductor/runs" / run_id
    write(run_root / "KNOWLEDGE_LINT.txt", "knowledge_lint: PASS\n")
    write(run_root / "EXECUTION_MODE.txt", "EXECUTION_ENABLED\n")
    return run_root


def passing_handoff(run_root: Path, stage: str, output: str | None = None) -> None:
    output_section = f"- `{output}`\n" if output else ""
    write(
        run_root / "pack/HANDOFF" / f"HANDOFF_STAGE_{stage}.md",
        "## Outputs Produced (paths)\n"
        f"{output_section}"
        "\n## Exit Criteria Status\n"
        "- PASS\n",
    )


def complete_i2_pack(run_root: Path) -> None:
    for stage in RUNTIME.STAGE_ORDER:
        passing_handoff(run_root, stage)
    intent = run_root / "pack/intent.md"
    write(intent, "# Intent\n")
    write(
        run_root / "pack/intent_lock_report.md",
        "- Verdict: PASS\n"
        f"- Locked SHA-256: `{RUNTIME.file_sha256(intent)}`\n",
    )
    write(run_root / "pack/PACK_AUDIT_REPORT.md", "- Verdict: PASS\n")


class FactoryPluginStatusTests(unittest.TestCase):
    def test_doctor_is_read_only_and_reports_compatibility(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative in (
                "AGENTS.md",
                "docs/Conductor/ARCHITECTURE.md",
                "docs/Conductor/ORCHESTRATION.md",
                "scripts/conductorctl",
            ):
                write(root / relative, "fixture\n")
            before = inventory(root)
            output = RUNTIME.evaluate_doctor(
                root,
                harness="codex",
                platform_name="darwin",
                python_version=(3, 11, 0),
            )
            self.assertEqual("READY", output["state"])
            self.assertEqual("CONDUCTOR_DOCTOR_OK", output["reason_code"])
            self.assertEqual([], output["mutations"])
            self.assertEqual(before, inventory(root))

    def test_unsupported_environment_fails_closed_without_mutation(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            before = inventory(root)
            output = RUNTIME.evaluate_doctor(
                root,
                harness="claude",
                platform_name="linux",
                python_version=(3, 11, 0),
            )
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_ENVIRONMENT_UNVERIFIED", output["reason_code"])
            self.assertEqual(before, inventory(root))

    def test_no_run_is_ready_to_initialize(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            before = inventory(root)
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("READY_TO_INITIALIZE", output["state"])
            self.assertEqual("CONDUCTOR_NO_ACTIVE_RUN", output["reason_code"])
            self.assertEqual(before, inventory(root))

    def test_passing_handoff_with_missing_output_is_contradiction(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            passing_handoff(run_root, "A", "pack/intent.md")
            before = inventory(root)
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_EVIDENCE_CONTRADICTION", output["reason_code"])
            self.assertEqual(
                "repair_stage_a_and_rerun_stage_lint", output["next_legal_action"]
            )
            self.assertIn("missing_output", output["blocker"])
            self.assertEqual(before, inventory(root))

    def test_unrepaired_weak_recall_blocks(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            write(run_root / "CONTEXT_RECALL_REPORT.md", "Coverage Verdict: WEAK\n")
            before = inventory(root)
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_WEAK_RECALL", output["reason_code"])
            self.assertEqual(before, inventory(root))

    def test_i2_pass_without_human_go_waits(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            complete_i2_pack(run_root)
            before = inventory(root)
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("WAITING_HUMAN_GO", output["state"])
            self.assertEqual("CONDUCTOR_HUMAN_GO_REQUIRED", output["reason_code"])
            self.assertEqual(before, inventory(root))

    def test_human_go_label_or_negative_value_does_not_authorize(self):
        for marker in ("- Human Go:\n", "- Human Go: NOT_RECORDED\n"):
            with self.subTest(marker=marker.strip()), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                run_root = create_run(root)
                complete_i2_pack(run_root)
                write(run_root / "EXECUTION_PROMPT.md", marker)
                output = RUNTIME.evaluate_progress(root)
                self.assertEqual("WAITING_HUMAN_GO", output["state"])
                self.assertEqual("CONDUCTOR_HUMAN_GO_REQUIRED", output["reason_code"])

    def test_exact_human_go_marker_authorizes_execution(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            complete_i2_pack(run_root)
            write(run_root / "EXECUTION_PROMPT.md", "- Human Go: RECORDED\n")
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("AUTHORIZED_FOR_EXECUTION", output["state"])
            self.assertEqual("CONDUCTOR_HUMAN_GO_RECORDED", output["reason_code"])

    def test_progress_rejects_the_same_output_path_failures_as_stage_lint(self):
        cases = (
            "- pack/evidence.txt\n",
            "- `pack/*.txt`\n",
            "- `/tmp/evidence.txt`\n",
            "- `../evidence.txt`\n",
            "- `pack/missing.txt`\n",
        )
        for output_line in cases:
            with self.subTest(output_line=output_line.strip()), tempfile.TemporaryDirectory() as temp_dir:
                root = Path(temp_dir)
                run_root = create_run(root)
                write(
                    run_root / "pack/HANDOFF/HANDOFF_STAGE_A.md",
                    "## Outputs Produced (paths)\n"
                    f"{output_line}"
                    "\n## Exit Criteria Status\n- PASS\n",
                )
                output = RUNTIME.evaluate_progress(root)
                self.assertEqual("BLOCKED", output["state"])
                self.assertEqual("CONDUCTOR_EVIDENCE_CONTRADICTION", output["reason_code"])

    def test_progress_accepts_nonempty_exact_output_path(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            write(run_root / "pack/evidence.txt", "ok\n")
            passing_handoff(run_root, "A", "pack/evidence.txt")
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("PLANNING_IN_PROGRESS", output["state"])

    def test_failed_intent_purple_gate_blocks_stage_e(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            for stage in ("A", "B", "C", "D"):
                passing_handoff(run_root, stage)
            write(run_root / "pack/intent.md", "# Intent\n")
            write(run_root / "pack/intent_lock_report.md", "- Verdict: FAIL\n")
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_INTENT_NOT_LOCKED", output["reason_code"])
            self.assertEqual(
                "repair_intent_and_repeat_purple",
                output["next_legal_action"],
            )

    def test_inline_intent_lock_format_is_accepted_when_digest_matches(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            for stage in ("A", "B", "C", "D"):
                passing_handoff(run_root, stage)
            intent = run_root / "pack/intent.md"
            write(intent, "# Intent\n")
            write(
                run_root / "pack/intent_lock_report.md",
                "- Verdict: PASS\n"
                f"- `intent.md` v2, SHA-256 `{RUNTIME.file_sha256(intent)}`\n",
            )
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("PLANNING_IN_PROGRESS", output["state"])
            self.assertEqual("run_stage_e", output["next_legal_action"])

    def test_inline_intent_lock_format_still_blocks_on_digest_mismatch(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            for stage in ("A", "B", "C", "D"):
                passing_handoff(run_root, stage)
            write(run_root / "pack/intent.md", "# Intent\n")
            write(
                run_root / "pack/intent_lock_report.md",
                "- Verdict: PASS\n"
                f"- `intent.md` v2, SHA-256 `{'0' * 64}`\n",
            )
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("BLOCKED", output["state"])
            self.assertEqual("CONDUCTOR_INTENT_NOT_LOCKED", output["reason_code"])

    def test_valid_intent_lock_allows_stage_e(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            run_root = create_run(root)
            for stage in ("A", "B", "C", "D"):
                passing_handoff(run_root, stage)
            intent = run_root / "pack/intent.md"
            write(intent, "# Intent\n")
            write(
                run_root / "pack/intent_lock_report.md",
                "- Verdict: PASS\n"
                f"- Locked SHA-256: `{RUNTIME.file_sha256(intent)}`\n",
            )
            output = RUNTIME.evaluate_progress(root)
            self.assertEqual("PLANNING_IN_PROGRESS", output["state"])
            self.assertEqual("run_stage_e", output["next_legal_action"])


if __name__ == "__main__":
    unittest.main()
