"""Conductor contract schemas (migration step 2b).

Asserts, for every schema under docs/Conductor/contracts/ (core) and
docs/adapters/bmad/contracts/ (BMAD adapter):
  * it is a valid JSON Schema 2020-12 document;
  * its template validates;
  * a set of negative fixtures (mutations of the template) is rejected.
Also proves the v2 verification manifest is a superset of Factory v1 by
validating the two golden-pack manifests against it after bumping only the
schema_version field, and that the core contracts directory stays
domain-neutral (adapter-specific contracts live with their adapter).
"""
from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

REPO_ROOT = Path(__file__).resolve().parents[1]
CORE_CONTRACTS = REPO_ROOT / "docs" / "Conductor" / "contracts"
CORE_TEMPLATES = REPO_ROOT / "docs" / "Conductor" / "templates"
BMAD_CONTRACTS = REPO_ROOT / "docs" / "adapters" / "bmad" / "contracts"
BMAD_TEMPLATES = REPO_ROOT / "docs" / "adapters" / "bmad" / "templates"
GOLDEN = REPO_ROOT / "tests" / "golden_packs"

# schema name -> (contracts dir, templates dir, template file)
LOCATIONS: dict[str, tuple[Path, Path, str]] = {
    "intent_pack": (CORE_CONTRACTS, CORE_TEMPLATES, "intent_pack.template.json"),
    "statement_of_completion": (CORE_CONTRACTS, CORE_TEMPLATES, "statement_of_completion.template.json"),
    "gap_request": (CORE_CONTRACTS, CORE_TEMPLATES, "gap_request.template.json"),
    "project_config": (CORE_CONTRACTS, CORE_TEMPLATES, "project_config.template.json"),
    "countersign": (CORE_CONTRACTS, CORE_TEMPLATES, "countersign.template.json"),
    "evidence_receipt": (CORE_CONTRACTS, CORE_TEMPLATES, "evidence_receipt.example.json"),
    "verification_manifest_v2": (CORE_CONTRACTS, CORE_TEMPLATES, "VERIFICATION_MANIFEST_TEMPLATE_V2.yaml"),
    "lane_policy": (BMAD_CONTRACTS, BMAD_TEMPLATES, "lane_policy.template.json"),
    "bmad_adapter_config": (BMAD_CONTRACTS, BMAD_TEMPLATES, "bmad_adapter_config.template.json"),
}
CORE_NEUTRALITY = re.compile(r"Symphony|AuditEdge|BMAD|\bTEA\b", re.IGNORECASE)


