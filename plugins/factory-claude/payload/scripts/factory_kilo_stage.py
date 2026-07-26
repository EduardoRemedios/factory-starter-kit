from __future__ import annotations

import hashlib
import json
import os
import shlex
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class FactoryKiloStageError(Exception):
    """Raised when a Kilo stage run cannot be prepared or completed safely."""


STAGES = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "I2")

STAGE_INPUTS: dict[str, tuple[str, ...]] = {
    "A": ("raw_brief.md", "CONTEXT_RECALL_REPORT.md", "EXECUTION_MODE.txt"),
    "B": ("pack/intent.md",),
    "C": ("pack/intent.md", "pack/intent_redteam.md"),
    "D": ("pack/intent.md", "pack/intent_redteam.md", "pack/intent_synthesis.md"),
    "E": ("pack/intent.md", "pack/intent_lock_report.md"),
    "F": ("pack/intent.md", "pack/risk_register.md", "pack/intent_lock_report.md"),
    "G": (
        "pack/intent.md",
        "pack/risk_register.md",
        "pack/verification_plan.md",
        "pack/traceability_matrix.md",
        "pack/intent_synthesis.md",
    ),
    "H": ("pack/intent.md", "pack/micro_sprints.md", "pack/verification_plan.md", "pack/traceability_matrix.md"),
    "I": ("pack/micro_sprints.md", "pack/verification_plan.md", "pack/traceability_matrix.md", "pack/risk_register.md"),
    "J": ("pack",),
    "I2": ("pack",),
}

STAGE_OUTPUTS: dict[str, tuple[str, ...]] = {
    "A": ("pack/intent.md",),
    "B": ("pack/intent_redteam.md",),
    "C": ("pack/intent.md", "pack/intent_synthesis.md"),
    "D": ("pack/intent_lock_report.md",),
    "E": ("pack/premortem.md", "pack/risk_register.md"),
    "F": ("pack/fixtures", "pack/verification_plan.md", "pack/traceability_matrix.md"),
    "G": ("pack/micro_sprints.md",),
    "J": ("pack/PACK_MANIFEST.md", "pack/PACK_CHECKLIST.md"),
    "I2": ("pack/PACK_AUDIT_REPORT.md", "pack/PACK_MANIFEST.md"),
}

LOCK_FILENAME = ".factory_kilo_stage.lock"
EXCLUDED_DIRS = {".git", ".factory_context", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
EXCLUDED_FILES = {LOCK_FILENAME}


@dataclass(frozen=True)
class StagePaths:
    run_root: Path
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    allowed_writes: tuple[str, ...]


def run_kilo_stage(
    *,
    root: Path,
    run: str,
    stage: str,
    model: str,
    variant: str | None = None,
    agent: str | None = None,
    kilo_bin: str = "kilo",
    auto: bool = False,
    timeout_seconds: int | None = None,
    dry_run: bool = False,
    allow_nested_kilo: bool = False,
) -> dict[str, Any]:
    stage = stage.upper()
    if stage not in STAGES:
        raise FactoryKiloStageError(f"unknown stage: {stage}")
    if not model:
        raise FactoryKiloStageError("model is required")

    paths = _stage_paths(root=root, run=run, stage=stage)
    prompt = _build_prompt(stage=stage, paths=paths, model=model)
    command = _build_command(
        kilo_bin=kilo_bin,
        root=root,
        model=model,
        variant=variant,
        agent=agent,
        auto=auto,
        prompt=prompt,
    )

    payload: dict[str, Any] = {
        "status": "DRY_RUN" if dry_run else "PENDING",
        "run_root": str(paths.run_root),
        "stage": stage,
        "model": model,
        "variant": variant,
        "agent": agent,
        "auto": auto,
        "command": _redacted_command(command),
        "prompt": prompt,
        "allowed_writes": list(paths.allowed_writes),
        "changed_paths": [],
        "unauthorized_paths": [],
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "evidence_path": None,
    }

    if dry_run:
        return payload

    try:
        paths.run_root.relative_to(root)
    except ValueError as exc:
        raise FactoryKiloStageError(f"kilo-stage execution requires the run root to be inside the repo: {paths.run_root}") from exc

    if not allow_nested_kilo and _running_under_kilo():
        raise FactoryKiloStageError(
            "refusing to run nested Kilo: invoke factoryctl kilo-stage from a neutral shell, Codex, or another non-Kilo orchestrator "
            "so Kilo remains the worker lane, not the parent process"
        )

    lock_path = _acquire_stage_lock(paths.run_root, stage)
    try:
        before = _snapshot(root)
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                text=True,
                capture_output=True,
                timeout=timeout_seconds,
                check=False,
            )
            exit_code: int | str = completed.returncode
            stdout = completed.stdout
            stderr = completed.stderr
        except subprocess.TimeoutExpired as exc:
            exit_code = "TIMEOUT"
            stdout = _decode_timeout_output(exc.stdout)
            stderr = _decode_timeout_output(exc.stderr)
            stderr = (stderr + "\n" if stderr else "") + f"kilo-stage timed out after {timeout_seconds} seconds"

        after = _snapshot(root)
        changed_paths = _changed_paths(before, after)
        unauthorized = _unauthorized_paths(
            changed_paths=changed_paths,
            allowed_writes=paths.allowed_writes,
            root=root,
            run_root=paths.run_root,
        )
        status = "PASS" if exit_code == 0 and not unauthorized else "FAIL"

        payload.update(
            {
                "status": status,
                "changed_paths": changed_paths,
                "unauthorized_paths": unauthorized,
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
            }
        )
        payload["evidence_path"] = str(_write_evidence(paths.run_root, payload))
    finally:
        _release_stage_lock(lock_path)
    return payload


