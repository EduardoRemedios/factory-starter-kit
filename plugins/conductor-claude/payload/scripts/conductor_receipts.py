"""Conductor receipts runner: executes verification-manifest checks and writes signed receipts.

The runner is the only legitimate author of receipts and of checks[].result. A receipt's
payload_sha256 covers every other field; contract-lint recomputes it, so a receipt written
or edited by an agent is detected as tampered. Output streams are captured bounded
(64 KiB each) to receipts/logs/ and only their digests and sizes enter the receipt.

    receipts run     --run RUN_ID [--check ID ...] [--timeout-seconds N]
    receipts attest  --run RUN_ID --check ID --signer NAME   (manual-type checks only)
"""
from __future__ import annotations

import json
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from conductor_contract_lint import (
    ContractLintError,
    read_yaml,
    receipt_payload_digest,
    safe_run_root,
    schema_errors,
    sha256_bytes,
)

MAX_STREAM_BYTES = 64 * 1024
RUNNABLE = {"static", "command", "test", "no_touch"}
TARGET_BASED = {"artifact", "fixture", "source_revalidation"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _bounded(data: bytes) -> bytes:
    return data[:MAX_STREAM_BYTES]


def _argv(command: Any) -> list[str]:
    if isinstance(command, list):
        return [str(part) for part in command]
    return shlex.split(str(command))


def _write_receipt(run_root: Path, run_id: str, check: dict[str, Any], *, argv: list[str], cwd: str, exit_code: int,
                   stdout: bytes, stderr: bytes, started: str, finished: str, expected_exit: int, root: Path) -> tuple[Path, dict[str, Any]]:
    logs = run_root / "receipts" / "logs"
    logs.mkdir(parents=True, exist_ok=True)
    out_path = logs / f"{check['id']}.stdout.txt"
    err_path = logs / f"{check['id']}.stderr.txt"
    out_path.write_bytes(_bounded(stdout))
    err_path.write_bytes(_bounded(stderr))
    receipt: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "check_id": check["id"],
        "command": argv,
        "cwd": cwd,
        "exit_code": exit_code,
        "expected_exit": expected_exit,
        "stdout_sha256": sha256_bytes(_bounded(stdout)),
        "stderr_sha256": sha256_bytes(_bounded(stderr)),
        "stdout_bytes": len(_bounded(stdout)),
        "stderr_bytes": len(_bounded(stderr)),
        "stdout_path": out_path.relative_to(run_root).as_posix(),
        "stderr_path": err_path.relative_to(run_root).as_posix(),
        "started_utc": started,
        "finished_utc": finished,
        "status": "PASS" if exit_code == expected_exit else "FAIL",
    }
    receipt["payload_sha256"] = receipt_payload_digest(receipt)
    problems = schema_errors(root, "evidence_receipt", receipt)
    if problems:
        raise ContractLintError("CONDUCTOR_RECEIPT_SCHEMA_INVALID", "; ".join(problems))
    path = run_root / "receipts" / f"{check['id']}.json"
    path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path, receipt


def _execute(root: Path, check: dict[str, Any], timeout_seconds: int) -> tuple[list[str], int, bytes, bytes]:
    argv = _argv(check["command"])
    try:
        completed = subprocess.run(argv, cwd=root, capture_output=True, timeout=timeout_seconds, check=False, shell=False)
        return argv, completed.returncode, completed.stdout, completed.stderr
    except FileNotFoundError as exc:
        return argv, 127, b"", f"CONDUCTOR_RECEIPT_COMMAND_MISSING: {exc}\n".encode("utf-8")
    except subprocess.TimeoutExpired as exc:
        return argv, 124, exc.stdout or b"", (exc.stderr or b"") + b"\nCONDUCTOR_RECEIPT_TIMEOUT\n"


def _target_check(root: Path, check: dict[str, Any]) -> tuple[list[str], int, bytes, bytes]:
    target = root / check["target"]
    argv = ["conductor-receipts", "target-exists", check["target"]]
    if target.is_file() and target.stat().st_size > 0:
        return argv, 0, f"{check['target']}: present, {target.stat().st_size} bytes\n".encode("utf-8"), b""
    return argv, 1, b"", f"{check['target']}: missing or empty\n".encode("utf-8")


