from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence


REPORT_NAMES = (
    "REPO_CARTOGRAPHY_REPORT.md",
    "CANON_DRIFT_REPORT.md",
    "VERIFICATION_STATUS_REPORT.md",
    "TRACEABILITY_REPORT.md",
    "OPERATIONAL_SNAPSHOT.md",
)

CANONICAL_DOCS = (
    "AGENTS.md",
    "docs/PROJECT_STATE.md",
    "docs/ROADMAP.md",
    "docs/CHANGELOG.md",
)

APPROVED_VERIFICATION_COMMANDS: dict[str, tuple[str, ...]] = {
    "knowledge_lint": ("bash", "scripts/knowledge_lint.sh"),
    "factoryctl_help": ("./scripts/factoryctl", "--help"),
}


@dataclass(frozen=True)
class Finding:
    id: str
    severity: str
    confidence: str
    source_paths: tuple[str, ...]
    commit: str
    reason: str


@dataclass
class ScanResult:
    metadata: dict[str, object]
    output_dir: Path
    reports: dict[str, Path] = field(default_factory=dict)
    findings: list[Finding] = field(default_factory=list)
    verification_results: dict[str, dict[str, object]] = field(default_factory=dict)


def run_scan(
    root: Path | str = ".",
    output_root: Path | str | None = None,
    scan_mode: str = "READ_ONLY",
    execute_verification: bool = False,
    verification_commands: Sequence[str] | None = None,
) -> ScanResult:
    """Run a manual advisory scan and write timestamped markdown reports."""

    repo_root = Path(root).resolve()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination_root = Path(output_root).resolve() if output_root else repo_root / "artifacts" / "cartographer"
    output_dir = destination_root / timestamp
    output_dir.mkdir(parents=True, exist_ok=True)

    scanned_commit = _git(repo_root, "rev-parse", "HEAD") or "UNKNOWN"
    short_commit = _git(repo_root, "rev-parse", "--short", "HEAD") or scanned_commit[:12]
    failed_steps: list[str] = []
    skipped_paths: list[str] = []
    verification_results: dict[str, dict[str, object]] = {}

    topology = _scan_topology(repo_root)
    canon = _scan_canon(repo_root)
    verification = _harvest_verification(repo_root)
    traceability = _scan_traceability(repo_root)

    if execute_verification:
        selected = tuple(verification_commands or ("knowledge_lint",))
        verification_results = _run_verification_commands(repo_root, selected)
        failed_steps.extend(
            name for name, result in verification_results.items() if result["status"] != "PASS"
        )
        skipped_paths.extend(
            f"verification_command:{name}"
            for name in sorted(set(APPROVED_VERIFICATION_COMMANDS) - set(selected))
        )
    else:
        skipped_paths.append("verification_command_execution")

    findings = _build_findings(
        repo_root=repo_root,
        commit=scanned_commit,
        canon=canon,
        verification=verification,
        traceability=traceability,
    )

    coverage_status = _classify_coverage(
        execute_verification=execute_verification,
        verification_results=verification_results,
        failed_steps=failed_steps,
        skipped_paths=skipped_paths,
    )
    confidence_level = _classify_confidence(scanned_commit, coverage_status)
    metadata: dict[str, object] = {
        "cartography_metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "scanned_commit": scanned_commit,
            "scan_mode": scan_mode,
            "coverage_status": coverage_status,
            "confidence_level": confidence_level,
            "failed_steps": failed_steps,
            "skipped_paths": skipped_paths,
        }
    }

    result = ScanResult(
        metadata=metadata,
        output_dir=output_dir,
        findings=findings,
        verification_results=verification_results,
    )

    report_payloads = {
        "REPO_CARTOGRAPHY_REPORT.md": _repo_report(metadata, topology, short_commit),
        "CANON_DRIFT_REPORT.md": _canon_report(metadata, canon, findings),
        "VERIFICATION_STATUS_REPORT.md": _verification_report(
            metadata, verification, verification_results, execute_verification
        ),
        "TRACEABILITY_REPORT.md": _traceability_report(metadata, traceability, findings),
        "OPERATIONAL_SNAPSHOT.md": _snapshot_report(
            metadata, topology, canon, verification, findings, short_commit
        ),
    }

    for name, text in report_payloads.items():
        path = output_dir / name
        path.write_text(text, encoding="utf-8")
        result.reports[name] = path

    return result


