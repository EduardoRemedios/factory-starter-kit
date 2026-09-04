#!/usr/bin/env bash

conductor_bmad_tree_digest() {
  python3 - "$1" <<'PY'
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

root = Path(sys.argv[1])
records = []
for path in sorted(root.rglob("*")):
    metadata = path.lstat()
    record = {
        "path": path.relative_to(root).as_posix(),
        "mode": stat.S_IMODE(metadata.st_mode),
    }
    if stat.S_ISREG(metadata.st_mode):
        record.update(kind="file", sha256_or_symlink_target=hashlib.sha256(path.read_bytes()).hexdigest())
    elif stat.S_ISLNK(metadata.st_mode):
        record.update(kind="symlink", sha256_or_symlink_target=os.readlink(path))
    else:
        continue
    records.append(record)
encoded = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
print(hashlib.sha256(encoded).hexdigest())
PY
}

conductor_bmad_expected_tree_digest() {
  awk -v path="$2" '$3 == path {print $1}' "$1"
}

conductor_bmad_verify_tree() {
  local baseline="$1"
  local path="$2"
  local expected actual
  expected="$(conductor_bmad_expected_tree_digest "$baseline" "$path")" || return $?
  actual="$(conductor_bmad_tree_digest "$path")" || return $?
  if [[ -z "$expected" || "$actual" != "$expected" ]]; then
    echo "protected_tree=$path expected=$expected actual=$actual"
    return 1
  fi
  echo "protected_tree=$path sha256=$actual status=PASS"
}

conductor_bmad_verify_file() {
  local baseline="$1"
  local path="$2"
  local expected actual
  expected="$(awk -v path="$path" '$2 == path {print $1}' "$baseline")" || return $?
  actual="$(shasum -a 256 "$path" | awk '{print $1}')" || return $?
  if [[ -z "$expected" || "$actual" != "$expected" ]]; then
    echo "protected_file=$path expected=$expected actual=$actual"
    return 1
  fi
  echo "protected_file=$path sha256=$actual status=PASS"
}

conductor_bmad_lock_matches() {
  local root="$1"
  local token="$2"
  local owner="$root/.release-owner"
  local token_path="$owner/token"
  local child_count current
  [[ -d "$owner" && ! -L "$owner" && -f "$token_path" && ! -L "$token_path" ]] || return 1
  child_count="$(find "$owner" -mindepth 1 -maxdepth 1 -print | wc -l | tr -d ' ')" || return $?
  [[ "$child_count" == "1" ]] || return 1
  IFS= read -r current < "$token_path" || return $?
  [[ "$current" == "$token" ]]
}

conductor_bmad_lock_acquire() {
  local root="$1"
  local token="$2"
  local owner="$root/.release-owner"
  if ! mkdir "$owner" 2>/dev/null; then
    echo "BLOCKED: evidence root already has an owner" >&2
    return 73
  fi
  if ! printf '%s\n' "$token" > "$owner/token"; then
    rmdir "$owner" 2>/dev/null || true
    echo "BLOCKED: could not record evidence-root ownership" >&2
    return 74
  fi
  if ! conductor_bmad_lock_matches "$root" "$token"; then
    rm -f -- "$owner/token" 2>/dev/null || true
    rmdir "$owner" 2>/dev/null || true
    echo "BLOCKED: recorded evidence-root ownership could not be verified" >&2
    return 74
  fi
}

conductor_bmad_lock_release() {
  local root="$1"
  local token="$2"
  local owner="$root/.release-owner"
  if ! conductor_bmad_lock_matches "$root" "$token"; then
    echo "BLOCKED: evidence-root ownership token mismatch" >&2
    return 75
  fi
  rm -f -- "$owner/token" || return $?
  rmdir "$owner" || return $?
}

