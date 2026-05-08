#!/usr/bin/env python3
"""Write a generic short-form bundle into strategy-notebook raw-input/.

This helper packages multiple short social posts from one source account or
stream into a single raw-input file. It is intentionally platform-neutral:
X, Threads, Truth Social, Locals, and similar short-form sources can all use
the same capture shape.

The helper does not OCR images. Instead, it expects the operator to provide the
OCR'd / transcribed bundle body and, optionally, a list of screenshot paths or
URLs for provenance.

WORK only; not Record.
"""

from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW_ROOT = REPO_ROOT / "codex" / "2026" / "raw-input"

import sys as _sys

if str(REPO_ROOT / "scripts") not in _sys.path:
    _sys.path.insert(0, str(REPO_ROOT / "scripts"))

from fetch_strategy_raw_input import _slugify  # noqa: E402


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _fmt_screenshot_ref(ref: str) -> str:
    ref = ref.strip()
    if not ref:
        return ""
    return ref


def _build_doc(
    *,
    ingest_date: date,
    pub_date: date,
    source_platform: str,
    account_author: str,
    source_url_profile: str | None,
    source_url: str | None,
    thread: str | None,
    title: str,
    body_text: str,
    screenshot_refs: list[str],
) -> str:
    front: dict[str, str] = {
        "ingest_date": ingest_date.isoformat(),
        "pub_date": pub_date.isoformat(),
        "kind": "shortform-bundle",
        "source_platform": source_platform,
        "account_author": account_author,
    }
    if source_url_profile:
        front["source_url_profile"] = source_url_profile
    if source_url or source_url_profile:
        front["source_url"] = source_url or source_url_profile or ""
    if thread:
        front["thread"] = thread
    if screenshot_refs:
        front["screenshot_count"] = str(len(screenshot_refs))

    fm = ["---"]
    for key, value in front.items():
        if value:
            fm.append(f"{key}: {value}")
    fm.append("---")

    lines = [
        "\n".join(fm),
        "",
        f"# {title}",
        "",
        f"**Platform:** {source_platform}",
        f"**Account:** {account_author}",
    ]
    if source_url_profile:
        lines.append(f"**Profile:** {source_url_profile}")
    lines.extend(
        [
            "",
            "## OCR bundle",
            "",
            body_text or "_(no OCR text supplied)_",
            "",
        ]
    )
    if screenshot_refs:
        lines.extend(["## Screenshot provenance", ""])
        for ref in screenshot_refs:
            lines.append(f"- {ref}")
        lines.append("")
    lines.append("_Backfill: `scripts/backfill_shortform_bundle_raw_input.py`; not Record._")
    lines.append("")
    return "\n".join(lines)


def _default_title(account_author: str, pub_date: date) -> str:
    return f"{account_author} short-form bundle - {pub_date.isoformat()}"


def _default_output_name(*, source_platform: str, account_author: str, pub_date: date) -> str:
    return (
        f"shortform-bundle-"
        f"{_slugify(source_platform, max_len=18)}-"
        f"{_slugify(account_author, max_len=28)}-"
        f"{pub_date.isoformat()}.md"
    )


def run(
    *,
    raw_root: Path,
    ingest_date: date,
    pub_date: date,
    source_platform: str,
    account_author: str,
    source_url_profile: str | None,
    source_url: str | None,
    thread: str | None,
    title: str | None,
    body_file: Path,
    screenshot_refs: Iterable[str],
    output: Path | None,
    apply: bool,
) -> Path:
    body_text = _read_text(body_file)
    refs = [_fmt_screenshot_ref(x) for x in screenshot_refs]
    refs = [x for x in refs if x]
    out_title = title or _default_title(account_author, pub_date)
    content = _build_doc(
        ingest_date=ingest_date,
        pub_date=pub_date,
        source_platform=source_platform,
        account_author=account_author,
        source_url_profile=source_url_profile,
        source_url=source_url,
        thread=thread,
        title=out_title,
        body_text=body_text,
        screenshot_refs=refs,
    )

    dest = output or (
        raw_root / pub_date.isoformat() / _default_output_name(
            source_platform=source_platform,
            account_author=account_author,
            pub_date=pub_date,
        )
    )

    if apply:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    return dest


def _parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=DEFAULT_RAW_ROOT, help="raw-input root")
    ap.add_argument("--ingest-date", type=str, default=None, help="YYYY-MM-DD ingest date")
    ap.add_argument("--pub-date", type=str, required=True, help="YYYY-MM-DD source publication date")
    ap.add_argument("--platform", default="x", help="source platform label, e.g. x, threads, truthsocial")
    ap.add_argument("--account", required=True, help="account / source author label, e.g. @handle")
    ap.add_argument("--profile-url", default=None, help="source profile or home URL")
    ap.add_argument("--source-url", default=None, help="bundle source URL (defaults to profile URL)")
    ap.add_argument("--thread", default=None, help="owning thread / lane id")
    ap.add_argument("--title", default=None, help="human-readable bundle title")
    ap.add_argument("--body-file", type=Path, required=True, help="OCR / short-form bundle body markdown")
    ap.add_argument(
        "--screenshot",
        action="append",
        default=[],
        help="screenshot path or URL; repeat for multiple screenshots",
    )
    ap.add_argument("--output", type=Path, default=None, help="explicit output path")
    ap.add_argument("--apply", action="store_true", help="write the file")
    return ap.parse_args()


def main() -> int:
    args = _parse_args()
    ingest = (
        datetime.strptime(args.ingest_date, "%Y-%m-%d").date()
        if args.ingest_date
        else date.today()
    )
    pub = datetime.strptime(args.pub_date, "%Y-%m-%d").date()
    dest = run(
        raw_root=args.root,
        ingest_date=ingest,
        pub_date=pub,
        source_platform=args.platform,
        account_author=args.account,
        source_url_profile=args.profile_url,
        source_url=args.source_url,
        thread=args.thread,
        title=args.title,
        body_file=args.body_file,
        screenshot_refs=args.screenshot,
        output=args.output,
        apply=args.apply,
    )
    if not args.apply:
        print(f"would write: {dest}")
    else:
        print(f"wrote: {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