def format_kilo_stage(payload: dict[str, Any]) -> str:
    lines = [
        f"kilo_stage: {payload['status']}",
        f"run_root={payload['run_root']}",
        f"stage={payload['stage']} model={payload['model']}",
        f"auto={payload['auto']} exit_code={payload['exit_code']}",
    ]
    if payload.get("variant"):
        lines[-1] += f" variant={payload['variant']}"
    if payload.get("agent"):
        lines[-1] += f" agent={payload['agent']}"
    lines.append("allowed_writes:")
    lines.extend(f"- {path}" for path in payload["allowed_writes"])
    if payload["changed_paths"]:
        lines.append("changed_paths:")
        lines.extend(f"- {path}" for path in payload["changed_paths"])
    if payload["unauthorized_paths"]:
        lines.append("unauthorized_paths:")
        lines.extend(f"- {path}" for path in payload["unauthorized_paths"])
    if payload.get("evidence_path"):
        lines.append(f"evidence_path={payload['evidence_path']}")
    if payload["status"] == "DRY_RUN":
        lines.append("command:")
        lines.append(" ".join(shlex.quote(part) for part in payload["command"]))
    return "\n".join(lines) + "\n"


def _build_command(
    *,
    kilo_bin: str,
    root: Path,
    model: str,
    variant: str | None,
    agent: str | None,
    auto: bool,
    prompt: str,
) -> list[str]:
    command = [
        kilo_bin,
        "run",
        "--dir",
        str(root),
        "--model",
        model,
        "--format",
        "json",
    ]
    if variant:
        command.extend(["--variant", variant])
    if agent:
        command.extend(["--agent", agent])
    if auto:
        command.append("--auto")
    command.append(prompt)
    return command


def _redacted_command(command: list[str]) -> list[str]:
    redacted: list[str] = []
    skip_next = False
    for part in command:
        if skip_next:
            redacted.append("<redacted>")
            skip_next = False
            continue
        redacted.append(part)
        if part in {"--password", "--username"}:
            skip_next = True
    return redacted


def _build_prompt(*, stage: str, paths: StagePaths, model: str) -> str:
    inputs = "\n".join(f"- {item}" for item in paths.inputs)
    outputs = "\n".join(f"- {item}" for item in paths.outputs)
    allowed = "\n".join(f"- {item}" for item in paths.allowed_writes)
    return f"""Run exactly one Factory stage in this repository.

Kilo External Lane Mode:
- You are the Kilo worker lane for this one stage only.
- The parent orchestrator is outside Kilo and will run validation after you exit.
- Do not launch `kilo`, `kilocode`, `factoryctl kilo-stage`, or any nested agent process.
- Do not continue to the next Factory stage.

Stage: {stage}
Model lane: {model}
Run root: {paths.run_root}

Read first:
- AGENTS.md
- docs/Factory/ORCHESTRATION.md
- docs/Factory/Spec/STAGE_CONTRACTS.md
- docs/Factory/templates/HANDOFF_STAGE_TEMPLATE.md
- docs/Factory/SCRATCHPAD.md Active Pitfalls only

Stage inputs:
{inputs}

Expected stage outputs:
{outputs}

Allowed write paths:
{allowed}

Hard rules:
- Do not implement product code.
- Do not run Kilo, kilocode, or factoryctl kilo-stage from inside this worker lane.
- Do not change Factory Core docs, scripts, templates, or files outside the allowed write paths.
- Write or update the stage handoff at pack/HANDOFF/HANDOFF_STAGE_{stage}.md.
- Preserve the stage contract and artifact naming exactly.
- If required inputs are missing or stage intent is ambiguous, write a FAIL handoff and stop.
- Keep changes small and explicit.
"""


