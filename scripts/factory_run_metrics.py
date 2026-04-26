from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


class FactoryRunMetricsError(Exception):
    """Raised when run metrics cannot be initialized."""


def init_run_metrics(root: Path, run: str, force: bool = False) -> dict[str, Any]:
    run_root = _resolve_run(root=root, run=run)
    template_path = root / "docs" / "Factory" / "templates" / "RUN_METRICS_TEMPLATE.md"
    output_path = run_root / "RUN_METRICS.md"

    if not template_path.is_file() or template_path.stat().st_size == 0:
        raise FactoryRunMetricsError(f"run metrics template missing or empty: {template_path}")
    if output_path.exists() and not force:
        raise FactoryRunMetricsError(f"RUN_METRICS.md already exists; use --force to overwrite: {output_path}")

    text = template_path.read_text(encoding="utf-8")
    sprint_id = _read_text(run_root / "SPRINT_ID.txt").strip()
    execution_mode = _read_text(run_root / "EXECUTION_MODE.txt").strip()

    replacements = {
        "v1 (YYYY-MM-DD): Initial run metrics record.": (
            f"v1 ({date.today().isoformat()}): Initial run metrics record."
        ),
        "- Run ID:": f"- Run ID: {run_root.name}",
        "- Sprint ID:": f"- Sprint ID: {sprint_id}" if sprint_id else "- Sprint ID:",
        "- Execution Mode: PLANNING_ONLY | EXECUTION_ENABLED": (
            f"- Execution Mode: {execution_mode}"
            if execution_mode in {"PLANNING_ONLY", "EXECUTION_ENABLED"}
            else "- Execution Mode: PLANNING_ONLY | EXECUTION_ENABLED"
        ),
    }
    for old, new in replacements.items():
        text = text.replace(old, new, 1)

    output_path.write_text(text, encoding="utf-8")
    return {
        "status": "created" if not force else "written",
        "run_root": str(run_root),
        "output_path": str(output_path),
        "template_path": str(template_path),
        "sprint_id": sprint_id,
        "execution_mode": execution_mode,
        "force": force,
    }


def format_run_metrics(payload: dict[str, Any]) -> str:
    lines = [
        f"run_metrics: {payload['status']}",
        f"run_root={payload['run_root']}",
        f"output_path={payload['output_path']}",
    ]
    if payload.get("sprint_id"):
        lines.append(f"sprint_id={payload['sprint_id']}")
    if payload.get("execution_mode"):
        lines.append(f"execution_mode={payload['execution_mode']}")
    return "\n".join(lines) + "\n"


def _resolve_run(root: Path, run: str) -> Path:
    run_candidate = Path(run).expanduser()
    if not run_candidate.is_absolute():
        direct = (root / run_candidate).resolve()
        by_id = (root / "docs" / "Factory" / "runs" / run).resolve()
        run_candidate = direct if direct.exists() else by_id
    else:
        run_candidate = run_candidate.resolve()

    if not run_candidate.exists():
        raise FactoryRunMetricsError(f"run root does not exist: {run_candidate}")
    if not run_candidate.is_dir():
        raise FactoryRunMetricsError(f"run root is not a directory: {run_candidate}")
    return run_candidate


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)
