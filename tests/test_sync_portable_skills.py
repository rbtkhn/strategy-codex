from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import sync_portable_skills as sps

class SyncPortableSkillsTests(unittest.TestCase):
    def test_parse_yaml_subset_supports_manifest_shape(self) -> None:
        text = """skills:
  - name: demo-skill
    source: demo/SKILL.md
    appendix: .cursor/skills/demo/CURSOR_APPENDIX.md
    target: .cursor/skills/demo/SKILL.md
    verify_forbidden_substrings:
      - platform/users/grace-mar/
      - process_approved_candidates
"""
        data = sps._parse_yaml_subset(text)
        self.assertEqual(data["skills"][0]["name"], "demo-skill")
        self.assertEqual(
            data["skills"][0]["verify_forbidden_substrings"],
            ["platform/users/grace-mar/", "process_approved_candidates"],
        )

    def test_parse_yaml_subset_rejects_block_scalars(self) -> None:
        text = """description: >
  wrapped
  text
"""
        with self.assertRaisesRegex(ValueError, "Unsupported YAML subset"):
            sps._parse_yaml_subset(text)

    def test_parse_yaml_subset_rejects_inline_collections(self) -> None:
        text = "skills: [demo-skill]\n"
        with self.assertRaisesRegex(ValueError, "Unsupported YAML subset"):
            sps._parse_yaml_subset(text)

    def test_scope_class_preserved_in_generated_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "skills" / "demo-skill" / "SKILL.md"
            src.parent.mkdir(parents=True)
            src.write_text(
                "---\nname: demo-skill\ndescription: Demo skill for sync test\nportable: true\nversion: 0.1.0\nscope_class: repo-governed\n---\n\n# Demo\n",
                encoding="utf-8",
            )
            apx = root / ".cursor" / "skills" / "demo-skill" / "CURSOR_APPENDIX.md"
            apx.parent.mkdir(parents=True)
            apx.write_text("Host paths here.\n", encoding="utf-8")
            tgt = root / ".cursor" / "skills" / "demo-skill" / "SKILL.md"

            entry = {
                "name": "demo-skill",
                "source": "demo-skill/SKILL.md",
                "appendix": ".cursor/skills/demo-skill/CURSOR_APPENDIX.md",
                "target": ".cursor/skills/demo-skill/SKILL.md",
            }

            orig_repo = sps._REPO
            sps._REPO = root
            try:
                status, errs = sps.sync_one(entry, dry_run=False, verify_only=False)
            finally:
                sps._REPO = orig_repo

            self.assertEqual(status, "ok", errs)
            self.assertFalse(errs)
            out = tgt.read_text(encoding="utf-8")
            self.assertIn("scope_class: repo-governed", out)
            self.assertIn("## Cursor / strategy-codex instance", out)
            self.assertNotIn("grace-mar instance", out)

    def test_appendix_does_not_override_scope_class(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src = root / "skills" / "demo-skill" / "SKILL.md"
            src.parent.mkdir(parents=True)
            src.write_text(
                "---\nname: demo-skill\ndescription: Demo skill for sync test\nportable: true\nversion: 0.1.0\nscope_class: repo-governed\n---\n\n# Demo\n",
                encoding="utf-8",
            )
            apx = root / ".cursor" / "skills" / "demo-skill" / "CURSOR_APPENDIX.md"
            apx.parent.mkdir(parents=True)
            apx.write_text("scope_class: personal\n", encoding="utf-8")
            tgt = root / ".cursor" / "skills" / "demo-skill" / "SKILL.md"

            entry = {
                "name": "demo-skill",
                "source": "demo-skill/SKILL.md",
                "appendix": ".cursor/skills/demo-skill/CURSOR_APPENDIX.md",
                "target": ".cursor/skills/demo-skill/SKILL.md",
            }

            orig_repo = sps._REPO
            sps._REPO = root
            try:
                status, errs = sps.sync_one(entry, dry_run=False, verify_only=False)
            finally:
                sps._REPO = orig_repo

            self.assertEqual(status, "ok", errs)
            out = tgt.read_text(encoding="utf-8")
            fm_block = out.split("---")[1] if out.count("---") >= 2 else ""
            self.assertIn("scope_class: repo-governed", fm_block)
            self.assertNotIn("scope_class: personal", fm_block)
            self.assertIn("scope_class: personal", out.split("## Cursor")[1])  # appendix body only

if __name__ == "__main__":
    unittest.main()
