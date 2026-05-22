from __future__ import annotations

import unittest

from scripts import sync_portable_skills as sps


class SyncPortableSkillsTests(unittest.TestCase):
    def test_parse_yaml_subset_supports_manifest_shape(self) -> None:
        text = """skills:
  - name: demo-skill
    source: demo/SKILL.md
    appendix: .cursor/skills/demo/CURSOR_APPENDIX.md
    target: .cursor/skills/demo/SKILL.md
    verify_forbidden_substrings:
      - users/grace-mar/
      - process_approved_candidates
"""
        data = sps._parse_yaml_subset(text)
        self.assertEqual(data["skills"][0]["name"], "demo-skill")
        self.assertEqual(
            data["skills"][0]["verify_forbidden_substrings"],
            ["users/grace-mar/", "process_approved_candidates"],
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


if __name__ == "__main__":
    unittest.main()
