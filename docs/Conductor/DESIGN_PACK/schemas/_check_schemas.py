"""Design-pack self-check: every schema parses, passes the 2020-12 metaschema when
jsonschema is available, and the Statement of Completion schema accepts a minimal
valid document while rejecting two negative fixtures. Run from the repo root:

    python3 docs/Conductor/DESIGN_PACK/schemas/_check_schemas.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

try:
    from jsonschema import Draft202012Validator as V
    HAVE = True
except ImportError:  # pragma: no cover - environment dependent
    HAVE = False


def main() -> int:
    ok = True
    for path in sorted(glob.glob(os.path.join(HERE, "*.schema.json"))):
        try:
            schema = json.load(open(path, encoding="utf-8"))
            if HAVE:
                V.check_schema(schema)
            print("OK  ", os.path.basename(path), "(metaschema)" if HAVE else "(json only)")
        except Exception as exc:  # noqa: BLE001 - report every failure
            ok = False
            print("FAIL", os.path.basename(path), exc)
    if not HAVE:
        print("jsonschema not installed; metaschema and fixture checks skipped")
        return 0 if ok else 1

    soc = json.load(open(os.path.join(HERE, "statement_of_completion.schema.json"), encoding="utf-8"))
    good = {
        "schema_version": 1,
        "run_id": "RUN_1",
        "intent_pack_sha256": "a" * 64,
        "rows": [{
            "requirement_id": "R-1",
            "status": "verified",
            "evidence": [{"check_id": "VM-1", "receipt_path": "receipts/VM-1.json", "receipt_sha256": "b" * 64}],
        }],
        "verifier": {"report_path": "notes/v.md", "report_sha256": "c" * 64, "fresh_context": True},
        "derived_state": "READY",
        "handoff_state": "REVIEW_READY",
    }
    V(soc).validate(good)
    print("SoC positive fixture: PASS")
    bad1 = json.loads(json.dumps(good))
    bad1["rows"][0]["evidence"] = []
    bad2 = json.loads(json.dumps(good))
    bad2["rows"][0]["status"] = "out_of_scope"
    for name, doc in (("verified without evidence", bad1), ("out_of_scope without decision_ref", bad2)):
        rejected = bool(list(V(soc).iter_errors(doc)))
        print(f"SoC negative '{name}': {'rejected' if rejected else 'NOT rejected'}")
        ok = ok and rejected
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
