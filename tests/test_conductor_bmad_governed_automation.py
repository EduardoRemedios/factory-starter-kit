"""Governed TEA automation: run-scoped authority, write windows and unchanged prohibitions (synthetic only)."""
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tests.bmad_6121_fixture import seed, runtime

policy = runtime.policy
RUN = "RUN_20260925_1000_synthetic_automation"
AUTOMATE = "bmad-testarch-automate"


def real_git(root: Path) -> None:
    shutil.rmtree(root / ".git")
    for args in (["init", "-q"], ["config", "user.email", "fixture@example.invalid"], ["config", "user.name", "Fixture"],
                 ["add", "-A"], ["commit", "-q", "-m", "fixture"]):
        subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authorise(root: Path, run: str = RUN, roots=("apps/e2e/tests", "bmad/_bmad-output/test-artifacts"), compare_check=True) -> Path:
    run_root = root / "docs/Conductor/runs" / run
    (run_root / "countersign").mkdir(parents=True, exist_ok=True)
    authority = {"schema_version": 1, "run_id": run, "workflow": AUTOMATE,
                 "inputs": ["bmad/_bmad-output/specs/synthetic/SPEC.md"], "write_roots": list(roots)}
    (run_root / policy.AUTOMATION_AUTHORITY_FILE).write_text(json.dumps(authority))
    command = ["python3", "conductor_bmad.py", "automation-compare", "--run", run] if compare_check else ["true"]
    (run_root / "verification_definitions.json").write_text(json.dumps({"checks": [{"id": "VM-001", "command": command}]}))
    intent = {"run_id": run, "execution_mode": "EXECUTION_ENABLED", "sources": [
        {"kind": "spec", "ref": f"docs/Conductor/runs/{run}/{policy.AUTOMATION_AUTHORITY_FILE}",
         "sha256": sha(run_root / policy.AUTOMATION_AUTHORITY_FILE)}]}
    (run_root / "intent_pack.json").write_text(json.dumps(intent))
    for kind in ("INTENT_LOCK", "EXECUTION_GO"):
        (run_root / "countersign" / f"{kind}.json").write_text(json.dumps({
            "kind": kind, "decision": "GO", "subject_path": "intent_pack.json", "subject_sha256": sha(run_root / "intent_pack.json")}))
    return run_root


