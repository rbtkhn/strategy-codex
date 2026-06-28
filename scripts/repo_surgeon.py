#!/usr/bin/env python3
"""
Repo Surgeon — advisory structural health report for strategy-codex.

Orchestrates existing check scripts plus scoped link and local-path scans.
Read-only except for report output paths.

See runtime/artifacts/repo-surgeon/README.md and
docs/skill-work/work-dev/operator-dashboard-consolidation-phase0.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from operator_report_utils import (  # noqa: E402
    Finding,
    authority_header,
    count_by_severity,
    markdown_table,
    overall_status,
    python_executable,
    run_check,
    utc_now_iso,
    write_report,
)
from repo_io import ARTIFACTS_DIR  # noqa: E402
from validate_structured_files import collect_markdown_paths, validate_markdown_links  # noqa: E402

DEFAULT_OUT = ARTIFACTS_DIR / "repo-surgeon" / "latest.md"
DEFAULT_JSON = ARTIFACTS_DIR / "repo-surgeon" / "latest.json"

SSOT_LINK_TARGETS = frozenset(
    {
        "AGENTS.md",
        "instance-doctrine.md",
        "docs/harness-architecture-map.md",
        "docs/root-directory-map.md",
    }
)

RETURN_PATHS = [
    "docs/root-directory-map.md",
    "docs/harness-architecture-map.md",
    "docs/runtime/context-budgeting.md",
    "skills/README.md",
    "runtime/artifacts/README.md",
]

ROUTING_SSOT_REL = frozenset(
    {
        "LLM-ROUTING.md",
        "repo-map.yaml",
        "AGENTS.md",
        "docs/start-here.md",
        "docs/root-directory-map.md",
        "docs/product-identity.md",
        "docs/public-orientation.md",
        "statecraft/voices/voice-index.md",
    }
)

LOCAL_PATH_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"/C:/", re.IGNORECASE), "/C:/ absolute Windows path"),
    (re.compile(r"C:\\dev\\", re.IGNORECASE), "C:\\dev\\ local path"),
    (re.compile(r"/Users/"), "/Users/ macOS home path"),
    (re.compile(r"file://", re.IGNORECASE), "file:// URL"),
    (re.compile(r"\\\\dev\\", re.IGNORECASE), "\\\\dev\\ UNC-style path"),
)

_SCAN_SUFFIXES = {".md", ".yaml", ".yml", ".json"}
_SKIP_DIR_NAMES = frozenset({".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"})


def _rel(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


def _collect_routing_ssot_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()
    for rel in ROUTING_SSOT_REL:
        path = (repo_root / rel).resolve()
        if path.is_file():
            files.add(path.resolve())
    voices = repo_root / "statecraft" / "voices"
    if voices.is_dir():
        for pattern in ("*-index.md", "*-source-index.md"):
            for p in voices.glob(f"**/{pattern}"):
                name = p.name
                if name in {"voice-index.md", "index.md"}:
                    continue
                if "master-index" in name or "analysis-index" in name:
                    continue
                if p.parent.name == "map":
                    continue
                files.add(p.resolve())
    return sorted(files)


def _collect_scan_files(repo_root: Path, scope: str) -> list[Path]:
    scope_norm = scope.strip().lower()
    if scope_norm == "routing-ssot":
        return _collect_routing_ssot_files(repo_root)
    md_paths = collect_markdown_paths(repo_root, scope)
    extra: set[Path] = set()
    roots: list[Path] = []
    scope_norm = scope.strip().lower()
    if scope_norm in {"docs", "all"}:
        roots.append(repo_root / "docs")
    if scope_norm in {"statecraft", "all"}:
        roots.append(repo_root / "statecraft")
    if scope_norm in {"skills", "all"}:
        roots.extend([repo_root / "skills", repo_root / ".cursor" / "skills"])

    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if path.suffix.lower() not in _SCAN_SUFFIXES:
                continue
            if any(part in _SKIP_DIR_NAMES for part in path.parts):
                continue
            extra.add(path)

    return sorted(set(md_paths) | extra)


def _parse_link_error(err: str) -> tuple[str, str, str]:
    if ":->" in err:
        left, detail = err.split(":->", 1)
        if ":" in left:
            file_part, raw = left.split(":", 1)
            return file_part, raw, detail
    return err, "", err


def _link_severity(missing_detail: str) -> str:
    detail_norm = missing_detail.replace("\\", "/").strip()
    for ssot in SSOT_LINK_TARGETS:
        if detail_norm == ssot or detail_norm.endswith("/" + ssot):
            return "blocking"
    if "outside repo" in missing_detail:
        return "warning"
    return "warning"


def _is_template_link(raw: str, detail: str) -> bool:
    combined = f"{raw} {detail}"
    if "*" in combined:
        return True
    if "YYYY-MM-DD" in combined:
        return True
    return False


def findings_from_links(
    repo_root: Path,
    scope: str,
    *,
    max_errors: int | None = None,
) -> list[Finding]:
    scan_paths = _collect_scan_files(repo_root, scope)
    paths = [p for p in scan_paths if p.suffix.lower() == ".md"]
    raw_errors = validate_markdown_links(paths, repo_root)
    findings: list[Finding] = []
    for err in raw_errors:
        file_part, raw, detail = _parse_link_error(err)
        if _is_template_link(raw, detail):
            continue
        severity = _link_severity(detail)
        findings.append(
            Finding(
                severity=severity,
                category="broken_link",
                file=file_part or None,
                line=None,
                message=f"broken link `{raw}` -> {detail}",
                suggested_action="Fix relative path or add missing target file",
            )
        )
    if max_errors is not None:
        return findings[:max_errors]
    return findings


def findings_from_local_path_leaks(repo_root: Path, scope: str) -> list[Finding]:
    findings: list[Finding] = []
    for path in _collect_scan_files(repo_root, scope):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue
        rel = _rel(repo_root, path)
        for line_no, line in enumerate(lines, start=1):
            for pattern, label in LOCAL_PATH_PATTERNS:
                if pattern.search(line):
                    findings.append(
                        Finding(
                            severity="warning",
                            category="local_path",
                            file=rel,
                            line=line_no,
                            message=f"{label} in line",
                            suggested_action="Use repo-relative paths in committed docs",
                        )
                    )
                    break
    return findings


def findings_from_checks(
    repo_root: Path,
    *,
    run_checks: bool,
    verify_portable: bool,
) -> tuple[list[Finding], dict[str, str]]:
    findings: list[Finding] = []
    outputs: dict[str, str] = {}
    if not run_checks:
        return findings, outputs

    py = python_executable()
    checks: list[tuple[str, list[str], str, str, str]] = [
        (
            "assert_root_folder_layout",
            [py, str(_SCRIPTS / "assert_root_folder_layout.py")],
            "blocking",
            "root_layout",
            "Review docs/root-directory-map.md and remove unexpected top-level folders",
        ),
        (
            "check_repo_path_adoption",
            [py, str(_SCRIPTS / "check_repo_path_adoption.py")],
            "warning",
            "path_adoption",
            "Run python3 scripts/adopt_repo_path_constants.py --apply",
        ),
        (
            "validate_skills",
            [py, str(_SCRIPTS / "validate_skills.py")],
            "blocking",
            "skill_drift",
            "Fix skill frontmatter or run validate_skills.py --fix where safe",
        ),
    ]
    if verify_portable:
        checks.append(
            (
                "sync_portable_skills",
                [py, str(_SCRIPTS / "sync_portable_skills.py"), "--verify"],
                "warning",
                "skill_drift",
                "Run python3 scripts/sync_portable_skills.py to refresh portable skills",
            )
        )

    for name, argv, severity, category, action in checks:
        code, text = run_check(argv, repo_root)
        outputs[name] = text
        if code == 0:
            continue
        summary = text.splitlines()[0] if text else f"{name} exited {code}"
        findings.append(
            Finding(
                severity=severity,
                category=category,
                file=None,
                line=None,
                message=summary,
                suggested_action=action,
            )
        )
    return findings, outputs


def build_findings(
    repo_root: Path,
    *,
    run_checks: bool,
    scope: str,
    verify_portable: bool,
    max_link_errors: int | None,
) -> tuple[list[Finding], dict[str, str]]:
    check_findings, check_outputs = findings_from_checks(
        repo_root,
        run_checks=run_checks,
        verify_portable=verify_portable,
    )
    link_findings = findings_from_links(repo_root, scope, max_errors=max_link_errors)
    leak_findings = (
        []
        if scope.strip().lower() == "routing-ssot"
        else findings_from_local_path_leaks(repo_root, scope)
    )
    all_findings = check_findings + link_findings + leak_findings
    return all_findings, check_outputs


def build_fix_order(findings: list[Finding], *, limit: int = 5) -> list[str]:
    order: list[str] = []
    for severity in ("blocking", "warning", "info"):
        for f in findings:
            if f.severity != severity:
                continue
            prefix = f"[{f.category}]"
            loc = ""
            if f.file:
                loc = f" ({f.file}"
                if f.line:
                    loc += f":{f.line}"
                loc += ")"
            line = f"{prefix}{loc} {f.message}"
            if f.suggested_action:
                line += f" — {f.suggested_action}"
            order.append(line)
            if len(order) >= limit:
                return order
    return order


def build_markdown(
    findings: list[Finding],
    fix_order: list[str],
    check_outputs: dict[str, str],
    *,
    generated_at: str,
    scope: str,
    commands_run: list[str],
    md_link_cap: int,
) -> str:
    status = overall_status(findings)
    counts = count_by_severity(findings)

    parts = [
        "# Repo Surgeon Report",
        "",
        authority_header(generated_at, RETURN_PATHS),
        "## 1. Overall Health",
        "",
        f"Status: **{status}**",
        "",
        f"- Blocking: {counts['blocking']}",
        f"- Warnings: {counts['warning']}",
        f"- Info: {counts['info']}",
        f"- Scope: `{scope}`",
        "",
        "## 2. Recommended Fix Order",
        "",
    ]
    if fix_order:
        for i, item in enumerate(fix_order, start=1):
            parts.append(f"{i}. {item}")
    else:
        parts.append("_No urgent fixes detected in this scope._")
    parts.extend(["", "## 3. Root Layout", ""])

    layout_out = check_outputs.get("assert_root_folder_layout", "_Check not run._")
    parts.append("```text")
    parts.append(layout_out or "_No output._")
    parts.append("```")
    parts.extend(["", "## 4. Broken Links", ""])

    link_rows = [
        {
            "Severity": f.severity,
            "File": f.file or "",
            "Problem": f.message,
            "Suggested fix": f.suggested_action or "",
        }
        for f in findings
        if f.category == "broken_link"
    ][:md_link_cap]
    parts.append(markdown_table(link_rows, ["Severity", "File", "Problem", "Suggested fix"]))

    parts.extend(["", "## 5. Local Path Leaks", ""])
    leak_rows = [
        {
            "File": f.file or "",
            "Line": f.line or "",
            "Path signal": f.message,
            "Suggested replacement": f.suggested_action or "",
        }
        for f in findings
        if f.category == "local_path"
    ][:md_link_cap]
    parts.append(markdown_table(leak_rows, ["File", "Line", "Path signal", "Suggested replacement"]))

    parts.extend(["", "## 6. Skill Drift", ""])
    for key in ("validate_skills", "sync_portable_skills"):
        if key in check_outputs:
            parts.append(f"### {key}")
            parts.append("```text")
            parts.append(check_outputs[key] or "_No output._")
            parts.append("```")
            parts.append("")

    parts.extend(["", "## 7. Command Appendix", ""])
    parts.append("Commands run:")
    for cmd in commands_run:
        parts.append(f"- `{cmd}`")
    parts.extend(["", "Commands suggested:"])
    suggested = sorted(
        {
            f.suggested_action
            for f in findings
            if f.suggested_action
        }
    )
    if suggested:
        for cmd in suggested:
            parts.append(f"- {cmd}")
    else:
        parts.append("- _None._")

    parts.extend(["", "## 8. Return Paths", ""])
    for path in RETURN_PATHS:
        parts.append(f"- `{path}`")
    parts.append("")
    return "\n".join(parts)


def build_json_payload(
    findings: list[Finding],
    fix_order: list[str],
    *,
    generated_at: str,
    commands_run: list[str],
) -> dict[str, Any]:
    status = overall_status(findings)
    counts = count_by_severity(findings)
    return {
        "generated_at": generated_at,
        "authority": "runtime_derived",
        "status": status,
        "blocking_count": counts["blocking"],
        "warning_count": counts["warning"],
        "info_count": counts["info"],
        "recommended_fix_order": fix_order,
        "findings": [f.to_dict() for f in findings],
        "commands": {
            "run": commands_run,
            "suggested": sorted(
                {f.suggested_action for f in findings if f.suggested_action}
            ),
        },
    }


def generate_report(
    repo_root: Path,
    *,
    out: Path = DEFAULT_OUT,
    json_out: Path = DEFAULT_JSON,
    snapshot: bool = False,
    run_checks: bool = True,
    scope: str = "docs",
    max_link_errors: int = 50,
    verify_portable: bool = False,
    fail_on_blocking: bool = False,
) -> tuple[int, dict[str, Any]]:
    """Build and write Repo Surgeon report; return (exit_code, json_payload)."""
    out_path = out if out.is_absolute() else (repo_root / out).resolve()
    json_path = json_out if json_out.is_absolute() else (repo_root / json_out).resolve()

    try:
        findings, check_outputs = build_findings(
            repo_root,
            run_checks=run_checks,
            scope=scope,
            verify_portable=verify_portable,
            max_link_errors=None,
        )
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 2, {}

    generated_at = utc_now_iso()
    fix_order = build_fix_order(findings)
    commands_run: list[str] = []
    if run_checks:
        commands_run.append(f"{python_executable()} scripts/assert_root_folder_layout.py")
        commands_run.append(f"{python_executable()} scripts/check_repo_path_adoption.py")
        commands_run.append(f"{python_executable()} scripts/validate_skills.py")
        if verify_portable:
            commands_run.append(f"{python_executable()} scripts/sync_portable_skills.py --verify")
    commands_run.append(f"{python_executable()} scripts/repo_surgeon.py --scope {scope}")

    md = build_markdown(
        findings,
        fix_order,
        check_outputs,
        generated_at=generated_at,
        scope=scope,
        commands_run=commands_run,
        md_link_cap=max_link_errors,
    )
    payload = build_json_payload(
        findings,
        fix_order,
        generated_at=generated_at,
        commands_run=commands_run,
    )

    write_report(out_path, md, snapshot=snapshot)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {out_path}")
    print(f"wrote {json_path}")
    print(f"status: {payload['status']} (blocking={payload['blocking_count']})")

    if fail_on_blocking and payload["blocking_count"] > 0:
        return 1, payload
    return 0, payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="Markdown report path",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=DEFAULT_JSON,
        help="JSON report path",
    )
    parser.add_argument("--snapshot", action="store_true", help="Also write dated .md copy")
    parser.add_argument(
        "--run-existing-checks",
        action="store_true",
        default=True,
        help="Run layout/path/skill check scripts (default: on)",
    )
    parser.add_argument(
        "--no-existing-checks",
        action="store_true",
        help="Skip subprocess check scripts",
    )
    parser.add_argument(
        "--scope",
        default="docs",
        choices=("docs", "statecraft", "skills", "all", "routing-ssot"),
        help="Markdown link and leak scan scope",
    )
    parser.add_argument(
        "--max-link-errors",
        type=int,
        default=50,
        help="Cap broken-link rows in Markdown (JSON lists all findings)",
    )
    parser.add_argument(
        "--verify-portable-skills",
        action="store_true",
        help="Also run sync_portable_skills.py --verify",
    )
    parser.add_argument(
        "--fail-on-blocking",
        action="store_true",
        help="Exit 1 when any blocking finding exists",
    )
    args = parser.parse_args()

    run_checks = args.run_existing_checks and not args.no_existing_checks
    code, _payload = generate_report(
        REPO_ROOT,
        out=args.out,
        json_out=args.json_out,
        snapshot=args.snapshot,
        run_checks=run_checks,
        scope=args.scope,
        max_link_errors=args.max_link_errors,
        verify_portable=args.verify_portable_skills,
        fail_on_blocking=args.fail_on_blocking,
    )
    return code


if __name__ == "__main__":
    raise SystemExit(main())
