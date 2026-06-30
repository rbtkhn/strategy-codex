#!/usr/bin/env python3
"""One-command statecraft source intake: header build, chunked body land, post-land chain."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from land_statecraft_source_body import merge  # noqa: E402

CHUNK_TARGET_BYTES = 12_000
FORCE_CHUNK_BYTES = 12 * 1024
FORCE_CHUNK_LINES = 80
DATE_SUFFIX_RE = re.compile(r"-(\d{4}-\d{2}-\d{2})$")
DAY_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def _read_body(body_files: list[Path], body_stdin: bool) -> str:
    parts: list[str] = []
    for bf in body_files:
        parts.append(bf.read_text(encoding="utf-8"))
    if body_stdin:
        parts.append(sys.stdin.read())
    body = "\n\n".join(p.strip() for p in parts if p.strip())
    if not body:
        raise ValueError("transcript body is empty")
    return body.strip() + "\n"

def _slug_from_out(out_path: Path) -> str:
    stem = out_path.stem
    match = DATE_SUFFIX_RE.search(stem)
    return stem[: match.start()] if match else stem

def _pub_date_from_out(out_path: Path) -> str | None:
    parent = out_path.parent.name
    return parent if DAY_DIR_RE.match(parent) else None

def _detect_family(out_path: Path, explicit: str) -> str:
    if explicit and explicit != "auto":
        return explicit
    name = out_path.name.lower()
    if "source-alex-mercouris" in name or "youtube-alex-mercouris" in name:
        return "mercouris-solo"
    if "source-duran-mercouris" in name or "transcript-duran-mercouris" in name:
        return "duran-mercouris"
    if "source-judging-freedom" in name:
        return "napolitano"
    if "source-mario-nawfal" in name:
        return "nawfal"
    return "generic"

def _resolve_sidecar_dir(out_path: Path, slug: str) -> Path:
    candidates = [
        out_path.parent / f"_land_{slug}",
        REPO_ROOT / ".codex-tmp" / "land" / slug,
    ]
    last_err: OSError | None = None
    for cand in candidates:
        try:
            cand.mkdir(parents=True, exist_ok=True)
            probe = cand / ".write_probe"
            probe.write_text("ok", encoding="utf-8")
            probe.unlink()
            return cand
        except OSError as exc:
            last_err = exc
    raise RuntimeError(
        f"cannot write sidecar dir (tried {[str(c) for c in candidates]}): {last_err}"
    )

def _split_body_chunks(body: str, target_bytes: int = CHUNK_TARGET_BYTES) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", body.strip()) if p.strip()]
    if not paragraphs:
        return [body.strip()]
    chunks: list[str] = []
    current: list[str] = []
    current_size = 0
    for para in paragraphs:
        para_bytes = len(para.encode("utf-8"))
        sep_bytes = 2 if current else 0
        if current and current_size + sep_bytes + para_bytes > target_bytes:
            chunks.append("\n\n".join(current))
            current = [para]
            current_size = para_bytes
        else:
            current.append(para)
            current_size += sep_bytes + para_bytes
    if current:
        chunks.append("\n\n".join(current))
    return chunks

def _yaml_quote(value: str) -> str:
    if not value:
        return '""'
    if any(ch in value for ch in ':"\\#\n'):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    return value

def _format_display_date(pub_date: str) -> str:
    try:
        dt = datetime.strptime(pub_date, "%Y-%m-%d")
        return dt.strftime("%A, %d %B %Y").replace(" 0", " ")
    except ValueError:
        return pub_date

def _build_mercouris_solo_header(
    *,
    title: str,
    pub_date: str,
    ingest_date: str,
    youtube_id: str | None,
    source_url: str | None,
    source_note: str,
) -> str:
    if youtube_id and not source_url:
        source_url = f"https://www.youtube.com/watch?v={youtube_id}"
    url_line = source_url or "_(unresolved direct watch URL)_"
    note = source_note or "Operator-pasted transcript; Mercouris solo channel monologue."
    yid_line = f"youtube_id: {youtube_id}\n" if youtube_id else ""
    src_url_yaml = _yaml_quote(source_url) if source_url else '""'
    return f"""---
