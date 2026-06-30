#!/usr/bin/env python3
"""Generate statecraft notes registry from note contract metadata."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NOTES_ROOT = REPO_ROOT / "statecraft" / "notes"
DEFAULT_MD = REPO_ROOT / "runtime" / "artifacts" / "statecraft-notes-registry.md"
DEFAULT_JSON = REPO_ROOT / "runtime" / "artifacts" / "statecraft-notes-registry.json"

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_statecraft_notes import (  # noqa: E402
    LINK_RE,
    STUB_MARKER,
    _resolve_link,
    build_inbound_note_links,
    classify_tier,
    parse_note_metadata,
    validate_note,
)
from notes_registry_lib import (  # noqa: E402
    RegistryRow,
    build_dashboard,
    build_registry_row,
    render_registry_json,
    render_registry_markdown,
)

def collect_registry_rows() -> list[RegistryRow]:
    all_paths = list(NOTES_ROOT.rglob("*.md"))
    inbound = build_inbound_note_links(all_paths)
    tier_a_rels = {
        p.relative_to(REPO_ROOT).as_posix()
        for p in all_paths
        if classify_tier(p) == "A"
    }
    rows: list[RegistryRow] = []

    for path in sorted(all_paths):
        tier = classify_tier(path)
        if tier not in {"A", "B"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if STUB_MARKER in text:
            continue
        meta = parse_note_metadata(path, text)
        rel = meta.rel
        issues = validate_note(meta, text=text, inbound_count=inbound.get(rel, 0))
        orphan_issue: str | None = None
        if tier == "A" and meta.authority_level == "shelf-native":
            out_links = [raw for raw in LINK_RE.findall(text) if _resolve_link(path, raw) is not None]
            if inbound.get(rel, 0) == 0 and not out_links:
                orphan_issue = f"{rel}: orphan shelf-native note (no in/out links)"
        rows.append(
            build_registry_row(
                meta,
                text,
                inbound_count=inbound.get(rel, 0),
                tier_a_rels=tier_a_rels,
                validate_issues=issues,
                orphan_issue=orphan_issue,
            )
        )
    return rows

def generate_outputs() -> tuple[list[RegistryRow], str, str]:
    rows = collect_registry_rows()
    dashboard = build_dashboard(rows)
    return rows, render_registry_markdown(rows, dashboard), render_registry_json(rows, dashboard)

def check_artifacts(*, md_path: Path, json_path: Path) -> int:
    if not md_path.is_file():
        print(f"error: missing {md_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1
    if not json_path.is_file():
        print(f"error: missing {json_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    md_expected, json_expected = generate_outputs()[1:]
    md_current = md_path.read_text(encoding="utf-8")
    json_current = json_path.read_text(encoding="utf-8")

    stale = False
    if md_current != md_expected:
        print(
            f"error: {md_path.relative_to(REPO_ROOT)} is out of date; run reindex_notes.py",
            file=sys.stderr,
        )
        stale = True
    if json_current != json_expected:
        try:
            cur = json.loads(json_current)
            exp = json.loads(json_expected)
            cur.pop("generated_at", None)
            exp.pop("generated_at", None)
            if cur != exp:
                print(
                    f"error: {json_path.relative_to(REPO_ROOT)} is out of date; run reindex_notes.py",
                    file=sys.stderr,
                )
                stale = True
        except json.JSONDecodeError:
            print(
                f"error: {json_path.relative_to(REPO_ROOT)} is out of date; run reindex_notes.py",
                file=sys.stderr,
            )
            stale = True
    if stale:
        return 1
    print("ok: statecraft notes registry artifacts match generator output")
    return 0

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_MD,
        help="Registry markdown output (default: runtime/artifacts/statecraft-notes-registry.md)",
    )
    ap.add_argument(
        "--json-output",
        type=Path,
        default=DEFAULT_JSON,
        help="Registry JSON output (default: runtime/artifacts/statecraft-notes-registry.json)",
    )
    ap.add_argument("--stdout", action="store_true", help="Print markdown registry to stdout only")
    ap.add_argument(
        "--format",
        choices=("md", "json"),
        default="md",
        help="Stdout format when --stdout (default: md)",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if registry artifacts differ from freshly computed output",
    )
    args = ap.parse_args()

    if args.check:
        return check_artifacts(md_path=args.output, json_path=args.json_output)

    rows, md_text, json_text = generate_outputs()
    if args.stdout:
        print(json_text if args.format == "json" else md_text)
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(md_text, encoding="utf-8")
    args.json_output.write_text(json_text, encoding="utf-8")
    print(
        f"reindex_notes: wrote {args.output.relative_to(REPO_ROOT)} "
        f"and {args.json_output.relative_to(REPO_ROOT)} ({len(rows)} rows)"
    )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
