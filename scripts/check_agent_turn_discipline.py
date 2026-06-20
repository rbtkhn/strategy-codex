#!/usr/bin/env python3
"""
Scan Cursor agent JSONL transcripts for parallel tool-use violations (Windows harness).

Read-only observability for agent-tool-latency-discipline rules #3 (one Shell per turn)
and #10 (no parallel StrReplace / read+write same path). Does not block live agent turns.

Usage:
  python scripts/check_agent_turn_discipline.py --latest
  python scripts/check_agent_turn_discipline.py --transcript path/to/session.jsonl
  python scripts/check_agent_turn_discipline.py --latest --json --last-turns 30
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

WRITE_TOOLS = frozenset({"Write", "StrReplace", "ApplyPatch", "EditNotebook", "Delete"})
HARD_RULES = frozenset(
    {
        "parallel_shell",
        "parallel_strreplace",
        "same_path_write_parallel",
        "read_write_same_path",
    }
)


@dataclass
class Violation:
    rule_id: str
    turn_index: int
    line_no: int
    detail: str
    severity: str = "hard"  # hard | warn


@dataclass
class DisciplineReport:
    transcript_path: Path | None = None
    assistant_turns_scanned: int = 0
    violations: list[Violation] = field(default_factory=list)
    error: str | None = None

    @property
    def hard_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "hard")

    @property
    def warn_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "warn")


def _configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def normalize_path(raw: str | None) -> str:
    if not raw or not str(raw).strip():
        return ""
    try:
        return str(Path(str(raw)).resolve()).replace("\\", "/").lower()
    except (OSError, ValueError):
        return str(raw).replace("\\", "/").lower()


def _tool_uses(message: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not isinstance(message, dict):
        return []
    content = message.get("content")
    if not isinstance(content, list):
        return []
    out: list[dict[str, Any]] = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_use":
            out.append(block)
    return out


def _tool_path(block: dict[str, Any]) -> str:
    inp = block.get("input")
    if not isinstance(inp, dict):
        return ""
    for key in ("path", "target_notebook", "target_file"):
        val = inp.get(key)
        if val:
            return normalize_path(str(val))
    return ""


def _tool_command_preview(block: dict[str, Any], limit: int = 80) -> str:
    inp = block.get("input")
    if not isinstance(inp, dict):
        return ""
    cmd = inp.get("command")
    if not cmd:
        return ""
    text = " ".join(str(cmd).split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def analyze_assistant_turn(
    turn_index: int,
    line_no: int,
    message: dict[str, Any] | None,
    *,
    strict: bool = False,
) -> list[Violation]:
    uses = _tool_uses(message)
    if not uses:
        return []

    violations: list[Violation] = []
    by_name = Counter(u.get("name") for u in uses)
    shell_count = by_name.get("Shell", 0)
    strreplace_count = by_name.get("StrReplace", 0)
    total = len(uses)

    if shell_count > 1:
        previews = [_tool_command_preview(u) for u in uses if u.get("name") == "Shell"]
        violations.append(
            Violation(
                rule_id="parallel_shell",
                turn_index=turn_index,
                line_no=line_no,
                detail=f"{shell_count} Shell calls: {' | '.join(p for p in previews if p) or 'see transcript'}",
            )
        )

    if strreplace_count > 1:
        paths = [_tool_path(u) for u in uses if u.get("name") == "StrReplace"]
        path_hint = paths[0] if paths else "multiple paths"
        violations.append(
            Violation(
                rule_id="parallel_strreplace",
                turn_index=turn_index,
                line_no=line_no,
                detail=f"{strreplace_count} StrReplace calls (e.g. {path_hint})",
            )
        )

    write_ops: list[tuple[str, str]] = []
    read_paths: set[str] = set()
    for block in uses:
        name = block.get("name") or ""
        path = _tool_path(block)
        if name == "Read" and path:
            read_paths.add(path)
        if name in WRITE_TOOLS and path:
            write_ops.append((name, path))

    if write_ops:
        path_counts = Counter(p for _n, p in write_ops)
        for path, count in path_counts.items():
            if count > 1:
                violations.append(
                    Violation(
                        rule_id="same_path_write_parallel",
                        turn_index=turn_index,
                        line_no=line_no,
                        detail=f"{count} write-class ops on `{path}`",
                    )
                )
        for name, path in write_ops:
            if path in read_paths:
                violations.append(
                    Violation(
                        rule_id="read_write_same_path",
                        turn_index=turn_index,
                        line_no=line_no,
                        detail=f"Read + {name} on `{path}`",
                    )
                )

    write_count = sum(1 for u in uses if u.get("name") in WRITE_TOOLS)
    if write_count > 1 and not any(v.rule_id == "parallel_strreplace" for v in violations):
        severity = "hard" if strict else "warn"
        violations.append(
            Violation(
                rule_id="parallel_write",
                turn_index=turn_index,
                line_no=line_no,
                detail=f"{write_count} write-class tools in one turn",
                severity=severity,
            )
        )

    if total > 8:
        violations.append(
            Violation(
                rule_id="tool_storm",
                turn_index=turn_index,
                line_no=line_no,
                detail=f"{total} tool_use blocks in one turn",
                severity="warn" if not strict else "hard",
            )
        )

    return violations


def find_latest_transcript(
    *,
    project_slug: str = "strategy-codex",
    transcripts_root: Path | None = None,
) -> Path | None:
    root = transcripts_root or (Path.home() / ".cursor" / "projects")
    if not root.is_dir():
        return None
    candidates: list[Path] = []
    for project_dir in root.iterdir():
        if not project_dir.is_dir():
            continue
        if project_slug not in project_dir.name:
            continue
        archive = project_dir / "agent-transcripts"
        if not archive.is_dir():
            continue
        candidates.extend(archive.rglob("*.jsonl"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def scan_transcript(
    path: Path,
    *,
    last_turns: int = 50,
    strict: bool = False,
) -> DisciplineReport:
    report = DisciplineReport(transcript_path=path)
    if not path.is_file():
        report.error = f"transcript not found: {path}"
        return report

    assistant_turns: list[tuple[int, int, dict[str, Any]]] = []
    try:
        with path.open(encoding="utf-8", errors="replace") as fh:
            for line_no, line in enumerate(fh, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("role") != "assistant":
                    continue
                message = row.get("message")
                if isinstance(message, dict):
                    assistant_turns.append((len(assistant_turns), line_no, message))
    except OSError as exc:
        report.error = str(exc)
        return report

    window = assistant_turns[-last_turns:] if last_turns > 0 else assistant_turns
    report.assistant_turns_scanned = len(window)

    for turn_index, line_no, message in window:
        report.violations.extend(
            analyze_assistant_turn(turn_index, line_no, message, strict=strict)
        )

    return report


def format_markdown_lines(report: DisciplineReport) -> list[str]:
    lines = ["## Agent turn discipline", ""]
    if report.error:
        lines.append(f"- **Scan:** skipped — {report.error}")
        lines.append("")
        return lines

    path = report.transcript_path
    rel = str(path) if path else "unknown"
    lines.append(f"- **Transcript:** `{rel}`")
    lines.append(f"- **Assistant turns scanned:** {report.assistant_turns_scanned}")
    lines.append(f"- **Hard violations:** {report.hard_count}")
    if report.warn_count:
        lines.append(f"- **Warnings:** {report.warn_count}")

    hard = [v for v in report.violations if v.severity == "hard"]
    if not hard:
        lines.append("- _No parallel Shell / StrReplace / same-path read+write in window._")
    else:
        lines.append("")
        lines.append("### Violations")
        lines.append("")
        for v in hard[:8]:
            lines.append(
                f"- `{v.rule_id}` @ assistant turn {v.turn_index} (jsonl L{v.line_no}): {v.detail}"
            )
        if len(hard) > 8:
            lines.append(f"- _… and {len(hard) - 8} more_")
        lines.append("")
        lines.append(
            "- **RLJ:** [parallel ban EXECUTE ship](../statecraft/recursive-learning-journal.md"
            "#2026-06-18---parallel-ban-on-file-tools-and-shell-calls-windows-execute-ship)"
        )
        lines.append(
            "- **Re-run:** `python scripts/check_agent_turn_discipline.py --latest`"
        )

    lines.append("")
    return lines


def main() -> int:
    _configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Scan agent transcripts for parallel tool violations.")
    parser.add_argument("--transcript", type=Path, help="Explicit Cursor agent JSONL path")
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Use newest jsonl under ~/.cursor/projects/*strategy-codex*/agent-transcripts/",
    )
    parser.add_argument(
        "--project",
        default="strategy-codex",
        help="Project folder slug match for --latest (default: strategy-codex)",
    )
    parser.add_argument(
        "--last-turns",
        type=int,
        default=50,
        help="Scan only the last N assistant turns (default: 50)",
    )
    parser.add_argument("--strict", action="store_true", help="Promote warnings to hard violations")
    parser.add_argument("--json", action="store_true", help="Machine-readable JSON on stdout")
    args = parser.parse_args()

    path = args.transcript
    if path is None:
        if not args.latest and os.isatty(0):
            args.latest = True
        path = find_latest_transcript(project_slug=args.project)
        if path is None:
            if args.json:
                print(json.dumps({"error": "no transcript found", "violations": []}))
            else:
                print("No Cursor agent transcript found.", file=sys.stderr)
            return 2

    report = scan_transcript(path, last_turns=args.last_turns, strict=args.strict)

    if args.json:
        payload = {
            "transcript": str(report.transcript_path) if report.transcript_path else None,
            "assistant_turns_scanned": report.assistant_turns_scanned,
            "error": report.error,
            "violations": [
                {
                    "rule_id": v.rule_id,
                    "severity": v.severity,
                    "turn_index": v.turn_index,
                    "line_no": v.line_no,
                    "detail": v.detail,
                }
                for v in report.violations
            ],
            "hard_count": report.hard_count,
            "warn_count": report.warn_count,
        }
        print(json.dumps(payload, indent=2))
    else:
        if report.error:
            print(f"Error: {report.error}", file=sys.stderr)
        else:
            print("\n".join(format_markdown_lines(report)).rstrip())
            if report.hard_count:
                print("", file=sys.stderr)

    if report.error:
        return 2
    return 1 if report.hard_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
