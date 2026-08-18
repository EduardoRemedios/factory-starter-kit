#!/usr/bin/env bash
set -euo pipefail

ROOT="${FACTORY_BMAD_VM011_ROOT:-}"
APPROVAL="${FACTORY_BMAD_VM011_APPROVED_PLAN_ID:-}"
RUNTIME="plugins/factory-bmad-claude/scripts/factory_bmad.py"
if [[ -z "$ROOT" || ! -d "$ROOT" ]]; then
  echo "BLOCKED: set FACTORY_BMAD_VM011_ROOT to the prepared disposable repository" >&2
  exit 2
fi
if [[ -z "$APPROVAL" ]]; then
  echo "BLOCKED: set FACTORY_BMAD_VM011_APPROVED_PLAN_ID to the exact human-approved bootstrap plan" >&2
  exit 2
fi

RECEIPT="$ROOT/docs/upstream/bmad/install-receipts/$APPROVAL.json"
if [[ -s "$RECEIPT" ]]; then
  python3 - "$RECEIPT" "$APPROVAL" <<'PY'
import json, sys
from pathlib import Path

receipt = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert receipt.get("schema_version") == 1, receipt
assert receipt.get("operation") == "bootstrap", receipt
assert receipt.get("plan_id") == sys.argv[2], receipt
assert receipt.get("outcome") == "APPLIED", receipt
assert receipt.get("return_code") == 0, receipt
assert receipt.get("unexpected_paths") == [], receipt
assert receipt.get("audit", {}).get("state") == "READY", receipt
print("Existing exact-plan bootstrap receipt: PASS")
PY
else
  python3 "$RUNTIME" --root "$ROOT" --json bootstrap --harness claude --approve-plan "$APPROVAL"
fi
python3 "$RUNTIME" --root "$ROOT" --json audit --harness claude

MANIFEST="$ROOT/_bmad/_config/manifest.yaml"
test -s "$MANIFEST"
test -s "$ROOT/docs/Factory/ARCHITECTURE.md"
test -x "$ROOT/scripts/factoryctl"
test -d "$ROOT/.git"
grep -q 'name: core' "$MANIFEST"
grep -q 'name: bmm' "$MANIFEST"
if grep -Eq 'name: (bmad-loop|tea)' "$MANIFEST"; then
  echo "BLOCKED: excluded module present after live installation" >&2
  exit 2
fi
if find "$ROOT/_bmad" "$ROOT/.claude/skills" -type l -print -quit | grep -q .; then
  echo "BLOCKED: symlink found in installed BMAD state" >&2
  exit 2
fi
echo "Pinned BMAD 6.10.0 Core+BMM installation and companion audit: PASS"