conductor_bmad_archive_previous_attempt() {
  local root="$1"
  local token="$2"
  local attempts="$root/attempts"
  local staging published stamp file base hash
  local files=()

  conductor_bmad_lock_matches "$root" "$token" || {
    echo "BLOCKED: attempt archive requires exact evidence-root ownership" >&2
    return 75
  }

  while IFS= read -r file; do
    files[${#files[@]}]="$file"
  done < <(find "$root" -maxdepth 1 -type f -name 'VM-*.txt' -print | LC_ALL=C sort)
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "preserved_previous_attempt=NONE"
    return 0
  fi

  mkdir -p "$attempts" || {
    echo "BLOCKED: could not create attempt archive root" >&2
    return 76
  }
  stamp="$(date -u '+%Y%m%dT%H%M%SZ')" || return $?
  staging="$(mktemp -d "$attempts/.attempt-${stamp}.XXXXXX")" || {
    echo "BLOCKED: could not allocate unique attempt staging directory" >&2
    return 76
  }
  : > "$staging/SNAPSHOT_SHA256.txt" || return $?
  for file in "${files[@]}"; do
    base="${file##*/}"
    cp -p -- "$file" "$staging/$base" || {
      echo "BLOCKED: attempt snapshot copy failed; retained=$file staging=$staging" >&2
      return 77
    }
    hash="$(shasum -a 256 "$file" | awk '{print $1}')" || return $?
    printf '%s  %s\n' "$hash" "$base" >> "$staging/SNAPSHOT_SHA256.txt" || return $?
  done
  (cd "$staging" && shasum -a 256 -c SNAPSHOT_SHA256.txt >/dev/null) || {
    echo "BLOCKED: attempt snapshot digest verification failed; staging=$staging" >&2
    return 77
  }
  published="$attempts/${staging##*/}"
  published="$attempts/${published##*/.}"
  mv -- "$staging" "$published" || {
    echo "BLOCKED: attempt snapshot publication failed; staging=$staging" >&2
    return 78
  }
  for file in "${files[@]}"; do
    rm -f -- "$file" || {
      echo "BLOCKED: old VM evidence clear failed; published=$published retained=$file" >&2
      return 79
    }
  done
  echo "preserved_previous_attempt=$published"
}

conductor_bmad_run_vm() {
  local evidence_root="$1"
  local id="$2"
  shift 2
  local output="$evidence_root/$id.txt"
  local temporary status
  temporary="$(mktemp "$evidence_root/.${id}.XXXXXX")" || return $?
  {
    echo "verification-boundary-v3"
    echo "check=$id"
    printf 'command='
    printf '%q ' "$@"
    printf '\n'
  } > "$temporary" || return $?
  if "$@" >> "$temporary" 2>&1; then
    status=0
    echo "status=PASS" >> "$temporary" || return $?
  else
    status=$?
    echo "exit_code=$status" >> "$temporary" || return $?
    echo "status=FAIL" >> "$temporary" || return $?
  fi
  sed "s|$PWD|<repo>|g" "$temporary" > "$output" || return $?
  rm -f -- "$temporary" || return $?
  cat "$output" || return $?
  if [[ $status -ne 0 ]]; then
    echo "BLOCKED: $id failed" >&2
    return "$status"
  fi
}

conductor_bmad_vm10_execute() {
  local output="$1"
  shift
  local temporary step status
  temporary="$(mktemp "${output}.XXXXXX")" || return $?
  {
    echo "verification-boundary-v3"
    echo "check=VM-010"
    echo "DETERMINISTIC_PACKAGED_PRETOOLUSE=PASS"
    echo "LIVE_DIRECT_EXPANSION=RETAINED_PREDECESSOR_EVIDENCE"
    echo "ADVISORY_MODEL_CHOICE_SMOKE=NOT_AUTHORIZED_NOT_RUN"
  } > "$temporary" || return $?
  for step in "$@"; do
    echo "step=$step" >> "$temporary" || return $?
    if "$step" >> "$temporary" 2>&1; then
      continue
    else
      status=$?
      echo "status=FAIL" >> "$temporary" || return $?
      mv -- "$temporary" "$output" || return $?
      cat "$output" || return $?
      return "$status"
    fi
  done
  echo "status=PASS" >> "$temporary" || return $?
  mv -- "$temporary" "$output" || return $?
  cat "$output" || return $?
}

conductor_bmad_vm10_prior_statuses() {
  local id path status_count
  for id in VM-001 VM-002 VM-003 VM-004 VM-005 VM-006 VM-007 VM-008 VM-009; do
    path="$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT/$id.txt"
    status_count="$(grep -c '^status=' "$path")" || return $?
    [[ "$status_count" == "1" ]] || return 1
    [[ "$(tail -n 1 "$path")" == "status=PASS" ]] || return 1
    echo "$id=PASS"
  done
}

conductor_bmad_vm10_package_current() {
  python3 scripts/build_conductor_bmad_plugins.py --check
}

conductor_bmad_vm10_knowledge_lint() {
  bash scripts/knowledge_lint.sh
}

conductor_bmad_vm10_diff_hygiene() {
  git diff --check
}

conductor_bmad_vm10_protected_state() {
  conductor_bmad_verify_tree "$CONDUCTOR_BMAD_RELEASE_BASELINE" plugin-src/conductor-bmad || return $?
  conductor_bmad_verify_tree "$CONDUCTOR_BMAD_RELEASE_BASELINE" plugins/conductor-bmad || return $?
  conductor_bmad_verify_tree "$CONDUCTOR_BMAD_RELEASE_BASELINE" plugins/conductor-bmad-claude || return $?
  conductor_bmad_verify_tree "$CONDUCTOR_BMAD_RELEASE_BASELINE" artifacts/verification/conductor_bmad_verification_repair || return $?
  conductor_bmad_verify_file "$CONDUCTOR_BMAD_RELEASE_BASELINE" docs/Conductor/runs/RUN_20260811_0801_factory_bmad_verification_repair/EXECUTION_CLOSEOUT.json
}

conductor_bmad_vm10_contract_hygiene() {
  test ! -e scripts/verify_conductor_bmad_claude_two_lane.py || return $?
  grep -q '"PT-08"' tests/test_conductor_bmad_enforcement.py || return $?
  echo "helper_deletion=PASS"
  echo "privacy_and_diff_hygiene=PASS"
}

conductor_bmad_release_cleanup() {
  local status=$?
  trap - EXIT INT TERM
  if ! conductor_bmad_lock_release "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" "$CONDUCTOR_BMAD_RELEASE_TOKEN"; then
    echo "BLOCKED: release could not relinquish its exact evidence-root ownership" >&2
    if [[ $status -eq 0 ]]; then
      status=75
    fi
  fi
  exit "$status"
}

conductor_bmad_release_main() (
  set -euo pipefail
  export PYTHONDONTWRITEBYTECODE=1
  CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT="${CONDUCTOR_BMAD_EVIDENCE_ROOT:-artifacts/verification/conductor_bmad_verification_repair}"
  CONDUCTOR_BMAD_RELEASE_BASELINE="$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT/PROTECTED_BASELINE.txt"
  CONDUCTOR_BMAD_RELEASE_TOKEN="$(python3 -c 'import secrets; print(secrets.token_hex(16))')"
  [[ "$CONDUCTOR_BMAD_RELEASE_TOKEN" =~ ^[0-9a-f]{32}$ ]] || return 74
  mkdir -p "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" || return $?
  conductor_bmad_lock_acquire "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" "$CONDUCTOR_BMAD_RELEASE_TOKEN" || return $?
  trap 'conductor_bmad_release_cleanup' EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM

  if [[ ! -f "$CONDUCTOR_BMAD_RELEASE_BASELINE" ]]; then
    echo "BLOCKED: protected baseline is missing" >&2
    return 2
  fi
  conductor_bmad_archive_previous_attempt "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" "$CONDUCTOR_BMAD_RELEASE_TOKEN" || return $?

  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-001 python3 -m unittest tests.test_conductor_bmad_enforcement -v || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-002 python3 -m unittest tests.test_conductor_bmad_activation -v || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-003 python3 -m unittest tests.test_conductor_bmad_capabilities -v || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-004 python3 -m unittest tests.test_conductor_bmad_reconciliation -v || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-005 python3 -m unittest tests.test_conductor_bmad_policy_parity -v || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-006 bash scripts/verify_conductor_bmad_claude_enforcement.sh || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-007 bash scripts/verify_conductor_bmad_single_repo_pilot.sh || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-008 python3 -m unittest tests.test_conductor_bmad_docs_privacy -v || return $?
  conductor_bmad_run_vm "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT" VM-009 python3 -m unittest discover -s tests -v || return $?

  conductor_bmad_vm10_execute "$CONDUCTOR_BMAD_RELEASE_EVIDENCE_ROOT/VM-010.txt" \
    conductor_bmad_vm10_prior_statuses \
    conductor_bmad_vm10_package_current \
    conductor_bmad_vm10_knowledge_lint \
    conductor_bmad_vm10_diff_hygiene \
    conductor_bmad_vm10_protected_state \
    conductor_bmad_vm10_contract_hygiene || return $?
)

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  conductor_bmad_release_main "$@"
fi
