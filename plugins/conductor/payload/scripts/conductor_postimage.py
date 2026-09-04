"""Conductor protected-postimage compare.

    postimage capture  --run RUN_ID [--root PATH ...]   digest every file under the protected roots
    postimage compare  --run RUN_ID                     recompute and diff against the capture

Protected roots come from --root, else PROJECT_CONFIG.json protected_roots, else the
Conductor defaults. The run's own directory is always excluded because G2 legitimately
writes there. Output: docs/Conductor/runs/<RUN_ID>/postimage/{preimage,compare}.json.
Harvested from the MS-01 protected-postimage comparison of the Factory lineage.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from conductor_contract_lint import PROJECT_CONFIG, RUNS_DIR, ContractLintError, safe_run_root, sha256_file

DEFAULT_ROOTS = ["docs/Conductor", "scripts", ".agents/skills", "AGENTS.md"]
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_roots(root: Path, explicit: list[str] | None) -> list[str]:
    if explicit:
        return sorted(set(explicit))
    config_path = root / PROJECT_CONFIG
    if config_path.is_file():
        try:
            roots = json.loads(config_path.read_text(encoding="utf-8")).get("protected_roots")
            if isinstance(roots, list) and roots:
                return sorted(set(str(r) for r in roots))
        except (OSError, json.JSONDecodeError):
            pass
    return DEFAULT_ROOTS


def digest_tree(root: Path, roots: list[str], exclude: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for rel in roots:
        base = root / rel
        if base.is_symlink():
            raise ContractLintError("CONDUCTOR_POSTIMAGE_SYMLINK_ROOT", rel)
        if base.is_file():
            files[rel] = sha256_file(base)
            continue
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                continue
            if exclude in path.parents or path == exclude:
                continue
            if path.is_symlink():
                raise ContractLintError("CONDUCTOR_POSTIMAGE_SYMLINK", path.relative_to(root).as_posix())
            if path.is_file():
                files[path.relative_to(root).as_posix()] = sha256_file(path)
    return files


def capture(root: Path, run_id: str, roots: list[str] | None = None) -> dict[str, Any]:
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    resolved = resolve_roots(root, roots)
    files = digest_tree(root, resolved, run_root.resolve())
    payload = {"schema_version": 1, "run_id": run_id, "protected_roots": resolved, "files": files,
               "file_count": len(files), "captured_utc": utc_now()}
    out = run_root / "postimage"
    out.mkdir(parents=True, exist_ok=True)
    (out / "preimage.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {k: v for k, v in payload.items() if k != "files"} | {"preimage": (RUNS_DIR / run_id / "postimage/preimage.json").as_posix()}


def compare(root: Path, run_id: str) -> dict[str, Any]:
    root = root.resolve()
    run_root = safe_run_root(root, run_id)
    pre_path = run_root / "postimage" / "preimage.json"
    if not pre_path.is_file():
        raise ContractLintError("CONDUCTOR_POSTIMAGE_PREIMAGE_MISSING", pre_path.as_posix())
    pre = json.loads(pre_path.read_text(encoding="utf-8"))
    post = digest_tree(root, pre["protected_roots"], run_root.resolve())
    before, after = pre["files"], post
    changed = sorted(p for p in before if p in after and before[p] != after[p])
    removed = sorted(p for p in before if p not in after)
    added = sorted(p for p in after if p not in before)
    status = "PASS" if not (changed or removed or added) else "FAIL"
    payload = {"schema_version": 1, "run_id": run_id, "protected_roots": pre["protected_roots"], "status": status,
               "changed": changed, "removed": removed, "added": added, "compared_utc": utc_now(),
               "preimage_file_count": len(before), "postimage_file_count": len(after)}
    (run_root / "postimage" / "compare.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return payload
