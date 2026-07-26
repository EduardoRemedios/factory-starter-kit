from __future__ import annotations

import datetime as dt
import json
import re
import uuid
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

RUNBOOKS_DIR = Path("ops/runbooks")
TASK_MEMORY_DIR = Path("artifacts/task_memory")
JOURNAL_PATH = TASK_MEMORY_DIR / "task_journal.jsonl"
REPORTS_DIR = TASK_MEMORY_DIR / "reports"

STOPWORDS = {
    "and",
    "are",
    "for",
    "from",
    "into",
    "not",
    "that",
    "the",
    "with",
    "your",
}

DEFAULT_RUNBOOKS: dict[str, dict[str, Any]] = {
    "factory_run": {
        "id": "factory_run",
        "title": "Factory Run and Stage Gates",
        "classification_keywords": [
            "factory",
            "run",
            "stage",
            "intent",
            "purple",
            "raw brief",
            "envelope",
            "pack",
        ],
        "tags": ["factory", "planning", "gates"],
        "checklist": [
            "Load context in the repository AGENTS read order before changing artifacts.",
            "Run `bash scripts/knowledge_lint.sh` and persist output where required.",
            "Preserve fail-closed behavior and schema-locked boundaries.",
            "Keep evidence chain ordering deterministic in all reports and artifacts.",
        ],
        "commands": [
            "bash scripts/knowledge_lint.sh",
            "./scripts/factoryctl stage-lint --run <RUN_ID> --stage <STAGE>",
            "./scripts/factoryctl pack-lint --run <RUN_ID>",
        ],
        "guardrails": [
            "No implicit scope expansion.",
            "If policy or contract assumptions are ambiguous, treat them as blocking.",
        ],
    },
    "sprint_close": {
        "id": "sprint_close",
        "title": "Sprint Closeout and Canonical Doc Sync",
        "classification_keywords": [
            "sprint",
            "close",
            "closeout",
            "go",
            "roadmap",
            "changelog",
            "completion report",
        ],
        "tags": ["docs", "closeout", "consistency"],
        "checklist": [
            "Confirm outcome and scope boundary in the completion report.",
            "Update project state, roadmap, and changelog in one cycle when GO closes work.",
            "Record concrete verification commands and evidence paths.",
            "Cross-link planning run and execution run artifacts where both exist.",
        ],
        "commands": [
            "rg \"Last updated|Current\" docs/PROJECT_STATE.md docs/ROADMAP.md docs/CHANGELOG.md",
        ],
        "guardrails": [
            "No stale status drift across canonical docs.",
            "Do not claim parity or production closure without evidence.",
        ],
    },
    "regression_triage": {
        "id": "regression_triage",
        "title": "Regression and Verification Triage",
        "classification_keywords": [
            "regression",
            "failing test",
            "test",
            "conformance",
            "suite",
            "failure",
            "triage",
        ],
        "tags": ["tests", "triage", "verification"],
        "checklist": [
            "Reproduce with the smallest deterministic command first.",
            "Separate product failures from test-harness or environment failures.",
            "Capture exact failing IDs and keep known-baseline failures explicit.",
            "Run targeted tests first, then broader regression if needed.",
        ],
        "commands": [
            "bash scripts/knowledge_lint.sh",
        ],
        "guardrails": [
            "Do not suppress failures without explicit baseline policy.",
            "Keep failure evidence reproducible.",
        ],
    },
    "code_change": {
        "id": "code_change",
        "title": "Code Change Delivery",
        "classification_keywords": [
            "implement",
            "fix",
            "refactor",
            "feature",
            "script",
            "workflow",
            "automation",
            "build",
        ],
        "tags": ["implementation", "quality"],
        "checklist": [
            "Lock constraints before edits.",
            "Make minimal auditable changes with explicit verification.",
            "Add or update tests for changed behavior where practical.",
            "Call out residual risks if full validation is not run.",
        ],
        "commands": [],
        "guardrails": [
            "Preserve existing behavior unless scope explicitly approves change.",
            "Avoid hidden schema or contract drift.",
        ],
    },
    "default": {
        "id": "default",
        "title": "General Task Execution",
        "classification_keywords": [],
        "tags": ["general"],
        "checklist": [
            "State assumptions explicitly.",
            "Prefer deterministic checks over implicit judgment.",
            "Leave a concise evidence trail.",
        ],
        "commands": [],
        "guardrails": [
            "Escalate ambiguity instead of guessing in high-impact paths.",
        ],
    },
}


class TaskMemoryError(RuntimeError):
    """Raised when task-memory state is invalid or incomplete."""


def _utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z0-9_\-]{3,}", text.lower())
    return [token for token in tokens if token not in STOPWORDS]


def _journal_file(root: Path) -> Path:
    return root / JOURNAL_PATH


def _runbooks_dir(root: Path) -> Path:
    return root / RUNBOOKS_DIR


def _reports_dir(root: Path) -> Path:
    return root / REPORTS_DIR


