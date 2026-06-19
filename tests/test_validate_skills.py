"""Ensure all skill metadata passes validation."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_skills.py"


class ValidateSkillsIntegrationTests(unittest.TestCase):
    def test_all_skills_valid_default_mode(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--json"],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, f"Validation failed:\n{result.stdout}")
        self.assertEqual(payload["error_count"], 0, payload.get("issues"))


class ValidateSkillsUnitTests(unittest.TestCase):
    def setUp(self) -> None:
        from scripts import validate_skills as vs

        self.vs = vs

    def test_verification_present_no_warn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True)
            skill_dir.joinpath("SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: x\nportable: true\nversion: 0.1.0\nscope_class: repo-governed\n---\n\n"
                "## Verification / Proof Standard\n\n- ok\n",
                encoding="utf-8",
            )
            (root / "skills" / "manifest.yaml").write_text(
                "skills:\n  - name: demo-skill\n    source: demo-skill/SKILL.md\n",
                encoding="utf-8",
            )
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate()
            finally:
                self.vs.REPO_ROOT = orig
        verification_issues = [
            i for i in issues if "Verification" in i["message"] and i["path"].endswith("demo-skill/SKILL.md")
        ]
        self.assertEqual(verification_issues, [])

    def test_strict_verification_fails_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True)
            skill_dir.joinpath("SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: x\nportable: true\nversion: 0.1.0\n---\n\n# Body\n",
                encoding="utf-8",
            )
            (root / "skills" / "manifest.yaml").write_text(
                "skills:\n  - name: demo-skill\n    source: demo-skill/SKILL.md\n",
                encoding="utf-8",
            )
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate(strict_verification=True)
            finally:
                self.vs.REPO_ROOT = orig
        errors = [i for i in issues if i["level"] == "error" and "strict-verification" in i["message"]]
        self.assertTrue(errors)

    def test_invalid_scope_class_errors(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True)
            skill_dir.joinpath("SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: x\nportable: true\nversion: 0.1.0\nscope_class: invalid\n---\n\n# Body\n",
                encoding="utf-8",
            )
            (root / "skills" / "manifest.yaml").write_text(
                "skills:\n  - name: demo-skill\n    source: demo-skill/SKILL.md\n",
                encoding="utf-8",
            )
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate()
            finally:
                self.vs.REPO_ROOT = orig
        errors = [i for i in issues if i["level"] == "error" and "scope_class" in i["message"]]
        self.assertTrue(errors)

    def test_manifest_scope_mismatch_warns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "demo-skill"
            skill_dir.mkdir(parents=True)
            skill_dir.joinpath("SKILL.md").write_text(
                "---\nname: demo-skill\ndescription: x\nportable: true\nversion: 0.1.0\nscope_class: repo-governed\n---\n\n# Body\n",
                encoding="utf-8",
            )
            (root / "skills" / "manifest.yaml").write_text(
                "skills:\n  - name: demo-skill\n    source: demo-skill/SKILL.md\n    scope_class: personal\n",
                encoding="utf-8",
            )
            orig = self.vs.REPO_ROOT
            self.vs.REPO_ROOT = root
            try:
                issues = self.vs.validate()
            finally:
                self.vs.REPO_ROOT = orig
        warns = [i for i in issues if i["level"] == "warn" and "differs from manifest" in i["message"]]
        self.assertTrue(warns)


if __name__ == "__main__":
    unittest.main()
