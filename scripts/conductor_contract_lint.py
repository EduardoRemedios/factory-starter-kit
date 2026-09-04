"""Conductor contract-lint: deterministic validation of the three gates.

    contract-lint intent      G1  Intent Pack (+ Project Config, countersign)
    contract-lint execution   G2  locked intent, manifest v2, receipts, postimage
    contract-lint completion  G3  Statement of Completion, gap requests, countersign

Every check is schema- or digest-based. Nothing here reads prose for meaning.
Reason codes are CONDUCTOR_CONTRACT_*. A result is PASS only when errors is empty;
warnings never block. The run layout is docs/Conductor/DESIGN_PACK/01_ARCHITECTURE.md §4.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator, FormatChecker

SCRIPT_DIR = Path(__file__).resolve().parent
KIT_ROOT = SCRIPT_DIR.parent
RUNS_DIR = Path("docs/Conductor/runs")
CONTRACTS_DIR = Path("docs/Conductor/contracts")
PROJECT_CONFIG = Path("docs/Conductor/PROJECT_CONFIG.json")
PLACEHOLDER_RE = re.compile(r"\b(TBD|TODO|REPLACE_WITH|N/A)\b|<[A-Z_]+>|YYYYMMDD|0{64}")
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")
RECEIPT_EXCLUDED = "payload_sha256"


class ContractLintError(Exception):
    def __init__(self, reason_code: str, detail: str) -> None:
        super().__init__(f"{reason_code}: {detail}")
        self.reason_code = reason_code
        self.detail = detail


# --------------------------------------------------------------------------- helpers

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def receipt_payload_digest(receipt: dict[str, Any]) -> str:
    body = {key: value for key, value in receipt.items() if key != RECEIPT_EXCLUDED}
    return sha256_bytes(canonical_json(body))


def load_schema(root: Path, name: str) -> dict[str, Any]:
    for base in (root / CONTRACTS_DIR, KIT_ROOT / CONTRACTS_DIR):
        path = base / f"{name}.schema.json"
        if path.is_file():
            return json.loads(path.read_text(encoding="utf-8"))
    raise ContractLintError("CONDUCTOR_CONTRACT_SCHEMA_MISSING", name)


def schema_errors(root: Path, name: str, document: Any) -> list[str]:
    validator = Draft202012Validator(load_schema(root, name), format_checker=FormatChecker())
    return [f"{name}: {'/'.join(str(p) for p in e.absolute_path) or '<root>'}: {e.message}" for e in validator.iter_errors(document)]


def safe_run_root(root: Path, run_id: str) -> Path:
    if not RUN_ID_RE.fullmatch(run_id):
        raise ContractLintError("CONDUCTOR_CONTRACT_RUN_ID_INVALID", run_id)
    cursor = root.resolve()
    for part in (*RUNS_DIR.parts, run_id):
        cursor = cursor / part
        if cursor.is_symlink():
            raise ContractLintError("CONDUCTOR_CONTRACT_UNSAFE_PATH", str(cursor))
    if not cursor.is_dir():
        raise ContractLintError("CONDUCTOR_CONTRACT_RUN_MISSING", str(cursor))
    return cursor


def safe_relative(base: Path, relative: str, label: str, errors: list[str]) -> Path | None:
    """Resolve a repo/run-relative path, rejecting absolute, traversal, and symlink components."""
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts or "\\" in relative:
        errors.append(f"CONDUCTOR_CONTRACT_UNSAFE_PATH: {label}: {relative}")
        return None
    cursor = base.resolve()
    for part in candidate.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            errors.append(f"CONDUCTOR_CONTRACT_UNSAFE_PATH: {label}: symlink in {relative}")
            return None
    if base.resolve() not in cursor.parents:
        errors.append(f"CONDUCTOR_CONTRACT_UNSAFE_PATH: {label}: escapes base: {relative}")
        return None
    return cursor


def read_json(path: Path, label: str, errors: list[str]) -> Any:
    if not path.is_file():
        errors.append(f"CONDUCTOR_CONTRACT_FILE_MISSING: {label}: {path}")
        return None
    if path.stat().st_size == 0:
        errors.append(f"CONDUCTOR_CONTRACT_FILE_EMPTY: {label}: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"CONDUCTOR_CONTRACT_FILE_INVALID: {label}: {exc}")
        return None


def read_yaml(path: Path, label: str, errors: list[str]) -> Any:
    if not path.is_file():
        errors.append(f"CONDUCTOR_CONTRACT_FILE_MISSING: {label}: {path}")
        return None
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"CONDUCTOR_CONTRACT_FILE_INVALID: {label}: {exc}")
        return None


def result(gate: str, run_id: str, errors: list[str], warnings: list[str], **details: Any) -> dict[str, Any]:
    return {
        "gate": gate,
        "run_id": run_id,
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        **details,
    }


# --------------------------------------------------------------------------- countersign

def check_countersign(run_root: Path, kind: str, subject: Path, root: Path, errors: list[str]) -> bool:
    """Return True only if countersign/<kind>.json exists, validates, is GO, and pins the subject's current digest."""
    path = run_root / "countersign" / f"{kind}.json"
    if not path.is_file():
        return False
    local: list[str] = []
    document = read_json(path, f"countersign/{kind}", local)
    if document is None:
        errors.extend(local)
        return False
    local.extend(schema_errors(root, "countersign", document))
    if local:
        errors.extend(local)
        return False
    if document["kind"] != kind:
        errors.append(f"CONDUCTOR_CONTRACT_COUNTERSIGN_KIND_MISMATCH: {path.name} declares {document['kind']}")
        return False
    expected_subject = subject.relative_to(run_root).as_posix()
    if document["subject_path"] != expected_subject:
        errors.append(f"CONDUCTOR_CONTRACT_COUNTERSIGN_SUBJECT_MISMATCH: {kind} signs {document['subject_path']}, expected {expected_subject}")
        return False
    if not subject.is_file():
        errors.append(f"CONDUCTOR_CONTRACT_FILE_MISSING: countersign subject {expected_subject}")
        return False
    if document["subject_sha256"] != sha256_file(subject):
        errors.append(f"CONDUCTOR_CONTRACT_COUNTERSIGN_STALE: {kind} pins a digest that no longer matches {expected_subject}")
        return False
    if document["decision"] != "GO":
        errors.append(f"CONDUCTOR_CONTRACT_COUNTERSIGN_NO_GO: {kind} records {document['decision']}")
        return False
    return True


