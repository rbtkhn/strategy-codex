from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from yaml_compat import safe_load_text

try:
    from scrub_skill_mojibake import control_char_issues, marker_count
except ModuleNotFoundError:  # pragma: no cover - script invoked as module
    from scripts.scrub_skill_mojibake import control_char_issues, marker_count  # type: ignore

FRONTMATTER_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
SKILL_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+/SKILL\.md)\)")

@dataclass(frozen=True)
class Issue:
    skill: str
    kind: str
    detail: str

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Audit a mounted Codex skill directory for unresolved frontmatter "
            "dependencies and broken relative links to other mounted skills."
        )
    )
    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path.home() / ".codex" / "skills",
        help="Mounted skills directory to audit (default: %(default)s).",
    )
    parser.add_argument(
        "--include-system",
        action="store_true",
        help="Include dot-prefixed skill directories such as .system.",
    )
    return parser.parse_args()

def iter_skill_files(skills_dir: Path, *, include_system: bool) -> Iterable[Path]:
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir():
            continue
        if not include_system and child.name.startswith("."):
            continue
        skill_file = child / "SKILL.md"
        if skill_file.exists():
            yield skill_file

def extract_frontmatter(text: str, *, feature: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data = safe_load_text(match.group(1), feature=feature)
    return data if isinstance(data, dict) else {}

def normalize_requires(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []

def collect_issues(skill_file: Path, mounted_skill_names: set[str]) -> list[Issue]:
    text = skill_file.read_text(encoding="utf-8")
    skill_name = skill_file.parent.name
    issues: list[Issue] = []

    frontmatter = extract_frontmatter(text, feature=f"frontmatter parse for {skill_name}")
    for required in normalize_requires(frontmatter.get("requires")):
        if required not in mounted_skill_names:
            issues.append(
                Issue(
                    skill=skill_name,
                    kind="missing-requires",
                    detail=f"requires '{required}' but it is not mounted",
                )
            )

    seen_targets: set[str] = set()
    for raw_target in SKILL_LINK_RE.findall(text):
        target = raw_target.strip()
        if target in seen_targets:
            continue
        seen_targets.add(target)
        if "://" in target or target.startswith("/"):
            continue
        resolved = (skill_file.parent / target).resolve()
        if not resolved.exists():
            issues.append(
                Issue(
                    skill=skill_name,
                    kind="broken-skill-link",
                    detail=f"links to missing skill file '{target}'",
                )
            )
    return issues

def collect_encoding_issues(skill_file: Path) -> list[Issue]:
    text = skill_file.read_text(encoding="utf-8")
    skill_name = skill_file.parent.name
    issues: list[Issue] = []

    count = marker_count(text)
    if count:
        issues.append(
            Issue(
                skill=skill_name,
                kind="encoding-mojibake",
                detail=f"{count} mojibake marker hit(s); run scripts/scrub_skill_mojibake.py",
            )
        )

    for detail in control_char_issues(text):
        issues.append(
            Issue(
                skill=skill_name,
                kind="encoding-control-char",
                detail=detail,
            )
        )
    return issues

def main() -> int:
    args = parse_args()
    skills_dir: Path = args.skills_dir

    if not skills_dir.exists():
        print(f"skills directory not found: {skills_dir}", file=sys.stderr)
        return 2
    if not skills_dir.is_dir():
        print(f"skills path is not a directory: {skills_dir}", file=sys.stderr)
        return 2

    skill_files = list(iter_skill_files(skills_dir, include_system=args.include_system))
    mounted_skill_names = {path.parent.name for path in skill_files}

    issues: list[Issue] = []
    for skill_file in skill_files:
        issues.extend(collect_issues(skill_file, mounted_skill_names))
        issues.extend(collect_encoding_issues(skill_file))

    print(f"Mounted skills directory: {skills_dir}")
    print(f"Audited skills: {len(skill_files)}")
    print(f"Issues: {len(issues)}")

    if not issues:
        print("OK: no unresolved mounted-skill dependencies, broken relative skill links, or encoding issues found.")
        return 0

    for issue in issues:
        print(f"- [{issue.kind}] {issue.skill}: {issue.detail}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
