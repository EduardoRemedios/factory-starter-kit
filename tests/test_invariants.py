"""Conductor INVARIANTS and AGENTS.md managed block (migration step 3).

* The Hard Guardrails and SIMPLE-CODE-GATE sections in docs/Conductor/INVARIANTS.md
  are byte-identical to the sections in AGENTS.md (the invariants were moved, not
  rewritten).
* AGENTS.md carries exactly one Conductor managed block whose recorded SHA-256
  matches its body, placed directly after the H1.
* INVARIANTS.md ships in the core plugin payload and must therefore stay
  domain-neutral.
"""
from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "AGENTS.md"
INVARIANTS = REPO_ROOT / "docs" / "Conductor" / "INVARIANTS.md"

START_RE = re.compile(r"<!-- conductor:managed:start v=(?P<v>[^ ]+) sha256=(?P<d>[a-f0-9]{64}) -->\n")
END = "<!-- conductor:managed:end -->\n"
NEUTRALITY = re.compile(r"Symphony|AuditEdge|BMAD|\bTEA\b", re.IGNORECASE)


def section(text: str, heading: str) -> str:
    """Return the text of a '## heading' section up to the next '## ' heading (exclusive)."""
    start = text.index(f"\n{heading}\n") + 1
    nxt = text.find("\n## ", start + len(heading))
    return text[start:] if nxt == -1 else text[start : nxt + 1]


class InvariantsTests(unittest.TestCase):
    def test_hard_guardrails_and_simple_code_gate_are_verbatim(self) -> None:
        agents = AGENTS.read_text(encoding="utf-8")
        invariants = INVARIANTS.read_text(encoding="utf-8")
        for heading in ("## 3) Hard Guardrails", "## 3.1) SIMPLE-CODE-GATE (v2)"):
            with self.subTest(section=heading):
                self.assertEqual(section(invariants, heading), section(agents, heading))

    def test_invariants_are_domain_neutral(self) -> None:
        self.assertIsNone(NEUTRALITY.search(INVARIANTS.read_text(encoding="utf-8")))

    def test_invariants_state_the_governing_principle_and_gates(self) -> None:
        text = INVARIANTS.read_text(encoding="utf-8")
        for needle in ("authority, outcomes, and write boundaries", "G1 Intent Lock", "G2 Governed Execution",
                       "G3 Adversarial Review and Completion", "## 2) Autonomy contract", "conductor:managed:start"):
            self.assertIn(needle, text)


class ManagedBlockTests(unittest.TestCase):
    def test_exactly_one_managed_block_with_matching_digest(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        starts = list(START_RE.finditer(text))
        self.assertEqual(len(starts), 1, "AGENTS.md must carry exactly one managed block")
        self.assertEqual(text.count(END), 1)
        m = starts[0]
        end = text.index(END, m.end())
        body = text[m.end() : end]
        self.assertEqual(hashlib.sha256(body.encode("utf-8")).hexdigest(), m.group("d"))

    def test_managed_block_follows_the_h1_and_precedes_project_content(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        first_line, rest = text.split("\n", 1)
        self.assertTrue(first_line.startswith("# "))
        self.assertTrue(rest.lstrip("\n").startswith("<!-- conductor:managed:start"))
        self.assertIn("## 1) Read Order (mandatory)", text.split(END, 1)[1])

    def test_managed_block_names_the_two_file_read_order_and_autonomy_contract(self) -> None:
        text = AGENTS.read_text(encoding="utf-8")
        body = text[START_RE.search(text).end() : text.index(END)]
        for needle in ("`docs/PROJECT_STATE.md`", "`docs/Conductor/INVARIANTS.md`", "Autonomy contract",
                       "do not narrow, widen, or swap it", "audit each claim against a receipt"):
            self.assertIn(needle, body)
        self.assertEqual(
            body[body.index("You are operating under Conductor governance") :].split("\n", 1)[0],
            INVARIANTS.read_text(encoding="utf-8").split("> You are operating under Conductor governance", 1)[1].split("\n", 1)[0].join(
                ["You are operating under Conductor governance", ""]
            ),
            "autonomy contract text must be identical in AGENTS.md and INVARIANTS.md",
        )


if __name__ == "__main__":
    unittest.main()
