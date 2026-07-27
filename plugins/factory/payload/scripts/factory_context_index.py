from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Sequence


DB_SCHEMA_VERSION = 1
SUPPORTED_DB_SCHEMA_VERSIONS = (1,)
DEFAULT_DB_ENV_VAR = "FACTORY_CONTEXT_DB_PATH"
LEGACY_DB_PATH = Path("artifacts/factory_context/context.sqlite3")
DEFAULT_SOURCE_PATTERNS = (
    "AGENTS.md",
    "docs/PROJECT_STATE.md",
    "docs/ROADMAP.md",
    "docs/CHANGELOG.md",
    "docs/Factory/**/*.md",
    "docs/onboarding/**/*.md",
    "docs/sprints/**/*.md",
)
MAX_CHUNK_LINES = 80
DEFAULT_REPORT_QUERY_LIMIT = 5

RUN_ID_RE = re.compile(r"\bRUN_\d{8}_\d{4}_[A-Za-z0-9_-]+\b")
MISSION_ID_RE = re.compile(r"\bMISSION_\d{8}_\d{3}\b")
PHASE_ID_RE = re.compile(r"\bPHASE_[A-Z0-9_]+\b")
SPRINT_ID_RE = re.compile(r"\b(?:SPRINT_\d{8}_\d{3}|P\d+[A-Z0-9_-]*-\d{2})\b")
CONSTRAINT_ID_RE = re.compile(r"\bC-[A-Z0-9][A-Z0-9_-]*\b")
RISK_ID_RE = re.compile(r"\b(?:R-\d{2,3}|RSK-\d{2,3}|R[A-Z]{1,6}\d{0,2}-\d{2,3})\b")
VERIFY_ID_RE = re.compile(r"\bVP-[A-Z0-9][A-Z0-9_-]*\b")
PITFALL_ID_RE = re.compile(r"\bFP-\d{3}\b")
DEFERRAL_ID_RE = re.compile(r"\bD-\d{3}\b")
MISSION_CHECK_RE = re.compile(r"\bMC-\d{2}\b")

FACT_PATTERNS = (
    ("run_id", RUN_ID_RE),
    ("mission_id", MISSION_ID_RE),
    ("phase_id", PHASE_ID_RE),
    ("sprint_id", SPRINT_ID_RE),
    ("constraint_id", CONSTRAINT_ID_RE),
    ("risk_id", RISK_ID_RE),
    ("verification_id", VERIFY_ID_RE),
    ("pitfall_id", PITFALL_ID_RE),
    ("deferral_id", DEFERRAL_ID_RE),
    ("mission_check_id", MISSION_CHECK_RE),
)

CONTEXT_REPORT_PROFILES: dict[str, dict[str, Any]] = {
    "stage-a": {
        "label": "Factory Stage A Preflight",
        "fallback_scopes": (
            "docs/Factory/runs",
            "docs/Factory/ProductOwner/phases",
            "docs",
        ),
        "default_queries": (
            "BLOCKING",
            "Critical",
            "deferral",
            "human GO",
            "scope expansion",
        ),
        "guidance": (
            "Use this before Stage A to surface binding constraints, unresolved blockers, "
            "prior human checkpoints, and recent scope decisions tied to the new run."
        ),
    },
    "po-brief": {
        "label": "PO Sprint Brief Recall",
        "fallback_scopes": (
            "docs/Factory/ProductOwner/phases",
            "docs/Factory/runs",
            "docs",
        ),
        "default_queries": (
            "Red Team",
            "BLOCKING",
            "descope",
            "accepted",
            "scope expansion",
        ),
        "guidance": (
            "Use this before drafting or reviewing a PO sprint brief to recover prior rationale, "
            "accepted descopes, and binding trade-offs inside the phase."
        ),
    },
    "mission-checkpoint": {
        "label": "Mission Checkpoint Recall",
        "fallback_scopes": (
            "docs/Factory/missions",
            "docs/Factory/runs",
            "docs",
        ),
        "default_queries": (
            "BLOCKING",
            "failed",
            "pack_complete",
            "closed_go",
            "human GO",
        ),
        "guidance": (
            "Use this before mission checkpointing or downstream mission-unit planning to recover "
            "cross-unit blockers, prior approvals, and terminal unit outcomes."
        ),
    },
}


