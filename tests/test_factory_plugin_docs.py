import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / "docs/onboarding"
REQUIRED_DOCS = {
    "FACTORY_PLUGIN_QUICK_START.md",
    "FACTORY_PLUGIN_REFERENCE.md",
    "FACTORY_PLUGIN_TROUBLESHOOTING.md",
    "FACTORY_PLUGIN_ROLLBACK.md",
    "FACTORY_PLUGIN_PILOT_RUNBOOK.md",
}
SKILL_IDS = {
    "doctor",
    "greenfield",
    "brownfield",
    "progress",
    "run",
    "validate",
    "update",
}


class FactoryPluginDocumentationTests(unittest.TestCase):
    def test_required_documents_exist_and_are_linked(self):
        self.assertTrue(
            all((DOCS_ROOT / name).is_file() for name in REQUIRED_DOCS)
        )
        reference = (DOCS_ROOT / "FACTORY_PLUGIN_REFERENCE.md").read_text(encoding="utf-8")
        self.assertIn("FACTORY_PLUGIN_QUICK_START.md", reference)

    def test_quick_start_names_every_public_entry_point(self):
        reference = (DOCS_ROOT / "FACTORY_PLUGIN_REFERENCE.md").read_text(
            encoding="utf-8"
        )
        for skill_id in SKILL_IDS:
            self.assertIn(f"$factory-{skill_id}", reference)
            self.assertIn(f"/factory:{skill_id}", reference)

    def test_pilot_contains_golden_journeys_and_thresholds(self):
        pilot = (DOCS_ROOT / "FACTORY_PLUGIN_PILOT_RUNBOOK.md").read_text(
            encoding="utf-8"
        )
        for journey in (
            "install",
            "doctor",
            "greenfield",
            "brownfield",
            "progress",
            "validate",
            "update",
            "rollback",
        ):
            self.assertIn(journey, pilot)
        for threshold in (
            "Open Critical defects",
            "Open High defects",
            "Destructive mutations",
            "Recovery success rate",
            "Journey completion rate",
            "Product Owner sign-off",
        ):
            self.assertIn(threshold, pilot)

    def test_troubleshooting_covers_fail_closed_reason_codes(self):
        troubleshooting = (
            DOCS_ROOT / "FACTORY_PLUGIN_TROUBLESHOOTING.md"
        ).read_text(encoding="utf-8")
        for reason in (
            "FACTORY_ENVIRONMENT_UNVERIFIED",
            "FACTORY_CONFLICT_USER_OWNED",
            "FACTORY_UNSAFE_PATH",
            "FACTORY_PLAN_STALE",
            "FACTORY_EVIDENCE_CONTRADICTION",
            "FACTORY_HUMAN_GO_REQUIRED",
            "FACTORY_SKILL_COLLISION",
            "FACTORY_ROLLBACK_EVIDENCE_MISMATCH",
        ):
            self.assertIn(reason, troubleshooting)

    def test_marketplace_policy_values_match_codex_contract(self):
        marketplace = json.loads(
            (REPO_ROOT / ".agents/plugins/marketplace.json").read_text(
                encoding="utf-8"
            )
        )
        entry = marketplace["plugins"][0]
        self.assertEqual("AVAILABLE", entry["policy"]["installation"])
        self.assertIn(
            entry["policy"]["authentication"], {"ON_INSTALL", "ON_USE"}
        )

    def test_runtime_help_exposes_documented_lifecycle_commands(self):
        completed = subprocess.run(
            [
                sys.executable,
                "plugins/factory/scripts/factory_plugin.py",
                "--help",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        for command in (
            "doctor",
            "greenfield",
            "brownfield",
            "progress",
            "update",
            "rollback",
        ):
            self.assertIn(command, completed.stdout)

    def test_skill_guidance_enforces_setup_routing_and_exact_approval(self):
        skill_root = REPO_ROOT / "plugin-src/factory/skills"
        doctor = (skill_root / "doctor.md").read_text(encoding="utf-8")
        self.assertIn(
            "Recommend Greenfield only when it contains no entry other than `.git`",
            doctor,
        )
        for name in ("greenfield.md", "brownfield.md", "update.md"):
            skill = (skill_root / name).read_text(encoding="utf-8")
            self.assertIn("exact full current plan ID", skill)
            self.assertIn("Generic approval", skill)

        greenfield = (skill_root / "greenfield.md").read_text(encoding="utf-8")
        self.assertIn('--root "$PWD"', greenfield)
        self.assertIn("same `--root`", greenfield)
        self.assertIn("Never invent", greenfield)
        self.assertIn("does not require an", greenfield)
        self.assertIn("existing Git worktree", greenfield)
        self.assertIn("authority for Greenfield versus Brownfield", greenfield)
        self.assertIn(".claude/settings.local.json", greenfield)
        self.assertIn("read-only preserved evidence", greenfield)
        self.assertIn("Never edit, delete, chmod, copy", greenfield)

        brownfield = (skill_root / "brownfield.md").read_text(encoding="utf-8")
        self.assertIn('--root "$PWD"', brownfield)
        self.assertIn("same `--root`", brownfield)
        self.assertIn("planned_files", brownfield)
        self.assertIn("change_plan", brownfield)
        self.assertIn("must not be", brownfield)
        self.assertIn("proposed change count", brownfield)

    def test_new_project_runs_greenfield_before_doctor(self):
        quick_start = (DOCS_ROOT / "FACTORY_PLUGIN_QUICK_START.md").read_text(
            encoding="utf-8"
        )
        claude_section = quick_start.split("## Claude Code", 1)[1].split(
            "## What Happens Before Any Write", 1
        )[0]
        self.assertLess(
            claude_section.index("/factory:greenfield"),
            claude_section.index("/factory:doctor"),
        )
        self.assertIn("current working directory", claude_section)
        self.assertIn("same quoted", claude_section)
        self.assertIn(".claude/settings.local.json", claude_section)
        self.assertIn("Factory never manages or", claude_section)
        self.assertIn("requires a fresh preview", claude_section)

    def test_claude_greenfield_troubleshooting_preserves_user_state(self):
        troubleshooting = (
            DOCS_ROOT / "FACTORY_PLUGIN_TROUBLESHOOTING.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Claude Local State Makes Greenfield Look Non-empty",
            troubleshooting,
        )
        self.assertIn(
            "does not parse, manage, modify, or",
            troubleshooting,
        )
        self.assertIn(".claude/hooks/.state/**", troubleshooting)
        self.assertIn("Do not delete user-owned content", troubleshooting)
        self.assertIn(
            "prepare a genuine existing project as a Git worktree",
            troubleshooting,
        )

    def test_validation_guidance_prevents_bytecode_cache_mutation(self):
        validation = (
            REPO_ROOT / "plugin-src/factory/skills/validate.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PYTHONDONTWRITEBYTECODE=1", validation)
        self.assertIn("git status --short", validation)
        self.assertIn("report every difference", validation)
        self.assertIn("bounded tool output", validation)

    def test_execution_contracts_require_exact_go_and_bounded_evidence(self):
        prompt = (REPO_ROOT / "docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md").read_text(
            encoding="utf-8"
        )
        orchestration = (REPO_ROOT / "docs/Factory/ORCHESTRATION.md").read_text(
            encoding="utf-8"
        )
        handoff = (REPO_ROOT / "docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md").read_text(
            encoding="utf-8"
        )
        for text in (prompt, orchestration):
            self.assertIn("- Human Go: RECORDED", text)
            self.assertIn("./scripts/factory-python", text)
            self.assertIn("bounded", text)
        self.assertIn("backtick-quoted exact", orchestration)
        self.assertIn("- `pack/exact-repository-or-run-relative-path`", handoff)

    def test_validation_guidance_preserves_read_only_evidence_boundaries(self):
        validation = (
            REPO_ROOT / "plugin-src/factory/skills/validate.md"
        ).read_text(encoding="utf-8")
        for required in (
            "same first read-only tool command",
            "same final read-only tool command",
            "Do not reuse a digest from an earlier checkpoint",
            "`UNKNOWN`",
            "bounded tool output",
            "explicit exit status",
            "pipe-safe failure propagation",
            "Do not use shell redirection",
            "`|| true`",
            "`/tmp`",
            "`/private/tmp`",
            "guessed scratch directory",
            "explicitly authorize the exact evidence path",
        ):
            self.assertIn(required, validation)

    def test_runtime_skills_use_supported_plugin_root_guidance(self):
        skill_root = REPO_ROOT / "plugin-src/factory/skills"
        for name in (
            "doctor.md",
            "greenfield.md",
            "brownfield.md",
            "progress.md",
            "update.md",
        ):
            skill = (skill_root / name).read_text(encoding="utf-8")
            self.assertIn("${CLAUDE_PLUGIN_ROOT}", skill)
            self.assertIn("by absolute path", skill)
            self.assertNotIn("<plugin-root>", skill)

    def test_distributable_onboarding_is_customer_neutral(self):
        text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(DOCS_ROOT.glob("*.md"))
        )
        for prohibited in ("Symphony", "AuditEdge", "BMAD", "TEA"):
            self.assertNotIn(prohibited, text)

    def test_bmad_handover_guidance_uses_one_integrity_recall_authority_map(self):
        for name in ("FACTORY_BMAD_QUICK_START.md", "FACTORY_BMAD_PILOT_RUNBOOK.md"):
            text = (REPO_ROOT / "docs/adapters/bmad" / name).read_text(encoding="utf-8")
            normalized = " ".join(text.split())
            self.assertIn("Snapshot manifest → project preflight", text)
            self.assertIn("Promoted `artifact.md` → Stage A recall", text)
            self.assertIn("Factory intent → authoritative only after Purple Gate PASS", text)
            self.assertIn("Do not use `SNAPSHOT_MANIFEST.json` as the Stage A required reference", normalized)

    def test_bmad_quick_start_offers_fast_and_full_discovery_routes(self):
        text = (REPO_ROOT / "docs/adapters/bmad/FACTORY_BMAD_QUICK_START.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Fast pilot handover", text)
        self.assertIn("Full discovery", text)
        self.assertIn("one useful technique", text)
        self.assertIn("limitations", text)

    def test_bmad_cli_rollout_docs_are_discoverable_and_bound_desktop(self):
        adapter_root = REPO_ROOT / "docs/adapters/bmad"
        quick_start = (adapter_root / "FACTORY_BMAD_QUICK_START.md").read_text(
            encoding="utf-8"
        )
        for name in (
            "FACTORY_BMAD_CLI_ROLLOUT_PLAYBOOK.md",
            "FACTORY_BMAD_FIRST_TESTER_HANDOFF.md",
            "FACTORY_BMAD_COMPATIBILITY_POLICY.md",
            "FACTORY_BMAD_BOOTSTRAP_RECOVERY.md",
        ):
            self.assertTrue((adapter_root / name).is_file(), name)
            self.assertIn(name, quick_start)
        compatibility = (adapter_root / "FACTORY_BMAD_COMPATIBILITY_POLICY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("verify_factory_bmad_cli_rollout.py", compatibility)
        self.assertIn("Claude Desktop Code tab", compatibility)
        self.assertIn("Unsupported Until Proved", compatibility)
        recovery = (adapter_root / "FACTORY_BMAD_BOOTSTRAP_RECOVERY.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("FACTORY_BMAD_BOOTSTRAP_POST_AUDIT_FAILED", recovery)
        self.assertIn("Do not retry bootstrap blindly", recovery)

    def test_bmad_first_tester_handoff_exercises_full_flow(self):
        handoff = (
            REPO_ROOT / "docs/adapters/bmad/FACTORY_BMAD_FIRST_TESTER_HANDOFF.md"
        ).read_text(encoding="utf-8")
        for required in (
            "ODYSSEY_V3_INITIAL_BMAD_BRIEF.md",
            "disposable Greenfield repository",
            "brownfield repository with neither Factory nor BMAD",
            "brownfield repository with BMAD already present and Factory absent",
            "verify_factory_bmad_cli_rollout.py",
            "/factory-bmad:doctor",
            "Factory Greenfield",
            "/factory-bmad:bootstrap",
            "/factory-bmad:audit",
            "/factory-bmad:intake",
            "/factory-bmad:promote",
            "/factory:run",
            "PLANNING_ONLY",
            "promoted snapshot ID",
            "aggregate hash",
            "Do not cite `_bmad-output/` directly",
            "Stop after the final Factory pack and `pack-lint`",
        ):
            self.assertIn(required, handoff)

    def test_bmad_guidance_explains_reload_discovery_and_denial(self):
        quick_start = (REPO_ROOT / "docs/adapters/bmad/FACTORY_BMAD_QUICK_START.md").read_text(
            encoding="utf-8"
        )
        bootstrap = (REPO_ROOT / "plugin-src/factory-bmad/skills/bootstrap/SKILL.md").read_text(
            encoding="utf-8"
        )
        for text in (quick_start, bootstrap):
            self.assertIn("fresh Claude Code session", " ".join(text.split()))
        normalized_quick_start = " ".join(quick_start.split())
        for phrase in (
            "autocomplete suggestion is not an invocation",
            "Doctor was not run",
            "/factory-bmad:doctor",
        ):
            self.assertIn(phrase, normalized_quick_start)


if __name__ == "__main__":
    unittest.main()
