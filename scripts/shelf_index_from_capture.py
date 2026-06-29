#!/usr/bin/env python3
"""Update voice shelf author/guest index from a landed archive capture.

Usage:
    python scripts/shelf_index_from_capture.py --path source-archive/statecraft/2026-06-27/source-pape-....md --dry-run
    python scripts/shelf_index_from_capture.py --path ... --apply
    python scripts/shelf_index_from_capture.py --path ... --apply --audit
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

import shelf_index_utils as shelf  # noqa: E402
from statecraft_day_archive import DEFAULT_ROOT, parse_frontmatter, read_text  # noqa: E402


def resolve_capture(path: Path, archive_root: Path) -> Path:
    path = path.resolve()
    if path.is_file():
        return path
    candidate = archive_root / path
    if candidate.is_file():
        return candidate
    candidate = REPO_ROOT / path
    if candidate.is_file():
        return candidate
    raise FileNotFoundError(f"capture not found: {path}")


def rebuild_pape_index() -> None:
    import build_pape_index as pape_idx  # noqa: E402

    pape_idx.main()


def rebuild_hoh_index() -> None:
    import build_hoh_index as hoh_idx  # noqa: E402

    hoh_idx.main()


def rebuild_martyanov_index() -> None:
    import build_martyanov_index as martyanov_idx  # noqa: E402

    martyanov_idx.main()


def rebuild_postol_index() -> None:
    import build_postol_index as postol_idx  # noqa: E402

    postol_idx.main()


def rebuild_krapivnik_index() -> None:
    import build_krapivnik_index as krapivnik_idx  # noqa: E402

    krapivnik_idx.main()


def rebuild_krainer_index() -> None:
    import build_krainer_index as krainer_idx  # noqa: E402

    krainer_idx.main()


def apply_for_slug(slug: str, capture: Path, meta: dict, body: str) -> bool:
    if slug == "pape":
        rebuild_pape_index()
        index_text = shelf.read_text(shelf.shelf_index_path(slug))
        return shelf.capture_cited_in_index(index_text, capture)
    if slug == "hoh":
        rebuild_hoh_index()
        index_text = shelf.read_text(shelf.shelf_index_path(slug))
        return shelf.capture_cited_in_index(index_text, capture)
    if slug == "martyanov":
        rebuild_martyanov_index()
        index_text = shelf.read_text(shelf.shelf_index_path(slug))
        return shelf.capture_cited_in_index(index_text, capture)
    if slug == "postol":
        rebuild_postol_index()
        index_text = shelf.read_text(shelf.shelf_index_path(slug))
        return shelf.capture_cited_in_index(index_text, capture)
    if slug == "krapivnik":
        rebuild_krapivnik_index()
        index_text = shelf.read_text(shelf.shelf_index_path(slug))
        return shelf.capture_cited_in_index(index_text, capture)
    if slug == "krainer":
        rebuild_krainer_index()
        index_text = shelf.read_text(shelf.shelf_index_path(slug))
        return shelf.capture_cited_in_index(index_text, capture)
    return shelf.append_capture_to_index(slug, capture, meta, body=body)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", type=Path, required=True, help="Landed source-*.md path")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Archive root")
    parser.add_argument("--dry-run", action="store_true", help="Print resolution only")
    parser.add_argument("--apply", action="store_true", help="Append row or rebuild pape index")
    parser.add_argument("--audit", action="store_true", help="Run --shelf-index after apply")
    args = parser.parse_args(argv)

    if not args.dry_run and not args.apply:
        print("error: specify --dry-run or --apply", file=sys.stderr)
        return 2

    try:
        capture = resolve_capture(args.path, args.root.resolve())
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    meta = parse_frontmatter(capture)
    body = read_text(capture)
    slugs = shelf.resolve_shelf_slugs(capture, meta, body)
    if not slugs:
        print(f"no voice shelf match for {capture.name}")
        return 0

    for slug in slugs:
        excluded = shelf.shelf_capture_excluded(slug, capture, meta, body)
        capture_class = shelf.classify_capture_class(slug, capture, meta, body)
        row = shelf.format_index_row(slug, capture, meta, capture_class=capture_class)
        cited = shelf.capture_cited_in_index(shelf.read_text(shelf.shelf_index_path(slug)), capture)
        print(f"slug={slug} class={capture_class} excluded={excluded} cited={cited}")
        print(f"  {row}")
        if excluded:
            continue
        if args.apply and not cited:
            if not apply_for_slug(slug, capture, meta, body):
                print(f"warn: failed to index {capture.name} under {slug}", file=sys.stderr)
            else:
                print(f"indexed {capture.name} under {slug}")

    if args.apply:
        still_missing = []
        for slug in slugs:
            if shelf.shelf_capture_excluded(slug, capture, meta, body):
                continue
            index_text = shelf.read_text(shelf.shelf_index_path(slug))
            if not shelf.capture_cited_in_index(index_text, capture):
                still_missing.append(slug)
        if still_missing:
            print(f"error: still unlisted after apply: {', '.join(still_missing)}", file=sys.stderr)
            return 1

    if args.audit and args.apply:
        code = 0
        for slug in slugs:
            proc = subprocess.run(
                [sys.executable, str(_SCRIPTS / "audit_statecraft_archive_index.py"), "--shelf-index", slug],
                cwd=REPO_ROOT,
            )
            code = max(code, proc.returncode)
        return code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
