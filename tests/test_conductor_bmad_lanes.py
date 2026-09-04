"""BMAD lane model (migration steps 6-7): lane parity with the JSON contract, complete coverage
of known skills, the invoked-skill rule (AC-L2), the declared root (AC-L3), the unsafe-layout
narrowing (AC-L4), and the TEA split (AC-L5)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tests.test_conductor_bmad_support import REPO_ROOT, runtime, seed_bmad, seed_factory, seed_git

LANE_POLICY = REPO_ROOT / "docs/adapters/bmad/lane_policy.json"
LANE_TEMPLATE = REPO_ROOT / "docs/adapters/bmad/templates/lane_policy.template.json"


def skill(root: Path, name: str) -> dict | None:
    return runtime.hook_decision(root, {"hook_event_name": "PreToolUse", "tool_name": "Skill", "tool_input": {"skill": name}})


def prompt(root: Path, name: str) -> dict | None:
    return runtime.hook_decision(root, {"hook_event_name": "UserPromptExpansion", "cwd": str(root), "expansion_type": "slash_command", "command_name": name})


def is_allowed(decision: dict | None) -> bool:
    if decision is None:
        return True
    specific = decision.get("hookSpecificOutput", {})
    return decision.get("decision") != "block" and specific.get("permissionDecision") != "deny"


class LanePolicyParityTests(unittest.TestCase):
    def test_published_lane_policy_equals_template_and_code(self) -> None:
        published = json.loads(LANE_POLICY.read_text(encoding="utf-8"))
        template = json.loads(LANE_TEMPLATE.read_text(encoding="utf-8"))
        self.assertEqual(published, template)
        self.assertEqual(published["policy_version"], runtime.policy.POLICY_VERSION)
        self.assertEqual(published["bmad_version"], runtime.policy.SUPPORTED_BMAD_VERSION)
        self.assertEqual(set(published["lanes"]["product_context"]["workflows"]), set(runtime.policy.PRODUCT_CONTEXT_WORKFLOWS))
        self.assertEqual(set(published["lanes"]["delivery"]["workflows"]), set(runtime.policy.DELIVERY_WORKFLOWS))
        self.assertEqual(set(published["helpers"]), set(runtime.policy.HELPER_WORKFLOWS))
        self.assertEqual(set(published["evidence_only"]), set(runtime.policy.EVIDENCE_ONLY_WORKFLOWS))
        self.assertEqual(tuple(published["lanes"]["product_context"]["write_roots"]), runtime.policy.PRODUCT_CONTEXT_WRITE_ROOTS)
        self.assertEqual(set(published["unsafe_layout_blocks"]), set(runtime.policy.UNSAFE_LAYOUT_BLOCKS))
        self.assertEqual(published["profiles"], runtime.policy.SOLUTION_CONTEXT_CAPABILITY_PROFILES)

    def test_lanes_are_disjoint_and_cover_every_known_skill(self) -> None:
        p = runtime.policy
        sets = [p.PRODUCT_CONTEXT_WORKFLOWS, p.HELPER_WORKFLOWS, p.EVIDENCE_ONLY_WORKFLOWS, p.NEUTRAL_TOOLING_WORKFLOWS, p.DELIVERY_WORKFLOWS]
        union: set[str] = set()
        for s in sets:
            self.assertFalse(union & s, f"lane overlap: {sorted(union & s)}")
            union |= s
        known = set(p.SUPPORTED_BMAD_SKILLS) | set(p.SUPPORTED_TEA_SKILLS)
        self.assertFalse(known - union, f"known skills without a lane: {sorted(known - union)}")
        self.assertEqual(runtime.policy_classify("bmad-something-new")["classification"], "UNRECOGNIZED_BLOCKING")


class InvokedSkillRuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        seed_git(self.root); seed_factory(self.root); seed_bmad(self.root, capabilities=True)

    def test_ac_l2_party_mode_is_allowed_but_cannot_reach_delivery(self) -> None:
        party = skill(self.root, "bmad-party-mode")
        self.assertTrue(is_allowed(party))
        self.assertIn("party mode", party["hookSpecificOutput"]["additionalContext"])
        for nested in ("bmad-review-adversarial-general", "bmad-advanced-elicitation", "bmad-editorial-review-prose"):
            self.assertTrue(is_allowed(skill(self.root, nested)), nested)
        for delivery in ("bmad-dev-story", "bmad-quick-dev", "bmad-sprint-planning", "bmad-code-review", "bmad-testarch-automate"):
            decision = skill(self.root, delivery)
            self.assertFalse(is_allowed(decision), delivery)
            self.assertIn("is delivery for Conductor-bound work", decision["hookSpecificOutput"]["permissionDecisionReason"])

    def test_ac_l1_prd_finalization_helpers_pass_under_the_hook(self) -> None:
        for name in ("bmad-prd", "bmad-validate-prd", "bmad-review-adversarial-general", "bmad-review-edge-case-hunter", "bmad-advanced-elicitation"):
            self.assertTrue(is_allowed(prompt(self.root, name)), name)

    def test_ac_l5_tea_design_allowed_automation_denied(self) -> None:
        for name in ("bmad-testarch-test-design", "bmad-testarch-nfr", "bmad-testarch-trace"):
            self.assertTrue(is_allowed(skill(self.root, name)), name)
        for name in ("bmad-testarch-automate", "bmad-testarch-ci", "bmad-testarch-atdd", "bmad-tea"):
            self.assertFalse(is_allowed(skill(self.root, name)), name)

    def test_neutral_tooling_passes_without_context(self) -> None:
        self.assertIsNone(skill(self.root, "bmad-customize"))


class DeclaredRootTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        seed_git(self.root); seed_factory(self.root)

    def declare(self, declared_root: str) -> None:
        config = self.root / "docs/Conductor/PROJECT_CONFIG.json"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(json.dumps({
            "schema_version": 1, "product_name": "Conductor", "protected_roots": ["scripts"], "allowed_harnesses": ["claude-code"],
            "default_budget": {"model": "m", "effort_g2": "high", "effort_g3": "high"}, "agents_md": {"mode": "managed_block"},
            "required_docs": [], "recall": {"trigger": "when_index_nonempty"},
            "adapters": {"bmad": {"declared_root": declared_root, "legacy_evidence_root": "docs/adapters/bmad/legacy-evidence"}},
        }), encoding="utf-8")

    def test_ac_l3_declared_non_root_installation_is_canonical(self) -> None:
        self.declare("tools/bmad/_bmad")
        seed_bmad(self.root / "tools" / "bmad", capabilities=False)
        layout = runtime.policy.assess_bmad_layout(self.root)
        self.assertEqual((layout["state"], layout["safe"], layout["declared_root"]), ("canonical_root", True, "tools/bmad/_bmad"), layout)
        self.assertEqual(layout["canonical_manifest"], "tools/bmad/_bmad/_config/manifest.yaml")
        self.assertEqual(runtime.policy.enforcement_activation(self.root)["reason_code"], "CONDUCTOR_BMAD_ENFORCEMENT_ACTIVE")
        self.assertTrue(is_allowed(prompt(self.root, "bmad-product-brief")))
        self.assertFalse(is_allowed(prompt(self.root, "bmad-dev-story")))

    def test_declared_root_plus_canonical_root_is_multiple_roots(self) -> None:
        self.declare("tools/bmad/_bmad")
        seed_bmad(self.root / "tools" / "bmad")
        seed_bmad(self.root)
        layout = runtime.policy.assess_bmad_layout(self.root)
        self.assertFalse(layout["safe"])
        self.assertEqual(layout["reason_code"], "CONDUCTOR_BMAD_MULTIPLE_ACTIVE_ROOTS")

    def test_invalid_declarations_fall_back_to_default_root(self) -> None:
        for bad in ("/abs/_bmad", "../_bmad", "docs/x/_bmad", "tools/bmadcore"):
            self.declare(bad)
            self.assertEqual(runtime.policy.active_bmad_root(self.root), Path("_bmad"), bad)

    def test_ac_l4_nested_layout_blocks_only_authority_actions(self) -> None:
        # no declaration: the nested tree is unsafe; discovery continues with a warning, authority actions block
        seed_bmad(self.root / "bmad")
        layout = runtime.policy.assess_bmad_layout(self.root)
        self.assertEqual(layout["state"], "nested_active")
        discovery = prompt(self.root, "bmad-product-brief")
        self.assertTrue(is_allowed(discovery))
        self.assertIn("LAYOUT WARNING", discovery["hookSpecificOutput"]["additionalContext"])
        self.assertFalse(is_allowed(prompt(self.root, "bmad-architecture")))
        # declaring that same tree makes it the canonical root
        self.declare("bmad/_bmad")
        self.assertEqual(runtime.policy.assess_bmad_layout(self.root)["state"], "canonical_root")
        self.assertNotIn("LAYOUT WARNING", prompt(self.root, "bmad-product-brief")["hookSpecificOutput"]["additionalContext"])


if __name__ == "__main__":
    unittest.main()