# --------------------------------------------------------------------------- G1

def load_intent(root: Path, run_root: Path, run_id: str, errors: list[str]) -> dict[str, Any] | None:
    path = run_root / "intent_pack.json"
    intent = read_json(path, "intent_pack.json", errors)
    if intent is None:
        return None
    errors.extend(schema_errors(root, "intent_pack", intent))
    if errors:
        return None
    if intent["run_id"] != run_id:
        errors.append(f"CONDUCTOR_CONTRACT_RUN_ID_MISMATCH: intent_pack.run_id={intent['run_id']} run={run_id}")
    text = path.read_text(encoding="utf-8")
    hits = sorted({m.group(0) for m in PLACEHOLDER_RE.finditer(text)})
    if hits:
        errors.append(f"CONDUCTOR_CONTRACT_PLACEHOLDER: intent_pack.json still contains {', '.join(hits)}")
    requirement_ids = [r["id"] for r in intent["requirements"]]
    if len(set(requirement_ids)) != len(requirement_ids):
        errors.append("CONDUCTOR_CONTRACT_DUPLICATE_ID: requirements")
    vr_ids = [v["id"] for v in intent["verification_requirements"]]
    if len(set(vr_ids)) != len(vr_ids):
        errors.append("CONDUCTOR_CONTRACT_DUPLICATE_ID: verification_requirements")
    for vr in intent["verification_requirements"]:
        unknown = sorted(set(vr["requirement_ids"]) - set(requirement_ids))
        if unknown:
            errors.append(f"CONDUCTOR_CONTRACT_UNKNOWN_REQUIREMENT: {vr['id']} references {unknown}")
    mode_path = run_root / "EXECUTION_MODE.txt"
    if mode_path.is_file():
        mode = mode_path.read_text(encoding="utf-8").strip()
        if mode != intent["execution_mode"]:
            errors.append(f"CONDUCTOR_CONTRACT_MODE_MISMATCH: EXECUTION_MODE.txt={mode} intent={intent['execution_mode']}")
    else:
        errors.append("CONDUCTOR_CONTRACT_FILE_MISSING: EXECUTION_MODE.txt")
    for source in intent["sources"]:
        target = safe_relative(root, source["ref"], f"sources[{source['kind']}]", errors)
        if target is None:
            continue
        if not target.is_file():
            errors.append(f"CONDUCTOR_CONTRACT_SOURCE_MISSING: {source['ref']}")
        elif sha256_file(target) != source["sha256"]:
            errors.append(f"CONDUCTOR_CONTRACT_SOURCE_DIGEST_MISMATCH: {source['ref']}")
    return intent


