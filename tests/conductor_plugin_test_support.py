from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


REPO_ROOT = Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / "tests" / "plugin_fixtures"
BASELINE_PATH = FIXTURES_DIR / "protected_baseline.json"

KNOWN_CONSTRAINT_IDS = {f"C-{index:02d}" for index in range(1, 17)}
REQUIRED_FIXTURE_FAMILIES = {
    "environment",
    "harness_parity",
    "instruction_bridge",
    "pilot_scorecard",
    "plugin_build",
    "repository_setup",
    "skill_coexistence",
    "status",
    "update_rollback",
}


def iter_golden_files() -> Iterator[Path]:
    yield from sorted(FIXTURES_DIR.glob("*/golden.json"))


def load_json(path: Path) -> dict[str, Any]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return loaded


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()
