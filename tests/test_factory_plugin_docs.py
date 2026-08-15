import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / "docs/onboarding"
REQUIRED_DOCS = {
    "FACTORY_FIRST_TESTER_HANDOFF.md",
    "FACTORY_PLUGIN_CLI_ROLLOUT_PLAYBOOK.md",
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
        onboarding = (DOCS_ROOT / "ONBOARDING_GUIDE.md").read_text(encoding="utf-8")
        self.assertIn("FACTORY_PLUGIN_QUICK_START.md", onboarding)
        readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("FACTORY_FIRST_TESTER_HANDOFF.md", readme)
        self.assertIn("factory-plugin-v0.2.3-rc.1", readme)

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
        self.assertIn("verify_factory_cli_rollout.py", pilot)

    def test_cli_rollout_preflight_is_documented(self):
        quick_start = (DOCS_ROOT / "FACTORY_PLUGIN_QUICK_START.md").read_text(
            encoding="utf-8"
        )
        playbook = (DOCS_ROOT / "FACTORY_PLUGIN_CLI_ROLLOUT_PLAYBOOK.md").read_text(
            encoding="utf-8"
        )
        handoff = (DOCS_ROOT / "FACTORY_FIRST_TESTER_HANDOFF.md").read_text(
            encoding="utf-8"
        )
        for text in (quick_start, playbook):
            self.assertIn("verify_factory_cli_rollout.py", text)
            self.assertIn("claude plugin --help", text)
        self.assertIn("/factory:greenfield", playbook)
        self.assertIn("/factory:brownfield", playbook)
        self.assertIn("verify_factory_cli_rollout.py", handoff)
        self.assertIn("factory-plugin-v0.2.3-rc.1", handoff)
        self.assertIn("/factory:greenfield", handoff)

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

    def test_validation_guidance_prevents_bytecode_cache_mutation(self):
        validation = (
            REPO_ROOT / "plugin-src/factory/skills/validate.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PYTHONDONTWRITEBYTECODE=1", validation)
        self.assertIn("git status --short", validation)
        self.assertIn("report every difference", validation)

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
        self.assertIn("Factory never", claude_section)
        self.assertIn("requires a fresh preview", claude_section)

    def test_claude_greenfield_troubleshooting_preserves_user_state(self):
        troubleshooting = (
            DOCS_ROOT / "FACTORY_PLUGIN_TROUBLESHOOTING.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "Claude Local Settings Make Greenfield Look Non-empty",
            troubleshooting,
        )
        self.assertIn(
            "does not parse, manage, modify, or remove it", troubleshooting
        )
        self.assertIn("Do not delete user-owned content", troubleshooting)

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

    def test_optional_bmad_routing_matrix_preserves_factory_only_default(self):
        matrix = (REPO_ROOT / "docs/integration/FACTORY_BMAD_ROUTING_MATRIX.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Factory-only adoption remains the default path", matrix)
        self.assertIn("New or empty target | Factory only", matrix)
        self.assertIn("Existing repository, BMAD only | Factory plus BMAD", matrix)
        self.assertIn("Installing `factory` must never require BMAD", matrix)
        self.assertIn("Desktop", matrix)


if __name__ == "__main__":
    unittest.main()
