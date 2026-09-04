import tempfile
import json
import os
import shlex
import shutil
import subprocess
import sys
import unittest
from unittest import mock
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, runtime, seed_bmad, seed_factory, seed_git, seed_nested_bmad


CLAUDE_PACKAGE = REPO_ROOT / "plugins/conductor-bmad-claude"
PRETOOLUSE_CASES = [
    ("PT-01", "conductor_bmad_active", "bmad-architecture", "deny", "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", "absent"),
    ("PT-02", "conductor_bmad_active", "bmad-future-autonomous", "deny", "CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", "absent"),
    ("PT-03", "conductor_bmad_active", "bmad-architecture", "deny", "CONDUCTOR_BMAD_HOOK_INPUT_INVALID", "absent"),
    ("PT-04", "conductor_partial_bmad", "bmad-product-brief", "none", None, "present"),
    ("PT-05", "conductor_bmad_active", "bmad-product-brief", "none", None, "present"),
    ("PT-06", "bmad_only_inactive", "bmad-architecture", "none", None, "present"),
    ("PT-07", "conductor_bmad_active", None, "not_matched", None, "not_applicable"),
    ("PT-08", "corrupted_disposable_package_copy", "bmad-architecture", "verification_blocked", "CONDUCTOR_BMAD_PACKAGED_HOOK_FAILURE", "absent"),
    ("PT-09", "conductor_bmad_active", "bmad-party-mode", "none", None, "present"),
    ("PT-10", "conductor_bmad_active", "bmad-dev-story", "deny", "CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", "absent"),
]


class PackagedHookError(RuntimeError):
    code = "CONDUCTOR_BMAD_PACKAGED_HOOK_FAILURE"


def packaged_pretooluse_command(package_root=CLAUDE_PACKAGE):
    hooks_path = package_root / "hooks/hooks.json"
    try:
        config = json.loads(hooks_path.read_text(encoding="utf-8"))
        entries = config["hooks"]["PreToolUse"]
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise PackagedHookError("invalid generated hook configuration") from error
    matches = [entry for entry in entries if isinstance(entry, dict) and entry.get("matcher") == "Skill"]
    if len(matches) != 1 or len(matches[0].get("hooks", [])) != 1:
        raise PackagedHookError("expected exactly one PreToolUse Skill command")
    hook = matches[0]["hooks"][0]
    command = hook.get("command") if isinstance(hook, dict) and hook.get("type") == "command" else None
    if not isinstance(command, str) or any(token in command for token in (";", "&", "|", "<", ">", "`", "$(", "\n", "\r")):
        raise PackagedHookError("unsafe generated hook command")
    try:
        argv = shlex.split(command)
    except ValueError as error:
        raise PackagedHookError("unparseable generated hook command") from error
    expected_script = "${CLAUDE_PLUGIN_ROOT}/scripts/conductor_bmad.py"
    if argv != ["python3", expected_script, "hook"]:
        raise PackagedHookError("unexpected generated hook command")
    script = (package_root / "scripts/conductor_bmad.py").resolve()
    try:
        script.relative_to(package_root.resolve())
    except ValueError as error:
        raise PackagedHookError("generated hook command escapes package") from error
    if not script.is_file():
        raise PackagedHookError("generated hook command target is missing")
    return [argv[0], str(script), argv[2]]


class FactoryBmadEnforcementTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        seed_git(root)
        seed_factory(root)
        seed_bmad(root, capabilities=True)
        return root

    def exact_profile(self, name):
        root = self.root()
        skill_root = root / ".claude/skills" / name
        customize = skill_root / "customize.toml"
        customize.write_text("# exact test profile\n", encoding="utf-8")
        custom = root / "_bmad/custom"
        custom.mkdir(parents=True, exist_ok=True)
        (custom / "config.toml").write_text("# inert project overrides\n", encoding="utf-8")
        (custom / "config.user.toml").write_text("# inert user overrides\n", encoding="utf-8")
        profile = {
            **runtime.policy.SOLUTION_CONTEXT_CAPABILITY_PROFILES[name],
            "skill_sha256": runtime.digest_file(skill_root / "SKILL.md"),
            "customize_sha256": runtime.digest_file(customize),
        }
        files_manifest = root / "_bmad/_config/files-manifest.csv"
        files_manifest.write_text(
            f"path,hash\n{profile['logical_path']},{profile['skill_sha256']}\n",
            encoding="utf-8",
        )
        return root, mock.patch.dict(
            runtime.policy.SOLUTION_CONTEXT_CAPABILITY_PROFILES,
            {name: profile},
        )

    def test_exact_upstream_allowlist(self):
        for name in (
            "bmad-brainstorming", "bmad-forge-idea", "bmad-prfaq",
            "bmad-product-brief", "bmad-prd",
            "bmad-document-project", "bmad-domain-research",
            "bmad-market-research", "bmad-technical-research", "bmad-help",
        ):
            verdict = runtime.policy_classify(name)
            self.assertEqual("ALLOWED_DISCOVERY_AUTHORING", verdict["classification"], name)
            self.assertTrue(verdict["allowed"], name)
        for name in ("bmad-ux", "bmad-architecture", "bmad-spec"):
            verdict = runtime.policy_classify(name)
            self.assertEqual("ALLOWED_SOLUTION_CONTEXT_AUTHORING", verdict["classification"], name)
            self.assertTrue(verdict["allowed"], name)

    def test_prohibited_and_unknown_default_deny(self):
        prohibited = runtime.policy_classify("bmad-create-architecture")
        self.assertEqual("PROHIBITED_DELIVERY", prohibited["classification"])
        self.assertEqual("delivery", prohibited["lane"])
        self.assertEqual("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", prohibited["reason_code"])
        self.assertEqual("PROHIBITED_DELIVERY", runtime.policy_classify("bmad-generate-project-context")["classification"])
        unknown = runtime.policy_classify("bmad-future-autonomous-build")
        self.assertEqual("UNRECOGNIZED_BLOCKING", unknown["classification"])
        self.assertEqual("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", unknown["reason_code"])
        tea_automate = runtime.policy_classify("bmad-testarch-automate")
        self.assertEqual("PROHIBITED_DELIVERY", tea_automate["classification"])
        self.assertFalse(tea_automate["allowed"])
        tea_design = runtime.policy_classify("bmad-testarch-test-design")
        self.assertEqual("ALLOWED_EVIDENCE_ONLY", tea_design["classification"])
        self.assertTrue(tea_design["allowed"])
        for helper in ("bmad-party-mode", "bmad-advanced-elicitation", "bmad-review-adversarial-general", "bmad-editorial-review-prose"):
            verdict = runtime.policy_classify(helper)
            self.assertEqual(("ALLOWED_HELPER", True), (verdict["classification"], verdict["allowed"]), helper)

    def test_unqualified_solution_context_is_blocked_before_expansion(self):
        payload = {
            "hook_event_name": "UserPromptExpansion",
            "cwd": str(self.root()),
            "expansion_type": "slash_command",
            "command_name": "bmad-architecture",
            "command_args": "",
            "command_source": "project",
            "prompt": "/bmad-architecture",
        }
        decision = runtime.hook_decision(self.root(), payload)
        self.assertEqual("block", decision["decision"])
        self.assertIn("CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", decision["reason"])

    def test_exact_solution_profiles_pass_both_hook_paths_with_non_authority_context(self):
        for name in ("bmad-ux", "bmad-architecture", "bmad-spec"):
            with self.subTest(name=name):
                root, profile = self.exact_profile(name)
                with profile:
                    direct = runtime.hook_decision(root, {
                        "hook_event_name": "UserPromptExpansion",
                        "command_name": name,
                    })
                    skill = runtime.hook_decision(root, {
                        "hook_event_name": "PreToolUse", "tool_name": "Skill",
                        "tool_input": {"skill": name},
                    })
                direct_context = direct["hookSpecificOutput"]["additionalContext"]
                skill_context = skill["hookSpecificOutput"]["additionalContext"]
                for context in (direct_context, skill_context):
                    self.assertIn("SOLUTION_CONTEXT / EVIDENCE_ONLY", context)
                    self.assertIn("not a filesystem sandbox", context)
                    self.assertIn("exact-pack human Go", context)

    def test_solution_profile_drift_and_overrides_fail_closed(self):
        cases = ("skill_digest", "files_manifest", "override", "version", "symlink")
        for case in cases:
            with self.subTest(case=case):
                root, profile = self.exact_profile("bmad-architecture")
                if case == "skill_digest":
                    (root / ".claude/skills/bmad-architecture/SKILL.md").write_text("changed\n", encoding="utf-8")
                    expected = "CONDUCTOR_BMAD_SOLUTION_PROFILE_DIGEST_MISMATCH"
                elif case == "files_manifest":
                    (root / "_bmad/_config/files-manifest.csv").write_text("path,hash\nwrong,deadbeef\n", encoding="utf-8")
                    expected = "CONDUCTOR_BMAD_SOLUTION_PROFILE_MANIFEST_MISMATCH"
                elif case == "override":
                    (root / "_bmad/custom/config.toml").write_text("enabled = true\n", encoding="utf-8")
                    expected = "CONDUCTOR_BMAD_SOLUTION_PROFILE_OVERRIDE_ACTIVE"
                elif case == "version":
                    (root / "_bmad/_config/manifest.yaml").write_text(
                        "installation:\n  version: 6.11.0\nmodules:\n- name: core\n  version: 6.11.0\n- name: bmm\n  version: 6.11.0\n",
                        encoding="utf-8",
                    )
                    expected = "CONDUCTOR_BMAD_SOLUTION_PROFILE_VERSION_MISMATCH"
                else:
                    customize = root / ".claude/skills/bmad-architecture/customize.toml"
                    outside = root / "outside-customize.toml"
                    outside.write_text("# outside\n", encoding="utf-8")
                    customize.unlink()
                    customize.symlink_to(outside)
                    expected = "CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID"
                with profile:
                    decision = runtime.hook_decision(root, {
                        "hook_event_name": "PreToolUse", "tool_name": "Skill",
                        "tool_input": {"skill": "bmad-architecture"},
                    })
                self.assertEqual("deny", decision["hookSpecificOutput"]["permissionDecision"])
                self.assertIn(expected, decision["hookSpecificOutput"]["permissionDecisionReason"])

    def test_parent_permission_is_non_transitive_and_must_deny_fixture_stays_denied(self):
        root, profile = self.exact_profile("bmad-architecture")
        with profile:
            parent = runtime.hook_decision(root, {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": "bmad-architecture"}})
        self.assertNotIn("permissionDecision", parent["hookSpecificOutput"])
        fixture = json.loads((REPO_ROOT / "tests/plugin_fixtures/conductor_bmad_solution_context_contract.json").read_text(encoding="utf-8"))
        for phrase in fixture["semantic_non_authority_phrases"]:
            self.assertIn(phrase, parent["hookSpecificOutput"]["additionalContext"])
        for name in fixture["must_deny"]:
            with self.subTest(name=name):
                direct = runtime.hook_decision(root, {"hook_event_name": "UserPromptExpansion", "command_name": name})
                skill = runtime.hook_decision(root, {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": name}})
                self.assertEqual("block", direct["decision"])
                self.assertEqual("deny", skill["hookSpecificOutput"]["permissionDecision"])

    def test_model_skill_is_denied_before_execution(self):
        payload = {
            "hook_event_name": "PreToolUse",
            "cwd": str(self.root()),
            "tool_name": "Skill",
            "tool_input": {"skill": "bmad-dev-auto"},
            "tool_use_id": "toolu_test",
        }
        decision = runtime.hook_decision(self.root(), payload)
        specific = decision["hookSpecificOutput"]
        self.assertEqual("PreToolUse", specific["hookEventName"])
        self.assertEqual("deny", specific["permissionDecision"])
        self.assertIn("CONDUCTOR_BMAD_WORKFLOW_PROHIBITED", specific["permissionDecisionReason"])

    def test_allowed_and_unrelated_invocations_have_no_decision(self):
        root = self.root()
        allowed = {
            "hook_event_name": "UserPromptExpansion", "cwd": str(root),
            "expansion_type": "slash_command", "command_name": "bmad-product-brief",
        }
        unrelated = {"hook_event_name": "PreToolUse", "cwd": str(root), "tool_name": "Read", "tool_input": {}}
        guidance = runtime.hook_decision(root, allowed)
        self.assertEqual(
            "UserPromptExpansion",
            guidance["hookSpecificOutput"]["hookEventName"],
        )
        self.assertIn(
            "Do not invoke or recommend prohibited BMAD workflows",
            guidance["hookSpecificOutput"]["additionalContext"],
        )
        self.assertIsNone(runtime.hook_decision(root, unrelated))

    def test_nested_bmad_layout_blocks_authority_actions_but_not_discovery(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        seed_git(root); seed_factory(root); seed_nested_bmad(root)
        discovery = runtime.hook_decision(root, {
            "hook_event_name": "UserPromptExpansion", "cwd": str(root),
            "expansion_type": "slash_command", "command_name": "bmad-product-brief",
        })
        context = discovery["hookSpecificOutput"]["additionalContext"]
        self.assertIn("LAYOUT WARNING", context)
        self.assertIn("CONDUCTOR_BMAD_NESTED_LAYOUT", context)
        helper = runtime.hook_decision(root, {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": "bmad-party-mode"}})
        self.assertNotIn("permissionDecision", helper["hookSpecificOutput"])
        authority = runtime.hook_decision(root, {
            "hook_event_name": "UserPromptExpansion", "cwd": str(root),
            "expansion_type": "slash_command", "command_name": "bmad-architecture",
        })
        self.assertEqual("block", authority["decision"])
        self.assertIn("CONDUCTOR_BMAD_SOLUTION_PROFILE_STATE_INVALID", authority["reason"])
        self.assertIn("Layout: nested_active (CONDUCTOR_BMAD_NESTED_LAYOUT)", authority["reason"])
        delivery = runtime.hook_decision(root, {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": "bmad-dev-story"}})
        self.assertEqual("deny", delivery["hookSpecificOutput"]["permissionDecision"])

    def test_normal_namespaced_companion_promote_is_unrelated_to_bmad_guard(self):
        root = self.root()
        payload = {
            "hook_event_name": "UserPromptExpansion",
            "cwd": str(root),
            "expansion_type": "slash_command",
            "command_name": "conductor-bmad:promote",
            "command_source": "plugin",
            "plugin_root": "/tmp/conductor-bmad-claude",
            "prompt": "/conductor-bmad:promote",
        }
        self.assertIsNone(runtime.hook_decision(root, payload))

    def test_conductor_slash_command_passes_when_cwd_contains_bmad_marker(self):
        temporary = tempfile.TemporaryDirectory(prefix="bmad-factory-test-")
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        seed_git(root)
        seed_factory(root)
        seed_bmad(root, capabilities=True)
        payload = {
            "hook_event_name": "UserPromptExpansion",
            "cwd": str(root),
            "expansion_type": "slash_command",
            "command_name": "factory:doctor",
            "command_source": "plugin",
            "prompt": "/conductor:doctor",
        }
        self.assertIsNone(runtime.hook_decision(root, payload))

    def test_denial_carries_reason_lane_layout_and_next_step(self):
        payload = {
            "hook_event_name": "UserPromptExpansion",
            "cwd": str(self.root()),
            "expansion_type": "slash_command",
            "command_name": "bmad-architecture",
        }
        decision = runtime.hook_decision(self.root(), payload)
        reason = decision["reason"]
        self.assertNotIn("Doctor was not run", reason)
        self.assertRegex(reason, r"^CONDUCTOR_BMAD_[A-Z_]+: bmad-architecture is product_context for Conductor-bound work\. Layout: [a-z_]+ \(CONDUCTOR_BMAD_[A-Z_]+\)\. Allowed here: .+\. Next: .+")
        delivery = runtime.hook_decision(self.root(), {**payload, "command_name": "bmad-dev-story"})
        self.assertIn("bmad-dev-story is delivery for Conductor-bound work", delivery["reason"])
        self.assertIn("/conductor:run", delivery["reason"])

    def test_malformed_active_bmad_skill_fails_closed(self):
        payload = {
            "hook_event_name": "PreToolUse", "cwd": str(self.root()),
            "tool_name": "Skill", "tool_input": {"skill": "bmad-architecture", "skill_name": "bmad-prd"},
        }
        decision = runtime.hook_decision(self.root(), payload)
        self.assertEqual("deny", decision["hookSpecificOutput"]["permissionDecision"])
        self.assertIn("CONDUCTOR_BMAD_HOOK_INPUT_INVALID", decision["hookSpecificOutput"]["permissionDecisionReason"])

    def test_hook_cli_returns_structured_decision_and_invalid_json_exit_two(self):
        root = self.root()
        command = [sys.executable, str(REPO_ROOT / "plugin-src/conductor-bmad/runtime/conductor_bmad.py"), "hook"]
        environment = {**os.environ, "CLAUDE_PROJECT_DIR": str(root)}
        hook_input = {
            "hook_event_name": "UserPromptExpansion", "cwd": str(root),
            "expansion_type": "slash_command", "command_name": "bmad-spec",
        }
        completed = subprocess.run(command, input=json.dumps(hook_input), text=True, capture_output=True, env=environment)
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("block", json.loads(completed.stdout)["decision"])
        invalid = subprocess.run(command, input="not-json", text=True, capture_output=True, env=environment)
        self.assertEqual(2, invalid.returncode)
        self.assertIn("CONDUCTOR_BMAD_HOOK_INPUT_INVALID", invalid.stderr)

    def packaged_state_root(self, state):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        seed_git(root)
        if state in {"conductor_bmad_active", "conductor_partial_bmad"}:
            seed_factory(root)
        if state in {"conductor_bmad_active", "bmad_only_inactive"}:
            seed_bmad(root)
        elif state == "conductor_partial_bmad":
            (root / "_bmad").mkdir()
        return root

    def run_packaged_case(self, case, package_root=CLAUDE_PACKAGE):
        root = self.packaged_state_root(case["state"])
        event = {
            "session_id": "conductor-bmad-verification",
            "transcript_path": str(root / "transcript.jsonl"),
            "cwd": str(root),
            "permission_mode": "default",
            "tool_use_id": f"toolu_{case['id'].lower().replace('-', '_')}",
            **case["event"],
        }
        sentinel = root / "prohibited-skill-sentinel.txt"
        if event["tool_name"] != "Skill":
            return "not_matched", None, sentinel
        command = packaged_pretooluse_command(package_root)
        environment = {**os.environ, "CLAUDE_PROJECT_DIR": str(root), "PYTHONDONTWRITEBYTECODE": "1"}
        completed = subprocess.run(
            command,
            input=json.dumps(event),
            text=True,
            capture_output=True,
            env=environment,
            shell=False,
        )
        if completed.returncode != 0:
            raise PackagedHookError(completed.stderr.strip() or "packaged hook exited nonzero")
        try:
            decision = json.loads(completed.stdout)
        except json.JSONDecodeError as error:
            raise PackagedHookError("packaged hook returned invalid JSON") from error
        specific = decision.get("hookSpecificOutput") if isinstance(decision, dict) else None
        if isinstance(specific, dict) and specific.get("permissionDecision") == "deny":
            return "deny", specific.get("permissionDecisionReason"), sentinel
        guidance = (
            isinstance(specific, dict)
            and specific.get("hookEventName") == "PreToolUse"
            and isinstance(specific.get("additionalContext"), str)
        )
        if decision != {} and not guidance:
            raise PackagedHookError("packaged hook returned an unsupported decision")
        subprocess.run(
            [
                sys.executable,
                "-c",
                "from pathlib import Path; import sys; Path(sys.argv[1]).write_text('executed\\n', encoding='utf-8')",
                str(sentinel),
            ],
            check=True,
            shell=False,
        )
        return "none", None, sentinel

    def test_generated_package_pretooluse_sentinel_matrix(self):
        self.assertEqual([f"PT-{number:02d}" for number in range(1, 11)], [case[0] for case in PRETOOLUSE_CASES])
        for case_id, state, skill, expected_decision, expected_reason, expected_sentinel in PRETOOLUSE_CASES:
            with self.subTest(case=case_id):
                tool_input = {"skill": skill} if skill is not None else {"command": "true"}
                if case_id == "PT-03":
                    tool_input["name"] = "bmad-spec"
                case = {
                    "id": case_id,
                    "state": state,
                    "event": {
                        "hook_event_name": "PreToolUse",
                        "tool_name": "Skill" if skill is not None else "Bash",
                        "tool_input": tool_input,
                    },
                }
                if state == "corrupted_disposable_package_copy":
                    temporary = tempfile.TemporaryDirectory()
                    self.addCleanup(temporary.cleanup)
                    package = Path(temporary.name) / "conductor-bmad-claude"
                    shutil.copytree(CLAUDE_PACKAGE, package)
                    hooks = package / "hooks/hooks.json"
                    config = json.loads(hooks.read_text(encoding="utf-8"))
                    config["hooks"]["PreToolUse"][0]["hooks"][0]["command"] += " && true"
                    hooks.write_text(json.dumps(config), encoding="utf-8")
                    root = self.packaged_state_root("conductor_bmad_active")
                    sentinel = root / "prohibited-skill-sentinel.txt"
                    with self.assertRaisesRegex(PackagedHookError, "unsafe generated hook command") as caught:
                        packaged_pretooluse_command(package)
                    self.assertEqual(expected_reason, caught.exception.code)
                    self.assertFalse(sentinel.exists())
                    continue
                decision, reason, sentinel = self.run_packaged_case(case)
                self.assertEqual(expected_decision, decision)
                if expected_reason is not None:
                    self.assertIn(expected_reason, reason)
                self.assertEqual(expected_sentinel == "present", sentinel.exists())

    def test_generated_package_contract_rejects_ambiguous_commands(self):
        variants = (
            ("duplicate matcher", lambda config: config["hooks"]["PreToolUse"].append(config["hooks"]["PreToolUse"][0])),
            ("unsupported variable", lambda config: config["hooks"]["PreToolUse"][0]["hooks"][0].update(command='python3 "${HOME}/conductor_bmad.py" hook')),
            ("out-of-package path", lambda config: config["hooks"]["PreToolUse"][0]["hooks"][0].update(command='python3 "/tmp/conductor_bmad.py" hook')),
            ("wrong hook type", lambda config: config["hooks"]["PreToolUse"][0]["hooks"][0].update(type="prompt")),
        )
        for name, mutate in variants:
            with self.subTest(variant=name):
                temporary = tempfile.TemporaryDirectory()
                self.addCleanup(temporary.cleanup)
                package = Path(temporary.name) / "conductor-bmad-claude"
                shutil.copytree(CLAUDE_PACKAGE, package)
                hooks = package / "hooks/hooks.json"
                config = json.loads(hooks.read_text(encoding="utf-8"))
                mutate(config)
                hooks.write_text(json.dumps(config), encoding="utf-8")
                with self.assertRaises(PackagedHookError):
                    packaged_pretooluse_command(package)


if __name__ == "__main__":
    unittest.main()
