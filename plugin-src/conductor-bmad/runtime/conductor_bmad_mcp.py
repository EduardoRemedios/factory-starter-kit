#!/usr/bin/env python3
"""Read-only BMAD workflow loading over MCP; each invocation is independently gated."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
import conductor_bmad_policy as policy


TOOL = {
    "name": "load_workflow",
    "description": "Load one named BMAD workflow through Factory lane policy. Delivery and unknown workflows are denied before instructions are returned. Every nested workflow must use this tool again. This does not authorize execution, promotion, or full Codex BMAD adoption.",
    "inputSchema": {
        "type": "object", "additionalProperties": False,
        "properties": {
            "root": {"type": "string", "description": "Absolute path to the current project root."},
            "name": {"type": "string", "description": "Exact BMAD skill name, for example bmad-help."},
        },
        "required": ["root", "name"],
    },
    "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
}


def denied(code: str) -> dict[str, Any]:
    return {"state": "BLOCKED", "reason_code": code}


def load_workflow(arguments: Any) -> dict[str, Any]:
    if not isinstance(arguments, dict) or set(arguments) != {"root", "name"}:
        return denied("CONDUCTOR_BMAD_LOADER_INPUT_INVALID")
    name, raw_root = arguments["name"], arguments["root"]
    if not isinstance(name, str) or not re.fullmatch(r"bmad-[a-z0-9-]+", name):
        return denied("CONDUCTOR_BMAD_LOADER_INPUT_INVALID")
    if not isinstance(raw_root, str) or not raw_root or not Path(raw_root).is_absolute():
        return denied("CONDUCTOR_BMAD_LOADER_INPUT_INVALID")
    verdict = policy.policy_classify(name)
    if not verdict["allowed"]:
        return denied(verdict["reason_code"])
    try:
        root = Path(raw_root).resolve(strict=True)
        audit = policy.inventory_audit(root, "codex")
        if audit["state"] != "READY":
            return denied(audit["reason_code"])
        if any(policy._regular_file(root, policy.skill_directory(root) / installed / "SKILL.md") is None
               for installed in policy.supported_skills(audit["installation_version"])):
            return denied("CONDUCTOR_BMAD_CAPABILITY_INCOMPLETE")
        if name in policy.SOLUTION_CONTEXT_AUTHORING_WORKFLOWS or audit["installation_version"] == "6.12.1-next.0":
            authorization = policy.solution_context_authorization(root, name)
            if not authorization["allowed"]:
                return denied(authorization["reason_code"])
            context = policy.bound_context(root, name)
        else:
            context = policy.bound_context(root, name)
        relative = policy.skill_directory(root) / name / "SKILL.md"
        skill = policy._regular_file(root, relative)
        if skill is None:
            return denied("CONDUCTOR_BMAD_LOADER_SKILL_UNSAFE_OR_MISSING")
        content = skill.read_bytes()
        # Recheck the same bytes returned to the model for qualified solution profiles.
        digest = hashlib.sha256(content).hexdigest()
        if (name in policy.SOLUTION_CONTEXT_AUTHORING_WORKFLOWS or audit["installation_version"] == "6.12.1-next.0") and digest != authorization["skill_sha256"]:
            return denied("CONDUCTOR_BMAD_SOLUTION_PROFILE_DIGEST_MISMATCH")
        instructions = content.decode("utf-8")
    except (OSError, UnicodeError, ValueError, RuntimeError):
        return denied("CONDUCTOR_BMAD_LOADER_READ_FAILED")
    return {
        "state": "LOADED", "reason_code": "CONDUCTOR_BMAD_GUARDED_LOAD_ALLOWED",
        "name": name, "root": str(root), "bmad_project_root": str(root / policy.active_bmad_root(root).parent), "skill_root": str(skill.parent),
        "skill_sha256": digest, "coverage_sha256": audit["coverage_sha256"],
        "authority_context": context,
        "route_constraint": "Load every subsequent or nested BMAD workflow through load_workflow. Do not read another BMAD SKILL.md directly, invoke Claude Skill, or treat a parent workflow as permission for its child. Stop on a denied load. This tool only returns instructions; it does not execute them or grant G1/G2/G3 approval.",
        "instructions": instructions,
    }


def response(request: Any, initialized: bool) -> tuple[dict[str, Any] | None, bool]:
    request_id = request.get("id") if isinstance(request, dict) else None
    def error(code: int, message: str):
        return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}, initialized
    if not isinstance(request, dict) or request.get("jsonrpc") != "2.0" or not isinstance(request.get("method"), str):
        return error(-32600, "Invalid request")
    method = request["method"]
    if "id" not in request:
        return None, initialized
    params = request.get("params", {})
    if not isinstance(params, dict):
        return error(-32602, "Invalid params")
    if method == "initialize":
        result = {
            "protocolVersion": "2025-06-18", "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "conductor-bmad", "version": "0.3.8"},
        }
        initialized = True
    elif method == "ping":
        result = {}
    elif not initialized:
        return error(-32000, "Initialize first")
    elif method == "tools/list":
        result = {"tools": [TOOL]}
    elif method == "tools/call":
        if params.get("name") != TOOL["name"]:
            return error(-32602, "Unknown tool")
        value = load_workflow(params.get("arguments"))
        result = {"content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False)}], "isError": value["state"] != "LOADED"}
    else:
        return error(-32601, "Method not found")
    return {"jsonrpc": "2.0", "id": request_id, "result": result}, initialized


def main() -> int:
    initialized = False
    for line in sys.stdin:
        try:
            request = json.loads(line)
        except (ValueError, UnicodeError, RecursionError):
            reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        else:
            reply, initialized = response(request, initialized)
        if reply is not None:
            print(json.dumps(reply, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
