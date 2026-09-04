#!/usr/bin/env bash
set -euo pipefail

CLAUDE_BIN="${CONDUCTOR_CLAUDE_BIN:?CONDUCTOR_CLAUDE_BIN is required}"
LIVE_ROOT="${CONDUCTOR_BMAD_LIVE_ROOT:?CONDUCTOR_BMAD_LIVE_ROOT is required}"
CONFIG="${CONDUCTOR_BMAD_LIVE_CONFIG_DIR:?CONDUCTOR_BMAD_LIVE_CONFIG_DIR is required}"
PREFLIGHT="${CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE:?CONDUCTOR_BMAD_PREFLIGHT_EVIDENCE is required}"
PREFLIGHT_SHA="${CONDUCTOR_BMAD_PREFLIGHT_SHA256:?CONDUCTOR_BMAD_PREFLIGHT_SHA256 is required}"
RELEASE_VERSION="${CONDUCTOR_RELEASE_VERSION:?CONDUCTOR_RELEASE_VERSION is required}"
CANDIDATE_ROOT="${CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT:?CONDUCTOR_BMAD_LIVE_CANDIDATE_ROOT is required}"
EVIDENCE_ROOT="${CONDUCTOR_BMAD_LIVE_EVIDENCE_ROOT:?CONDUCTOR_BMAD_LIVE_EVIDENCE_ROOT is required}"
PERMISSION_RULE="${CONDUCTOR_BMAD_PERMISSION_RULE:?CONDUCTOR_BMAD_PERMISSION_RULE is required}"
PYTHON_LAUNCHER="${CONDUCTOR_PYTHON_LAUNCHER:-$PWD/scripts/conductor-python}"

if [[ ! -x "$CLAUDE_BIN" || ! -x "$PYTHON_LAUNCHER" ]]; then
  echo "BLOCKED: explicit Claude or Factory Python launcher is invalid" >&2
  exit 2
fi
if [[ -e "$LIVE_ROOT" || -L "$LIVE_ROOT" ]]; then
  echo "BLOCKED: CONDUCTOR_BMAD_LIVE_ROOT must be absent" >&2
  exit 2
fi

export CLAUDE_CONFIG_DIR="$CONFIG"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
export DISABLE_TELEMETRY=1

"$PYTHON_LAUNCHER" scripts/verify_conductor_bmad_live_preflight.py \
  --verify-verdict "$PREFLIGHT" \
  --expected-verdict-sha256 "$PREFLIGHT_SHA" \
  --expected-claude-bin "$CLAUDE_BIN" \
  --expected-config-root "$CONFIG" \
  --expected-evidence-root "$EVIDENCE_ROOT" \
  --expected-candidate-root "$CANDIDATE_ROOT" \
  --expected-live-root "$LIVE_ROOT" \
  --expected-permission-rule "$PERMISSION_RULE" \
  --expected-release-version "$RELEASE_VERSION"

"$CLAUDE_BIN" --version
PLUGIN_VALIDATION="$($CLAUDE_BIN plugin validate --strict "$CANDIDATE_ROOT/plugins/conductor-bmad-claude")"
MARKET_VALIDATION="$($CLAUDE_BIN plugin validate --strict "$CANDIDATE_ROOT/.claude-plugin/marketplace.json")"
printf '%s\n' "$PLUGIN_VALIDATION" | sed "s|$PWD|<repo>|g"
printf '%s\n' "$MARKET_VALIDATION" | sed "s|$PWD|<repo>|g"

MARKET="$LIVE_ROOT/marketplace"
PROJECT="$LIVE_ROOT/project"
mkdir -p "$MARKET/plugins" "$CONFIG" "$PROJECT"
cp -R "$CANDIDATE_ROOT/plugins/conductor-claude" "$MARKET/plugins/conductor-claude"
cp -R "$CANDIDATE_ROOT/plugins/conductor-bmad-claude" "$MARKET/plugins/conductor-bmad-claude"
cp -R "$CANDIDATE_ROOT/.claude-plugin" "$MARKET/.claude-plugin"
git -C "$MARKET" init -q
git -C "$MARKET" add .
git -C "$MARKET" -c user.name='Factory Verification' -c user.email='factory@example.invalid' commit -qm 'isolated marketplace'
git -C "$MARKET" tag "factory--v$RELEASE_VERSION"
git -C "$MARKET" tag "conductor-bmad--v$RELEASE_VERSION"
git -C "$PROJECT" init -q

"$CLAUDE_BIN" plugin marketplace add "$MARKET"
"$CLAUDE_BIN" plugin install conductor-bmad@factory-starter-kit
LIST="$($CLAUDE_BIN plugin list --json)"
"$PYTHON_LAUNCHER" - "$LIST" <<'PY'
import json, sys
items = json.loads(sys.argv[1])
names = {str(item.get("id") or item.get("name")): item for item in items}
factory = next(item for name, item in names.items() if name.startswith("factory@"))
companion = next(item for name, item in names.items() if name.startswith("conductor-bmad@"))
assert factory.get("enabled") is True, factory
assert companion.get("enabled") is True, companion
assert not factory.get("errors"), factory
assert not companion.get("errors"), companion
print("Factory dependency composition: PASS")
PY

if DISABLE_OUTPUT="$($CLAUDE_BIN plugin disable conductor@factory-starter-kit 2>&1)"; then
  echo "BLOCKED: Claude allowed a required Factory dependency to be disabled" >&2
  exit 2
fi
grep -q 'still required by conductor-bmad' <<<"$DISABLE_OUTPUT"
echo "Required dependency cannot be disabled independently: PASS"