def check_project_config(root: Path, errors: list[str], warnings: list[str]) -> dict[str, Any] | None:
    path = root / PROJECT_CONFIG
    if not path.is_file():
        warnings.append("CONDUCTOR_CONTRACT_PROJECT_CONFIG_ABSENT: docs/Conductor/PROJECT_CONFIG.json not found; defaults assumed")
        return None
    config = read_json(path, "PROJECT_CONFIG.json", errors)
    if config is None:
        return None
    local = schema_errors(root, "project_config", config)
    errors.extend(local)
    if local:
        return None
    for name, block in (config.get("adapters") or {}).items():
        schema_path = root / "docs" / "adapters" / name / "contracts" / f"{name}_adapter_config.schema.json"
        if not schema_path.is_file():
            errors.append(f"CONDUCTOR_CONTRACT_ADAPTER_SCHEMA_MISSING: adapters.{name}")
            continue
        validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")), format_checker=FormatChecker())
        for error in validator.iter_errors(block):
            errors.append(f"CONDUCTOR_CONTRACT_ADAPTER_CONFIG_INVALID: adapters.{name}: {error.message}")
    for doc in config.get("required_docs", []):
        target = safe_relative(root, doc, "required_docs", errors)
        if target is not None and not target.is_file():
            errors.append(f"CONDUCTOR_CONTRACT_REQUIRED_DOC_MISSING: {doc}")
    if config.get("agents_md", {}).get("mode") == "managed_block":
        check_managed_block(root, errors)
    return config


MANAGED_START_RE = re.compile(r"<!-- conductor:managed:start v=[^ \n]+ sha256=(?P<d>[a-f0-9]{64}) -->\n")
MANAGED_END = "<!-- conductor:managed:end -->\n"


def check_managed_block(root: Path, errors: list[str]) -> None:
    """AGENTS.md must carry exactly one managed block whose recorded digest matches its body."""
    agents = root / "AGENTS.md"
    if not agents.is_file():
        errors.append("CONDUCTOR_CONTRACT_AGENTS_MD_MISSING")
        return
    text = agents.read_text(encoding="utf-8")
    starts = list(MANAGED_START_RE.finditer(text))
    if len(starts) != 1 or text.count(MANAGED_END) != 1:
        errors.append(f"CONDUCTOR_CONTRACT_MANAGED_BLOCK_COUNT: found {len(starts)} start and {text.count(MANAGED_END)} end markers")
        return
    end = text.find(MANAGED_END, starts[0].end())
    if end == -1:
        errors.append("CONDUCTOR_CONTRACT_MANAGED_BLOCK_UNTERMINATED")
        return
    body = text[starts[0].end() : end]
    if sha256_bytes(body.encode("utf-8")) != starts[0].group("d"):
        errors.append("CONDUCTOR_CONTRACT_MANAGED_BLOCK_DIGEST_MISMATCH: the block body was edited")


