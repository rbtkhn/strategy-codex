#!/usr/bin/env python3
"""Normalize capture channel_slug using host-first rules (not thread alone)."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "source-archive" / "statecraft"
DEEP_DIVE_PATTERN = re.compile(
    r"^(channel_slug:\s*)[\"']?daniel-davis-deep-dive[\"']?\s*$",
    re.MULTILINE,
)

# Host line -> canonical channel_slug (upload channel, not analyst thread).
HOST_SLUG: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^host:\s*Glenn Diesen\s*$", re.MULTILINE | re.IGNORECASE), "glenn-diesen"),
    (re.compile(r"^host:\s*Daniel Davis\s*$", re.MULTILINE | re.IGNORECASE), "daniel-davis"),
    (re.compile(r"^host:\s*Lt Col\.?\s+Daniel Davis\s*$", re.MULTILINE | re.IGNORECASE), "daniel-davis"),
    (re.compile(r"^host:\s*daniel-davis\s*$", re.MULTILINE | re.IGNORECASE), "daniel-davis"),
    (re.compile(r"^host:\s*Daniel Davis\s*/\s*Deep Dive\s*$", re.MULTILINE | re.IGNORECASE), "daniel-davis"),
]

SHOW_SLUG: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"^show:\s*Daniel Davis Deep Dive", re.MULTILINE | re.IGNORECASE), "daniel-davis"),
    (re.compile(r"^show:\s*Glenn Diesen\b", re.MULTILINE | re.IGNORECASE), "glenn-diesen"),
]

PREFIX_SLUG: list[tuple[str, str]] = [
    ("source-glenn-diesen-", "glenn-diesen"),
    ("source-diesen-", "glenn-diesen"),
    ("source-daniel-davis-", "daniel-davis"),
]


def split_frontmatter(text: str) -> tuple[str, str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end < 0:
        return None
    return text[:3], text[3:end], text[end:]


def slug_from_host(fm: str) -> str | None:
    for pattern, slug in HOST_SLUG:
        if pattern.search(fm):
            return slug
    return None


def slug_from_show(fm: str) -> str | None:
    for pattern, slug in SHOW_SLUG:
        if pattern.search(fm):
            return slug
    return None


def slug_from_filename(filename: str) -> str | None:
    for prefix, slug in PREFIX_SLUG:
        if filename.startswith(prefix):
            return slug
    return None


def slug_from_thread_fallback(fm: str, filename: str) -> str | None:
    """Last resort: Davis-channel solo captures with thread but no host line."""
    if not filename.startswith("source-daniel-davis-"):
        return None
    if re.search(r"^thread:\s*diesen\s*$", fm, re.MULTILINE):
        return None
    if re.search(r"^thread:\s*davis\s*$", fm, re.MULTILINE):
        return "daniel-davis"
    if re.search(r"^thread_expert:\s*davis\s*$", fm, re.MULTILINE):
        return None  # often guest-on-other-channel; require host or show
    if re.search(r"^threads:\s*\[[^\]]*\bdavis\b[^\]]*\]", fm, re.MULTILINE):
        # Ambiguous when both davis and diesen — require host for dyad files.
        if re.search(r"^threads:\s*\[[^\]]*\bdiesen\b[^\]]*\]", fm, re.MULTILINE):
            return None
        return "daniel-davis"
    title = re.search(r"^title:\s*[\"']?(.+)", fm, re.MULTILINE)
    if title and re.search(r"Lt Col Daniel Davis|Daniel Davis Deep Dive", title.group(1), re.I):
        return "daniel-davis"
    if "intel-briefing" in filename and "diesen" not in filename:
        return "daniel-davis"
    return None


def resolve_channel_slug(fm: str, filename: str) -> str | None:
    """Host-first channel_slug; thread alone must not override a non-Davis host."""
    host_slug = slug_from_host(fm)
    if host_slug:
        return host_slug
    show_slug = slug_from_show(fm)
    if show_slug:
        return show_slug
    prefix_slug = slug_from_filename(filename)
    if prefix_slug:
        return prefix_slug
    return slug_from_thread_fallback(fm, filename)


def insert_after_line(fm: str, line_pattern: str, slug: str) -> str | None:
    match = re.search(line_pattern, fm, re.MULTILINE)
    if not match:
        return None
    insert_at = match.end()
    return fm[:insert_at] + f"\nchannel_slug: {slug}" + fm[insert_at:]


def upsert_channel_slug(fm: str, slug: str) -> str:
    if re.search(r"^channel_slug:", fm, re.MULTILINE):
        return re.sub(r"^channel_slug:\s*.+\s*$", f"channel_slug: {slug}", fm, flags=re.MULTILINE)
    anchors = [
        r"^host:\s*.+$",
        r"^show:\s*.+$",
        r"^thread:\s*.+$",
        r"^thread_expert:\s*.+$",
        r"^threads:\s*\[[^\]]+\]\s*$",
        r"^kind:\s*\S+\s*$",
        r"^pub_date:\s*\S+\s*$",
        r"^date:\s*\S+\s*$",
        r"^title:\s*.*$",
    ]
    for anchor in anchors:
        updated = insert_after_line(fm, anchor, slug)
        if updated:
            return updated
    return f"channel_slug: {slug}\n{fm.lstrip()}"


def patch_capture(path: Path, *, dry_run: bool = False) -> tuple[str, str | None] | None:
    """Return (action, expected_slug) where action is add|fix|ok|skip."""
    text = path.read_text(encoding="utf-8")
    parts = split_frontmatter(text)
    if not parts:
        return None
    _, fm, tail = parts
    expected = resolve_channel_slug(fm, path.name)
    if not expected:
        return ("skip", None)
    current = re.search(r"^channel_slug:\s*(.+)\s*$", fm, re.MULTILINE)
    if not current:
        new_fm = upsert_channel_slug(fm, expected)
        if not dry_run:
            path.write_text("---" + new_fm + tail, encoding="utf-8")
        return ("add", expected)
    current_slug = current.group(1).strip().strip("'\"")
    if current_slug == expected:
        return ("ok", expected)
    new_fm = upsert_channel_slug(fm, expected)
    if not dry_run:
        path.write_text("---" + new_fm + tail, encoding="utf-8")
    return ("fix", expected)


def iter_captures() -> list[Path]:
    paths: list[Path] = []
    for pattern in ("source-daniel-davis-*.md", "source-glenn-diesen-*.md", "source-glenn-diesen-daniel-davis-*.md"):
        paths.extend(
            p
            for p in ROOT.rglob(pattern)
            if "_land_" not in p.parts and p.name != "header.md"
        )
    return sorted(set(paths))


def audit_captures() -> list[tuple[Path, str, str | None, str]]:
    """Rows: path, current_slug, expected_slug, issue."""
    rows: list[tuple[Path, str, str | None, str]] = []
    for path in iter_captures():
        text = path.read_text(encoding="utf-8")
        parts = split_frontmatter(text)
        if not parts:
            continue
        _, fm, _ = parts
        expected = resolve_channel_slug(fm, path.name)
        current_m = re.search(r"^channel_slug:\s*(.+)\s*$", fm, re.MULTILINE)
        current = current_m.group(1).strip().strip("'\"") if current_m else ""
        host_m = re.search(r"^host:\s*(.+)\s*$", fm, re.MULTILINE)
        host = host_m.group(1).strip() if host_m else ""
        if expected and current and current != expected:
            rows.append((path, current, expected, f"slug mismatch (host={host or '?'})"))
        elif expected and not current:
            rows.append((path, "", expected, f"missing slug (host={host or '?'})"))
        elif not expected and current == "daniel-davis" and host and "diesen" in host.lower():
            rows.append((path, current, expected, "daniel-davis slug on Diesen-host capture"))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", action="store_true", help="Report host/slug mismatches only.")
    parser.add_argument("--fix-wrong", action="store_true", help="Correct channel_slug when host disagrees.")
    args = parser.parse_args()

    if args.audit:
        rows = audit_captures()
        print(f"Audit findings: {len(rows)}")
        for path, current, expected, issue in rows[:20]:
            print(f"  {issue}")
            print(f"    {path.relative_to(REPO)}")
            print(f"    current={current or '-'} expected={expected or '-'}")
        if len(rows) > 20:
            print(f"  ... and {len(rows) - 20} more")
        return 1 if rows else 0

    deep_dive: list[Path] = []
    added: list[Path] = []
    fixed: list[Path] = []
    skipped: list[Path] = []

    for path in iter_captures():
        text = path.read_text(encoding="utf-8")
        new_text = DEEP_DIVE_PATTERN.sub(r"\1daniel-davis", text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            deep_dive.append(path)
            text = new_text

        parts = split_frontmatter(text)
        if not parts:
            continue
        _, fm, _ = parts
        expected = resolve_channel_slug(fm, path.name)
        current_m = re.search(r"^channel_slug:\s*(.+)\s*$", fm, re.MULTILINE)
        current = current_m.group(1).strip().strip("'\"") if current_m else ""

        if not expected:
            if not current:
                skipped.append(path)
            continue

        if current == expected:
            continue

        if current and not args.fix_wrong:
            skipped.append(path)
            continue

        result = patch_capture(path, dry_run=False)
        if not result:
            continue
        action, _ = result
        if action == "add":
            added.append(path)
        elif action == "fix":
            fixed.append(path)

    print(f"Normalized daniel-davis-deep-dive slug: {len(deep_dive)}")
    print(f"Backfilled channel_slug: {len(added)}")
    print(f"Fixed wrong channel_slug: {len(fixed)}")
    print(f"Skipped (no host resolution / wrong slug without --fix-wrong): {len(skipped)}")
    for path in (added + fixed)[:8]:
        print(f"  + {path.relative_to(REPO)}")
    if len(added) + len(fixed) > 8:
        print(f"  ... and {len(added) + len(fixed) - 8} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
