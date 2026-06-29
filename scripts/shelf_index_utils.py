#!/usr/bin/env python3
"""Shared shelf index resolution, exclusion, and row-append helpers."""
from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

REPO_ROOT = Path(__file__).resolve().parents[1]
VOICES_DIR = REPO_ROOT / "statecraft" / "voices"

WRITER_SHELF_SLUGS = frozenset({"parsi", "pape", "crooke", "ritter"})

# Slugs with slug-specific logic in shelf_capture_excluded() — must have YAML exclusions entry.
CODE_EXCLUSION_SLUGS = frozenset({"pape", "ritter", "crooke", "jiang", "karaganov"})

GUEST_REBUILD_SHELF_SLUGS = frozenset(
    {
        "aguilar",
        "baud",
        "hoh",
        "jiang",
        "kent",
        "matlock",
        "martyanov",
        "postol",
        "krapivnik",
        "krainer",
    }
)

GUEST_NAME_PATTERNS: dict[str, re.Pattern[str]] = {
    "baud": re.compile(r"jacques\s+baud|col\.?\s+jacques\s+baud|\bbaud\b", re.I),
    "aguilar": re.compile(r"anthony\s+aguilar|lt\.?\s*col\.?\s+anthony\s+aguilar", re.I),
    "parsi": re.compile(r"trita\s+parsi|\bparsi\b", re.I),
    "pape": re.compile(r"robert\s+pape|professor\s+pape|prof\s+pape|\bpape\b", re.I),
    "crooke": re.compile(r"alastair\s+crooke|\bcrooke\b", re.I),
    "ritter": re.compile(r"scott\s+ritter|\britter\b", re.I),
    "martyanov": re.compile(r"andrei\s+martyanov|\bmartyanov\b|\bmartynaov\b", re.I),
    "krainer": re.compile(r"alex\s+krainer|\bkrainer\b", re.I),
    "kent": re.compile(r"joe\s+kent", re.I),
    "matlock": re.compile(r"jack\s+matlock", re.I),
    "jiang": re.compile(r"jiang\s+xueqin", re.I),
}

JIANG_SNEAKO_INTERVIEW = "source-interviews-15-sneako-jiang-dugin-eschatology-2026-04-14.md"
JIANG_PH_FILENAME_PREFIXES = (
    "source-game-theory-",
    "source-gb-",
    "source-predictive-history-",
)

SLUG_FILENAME_ALIASES: dict[str, tuple[str, ...]] = {
    "alkhorshid": ("alkorshid",),
    "martyanov": ("martynaov",),
}

PAPE_DATE_STUB = re.compile(r"^source-pape-\d{4}-\d{2}-\d{2}\.md$", re.I)
RITTER_DATE_STUB = re.compile(r"^source-ritter-\d{4}-\d{2}-\d{2}\.md$", re.I)
INTERVIEW_KINDS = frozenset({"transcript", "cleaned-transcript", "interview"})
AUTHORED_KINDS = frozenset({"substack-post", "article", "essay", "newsletter", "rss-item"})
_SLUG_FILENAME_PATTERNS: dict[str, re.Pattern[str]] = {}


def slug_token_in_capture_filename(slug: str, filename: str) -> bool:
    """Match slug as a hyphen-delimited token in capture filenames (not substring)."""
    key = slug.casefold()
    tokens = (key,) + SLUG_FILENAME_ALIASES.get(key, ())
    name_fold = filename.casefold()
    for token in tokens:
        pattern = _SLUG_FILENAME_PATTERNS.get(token)
        if pattern is None:
            slug_esc = re.escape(token)
            pattern = re.compile(rf"(?:^|-){slug_esc}(?:-|\.|$)", re.I)
            _SLUG_FILENAME_PATTERNS[token] = pattern
        if pattern.search(name_fold):
            return True
    return False