def load(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    return json.loads(text)


def schema(name: str) -> dict[str, Any]:
    return load(LOCATIONS[name][0] / f"{name}.schema.json")


def template(name: str) -> Any:
    _, templates, filename = LOCATIONS[name]
    return load(templates / filename)


def errors(name: str, document: Any) -> list[str]:
    return [e.message for e in Draft202012Validator(schema(name), format_checker=FormatChecker()).iter_errors(document)]


def mutate(document: Any, fn) -> Any:
    clone = copy.deepcopy(document)
    fn(clone)
    return clone


class SchemaFilesTests(unittest.TestCase):
    def test_every_schema_file_is_mapped_and_valid_2020_12(self) -> None:
        on_disk = sorted(
            p.name.removesuffix(".schema.json")
            for d in (CORE_CONTRACTS, BMAD_CONTRACTS)
            for p in d.glob("*.schema.json")
        )
        self.assertEqual(on_disk, sorted(LOCATIONS), "every schema file must be in LOCATIONS and vice versa")
        for name in on_disk:
            with self.subTest(schema=name):
                Draft202012Validator.check_schema(schema(name))

    def test_every_template_validates_against_its_schema(self) -> None:
        for name in LOCATIONS:
            with self.subTest(schema=name):
                self.assertEqual(errors(name, template(name)), [])

    def test_core_contracts_and_templates_are_domain_neutral(self) -> None:
        for path in list(CORE_CONTRACTS.iterdir()) + [
            CORE_TEMPLATES / filename for (d, _, filename) in LOCATIONS.values() if d == CORE_CONTRACTS
        ]:
            with self.subTest(file=path.relative_to(REPO_ROOT).as_posix()):
                self.assertIsNone(CORE_NEUTRALITY.search(path.read_text(encoding="utf-8")))

    def test_templates_carry_no_placeholder_digests_except_zero(self) -> None:
        # Templates use an all-zero digest as the obvious placeholder; anything else looks like a real pin.
        for name in LOCATIONS:
            text = json.dumps(template(name))
            for digest in re.findall(r"[a-f0-9]{64}", text):
                if name in {"lane_policy"}:  # pinned BMAD 6.10.0 profiles are real by design
                    continue
                with self.subTest(schema=name, digest=digest[:8]):
                    self.assertEqual(digest, "0" * 64)


class NegativeFixtureTests(unittest.TestCase):
    """Each fixture removes or corrupts one thing the schema must catch."""

    def assert_rejected(self, name: str, document: Any, why: str) -> None:
        self.assertTrue(errors(name, document), f"{name}: expected rejection: {why}")

    def run_cases(self, name: str, cases: dict[str, Any]) -> None:
        base = template(name)
        for why, fn in cases.items():
            with self.subTest(case=why):
                self.assert_rejected(name, mutate(base, fn), why)

    def test_intent_pack(self) -> None:
        self.run_cases("intent_pack", {
            "placeholder goal": lambda d: d.__setitem__("goal", "TBD"),
            "no requirements": lambda d: d.__setitem__("requirements", []),
            "bad severity": lambda d: d["requirements"][0].__setitem__("severity", "urgent"),
            "budget without model": lambda d: d["budget"].pop("model"),
            "unknown effort": lambda d: d["budget"].__setitem__("effort_g2", "ultra"),
            "bad source digest": lambda d: d["sources"][0].__setitem__("sha256", "abc"),
            "extra field": lambda d: d.__setitem__("stage", "A"),
            "empty scope_in": lambda d: d.__setitem__("scope_in", []),
        })

    def test_statement_of_completion(self) -> None:
        self.run_cases("statement_of_completion", {
            "verified without evidence": lambda d: d["rows"][0].__setitem__("evidence", []),
            "out_of_scope without decision_ref": lambda d: d["rows"][1].pop("decision_ref"),
            "unknown status": lambda d: d["rows"][0].__setitem__("status", "done"),
            "verifier not fresh": lambda d: d["verifier"].__setitem__("fresh_context", False),
            "authored derived_state value": lambda d: d.__setitem__("derived_state", "APPROVED"),
            "merge_ready without preflight summary": lambda d: d.__setitem__("handoff_state", "MERGE_READY"),
            "absolute receipt path": lambda d: d["rows"][0]["evidence"][0].__setitem__("receipt_path", "/etc/passwd"),
            "path traversal": lambda d: d["rows"][0]["evidence"][0].__setitem__("receipt_path", "../x.json"),
        })

    def test_gap_request(self) -> None:
        self.run_cases("gap_request", {
            "snapshot id without digest": lambda d: d.pop("origin_snapshot_sha256"),
            "unknown gap type": lambda d: d.__setitem__("gap_type", "budget"),
            "empty question": lambda d: d.__setitem__("question", ""),
            "unknown supersession impact": lambda d: d.__setitem__("supersession_impact", "maybe"),
            "resolution with new snapshot id but no digest": lambda d: d.__setitem__(
                "resolution", {"decided_by": "x", "utc": "2026-01-01T00:00:00Z", "decision": "ok", "new_snapshot_id": "SNAP-2"}
            ),
            "bad resolution timestamp": lambda d: d.__setitem__(
                "resolution", {"decided_by": "x", "utc": "yesterday", "decision": "ok"}
            ),
        })

    def test_project_config(self) -> None:
        self.run_cases("project_config", {
            "unknown harness": lambda d: d["allowed_harnesses"].append("vscode-copilot"),
            "no protected roots": lambda d: d.__setitem__("protected_roots", []),
            "preflight timeout over cap": lambda d: d.__setitem__("project_preflight", {"enabled": True, "timeout_seconds": 301}),
            "unknown recall trigger": lambda d: d["recall"].__setitem__("trigger", "sometimes"),
            "adapter key with uppercase": lambda d: d["adapters"].__setitem__("BMAD", {}),
            "adapter value not an object": lambda d: d["adapters"].__setitem__("bmad", "on"),
            "legacy top-level adapter block": lambda d: d.__setitem__("bmad", {"declared_root": "_bmad"}),
            "unknown agents_md mode": lambda d: d["agents_md"].__setitem__("mode", "overwrite"),
        })

    def test_bmad_adapter_config(self) -> None:
        self.run_cases("bmad_adapter_config", {
            "declared root under docs": lambda d: d.__setitem__("declared_root", "docs/bmad/_bmad"),
            "declared root absolute": lambda d: d.__setitem__("declared_root", "/tmp/_bmad"),
            "declared root traversal": lambda d: d.__setitem__("declared_root", "../_bmad"),
            "legacy root moved": lambda d: d.__setitem__("legacy_evidence_root", "docs/upstream/legacy"),
            "extra field": lambda d: d.__setitem__("allow_nested", True),
        })

    def test_lane_policy(self) -> None:
        self.run_cases("lane_policy", {
            "unknown_default allow": lambda d: d.__setitem__("unknown_default", "allow"),
            "discovery in unsafe_layout_blocks": lambda d: d["unsafe_layout_blocks"].append("discovery"),
            "empty unsafe_layout_blocks": lambda d: d.__setitem__("unsafe_layout_blocks", []),
            "non-bmad skill name": lambda d: d["helpers"].append("superpowers-brainstorm"),
            "duplicate helper": lambda d: d["helpers"].append(d["helpers"][0]),
            "profile missing digest": lambda d: d["profiles"]["bmad-spec"].pop("skill_sha256"),
            "bad bmad version": lambda d: d.__setitem__("bmad_version", "6.10"),
            "no write roots": lambda d: d["lanes"]["product_context"].__setitem__("write_roots", []),
        })

    def test_countersign(self) -> None:
        self.run_cases("countersign", {
            "unknown kind": lambda d: d.__setitem__("kind", "MERGE"),
            "unknown decision": lambda d: d.__setitem__("decision", "MAYBE"),
            "empty signer": lambda d: d.__setitem__("signer", ""),
            "bad digest": lambda d: d.__setitem__("subject_sha256", "xyz"),
            "bad timestamp": lambda d: d.__setitem__("utc", "yesterday"),
            "non-UTC timestamp": lambda d: d.__setitem__("utc", "2026-01-01T00:00:00+02:00"),
            "extra field": lambda d: d.__setitem__("approved_by_agent", True),
        })

    def test_evidence_receipt(self) -> None:
        self.run_cases("evidence_receipt", {
            "missing payload digest": lambda d: d.pop("payload_sha256"),
            "string command": lambda d: d.__setitem__("command", "python3 -m unittest"),
            "stdout over cap": lambda d: d.__setitem__("stdout_bytes", 65537),
            "unknown status": lambda d: d.__setitem__("status", "OK"),
            "absolute log path": lambda d: d.__setitem__("stdout_path", "/var/log/x"),
        })

    def test_verification_manifest_v2(self) -> None:
        self.run_cases("verification_manifest_v2", {
            "wrong schema_version": lambda d: d.__setitem__("schema_version", 1),
            "check without requirement or constraint ids": lambda d: d["checks"][0].pop("requirement_ids"),
            "command-type check without command": lambda d: d["checks"][0].pop("command"),
            "no_touch without preimage": lambda d: d["checks"][1].pop("preimage_manifest"),
            "artifact check without target": lambda d: d["checks"].append(
                {"id": "VM-003", "tier": "V1", "type": "artifact", "requirement_ids": ["R-001"],
                 "description": "x", "halt_on_failure": True, "evidence_path": "receipts/VM-003.json"}
            ),
            "result without receipt": lambda d: d["checks"][0].__setitem__("result", {"status": "PASS"}),
            "unknown result status": lambda d: d["checks"][0].__setitem__("result", {"status": "OK", "receipt_path": "receipts/VM-001.json"}),
            "unknown tier": lambda d: d["checks"][0].__setitem__("tier", "V5"),
            "unknown check type": lambda d: d["checks"][0].__setitem__("type", "vibes"),
        })


class V1CompatibilityTests(unittest.TestCase):
    """The v2 manifest schema must accept every qualified Factory v1 manifest once schema_version is bumped."""

    def test_golden_pack_manifests_validate_as_v2(self) -> None:
        manifests = sorted(GOLDEN.glob("*/pack/verification_manifest.yaml"))
        self.assertTrue(manifests, "golden packs must carry verification manifests")
        for path in manifests:
            with self.subTest(manifest=path.relative_to(REPO_ROOT).as_posix()):
                document = load(path)
                self.assertEqual(document["schema_version"], 1)
                document["schema_version"] = 2
                self.assertEqual(errors("verification_manifest_v2", document), [])


if __name__ == "__main__":
    unittest.main()
