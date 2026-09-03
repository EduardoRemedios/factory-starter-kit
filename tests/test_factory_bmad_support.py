import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_PATH = REPO_ROOT / "plugin-src/factory-bmad/runtime/factory_bmad.py"
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("factory_bmad_runtime", RUNTIME_PATH)
runtime = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = runtime
SPEC.loader.exec_module(runtime)


def seed_git(root: Path) -> None:
    (root / ".git").mkdir(exist_ok=True)


def seed_factory(root: Path) -> None:
    (root / "docs/Factory").mkdir(parents=True, exist_ok=True)
    (root / "docs/Factory/ARCHITECTURE.md").write_text("# Factory\n", encoding="utf-8")
    (root / "scripts").mkdir(exist_ok=True)
    (root / "scripts/factoryctl").write_text("#!/bin/sh\n", encoding="utf-8")


def seed_bmad(root: Path, modules: dict[str, str] | None = None, *, capabilities: bool = False) -> Path:
    modules = modules or {"core": "6.10.0", "bmm": "6.10.0"}
    path = root / "_bmad/_config/manifest.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["installation:", "  version: 6.10.0", "modules:"]
    for name, version in modules.items():
        lines.extend([f"- name: {name}", f"  version: {version}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    if capabilities:
        for name in runtime.SUPPORTED_BMAD_SKILLS:
            skill = root / ".claude" / "skills" / name / "SKILL.md"
            skill.parent.mkdir(parents=True, exist_ok=True)
            skill.write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
        if "tea" in modules:
            for name in runtime.SUPPORTED_TEA_SKILLS:
                skill = root / ".claude" / "skills" / name / "SKILL.md"
                skill.parent.mkdir(parents=True, exist_ok=True)
                skill.write_text(f"---\nname: {name}\n---\n", encoding="utf-8")
    return path


def seed_nested_bmad(root: Path, modules: dict[str, str] | None = None, *, capabilities: bool = False) -> Path:
    return seed_bmad(root / "bmad", modules, capabilities=capabilities)
