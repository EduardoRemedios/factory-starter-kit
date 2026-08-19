import tempfile
import unittest
from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from tests.test_factory_bmad_support import runtime, seed_bmad, seed_factory


class FactoryBmadBootstrapTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def test_five_state_routing(self):
        green = self.root()
        self.assertEqual("NEITHER_GREENFIELD", runtime.doctor(green, "claude")["state"])
        brown = self.root()
        (brown / "app.py").write_text("pass\n", encoding="utf-8")
        self.assertEqual("NEITHER_BROWNFIELD", runtime.doctor(brown, "claude")["state"])
        factory = self.root(); seed_factory(factory)
        self.assertEqual("FACTORY_ONLY", runtime.doctor(factory, "claude")["state"])
        bmad = self.root(); seed_bmad(bmad)
        self.assertEqual("BMAD_ONLY", runtime.doctor(bmad, "claude")["state"])
        both = self.root(); seed_factory(both); seed_bmad(both)
        self.assertEqual("BOTH_PRESENT", runtime.doctor(both, "claude")["state"])

    def test_claude_metadata_only_is_greenfield(self):
        root = self.root()
        (root / ".claude").mkdir()
        (root / ".claude/settings.local.json").write_text("{}\n", encoding="utf-8")
        self.assertEqual("NEITHER_GREENFIELD", runtime.doctor(root, "claude")["state"])

    def test_partial_state_blocks(self):
        root = self.root(); (root / "_bmad").mkdir()
        payload = runtime.doctor(root, "claude")
        self.assertEqual("BLOCKED", payload["state"])
        self.assertEqual("FACTORY_BMAD_PARTIAL_STATE", payload["reason_code"])

    def test_preview_is_zero_write_and_exactly_pinned(self):
        root = self.root(); seed_factory(root)
        before = runtime.tree_inventory(root)
        payload = runtime.bootstrap(root, "claude", None)
        self.assertEqual("PLAN_READY", payload["state"])
        self.assertEqual(before, runtime.tree_inventory(root))
        command = payload["plan"]["command"]
        self.assertIn("bmad-method@6.10.0", command)
        self.assertEqual(["core", "bmm"], payload["plan"]["modules"])
        self.assertEqual(["bmad-loop", "tea"], payload["plan"]["excluded_modules"])
        self.assertNotIn(".claude/settings.local.json", payload["plan"]["allowed_prefixes"])

    def test_wrong_approval_never_executes(self):
        root = self.root(); seed_factory(root)
        before = runtime.tree_inventory(root)
        payload = runtime.bootstrap(root, "claude", "wrong")
        self.assertEqual("FACTORY_BMAD_PLAN_APPROVAL_MISMATCH", payload["reason_code"])
        self.assertEqual(before, runtime.tree_inventory(root))

    def test_claude_hook_state_does_not_stale_bootstrap_plan(self):
        root = self.root(); seed_factory(root)
        preview = runtime.bootstrap(root, "claude", None)
        (root / ".claude/hooks/.state").mkdir(parents=True)
        (root / ".claude/hooks/.state/hook-errors.log").write_text(
            "harness state\n", encoding="utf-8"
        )
        current = runtime.bootstrap(root, "claude", None)
        self.assertEqual(preview["plan"]["plan_id"], current["plan"]["plan_id"])

        def fake_installer(*_args, **_kwargs):
            seed_bmad(root, capabilities=True)
            return CompletedProcess([], 0, "installed", "")

        with patch.object(runtime.subprocess, "run", side_effect=fake_installer):
            payload = runtime.bootstrap(root, "claude", preview["plan"]["plan_id"])
        self.assertEqual("FACTORY_BMAD_BOOTSTRAP_APPLIED", payload["reason_code"])

    def test_inventory_records_empty_directories_and_symlinks_without_following(self):
        root = self.root()
        (root / "empty").mkdir()
        outside = root.parent / f"{root.name}-outside"
        outside.write_text("do not read\n", encoding="utf-8")
        self.addCleanup(lambda: outside.unlink(missing_ok=True))
        (root / "link").symlink_to(outside)
        inventory = runtime.tree_inventory(root)
        self.assertEqual("directory", inventory["empty"])
        self.assertEqual(f"symlink:{outside}", inventory["link"])
        self.assertNotIn(runtime.digest_file(outside), inventory["link"])

    def test_post_audit_blocks_unexpected_empty_directory(self):
        root = self.root(); seed_factory(root)
        preview = runtime.bootstrap(root, "claude", None)

        def fake_installer(*_args, **_kwargs):
            seed_bmad(root)
            (root / "unexpected-empty").mkdir()
            return CompletedProcess([], 0, "installed", "")

        with patch.object(runtime.subprocess, "run", side_effect=fake_installer):
            payload = runtime.bootstrap(root, "claude", preview["plan"]["plan_id"])
        self.assertEqual("FACTORY_BMAD_BOOTSTRAP_POST_AUDIT_FAILED", payload["reason_code"])
        self.assertEqual(["unexpected-empty"], payload["unexpected_paths"])

    def test_claude_container_is_allowed_but_settings_are_not(self):
        root = self.root(); seed_factory(root)
        preview = runtime.bootstrap(root, "claude", None)
        self.assertEqual([".claude"], preview["plan"]["allowed_container_paths"])

        def fake_installer(*_args, **_kwargs):
            seed_bmad(root, capabilities=True)
            (root / ".claude/settings.json").write_text("{}\n", encoding="utf-8")
            return CompletedProcess([], 0, "installed", "")

        with patch.object(runtime.subprocess, "run", side_effect=fake_installer):
            payload = runtime.bootstrap(root, "claude", preview["plan"]["plan_id"])
        self.assertEqual("FACTORY_BMAD_BOOTSTRAP_POST_AUDIT_FAILED", payload["reason_code"])
        self.assertIn(".claude/settings.json", payload["unexpected_paths"])
        self.assertNotIn(".claude", payload["unexpected_paths"])


if __name__ == "__main__":
    unittest.main()
