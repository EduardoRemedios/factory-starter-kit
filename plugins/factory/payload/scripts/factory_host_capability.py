#!/usr/bin/env python3
"""Validate or discover schema-locked Factory host capabilities."""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
from pathlib import Path
from typing import Any, Sequence


SCHEMA_VERSION = 1
ARTIFACT_NAME = "host_capabilities.json"
POSTURES = {"VERIFIED_LOCAL", "DEFERRED_TARGET"}
KINDS = {"executable_file", "file", "directory"}
CAPABILITY_ID = re.compile(r"^[a-z][a-z0-9_]*$")
TOP_LEVEL_KEYS = {"schema_version", "run_id", "posture", "host", "capabilities"}
HOST_KEYS = {"system", "machine"}
CAPABILITY_KEYS = {"id", "path", "kind"}


def host_identity() -> dict[str, str]:
    return {"system": platform.system(), "machine": platform.machine()}


def artifact_path(root: Path, run_id: str) -> Path:
    return root / "docs" / "Factory" / "runs" / run_id / "pack" / ARTIFACT_NAME


def _result(
    *,
    status: str,
    reason_code: str,
    run_id: str,
    posture: str | None = None,
    capability_count: int = 0,
    errors: Sequence[str] = (),
    path: Path | None = None,
) -> dict[str, Any]:
    return {
        "status": status,
        "reason_code": reason_code,
        "run_id": run_id,
        "posture": posture,
        "capability_count": capability_count,
        "errors": list(errors)[:20],
        "artifact_path": path.as_posix() if path is not None else None,
        "mutations": [],
    }


def _normalized_absolute(value: str) -> bool:
    candidate = Path(value)
    return candidate.is_absolute() and os.path.normpath(value) == value


def _capability_error(entry: dict[str, Any]) -> str | None:
    path = Path(entry["path"])
    if not path.exists():
        return f"{entry['id']}:PATH_MISSING"
    if entry["kind"] == "directory":
        return None if path.is_dir() else f"{entry['id']}:KIND_MISMATCH"
    if not path.is_file():
        return f"{entry['id']}:KIND_MISMATCH"
    if entry["kind"] == "executable_file" and not os.access(path, os.X_OK):
        return f"{entry['id']}:NOT_EXECUTABLE"
    return None


