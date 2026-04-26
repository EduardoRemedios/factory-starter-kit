#!/usr/bin/env bash
set -euo pipefail

# Factory Starter Kit — Knowledge Lint Preflight
#
# This validates the generic Factory doc spine before a run starts.
# Adapt the required_files list and pattern checks to match your
# project's canonical docs if you customize the starter kit.

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

required_files=(
  "AGENTS.md"
  "docs/PROJECT_STATE.md"
  "docs/ROADMAP.md"
  "docs/CHANGELOG.md"
  "docs/Factory/ARCHITECTURE.md"
  "docs/Factory/ORCHESTRATION.md"
  "docs/Factory/Harnesses/README.md"
  "docs/Factory/Harnesses/CODEX.md"
  "docs/Factory/MISSION_MODE.md"
  "docs/Factory/SCRATCHPAD.md"
  "docs/Factory/Spec/DEFINITIONS.md"
  "docs/Factory/Spec/STAGE_CONTRACTS.md"
  "docs/Factory/Spec/NAMING_CONVENTIONS.md"
  "docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md"
  "docs/Factory/templates/CONTEXT_RECALL_REPORT_TEMPLATE.md"
  "docs/Factory/templates/PACK_CHECKLIST_TEMPLATE.md"
  "docs/Factory/templates/PACK_MANIFEST_TEMPLATE.md"
  "docs/Factory/templates/EXECUTION_PROMPT_TEMPLATE.md"
  "docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md"
  "docs/Factory/templates/MISSION_MANIFEST_TEMPLATE.md"
  "docs/Factory/templates/MISSION_CHECKPOINT_TEMPLATE.md"
  "docs/Factory/templates/MISSION_EXECUTION_PROMPT_TEMPLATE.md"
  "docs/Factory/templates/MISSION_COMPLETION_REPORT_TEMPLATE.md"
  "docs/Factory/ProductOwner/PO_PROCESS.md"
  "docs/Factory/ProductOwner/PO_ROLE_DEFINITION.md"
  "docs/Factory/ProductOwner/PHASE_INTENT_REVIEW_CHECKLIST.md"
  "docs/Factory/ProductOwner/BRIEF_REVIEW_CHECKLIST.md"
  "docs/Factory/ProductOwner/templates/PHASE_BRIEF_TEMPLATE.md"
  "docs/Factory/ProductOwner/templates/PHASE_INTENT_TEMPLATE.md"
  "docs/Factory/ProductOwner/templates/PHASE_STATE_TEMPLATE.md"
  "scripts/factoryctl"
  "scripts/factory_context_index.py"
  "scripts/factory_pack_lint.py"
  "scripts/factory_stage_lint.py"
  "scripts/mission_lint.sh"
  ".agents/skills/factory-root-planner/SKILL.md"
  ".agents/skills/factory-purple-gate/SKILL.md"
  ".agents/skills/factory-pack-consolidator/SKILL.md"
  ".agents/skills/factory-execution-closeout/SKILL.md"
)

for path in "${required_files[@]}"; do
  require_nonempty_file "$path"
done

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

has_pattern '^## 0\.2 External Research Safety Protocol \(HARD for research-heavy runs\)$' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing external research safety protocol section"

has_pattern '^## 0\.3 Execution Enablement Contract \(HARD\)$' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing execution enablement contract section"

has_pattern '^## 0\.4 Mission Mode \(Additive, Optional\)$' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing mission mode section"

has_pattern '^## 0\.5 Product Owner Lane \(Optional, Upstream of Factory\)$' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing Product Owner lane section"

has_pattern 'CONTEXT_RECALL_REPORT\.md' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing context recall report contract"

has_pattern 'mission_lint\.sh' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing mission-lint contract"

has_pattern 'EXECUTION_MODE\.txt' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing run-root execution mode contract"

has_pattern 'factoryctl pack-lint --run <RUN_ID>' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing pack-lint validation contract"

has_pattern 'factoryctl stage-lint --run <RUN_ID> --stage <STAGE>' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing stage-lint validation contract"

has_pattern 'factoryctl stage-lint --run <RUN_ID> --stage <STAGE>' AGENTS.md \
  || fail "AGENTS.md missing stage-lint canonical command"

has_pattern 'gpt-5\.5' docs/Factory/Harnesses/CODEX.md \
  || fail "Codex harness adapter missing GPT-5.5 local model guidance"