def run_receipts(root: Path, run_id: str, check_ids: list[str] | None = None, timeout_seconds: int = 900) -> dict[str, Any]:
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    manifest_path = run_root / "verification_manifest.yaml"
    errors: list[str] = []
    manifest = read_yaml(manifest_path, "verification_manifest.yaml", errors)
    if manifest is None:
        raise ContractLintError("CONDUCTOR_RECEIPT_MANIFEST_MISSING", "; ".join(errors))
    problems = schema_errors(root, "verification_manifest_v2", manifest)
    if problems:
        raise ContractLintError("CONDUCTOR_RECEIPT_MANIFEST_INVALID", "; ".join(problems))
    wanted = set(check_ids) if check_ids else None
    order = manifest.get("execution_order") or [c["id"] for c in manifest["checks"]]
    by_id = {c["id"]: c for c in manifest["checks"]}
    outcomes: dict[str, str] = {}
    for check_id in order:
        check = by_id.get(check_id)
        if check is None or (wanted is not None and check_id not in wanted):
            continue
        started = utc_now()
        if check["type"] in RUNNABLE:
            argv, code, out, err = _execute(root, check, timeout_seconds)
        elif check["type"] in TARGET_BASED:
            argv, code, out, err = _target_check(root, check)
        else:  # manual: needs `receipts attest`
            check["result"] = {"status": "NOT_RUN", "receipt_path": f"receipts/{check_id}.json"}
            outcomes[check_id] = "NOT_RUN"
            continue
        path, receipt = _write_receipt(run_root, run_id, check, argv=argv, cwd=".", exit_code=code, stdout=out, stderr=err,
                                       started=started, finished=utc_now(), expected_exit=int(check.get("expected_exit", 0)), root=root)
        check["result"] = {"status": receipt["status"], "receipt_path": path.relative_to(run_root).as_posix(),
                           "exit_code": code, "utc": receipt["finished_utc"]}
        outcomes[check_id] = receipt["status"]
        if receipt["status"] == "FAIL" and check["halt_on_failure"]:
            break
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {"run_id": run_id, "outcomes": outcomes, "manifest": manifest_path.relative_to(root).as_posix()}


def attest(root: Path, run_id: str, check_id: str, signer: str, note: str = "") -> dict[str, Any]:
    """Record a human attestation for a manual-type check. The signer's name is the command line of the receipt."""
    root = root.resolve()
    if not signer.strip():
        raise ContractLintError("CONDUCTOR_RECEIPT_SIGNER_REQUIRED", "attestation needs a signer")
    run_root = safe_run_root(root, run_id)
    manifest_path = run_root / "verification_manifest.yaml"
    errors: list[str] = []
    manifest = read_yaml(manifest_path, "verification_manifest.yaml", errors)
    if manifest is None:
        raise ContractLintError("CONDUCTOR_RECEIPT_MANIFEST_MISSING", "; ".join(errors))
    check = next((c for c in manifest["checks"] if c["id"] == check_id), None)
    if check is None:
        raise ContractLintError("CONDUCTOR_RECEIPT_UNKNOWN_CHECK", check_id)
    if check["type"] != "manual":
        raise ContractLintError("CONDUCTOR_RECEIPT_ATTEST_NOT_MANUAL", f"{check_id} is type {check['type']}; run it instead")
    now = utc_now()
    argv = ["conductor-receipts", "human-attestation", signer.strip()]
    stdout = f"attested by {signer.strip()} at {now}\n{note}".encode("utf-8")
    path, receipt = _write_receipt(run_root, run_id, check, argv=argv, cwd=".", exit_code=0, stdout=stdout, stderr=b"",
                                   started=now, finished=now, expected_exit=0, root=root)
    check["result"] = {"status": "PASS", "receipt_path": path.relative_to(run_root).as_posix(), "exit_code": 0, "utc": now}
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return {"run_id": run_id, "check_id": check_id, "receipt": path.relative_to(root).as_posix(), "signer": signer.strip()}


if __name__ == "__main__":  # pragma: no cover - thin manual entry point; conductorctl is the CLI
    print("use: conductorctl receipts run|attest", file=sys.stderr)
    sys.exit(2)
