from __future__ import annotations

import hashlib
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from factory_context_index import build_context_index, describe_context  # noqa: E402


class FactoryUpstreamContextTests(unittest.TestCase):
    def test_promoted_markdown_is_indexed_as_upstream_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            self._write(root / "docs/upstream/research/product-brief.md", "# Product Brief\n\nPromoted evidence.\n")
            self._write(root / "_bmad-output/product-brief.md", "# Draft Brief\n\nUnpromoted draft.\n")
            db_path = root / "context.sqlite3"

            build_context_index(root=root, db_path=db_path)
            description = describe_context(root=root, db_path=db_path)

            self.assertEqual(1, description["source_count"])
            self.assertEqual({"upstream_evidence": 1}, description["artifact_counts"])
            self.assertEqual(
                ["docs/upstream/research/product-brief.md"],
                description["sources"],
            )

    def test_order_and_content_digests_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            contents = {
                "docs/upstream/z-last.md": "# Last\n\nZ evidence.\n",
                "docs/upstream/a-first.md": "# First\n\nA evidence.\n",
            }
            for relative, text in contents.items():
                self._write(root / relative, text)
            db_path = root / "context.sqlite3"

            build_context_index(root=root, db_path=db_path)
            first = self._source_rows(db_path)
            build_context_index(root=root, db_path=db_path)
            second = self._source_rows(db_path)

            expected = [
                (
                    relative,
                    "upstream_evidence",
                    hashlib.sha256(text.encode("utf-8")).hexdigest(),
                )
                for relative, text in sorted(contents.items())
            ]
            self.assertEqual(expected, first)
            self.assertEqual(first, second)

    def _write(self, path: Path, text: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def _source_rows(self, db_path: Path) -> list[tuple[str, str, str]]:
        with sqlite3.connect(db_path) as connection:
            return connection.execute(
                "SELECT path, artifact_type, content_sha FROM sources ORDER BY path"
            ).fetchall()


if __name__ == "__main__":
    unittest.main()
