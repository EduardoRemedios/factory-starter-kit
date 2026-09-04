#!/usr/bin/env python3
"""Read-only Claude Code CLI rollout preflight for Factory-only pilots."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_CLAUDE_PREFIX = "2.1."
STATUSES = {"PASS": 0, "WARN": 1, "BLOCKED": 2}
CACHE_MARKETPLACE_NAME = "factory-starter-kit"


def check(check_id: str, status: str, detail: str) -> dict[str, str]:
    if status not in STATUSES:
        raise ValueError(f"unknown check status: {status}")
    return {"id": check_id, "status": status, "detail": detail}


def summarize(checks: list[dict[str, str]]) -> str:
    worst = max((STATUSES[item["status"]] for item in checks), default=0)
    for status, value in STATUSES.items():
        if value == worst:
            return status
    return "BLOCKED"


def run_text(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return subprocess.CompletedProcess(command, 127, "", str(error))


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def tree_entries(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(item for item in root.rglob("*") if item.is_file())
    }


def source_constant(path: Path, name: str) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(rf"^{re.escape(name)}\s*=\s*['\"]([^'\"]+)['\"]", text, re.MULTILINE)
    return match.group(1) if match else None


def version_at_least(value: str, minimum: tuple[int, int]) -> bool:
    parts = value.split(".")
    if len(parts) < 2 or not all(part.isdigit() for part in parts[:2]):
        return False
    return tuple(int(part) for part in parts[:2]) >= minimum


def claude_cache_checks(root: Path, cache_root: Path) -> list[dict[str, str]]:
    source = root / "plugins/conductor-claude"
    manifest = load_json(source / ".claude-plugin/plugin.json")
    version = manifest.get("version") if isinstance(manifest, dict) else None
    if not isinstance(version, str):
        return [
            check(
                "claude_cache_conductor",
                "BLOCKED",
                "missing source version in plugins/conductor-claude/.claude-plugin/plugin.json",
            )
        ]
    cached = cache_root / CACHE_MARKETPLACE_NAME / "conductor" / version
    if not cached.exists():
        return [
            check(
                "claude_cache_conductor",
                "PASS",
                f"no cached factory {version} under {cache_root / CACHE_MARKETPLACE_NAME}",
            )
        ]
    if not cached.is_dir():
        return [
            check(
                "claude_cache_conductor",
                "BLOCKED",
                f"{cached} is not a directory",
            )
        ]
    source_entries = tree_entries(source)
    cached_entries = tree_entries(cached)
    mismatched = [
        path for path, digest in source_entries.items() if cached_entries.get(path) != digest
    ]
    if not mismatched:
        return [
            check(
                "claude_cache_conductor",
                "PASS",
                f"cached factory {version} matches marketplace source",
            )
        ]
    return [
        check(
            "claude_cache_conductor",
            "BLOCKED",
            (
                f"cached factory {version} differs from marketplace source; "
                "uninstall factory, run `claude plugin prune`, then reinstall "
                f"from the durable checkout; mismatched={mismatched[:5]}"
            ),
        )
    ]


def marketplace_checks(root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    marketplace = load_json(root / ".claude-plugin/marketplace.json")
    source = load_json(root / "plugin-src/conductor/manifest.json")
    package = load_json(root / "plugins/conductor-claude/.claude-plugin/plugin.json")
    runtime_version = source_constant(root / "plugin-src/conductor/runtime/conductor_plugin.py", "PLUGIN_VERSION")
    source_version = source.get("version") if isinstance(source, dict) else None
    package_version = package.get("version") if isinstance(package, dict) else None

    if marketplace is None:
        checks.append(check("marketplace_manifest", "BLOCKED", "missing or invalid .claude-plugin/marketplace.json"))
    else:
        names = {item.get("name") for item in marketplace.get("plugins", []) if isinstance(item, dict)}
        checks.append(
            check(
                "marketplace_manifest",
                "PASS" if "conductor" in names else "BLOCKED",
                f"plugins={sorted(name for name in names if isinstance(name, str))}",
            )
        )

    if source_version and source_version == package_version == runtime_version:
        checks.append(check("package_versions", "PASS", f"factory {source_version}"))
    else:
        checks.append(
            check(
                "package_versions",
                "BLOCKED",
                f"source={source_version!r} package={package_version!r} runtime={runtime_version!r}",
            )
        )

    return checks


def external_checks(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.skip_external:
        return [check("external_binaries", "WARN", "not checked because --skip-external was supplied")]

    checks: list[dict[str, str]] = []
    system = platform.system().lower()
    checks.append(check("platform", "PASS" if system == "darwin" else "BLOCKED", platform.platform()))
    checks.append(
        check(
            "current_python",
            "PASS" if sys.version_info >= (3, 11) else "BLOCKED",
            sys.version.split()[0],
        )
    )

    hook_python = shutil.which("python3")
    if hook_python is None:
        checks.append(check("python3_path", "BLOCKED", "python3 is not on PATH"))
    else:
        probe = run_text([hook_python, "-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"], args.marketplace_root)
        version = probe.stdout.strip()
        status = "PASS" if probe.returncode == 0 and version_at_least(version, (3, 11)) else "BLOCKED"
        checks.append(check("python3_path", status, f"{hook_python} {version or probe.stderr.strip()}"))

    git = shutil.which("git")
    checks.append(check("git", "PASS" if git else "BLOCKED", git or "git is not on PATH"))

    claude = Path(args.claude_bin) if args.claude_bin else None
    if claude is None:
        found = shutil.which("claude")
        claude = Path(found) if found else None
    if claude is None or not claude.is_file():
        checks.append(check("claude_binary", "BLOCKED", "claude executable not found"))
    else:
        version = run_text([str(claude), "--version"], args.marketplace_root)
        observed = (version.stdout + version.stderr).strip()
        match = re.search(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", observed)
        if version.returncode != 0 or match is None:
            checks.append(check("claude_version", "BLOCKED", observed or "claude --version failed"))
        elif not match.group(0).startswith(args.expected_claude_prefix):
            checks.append(check("claude_version", "WARN", f"{match.group(0)} outside expected prefix {args.expected_claude_prefix}"))
        else:
            checks.append(check("claude_version", "PASS", match.group(0)))
        plugin = run_text([str(claude), "plugin", "--help"], args.marketplace_root)
        checks.append(
            check(
                "claude_plugin_interface",
                "PASS" if plugin.returncode == 0 else "BLOCKED",
                "available" if plugin.returncode == 0 else (plugin.stderr.strip() or plugin.stdout.strip() or "plugin help failed"),
            )
        )
    return checks


def target_checks(path: Path | None) -> list[dict[str, str]]:
    if path is None:
        return [check("target_root", "WARN", "not checked; pass --target-root for team repository preflight")]
    if path.is_symlink():
        return [check("target_root", "BLOCKED", "target root is a symlink")]
    if not path.exists():
        return [check("target_root", "PASS", "absent target is valid for Greenfield preview")]
    if not path.is_dir():
        return [check("target_root", "BLOCKED", "target root is not a directory")]
    git = run_text(["git", "-C", str(path), "rev-parse", "--show-toplevel"], path)
    if git.returncode != 0:
        entries = sorted(item.name for item in path.iterdir())
        status = "PASS" if not entries else "WARN"
        detail = "empty existing directory" if not entries else f"non-git directory entries={entries[:10]}"
        return [check("target_root", status, detail)]
    status = run_text(["git", "-C", str(path), "status", "--short"], path)
    clean = status.returncode == 0 and not status.stdout.strip()
    return [
        check("target_root", "PASS", f"git worktree {git.stdout.strip()}"),
        check("target_git_status", "PASS" if clean else "WARN", "clean" if clean else "dirty; preserve current work and expect plan churn"),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--marketplace-root", type=Path, default=Path.cwd())
    parser.add_argument("--target-root", type=Path)
    parser.add_argument("--claude-bin")
    parser.add_argument(
        "--claude-cache-root",
        type=Path,
        default=Path.home() / ".claude/plugins/cache",
    )
    parser.add_argument("--expected-claude-prefix", default=DEFAULT_CLAUDE_PREFIX)
    parser.add_argument("--skip-external", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    args.marketplace_root = args.marketplace_root.resolve()

    checks = [
        *marketplace_checks(args.marketplace_root),
        *claude_cache_checks(args.marketplace_root, args.claude_cache_root.expanduser()),
        *external_checks(args),
        *target_checks(args.target_root.resolve() if args.target_root else None),
    ]
    state = summarize(checks)
    next_action = {
        "PASS": "start_or_continue_the_factory_cli_pilot",
        "WARN": "review_warnings_before_user_pilot",
        "BLOCKED": "fix_blockers_before_user_pilot",
    }[state]
    payload = {
        "schema_version": 1,
        "state": state,
        "next_action": next_action,
        "checks": checks,
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"state: {state}")
        print(f"next_action: {next_action}")
        for item in checks:
            print(f"{item['status']:7} {item['id']}: {item['detail']}")
    return 1 if state == "BLOCKED" else 0


if __name__ == "__main__":
    raise SystemExit(main())
