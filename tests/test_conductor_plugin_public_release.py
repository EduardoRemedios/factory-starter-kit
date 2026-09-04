from __future__ import annotations

import hashlib
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = (
    REPO_ROOT / ".agents/plugins",
    REPO_ROOT / ".claude-plugin",
    REPO_ROOT / "plugin-src",
    REPO_ROOT / "plugins",
    REPO_ROOT / "docs/Conductor/Research",
    REPO_ROOT / "docs/onboarding",
    REPO_ROOT / "tests/plugin_fixtures",
)
PUBLIC_FILES = (
    REPO_ROOT / "docs/CHANGELOG.md",
    REPO_ROOT / "docs/PROJECT_STATE.md",
    REPO_ROOT / "docs/ROADMAP.md",
)
FORBIDDEN_TOKEN_HASHES = {
    "0c873ecbd3c57a0116ca9190d67c9d72bc0154efc4f81cca5d11c62181846184",
    "53c1bbe0029caaf6a967a11ce3b7f47251dea40860f3280ea7064c37c4b985c2",
    "b709d82cc6c8b5f012647fc8711dc21bc8449d0be71da3c50678194b0fadd267",
    "3f40462915a3e6026a4d790127b95ded4d870f6ab18d9af2fcbc454168255237",
}


class FactoryPluginPublicReleaseTests(unittest.TestCase):
    def test_public_release_surfaces_do_not_contain_private_context(self):
        files = list(PUBLIC_FILES)
        for root in PUBLIC_ROOTS:
            files.extend(path for path in root.rglob("*") if path.is_file())

        violations: list[str] = []
        for path in sorted(files):
            try:
                text = path.read_text(encoding="utf-8").lower()
            except UnicodeDecodeError:
                continue
            for token in set(re.findall(r"[a-z0-9_]+", text)):
                token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
                if token_hash in FORBIDDEN_TOKEN_HASHES:
                    violations.append(
                        f"{path.relative_to(REPO_ROOT)} contains a blocked private token"
                    )

        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
