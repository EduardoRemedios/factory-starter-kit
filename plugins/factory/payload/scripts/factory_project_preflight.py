from __future__ import annotations

import hashlib
import json
import os
import re
import selectors
import signal
import subprocess
import time
from pathlib import Path
from typing import Any


DECLARATION_PATH = Path("docs/Factory/PROJECT_PREFLIGHT.json")
PROJECT_COMMAND = Path("scripts/factory_project_preflight")
MAX_STREAM_BYTES = 64 * 1024
DEFAULT_TIMEOUT_SECONDS = 60
MAX_TIMEOUT_SECONDS = 300
RUN_ID_RE = re.compile(r"RUN_\d{8}_\d{4}_[A-Za-z0-9_-]+")
REASON_CODE_RE = re.compile(r"[A-Z][A-Z0-9_]+")


class ProjectPreflightError(RuntimeError):
    """Raised only for invalid Core invocation, not project verdicts."""


def _result(reason_code: str, *, outcome: str = "halt", **details: Any) -> dict[str, Any]:
    return {
        "outcome": outcome,
        "reason_code": reason_code,
        **details,
    }


def _load_declaration(root: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    path = root / DECLARATION_PATH
    if not path.exists():
        return None, None
    if not path.is_file():
        return None, _result("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID")
    try:
        declaration = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None, _result("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID")
    if not isinstance(declaration, dict):
        return None, _result("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID")
    if set(declaration) - {"schema_version", "timeout_seconds"}:
        return None, _result("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID")
    if declaration.get("schema_version") != 1:
        return None, _result("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID")
    timeout = declaration.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS)
    if isinstance(timeout, bool) or not isinstance(timeout, int) or not 1 <= timeout <= MAX_TIMEOUT_SECONDS:
        return None, _result("FACTORY_PROJECT_PREFLIGHT_DECLARATION_INVALID")
    return {"schema_version": 1, "timeout_seconds": timeout}, None


def _kill_process_group(process: subprocess.Popen[bytes]) -> None:
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    if process.poll() is None:
        process.wait()


def _run_bounded(
    argv: list[str], *, cwd: Path, timeout_seconds: int
) -> tuple[int | None, bytes, bytes, str | None]:
    process = subprocess.Popen(
        argv,
        cwd=cwd,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        start_new_session=True,
    )
    assert process.stdout is not None
    assert process.stderr is not None
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    deadline = time.monotonic() + timeout_seconds
    failure: str | None = None

    try:
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                failure = "timeout"
                break
            events = selector.select(timeout=min(remaining, 0.1))
            for key, _ in events:
                chunk = os.read(key.fileobj.fileno(), 8192)
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                stream = key.data
                buffers[stream].extend(chunk)
                if len(buffers[stream]) > MAX_STREAM_BYTES:
                    failure = "output_too_large"
                    break
            if failure:
                break
    finally:
        selector.close()

    if failure:
        _kill_process_group(process)
    else:
        process.wait()
    process.stdout.close()
    process.stderr.close()
    return (
        process.returncode,
        bytes(buffers["stdout"][:MAX_STREAM_BYTES]),
        bytes(buffers["stderr"][:MAX_STREAM_BYTES]),
        failure,
    )


def _stream_metadata(stdout: bytes, stderr: bytes) -> dict[str, Any]:
    return {
        "stdout_bytes_retained": len(stdout),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stderr_bytes_retained": len(stderr),
        "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
    }