has_pattern 'Codex cloud tasks and code review currently run on `GPT-5\.3-Codex`' docs/Factory/Harnesses/CODEX.md \
  || fail "Codex harness adapter missing cloud/review model boundary"

has_pattern '^## Codex CLI Terminal Flow$' docs/Factory/Harnesses/CODEX.md \
  || fail "Codex harness adapter missing CLI terminal flow"

has_pattern '^## Adapter Rule$' docs/Factory/Harnesses/README.md \
  || fail "Harness adapter README missing adapter rule"

has_pattern '^### 6\.1 Execution Prompt Generation \(execution-enabled runs only\)$' docs/Factory/ORCHESTRATION.md \
  || fail "Orchestration missing execution-enabled post-gate prompt contract"

has_pattern '^## Context recall rule \(HARD\)$' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing context recall rule"

has_pattern '^## POST_GATE — Execution Prompt Generation \(execution-enabled runs only\)$' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing execution-enabled post-gate execution prompt stage"

has_pattern '^## POST_I2_VALIDATION — Pack Lint$' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing post-I2 pack-lint validation stage"

has_pattern '^## STAGE_VALIDATION — Stage Lint$' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing stage-lint validation section"

has_pattern '^## MISSION_WRAPPER \(additive, optional — not a replacement stage chain\)$' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing mission wrapper section"

has_pattern 'MISSION_LINT\.txt' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing Mission Mode lint evidence contract"

has_pattern 'Run execution mode defaults to `PLANNING_ONLY`' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing planning-only default execution mode guardrail"

has_pattern 'Use the <skill name> skill\.' docs/Factory/Spec/STAGE_CONTRACTS.md \
  || fail "Stage contracts missing deterministic skill invocation directive"

has_pattern 'CONTEXT_RECALL_REPORT\.md' docs/Factory/Spec/NAMING_CONVENTIONS.md \
  || fail "Naming conventions missing context recall artifact names"

has_pattern 'MISSION_CONTEXT_RECALL_REPORT\.md' docs/Factory/MISSION_MODE.md \
  || fail "Mission mode contract missing mission context recall evidence"

has_pattern '^### 2\.2\.1 Mission unit status semantics$' docs/Factory/MISSION_MODE.md \
  || fail "Mission mode contract missing mission unit status semantics section"

has_pattern '^## 3\. Mission lifecycle \(HARD\)$' docs/Factory/MISSION_MODE.md \
  || fail "Mission mode contract missing mission lifecycle section"

has_pattern 'BRIEF_SPRINT_<N>_CONTEXT_RECALL_REPORT\.md' docs/Factory/ProductOwner/PO_PROCESS.md \
  || fail "PO process missing brief context recall report contract"

has_pattern 'CONTEXT_RECALL_REPORT\.md' docs/Factory/templates/PACK_MANIFEST_TEMPLATE.md \
  || fail "Pack manifest template missing context recall report completeness check"

has_pattern '^## Skill Routing Contract$' docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md \
  || fail "Handoff template missing Skill Routing Contract section"

has_pattern '^C9\. Knowledge lint preflight passed and evidence artifact is present in run root \(`KNOWLEDGE_LINT.txt`\)\.$' docs/Factory/Spec/PURPLE_GATE_CHECKLIST.md \
  || fail "Purple checklist missing C9 knowledge-lint critical item"

has_pattern '^C9\. Knowledge lint preflight passed and evidence artifact is present in run root \(`KNOWLEDGE_LINT.txt`\)\. \| Answer: YES/NO \| Evidence: \.\./KNOWLEDGE_LINT\.txt$' docs/Factory/templates/PACK_CHECKLIST_TEMPLATE.md \
  || fail "Pack checklist template missing C9 knowledge-lint item"

./scripts/factoryctl context-index --help >/dev/null \
  || fail "factoryctl context-index help probe failed"

./scripts/factoryctl context-recall --help >/dev/null \
  || fail "factoryctl context-recall help probe failed"

./scripts/factoryctl context-report --help >/dev/null \
  || fail "factoryctl context-report help probe failed"

./scripts/factoryctl pack-lint --help >/dev/null \
  || fail "factoryctl pack-lint help probe failed"

./scripts/factoryctl stage-lint --help >/dev/null \
  || fail "factoryctl stage-lint help probe failed"

echo "knowledge_lint: PASS"
echo "knowledge_lint: checked_files=${#required_files[@]} active_pitfalls=$pitfall_count"