ingest_date: {ingest_date}
pub_date: {pub_date}
kind: transcript
source_form: solo
source_type: youtube
transcript_type: operator_pasted_youtube_transcript
host_people:
  - Alexander Mercouris
show_title: Mercouris
channel_name: Alexander Mercouris
thread: mercouris
threads:
  - mercouris
thread_expert: mercouris
show: Mercouris
host: Alexander Mercouris
title: {_yaml_quote(title)}
channel_slug: alex-mercouris
channel_url: "https://www.youtube.com/@AlexMercouris/videos"
source_url: {src_url_yaml}
{yid_line}source_note: {_yaml_quote(note)}
evidence_grade: transcript-bearing
opening_tier: host-monologue
capture_note: Operator paste; full solo program body preserved from user-supplied YouTube transcript.
editorial_note: Operator-pasted transcript; ASR artifacts retained; not human-verified verbatim against audio.
---

# {title}

**Channel:** Alexander Mercouris (solo)  
**Date:** {_format_display_date(pub_date)} (host)  
**URL:** {url_line}

## Transcript

"""

def _needs_chunked_land(body: str, family: str) -> bool:
    if family == "mercouris-solo":
        return True
    body_bytes = len(body.encode("utf-8"))
    line_count = body.count("\n") + 1
    return body_bytes >= FORCE_CHUNK_BYTES or line_count >= FORCE_CHUNK_LINES

def _resolve_out(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path

def _print_receipt(
    *,
    out_path: Path,
    family: str,
    chunked: bool,
    chunk_count: int,
    total_bytes: int,
    sidecar_dir: Path | None,
    post_land: bool,
    queue_lines: list[str] | None,
) -> None:
    rel = out_path.relative_to(REPO_ROOT).as_posix()
    print("")
    print("## intake receipt")
    print(f"  file: {rel}")
    print(f"  family: {family}")
    print(f"  chunked: {chunked} · chunks: {chunk_count} · bytes: {total_bytes}")
    if sidecar_dir:
        print(f"  sidecar_dir: {sidecar_dir.relative_to(REPO_ROOT).as_posix()}")
    print(f"  post_land: {'yes' if post_land else 'skipped'}")
    if queue_lines:
        for line in queue_lines[:4]:
            print(f"  {line}")

def land_intake(
    *,
    out: Path,
    body: str,
    header_text: str | None,
    family: str,
    dry_run: bool,
    keep_sidecars: bool,
    skip_post_land: bool,
) -> int:
    out = _resolve_out(out)
    pub_date = _pub_date_from_out(out)
    if not pub_date:
        print("error: --out must live under source-archive/statecraft/YYYY-MM-DD/", file=sys.stderr)
        return 1

    slug = _slug_from_out(out)
    chunked = _needs_chunked_land(body, family)
    sidecar_dir: Path | None = None
    chunk_count = 1

    if chunked:
        sidecar_dir = _resolve_sidecar_dir(out, slug)
        header_path = sidecar_dir / "header.md"
        if header_text is None:
            print("error: chunked land requires --header or family metadata flags", file=sys.stderr)
            return 1
        header_path.write_text(header_text, encoding="utf-8")
        chunks = _split_body_chunks(body)
        chunk_count = len(chunks)
        body_paths: list[Path] = []
        for idx, chunk in enumerate(chunks, start=1):
            bp = sidecar_dir / f"p{idx}.txt"
            body_paths.append(bp)
            text = chunk + ("\n" if not chunk.endswith("\n") else "")
            bp.write_text(text, encoding="utf-8")
        rc = merge(header_path, body_paths, out, dry_run)
        if rc != 0:
            return rc
    else:
        if not header_text:
            print("error: direct land requires --header or family metadata flags", file=sys.stderr)
            return 1
        merged = header_text + body
        if dry_run:
            print(f"dry-run: would write {out} ({len(merged.encode('utf-8'))} bytes)")
        else:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(merged, encoding="utf-8")
            print(f"wrote {out} ({len(merged.encode('utf-8'))} bytes)")

    total_bytes = out.stat().st_size if out.is_file() and not dry_run else len(body.encode("utf-8"))

    post_land = False
    if not skip_post_land and not dry_run:
        from post_land_statecraft_batch import post_land_batch  # noqa: PLC0415

        rc = post_land_batch([out], sync_daily=pub_date)
        post_land = True
        if rc != 0:
            return rc

    queue_lines: list[str] | None = None
    if not dry_run:
        try:
            from statecraft_intake_queue import build_queue_report, format_human  # noqa: PLC0415

            rows, sync = build_queue_report(pub_date, allow_desync=True)
            human = format_human(pub_date, rows, sync)
            queue_lines = human.splitlines()
            print("")
            print(human.rstrip())
        except (FileNotFoundError, RuntimeError) as exc:
            print(f"queue report skipped: {exc}", file=sys.stderr)

    if sidecar_dir and not keep_sidecars and not dry_run:
        shutil.rmtree(sidecar_dir, ignore_errors=True)
        print(f"removed sidecar dir {sidecar_dir.relative_to(REPO_ROOT).as_posix()}")
    elif sidecar_dir and dry_run and not keep_sidecars:
        shutil.rmtree(sidecar_dir, ignore_errors=True)

    _print_receipt(
        out_path=out,
        family=family,
        chunked=chunked,
        chunk_count=chunk_count,
        total_bytes=total_bytes,
        sidecar_dir=sidecar_dir if keep_sidecars else None,
        post_land=post_land,
        queue_lines=queue_lines,
    )
    return 0

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="Canonical archive output path.")
    parser.add_argument("--body-file", action="append", default=[], type=Path, help="Body file; repeat to concat.")
    parser.add_argument("--body-stdin", action="store_true", help="Read body from stdin.")
    parser.add_argument("--header", type=Path, help="Pre-built header through ## Transcript.")
    parser.add_argument("--family", default="auto", help="mercouris-solo | auto | generic.")
    parser.add_argument("--youtube-id", help="YouTube id (mercouris-solo).")
    parser.add_argument("--title", help="Episode title (mercouris-solo).")
    parser.add_argument("--pub-date", help="YYYY-MM-DD (default from --out parent).")
    parser.add_argument("--ingest-date", help="YYYY-MM-DD (default today).")
    parser.add_argument("--source-url", help="Direct source URL.")
    parser.add_argument("--source-note", default="", help="source_note frontmatter.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-sidecars", action="store_true")
    parser.add_argument("--skip-post-land", action="store_true")
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    body_files = [_resolve_out(p) for p in args.body_file]
    if not body_files and not args.body_stdin:
        print("error: supply --body-file and/or --body-stdin", file=sys.stderr)
        return 1
    try:
        body = _read_body(body_files, args.body_stdin)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out = _resolve_out(args.out)
    family = _detect_family(out, args.family)
    pub_date = args.pub_date or _pub_date_from_out(out)
    if not pub_date:
        print("error: could not infer pub_date; pass --pub-date", file=sys.stderr)
        return 1
    ingest_date = args.ingest_date or date.today().isoformat()

    header_text: str | None = None
    if args.header:
        header_path = _resolve_out(args.header)
        if not header_path.is_file():
            print(f"error: header not found: {header_path}", file=sys.stderr)
            return 1
        header_text = header_path.read_text(encoding="utf-8")
        if not header_text.endswith("\n"):
            header_text += "\n"
    elif family == "mercouris-solo":
        if not args.title:
            print("error: mercouris-solo requires --title (or --header)", file=sys.stderr)
            return 1
        if not args.youtube_id and not args.source_url:
            print("error: mercouris-solo requires --youtube-id or --source-url", file=sys.stderr)
            return 1
        header_text = _build_mercouris_solo_header(
            title=args.title.strip(),
            pub_date=pub_date,
            ingest_date=ingest_date,
            youtube_id=(args.youtube_id or "").strip() or None,
            source_url=(args.source_url or "").strip() or None,
            source_note=args.source_note.strip(),
        )

    return land_intake(
        out=out,
        body=body,
        header_text=header_text,
        family=family,
        dry_run=args.dry_run,
        keep_sidecars=args.keep_sidecars,
        skip_post_land=args.skip_post_land,
    )

if __name__ == "__main__":
    raise SystemExit(main())