def lint_intent(root: Path, run_id: str) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    run_root = safe_run_root(root, run_id)
    intent = load_intent(root, run_root, run_id, errors)
    check_project_config(root, errors, warnings)
    locked = False
    if intent is not None and not errors:
        locked = check_countersign(run_root, "INTENT_LOCK", run_root / "intent_pack.json", root, errors)
    state = "INTENT_INVALID" if errors else ("INTENT_LOCKED" if locked else "INTENT_DRAFT")
    return result("G1", run_id, errors, warnings, state=state,
                  intent_pack_sha256=sha256_file(run_root / "intent_pack.json") if (run_root / "intent_pack.json").is_file() else None)


# --------------------------------------------------------------------------- G2

def load_manifest(root: Path, run_root: Path, run_id: str, intent: dict[str, Any], errors: list[str], warnings: list[str]) -> dict[str, Any] | None:
    path = run_root / "verification_manifest.yaml"
    declared = [v["id"] for v in intent["verification_requirements"]]
    if not path.is_file():
        if declared:
            errors.append(f"CONDUCTOR_CONTRACT_MANIFEST_MISSING: intent declares {len(declared)} verification requirements")
        else:
            warnings.append("CONDUCTOR_CONTRACT_MANIFEST_ABSENT: no verification requirements declared; nothing to prove")
        return None
    manifest = read_yaml(path, "verification_manifest.yaml", errors)
    if manifest is None:
        return None
    local = schema_errors(root, "verification_manifest_v2", manifest)
    errors.extend(local)
    if local:
        return None
    if manifest["run_id"] != run_id:
        errors.append(f"CONDUCTOR_CONTRACT_RUN_ID_MISMATCH: manifest.run_id={manifest['run_id']}")
    if manifest["execution_mode"] != intent["execution_mode"]:
        errors.append(f"CONDUCTOR_CONTRACT_MODE_MISMATCH: manifest={manifest['execution_mode']} intent={intent['execution_mode']}")
    check_ids = [c["id"] for c in manifest["checks"]]
    if len(set(check_ids)) != len(check_ids):
        errors.append("CONDUCTOR_CONTRACT_DUPLICATE_ID: manifest checks")
    if set(check_ids) != set(declared):
        errors.append(f"CONDUCTOR_CONTRACT_CHECK_SET_MISMATCH: manifest={sorted(check_ids)} intent={sorted(declared)}")
    requirement_ids = {r["id"] for r in intent["requirements"]}
    for check in manifest["checks"]:
        unknown = sorted(set(check.get("requirement_ids", [])) - requirement_ids)
        if unknown:
            errors.append(f"CONDUCTOR_CONTRACT_UNKNOWN_REQUIREMENT: {check['id']} references {unknown}")
    order = manifest.get("execution_order")
    if order is not None:
        missing = sorted(set(check_ids) - set(order))
        if missing:
            errors.append(f"CONDUCTOR_CONTRACT_EXECUTION_ORDER_INCOMPLETE: {missing}")
    return manifest


def verify_receipt(root: Path, run_root: Path, run_id: str, check: dict[str, Any], errors: list[str]) -> dict[str, Any] | None:
    """Validate a check's result block against its receipt. Returns the receipt on success."""
    res = check.get("result")
    if res is None:
        return None
    receipt_path = safe_relative(run_root, res["receipt_path"], f"{check['id']}.result.receipt_path", errors)
    if receipt_path is None:
        return None
    receipt = read_json(receipt_path, f"{check['id']} receipt", errors)
    if receipt is None:
        return None
    local = schema_errors(root, "evidence_receipt", receipt)
    if local:
        errors.extend(local)
        return None
    if receipt_payload_digest(receipt) != receipt["payload_sha256"]:
        errors.append(f"CONDUCTOR_CONTRACT_RECEIPT_TAMPERED: {check['id']}: payload digest does not match (agent-authored or edited receipt)")
        return None
    if receipt["run_id"] != run_id or receipt["check_id"] != check["id"]:
        errors.append(f"CONDUCTOR_CONTRACT_RECEIPT_IDENTITY_MISMATCH: {check['id']}")
        return None
    if receipt["status"] != res["status"]:
        errors.append(f"CONDUCTOR_CONTRACT_RESULT_MISMATCH: {check['id']}: manifest says {res['status']}, receipt says {receipt['status']}")
        return None
    for stream in ("stdout_path", "stderr_path"):
        log = safe_relative(run_root, receipt[stream], f"{check['id']}.{stream}", errors)
        if log is not None and not log.is_file():
            errors.append(f"CONDUCTOR_CONTRACT_FILE_MISSING: {check['id']} {stream}")
    return receipt


