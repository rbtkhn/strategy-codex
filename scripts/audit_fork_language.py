#!/usr/bin/env python3
"""
Read-only audit for fork-default language in operator-facing docs.

Flags phrases that imply Grace-Mar fork growth or Voice as the default
strategy-codex objective. SSOT rules: config/fork-language-audit.v1.json

See docs/grace-mar-instance-boundary.md (maintenance).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = REPO_ROOT / "config" / "fork-language-audit.v1.json"


def _configure_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _should_skip(rel_posix: str, cfg: dict[str, Any]) -> bool:
    for prefix in cfg.get("skip_path_prefixes", []):
        if rel_posix.startswith(prefix) or rel_posix.replace("\\", "/").startswith(prefix):
            return True
    exact = set(cfg.get("skip_paths_exact", []))
    if rel_posix in exact:
        return True
    return False


def _iter_files(repo_root: Path, cfg: dict[str, Any]) -> list[Path]:
    out: set[Path] = set()
    for pattern in cfg.get("scan_globs", []):
        for path in repo_root.glob(pattern):
            if not path.is_file():
                continue
            rel = path.relative_to(repo_root).as_posix()
            if _should_skip(rel, cfg):
                continue
            out.add(path.resolve())
    return sorted(out)


def _compile_rules(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    compiled: list[dict[str, Any]] = []
    for rule in cfg.get("rules", []):
        compiled.append(
            {
                **rule,
                "regex": re.compile(rule["pattern"]),
            }
        )
    return compiled


def _context_suppressed(lines: list[str], line_index: int, suppress_re: re.Pattern[str] | None) -> bool:
    if not suppress_re:
        return False
    start = max(0, line_index - 8)
    window = "\n".join(lines[start : line_index + 1])
    return bool(suppress_re.search(window))


def audit_repo(repo_root: Path, config_path: Path) -> dict[str, Any]:
    cfg = _load_config(config_path)
    suppress_re = None
    raw_suppress = cfg.get("context_suppress_regex")
    if raw_suppress:
        suppress_re = re.compile(raw_suppress)

    rules = _compile_rules(cfg)
    findings: list[dict[str, Any]] = []

    for path in _iter_files(repo_root, cfg):
        rel = path.relative_to(repo_root).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            findings.append(
                {
                    "ruleId": "read-error",
                    "path": rel,
                    "line": None,
                    "severity": "error",
                    "message": str(exc),
                    "excerpt": "",
                }
            )
            continue

        file_lines = text.splitlines()
        for line_no, line in enumerate(file_lines, start=1):
            if _context_suppressed(file_lines, line_no - 1, suppress_re):
                continue
            for rule in rules:
                if not rule["regex"].search(line):
                    continue
                findings.append(
                    {
                        "ruleId": rule["id"],
                        "path": rel,
                        "line": line_no,
                        "severity": rule.get("severity", "warn"),
                        "message": rule["message"],
                        "excerpt": line.strip()[:240].encode("utf-8", "replace").decode("utf-8"),
                    }
                )

    errors = [f for f in findings if f["severity"] == "error"]
    warns = [f for f in findings if f["severity"] == "warn"]
    return {
        "ok": len(findings) == 0,
        "findingCount": len(findings),
        "errorCount": len(errors),
        "warnCount": len(warns),
        "findings": findings,
    }


def _render_text(report: dict[str, Any], *, errors_only: bool) -> str:
    if report["ok"]:
        return "ok: fork-language audit found no operator-routing drift"
    lines = [
        f"findings: {report['findingCount']} "
        f"(errors={report['errorCount']}, warns={report['warnCount']})"
    ]
    for item in report["findings"]:
        if errors_only and item["severity"] != "error":
            continue
        loc = item["path"]
        if item.get("line"):
            loc = f"{loc}:{item['line']}"
        sev = item["severity"].upper()
        lines.append(f"- [{sev} {item['ruleId']}] {loc}")
        lines.append(f"  {item['message']}")
        if item.get("excerpt"):
            lines.append(f"  > {item['excerpt']}")
    return "\n".join(lines)


def main() -> int:
    _configure_stdout()
    parser = argparse.ArgumentParser(
        description="Audit operator docs for fork-default language (read-only)."
    )
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Report/exit on error-severity findings only",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any finding (including warns)",
    )
    args = parser.parse_args()

    report = audit_repo(args.repo_root.resolve(), args.config.resolve())

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(_render_text(report, errors_only=args.errors_only))

    if report["ok"]:
        return 0
    if args.errors_only:
        return 1 if report["errorCount"] else 0
    if args.strict:
        return 1
    return 1 if report["errorCount"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