def _validate_project_output(root: Path, stdout: bytes) -> dict[str, Any]:
    try:
        text = stdout.decode("utf-8")
        payload = json.loads(text)
    except (UnicodeError, json.JSONDecodeError):
        return _result("FACTORY_PROJECT_PREFLIGHT_OUTPUT_MALFORMED")

    if not isinstance(payload, dict) or set(payload) != {
        "schema_version",
        "status",
        "reason_code",
        "evidence_paths",
    }:
        return _result("FACTORY_PROJECT_PREFLIGHT_OUTPUT_AMBIGUOUS")
    if payload.get("schema_version") != 1 or payload.get("status") not in {"PASS", "FAIL"}:
        return _result("FACTORY_PROJECT_PREFLIGHT_OUTPUT_AMBIGUOUS")
    project_reason = payload.get("reason_code")
    evidence_paths = payload.get("evidence_paths")
    if (
        not isinstance(project_reason, str)
        or not REASON_CODE_RE.fullmatch(project_reason)
        or not isinstance(evidence_paths, list)
        or not all(isinstance(item, str) and item for item in evidence_paths)
    ):
        return _result("FACTORY_PROJECT_PREFLIGHT_OUTPUT_AMBIGUOUS")

    normalized_paths: list[str] = []
    for value in evidence_paths:
        relative = Path(value)
        if relative.is_absolute() or ".." in relative.parts:
            return _result("FACTORY_PROJECT_PREFLIGHT_EVIDENCE_PATH_INVALID")
        candidate = (root / relative).resolve()
        try:
            normalized = candidate.relative_to(root).as_posix()
        except ValueError:
            return _result("FACTORY_PROJECT_PREFLIGHT_EVIDENCE_PATH_INVALID")
        if not candidate.is_file():
            return _result("FACTORY_PROJECT_PREFLIGHT_EVIDENCE_PATH_INVALID")
        normalized_paths.append(normalized)

    if payload["status"] == "FAIL":
        return _result(
            "FACTORY_PROJECT_PREFLIGHT_FAILED",
            project_reason_code=project_reason,
            evidence_paths=normalized_paths,
        )
    return _result(
        "FACTORY_PROJECT_PREFLIGHT_PASS",
        outcome="pass",
        project_reason_code=project_reason,
        evidence_paths=normalized_paths,
    )


def run_project_preflight(root: Path, run_id: str) -> dict[str, Any]:
    root = root.resolve()
    if not RUN_ID_RE.fullmatch(run_id):
        raise ProjectPreflightError(f"invalid Factory run ID: {run_id}")

    declaration, declaration_error = _load_declaration(root)
    if declaration_error:
        return declaration_error
    if declaration is None:
        return _result(
            "FACTORY_PROJECT_PREFLIGHT_NOT_DECLARED",
            outcome="pass",
            result_required=False,
        )

    command = root / PROJECT_COMMAND
    if not command.exists() or not command.is_file():
        return _result("FACTORY_PROJECT_PREFLIGHT_COMMAND_MISSING")
    if command.is_symlink() or not os.access(command, os.X_OK):
        return _result("FACTORY_PROJECT_PREFLIGHT_COMMAND_INVALID")

    return_code, stdout, stderr, failure = _run_bounded(
        [str(command), "--run", run_id, "--json"],
        cwd=root,
        timeout_seconds=declaration["timeout_seconds"],
    )
    metadata = _stream_metadata(stdout, stderr)
    if failure == "timeout":
        return _result("FACTORY_PROJECT_PREFLIGHT_TIMEOUT", **metadata)
    if failure == "output_too_large":
        return _result("FACTORY_PROJECT_PREFLIGHT_OUTPUT_TOO_LARGE", **metadata)
    if return_code != 0:
        return _result(
            "FACTORY_PROJECT_PREFLIGHT_EXIT_NONZERO",
            return_code=return_code,
            **metadata,
        )

    return {**_validate_project_output(root, stdout), **metadata}


def _evidence_run_root(root: Path, run_id: str) -> Path:
    if not RUN_ID_RE.fullmatch(run_id):
        raise ProjectPreflightError(f"invalid Factory run ID: {run_id}")
    cursor = root.resolve()
    for part in ("docs", "Factory", "runs", run_id):
        cursor = cursor / part
        if cursor.is_symlink():
            raise ProjectPreflightError(f"unsafe Factory run root: {run_id}")
    if not cursor.is_dir():
        raise ProjectPreflightError(f"Factory run root does not exist: {run_id}")
    return cursor


def write_project_preflight_evidence(root: Path, run_id: str, result: dict[str, Any]) -> Path:
    run_root = _evidence_run_root(root, run_id)
    status = "PASS" if result["outcome"] == "pass" else "HALT"
    lines = [
        f"project_preflight: {status}",
        f"reason_code: {result['reason_code']}",
        f"run_id: {run_id}",
    ]
    for key in (
        "project_reason_code",
        "return_code",
        "stdout_bytes_retained",
        "stdout_sha256",
        "stderr_bytes_retained",
        "stderr_sha256",
        "result_required",
    ):
        if key in result:
            lines.append(f"{key}: {result[key]}")
    for path in result.get("evidence_paths", []):
        lines.append(f"evidence_path: {path}")
    evidence_path = run_root / "PROJECT_PREFLIGHT.txt"
    evidence_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return evidence_path
