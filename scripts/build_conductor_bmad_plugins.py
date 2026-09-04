#!/usr/bin/env python3
"""Generate Claude and Codex Factory BMAD packages from one authored source."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "plugin-src/conductor-bmad"
PACKAGE_ROOTS = {
    "codex": REPO_ROOT / "plugins/conductor-bmad",
    "claude": REPO_ROOT / "plugins/conductor-bmad-claude",
}
SKILL_IDS = {"doctor", "bootstrap", "audit", "promote", "intake"}


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_manifest() -> dict[str, Any]:
    manifest = json.loads((SOURCE_ROOT / "manifest.json").read_text(encoding="utf-8"))
    ids = [skill["id"] for skill in manifest["skills"]]
    if set(ids) != SKILL_IDS or len(ids) != len(SKILL_IDS):
        raise ValueError("companion manifest must contain each approved skill exactly once")
    for skill_id in ids:
        if not (SOURCE_ROOT / "skills" / skill_id / "SKILL.md").is_file():
            raise ValueError(f"missing source skill: {skill_id}")
    return manifest


def skill_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3:
        raise ValueError(f"invalid skill frontmatter: {path}")
    return parts[2].lstrip()


def skill_text(name: str, description: str, body: str) -> str:
    return f"---\nname: {name}\ndescription: {description.strip()}\n---\n\n{body.rstrip()}\n"


def openai_yaml(source: Path, generated_name: str, display_name: str) -> str:
    text = source.read_text(encoding="utf-8")
    text = re.sub(r'^\s*display_name:.*$', f'  display_name: "{display_name}"', text, flags=re.MULTILINE)
    text = re.sub(r'\$[a-z-]+', f'${generated_name}', text)
    return text.rstrip() + "\n"


def write_package(root: Path, platform: str, manifest: dict[str, Any]) -> None:
    (root / "skills").mkdir(parents=True)
    (root / "scripts").mkdir()
    (root / "assets/project-adapter").mkdir(parents=True)
    for skill in manifest["skills"]:
        skill_id = skill["id"]
        generated = f"conductor-bmad-{skill_id}" if platform == "codex" else skill_id
        destination = root / "skills" / generated
        destination.mkdir()
        source = SOURCE_ROOT / "skills" / skill_id
        (destination / "SKILL.md").write_text(
            skill_text(generated, skill["description"], skill_body(source / "SKILL.md")),
            encoding="utf-8",
        )
        if platform == "codex":
            (destination / "agents").mkdir()
            display = f"Factory BMAD {skill_id.title()}"
            (destination / "agents/openai.yaml").write_text(
                openai_yaml(source / "agents/openai.yaml", generated, display), encoding="utf-8"
            )
    shutil.copyfile(SOURCE_ROOT / "runtime/conductor_bmad.py", root / "scripts/conductor_bmad.py")
    shutil.copyfile(SOURCE_ROOT / "runtime/conductor_bmad_policy.py", root / "scripts/conductor_bmad_policy.py")
    for source in sorted((SOURCE_ROOT / "project-adapter").iterdir()):
        if source.is_file():
            shutil.copy2(source, root / "assets/project-adapter" / source.name)
    shutil.copyfile(
        SOURCE_ROOT / "runtime/conductor_bmad_policy.py",
        root / "assets/project-adapter/conductor_bmad_policy.py",
    )
    if platform == "codex":
        plugin = {
            "name": manifest["name"], "version": manifest["version"],
            "description": manifest["description"], "author": manifest["author"],
            "skills": "./skills/", "interface": {**manifest["interface"], "capabilities": []},
        }
        destination = root / ".codex-plugin/plugin.json"
    else:
        plugin = {
            "name": manifest["name"], "version": manifest["version"],
            "description": manifest["description"], "author": manifest["author"],
            "dependencies": [{"name": "conductor", "version": manifest["conductor_dependency"]}],
        }
        destination = root / ".claude-plugin/plugin.json"
        (root / "hooks").mkdir()
        shutil.copyfile(SOURCE_ROOT / "hooks/hooks.json", root / "hooks/hooks.json")
    destination.parent.mkdir()
    destination.write_text(json_text(plugin), encoding="utf-8")
    files = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.name == "OWNERSHIP.json":
            continue
        files.append({"path": path.relative_to(root).as_posix(), "sha256": sha256(path), "classification": "release-owned"})
    ownership = {
        "schema_version": 1, "package": manifest["name"], "version": manifest["version"],
        "generated_from": "plugin-src/conductor-bmad", "files": files,
    }
    (root / "OWNERSHIP.json").write_text(json_text(ownership), encoding="utf-8")


def tree(root: Path) -> dict[Path, bytes]:
    return {path.relative_to(root): path.read_bytes() for path in root.rglob("*") if path.is_file()}


def build(check: bool) -> bool:
    manifest = load_manifest()
    with tempfile.TemporaryDirectory(prefix="conductor-bmad-build-") as temporary:
        staging = Path(temporary)
        for platform in PACKAGE_ROOTS:
            write_package(staging / platform, platform, manifest)
        if check:
            stale = [name for name, path in PACKAGE_ROOTS.items() if not path.exists() or tree(path) != tree(staging / name)]
            if stale:
                print(f"Factory BMAD packages are stale: {', '.join(stale)}")
                return False
            print("Factory BMAD packages are current.")
            return True
        for platform, destination in PACKAGE_ROOTS.items():
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(staging / platform, destination)
    print("Generated Factory BMAD packages for Claude and Codex.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    return 0 if build(parser.parse_args().check) else 1


if __name__ == "__main__":
    raise SystemExit(main())