def _classify_coverage(
    *,
    execute_verification: bool,
    verification_results: dict[str, dict[str, object]],
    failed_steps: Sequence[str],
    skipped_paths: Sequence[str],
) -> str:
    if failed_steps:
        return "DEGRADED"
    if not execute_verification:
        return "PARTIAL"
    expected = set(APPROVED_VERIFICATION_COMMANDS)
    passed = {name for name, result in verification_results.items() if result.get("status") == "PASS"}
    if expected <= passed and not skipped_paths:
        return "COMPLETE"
    return "PARTIAL"


def _classify_confidence(scanned_commit: str, coverage_status: str) -> str:
    if scanned_commit == "UNKNOWN":
        return "LOW"
    if coverage_status == "COMPLETE":
        return "HIGH"
    return "MEDIUM"


def _git(root: Path, *args: str) -> str | None:
    try:
        completed = subprocess.run(
            ("git", *args),
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def _scan_topology(root: Path) -> dict[str, object]:
    top_level_dirs = sorted(
        item.name
        for item in root.iterdir()
        if item.is_dir() and not item.name.startswith(".") and item.name != "__pycache__"
    )
    python_files = [path for path in root.rglob("*.py") if _is_scannable(path)]
    tests = [path for path in (root / "tests").glob("test_*.py")] if (root / "tests").exists() else []
    factory_runs = list((root / "docs/Factory/runs").glob("RUN_*")) if (root / "docs/Factory/runs").exists() else []
    return {
        "top_level_dirs": top_level_dirs,
        "python_file_count": len(python_files),
        "test_file_count": len(tests),
        "factory_run_count": len(factory_runs),
        "scripts_present": (root / "scripts").exists(),
        "docs_present": (root / "docs").exists(),
        "factory_present": (root / "docs/Factory").exists(),
    }


def _scan_canon(root: Path) -> dict[str, object]:
    docs: dict[str, dict[str, object]] = {}
    missing: list[str] = []
    for rel in CANONICAL_DOCS:
        path = root / rel
        if not path.exists():
            missing.append(rel)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        docs[rel] = {
            "bytes": path.stat().st_size,
            "last_updated_lines": [
                line.strip() for line in text.splitlines() if "Last updated" in line
            ][:3],
            "mentions_planning_only": "PLANNING_ONLY" in text,
            "mentions_factory": "Factory" in text or "factory" in text,
        }
    return {"docs": docs, "missing": missing}


def _harvest_verification(root: Path) -> dict[str, object]:
    latest_preflight = _latest_merge_preflight(root)
    return {
        "latest_merge_preflight": str(latest_preflight.relative_to(root)) if latest_preflight else None,
        "knowledge_lint_present": (root / "scripts/knowledge_lint.sh").exists(),
        "factoryctl_present": (root / "scripts/factoryctl").exists(),
        "known_failures_count": _count_data_lines(root / "tests/KNOWN_FAILURES.txt"),
        "merge_gate_excludes_count": _count_data_lines(root / "tests/MERGE_GATE_EXCLUDES.txt"),
    }


def _scan_traceability(root: Path) -> dict[str, object]:
    factory_runs = root / "docs/Factory/runs"
    traceability_files = list(factory_runs.rglob("traceability_matrix.md")) if factory_runs.exists() else []
    verification_plans = list(factory_runs.rglob("verification_plan.md")) if factory_runs.exists() else []
    manifests = list(factory_runs.rglob("verification_manifest.yaml")) if factory_runs.exists() else []
    return {
        "traceability_matrix_count": len(traceability_files),
        "verification_plan_count": len(verification_plans),
        "verification_manifest_count": len(manifests),
    }


def _run_verification_commands(root: Path, selected: Iterable[str]) -> dict[str, dict[str, object]]:
    results: dict[str, dict[str, object]] = {}
    for name in selected:
        command = APPROVED_VERIFICATION_COMMANDS.get(name)
        if command is None:
            results[name] = {"status": "SKIPPED", "reason": "command_not_approved"}
            continue
        completed = subprocess.run(
            command,
            cwd=root,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        results[name] = {
            "status": "PASS" if completed.returncode == 0 else "FAIL",
            "returncode": completed.returncode,
            "command": " ".join(command),
            "output_preview": completed.stdout[-1200:],
        }
    return results


def _build_findings(
    repo_root: Path,
    commit: str,
    canon: dict[str, object],
    verification: dict[str, object],
    traceability: dict[str, object],
) -> list[Finding]:
    findings: list[Finding] = []
    missing = tuple(canon.get("missing", ()))
    if missing:
        findings.append(
            Finding(
                id="CANON-MISSING-001",
                severity="HIGH",
                confidence="HIGH",
                source_paths=missing,
                commit=commit,
                reason="One or more canonical status documents are missing.",
            )
        )
    if not verification.get("latest_merge_preflight"):
        findings.append(
            Finding(
                id="VERIFY-EVIDENCE-001",
                severity="INFO",
                confidence="MEDIUM",
                source_paths=("artifacts/merge_preflight/",),
                commit=commit,
                reason="No latest merge preflight summary was found to harvest.",
            )
        )
    if int(traceability.get("traceability_matrix_count", 0)) == 0:
        findings.append(
            Finding(
                id="TRACE-MATRIX-001",
                severity="INFO",
                confidence="HIGH",
                source_paths=("docs/Factory/runs/",),
                commit=commit,
                reason="No Factory traceability matrices were found; this is expected in a fresh starter kit.",
            )
        )
    if not findings:
        findings.append(
            Finding(
                id="INFO-SCAN-001",
                severity="INFO",
                confidence="MEDIUM",
                source_paths=tuple(path for path in CANONICAL_DOCS if (repo_root / path).exists()),
                commit=commit,
                reason="Manual v0 scan completed with no high-signal generated drift finding.",
            )
        )
    return findings


def _latest_merge_preflight(root: Path) -> Path | None:
    latest = root / "artifacts/merge_preflight/LATEST_RUN.txt"
    if latest.exists():
        value = latest.read_text(encoding="utf-8").strip()
        if value:
            path = root / value / "SUMMARY.md"
            if path.exists():
                return path
    base = root / "artifacts/merge_preflight"
    if not base.exists():
        return None
    summaries = sorted(base.glob("*/SUMMARY.md"), key=lambda path: path.stat().st_mtime, reverse=True)
    return summaries[0] if summaries else None


def _count_data_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#"))


def _is_scannable(path: Path) -> bool:
    parts = set(path.parts)
    return "__pycache__" not in parts and ".git" not in parts and "node_modules" not in parts


def _metadata_block(metadata: dict[str, object]) -> str:
    return "```json\n" + json.dumps(metadata, indent=2) + "\n```\n"


def _findings_block(findings: Sequence[Finding]) -> str:
    lines: list[str] = []
    for finding in findings:
        lines.extend(
            [
                f"## Finding {finding.id}",
                f"- Severity: {finding.severity}",
                f"- Confidence: {finding.confidence}",
                f"- Commit: {finding.commit}",
                f"- Evidence: {', '.join(finding.source_paths) or 'none'}",
                f"- Reason: {finding.reason}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _repo_report(metadata: dict[str, object], topology: dict[str, object], short_commit: str) -> str:
    return (
        "# Repo Cartography Report\n\n"
        "Advisory report only. Repository artifacts remain canonical.\n\n"
        f"{_metadata_block(metadata)}\n"
        f"- Scanned commit: {short_commit}\n"
        f"- Top-level directories: {', '.join(topology['top_level_dirs'])}\n"
        f"- Python files: {topology['python_file_count']}\n"
        f"- Test files: {topology['test_file_count']}\n"
        f"- Factory runs: {topology['factory_run_count']}\n"
        f"- Scripts/docs/Factory present: {topology['scripts_present']}/{topology['docs_present']}/{topology['factory_present']}\n"
    )


def _canon_report(metadata: dict[str, object], canon: dict[str, object], findings: Sequence[Finding]) -> str:
    lines = ["# Canon Drift Report", "", "Advisory report only. Human-approved docs remain canonical.", "", _metadata_block(metadata)]
    docs = canon["docs"]
    for rel, info in docs.items():
        lines.append(f"## {rel}")
        lines.append(f"- Bytes: {info['bytes']}")
        lines.append(f"- Last-updated lines: {info['last_updated_lines'] or ['not found']}")
        lines.append("")
    lines.append(_findings_block([finding for finding in findings if finding.id.startswith(("CANON", "INFO"))]))
    return "\n".join(lines)


def _verification_report(
    metadata: dict[str, object],
    verification: dict[str, object],
    verification_results: dict[str, dict[str, object]],
    executed: bool,
) -> str:
    return (
        "# Verification Status Report\n\n"
        "Advisory report only. Merge and Factory gates remain authoritative.\n\n"
        f"{_metadata_block(metadata)}\n"
        f"- Existing merge preflight summary: {verification['latest_merge_preflight'] or 'not found'}\n"
        f"- Knowledge lint script present: {verification['knowledge_lint_present']}\n"
        f"- Factoryctl present: {verification['factoryctl_present']}\n"
        f"- Known failure entries: {verification['known_failures_count']}\n"
        f"- Merge gate exclude entries: {verification['merge_gate_excludes_count']}\n"
        f"- Verification commands executed in this scan: {executed}\n"
        "- Coverage status interpretation: COMPLETE means every approved starter-kit verification command "
        "was executed and passed; deployment remains a separate unassessed state.\n"
        f"- Command results: {json.dumps(verification_results, indent=2)}\n"
    )


def _traceability_report(
    metadata: dict[str, object], traceability: dict[str, object], findings: Sequence[Finding]
) -> str:
    return (
        "# Traceability Report\n\n"
        "Advisory report only. Factory packs remain source evidence.\n\n"
        f"{_metadata_block(metadata)}\n"
        f"- Traceability matrices found: {traceability['traceability_matrix_count']}\n"
        f"- Verification plans found: {traceability['verification_plan_count']}\n"
        f"- Verification manifests found: {traceability['verification_manifest_count']}\n\n"
        f"{_findings_block([finding for finding in findings if finding.id.startswith(('TRACE', 'INFO'))])}"
    )


def _snapshot_report(
    metadata: dict[str, object],
    topology: dict[str, object],
    canon: dict[str, object],
    verification: dict[str, object],
    findings: Sequence[Finding],
    short_commit: str,
) -> str:
    return (
        "# Operational Snapshot\n\n"
        "Advisory report only. Do not treat this snapshot as canonical truth.\n\n"
        f"{_metadata_block(metadata)}\n"
        "## Repository State\n"
        f"- Commit: {short_commit}\n"
        f"- Scripts/docs/Factory present: {topology['scripts_present']}/{topology['docs_present']}/{topology['factory_present']}\n\n"
        "## Verification State\n"
        f"- Latest merge preflight: {verification['latest_merge_preflight'] or 'not found'}\n"
        f"- Knowledge lint script present: {verification['knowledge_lint_present']}\n\n"
        "## Deployment State\n"
        "- Not assessed by Cartographer v0.\n"
        "- A COMPLETE repository verification scan does not imply deployment health.\n\n"
        "## Recommended Human Review\n"
        f"- Review findings count: {len(findings)}\n"
        "- Decide whether reviewed snapshots should be published to a dashboard or collaboration channel.\n\n"
        f"{_findings_block(findings)}"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate advisory repo cartography reports.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--output-root", default=None, help="Output root. Defaults to artifacts/cartographer.")
    parser.add_argument(
        "--execute-verification",
        action="store_true",
        help="Opt in to approved verification command execution.",
    )
    parser.add_argument(
        "--verification-command",
        action="append",
        choices=sorted(APPROVED_VERIFICATION_COMMANDS),
        help="Approved verification command to run when --execute-verification is set.",
    )
    args = parser.parse_args(argv)

    result = run_scan(
        root=args.root,
        output_root=args.output_root,
        execute_verification=args.execute_verification,
        verification_commands=args.verification_command,
    )
    print(f"cartographer: output_dir={result.output_dir}")
    for name, path in sorted(result.reports.items()):
        print(f"cartographer: report={name} path={path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