def bootstrap_task_memory(root: Path, force: bool = False) -> dict[str, Any]:
    runbook_dir = _runbooks_dir(root)
    task_memory_dir = root / TASK_MEMORY_DIR
    journal_file = _journal_file(root)

    runbook_dir.mkdir(parents=True, exist_ok=True)
    task_memory_dir.mkdir(parents=True, exist_ok=True)
    _reports_dir(root).mkdir(parents=True, exist_ok=True)

    written_runbooks: list[str] = []
    for runbook_id, runbook in DEFAULT_RUNBOOKS.items():
        target = runbook_dir / f"{runbook_id}.yaml"
        if force or not target.exists():
            target.write_text(yaml.safe_dump(runbook, sort_keys=False), encoding="utf-8")
            written_runbooks.append(str(target))

    if force and journal_file.exists():
        journal_file.write_text("", encoding="utf-8")
    elif not journal_file.exists():
        journal_file.touch()

    return {
        "timestamp_utc": _utc_now(),
        "root": str(root),
        "runbooks_written": written_runbooks,
        "journal_path": str(journal_file),
    }


def load_runbooks(root: Path) -> dict[str, dict[str, Any]]:
    runbook_dir = _runbooks_dir(root)
    if not runbook_dir.exists():
        raise TaskMemoryError("Runbook directory is missing. Run `scripts/factoryctl memory-init` first.")

    runbooks: dict[str, dict[str, Any]] = {}
    for runbook_file in sorted(runbook_dir.glob("*.y*ml")):
        payload = yaml.safe_load(runbook_file.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TaskMemoryError(f"Runbook file has invalid format: {runbook_file}")
        runbook_id = str(payload.get("id") or runbook_file.stem)
        payload["id"] = runbook_id
        payload.setdefault("title", runbook_id)
        payload.setdefault("classification_keywords", [])
        payload.setdefault("tags", [])
        payload.setdefault("checklist", [])
        payload.setdefault("commands", [])
        payload.setdefault("guardrails", [])
        runbooks[runbook_id] = payload

    if not runbooks:
        raise TaskMemoryError("No runbooks found. Run `scripts/factoryctl memory-init` to seed defaults.")
    if "default" not in runbooks:
        runbooks["default"] = DEFAULT_RUNBOOKS["default"]
    return runbooks


def load_journal(root: Path) -> list[dict[str, Any]]:
    journal_file = _journal_file(root)
    if not journal_file.exists():
        raise TaskMemoryError("Task journal is missing. Run `scripts/factoryctl memory-init` first.")

    entries: list[dict[str, Any]] = []
    for idx, line in enumerate(journal_file.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TaskMemoryError(f"Malformed JSON in task journal at line {idx}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise TaskMemoryError(f"Invalid task journal entry at line {idx}: expected object")
        entries.append(payload)
    return entries


def classify_task(task: str, runbooks: dict[str, dict[str, Any]]) -> dict[str, Any]:
    task_text = task.lower()
    best_id = "default"
    best_matches: list[str] = []

    for runbook_id, runbook in runbooks.items():
        keywords = [str(item).lower() for item in runbook.get("classification_keywords", [])]
        if not keywords:
            continue
        matches = [kw for kw in keywords if kw in task_text]
        if len(matches) > len(best_matches):
            best_id = runbook_id
            best_matches = matches

    confidence = min(0.95, 0.45 + 0.1 * len(best_matches)) if best_matches else 0.2
    return {
        "runbook_id": best_id,
        "matched_keywords": best_matches,
        "confidence": round(confidence, 2),
    }


def _top_blockers(entries: list[dict[str, Any]], runbook_id: str, max_items: int = 5) -> list[str]:
    blocker_counter: Counter[str] = Counter()
    for entry in entries:
        if entry.get("runbook_id") != runbook_id:
            continue
        if entry.get("outcome") not in {"blocked", "partial"}:
            continue
        blocker_counter.update(_tokenize(str(entry.get("notes") or "")))
    return [token for token, _ in blocker_counter.most_common(max_items)]


def suggest_task(root: Path, task: str) -> dict[str, Any]:
    runbooks = load_runbooks(root)
    entries = load_journal(root)
    classification = classify_task(task, runbooks)
    runbook = runbooks[classification["runbook_id"]]

    recent_lessons: list[dict[str, str]] = []
    for entry in reversed(entries):
        if entry.get("runbook_id") != runbook["id"] or entry.get("outcome") == "success":
            continue
        notes = str(entry.get("notes") or "").strip()
        if not notes:
            continue
        recent_lessons.append(
            {
                "timestamp_utc": str(entry.get("timestamp_utc") or ""),
                "outcome": str(entry.get("outcome") or ""),
                "notes": notes,
            }
        )
        if len(recent_lessons) >= 3:
            break

    return {
        "timestamp_utc": _utc_now(),
        "task": task,
        "classification": classification,
        "runbook": {
            "id": runbook["id"],
            "title": runbook.get("title", runbook["id"]),
            "tags": list(runbook.get("tags", [])),
            "checklist": list(runbook.get("checklist", [])),
            "commands": list(runbook.get("commands", [])),
            "guardrails": list(runbook.get("guardrails", [])),
        },
        "recent_lessons": recent_lessons,
        "top_blocker_keywords": _top_blockers(entries, runbook["id"]),
    }


def log_task(
    root: Path,
    task: str,
    outcome: str,
    notes: str,
    runbook_id: str | None = None,
    duration_minutes: int | None = None,
) -> dict[str, Any]:
    outcome = outcome.strip().lower()
    if outcome not in {"success", "partial", "blocked"}:
        raise TaskMemoryError("Outcome must be one of: success, partial, blocked")

    runbooks = load_runbooks(root)
    if runbook_id is None:
        runbook_id = classify_task(task, runbooks)["runbook_id"]
    if runbook_id not in runbooks:
        raise TaskMemoryError(f"Unknown runbook_id: {runbook_id}")

    entry = {
        "entry_id": f"TM-{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}",
        "timestamp_utc": _utc_now(),
        "task": task,
        "runbook_id": runbook_id,
        "outcome": outcome,
        "notes": notes,
        "duration_minutes": duration_minutes,
        "tags": runbooks[runbook_id].get("tags", []),
    }

    journal_file = _journal_file(root)
    with journal_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def review_task_memory(root: Path, write_report: bool = True) -> dict[str, Any]:
    runbooks = load_runbooks(root)
    entries = load_journal(root)

    summary: dict[str, dict[str, int]] = {}
    for runbook_id in runbooks:
        summary[runbook_id] = {"success": 0, "partial": 0, "blocked": 0, "total": 0}

    blocker_counter: Counter[str] = Counter()
    for entry in entries:
        runbook_id = str(entry.get("runbook_id") or "default")
        summary.setdefault(runbook_id, {"success": 0, "partial": 0, "blocked": 0, "total": 0})
        outcome = str(entry.get("outcome") or "")
        if outcome not in {"success", "partial", "blocked"}:
            continue
        summary[runbook_id][outcome] += 1
        summary[runbook_id]["total"] += 1
        if outcome in {"partial", "blocked"}:
            blocker_counter.update(_tokenize(str(entry.get("notes") or "")))

    lines = [
        "# Task Memory Review",
        "",
        f"- Generated: {_utc_now()}",
        f"- Journal entries: {len(entries)}",
        "",
        "## Runbook Summary",
        "",
        "| Runbook | Total | Success | Partial | Blocked |",
        "|---|---:|---:|---:|---:|",
    ]
    for runbook_id in sorted(summary):
        stats = summary[runbook_id]
        if stats["total"] == 0:
            continue
        lines.append(
            f"| {runbook_id} | {stats['total']} | {stats['success']} | {stats['partial']} | {stats['blocked']} |"
        )

    lines.extend(["", "## Top Blocker Keywords", ""])
    top_blockers = blocker_counter.most_common(10)
    if top_blockers:
        for keyword, count in top_blockers:
            lines.append(f"- {keyword}: {count}")
    else:
        lines.append("- none")

    report_text = "\n".join(lines) + "\n"
    report_path: str | None = None
    if write_report:
        report_dir = _reports_dir(root)
        report_dir.mkdir(parents=True, exist_ok=True)
        filename = f"TASK_MEMORY_REVIEW_{dt.datetime.now(dt.timezone.utc).strftime('%Y%m%d_%H%M%S')}.md"
        target = report_dir / filename
        target.write_text(report_text, encoding="utf-8")
        report_path = str(target)

    return {
        "timestamp_utc": _utc_now(),
        "entry_count": len(entries),
        "summary": summary,
        "top_blockers": [{"keyword": word, "count": count} for word, count in top_blockers],
        "report_path": report_path,
        "report": report_text,
    }


def format_suggestion_text(payload: dict[str, Any]) -> str:
    runbook = payload["runbook"]
    classification = payload["classification"]

    lines = [
        f"Timestamp: {payload['timestamp_utc']}",
        f"Runbook: {runbook['id']} ({runbook['title']})",
        (
            f"Classification confidence: {classification['confidence']}"
            + (
                f" | matched: {', '.join(classification['matched_keywords'])}"
                if classification["matched_keywords"]
                else ""
            )
        ),
        "",
        "Checklist:",
    ]
    for step in runbook.get("checklist", []):
        lines.append(f"- {step}")

    lines.extend(["", "Suggested commands:"])
    commands = runbook.get("commands", [])
    lines.extend([f"- {command}" for command in commands] or ["- none"])

    lines.extend(["", "Guardrails:"])
    guardrails = runbook.get("guardrails", [])
    lines.extend([f"- {guardrail}" for guardrail in guardrails] or ["- none"])

    lines.extend(["", "Recent lessons:"])
    lessons = payload.get("recent_lessons", [])
    if lessons:
        for lesson in lessons:
            lines.append(f"- [{lesson['outcome']}] {lesson['timestamp_utc']}: {lesson['notes']}")
    else:
        lines.append("- none")

    blockers = payload.get("top_blocker_keywords", [])
    lines.extend(["", "Top blocker keywords: " + (", ".join(blockers) if blockers else "none")])
    return "\n".join(lines)
