#!/usr/bin/env python3
"""Read-only Strategy-codex return hint for explicit strategy/source return.

This helper inspects the canonical Strategy-codex inbox/raw-input surfaces and
returns a compact re-entry hint. It does not compose notebook prose, fetch
sources, or mutate any files.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CODEX_ROOT = REPO_ROOT / "codex"
DEFAULT_INBOX = CODEX_ROOT / "daily-strategy-inbox.md"
DEFAULT_STATUS = CODEX_ROOT / "STATUS.md"
DEFAULT_RAW_ROOT = CODEX_ROOT / "years" / "2026" / "raw-input"
RE_URL = re.compile(r"https://[^\s\]>)}]+")
RE_RAW_INPUT_MD = re.compile(r"raw-input/[^\s\])]+\.md")

APPEND_MARKERS = (
    "_(Append below this line during the day.)_",
    "<!-- append below -->",
)


@dataclass(frozen=True)
class StrategyReturnHint:
    live_seam: str
    ready: int
    verify: int
    raw_input_gap: int
    carry: int
    suggested_move: str
    active_chapter: str | None = None
    active_days_path: str | None = None
    raw_input_gap_urls: tuple[str, ...] = ()

    def markdown_lines(self) -> list[str]:
        chapter_tail = ""
        if self.active_chapter:
            chapter_tail = f"; active chapter={self.active_chapter}"
        return [
            "## Strategy return (explicit route)",
            "",
            f"- Live seam: {self.live_seam}",
            (
                "- Inbox triage: "
                f"ready={self.ready}, verify={self.verify}, "
                f"raw-input gap={self.raw_input_gap}, carry={self.carry}{chapter_tail}"
            ),
            f"- Suggested strategy move: {self.suggested_move}",
            "",
        ]


def read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def live_accumulator_text(inbox_text: str) -> str:
    """Return the active accumulator body, preferring the explicit append marker."""
    best = -1
    marker_len = 0
    for marker in APPEND_MARKERS:
        idx = inbox_text.rfind(marker)
        if idx > best:
            best = idx
            marker_len = len(marker)
    if best >= 0:
        return inbox_text[best + marker_len :].strip()

    idx = inbox_text.rfind("**Accumulator for:**")
    if idx >= 0:
        return inbox_text[idx:].strip()
    return inbox_text.strip()


def active_chapter_from_status(status_text: str) -> str | None:
    match = re.search(r"\|\s*\*\*Active chapter\*\*\s*\|\s*`?([^`|\s]+)`?\s*\|", status_text)
    if not match:
        return None
    return match.group(1).strip()


def resolve_active_days_path(repo_root: Path, active_chapter: str | None) -> Path | None:
    if not active_chapter:
        return None
    candidates = [
        repo_root / "codex" / "years" / "2026" / "chapters" / active_chapter / "days.md",
        repo_root / "codex" / "2026" / "chapters" / active_chapter / "days.md",
        repo_root / "codex" / "chapters" / active_chapter / "days.md",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return candidates[0]


def article_capture_candidate(url: str) -> bool:
    u = url.lower()
    if "watch?v=tbd" in u:
        return False
    return (
        ("conflictsforum.substack.com" in u)
        or ("substack.com" in u and "/p/" in u)
        or ("youtube.com/watch?v=" in u)
        or ("youtu.be/" in u)
    )


def urls_from_text(text: str) -> set[str]:
    found: set[str] = set()
    for match in RE_URL.finditer(text):
        url = match.group(0).rstrip(".,);]")
        if len(url) > 12:
            found.add(url)
    return found


def normalize_url(url: str) -> str:
    return url.rstrip("/")


def source_urls_from_raw(raw_root: Path) -> set[str]:
    out: set[str] = set()
    if not raw_root.is_dir():
        return out
    for md in raw_root.rglob("*.md"):
        if md.name == "README.md":
            continue
        block = read_text(md)
        if not block.startswith("---"):
            continue
        end = block.find("\n---", 3)
        if end < 0:
            continue
        for line in block[3:end].splitlines():
            line = line.strip()
            if not line.startswith("source_url:"):
                continue
            val = line.split(":", 1)[1].strip().strip("\"'")
            if val.startswith("http"):
                out.add(normalize_url(val))
            break
    return out


def raw_input_pointer_rows(live_text: str) -> set[str]:
    """Rows that already point at a raw-input markdown file."""
    out: set[str] = set()
    for raw_line in live_text.splitlines():
        line = raw_line.strip()
        if RE_RAW_INPUT_MD.search(line):
            out.add(line)
    return out


def _url_has_raw_pointer_in_row(url: str, pointer_rows: set[str]) -> bool:
    return any(url in row for row in pointer_rows)


def raw_input_gap_urls(live_text: str, raw_root: Path) -> tuple[str, ...]:
    inbox_urls = {u for u in urls_from_text(live_text) if article_capture_candidate(u)}
    raw_urls = source_urls_from_raw(raw_root)
    pointer_rows = raw_input_pointer_rows(live_text)
    gaps: set[str] = set()
    for inbox_url in inbox_urls:
        if _url_has_raw_pointer_in_row(inbox_url, pointer_rows):
            continue
        ni = normalize_url(inbox_url)
        slug = ""
        if "/p/" in ni:
            slug = ni.split("/p/", 1)[1].split("?", 1)[0].strip("/")
        matched = any(
            ni == ru or ni.startswith(ru) or ru.startswith(ni) or (slug and slug in ru)
            for ru in raw_urls
        )
        if not matched:
            gaps.add(inbox_url)
    return tuple(sorted(gaps))


def raw_input_gap_count(live_text: str, raw_root: Path) -> int:
    return len(raw_input_gap_urls(live_text, raw_root))


def accumulator_drift_days(accumulator_date: str | None, *, today: date | None = None) -> int | None:
    if accumulator_date is None:
        return None
    today = today or date.today()
    try:
        parsed = date.fromisoformat(accumulator_date)
    except ValueError:
        return None
    return (today - parsed).days


def classify_lines(live_text: str) -> tuple[int, int, int, str]:
    ready = 0
    verify = 0
    carry = 0
    seam = ""

    for raw_line in live_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        lower = line.lower()
        if any(token in lower for token in ("batch-analysis", "page-ready", "strategy-page", "compose-read", "weave")):
            ready += 1
            if not seam:
                seam = line
        if "verify:" in lower or "verify-" in lower or "pending-primary" in lower or "needs verify" in lower:
            verify += 1
            if not seam:
                seam = line
        if any(token in lower for token in ("open loop", "carry", "revisit", "falsifier", "live tension", "tension:")):
            carry += 1
            if not seam:
                seam = line

    if not seam:
        nonempty = [line.strip() for line in live_text.splitlines() if line.strip()]
        seam = nonempty[-1] if nonempty else "No live accumulator residue detected."
    return ready, verify, carry, compress_line(seam)


def compress_line(line: str, max_len: int = 180) -> str:
    clean = " ".join(line.replace("`", "").split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 1] + "..."


def suggested_c_move(*, raw_input_gap: int, verify: int, ready: int) -> str:
    if raw_input_gap:
        return "source hygiene first - close raw-input gaps before composing."
    if verify:
        return "verify seam first - resolve source/claim status before synthesis."
    if ready:
        return "compose-read - review synthesis-ready clusters for page/chapter use."
    return "light daily-brief orientation - re-enter gently; no heavy compose signal yet."


def build_strategy_return_hint(
    repo_root: Path = REPO_ROOT,
    *,
    inbox_path: Path | None = None,
    raw_root: Path | None = None,
    status_path: Path | None = None,
) -> StrategyReturnHint:
    inbox = inbox_path or repo_root / "codex" / "daily-strategy-inbox.md"
    raw = raw_root or repo_root / "codex" / "years" / "2026" / "raw-input"
    status = status_path or repo_root / "codex" / "STATUS.md"

    live_text = live_accumulator_text(read_text(inbox))
    ready, verify, carry, live_seam = classify_lines(live_text)
    gap_urls = raw_input_gap_urls(live_text, raw)
    gaps = len(gap_urls)
    active = active_chapter_from_status(read_text(status))
    days = resolve_active_days_path(repo_root, active)
    days_rel = None
    if days is not None:
        try:
            days_rel = days.relative_to(repo_root).as_posix()
        except ValueError:
            days_rel = str(days)
    return StrategyReturnHint(
        live_seam=live_seam,
        ready=ready,
        verify=verify,
        raw_input_gap=gaps,
        raw_input_gap_urls=gap_urls,
        carry=carry,
        suggested_move=suggested_c_move(raw_input_gap=gaps, verify=verify, ready=ready),
        active_chapter=active,
        active_days_path=days_rel,
    )


def format_strategy_return_lines(repo_root: Path = REPO_ROOT) -> list[str]:
    return build_strategy_return_hint(repo_root).markdown_lines()


def configure_utf8_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    configure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Print the read-only Strategy return hint for explicit strategy/source return.")
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    print("\n".join(format_strategy_return_lines(args.repo_root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
