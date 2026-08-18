import tempfile
import unittest
from pathlib import Path

from tests.test_factory_bmad_support import runtime, seed_bmad, seed_factory, seed_git


class FactoryBmadActivationTests(unittest.TestCase):
    def root(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def test_five_states_keep_one_route(self):
        roots = [self.root() for _ in range(5)]
        (roots[1] / "app.py").write_text("pass\n", encoding="utf-8")
        seed_factory(roots[2])
        seed_bmad(roots[3])
        seed_factory(roots[4]); seed_bmad(roots[4])
        expected = ["NEITHER_GREENFIELD", "NEITHER_BROWNFIELD", "FACTORY_ONLY", "BMAD_ONLY", "BOTH_PRESENT"]
        for root, state in zip(roots, expected):
            payload = runtime.doctor(root, "claude")
            self.assertEqual(state, payload["state"])
            self.assertTrue(payload["next_legal_action"])

    def test_bmad_only_routes_factory_brownfield_as_first_mutation(self):
        root = self.root(); seed_git(root); seed_bmad(root)
        payload = runtime.doctor(root, "claude")
        self.assertEqual("BMAD_ONLY", payload["state"])
        self.assertEqual("run_factory_brownfield_preview", payload["next_legal_action"])
        self.assertFalse(runtime.enforcement_activation(root)["active"])

    def test_guard_requires_git_factory_and_bmad_coexistence(self):
        no_git = self.root(); seed_factory(no_git); seed_bmad(no_git)
        self.assertFalse(runtime.enforcement_activation(no_git)["active"])
        active = self.root(); seed_git(active); seed_factory(active); seed_bmad(active)
        self.assertTrue(runtime.enforcement_activation(active)["active"])
        self.assertEqual("FACTORY_BMAD_ENFORCEMENT_ACTIVE", runtime.enforcement_activation(active)["reason_code"])

    def test_partial_bmad_beside_factory_activates_fail_closed(self):
        root = self.root(); seed_git(root); seed_factory(root); (root / "_bmad").mkdir()
        activation = runtime.enforcement_activation(root)
        self.assertTrue(activation["active"])
        self.assertEqual("FACTORY_BMAD_ENFORCEMENT_ACTIVE_PARTIAL", activation["reason_code"])


if __name__ == "__main__":
    unittest.main()
