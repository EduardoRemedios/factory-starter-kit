from __future__ import annotations

import unittest

from tests.factory_plugin_test_support import (
    KNOWN_CONSTRAINT_IDS,
    REQUIRED_FIXTURE_FAMILIES,
    iter_golden_files,
    load_json,
)


class FactoryPluginGoldenFixtureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_paths = list(iter_golden_files())
        self.fixtures = [(path, load_json(path)) for path in self.fixture_paths]

    def test_required_fixture_families_are_present(self) -> None:
        self.assertEqual(
            {path.parent.name for path in self.fixture_paths},
            REQUIRED_FIXTURE_FAMILIES,
        )

    def test_fixture_and_case_ids_are_unique(self) -> None:
        fixture_ids: set[str] = set()
        case_ids: set[str] = set()
        for path, fixture in self.fixtures:
            fixture_id = fixture.get("fixture_id")
            self.assertIsInstance(fixture_id, str, path)
            self.assertNotIn(fixture_id, fixture_ids, path)
            fixture_ids.add(fixture_id)
            for case in fixture.get("cases", []):
                case_id = case.get("case_id")
                self.assertIsInstance(case_id, str, path)
                self.assertNotIn(case_id, case_ids, path)
                case_ids.add(case_id)

    def test_constraint_references_are_known_and_complete(self) -> None:
        covered: set[str] = set()
        for path, fixture in self.fixtures:
            constraints = fixture.get("constraints")
            self.assertIsInstance(constraints, list, path)
            self.assertTrue(constraints, path)
            self.assertTrue(all(item in KNOWN_CONSTRAINT_IDS for item in constraints), path)
            covered.update(constraints)
        self.assertEqual(covered, KNOWN_CONSTRAINT_IDS)

    def test_halt_and_blocked_cases_have_reason_codes_and_no_mutations(self) -> None:
        for path, fixture in self.fixtures:
            for case in fixture.get("cases", []):
                outcome = case.get("expected_result") or case.get("expected_state")
                if outcome not in {"HALT", "BLOCKED"}:
                    continue
                self.assertRegex(case.get("expected_reason_code", ""), r"^FACTORY_[A-Z0-9_]+$", path)
                self.assertEqual(case.get("mutations"), [], path)

    def test_read_only_status_cases_declare_zero_mutations(self) -> None:
        for path, fixture in self.fixtures:
            if path.parent.name != "status":
                continue
            for case in fixture["cases"]:
                self.assertEqual(case.get("mutations"), [], case["case_id"])

    def test_each_fixture_declares_a_golden_outcome(self) -> None:
        for path, fixture in self.fixtures:
            has_outcome = any(
                key in fixture
                for key in ("expected", "expected_normalized_result", "expected_result_when_threshold_met")
            )
            cases = fixture.get("cases", [])
            case_outcomes = bool(cases) and all(
                "expected_result" in case or "expected_state" in case for case in cases
            )
            self.assertTrue(has_outcome or case_outcomes, path)


if __name__ == "__main__":
    unittest.main()
