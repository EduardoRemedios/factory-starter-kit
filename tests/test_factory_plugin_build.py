import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = REPO_ROOT / "plugin-src" / "factory"
PACKAGES = {
    "codex": REPO_ROOT / "plugins" / "factory",
    "claude": REPO_ROOT / "plugins" / "factory-claude",
}


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def body_without_frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    _, _, body = text.split("---", 2)
    return body.lstrip()


class FactoryPluginBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(
            (SOURCE_ROOT / "manifest.json").read_text(encoding="utf-8")
        )
        subprocess.run(
            [sys.executable, "scripts/build_factory_plugins.py", "--check"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_required_manifests_are_present(self):
        self.assertTrue((PACKAGES["codex"] / ".codex-plugin/plugin.json").is_file())
        self.assertTrue((PACKAGES["claude"] / ".claude-plugin/plugin.json").is_file())

    def test_packages_include_open_source_metadata(self):
        license_bytes = (REPO_ROOT / "LICENSE").read_bytes()
        for platform, package in PACKAGES.items():
            manifest_path = (
                package / ".codex-plugin/plugin.json"
                if platform == "codex"
                else package / ".claude-plugin/plugin.json"
            )
            package_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual("Apache-2.0", package_manifest["license"])
            self.assertEqual(
                "https://github.com/EduardoRemedios/factory-starter-kit",
                package_manifest["repository"],
            )
            self.assertEqual(license_bytes, (package / "LICENSE").read_bytes())

    def test_packages_have_exact_public_skill_set(self):
        expected_ids = {skill["id"] for skill in self.manifest["skills"]}
        codex_ids = {
            path.name.removeprefix("factory-")
            for path in (PACKAGES["codex"] / "skills").iterdir()
            if path.is_dir()
        }
        claude_ids = {
            path.name
            for path in (PACKAGES["claude"] / "skills").iterdir()
            if path.is_dir()
        }
        self.assertEqual(expected_ids, codex_ids)
        self.assertEqual(expected_ids, claude_ids)

    def test_shared_skill_bodies_are_equal(self):
        for skill in self.manifest["skills"]:
            skill_id = skill["id"]
            source = (SOURCE_ROOT / "skills" / f"{skill_id}.md").read_text(
                encoding="utf-8"
            )
            codex = body_without_frontmatter(
                PACKAGES["codex"] / "skills" / f"factory-{skill_id}" / "SKILL.md"
            )
            claude = body_without_frontmatter(
                PACKAGES["claude"] / "skills" / skill_id / "SKILL.md"
            )
            self.assertEqual(source, codex)
            self.assertEqual(source, claude)

    def test_second_generation_is_clean(self):
        before = {platform: tree_digest(path) for platform, path in PACKAGES.items()}
        subprocess.run(
            [sys.executable, "scripts/build_factory_plugins.py"],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        after = {platform: tree_digest(path) for platform, path in PACKAGES.items()}
        self.assertEqual(before, after)

    def test_platform_payloads_are_equal(self):
        codex_payload = PACKAGES["codex"] / "payload"
        claude_payload = PACKAGES["claude"] / "payload"
        self.assertEqual(tree_digest(codex_payload), tree_digest(claude_payload))
        self.assertEqual(
            (codex_payload / "OWNERSHIP.json").read_bytes(),
            (claude_payload / "OWNERSHIP.json").read_bytes(),
        )

    def test_project_installation_state_is_not_packaged(self):
        for package in PACKAGES.values():
            self.assertFalse(
                (package / "payload/docs/Factory/installation").exists()
            )

    def test_shared_runtime_is_equal(self):
        source = (SOURCE_ROOT / "runtime" / "factory_plugin.py").read_bytes()
        for package in PACKAGES.values():
            self.assertEqual(source, (package / "scripts" / "factory_plugin.py").read_bytes())


if __name__ == "__main__":
    unittest.main()
