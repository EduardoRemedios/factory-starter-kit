#!/usr/bin/env python3
"""Generate Claude and Codex Factory plugin packages from one authored source."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "plugin-src" / "conductor"
PACKAGE_ROOTS = {
    "codex": REPO_ROOT / "plugins" / "conductor",
    "claude": REPO_ROOT / "plugins" / "conductor-claude",
}
ALLOWED_SKILL_IDS = {
    "brownfield",
    "doctor",
    "greenfield",
    "progress",
    "run",
    "update",
    "validate",
}
PROJECT_OWNED_SEEDS = {
    Path("AGENTS.md"): Path("AGENTS.md"),
    Path("docs/CHANGELOG.md"): Path(
        "plugin-src/conductor/project-seeds/docs/CHANGELOG.md"
    ),
    Path("docs/PROJECT_STATE.md"): Path(
        "plugin-src/conductor/project-seeds/docs/PROJECT_STATE.md"
    ),
    Path("docs/ROADMAP.md"): Path(
        "plugin-src/conductor/project-seeds/docs/ROADMAP.md"
    ),
    Path("docs/Conductor/SCRATCHPAD.md"): Path(
        "plugin-src/conductor/project-seeds/docs/Conductor/SCRATCHPAD.md"
    ),
    Path("docs/Conductor/PROJECT_CONFIG.json"): Path(
        "plugin-src/conductor/project-seeds/docs/Conductor/PROJECT_CONFIG.json"
    ),
}


def load_manifest() -> dict[str, Any]:
    manifest = json.loads((SOURCE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    skill_ids = [skill["id"] for skill in manifest["skills"]]
    if set(skill_ids) != ALLOWED_SKILL_IDS or len(skill_ids) != len(ALLOWED_SKILL_IDS):
        raise ValueError("manifest skills must contain each approved public skill exactly once")
    for skill_id in skill_ids:
        if not skill_id.replace("-", "").isalnum() or skill_id.startswith("-"):
            raise ValueError(f"unsafe skill id: {skill_id!r}")
        if not (SOURCE_ROOT / "skills" / f"{skill_id}.md").is_file():
            raise ValueError(f"missing authored skill body: {skill_id}")
    return manifest


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def skill_text(name: str, description: str, body: str) -> str:
    safe_description = description.replace("\n", " ").strip()
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {safe_description}\n"
        "---\n\n"
        f"{body.rstrip()}\n"
    )


def payload_sources() -> list[tuple[Path, Path, str]]:
    sources: dict[Path, tuple[Path, str]] = {
        destination: (source, "project-owned")
        for destination, source in PROJECT_OWNED_SEEDS.items()
    }
    sources[Path("requirements.txt")] = (Path("requirements.txt"), "release-owned")

    for base in (Path("docs/Conductor"), Path("docs/onboarding")):
        for source in sorted((REPO_ROOT / base).rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(REPO_ROOT)
            if relative in PROJECT_OWNED_SEEDS:
                continue
            if (
                "runs" in relative.parts
                or "Research" in relative.parts
                or "installation" in relative.parts
            ):
                continue
            if "phases" in relative.parts:
                continue
            if "DESIGN_PACK" in relative.parts or relative.name == "CONDUCTOR_DESIGN_BRIEF.md":
                continue
            sources[relative] = (relative, "release-owned")

    for source in sorted((REPO_ROOT / "scripts").iterdir()):
        if (
            source.is_file()
            and source.name not in {
                "build_conductor_plugins.py",
                "build_conductor_bmad_plugins.py",
            }
            and not (
                source.name.startswith("verify_conductor_bmad_")
                and source.suffix in {".py", ".sh"}
            )
        ):
            relative = source.relative_to(REPO_ROOT)
            sources[relative] = (relative, "release-owned")

    for base in (
        Path(".agents/skills"),
        Path("tests/fixtures"),
        Path("tools/repo_cartographer"),
    ):
        if not (REPO_ROOT / base).is_dir():
            continue
        for source in sorted((REPO_ROOT / base).rglob("*")):
            if source.is_file() and (
                base != Path(".agents/skills")
                or source.parent.name.startswith("conductor-")
            ) and "__pycache__" not in source.parts:
                relative = source.relative_to(REPO_ROOT)
                sources[relative] = (relative, "release-owned")

    recall_test = Path("tests/test_context_recall_repair.py")
    sources[recall_test] = (recall_test, "release-owned")

    missing = [source for source, _ in sources.values() if not (REPO_ROOT / source).is_file()]
    if missing:
        raise ValueError(f"missing payload sources: {missing}")
    return [
        (destination, source, classification)
        for destination, (source, classification) in sorted(
            sources.items(), key=lambda item: item[0].as_posix()
        )
    ]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_payload(package_root: Path, manifest: dict[str, Any]) -> None:
    payload_root = package_root / "payload"
    entries: list[dict[str, str]] = []
    for relative, source_relative, classification in payload_sources():
        source = REPO_ROOT / source_relative
        destination = payload_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        entries.append(
            {
                "path": relative.as_posix(),
                "classification": classification,
                "sha256": sha256(source),
            }
        )
    ownership = {
        "schema_version": 1,
        "package": manifest["name"],
        "version": manifest["version"],
        "files": entries,
    }
    (payload_root / "OWNERSHIP.json").write_text(
        json_text(ownership), encoding="utf-8"
    )


def write_packages(staging_root: Path, manifest: dict[str, Any]) -> None:
    for platform in PACKAGE_ROOTS:
        package_root = staging_root / platform
        (package_root / "skills").mkdir(parents=True)
        (package_root / "scripts").mkdir()

        for skill in manifest["skills"]:
            skill_id = skill["id"]
            generated_name = f"conductor-{skill_id}" if platform == "codex" else skill_id
            body = (SOURCE_ROOT / "skills" / f"{skill_id}.md").read_text(encoding="utf-8")
            skill_dir = package_root / "skills" / generated_name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                skill_text(generated_name, skill["description"], body),
                encoding="utf-8",
            )

        runtime = SOURCE_ROOT / "runtime" / "conductor_plugin.py"
        shutil.copyfile(runtime, package_root / "scripts" / "conductor_plugin.py")
        shutil.copyfile(REPO_ROOT / "LICENSE", package_root / "LICENSE")
        write_payload(package_root, manifest)

        if platform == "codex":
            plugin_manifest = {
                "name": manifest["name"],
                "version": manifest["version"],
                "description": manifest["description"],
                "author": manifest["author"],
                "skills": "./skills/",
                "interface": {
                    **manifest["interface"],
                    "capabilities": [],
                },
            }
            manifest_path = package_root / ".codex-plugin" / "plugin.json"
        else:
            plugin_manifest = {
                "name": manifest["name"],
                "version": manifest["version"],
                "description": manifest["description"],
                "author": manifest["author"],
            }
            manifest_path = package_root / ".claude-plugin" / "plugin.json"

        manifest_path.parent.mkdir()
        manifest_path.write_text(json_text(plugin_manifest), encoding="utf-8")
        ownership = {
            "schema_version": 1,
            "package": manifest["name"],
            "version": manifest["version"],
            "classification": "release-owned",
            "generated_from": "plugin-src/conductor",
        }
        (package_root / "OWNERSHIP.json").write_text(json_text(ownership), encoding="utf-8")


def replace_packages(staging_root: Path) -> None:
    for platform, destination in PACKAGE_ROOTS.items():
        source = staging_root / platform
        if destination.parent != REPO_ROOT / "plugins":
            raise RuntimeError(f"refusing unsafe package destination: {destination}")
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)


def build(check: bool) -> bool:
    manifest = load_manifest()
    with tempfile.TemporaryDirectory(prefix="conductor-plugin-build-") as temp_dir:
        staging_root = Path(temp_dir)
        write_packages(staging_root, manifest)
        if check:
            mismatches = [
                platform
                for platform, destination in PACKAGE_ROOTS.items()
                if not destination.exists()
                or not directories_equal(staging_root / platform, destination)
            ]
            if mismatches:
                print(f"Factory plugin packages are stale: {', '.join(mismatches)}")
                return False
            print("Factory plugin packages are current.")
            return True
        replace_packages(staging_root)
    print("Generated Factory plugin packages for Claude and Codex.")
    return True


def directories_equal(left: Path, right: Path) -> bool:
    left_files = {
        path.relative_to(left): path.read_bytes()
        for path in left.rglob("*")
        if path.is_file()
    }
    right_files = {
        path.relative_to(right): path.read_bytes()
        for path in right.rglob("*")
        if path.is_file()
    }
    return left_files == right_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if generated packages differ from the authored source",
    )
    args = parser.parse_args()
    return 0 if build(args.check) else 1


if __name__ == "__main__":
    raise SystemExit(main())