class FactoryContextIndexError(RuntimeError):
    """Raised when the context index is missing or malformed."""


def _utc_now() -> str:
    return (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def default_context_db_path() -> Path:
    override = os.environ.get(DEFAULT_DB_ENV_VAR)
    if override:
        return Path(override).expanduser()
    return Path("/tmp/factory_starter_kit_context/context.sqlite3")


def _resolve_context_db_path(root: Path, db_path: Path | None = None) -> Path:
    if db_path is not None:
        return db_path.expanduser().resolve()

    default_path = default_context_db_path().resolve()
    if default_path.exists():
        return default_path

    legacy_path = (root / LEGACY_DB_PATH).resolve()
    if legacy_path.exists():
        return legacy_path

    return default_path


def _ensure_supported_db_version(version: int) -> None:
    if int(version) not in SUPPORTED_DB_SCHEMA_VERSIONS:
        raise FactoryContextIndexError(f"unsupported factory context DB schema version: {version}")


def _discover_source_paths(root: Path, patterns: Iterable[str]) -> list[Path]:
    discovered: set[Path] = set()
    for pattern in patterns:
        if any(ch in pattern for ch in "*?[]"):
            matches = root.glob(pattern)
        else:
            matches = [root / pattern]
        for match in matches:
            if match.is_file():
                discovered.add(match.resolve())
    return sorted(discovered, key=lambda path: path.relative_to(root).as_posix())


def _extract_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def _extract_version(text: str) -> str | None:
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if line.strip() == "## Version" and idx + 1 < len(lines):
            value = lines[idx + 1].strip()
            if value:
                return value
    return None


def _classify_source(rel_path: str, text: str) -> dict[str, Any]:
    path_parts = Path(rel_path).parts
    artifact_type = "canonical_doc"
    run_id = None
    mission_id = None
    phase_id = None
    sprint_id = None

    if len(path_parts) >= 4 and path_parts[:3] == ("docs", "Factory", "runs"):
        run_id = path_parts[3]
        artifact_type = "factory_run_pack_artifact" if "pack" in path_parts else "factory_run_root_artifact"
    elif len(path_parts) >= 4 and path_parts[:3] == ("docs", "Factory", "missions"):
        mission_id = path_parts[3]
        artifact_type = "mission_artifact"
    elif len(path_parts) >= 5 and path_parts[:4] == ("docs", "Factory", "ProductOwner", "phases"):
        phase_id = path_parts[4]
        artifact_type = "po_phase_artifact"
    elif rel_path == "AGENTS.md":
        artifact_type = "repo_context_doc"

    if not run_id:
        match = RUN_ID_RE.search(text)
        run_id = match.group(0) if match else None
    if not mission_id:
        match = MISSION_ID_RE.search(text)
        mission_id = match.group(0) if match else None
    if not phase_id:
        match = PHASE_ID_RE.search(text)
        phase_id = match.group(0) if match else None
    match = SPRINT_ID_RE.search(text)
    sprint_id = match.group(0) if match else None

    return {
        "artifact_type": artifact_type,
        "run_id": run_id,
        "mission_id": mission_id,
        "phase_id": phase_id,
        "sprint_id": sprint_id,
    }


def _token_estimate(text: str) -> int:
    return max(1, len(re.findall(r"[A-Za-z0-9_]+", text)))


def _chunk_markdown(text: str) -> list[dict[str, Any]]:
    lines = text.splitlines()
    if not lines:
        return []

    chunks: list[dict[str, Any]] = []
    current_lines: list[str] = []
    current_start = 1
    current_heading = "Document Start"
    heading_stack: list[tuple[int, str]] = []

    def flush(end_line: int) -> None:
        nonlocal current_lines, current_start, current_heading
        body = "\n".join(current_lines).strip()
        if not body:
            current_lines = []
            return
        chunks.append(
            {
                "start_line": current_start,
                "end_line": end_line,
                "heading": current_heading,
                "content": body,
            }
        )
        current_lines = []

    for idx, line in enumerate(lines, start=1):
        heading_match = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading_match:
            if current_lines:
                flush(idx - 1)
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
            current_heading = " > ".join(part for _, part in heading_stack)
            current_start = idx
            current_lines = [line]
            continue

        if not current_lines:
            current_lines = [line]
            current_start = idx
        else:
            current_lines.append(line)

        if len(current_lines) >= MAX_CHUNK_LINES:
            flush(idx)
            current_start = idx + 1

    if current_lines:
        flush(len(lines))

    return chunks


def _extract_facts(chunk_text: str) -> list[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for fact_type, pattern in FACT_PATTERNS:
        for match in pattern.finditer(chunk_text):
            found.add((fact_type, match.group(0)))
    return sorted(found)


def _normalize_scope(scope: str | None) -> str | None:
    if not scope:
        return None
    return scope.strip().strip("/")


def _matches_scope(row: sqlite3.Row, scope: str | None) -> bool:
    if not scope:
        return True
    normalized = _normalize_scope(scope)
    if not normalized:
        return True
    path = row["path"]
    if path == normalized or path.startswith(f"{normalized}/"):
        return True
    for field in ("run_id", "mission_id", "phase_id", "sprint_id"):
        value = row[field]
        if value and value == normalized:
            return True
    return False


def _looks_like_identifier(value: str) -> bool:
    for _, pattern in FACT_PATTERNS:
        if pattern.fullmatch(value):
            return True
    return False


def _normalize_required_ref_path(root: Path, value: str) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            return path.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            return path.resolve().as_posix()
    return path.as_posix().lstrip("./")


class SQLiteFactoryContextIndex:
    def __init__(self, root: Path, db_path: Path) -> None:
        self.root = root.resolve()
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row

    def close(self) -> None:
        self.connection.close()

    def initialize(self) -> None:
        self.connection.executescript(
            """
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT NOT NULL UNIQUE,
                title TEXT NOT NULL,
                version TEXT,
                artifact_type TEXT NOT NULL,
                run_id TEXT,
                mission_id TEXT,
                phase_id TEXT,
                sprint_id TEXT,
                line_count INTEGER NOT NULL,
                char_count INTEGER NOT NULL,
                content_sha TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
                source_path TEXT NOT NULL,
                heading TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                token_estimate INTEGER NOT NULL,
                content TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_path TEXT NOT NULL,
                chunk_id INTEGER NOT NULL REFERENCES chunks(id) ON DELETE CASCADE,
                fact_type TEXT NOT NULL,
                value TEXT NOT NULL
            );
            """
        )
        self.connection.execute("PRAGMA foreign_keys=ON")
        self.connection.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('schema_version', ?)",
            (str(DB_SCHEMA_VERSION),),
        )
        self.connection.commit()

    def schema_version(self) -> int:
        row = self.connection.execute(
            "SELECT value FROM meta WHERE key = 'schema_version'"
        ).fetchone()
        if row is None:
            raise FactoryContextIndexError("context index schema_version is missing")
        return int(row["value"])

    def rebuild(self, patterns: Iterable[str]) -> dict[str, Any]:
        self.initialize()
        self.connection.execute("DELETE FROM facts")
        self.connection.execute("DELETE FROM chunks")
        self.connection.execute("DELETE FROM sources")
        self.connection.commit()

        source_count = 0
        chunk_count = 0
        fact_count = 0
        for source_path in _discover_source_paths(self.root, patterns):
            rel_path = source_path.relative_to(self.root).as_posix()
            text = source_path.read_text(encoding="utf-8")
            metadata = _classify_source(rel_path, text)
            title = _extract_title(text, rel_path)
            version = _extract_version(text)
            content_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
            source_cursor = self.connection.execute(
                """
                INSERT INTO sources (
                    path, title, version, artifact_type, run_id, mission_id, phase_id, sprint_id,
                    line_count, char_count, content_sha
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    rel_path,
                    title,
                    version,
                    metadata["artifact_type"],
                    metadata["run_id"],
                    metadata["mission_id"],
                    metadata["phase_id"],
                    metadata["sprint_id"],
                    len(text.splitlines()),
                    len(text),
                    content_sha,
                ),
            )
            source_id = int(source_cursor.lastrowid)
            source_count += 1

            for chunk in _chunk_markdown(text):
                chunk_cursor = self.connection.execute(
                    """
                    INSERT INTO chunks (
                        source_id, source_path, heading, start_line, end_line, token_estimate, content
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        source_id,
                        rel_path,
                        chunk["heading"],
                        chunk["start_line"],
                        chunk["end_line"],
                        _token_estimate(chunk["content"]),
                        chunk["content"],
                    ),
                )
                chunk_id = int(chunk_cursor.lastrowid)
                chunk_count += 1
                for fact_type, value in _extract_facts(chunk["content"]):
                    self.connection.execute(
                        """
                        INSERT INTO facts (source_path, chunk_id, fact_type, value)
                        VALUES (?, ?, ?, ?)
                        """,
                        (rel_path, chunk_id, fact_type, value),
                    )
                    fact_count += 1

        self.connection.commit()
        return {
            "db_path": str(self.db_path),
            "source_count": source_count,
            "chunk_count": chunk_count,
            "fact_count": fact_count,
            "timestamp_utc": _utc_now(),
        }

    def _source_rows(self) -> list[sqlite3.Row]:
        return self.connection.execute("SELECT * FROM sources ORDER BY path ASC").fetchall()

    def describe(self, scope: str | None = None) -> dict[str, Any]:
        rows = [row for row in self._source_rows() if _matches_scope(row, scope)]
        artifact_counts = Counter(row["artifact_type"] for row in rows)
        return {
            "scope": scope,
            "source_count": len(rows),
            "artifact_counts": dict(sorted(artifact_counts.items())),
            "sources": [row["path"] for row in rows],
        }

    def recall(self, query: str, scope: str | None = None, limit: int = 8) -> dict[str, Any]:
        query_lower = query.lower().strip()
        terms = [term for term in re.findall(r"[A-Za-z0-9_/-]+", query_lower) if len(term) >= 2]
        rows = self.connection.execute(
            """
            SELECT
                chunks.id AS chunk_id,
                chunks.source_path,
                chunks.heading,
                chunks.start_line,
                chunks.end_line,
                chunks.content,
                sources.title,
                sources.artifact_type,
                sources.run_id,
                sources.mission_id,
                sources.phase_id,
                sources.sprint_id,
                sources.path
            FROM chunks
            JOIN sources ON sources.id = chunks.source_id
            ORDER BY chunks.source_path ASC, chunks.start_line ASC
            """
        ).fetchall()

        matches: list[dict[str, Any]] = []
        for row in rows:
            if not _matches_scope(row, scope):
                continue
            content_lower = row["content"].lower()
            if query_lower not in content_lower and terms and not all(term in content_lower for term in terms):
                continue
            score = content_lower.count(query_lower) if query_lower else 0
            if score == 0:
                score = sum(content_lower.count(term) for term in terms)
            excerpt = row["content"][:400].strip()
            matches.append(
                {
                    "chunk_id": row["chunk_id"],
                    "source_path": row["source_path"],
                    "title": row["title"],
                    "artifact_type": row["artifact_type"],
                    "heading": row["heading"],
                    "start_line": row["start_line"],
                    "end_line": row["end_line"],
                    "score": score,
                    "excerpt": excerpt,
                }
            )

        matches.sort(key=lambda item: (-item["score"], item["source_path"], item["start_line"]))
        return {
            "query": query,
            "scope": scope,
            "match_count": len(matches),
            "matches": matches[:limit],
        }

    def trace(self, identifier: str, scope: str | None = None) -> dict[str, Any]:
        rows = self.connection.execute(
            """
            SELECT
                facts.fact_type,
                facts.value,
                chunks.id AS chunk_id,
                chunks.source_path,
                chunks.heading,
                chunks.start_line,
                chunks.end_line,
                sources.title,
                sources.artifact_type,
                sources.path,
                sources.run_id,
                sources.mission_id,
                sources.phase_id,
                sources.sprint_id
            FROM facts
            JOIN chunks ON chunks.id = facts.chunk_id
            JOIN sources ON sources.path = facts.source_path
            WHERE facts.value = ?
            ORDER BY facts.source_path ASC, chunks.start_line ASC
            """,
            (identifier,),
        ).fetchall()

        matches = []
        for row in rows:
            if not _matches_scope(row, scope):
                continue
            matches.append(
                {
                    "fact_type": row["fact_type"],
                    "value": row["value"],
                    "chunk_id": row["chunk_id"],
                    "source_path": row["source_path"],
                    "title": row["title"],
                    "artifact_type": row["artifact_type"],
                    "heading": row["heading"],
                    "start_line": row["start_line"],
                    "end_line": row["end_line"],
                }
            )
        return {
            "identifier": identifier,
            "scope": scope,
            "match_count": len(matches),
            "matches": matches,
        }

    def expand(self, ref: str) -> dict[str, Any]:
        chunk: sqlite3.Row | None = None
        if ref.isdigit():
            chunk = self.connection.execute(
                """
                SELECT chunks.id AS chunk_id, chunks.source_path, chunks.heading, chunks.start_line,
                       chunks.end_line, chunks.content, sources.title
                FROM chunks
                JOIN sources ON sources.id = chunks.source_id
                WHERE chunks.id = ?
                """,
                (int(ref),),
            ).fetchone()
        if chunk:
            return {
                "ref": ref,
                "type": "chunk",
                "chunk_id": chunk["chunk_id"],
                "source_path": chunk["source_path"],
                "title": chunk["title"],
                "heading": chunk["heading"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "content": chunk["content"],
            }

        normalized = _normalize_required_ref_path(self.root, ref)
        source = self.connection.execute(
            "SELECT path, title FROM sources WHERE path = ?",
            (normalized,),
        ).fetchone()
        if source:
            chunks = self.connection.execute(
                """
                SELECT id, heading, start_line, end_line, content
                FROM chunks
                WHERE source_path = ?
                ORDER BY start_line ASC
                """,
                (normalized,),
            ).fetchall()
            return {
                "ref": ref,
                "type": "source",
                "source_path": normalized,
                "title": source["title"],
                "chunks": [
                    {
                        "chunk_id": row["id"],
                        "heading": row["heading"],
                        "start_line": row["start_line"],
                        "end_line": row["end_line"],
                        "content": row["content"],
                    }
                    for row in chunks
                ],
            }

        raise FactoryContextIndexError(f"unknown context reference: {ref}")


def build_context_index(root: Path, db_path: Path | None = None) -> dict[str, Any]:
    db = SQLiteFactoryContextIndex(root=root, db_path=_resolve_context_db_path(root, db_path))
    try:
        return db.rebuild(DEFAULT_SOURCE_PATTERNS)
    finally:
        db.close()


def _open_index(root: Path, db_path: Path | None = None) -> SQLiteFactoryContextIndex:
    db = SQLiteFactoryContextIndex(root=root, db_path=_resolve_context_db_path(root, db_path))
    db.initialize()
    _ensure_supported_db_version(db.schema_version())
    return db


def describe_context(root: Path, db_path: Path | None = None, scope: str | None = None) -> dict[str, Any]:
    db = _open_index(root, db_path)
    try:
        return db.describe(scope=scope)
    finally:
        db.close()


def recall_context(
    root: Path,
    query: str,
    db_path: Path | None = None,
    scope: str | None = None,
    limit: int = 8,
) -> dict[str, Any]:
    db = _open_index(root, db_path)
    try:
        return db.recall(query=query, scope=scope, limit=limit)
    finally:
        db.close()


def trace_context(
    root: Path,
    identifier: str,
    db_path: Path | None = None,
    scope: str | None = None,
) -> dict[str, Any]:
    db = _open_index(root, db_path)
    try:
        return db.trace(identifier=identifier, scope=scope)
    finally:
        db.close()


def expand_context(root: Path, ref: str, db_path: Path | None = None) -> dict[str, Any]:
    db = _open_index(root, db_path)
    try:
        return db.expand(ref=ref)
    finally:
        db.close()


def format_context_recall(payload: dict[str, Any]) -> str:
    lines = [
        f"Query: {payload['query']}",
        f"Scope: {payload['scope'] or 'ALL'}",
        f"Matches: {payload['match_count']}",
    ]
    for idx, match in enumerate(payload["matches"], start=1):
        lines.extend(
            [
                "",
                f"{idx}. {match['source_path']}:{match['start_line']}",
                f"   Heading: {match['heading']}",
                f"   Score: {match['score']}",
                f"   Excerpt: {match['excerpt'].replace(chr(10), ' ')}",
            ]
        )
    return "\n".join(lines) + "\n"


def format_context_trace(payload: dict[str, Any]) -> str:
    lines = [
        f"Identifier: {payload['identifier']}",
        f"Scope: {payload['scope'] or 'ALL'}",
        f"Matches: {payload['match_count']}",
    ]
    for idx, match in enumerate(payload["matches"], start=1):
        lines.extend(
            [
                "",
                f"{idx}. {match['source_path']}:{match['start_line']}",
                f"   Type: {match['fact_type']}",
                f"   Heading: {match['heading']}",
            ]
        )
    return "\n".join(lines) + "\n"


def format_context_expand(payload: dict[str, Any]) -> str:
    if payload["type"] == "chunk":
        return (
            f"Chunk {payload['chunk_id']} | {payload['source_path']}:{payload['start_line']}-{payload['end_line']}\n"
            f"Heading: {payload['heading']}\n\n"
            f"{payload['content']}\n"
        )

    lines = [f"Source: {payload['source_path']}", f"Title: {payload['title']}"]
    for chunk in payload["chunks"]:
        lines.extend(
            [
                "",
                f"Chunk {chunk['chunk_id']} | {chunk['start_line']}-{chunk['end_line']}",
                f"Heading: {chunk['heading']}",
                chunk["content"],
            ]
        )
    return "\n".join(lines) + "\n"


def format_context_describe(payload: dict[str, Any]) -> str:
    lines = [
        f"Scope: {payload['scope'] or 'ALL'}",
        f"Sources: {payload['source_count']}",
        "Artifact counts:",
    ]
    for artifact_type, count in payload["artifact_counts"].items():
        lines.append(f"- {artifact_type}: {count}")
    return "\n".join(lines) + "\n"


def _dedupe_preserve_order(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        cleaned = value.strip()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        output.append(cleaned)
    return output


def _profile_definition(profile: str) -> dict[str, Any]:
    if profile not in CONTEXT_REPORT_PROFILES:
        raise FactoryContextIndexError(f"unsupported context-report profile: {profile}")
    return CONTEXT_REPORT_PROFILES[profile]


def _evaluate_required_ref(
    root: Path,
    db: SQLiteFactoryContextIndex,
    required_ref: str,
    scope: str,
) -> dict[str, Any]:
    if _looks_like_identifier(required_ref):
        payload = db.trace(identifier=required_ref, scope=scope)
        status = "RESOLVED" if payload["match_count"] > 0 else "UNRESOLVED"
        return {
            "required_ref": required_ref,
            "status": status,
            "resolution_type": "identifier",
            "evidence": payload["matches"][:3],
        }

    normalized = _normalize_required_ref_path(root, required_ref)
    rows = [row for row in db._source_rows() if _matches_scope(row, scope)]
    matching = [row for row in rows if row["path"] == normalized]
    status = "RESOLVED" if matching else "UNRESOLVED"
    evidence = [
        {
            "source_path": row["path"],
            "title": row["title"],
            "artifact_type": row["artifact_type"],
        }
        for row in matching[:3]
    ]
    return {
        "required_ref": required_ref,
        "normalized_ref": normalized,
        "status": status,
        "resolution_type": "path",
        "evidence": evidence,
    }


def _coverage_verdict(
    source_count: int,
    recall_results: Sequence[dict[str, Any]],
    trace_results: Sequence[dict[str, Any]],
    required_ref_results: Sequence[dict[str, Any]],
) -> str:
    if source_count == 0:
        return "WEAK"
    if any(result["status"] == "UNRESOLVED" for result in required_ref_results):
        return "WEAK"
    has_recall_hits = any(result["match_count"] > 0 for result in recall_results)
    has_trace_hits = any(result["match_count"] > 0 for result in trace_results)
    if not has_recall_hits and not has_trace_hits:
        return "WEAK"
    return "SUFFICIENT"


def _attempt_score(attempt: dict[str, Any]) -> tuple[int, int, int, int]:
    resolved_required_refs = sum(
        1 for result in attempt["required_ref_results"] if result["status"] == "RESOLVED"
    )
    recall_hits = sum(result["match_count"] for result in attempt["recall_results"])
    trace_hits = sum(result["match_count"] for result in attempt["trace_results"])
    source_count = attempt["describe"]["source_count"]
    return (source_count, recall_hits, trace_hits, resolved_required_refs)


def _collect_report_attempt(
    root: Path,
    db: SQLiteFactoryContextIndex,
    scope: str,
    queries: Sequence[str],
    trace_ids: Sequence[str],
    required_refs: Sequence[str],
    limit: int,
) -> dict[str, Any]:
    describe = db.describe(scope=scope)
    recall_results = [db.recall(query=query, scope=scope, limit=limit) for query in queries]
    trace_results = [db.trace(identifier=identifier, scope=scope) for identifier in trace_ids]
    required_ref_results = [
        _evaluate_required_ref(root=root, db=db, required_ref=required_ref, scope=scope)
        for required_ref in required_refs
    ]
    return {
        "scope": scope,
        "describe": describe,
        "recall_results": recall_results,
        "trace_results": trace_results,
        "required_ref_results": required_ref_results,
        "coverage_verdict": _coverage_verdict(
            source_count=describe["source_count"],
            recall_results=recall_results,
            trace_results=trace_results,
            required_ref_results=required_ref_results,
        ),
    }


def _render_source_hit(hit: dict[str, Any]) -> str:
    return f"- `{hit['source_path']}` ({hit.get('artifact_type', 'unknown')})"


def _render_context_report(
    *,
    profile: str,
    profile_label: str,
    guidance: str,
    requested_scope: str,
    effective_scope: str,
    attempted_scopes: Sequence[str],
    fallback_applied: bool,
    coverage_verdict: str,
    source_index: str,
    generated_at: str,
    focus_terms: Sequence[str],
    trace_ids: Sequence[str],
    required_refs: Sequence[str],
    attempt: dict[str, Any],
) -> str:
    unresolved = [
        result["required_ref"]
        for result in attempt["required_ref_results"]
        if result["status"] == "UNRESOLVED"
    ]
    lines = [
        "# Context Recall Report",
        "",
        "## Version",
        "v1",
        "",
        "## Change Log",
        f"- v1 ({generated_at[:10]}): Generated recall report for profile `{profile}`.",
        "",
        "## Report Metadata",
        f"- Profile: {profile} ({profile_label})",
        f"- Requested Scope: {requested_scope}",
        f"- Effective Scope: {effective_scope}",
        f"- Attempted Scopes: {', '.join(attempted_scopes)}",
        f"- Fallback Applied: {'YES' if fallback_applied else 'NO'}",
        f"- Coverage Verdict: {coverage_verdict}",
        f"- Generated At (UTC): {generated_at}",
        f"- Source Index: {source_index}",
        "",
        "## Purpose",
        f"- {guidance}",
        "",
        "## Coverage Snapshot",
        f"- Indexed sources in effective scope: {attempt['describe']['source_count']}",
        f"- Artifact types: {json.dumps(attempt['describe']['artifact_counts'], sort_keys=True)}",
        f"- Focus terms: {', '.join(focus_terms) if focus_terms else 'None'}",
        f"- Trace IDs: {', '.join(trace_ids) if trace_ids else 'None'}",
        f"- Required refs: {', '.join(required_refs) if required_refs else 'None'}",
        f"- Unresolved required refs: {', '.join(unresolved) if unresolved else 'None'}",
        "",
        "## Recall Queries",
    ]

    for idx, result in enumerate(attempt["recall_results"], start=1):
        lines.append(f"### Q{idx}. `{result['query']}`")
        lines.append(f"- Result count: {result['match_count']}")
        if result["matches"]:
            lines.append("- Evidence:")
            for match in result["matches"]:
                lines.append(
                    f"  - `{match['source_path']}:{match['start_line']}` [{match['heading']}]"
                )
        else:
            lines.append("- Evidence: None")
        lines.append("")

    lines.append("## Trace Queries")
    for idx, result in enumerate(attempt["trace_results"], start=1):
        lines.append(f"### T{idx}. `{result['identifier']}`")
        lines.append(f"- Match count: {result['match_count']}")
        if result["matches"]:
            lines.append("- Evidence:")
            for match in result["matches"]:
                lines.append(
                    f"  - `{match['source_path']}:{match['start_line']}` [{match['fact_type']}]"
                )
        else:
            lines.append("- Evidence: None")
        lines.append("")

    lines.append("## Required Reference Checks")
    for idx, result in enumerate(attempt["required_ref_results"], start=1):
        lines.append(f"### R{idx}. `{result['required_ref']}`")
        lines.append(f"- Status: {result['status']}")
        lines.append(f"- Resolution Type: {result['resolution_type']}")
        if result["evidence"]:
            lines.append("- Evidence:")
            for hit in result["evidence"]:
                lines.append(f"  {_render_source_hit(hit)}")
        else:
            lines.append("- Evidence: None")
        lines.append("")

    lines.extend(
        [
            "## Operator Notes",
            "- Carry forward any blockers, approvals, descopes, and human checkpoint references recovered above before the next stage proceeds.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_context_report(
    *,
    root: Path,
    output_path: Path,
    profile: str,
    scope: str,
    focus_terms: Sequence[str] | None = None,
    trace_ids: Sequence[str] | None = None,
    fallback_scopes: Sequence[str] | None = None,
    required_refs: Sequence[str] | None = None,
    additional_queries: Sequence[str] | None = None,
    limit: int = DEFAULT_REPORT_QUERY_LIMIT,
    db_path: Path | None = None,
    fail_on_weak_coverage: bool = False,
) -> dict[str, Any]:
    profile_definition = _profile_definition(profile)
    focus_terms = _dedupe_preserve_order(focus_terms or [])
    trace_ids = _dedupe_preserve_order(trace_ids or [])
    required_refs = _dedupe_preserve_order(required_refs or [])
    queries = _dedupe_preserve_order(
        list(profile_definition["default_queries"]) + list(additional_queries or []) + list(focus_terms)
    )
    requested_scope = scope
    attempted_scopes = _dedupe_preserve_order([requested_scope] + list(fallback_scopes or []) + list(profile_definition["fallback_scopes"]))

    db = _open_index(root, db_path)
    try:
        attempts = [
            _collect_report_attempt(
                root=root,
                db=db,
                scope=attempt_scope,
                queries=queries,
                trace_ids=trace_ids,
                required_refs=required_refs,
                limit=limit,
            )
            for attempt_scope in attempted_scopes
        ]
    finally:
        db.close()

    sufficient_attempt = next(
        (attempt for attempt in attempts if attempt["coverage_verdict"] == "SUFFICIENT"),
        None,
    )
    if sufficient_attempt is not None:
        selected = sufficient_attempt
    else:
        selected = max(attempts, key=_attempt_score)

    generated_at = _utc_now()
    output_abs = output_path if output_path.is_absolute() else root / output_path
    output_abs.parent.mkdir(parents=True, exist_ok=True)
    report = _render_context_report(
        profile=profile,
        profile_label=profile_definition["label"],
        guidance=profile_definition["guidance"],
        requested_scope=requested_scope,
        effective_scope=selected["scope"],
        attempted_scopes=attempted_scopes,
        fallback_applied=selected["scope"] != requested_scope,
        coverage_verdict=selected["coverage_verdict"],
        source_index=str(_resolve_context_db_path(root, db_path)),
        generated_at=generated_at,
        focus_terms=focus_terms,
        trace_ids=trace_ids,
        required_refs=required_refs,
        attempt=selected,
    )
    output_abs.write_text(report, encoding="utf-8")

    payload = {
        "output_path": str(output_abs),
        "profile": profile,
        "requested_scope": requested_scope,
        "effective_scope": selected["scope"],
        "attempted_scopes": attempted_scopes,
        "coverage_verdict": selected["coverage_verdict"],
        "query_count": len(queries),
        "trace_count": len(trace_ids),
        "required_ref_count": len(required_refs),
        "generated_at_utc": generated_at,
    }
    if fail_on_weak_coverage and selected["coverage_verdict"] == "WEAK":
        raise FactoryContextIndexError(
            f"context recall report written with WEAK coverage: {output_abs}"
        )
    return payload