def check_postimage(run_root: Path, errors: list[str], warnings: list[str], require: bool) -> str:
    compare = run_root / "postimage" / "compare.json"
    if not compare.is_file():
        (errors if require else warnings).append("CONDUCTOR_CONTRACT_POSTIMAGE_MISSING: postimage/compare.json not found")
        return "MISSING"
    local: list[str] = []
    document = read_json(compare, "postimage/compare.json", local)
    if document is None:
        errors.extend(local)
        return "INVALID"
    status = document.get("status")
    if status != "PASS":
        errors.append(f"CONDUCTOR_CONTRACT_POSTIMAGE_FAILED: protected roots changed: {document.get('changed', [])}")
    return str(status)


def lint_execution(root: Path, run_id: str, require_complete: bool = False) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    run_root = safe_run_root(root, run_id)
    intent = load_intent(root, run_root, run_id, errors)
    if intent is None or errors:
        return result("G2", run_id, errors, warnings, state="INTENT_INVALID")
    if not check_countersign(run_root, "INTENT_LOCK", run_root / "intent_pack.json", root, errors):
        if not errors:
            errors.append("CONDUCTOR_CONTRACT_INTENT_NOT_LOCKED: countersign/INTENT_LOCK.json absent")
        return result("G2", run_id, errors, warnings, state="INTENT_NOT_LOCKED")
    if intent["execution_mode"] == "EXECUTION_ENABLED":
        if not check_countersign(run_root, "EXECUTION_GO", run_root / "intent_pack.json", root, errors):
            if not errors:
                errors.append("CONDUCTOR_CONTRACT_EXECUTION_NOT_AUTHORIZED: countersign/EXECUTION_GO.json absent for EXECUTION_ENABLED run")
            return result("G2", run_id, errors, warnings, state="EXECUTION_NOT_AUTHORIZED")
    manifest = load_manifest(root, run_root, run_id, intent, errors, warnings)
    checks: dict[str, str] = {}
    if manifest is not None and not errors:
        for check in manifest["checks"]:
            receipt = verify_receipt(root, run_root, run_id, check, errors)
            status = check["result"]["status"] if check.get("result") else "NOT_RUN"
            checks[check["id"]] = status if receipt or status == "NOT_RUN" else "INVALID"
            if status == "FAIL" and check["halt_on_failure"]:
                errors.append(f"CONDUCTOR_CONTRACT_HALT_ON_FAILURE: {check['id']} failed")
    incomplete = sorted(cid for cid, status in checks.items() if status in {"NOT_RUN", "SKIPPED"})
    if incomplete:
        (errors if require_complete else warnings).append(f"CONDUCTOR_CONTRACT_CHECKS_INCOMPLETE: {incomplete}")
    postimage = check_postimage(run_root, errors, warnings, require=require_complete)
    complete = manifest is not None and not incomplete and postimage == "PASS" and not errors
    state = "EXECUTION_INVALID" if errors else ("EXECUTION_COMPLETE" if complete else "EXECUTION_IN_PROGRESS")
    return result("G2", run_id, errors, warnings, state=state, checks=checks, postimage=postimage)


# --------------------------------------------------------------------------- G3

def derive_state(rows: list[dict[str, Any]]) -> str:
    if any(r["status"] == "not_done" and not r.get("decision_ref") for r in rows):
        return "BLOCKED"
    if any(r["status"] in {"partial", "out_of_scope", "not_done"} for r in rows):
        return "NEEDS_HUMAN_DECISION"
    return "READY"