def norm_scalar(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return norm_scalar(value[0]) if value else ""
    return str(value).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def shelf_index_path(slug: str, voices_dir: Path | None = None) -> Path:
    base = voices_dir or VOICES_DIR
    return base / slug / f"{slug}-index.md"


def companion_paths(slug: str, voices_dir: Path | None = None) -> list[Path]:
    base = voices_dir or VOICES_DIR
    shelf = base / slug
    if not shelf.is_dir():
        return []
    out: list[Path] = []
    for pattern in (f"{slug}-forecast-ledger*.md", f"{slug}-interview-appearances*.md"):
        out.extend(sorted(shelf.glob(pattern)))
    return out


def _pape_janssen_studio(meta: dict[str, object], body: str) -> bool:
    if re.search(
        r"cyrus\s+janssen\s+studio|pape\s*\(\s*cyrus\s+janssen|cannot beat iran|can not beat iran",
        body,
        re.I,
    ):
        return True
    title = norm_scalar(meta.get("title"))
    return "Cyrus Janssen studio" in title or "Can NOT Beat Iran" in title


def _jiang_named_guest(meta: dict[str, object]) -> bool:
    pattern = GUEST_NAME_PATTERNS.get("jiang")
    if pattern is None:
        return False
    guest = norm_scalar(meta.get("guest"))
    if guest and pattern.search(guest):
        return True
    people = meta.get("guest_people")
    if isinstance(people, list):
        for person in people:
            if pattern.search(str(person)):
                return True
    elif people and pattern.search(str(people)):
        return True
    return False


def _jiang_is_host(meta: dict[str, object]) -> bool:
    pattern = GUEST_NAME_PATTERNS.get("jiang")
    if pattern is None:
        return False
    host = norm_scalar(meta.get("host"))
    if host and pattern.search(host):
        return True
    host_people = meta.get("host_people")
    if isinstance(host_people, list):
        for person in host_people:
            if pattern.search(str(person)):
                return True
    elif host_people and pattern.search(str(host_people)):
        return True
    return False


def _jiang_ph_owned_filename(path: Path) -> bool:
    name = path.name.casefold()
    if name == JIANG_SNEAKO_INTERVIEW.casefold():
        return False
    for prefix in JIANG_PH_FILENAME_PREFIXES:
        if name.startswith(prefix):
            return True
    if name.startswith("source-interviews-"):
        return True
    return False


def is_jiang_external_interview(
    meta: dict[str, object], path: Path, body: str = ""
) -> bool:
    """True when capture belongs on jiang-index (external-channel guest appearances)."""
    name = path.name.casefold()
    if name.startswith("source-dialogue-works-") and "jiang" in name:
        return False
    if name == JIANG_SNEAKO_INTERVIEW.casefold():
        pattern = GUEST_NAME_PATTERNS["jiang"]
        title = norm_scalar(meta.get("title"))
        return bool(pattern.search(title) or pattern.search(body[:2000]))
    if _jiang_ph_owned_filename(path):
        return False
    source_form = norm_scalar(meta.get("source_form"))
    kind = norm_scalar(meta.get("kind"))
    if source_form == "solo":
        return False
    if _jiang_is_host(meta):
        return False
    if kind not in INTERVIEW_KINDS and source_form not in {"interview"}:
        return False
    if not _jiang_named_guest(meta):
        return False
    return True


def shelf_capture_excluded(slug: str, path: Path, meta: dict[str, object], body: str = "") -> bool:
    name = path.name.casefold()
    slug_fold = slug.casefold()
    if slug == "jiang":
        return not is_jiang_external_interview(meta, path, body)
    if slug == "pape":
        if name.startswith("verify-pape-"):
            return True
        if name.startswith("x-pape-"):
            return True
        if PAPE_DATE_STUB.match(path.name) and not _pape_janssen_studio(meta, body):
            return True
        source_path = norm_scalar(meta.get("source_path"))
        if "strategy-notebook/experts/pape/transcript" in source_path:
            return True
        return False
    if slug == "ritter":
        if RITTER_DATE_STUB.match(path.name):
            return True
        if name.startswith("verify-ritter-") or name.startswith("ritter-rant-"):
            return True
        return False
    if slug == "crooke":
        if re.match(r"^\d{4}-\d{2}-\d{2}-crooke\.md$", path.name, re.I):
            return True
        if name == "transcript-crooke.md" or name.startswith("verify-crooke-"):
            return True
        return False
    if slug == "parsi":
        return False
    if slug == "karaganov":
        # Ritter (and similar) reaction essays cite Karaganov but are not guest appearances.
        if name.startswith("source-ritter-") and slug_token_in_capture_filename("karaganov", path.name):
            return True
        return False
    return False


def _guest_named(meta: dict[str, object], slug: str) -> bool:
    pattern = GUEST_NAME_PATTERNS.get(slug)
    if pattern is None:
        return False
    title = norm_scalar(meta.get("title"))
    if pattern.search(title):
        return True
    guest = norm_scalar(meta.get("guest"))
    if guest and pattern.search(guest):
        return True
    for key in ("guest_people", "host_people", "people"):
        people = meta.get(key)
        if isinstance(people, list):
            for person in people:
                if pattern.search(str(person)):
                    return True
        elif people and pattern.search(str(people)):
            return True
    author = norm_scalar(meta.get("author"))
    if slug in ("pape", "crooke", "ritter", "parsi") and pattern.search(author):
        return True
    return False


def capture_matches_shelf(slug: str, path: Path, meta: dict[str, object], body: str = "") -> bool:
    if slug == "jiang":
        return is_jiang_external_interview(meta, path, body)
    if shelf_capture_excluded(slug, path, meta, body):
        return False
    slug_fold = slug.casefold()
    if norm_scalar(meta.get("thread")) == slug:
        return True
    if slug_token_in_capture_filename(slug, path.name):
        return True
    if _guest_named(meta, slug):
        return True
    return False


def resolve_shelf_slugs(path: Path, meta: dict[str, object], body: str = "") -> list[str]:
    slugs: list[str] = []
    for slug in sorted(WRITER_SHELF_SLUGS | GUEST_REBUILD_SHELF_SLUGS):
        if not shelf_index_path(slug).is_file():
            continue
        if capture_matches_shelf(slug, path, meta, body):
            slugs.append(slug)
    return slugs


CaptureClass = Literal["authored", "guest", "other"]


def classify_capture_class(slug: str, path: Path, meta: dict[str, object], body: str = "") -> CaptureClass:
    kind = norm_scalar(meta.get("kind"))
    source_form = norm_scalar(meta.get("source_form"))
    name = path.name.casefold()
    slug_fold = slug.casefold()
    if slug == "pape":
        import build_pape_index as pape_idx  # noqa: E402

        if pape_idx.is_pape_guest(meta, body):
            return "guest"
        if kind in AUTHORED_KINDS or name.startswith("source-pape-"):
            return "authored"
        return "guest"
    if kind in AUTHORED_KINDS or (name.startswith(f"source-{slug}-") and kind not in INTERVIEW_KINDS):
        return "authored"
    if kind in INTERVIEW_KINDS or source_form in {"interview", "post", "solo"}:
        return "guest"
    if norm_scalar(meta.get("thread")) == slug and kind not in INTERVIEW_KINDS:
        return "authored"
    return "guest" if slug_fold not in name else "authored"


def pub_date_for_capture(meta: dict[str, object], path: Path) -> str:
    pub = norm_scalar(meta.get("pub_date"))
    if len(pub) >= 10:
        return pub[:10]
    day = path.parent.name
    if re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        return day
    return day


def month_heading(pub_date: str) -> str:
    if len(pub_date) >= 7:
        return f"## {pub_date[:7]}"
    return f"## {pub_date}"


def short_title(meta: dict[str, object], path: Path) -> str:
    title = norm_scalar(meta.get("title"))
    if not title or title == path.stem:
        title = path.stem.removeprefix("source-").replace("-", " ")
        if len(title) > 72:
            title = title[:69] + "…"
        return title.title()
    if len(title) > 72:
        title = title[:69] + "…"
    return title


def archive_rel_link(path: Path) -> str:
    return f"../../../source-archive/statecraft/{path.parent.name}/{path.name}"


def format_index_row(
    slug: str,
    path: Path,
    meta: dict[str, object],
    *,
    capture_class: CaptureClass,
) -> str:
    pub = pub_date_for_capture(meta, path)
    title = short_title(meta, path)
    rel = archive_rel_link(path)
    label = f"{pub} — {title}"
    if capture_class == "authored":
        suffix = " — **authored**"
    else:
        host = norm_scalar(meta.get("host")) or norm_scalar(meta.get("channel_slug")) or "host"
        suffix = f" — **guest** · {host}"
    return f"- [{label}]({rel}){suffix}"


def capture_cited_in_index(index_text: str, path: Path) -> bool:
    rel = f"source-archive/statecraft/{path.parent.name}/{path.name}".replace("\\", "/")
    return path.name in index_text or rel in index_text


def append_capture_to_index(
    slug: str,
    path: Path,
    meta: dict[str, object],
    *,
    body: str = "",
    voices_dir: Path | None = None,
) -> bool:
    index_path = shelf_index_path(slug, voices_dir)
    if not index_path.is_file():
        return False
    text = read_text(index_path)
    if capture_cited_in_index(text, path):
        return False
    capture_class = classify_capture_class(slug, path, meta, body)
    row = format_index_row(slug, path, meta, capture_class=capture_class)
    pub = pub_date_for_capture(meta, path)
    heading = month_heading(pub)
    if heading not in text:
        text = text.rstrip() + f"\n\n{heading}\n\n{row}\n"
    else:
        parts = text.split(heading, 1)
        after = parts[1]
        next_h = re.search(r"\n## \d{4}-\d{2}", after)
        if next_h:
            insert_at = next_h.start()
            after = after[:insert_at].rstrip() + f"\n{row}" + after[insert_at:]
        else:
            after = after.rstrip() + f"\n{row}\n"
        text = parts[0] + heading + after
    index_path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8", newline="\n")
    return True
