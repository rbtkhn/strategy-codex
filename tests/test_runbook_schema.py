"""Runbook schema validation tests."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

class RunbookSchemaTests(unittest.TestCase):
    def setUp(self) -> None:
        from scripts import validate_skills as vs

        self.vs = vs

    def _minimal_runbook(self, *, skills: list[str] | None = None, omit_section: str | None = None) -> str:
        skills = skills or ["statecraft-source-intake"]
        sections = [
            ("Purpose", "Produce X."),
            ("Trigger", "Use when..."),
            ("Skills Composed", "| Step | Skill | Role |\n| 1 | a | b |"),
            ("Inputs Required", "- input"),
            ("Workflow Steps", "1. step"),
            ("Human Approval Points", "- before merge"),
            ("Stop Conditions", "- missing source"),
            ("Verification / Proof Standard", "- archive exists"),
            ("Outputs", "- output"),
            ("Return Paths", "- skills/README.md"),
        ]
        body_parts = []
        for title, content in sections:
            if omit_section and title.lower() == omit_section.lower():
                continue
            body_parts.append(f"## {title}\n\n{content}\n")
        body = "\n".join(body_parts)
        skills_yaml = "\n".join(f"  - {s}" for s in skills)
        return f"""---
name: test-runbook
description: Test runbook
portable: true
version: 0.1.0
scope_class: repo-governed
skills:
{skills_yaml}
outputs:
  - out
authority: advisory_only
---

# Test Runbook

{body}
"""

    def test_valid_runbook_in_repo_passes(self) -> None:
        runbooks = list((REPO_ROOT / "skills" / "runbooks").glob("*.runbook.md"))
        if not runbooks:
            self.skipTest("No runbooks yet")
        issues = self.vs.validate()
        runbook_errors = [
            i
            for i in issues
            if i["level"] == "error" and "runbooks" in i["path"] and i["path"].endswith(".runbook.md")
        ]
        self.assertEqual(runbook_errors, [], runbook_errors)

    def test_missing_section_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rb_dir = root / "skills" / "runbooks"
            rb_dir.mkdir(parents=True)
            rb_dir.joinpath("bad.runbook.md").write_text(
                self._minimal_runbook(omit_section="Stop Conditions"),
                encoding="utf-8",
            )
            (root / "skills" / "manifest.yaml").write_text("skills: []\n", encoding="utf-8")
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate()
            finally:
                self.vs.REPO_ROOT = orig
        errors = [i for i in issues if "Stop Conditions" in i["message"]]
        self.assertTrue(errors)

    def test_bad_skill_reference_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rb_dir = root / "skills" / "runbooks"
            rb_dir.mkdir(parents=True)
            rb_dir.joinpath("bad.runbook.md").write_text(
                self._minimal_runbook(skills=["nonexistent-skill-xyz"]),
                encoding="utf-8",
            )
            (root / "skills" / "manifest.yaml").write_text("skills: []\n", encoding="utf-8")
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate()
            finally:
                self.vs.REPO_ROOT = orig
        errors = [i for i in issues if "nonexistent-skill-xyz" in i["message"]]
        self.assertTrue(errors)

    def test_forbidden_authority_phrase_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rb_dir = root / "skills" / "runbooks"
            rb_dir.mkdir(parents=True)
            text = self._minimal_runbook()
            text = text.replace("Produce X.", "This workflow supports silent merge of Record.")
            rb_dir.joinpath("bad.runbook.md").write_text(text, encoding="utf-8")
            (root / "skills" / "manifest.yaml").write_text("skills: []\n", encoding="utf-8")
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate()
            finally:
                self.vs.REPO_ROOT = orig
        errors = [i for i in issues if "silent merge" in i["message"].lower() or "authority" in i["message"].lower()]
        self.assertTrue(errors)

if __name__ == "__main__":
    unittest.main()