def lint_completion(root: Path, run_id: str) -> dict[str, Any]:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    run_root = safe_run_root(root, run_id)
    intent = load_intent(root, run_root, run_id, errors)
    if intent is None or errors:
        return result("G3", run_id, errors, warnings, state="INTENT_INVALID")
    intent_digest = sha256_file(run_root / "intent_pack.json")
    if not check_countersign(run_root, "INTENT_LOCK", run_root / "intent_pack.json", root, errors) and not errors:
        errors.append("CONDUCTOR_CONTRACT_INTENT_NOT_LOCKED: countersign/INTENT_LOCK.json absent")
    manifest = load_manifest(root, run_root, run_id, intent, errors, warnings)
    manifest_results: dict[str, str] = {}
    if manifest is not None:
        for check in manifest["checks"]:
            receipt = verify_receipt(root, run_root, run_id, check, errors)
            manifest_results[check["id"]] = receipt["status"] if receipt else "NOT_RUN"

    statement_path = run_root / "statement_of_completion.json"
    statement = read_json(statement_path, "statement_of_completion.json", errors)
    if statement is None:
        return result("G3", run_id, errors, warnings, state="COMPLETION_MISSING")
    local = schema_errors(root, "statement_of_completion", statement)
    errors.extend(local)
    if local:
        return result("G3", run_id, errors, warnings, state="COMPLETION_INVALID")
    if statement["run_id"] != run_id:
        errors.append(f"CONDUCTOR_CONTRACT_RUN_ID_MISMATCH: statement.run_id={statement['run_id']}")
    if statement["intent_pack_sha256"] != intent_digest:
        errors.append("CONDUCTOR_CONTRACT_INTENT_DIGEST_MISMATCH: statement pins a different intent_pack.json")

    requirement_ids = [r["id"] for r in intent["requirements"]]
    row_ids = [r["requirement_id"] for r in statement["rows"]]
    if sorted(row_ids) != sorted(requirement_ids) or len(set(row_ids)) != len(row_ids):
        errors.append(f"CONDUCTOR_CONTRACT_ROW_SET_MISMATCH: rows={sorted(row_ids)} requirements={sorted(requirement_ids)}")

    for row in statement["rows"]:
        rid = row["requirement_id"]
        if row["status"] == "verified":
            for ev in row["evidence"]:
                if ev["check_id"] not in manifest_results:
                    errors.append(f"CONDUCTOR_CONTRACT_UNKNOWN_CHECK: {rid} cites {ev['check_id']}")
                    continue
                receipt_path = safe_relative(run_root, ev["receipt_path"], f"{rid}.evidence", errors)
                if receipt_path is None:
                    continue
                if not receipt_path.is_file() or receipt_path.stat().st_size == 0:
                    errors.append(f"CONDUCTOR_CONTRACT_EVIDENCE_MISSING: {rid} -> {ev['receipt_path']}")
                    continue
                if sha256_file(receipt_path) != ev["receipt_sha256"]:
                    errors.append(f"CONDUCTOR_CONTRACT_EVIDENCE_DIGEST_MISMATCH: {rid} -> {ev['receipt_path']}")
                if manifest_results[ev["check_id"]] != "PASS":
                    errors.append(f"CONDUCTOR_CONTRACT_EVIDENCE_NOT_PASSING: {rid} cites {ev['check_id']} whose receipt is {manifest_results[ev['check_id']]}")
        if row.get("decision_ref"):
            target = safe_relative(run_root, row["decision_ref"], f"{rid}.decision_ref", errors)
            if target is not None:
                parts = target.relative_to(run_root.resolve()).parts
                if not target.is_file():
                    errors.append(f"CONDUCTOR_CONTRACT_DECISION_MISSING: {rid} -> {row['decision_ref']}")
                elif parts[0] not in {"countersign", "gap_requests"}:
                    errors.append(f"CONDUCTOR_CONTRACT_DECISION_NOT_HUMAN: {rid} -> {row['decision_ref']} is not under countersign/ or gap_requests/")
                elif parts[0] == "gap_requests":
                    gap: list[str] = []
                    doc = read_json(target, row["decision_ref"], gap)
                    if doc is None or "resolution" not in doc:
                        errors.append(f"CONDUCTOR_CONTRACT_DECISION_UNRESOLVED: {rid} -> {row['decision_ref']} has no resolution")
        elif row["status"] == "not_done":
            warnings.append(f"CONDUCTOR_CONTRACT_NOT_DONE_UNDECIDED: {rid}")

    verifier = safe_relative(run_root, statement["verifier"]["report_path"], "verifier.report_path", errors)
    if verifier is not None:
        if not verifier.is_file():
            errors.append("CONDUCTOR_CONTRACT_VERIFIER_MISSING: verifier report not found")
        elif sha256_file(verifier) != statement["verifier"]["report_sha256"]:
            errors.append("CONDUCTOR_CONTRACT_VERIFIER_DIGEST_MISMATCH")

    expected_state = derive_state(statement["rows"])
    if statement["derived_state"] != expected_state:
        errors.append(f"CONDUCTOR_CONTRACT_DERIVED_STATE_MISMATCH: statement says {statement['derived_state']}, lint derives {expected_state}")

    if statement["handoff_state"] == "MERGE_READY":
        summary = safe_relative(root, statement.get("merge_preflight_summary", ""), "merge_preflight_summary", errors)
        verdict_ok = summary is not None and summary.is_file() and re.search(
            r"(?m)^\s*-?\s*Verdict:\s*MERGE_READY\s*$", summary.read_text(encoding="utf-8")
        )
        if not verdict_ok:
            errors.append("CONDUCTOR_CONTRACT_MERGE_READY_UNPROVEN: merge preflight summary missing or not MERGE_READY")

    gaps_dir = run_root / "gap_requests"
    reopen: list[str] = []
    if gaps_dir.is_dir():
        for gap_path in sorted(gaps_dir.glob("*.json")):
            gap = read_json(gap_path, gap_path.name, errors)
            if gap is None:
                continue
            local = schema_errors(root, "gap_request", gap)
            errors.extend(local)
            if local:
                continue
            if gap["run_id"] != run_id or gap["intent_pack_sha256"] != intent_digest:
                errors.append(f"CONDUCTOR_CONTRACT_GAP_IDENTITY_MISMATCH: {gap_path.name}")
            resolution = gap.get("resolution") or {}
            if gap["supersession_impact"] == "active_scope" and resolution.get("new_snapshot_id"):
                reopen.append(gap["gap_id"])
    if reopen:
        errors.append(f"CONDUCTOR_CONTRACT_G1_REOPEN_REQUIRED: gap requests {reopen} supersede active scope; re-lock intent before completion")

    countersigned = False
    if not errors:
        countersigned = check_countersign(run_root, "COMPLETION", statement_path, root, errors)
    state = "COMPLETION_INVALID" if errors else ("COMPLETION_COUNTERSIGNED" if countersigned else "COMPLETION_DRAFT")
    return result("G3", run_id, errors, warnings, state=state, derived_state=expected_state,
                  handoff_state=statement["handoff_state"], countersigned=countersigned)


def format_result(payload: dict[str, Any]) -> str:
    lines = [f"contract-lint {payload['gate']}: {payload['status']} run={payload['run_id']} state={payload.get('state')}"]
    for key in ("derived_state", "handoff_state", "postimage"):
        if key in payload:
            lines.append(f"  {key}={payload[key]}")
    if "checks" in payload:
        lines.append("  checks=" + ", ".join(f"{k}:{v}" for k, v in sorted(payload["checks"].items())))
    for error in payload["errors"]:
        lines.append(f"  ERROR {error}")
    for warning in payload["warnings"]:
        lines.append(f"  WARN  {warning}")
    return "\n".join(lines)
