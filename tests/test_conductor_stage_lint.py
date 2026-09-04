import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from conductor_pack_lint import WORD_CAPS, check_word_cap  # noqa: E402
from conductor_stage_lint import (  # noqa: E402
    STAGE_OUTPUTS,
    check_stage_output_word_cap,
    lint_stage,
)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def handoff_text(output_line: str) -> str:
    return (
        "## Version\n"
        "v1\n"
        "## Change Log\n"
        "- v1 current\n"
        "## Stage\n"
        "- Stage ID: STAGE_B\n"
        "## Iteration\n"
        "- Iteration: 1 of max 2\n"
        "## Inputs (LOAD)\n"
        "- source\n"
        "## Inputs (DISK)\n"
        "- source\n"
        "## Skill Routing Contract\n"
        "- Skill used (or `NONE`): NONE\n"
        "## Outputs Produced (paths)\n"
        f"{output_line}\n"
        "## Verification Steps Recommended\n"
        "- inspect\n"
        "## Exit Criteria Status\n"
        "- PASS\n"
    )


class FactoryStageOutputPathTests(unittest.TestCase):
    def lint(self, root: Path, output_line: str):
        run_id = "RUN_20260813_0000_fixture"
        run_root = root / "docs/Conductor/runs" / run_id
        write(run_root / "pack/intent_redteam.md", "evidence\n")
        write(run_root / "pack/HANDOFF/HANDOFF_STAGE_B.md", handoff_text(output_line))
        return lint_stage(root, run_id, "B")

    def test_accepts_nonempty_run_relative_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "docs/Conductor/runs/RUN_20260813_0000_fixture/pack/evidence.txt", "ok\n")
            self.assertEqual("PASS", self.lint(root, "- `pack/evidence.txt`")["status"])

    def test_accepts_nonempty_repository_relative_docs_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "docs/shared-evidence.txt", "ok\n")
            self.assertEqual("PASS", self.lint(root, "- `docs/shared-evidence.txt`")["status"])

    def test_rejects_malformed_or_unsafe_declarations(self):
        cases = (
            "- pack/evidence.txt",
            "- `pack/*.txt`",
            "- `/tmp/evidence.txt`",
            "- `../evidence.txt`",
            "- `pack/$(command).txt`",
        )
        for output_line in cases:
            with self.subTest(output_line=output_line), tempfile.TemporaryDirectory() as temp_dir:
                result = self.lint(Path(temp_dir), output_line)
                self.assertEqual("FAIL", result["status"])

    def test_rejects_missing_or_empty_targets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            missing = self.lint(root, "- `pack/missing.txt`")
            self.assertEqual("FAIL", missing["status"])
            self.assertTrue(any("missing output" in item for item in missing["errors"]))

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write(root / "docs/Conductor/runs/RUN_20260813_0000_fixture/pack/empty.txt", "")
            empty = self.lint(root, "- `pack/empty.txt`")
            self.assertEqual("FAIL", empty["status"])
            self.assertTrue(any("empty output" in item for item in empty["errors"]))

    def test_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            outside = root / "outside"
            write(outside / "evidence.txt", "secret\n")
            link = root / "docs/Conductor/runs/RUN_20260813_0000_fixture/pack/link"
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(outside, target_is_directory=True)
            result = self.lint(root, "- `pack/link/evidence.txt`")
            self.assertEqual("FAIL", result["status"])
            self.assertTrue(any("escapes its root" in item for item in result["errors"]))

    def test_stage_artifact_caps_match_pack_lint_under_exact_and_over(self):
        cases = (
            ("A", "intent.md"),
            ("C", "intent.md"),
            ("C", "intent_synthesis.md"),
            ("D", "intent_lock_report.md"),
            ("E", "premortem.md"),
            ("E", "risk_register.md"),
            ("F", "verification_plan.md"),
        )
        for stage, name in cases:
            self.assertTrue(any(path.endswith(name) for path in STAGE_OUTPUTS[stage]))
            cap = WORD_CAPS[name]
            for relation, count, expected_failure in (
                ("under", cap - 1, False),
                ("exact", cap, False),
                ("over", cap + 1, True),
            ):
                with self.subTest(stage=stage, artifact=name, relation=relation):
                    text = "word " * count
                    stage_errors: list[str] = []
                    pack_errors: list[str] = []
                    check_stage_output_word_cap(Path(name), text, stage_errors)
                    check_word_cap(Path(name), text, pack_errors)
                    self.assertEqual(expected_failure, bool(stage_errors))
                    self.assertEqual(pack_errors, stage_errors)


if __name__ == "__main__":
    unittest.main()