def _stage_paths(*, root: Path, run: str, stage: str) -> StagePaths:
    run_root = _resolve_run(root=root, run=run)
    inputs = STAGE_INPUTS[stage]
    outputs = _stage_outputs(run_root=run_root, stage=stage)
    handoff = f"pack/HANDOFF/HANDOFF_STAGE_{stage}.md"
    allowed_writes = tuple(dict.fromkeys((*outputs, handoff)))
    return StagePaths(run_root=run_root, inputs=inputs, outputs=outputs, allowed_writes=allowed_writes)


def _stage_outputs(*, run_root: Path, stage: str) -> tuple[str, ...]:
    if stage == "H":
        sprint_id = _read_text(run_root / "SPRINT_ID.txt").strip()
        return ("SPRINT_ID.txt", f"pack/{sprint_id}_ENVELOPE.md") if sprint_id else ("SPRINT_ID.txt",)
    if stage == "I":
        sprint_id = _read_text(run_root / "SPRINT_ID.txt").strip()
        if not sprint_id:
            return ()
        return (f"pack/{sprint_id}_ENVELOPE.md", f"pack/{sprint_id}_ENVELOPE_REDTEAM.md")
    return STAGE_OUTPUTS[stage]


def _resolve_run(root: Path, run: str) -> Path:
    run_candidate = Path(run).expanduser()
    if not run_candidate.is_absolute():
        direct = (root / run_candidate).resolve()
        by_id = (root / "docs" / "Factory" / "runs" / run).resolve()
        run_candidate = direct if direct.exists() else by_id
    else:
        run_candidate = run_candidate.resolve()

    if not run_candidate.exists():
        raise FactoryKiloStageError(f"run root does not exist: {run_candidate}")
    if not run_candidate.is_dir():
        raise FactoryKiloStageError(f"run root is not a directory: {run_candidate}")
    return run_candidate


def _snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in root.rglob("*"):
        if _is_excluded(path):
            continue
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(root).as_posix()
            snapshot[relative] = _sha256(path)
        except OSError:
            continue
    return snapshot


def _is_excluded(path: Path) -> bool:
    return path.name in EXCLUDED_FILES or any(part in EXCLUDED_DIRS for part in path.parts)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    paths = set(before) | set(after)
    return sorted(path for path in paths if before.get(path) != after.get(path))


def _unauthorized_paths(
    *,
    changed_paths: list[str],
    allowed_writes: tuple[str, ...],
    root: Path,
    run_root: Path,
) -> list[str]:
    run_prefix = run_root.relative_to(root).as_posix()
    allowed_repo_paths = tuple(f"{run_prefix}/{allowed}" for allowed in allowed_writes)
    return [path for path in changed_paths if not _is_allowed(path, allowed_repo_paths)]


def _is_allowed(path: str, allowed_writes: tuple[str, ...]) -> bool:
    for allowed in allowed_writes:
        if path == allowed or path.startswith(f"{allowed.rstrip('/')}/"):
            return True
    return False


def _write_evidence(run_root: Path, payload: dict[str, Any]) -> Path:
    evidence_dir = run_root / "kilo_stage_runs"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = evidence_dir / f"STAGE_{payload['stage']}_{stamp}.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def _decode_timeout_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _acquire_stage_lock(run_root: Path, stage: str) -> Path:
    path = run_root / LOCK_FILENAME
    payload = {
        "stage": stage,
        "pid": os.getpid(),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError as exc:
        details = _read_text(path).strip()
        raise FactoryKiloStageError(
            f"kilo-stage lock exists: {path}. Another stage may still be running. "
            f"Inspect active Kilo processes before removing it. Lock: {details}"
        ) from exc
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, sort_keys=True)
        handle.write("\n")
    return path


def _release_stage_lock(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return


def _running_under_kilo() -> bool:
    pid = os.getppid()
    for _ in range(12):
        if pid <= 1:
            return False
        try:
            completed = subprocess.run(
                ["ps", "-o", "ppid=", "-o", "command=", "-p", str(pid)],
                text=True,
                capture_output=True,
                check=False,
            )
        except OSError:
            return False
        line = completed.stdout.strip()
        if not line:
            return False
        parts = line.split(maxsplit=1)
        if not parts:
            return False
        try:
            parent_pid = int(parts[0])
        except ValueError:
            return False
        command = parts[1] if len(parts) > 1 else ""
        command_name = Path(command.split()[0]).name if command.split() else ""
        if command_name in {"kilo", "kilocode"} or "/kilo" in command or "Kilo CLI" in command:
            return True
        pid = parent_pid
    return False