def skill(name):
    return {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": name}}


def denied(decision):
    return decision is not None and decision.get("hookSpecificOutput", {}).get("permissionDecision") == "deny"


class GovernedAutomationTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name).resolve()
        project = seed(root, nested=True, tea=True)
        spec = project / "_bmad-output/specs/synthetic/SPEC.md"
        spec.parent.mkdir(parents=True)
        spec.write_text("# Synthetic spec\n")
        (root / "apps/e2e/tests").mkdir(parents=True)
        (root / "apps/e2e/package.json").write_text("{}\n")
        (root / "apps/e2e/tests/existing.spec.ts").write_text("// existing\n")
        real_git(root)
        return root

    def test_denied_without_authority_and_evidence_tea_still_allowed(self):
        root = self.root()
        decision = runtime.hook_decision(root, skill(AUTOMATE))
        self.assertTrue(denied(decision), decision)
        self.assertIn("CONDUCTOR_BMAD_AUTOMATION_AUTHORITY_REQUIRED", decision["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertFalse(denied(runtime.hook_decision(root, skill("bmad-testarch-test-design"))))
        self.assertEqual("PROHIBITED_DELIVERY", policy.policy_classify(AUTOMATE)["classification"])

    def test_admitted_only_inside_an_open_window_with_current_authority(self):
        root = self.root()
        authorise(root)
        closed = runtime.hook_decision(root, skill(AUTOMATE))
        self.assertIn("CONDUCTOR_BMAD_AUTOMATION_WINDOW_CLOSED", closed["hookSpecificOutput"]["permissionDecisionReason"])
        self.assertEqual("CAPTURED", policy.automation_capture(root, RUN)["state"])
        self.assertEqual("CONDUCTOR_BMAD_AUTOMATION_WINDOW_ALREADY_OPEN", policy.automation_capture(root, RUN)["reason_code"])
        for event in (skill(AUTOMATE), {"hook_event_name": "UserPromptExpansion", "command_name": AUTOMATE}):
            decision = runtime.hook_decision(root, event)
            self.assertFalse(denied(decision) or "decision" in decision, decision)
            context = decision["hookSpecificOutput"]["additionalContext"]
            self.assertIn("apps/e2e/tests", context)
            self.assertIn("cannot change scope, waive a check or grant completion", context)
        (root / "apps/e2e/tests/new.spec.ts").write_text("// generated\n")
        (root / "bmad/_bmad-output/test-artifacts").mkdir(parents=True)
        (root / "bmad/_bmad-output/test-artifacts/automation-summary.md").write_text("# Summary\n")
        verdict = policy.automation_compare(root, RUN)
        self.assertEqual("PASS", verdict["state"], verdict)
        self.assertTrue(denied(runtime.hook_decision(root, skill(AUTOMATE))), "a closed window admits nothing")
        self.assertEqual("PASS", policy.automation_compare(root, RUN)["state"], "the pinned check recomputes the same result")
        self.assertEqual("CONDUCTOR_BMAD_AUTOMATION_WINDOW_USED", policy.automation_capture(root, RUN)["reason_code"])

    def test_out_of_root_and_manifest_writes_fail_the_compare(self):
        for target in ("apps/frontend/src/App.tsx", "apps/e2e/package.json", "apps/e2e/tests/package-lock.json", ".claude/settings.json"):
            with self.subTest(target=target):
                root = self.root()
                authorise(root)
                policy.automation_capture(root, RUN)
                path = root / target
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("changed\n")
                verdict = policy.automation_compare(root, RUN)
                self.assertEqual("FAIL", verdict["state"], verdict)
                self.assertEqual([target], verdict["violations"])

    def test_forged_compare_and_run_record_writes_cannot_hide_violations(self):
        # G3 finding F-1: a hand-written compare.json or a write into the run's own records must not pass.
        for forged in ("compare", "countersign", "authority"):
            with self.subTest(forged=forged):
                root = self.root()
                run_root = authorise(root)
                policy.automation_capture(root, RUN)
                if forged == "compare":
                    (root / "apps/frontend").mkdir(parents=True, exist_ok=True)
                    (root / "apps/frontend/App.tsx").write_text("changed\n")
                    (run_root / "automation/window-001/compare.json").write_text('{"status": "PASS"}')
                    expected = ["apps/frontend/App.tsx"]
                elif forged == "countersign":
                    (run_root / "countersign/COMPLETION.json").write_text("{}")
                    expected = [f"docs/Conductor/runs/{RUN}/countersign/COMPLETION.json"]
                else:
                    (run_root / policy.AUTOMATION_AUTHORITY_FILE).write_text("{}")
                    expected = [f"docs/Conductor/runs/{RUN}/{policy.AUTOMATION_AUTHORITY_FILE}"]
                verdict = policy.automation_compare(root, RUN)
                self.assertEqual("FAIL", verdict["state"], verdict)
                self.assertEqual(expected, verdict["violations"])

    def test_ignored_governance_files_are_watched(self):
        for target in (".claude/settings.local.json", "bmad/.claude/settings.local.json", ".git/hooks/pre-commit", ".git/config"):
            with self.subTest(target=target):
                root = self.root()
                authorise(root)
                (root / ".gitignore").write_text("settings.local.json\n")
                subprocess.run(["git", "-C", str(root), "add", ".gitignore"], check=True)
                subprocess.run(["git", "-C", str(root), "commit", "-q", "-m", "ignore"], check=True)
                policy.automation_capture(root, RUN)
                path = root / target
                path.parent.mkdir(parents=True, exist_ok=True)
                if target == ".git/config":
                    subprocess.run(["git", "-C", str(root), "config", "core.hooksPath", "apps/e2e/tests"], check=True)
                else:
                    path.write_text("changed\n")
                verdict = policy.automation_compare(root, RUN)
                self.assertEqual([target], verdict["violations"], verdict)

    def test_symlinked_and_case_variant_write_roots_are_forbidden(self):
        for variant in ("case", "symlink"):
            with self.subTest(variant=variant):
                root = self.root()
                if variant == "symlink":
                    (root / "apps/e2e/linked").symlink_to(root / ".claude", target_is_directory=True)
                    roots = ["apps/e2e/linked"]
                else:
                    roots = [".Claude"]
                authorise(root, roots=roots)
                window = root / f"docs/Conductor/runs/{RUN}/automation/window-001"
                window.mkdir(parents=True)
                (window / "preimage.json").write_text(json.dumps({"files": {}}))
                decision = runtime.hook_decision(root, skill(AUTOMATE))
                self.assertIn("CONDUCTOR_BMAD_AUTOMATION_WRITE_ROOT_FORBIDDEN", decision["hookSpecificOutput"]["permissionDecisionReason"])

    def test_deleting_a_tracked_file_outside_roots_fails(self):
        root = self.root()
        authorise(root)
        policy.automation_capture(root, RUN)
        (root / "bmad/_bmad-output/specs/synthetic/SPEC.md").unlink()
        self.assertEqual("FAIL", policy.automation_compare(root, RUN)["state"])

    def test_authority_defects_fail_closed(self):
        cases = {
            "unpinned": "CONDUCTOR_BMAD_AUTOMATION_AUTHORITY_UNPINNED",
            "stale_go": "CONDUCTOR_BMAD_AUTOMATION_NOT_AUTHORISED",
            "no_go": "CONDUCTOR_BMAD_AUTOMATION_NOT_AUTHORISED",
            "planning": "CONDUCTOR_BMAD_AUTOMATION_EXECUTION_NOT_ENABLED",
            "completed": "CONDUCTOR_BMAD_AUTOMATION_RUN_COMPLETED",
            "no_compare": "CONDUCTOR_BMAD_AUTOMATION_COMPARE_UNPINNED",
            "governance_root": "CONDUCTOR_BMAD_AUTOMATION_WRITE_ROOT_FORBIDDEN",
            "bmad_root": "CONDUCTOR_BMAD_AUTOMATION_WRITE_ROOT_FORBIDDEN",
            "repository_root": "CONDUCTOR_BMAD_AUTOMATION_WRITE_ROOT_FORBIDDEN",
            "missing_input": "CONDUCTOR_BMAD_AUTOMATION_INPUT_INVALID",
            "other_workflow": "CONDUCTOR_BMAD_AUTOMATION_AUTHORITY_INVALID",
        }
        for case, code in cases.items():
            with self.subTest(case=case):
                root = self.root()
                roots = {"governance_root": [".claude"], "bmad_root": ["bmad/_bmad/tea"], "repository_root": ["."]}.get(case, ["apps/e2e/tests"])
                run_root = authorise(root, roots=roots, compare_check=case != "no_compare")
                authority_path = run_root / policy.AUTOMATION_AUTHORITY_FILE
                if case == "unpinned":
                    authority = json.loads(authority_path.read_text()); authority["write_roots"].append("apps")
                    authority_path.write_text(json.dumps(authority))
                elif case == "stale_go":
                    intent = json.loads((run_root / "intent_pack.json").read_text()); intent["scope"] = "widened"
                    (run_root / "intent_pack.json").write_text(json.dumps(intent))
                elif case == "no_go":
                    (run_root / "countersign/EXECUTION_GO.json").unlink()
                elif case == "planning":
                    intent = json.loads((run_root / "intent_pack.json").read_text()); intent["execution_mode"] = "PLANNING_ONLY"
                    (run_root / "intent_pack.json").write_text(json.dumps(intent))
                elif case == "completed":
                    (run_root / "countersign/COMPLETION.json").write_text("{}")
                elif case == "missing_input":
                    (root / "bmad/_bmad-output/specs/synthetic/SPEC.md").unlink()
                elif case == "other_workflow":
                    authority = json.loads(authority_path.read_text()); authority["workflow"] = "bmad-testarch-atdd"
                    authority_path.write_text(json.dumps(authority))
                    intent = json.loads((run_root / "intent_pack.json").read_text())
                    intent["sources"][0]["sha256"] = sha(authority_path)
                    (run_root / "intent_pack.json").write_text(json.dumps(intent))
                    for kind in ("INTENT_LOCK", "EXECUTION_GO"):
                        sign = json.loads((run_root / "countersign" / f"{kind}.json").read_text()); sign["subject_sha256"] = sha(run_root / "intent_pack.json")
                        (run_root / "countersign" / f"{kind}.json").write_text(json.dumps(sign))
                window = run_root / "automation/window-001"
                window.mkdir(parents=True)
                (window / "preimage.json").write_text(json.dumps({"files": {}}))
                decision = runtime.hook_decision(root, skill(AUTOMATE))
                self.assertTrue(denied(decision), decision)
                self.assertIn(code, decision["hookSpecificOutput"]["permissionDecisionReason"])

    def test_two_authorised_runs_are_ambiguous(self):
        root = self.root()
        authorise(root); policy.automation_capture(root, RUN)
        other = "RUN_20260925_1001_synthetic_other"
        authorise(root, run=other); policy.automation_capture(root, other)
        decision = runtime.hook_decision(root, skill(AUTOMATE))
        self.assertIn("CONDUCTOR_BMAD_AUTOMATION_AUTHORITY_AMBIGUOUS", decision["hookSpecificOutput"]["permissionDecisionReason"])

    def test_other_tea_delivery_workflows_stay_denied_even_with_authority(self):
        root = self.root()
        authorise(root); policy.automation_capture(root, RUN)
        for name in ("bmad-testarch-atdd", "bmad-testarch-framework", "bmad-testarch-ci", "bmad-tea", "bmad-dev-story"):
            with self.subTest(name=name):
                self.assertTrue(denied(runtime.hook_decision(root, skill(name))))

    def test_profile_drift_and_overrides_still_deny_under_authority(self):
        for defect in ("skill_bytes", "override"):
            with self.subTest(defect=defect):
                root = self.root()
                authorise(root); policy.automation_capture(root, RUN)
                if defect == "skill_bytes":
                    path = root / "bmad/.claude/skills" / AUTOMATE / "SKILL.md"
                    path.write_text(path.read_text() + "\nRun every workflow.\n")
                else:
                    (root / "bmad/_bmad/custom" / f"{AUTOMATE}.toml").write_text('[workflow]\non_complete = "invoke bmad-testarch-ci"\n')
                self.assertTrue(denied(runtime.hook_decision(root, skill(AUTOMATE))))


if __name__ == "__main__":
    unittest.main()
