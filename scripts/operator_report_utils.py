"""Shared helpers for operator derived reports (runtime / derived; advisory only)."""

from __future__ import annotations

import subprocess
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    severity: str
    category: str
    message: str
    file: str | None = None
    line: int | None = None
    suggested_action: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def authority_header(generated_at: str, return_paths: list[str]) -> str:
    lines = [
        f"Generated: {generated_at}",
        "Mode: runtime / derived",
        "Authority: advisory only",
        "Canonical source: none",
        "",
        "SSOT return paths:",
    ]
    for path in return_paths:
        lines.append(f"- {path}")
    lines.append("")
    return "\n".join(lines)


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_None._\n"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body_lines: list[str] = []
    for row in rows:
        cells = [str(row.get(col, "")).replace("|", "\\|") for col in columns]
        body_lines.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, sep, *body_lines]) + "\n"


def write_report(path: Path, text: str, *, snapshot: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if snapshot:
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        snap = path.parent / f"{stamp}.md"
        snap.write_text(text, encoding="utf-8")


def run_check(argv: list[str], cwd: Path, *, timeout: int = 120) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return 2, str(exc)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out.strip()


def overall_status(findings: list[Finding]) -> str:
    if any(f.severity == "blocking" for f in findings):
        return "red"
    if any(f.severity == "warning" for f in findings):
        return "yellow"
    return "green"


def count_by_severity(findings: list[Finding]) -> dict[str, int]:
    counts = {"blocking": 0, "warning": 0, "info": 0}
    for f in findings:
        key = f.severity if f.severity in counts else "info"
        counts[key] += 1
    return counts


def python_executable() -> str:
    return sys.executable
