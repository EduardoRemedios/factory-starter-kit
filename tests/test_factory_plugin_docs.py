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

    def test_validation_guidance_prevents_bytecode_cache_mutation(self):
        validation = (
            REPO_ROOT / "plugin-src/factory/skills/validate.md"
        ).read_text(encoding="utf-8")
        self.assertIn("PYTHONDONTWRITEBYTECODE=1", validation)
        self.assertIn("git status --short", validation)
        self.assertIn("report every difference", validation)

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


if __name__ == "__main__":
    unittest.main()
