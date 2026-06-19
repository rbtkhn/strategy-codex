"""Cross-host install guide smoke tests."""

from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOC = REPO_ROOT / "docs" / "skills" / "cross-host-install.md"


class CrossHostInstallDocTests(unittest.TestCase):
    def test_doc_exists(self) -> None:
        self.assertTrue(DOC.is_file(), f"Missing {DOC}")

    def test_host_matrix_includes_required_hosts(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        for host in ("Cursor", "Claude Code", "Codex", "ChatGPT", "Generic"):
            self.assertIn(host, text, f"Host matrix missing {host}")

    def test_return_paths_link_skills_readme_and_schema(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("skills/README.md", text)
        self.assertIn("skills/_schema.md", text)


if __name__ == "__main__":
    unittest.main()