def validate_document(
    document: Any,
    *,
    run_id: str,
    current_host: dict[str, str] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITY_SCHEMA_INVALID",
            run_id=run_id,
            errors=["DOCUMENT_NOT_OBJECT"],
        )
    if set(document) != TOP_LEVEL_KEYS:
        errors.append("TOP_LEVEL_KEYS_INVALID")
    if document.get("schema_version") != SCHEMA_VERSION:
        errors.append("SCHEMA_VERSION_INVALID")
    if document.get("run_id") != run_id:
        errors.append("RUN_ID_MISMATCH")

    posture = document.get("posture")
    if posture not in POSTURES:
        errors.append("POSTURE_INVALID")

    host = document.get("host")
    if not isinstance(host, dict) or set(host) != HOST_KEYS:
        errors.append("HOST_SCHEMA_INVALID")
    elif not all(isinstance(host.get(key), str) and host[key].strip() for key in HOST_KEYS):
        errors.append("HOST_VALUE_INVALID")

    capabilities = document.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("CAPABILITIES_INVALID")
        capabilities = []

    seen: set[str] = set()
    valid_entries: list[dict[str, Any]] = []
    for index, entry in enumerate(capabilities):
        label = f"CAPABILITY_{index + 1}"
        if not isinstance(entry, dict) or set(entry) != CAPABILITY_KEYS:
            errors.append(f"{label}_SCHEMA_INVALID")
            continue
        capability_id = entry.get("id")
        path_value = entry.get("path")
        kind = entry.get("kind")
        if not isinstance(capability_id, str) or not CAPABILITY_ID.fullmatch(capability_id):
            errors.append(f"{label}_ID_INVALID")
        elif capability_id in seen:
            errors.append(f"{label}_ID_DUPLICATE")
        else:
            seen.add(capability_id)
        if not isinstance(path_value, str) or not _normalized_absolute(path_value):
            errors.append(f"{label}_PATH_INVALID")
        if kind not in KINDS:
            errors.append(f"{label}_KIND_INVALID")
        if (
            isinstance(capability_id, str)
            and CAPABILITY_ID.fullmatch(capability_id)
            and capability_id in seen
            and isinstance(path_value, str)
            and _normalized_absolute(path_value)
            and kind in KINDS
        ):
            valid_entries.append(entry)

    if errors:
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITY_SCHEMA_INVALID",
            run_id=run_id,
            posture=posture if isinstance(posture, str) else None,
            capability_count=len(capabilities),
            errors=errors,
        )
    if posture == "DEFERRED_TARGET":
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITIES_DEFERRED_TARGET",
            run_id=run_id,
            posture=posture,
            capability_count=len(valid_entries),
        )

    current = current_host or host_identity()
    if host != current:
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITY_HOST_MISMATCH",
            run_id=run_id,
            posture=posture,
            capability_count=len(valid_entries),
        )

    capability_errors = [error for entry in valid_entries if (error := _capability_error(entry))]
    if capability_errors:
        reason_code = "FACTORY_HOST_CAPABILITY_PATH_MISSING"
        if any("KIND_MISMATCH" in item for item in capability_errors):
            reason_code = "FACTORY_HOST_CAPABILITY_KIND_MISMATCH"
        elif any("NOT_EXECUTABLE" in item for item in capability_errors):
            reason_code = "FACTORY_HOST_CAPABILITY_NOT_EXECUTABLE"
        return _result(
            status="BLOCKED",
            reason_code=reason_code,
            run_id=run_id,
            posture=posture,
            capability_count=len(valid_entries),
            errors=capability_errors,
        )
    return _result(
        status="PASS",
        reason_code="FACTORY_HOST_CAPABILITIES_VALID",
        run_id=run_id,
        posture=posture,
        capability_count=len(valid_entries),
    )


def validate_artifact(root: Path, run_id: str) -> dict[str, Any]:
    path = artifact_path(root, run_id)
    if not path.is_file():
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITIES_MISSING",
            run_id=run_id,
            path=path.relative_to(root),
        )
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITY_SCHEMA_INVALID",
            run_id=run_id,
            errors=["ARTIFACT_UNREADABLE"],
            path=path.relative_to(root),
        )
    result = validate_document(document, run_id=run_id)
    return {**result, "artifact_path": path.relative_to(root).as_posix()}


def discover_artifact(
    root: Path,
    run_id: str,
    requirements: Sequence[Sequence[str]],
    output: str,
) -> dict[str, Any]:
    run_root = root / "docs" / "Factory" / "runs" / run_id
    expected = run_root / "pack" / ARTIFACT_NAME
    candidate = run_root / output
    if candidate != expected or candidate.is_symlink() or not candidate.parent.is_dir():
        return _result(
            status="BLOCKED",
            reason_code="FACTORY_HOST_CAPABILITY_OUTPUT_INVALID",
            run_id=run_id,
            path=expected.relative_to(root),
        )
    capabilities = [
        {"id": values[0], "kind": values[1], "path": values[2]}
        for values in requirements
    ]
    document = {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "posture": "VERIFIED_LOCAL",
        "host": host_identity(),
        "capabilities": capabilities,
    }
    result = validate_document(document, run_id=run_id)
    if result["status"] != "PASS":
        return {**result, "artifact_path": expected.relative_to(root).as_posix()}
    expected.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        **result,
        "artifact_path": expected.relative_to(root).as_posix(),
        "mutations": [expected.relative_to(root).as_posix()],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate or discover Factory host capabilities.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--run", required=True)
    parser.add_argument("--discover", action="store_true")
    parser.add_argument("--require", action="append", nargs=3, default=[])
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).resolve()
    if args.discover:
        if not args.require or not args.output:
            payload = _result(
                status="BLOCKED",
                reason_code="FACTORY_HOST_CAPABILITY_DISCOVERY_ARGUMENTS_INVALID",
                run_id=args.run,
            )
        else:
            payload = discover_artifact(root, args.run, args.require, args.output)
    else:
        payload = validate_artifact(root, args.run)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
