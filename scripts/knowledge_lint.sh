#!/usr/bin/env bash
set -euo pipefail

# Factory Starter Kit — Knowledge Lint Preflight
#
# This script validates that the doc spine required by the Factory pipeline
# is intact before a run starts. Adapt the required_files list to match
# your project's canonical documents.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

fail() {
  echo "knowledge_lint: FAIL - $1" >&2
  exit 1
}

require_nonempty_file() {
  local path="$1"
  [[ -s "$path" ]] || fail "required file missing or empty: $path"
}

has_pattern() {
  local pattern="$1"
  local file="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -q "$pattern" "$file"
  else
    grep -Eq "$pattern" "$file"
  fi
}

echo "knowledge_lint: starting"

# ============================================================
# ADAPT THIS LIST to your project's canonical documents.
# These are the minimum files the Factory pipeline needs
# to be present and non-empty before a run can start.
# ============================================================
required_files=(
  "AGENTS.md"
  "docs/PROJECT_STATE.md"
  "docs/ROADMAP.md"
  "docs/CHANGELOG.md"
  "docs/Factory/ORCHESTRATION.md"
  "docs/Factory/SCRATCHPAD.md"
  "docs/Factory/Spec/STAGE_CONTRACTS.md"
  "docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md"
  "docs/Factory/templates/PACK_CHECKLIST_TEMPLATE.md"
  "docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md"
)

for path in "${required_files[@]}"; do
  require_nonempty_file "$path"
done

# Validate Scratchpad structure
has_pattern '^## Active Pitfalls \(Mandatory\)' docs/Factory/SCRATCHPAD.md \
  || fail "missing mandatory 'Active Pitfalls' section in docs/Factory/SCRATCHPAD.md"

pitfall_count="$(
  awk '
    /^## Active Pitfalls \(Mandatory\)/ { in_block=1; next }
    /^---/ && in_block { exit }
    in_block && /^- FP-[0-9][0-9][0-9] / { count++ }
    END { print count+0 }
  ' docs/Factory/SCRATCHPAD.md
)"

[[ "$pitfall_count" -ge 1 ]] || fail "Active Pitfalls section must include at least 1 entry"
[[ "$pitfall_count" -le 12 ]] || fail "Active Pitfalls section exceeds cap of 12 entries (found $pitfall_count)"

# Validate key Factory structural contracts exist
has_pattern '^## 0\.3 Execution Enablement Contract \(HARD\)$' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing execution enablement contract section"

has_pattern 'EXECUTION_MODE\.txt' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing run-root execution mode contract"

echo "knowledge_lint: PASS"
echo "knowledge_lint: checked_files=${#required_files[@]} active_pitfalls=$pitfall_count"
