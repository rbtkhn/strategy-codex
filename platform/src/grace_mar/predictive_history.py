"""Public intake command for Predictive History corpus uploads.

This is the user-facing replacement for legacy ``work-jiang`` intake wording.
It stages a corpus note under ``codex/predictive-history/intake/`` with
Predictive History frontmatter, auto-detects the volume when possible, and
asks for clarification only when the volume is ambiguous.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

from grace_mar.repo_io import repo_root

VOLUME_CHOICES: tuple[tuple[str, str, str], ...] = (
    ("1", "I", "Geo-Strategy"),
    ("2", "II", "Civilization"),
    ("3", "III", "Secret History"),
    ("4", "IV", "Game Theory"),
    ("5", "V", "Great Books"),
    ("6", "VI", "Interviews"),
    ("7", "VII", "Essays"),
)

_VOLUME_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bgeo[-\s]?strategy\b", re.I), "Volume I - Geo-Strategy"),
    (re.compile(r"\bcivilization\b|\bciv[-\s]?\d+\b", re.I), "Volume II - Civilization"),
    (re.compile(r"\bsecret[-\s]?history\b|\bsh[-\s]?\d+\b", re.I), "Volume III - Secret History"),
    (re.compile(r"\bgame[-\s]?theory\b|\bgt[-\s]?\d+\b", re.I), "Volume IV - Game Theory"),
    (re.compile(r"\bgreat[-\s]?books\b|\bgb[-\s]?\d+\b", re.I), "Volume V - Great Books"),
    (re.compile(r"\binterviews?\b|\bvi[-\s]?\d+\b", re.I), "Volume VI - Interviews"),
    (re.compile(r"\bessay(s)?\b|\bes[-\s]?\d+\b|\bsubstack\b", re.I), "Volume VII - Essays"),
)


def _slugify(text: str, *, max_len: int = 80) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return (s[:max_len].rstrip("-") or "item")


def _extract_title(body: str) -> str | None:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("# "):
            return stripped[2:].strip() or None
        return stripped
    return None


def infer_volume(text: str) -> str | None:
    """Best-effort Predictive History volume inference from title/body text."""
    if not text:
        return None
    normalized = " ".join(text.split())
    for pattern, volume in _VOLUME_PATTERNS:
        if pattern.search(normalized):
            return volume
    return None


def _prompt_for_volume(default_text: str) -> str | None:
    print("Predictive History volume is ambiguous.", file=sys.stderr)
    print("Choose a volume, or press Enter to leave it unstated:", file=sys.stderr)
    for key, roman, label in VOLUME_CHOICES:
        print(f"  {key}. Volume {roman} - {label}", file=sys.stderr)
    choice = input(f"{default_text}> ").strip()
    if not choice:
        return None
    for key, roman, label in VOLUME_CHOICES:
        if choice == key or choice.lower() == roman.lower():
            return f"Volume {roman} - {label}"
        if choice.lower() == label.lower() or choice.lower() == f"volume {roman.lower()} - {label.lower()}":
            return f"Volume {roman} - {label}"
    print(f"Unrecognized choice: {choice!r}", file=sys.stderr)
    return None


def _frontmatter(
    *,
    ingest_date: str,
    pub_date: str,
    title: str,
    source_url: str | None,
    source_note: str,
    volume: str | None,
) -> str:
    lines = [
        "---",
        f"ingest_date: {ingest_date}",
        f"pub_date: {pub_date}",
        "series: Predictive History",
        "kind: predictive-history-intake",
        "stage: intake",
    ]
    if volume:
        lines.append(f"volume: {json.dumps(volume, ensure_ascii=True)}")
    lines.append(f"title: {json.dumps(title, ensure_ascii=True)}")
    if source_url:
        lines.append(f"source_url: {json.dumps(source_url, ensure_ascii=True)}")
    lines.append(f"source_note: {json.dumps(source_note, ensure_ascii=True)}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def build_document(
    *,
    body: str,
    title: str | None,
    source_url: str | None,
    source_note: str,
    ingest_date: str,
    pub_date: str,
    volume: str | None,
) -> tuple[str, str, str | None]:
    """Return ``(filename, markdown, resolved_volume)`` for one intake note."""
    body = body.rstrip()
    resolved_title = title or _extract_title(body) or "Predictive History intake"
    resolved_volume = volume or infer_volume(" ".join(filter(None, [resolved_title, body, source_url or ""])))
    filename = f"predictive-history-{pub_date}-{_slugify(resolved_title)}.md"
    frontmatter = _frontmatter(
        ingest_date=ingest_date,
        pub_date=pub_date,
        title=resolved_title,
        source_url=source_url,
        source_note=source_note,
        volume=resolved_volume,
    )
    rendered_body = body
    if body and not body.lstrip().startswith("# "):
        rendered_body = f"# {resolved_title}\n\n{body}"
    if not rendered_body:
        rendered_body = f"# {resolved_title}\n"
    if not rendered_body.endswith("\n"):
        rendered_body += "\n"
    document = frontmatter + rendered_body
    return filename, document, resolved_volume


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--title", default="", help="Corpus item title")
    p.add_argument("--source-url", default="", help="Source URL for the upload")
    p.add_argument("--source-note", default="Predictive History corpus intake", help="Short provenance note")
    p.add_argument("--volume", default="", help="Explicit volume label, e.g. 'Volume IV - Game Theory'")
    p.add_argument("--body-file", type=Path, default=None, help="Read body text from a file")
    p.add_argument("--body", default="", help="Inline body text")
    p.add_argument("--outdir", type=Path, default=repo_root() / "codex" / "predictive-history" / "intake")
    p.add_argument("--pub-date", default=date.today().isoformat(), help="Publication / air date (YYYY-MM-DD)")
    p.add_argument("--ingest-date", default=date.today().isoformat(), help="Ingest date (YYYY-MM-DD)")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    p.add_argument("--apply", action="store_true", help="Write the intake note (default when --dry-run is absent)")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    if args.dry_run and args.apply:
        raise SystemExit("Use only one of --dry-run or --apply")

    apply = args.apply or not args.dry_run

    body = args.body
    if args.body_file is not None:
        body = args.body_file.read_text(encoding="utf-8")
    elif not body and not sys.stdin.isatty():
        body = sys.stdin.read()

    explicit_volume = args.volume.strip() or None
    if explicit_volume is None:
        inferred = infer_volume(" ".join(filter(None, [args.title, body, args.source_url])))
        if inferred is None and sys.stdin.isatty():
            inferred = _prompt_for_volume(args.title or "predictive-history")
        explicit_volume = inferred
    outdir: Path = args.outdir.resolve()
    filename, document, resolved_volume = build_document(
        body=body,
        title=args.title.strip() or None,
        source_url=args.source_url.strip() or None,
        source_note=args.source_note.strip(),
        ingest_date=args.ingest_date,
        pub_date=args.pub_date,
        volume=explicit_volume,
    )
    outpath = outdir / filename
    if apply and resolved_volume is None:
        raise SystemExit(
            "Predictive History volume is ambiguous; pass --volume or run interactively to choose one."
        )

    if not apply:
        print(f"would write: {_display_path(outpath)}")
        return 0

    outdir.mkdir(parents=True, exist_ok=True)
    outpath.write_text(document, encoding="utf-8")
    print(f"wrote: {_display_path(outpath)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
