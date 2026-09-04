#!/usr/bin/env bash
# Project merge preflight per docs/Factory/MERGE_PROTOCOL.md.
# Runs the merge preconditions against the configured base branch and writes
# evidence to artifacts/merge_preflight/<UTC>/SUMMARY.md plus one log per
# check. Exits 0 only when every check passes (MERGE_READY).
# Base override: MERGE_PREFLIGHT_BASE=origin/<branch> (default origin/main).
set -u -o pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BASE_REF="${MERGE_PREFLIGHT_BASE:-origin/main}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
EVIDENCE_DIR="artifacts/merge_preflight/$STAMP"
mkdir -p "$EVIDENCE_DIR"
SUMMARY="$EVIDENCE_DIR/SUMMARY.md"

ROWS=""
OVERALL="MERGE_READY"

record() {
  ROWS="${ROWS}| $1 | $2 | $3 |
"
  if [ "$2" = "FAIL" ]; then
    OVERALL="NOT_MERGE_READY"
  fi
}

check() {
  local name="$1"
  shift
  local log="$EVIDENCE_DIR/$name.log"
  if "$@" >"$log" 2>&1; then
    record "$name" "PASS" "$log"
  else
    record "$name" "FAIL" "$log"
  fi
}

clean_worktree() {
  # The preflight's own evidence path is the one sanctioned untracked location.
  local status
  status="$(git status --porcelain=v1 -uall)" || return 1
  status="$(printf '%s\n' "$status" | grep -v '^?? artifacts/merge_preflight/')" || true
  if [ -n "$status" ]; then
    printf '%s\n' "$status"
    return 1
  fi
  echo "tree clean outside artifacts/merge_preflight/"
}

base_sync() {
  git fetch -q origin || return 1
  local base_sha
  base_sha="$(git rev-parse "$BASE_REF")" || return 1
  echo "base $BASE_REF at $base_sha"
  git merge-base --is-ancestor "$base_sha" HEAD
}

pack_lint_all_runs() {
  if [ ! -d docs/Factory/runs ]; then
    echo "no Factory runs present; nothing to pack-lint"
    return 0
  fi
  local failed=0 run_dir
  for run_dir in docs/Factory/runs/*/; do
    [ -d "$run_dir" ] || continue
    if ./scripts/factoryctl pack-lint --run "$(basename "$run_dir")"; then
      echo "pack-lint PASS: $(basename "$run_dir")"
    else
      echo "pack-lint FAIL: $(basename "$run_dir")"
      failed=1
    fi
  done
  return "$failed"
}

check clean_worktree clean_worktree
check base_sync base_sync
check git_diff_check git diff --check
check knowledge_lint bash scripts/knowledge_lint.sh
check full_test_suite ./scripts/factory-python -m unittest discover -s tests -p 'test_*.py'
check pack_lint pack_lint_all_runs

{
  echo "# Merge Preflight Summary"
  echo
  echo "- Timestamp (UTC): $STAMP"
  echo "- HEAD: $(git rev-parse HEAD)"
  echo "- Base ref: $BASE_REF"
  echo "- Verdict: $OVERALL"
  echo
  echo "| Check | Result | Log |"
  echo "|---|---|---|"
  printf '%s' "$ROWS"
  echo
  echo "MERGE_READY permits asking for merge authorization only; it grants no"
  echo "merge, publication, pilot, or rollout authority by itself, and it goes"
  echo "stale if the base branch moves afterward."
} > "$SUMMARY"

echo "merge_preflight: $OVERALL"
echo "summary: $SUMMARY"
[ "$OVERALL" = "MERGE_READY" ]
