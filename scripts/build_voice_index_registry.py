#!/usr/bin/env python3
"""Generate voice index parity registry (runtime/artifacts/voice-index-parity.*)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MD = REPO_ROOT / "runtime" / "artifacts" / "voice-index-parity.md"
DEFAULT_JSON = REPO_ROOT / "runtime" / "artifacts" / "voice-index-parity.json"
DEFAULT_ARCHIVE = REPO_ROOT / "source-archive" / "statecraft"

_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import voice_index_registry_core as core  # noqa: E402

_GENERATED_AT_RE = re.compile(r"^_Generated at .+_$", re.M)

def _normalize_md_for_check(text: str) -> str:
    return _GENERATED_AT_RE.sub("_Generated at CHECK_", text)

def _normalize_json_for_check(text: str) -> dict:
    data = json.loads(text)
    data.pop("generated_at", None)
    return data

def check_artifacts(*, md_path: Path, json_path: Path, archive_root: Path) -> int:
    if not md_path.is_file():
        print(f"error: missing {md_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    if not json_path.is_file():
        print(f"error: missing {json_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    _rows, md_expected, json_expected = core.generate_outputs(archive_root=archive_root)
    yaml_findings = core.validate_yaml_code_exclusion_parity()
    for f in yaml_findings:
        if f.level == "fail":
            print(f"error: [{f.code}] {f.message}", file=sys.stderr)
            return 1

    md_current = md_path.read_text(encoding="utf-8")
    json_current = json_path.read_text(encoding="utf-8")

    stale = False
    if _normalize_md_for_check(md_current) != _normalize_md_for_check(md_expected):
        print(
            f"error: {md_path.relative_to(REPO_ROOT)} is out of date; "
            "run build_voice_index_registry.py",
            file=sys.stderr,
        )
        stale = True
    try:
        if _normalize_json_for_check(json_current) != _normalize_json_for_check(json_expected):
            print(
                f"error: {json_path.relative_to(REPO_ROOT)} is out of date; "
                "run build_voice_index_registry.py",
                file=sys.stderr,
            )
            stale = True
    except json.JSONDecodeError:
        print(
            f"error: {json_path.relative_to(REPO_ROOT)} is invalid JSON; regenerate",
            file=sys.stderr,
        )
        stale = True

    fail_rows = [r for r in _rows if r.parity == "fail"]
    if fail_rows:
        for row in fail_rows[:5]:
            print(f"warn: voice index parity fail: {row.voice}", file=sys.stderr)
        if len(fail_rows) > 5:
            print(f"warn: … and {len(fail_rows) - 5} more parity fail(s)", file=sys.stderr)

    if stale:
        return 1
    summary = core.build_summary(_rows)
    print(
        f"voice index registry: artifacts fresh ({summary['parity_pass']} pass, "
        f"{summary['parity_warn']} warn, {summary['parity_fail']} fail)"
    )
    return 0

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_MD, help="Markdown output path")
    parser.add_argument("--json-output", type=Path, default=DEFAULT_JSON, help="JSON output path")
    parser.add_argument("--root", type=Path, default=DEFAULT_ARCHIVE, help="Archive root")
    parser.add_argument("--voice", metavar="SLUG", help="Single voice index row only")
    parser.add_argument("--check", action="store_true", help="Exit 1 if artifacts stale or parity fails")
    parser.add_argument("--json", action="store_true", dest="json_stdout", help="Print JSON to stdout")
    parser.add_argument("--stdout", action="store_true", help="Print markdown to stdout")
    args = parser.parse_args(argv)

    if args.check:
        return check_artifacts(md_path=args.output, json_path=args.json_output, archive_root=args.root)

    rows, md_text, json_text = core.generate_outputs(
        archive_root=args.root,
        slug_filter=args.voice,
    )

    if args.json_stdout:
        if args.voice and len(rows) == 1:
            print(json.dumps(asdict(rows[0]), indent=2))
        else:
            print(json_text, end="")
        return 0

    if args.stdout:
        print(md_text, end="")
        return 0

    if args.voice:
        if not rows:
            print(f"error: no voice index for slug {args.voice!r}", file=sys.stderr)
            return 1
        print(md_text, end="")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md_text, encoding="utf-8")
    args.json_output.write_text(json_text, encoding="utf-8")
    summary = core.build_summary(rows)
    print(
        f"build_voice_index_registry: wrote {args.output.relative_to(REPO_ROOT)} "
        f"and {args.json_output.relative_to(REPO_ROOT)} "
        f"({summary['voices_discovered']} voices, {summary['parity_pass']} pass)"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
