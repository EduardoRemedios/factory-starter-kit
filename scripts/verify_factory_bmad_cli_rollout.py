#!/usr/bin/env python3
"""Read-only Claude Code CLI rollout preflight for Factory-BMAD pilots."""

from __future__ import annotations

import argparse
import json
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


EXPECTED_RELEASE = "0.2.3"
EXPECTED_BMAD = "6.10.0"
DEFAULT_CLAUDE_PREFIX = "2.1."
STATUSES = {"PASS": 0, "WARN": 1, "BLOCKED": 2}


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


def marketplace_checks(root: Path) -> list[dict[str, str]]:
    checks: list[dict[str, str]] = []
    marketplace = load_json(root / ".claude-plugin/marketplace.json")
    factory = load_json(root / "plugins/factory-claude/.claude-plugin/plugin.json")
    companion = load_json(root / "plugins/factory-bmad-claude/.claude-plugin/plugin.json")
    hooks = load_json(root / "plugins/factory-bmad-claude/hooks/hooks.json")
    source = load_json(root / "plugin-src/factory-bmad/manifest.json")

    if marketplace is None:
        checks.append(check("marketplace_manifest", "BLOCKED", "missing or invalid .claude-plugin/marketplace.json"))
    else:
        names = {item.get("name") for item in marketplace.get("plugins", []) if isinstance(item, dict)}
        status = "PASS" if {"factory", "factory-bmad"} <= names else "BLOCKED"
        checks.append(check("marketplace_manifest", status, f"plugins={sorted(name for name in names if isinstance(name, str))}"))

    versions = {
        value.get("version")
        for value in (factory, companion, source)
        if isinstance(value, dict)
    }
    dependency = companion.get("dependencies") if isinstance(companion, dict) else None
    expected_dependency = [{"name": "factory", "version": f"~{EXPECTED_RELEASE}"}]
    if versions == {EXPECTED_RELEASE} and dependency == expected_dependency:
        checks.append(check("package_versions", "PASS", f"factory/factory-bmad {EXPECTED_RELEASE} with dependency ~{EXPECTED_RELEASE}"))
    else:
        checks.append(check("package_versions", "BLOCKED", f"versions={sorted(str(item) for item in versions)} dependency={dependency!r}"))

    bmad_version = source_constant(root / "plugin-src/factory-bmad/runtime/factory_bmad.py", "BMAD_VERSION")
    if bmad_version == EXPECTED_BMAD:
        checks.append(check("bmad_pin", "PASS", f"bmad-method {EXPECTED_BMAD}"))
    else:
        checks.append(check("bmad_pin", "BLOCKED", f"expected {EXPECTED_BMAD}, found {bmad_version!r}"))

    command_values: list[str] = []
    if isinstance(hooks, dict):
        for event in ("UserPromptExpansion", "PreToolUse"):
            for entry in hooks.get("hooks", {}).get(event, []):
                for hook in entry.get("hooks", []) if isinstance(entry, dict) else []:
                    command = hook.get("command") if isinstance(hook, dict) else None
                    if isinstance(command, str):
                        command_values.append(command)
    expected = 'python3 "${CLAUDE_PLUGIN_ROOT}/scripts/factory_bmad.py" hook'
    if command_values and all(command == expected for command in command_values):
        checks.append(check("hook_command", "PASS", "Claude hook command matches packaged Factory-BMAD guard"))
    else:
        checks.append(check("hook_command", "BLOCKED", f"unexpected hook commands={command_values!r}"))
    return checks


def external_checks(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.skip_external:
        return [
            check("external_binaries", "WARN", "not checked because --skip-external was supplied"),
        ]

    checks: list[dict[str, str]] = []
    system = platform.system().lower()
    checks.append(
        check(
            "platform",
            "PASS" if system == "darwin" else "BLOCKED",
            platform.platform(),
        )
    )
    checks.append(
        check(
            "current_python",
            "PASS" if sys.version_info >= (3, 11) else "BLOCKED",
            sys.version.split()[0],
        )
    )

    hook_python = shutil.which("python3")
    if hook_python is None:
        checks.append(check("hook_python", "BLOCKED", "python3 is not on PATH"))
    else:
        probe = run_text([hook_python, "-c", "import sys; print('.'.join(map(str, sys.version_info[:3])))"], args.marketplace_root)
        version = probe.stdout.strip()
        status = "PASS" if probe.returncode == 0 and version_at_least(version, (3, 11)) else "BLOCKED"
        checks.append(check("hook_python", status, f"{hook_python} {version or probe.stderr.strip()}"))

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

    npx = shutil.which("npx")
    if npx is None:
        checks.append(check("npx", "BLOCKED", "npx is required for pinned BMAD bootstrap"))
    else:
        version = run_text([npx, "--version"], args.marketplace_root)
        checks.append(
            check(
                "npx",
                "PASS" if version.returncode == 0 else "BLOCKED",
                f"{npx} {(version.stdout or version.stderr).strip()}",
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
    parser.add_argument("--expected-claude-prefix", default=DEFAULT_CLAUDE_PREFIX)
    parser.add_argument("--skip-external", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    args.marketplace_root = args.marketplace_root.resolve()

    checks = [
        *marketplace_checks(args.marketplace_root),
        *external_checks(args),
        *target_checks(args.target_root.resolve() if args.target_root else None),
    ]
    state = summarize(checks)
    next_action = {
        "PASS": "start_or_continue_the_guided_cli_pilot",
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
