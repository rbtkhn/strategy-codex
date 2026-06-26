#!/usr/bin/env python3
"""Normalize Judging Freedom / Napolitano archive scaffold in place.

Spec (conservative trim lanes):
  1. cold_open — ideological boilerplate before the host intro anchor (always strip when detected)
  2. sponsor — separable canned reads after "But first, this" (or equivalent)
  3. close_promo — routine lineup / schedule tails at episode close

Keeps short host date + topic tease before guest entry. Default is dry-run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_ROOT = REPO_ROOT / "source-archive" / "statecraft"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TRANSCRIPT_SECTION_RE = re.compile(r"(^## Transcript\s*\n)(.*)$", re.DOTALL | re.MULTILINE)

HOST_INTRO_RE = re.compile(
    r"(?:\[Music\]\s*)*(?:Heat\.\s*Heat\.\s*)?"
    r"(?:>>\s*)?(?:\[music\]\s*)*(?:>>\s*)?"
    r"(?:Hi|Hey) everyone,?\s+"
    r"Judge Andrew N(?:ap(?:olitano|alitaniano)|palitano|palitaniano) here for (?:a\s+)?[Jj]udging\s+[Ff]reedom",
    re.IGNORECASE,
)
COLD_OPEN_SIGNAL_RE = re.compile(
    r"\b(?:Undeclared wars are commonplace|alter or abolish the government|"
    r"What if sometimes to love your country|freedom's greatest hour of danger|"
    r"preemptive war, otherwise known as aggression|What if Jefferson was right)\b",
    re.IGNORECASE,
)
SPONSOR_BRIDGE_RE = re.compile(r"\bBut first,?\s+this\b", re.IGNORECASE)
SPONSOR_SIGNAL_RE = re.compile(
    r"\b(?:Lear Capital|Patriot Supply|Patriot Preparedness|preparewiththe(?:adjudge|judge)?|"
    r"preparewiththeadjudge|leerjudgenap|Grid Doctor|bonus medals|qualified purchase|"
    r"call my friends at|my friends at Lear|precious metals?|gold and silver from|800\d{7})\b",
    re.IGNORECASE,
)
GUEST_ENTRY_RE = re.compile(
    r"(?:>>\s*)?"
    r"(?:(?:Professor|Prof\.|Ambassador|Amb\.|Colonel|Col\.|Dr\.|Judge|Ray)\s+"
    r"[\w\.'\s-]+,\s*(?:welcome|good day|always a pleasure|thank you|a pleasure|thank you very much))"
    r"|(?:Professor|Prof\.|Ambassador|Colonel|Col\.|Ray)\s+[\w\.'\s-]+\s+joins us now",
    re.IGNORECASE,
)
CLOSE_PROMO_START_RE = re.compile(
    r"(?:\s+And\s+)?(?:"
    r"Coming up(?:,?\s+(?:\w+\s+)*)(?:if you.re watching|on all of this|later today|tomorrow)|"
    r"coming up on all of this|"
    r"on Monday we will have(?: our usual lineup)?|"
    r"And of course on Monday|"
    r"All the best\.\s+Coming up|"
    r"Well, thank you for watching everybody\.)",
    re.IGNORECASE,
)
CLOSE_SIGNOFF_RE = re.compile(
    r"(?:Judge|judge)\s+Nap(?:olitano|alitaniano|palitaniano)\s+for\s+[Jj]udging\s+[Ff]reedom",
    re.IGNORECASE,
)
MUSIC_NOISE_RE = re.compile(r"(?:\[Music\]\s*|Heat\.\s*Heat\.\s*)+", re.IGNORECASE)

EDITORIAL_COLD_OPEN_NOTE = (
    "Ideological cold open trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_SPONSOR_NOTE = (
    "Canned sponsor read trimmed in place; SSOT body otherwise preserved."
)
EDITORIAL_CLOSE_NOTE = (
    "Routine closing lineup promo trimmed in place; SSOT body otherwise preserved."
)

GUEST_TITLE_PREFIXES = (
    "amb.",
    "ambassador",
    "colonel",
    "col.",
    "professor",
    "prof.",
    "judge",
    "dr.",
    "dr",
    "lt.",
)

VALID_TRIM_LANES = frozenset({"cold_open", "sponsor", "close_promo", "noise"})
DEFAULT_TRIM_LANES = VALID_TRIM_LANES


def parse_lanes(raw: str | None) -> frozenset[str]:
    if not raw:
        return DEFAULT_TRIM_LANES
    lanes = {part.strip() for part in raw.split(",") if part.strip()}
    unknown = lanes - VALID_TRIM_LANES
    if unknown:
        raise SystemExit(f"Unknown --lanes value(s): {', '.join(sorted(unknown))}")
    return frozenset(lanes)


@dataclass(frozen=True)
class FileChange:
    path: Path
    opening_tier: str
    cold_open_trimmed: bool = False
    sponsor_trimmed: bool = False
    close_promo_trimmed: bool = False
    paragraphs_removed: int = 0


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    return parse_simple_frontmatter(match.group(1)), text[match.end() :]


def parse_simple_frontmatter(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if value.startswith('"') and value.endswith('"'):
            data[key] = json.loads(value)
        elif value.lower() in {"true", "false"}:
            data[key] = value.lower() == "true"
        else:
            data[key] = value
    return data


def dump_simple_frontmatter(data: dict[str, Any]) -> str:
    lines: list[str] = []
    for key, value in data.items():
        if isinstance(value, bool):
            rendered = "true" if value else "false"
        else:
            text = str(value)
            if text == "" or any(ch in text for ch in ':"#[]{}') or text != text.strip():
                rendered = json.dumps(text, ensure_ascii=False)
            else:
                rendered = text
        lines.append(f"{key}: {rendered}")
    return "\n".join(lines)


def dump_frontmatter(data: dict[str, Any]) -> str:
    return f"---\n{dump_simple_frontmatter(data).rstrip()}\n---\n\n"


def is_napolitano_capture(meta: dict[str, Any], path: Path) -> bool:
    name = path.name.lower()
    channel = str(meta.get("channel_slug") or "").strip().lower()
    if channel in ("judging-freedom", "napolitano", "judge-napolitano-judging-freedom"):
        return True
    if not name.startswith("source-judging-freedom-"):
        return False
    show = str(meta.get("show") or meta.get("show_title") or "").strip().lower()
    if show and "judging freedom" not in show:
        return False
    return True


def split_paragraphs(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    return [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]


def join_paragraphs(paragraphs: list[str]) -> str:
    if not paragraphs:
        return ""
    return "\n\n".join(paragraphs).rstrip() + "\n"


def guest_paragraph_cues(guest: str) -> set[str]:
    clean = " ".join(guest.split()).strip()
    if not clean:
        return set()
    low = clean.lower()
    cues = {low}
    parts = [part for part in re.split(r"\s+", low) if part]
    if parts:
        cues.add(parts[-1])
    for title in GUEST_TITLE_PREFIXES:
        if low.startswith(title + " "):
            cues.add(low[len(title) + 1 :].strip())
    return {cue for cue in cues if cue}


def strip_leading_music_noise(text: str) -> tuple[str, bool]:
    stripped = MUSIC_NOISE_RE.sub("", text, count=1).lstrip()
    if stripped != text.lstrip():
        return stripped, True
    return text, False


def trim_cold_open_block(text: str) -> tuple[str, bool]:
    intro = HOST_INTRO_RE.search(text)
    if not intro:
        return text, False
    before = text[: intro.start()].strip()
    if not before:
        return text, False
    if not COLD_OPEN_SIGNAL_RE.search(before) and len(before.split()) < 40:
        # Short non-ideological preamble (e.g. music tags only) — handled elsewhere.
        return text, False
    trimmed = text[intro.start() :].lstrip()
    trimmed, _ = strip_leading_music_noise(trimmed)
    return trimmed, trimmed != text


def find_guest_entry_index(paragraphs: list[str], guest: str) -> int | None:
    joined = "\n\n".join(paragraphs[:6])
    match = GUEST_ENTRY_RE.search(joined)
    if match:
        offset = 0
        for idx, para in enumerate(paragraphs[:6]):
            if offset + len(para) >= match.start():
                return idx
            offset += len(para) + 2
    cues = guest_paragraph_cues(guest)
    for idx, para in enumerate(paragraphs[:6]):
        lower = para.lower()
        if cues and any(cue in lower for cue in cues):
            if re.search(r"\b(?:welcome|good day|thank you|joins us now|pleasure)\b", lower):
                return idx
    return None


def trim_sponsor_block(paragraphs: list[str], guest: str) -> tuple[list[str], bool]:
    if not paragraphs:
        return paragraphs, False
    guest_idx = find_guest_entry_index(paragraphs, guest)
    if guest_idx is None:
        guest_idx = min(5, len(paragraphs))

    window = paragraphs[: guest_idx + 1]
    window_text = "\n\n".join(window)
    if not SPONSOR_SIGNAL_RE.search(window_text):
        return paragraphs, False

    bridge = SPONSOR_BRIDGE_RE.search(window_text)
    guest_match = GUEST_ENTRY_RE.search(window_text)
    if not guest_match:
        return paragraphs, False
    if bridge and guest_match.start() <= bridge.start():
        return paragraphs, False
    if not bridge and not any(SPONSOR_SIGNAL_RE.search(p) for p in window[1:guest_idx]):
        return paragraphs, False

    new_window: list[str] = []
    sponsor_active = False
    for para in window:
        bridge_match = SPONSOR_BRIDGE_RE.search(para)
        guest_in_para = GUEST_ENTRY_RE.search(para)
        if bridge_match and guest_in_para and guest_in_para.start() > bridge_match.start():
            before = para[: bridge_match.start()].rstrip()
            after = para[guest_in_para.start() :].lstrip()
            if before:
                new_window.append(before)
            if after:
                new_window.append(after)
            sponsor_active = False
            continue
        if bridge_match:
            before = para[: bridge_match.start()].rstrip()
            if before:
                new_window.append(before)
            sponsor_active = True
            continue
        if sponsor_active:
            if guest_in_para or (
                guest
                and any(cue in para.lower() for cue in guest_paragraph_cues(guest))
                and re.search(r"\b(?:welcome|good day|thank you)\b", para, re.I)
            ):
                sponsor_active = False
                new_window.append(para)
            elif SPONSOR_SIGNAL_RE.search(para):
                continue
            else:
                sponsor_active = False
                new_window.append(para)
        else:
            new_window.append(para)

    if new_window == window:
        return paragraphs, False
    tail_start = guest_idx + 1 if guest_idx < len(paragraphs) - 1 else len(paragraphs)
    return new_window + paragraphs[tail_start:], True


def trim_close_promo_block(paragraphs: list[str]) -> tuple[list[str], bool]:
    if not paragraphs:
        return paragraphs, False
    full_text = "\n\n".join(paragraphs)
    search_window = full_text[-8000:] if len(full_text) > 8000 else full_text
    window_offset = len(full_text) - len(search_window)
    promo = CLOSE_PROMO_START_RE.search(search_window)
    if not promo:
        if CLOSE_SIGNOFF_RE.search(search_window) and re.search(
            r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b.*?"
            r"(?:morning|afternoon|evening)",
            search_window,
            re.I | re.DOTALL,
        ):
            promo = CLOSE_SIGNOFF_RE.search(search_window)
        else:
            return paragraphs, False
    cut_at = window_offset + promo.start()
    trimmed = full_text[:cut_at].rstrip()
    if not trimmed or trimmed == full_text:
        return paragraphs, False
    new_paragraphs = split_paragraphs(trimmed)
    if not new_paragraphs:
        return [trimmed], True
    if new_paragraphs == paragraphs:
        return paragraphs, False
    return new_paragraphs, True


def classify_opening_tier(
    paragraphs: list[str],
    *,
    cold_open_present: bool,
    sponsor_present: bool,
) -> str:
    if cold_open_present or sponsor_present:
        return "full-scaffold"
    if not paragraphs:
        return "clean"
    first = paragraphs[0]
    if HOST_INTRO_RE.search(first):
        words = len(first.split())
        if words <= 80:
            return "host-tease"
        return "host-tease"
    return "clean"


def opening_has_cold_open(paragraphs: list[str]) -> bool:
    if not paragraphs:
        return False
    text = "\n\n".join(paragraphs[:2])
    intro = HOST_INTRO_RE.search(text)
    if not intro:
        return bool(COLD_OPEN_SIGNAL_RE.search(text))
    return bool(COLD_OPEN_SIGNAL_RE.search(text[: intro.start()]))


def opening_has_sponsor(paragraphs: list[str]) -> bool:
    if not paragraphs:
        return False
    return bool(SPONSOR_SIGNAL_RE.search("\n\n".join(paragraphs[:5])))


def trim_transcript_body(
    body: str,
    guest: str,
    *,
    allow_cold_open: bool,
    allow_sponsor: bool,
    allow_close: bool,
    allow_noise: bool = True,
) -> tuple[str, bool, FileChange]:
    paragraphs = split_paragraphs(body)
    if not paragraphs:
        return body, False, FileChange(Path(), "clean")

    changed = False
    removed = 0
    cold_trimmed = False
    sponsor_trimmed = False
    close_trimmed = False

    joined = join_paragraphs(paragraphs)
    if allow_cold_open:
        new_joined, did = trim_cold_open_block(joined)
        if did:
            paragraphs = split_paragraphs(new_joined)
            cold_trimmed = True
            changed = True

    if allow_noise:
        noise_joined, noise = strip_leading_music_noise(join_paragraphs(paragraphs))
        if noise:
            paragraphs = split_paragraphs(noise_joined)
            changed = True

    if allow_sponsor:
        new_paragraphs, did = trim_sponsor_block(paragraphs, guest)
        if did:
            removed += max(0, len(paragraphs) - len(new_paragraphs))
            paragraphs = new_paragraphs
            sponsor_trimmed = True
            changed = True

    if allow_close:
        new_paragraphs, did = trim_close_promo_block(paragraphs)
        if did:
            removed += max(0, len(paragraphs) - len(new_paragraphs))
            paragraphs = new_paragraphs
            close_trimmed = True
            changed = True

    tier = classify_opening_tier(
        paragraphs,
        cold_open_present=opening_has_cold_open(paragraphs),
        sponsor_present=opening_has_sponsor(paragraphs),
    )
    if not changed:
        tier = classify_opening_tier(
            paragraphs,
            cold_open_present=False,
            sponsor_present=opening_has_sponsor(paragraphs),
        )

    new_body = join_paragraphs(paragraphs) if changed else body
    return (
        new_body,
        changed,
        FileChange(
            Path(),
            tier,
            cold_open_trimmed=cold_trimmed,
            sponsor_trimmed=sponsor_trimmed,
            close_promo_trimmed=close_trimmed,
            paragraphs_removed=removed,
        ),
    )


def split_body_sections(body: str) -> tuple[str, str, str]:
    match = TRANSCRIPT_SECTION_RE.search(body)
    if match:
        prefix = body[: match.start()]
        transcript_header = match.group(1)
        transcript_body = match.group(2)
        return prefix, transcript_header, transcript_body

    lines = body.splitlines(keepends=True)
    idx = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        if stripped == "" or stripped.startswith("#") or stripped.startswith("**"):
            idx += 1
            continue
        break
    while idx < len(lines) and lines[idx].strip() == "":
        idx += 1
    prefix = "".join(lines[:idx])
    transcript_body = "".join(lines[idx:])
    return prefix, "", transcript_body


def merge_body_sections(prefix: str, transcript_header: str, transcript_body: str) -> str:
    if not transcript_header:
        return prefix + transcript_body
    return prefix + transcript_header + transcript_body


def append_editorial_note(meta: dict[str, Any], note: str) -> None:
    existing = str(meta.get("editorial_note") or "").strip()
    if note.lower() in existing.lower():
        return
    meta["editorial_note"] = f"{existing} {note}".strip() if existing else note


def normalize_text(
    path: Path,
    text: str,
    *,
    tag_only: bool = False,
    lanes: frozenset[str] = DEFAULT_TRIM_LANES,
) -> tuple[bool, str, FileChange | None]:
    meta, body = split_frontmatter(text)
    if not is_napolitano_capture(meta, path):
        return False, text, None

    guest = str(meta.get("guest") or "")
    prefix, transcript_header, transcript_body = split_body_sections(body)
    if not transcript_body.strip():
        return False, text, None

    original_paragraphs = split_paragraphs(transcript_body)
    cold_done = bool(meta.get("napolitano_cold_open_trim_applied"))
    sponsor_done = bool(meta.get("napolitano_sponsor_trim_applied"))
    close_done = bool(meta.get("napolitano_close_promo_trim_applied"))
    noise_done = bool(meta.get("napolitano_leading_noise_trim_applied"))

    allow_cold_open = "cold_open" in lanes and not cold_done
    allow_sponsor = "sponsor" in lanes and not sponsor_done
    allow_close = "close_promo" in lanes and not close_done
    allow_noise = "noise" in lanes and not noise_done

    if tag_only:
        tier = classify_opening_tier(
            original_paragraphs,
            cold_open_present=opening_has_cold_open(original_paragraphs),
            sponsor_present=opening_has_sponsor(original_paragraphs),
        )
        if meta.get("opening_tier") != tier:
            meta["opening_tier"] = tier
            return True, dump_frontmatter(meta) + body, FileChange(path, tier)
        return False, text, None

    lane_done = {
        "cold_open": cold_done,
        "sponsor": sponsor_done,
        "close_promo": close_done,
        "noise": noise_done,
    }
    if all(lane_done[lane] for lane in lanes):
        tier = str(meta.get("opening_tier") or "host-tease")
        return False, text, FileChange(path, tier)

    new_body, changed, change = trim_transcript_body(
        transcript_body,
        guest,
        allow_cold_open=allow_cold_open,
        allow_sponsor=allow_sponsor,
        allow_close=allow_close,
        allow_noise=allow_noise,
    )
    if not changed:
        if meta.get("opening_tier"):
            return False, text, FileChange(path, str(meta.get("opening_tier")))
        tier = classify_opening_tier(
            original_paragraphs,
            cold_open_present=False,
            sponsor_present=opening_has_sponsor(original_paragraphs),
        )
        meta["opening_tier"] = tier
        return True, dump_frontmatter(meta) + body, FileChange(path, tier)

    if change.cold_open_trimmed:
        meta["napolitano_cold_open_trim_applied"] = True
        append_editorial_note(meta, EDITORIAL_COLD_OPEN_NOTE)
    if change.sponsor_trimmed:
        meta["napolitano_sponsor_trim_applied"] = True
        append_editorial_note(meta, EDITORIAL_SPONSOR_NOTE)
    if change.close_promo_trimmed:
        meta["napolitano_close_promo_trim_applied"] = True
        append_editorial_note(meta, EDITORIAL_CLOSE_NOTE)
    if (
        change.cold_open_trimmed
        or change.sponsor_trimmed
        or change.close_promo_trimmed
        or (
            changed
            and not change.cold_open_trimmed
            and not change.sponsor_trimmed
            and not change.close_promo_trimmed
        )
    ):
        meta["napolitano_leading_noise_trim_applied"] = True

    meta["opening_tier"] = change.opening_tier
    merged = merge_body_sections(prefix, transcript_header, new_body)
    new_text = dump_frontmatter(meta) + merged
    return (
        True,
        new_text,
        FileChange(
            path,
            change.opening_tier,
            cold_open_trimmed=change.cold_open_trimmed,
            sponsor_trimmed=change.sponsor_trimmed,
            close_promo_trimmed=change.close_promo_trimmed,
            paragraphs_removed=change.paragraphs_removed,
        ),
    )


def candidate_paths(root: Path, explicit: list[Path] | None = None) -> list[Path]:
    if explicit:
        return sorted({p.resolve() for p in explicit})
    paths: list[Path] = []
    for path in root.rglob("source-judging-freedom-*.md"):
        if ".cleaned." in path.name:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        meta, _ = split_frontmatter(text)
        if is_napolitano_capture(meta, path):
            paths.append(path)
    return sorted(set(paths))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ARCHIVE_ROOT)
    parser.add_argument("--path", type=Path, action="append", default=[], help="Explicit archive file(s).")
    parser.add_argument("--apply", action="store_true", help="Write changes in place.")
    parser.add_argument("--tag-only", action="store_true", help="Only set opening_tier metadata.")
    parser.add_argument(
        "--lanes",
        default="cold_open,sponsor,close_promo,noise",
        help="Comma-separated trim lanes (default: all).",
    )
    args = parser.parse_args()
    lanes = parse_lanes(args.lanes)

    explicit = [REPO_ROOT / p if not p.is_absolute() else p for p in args.path] if args.path else None
    paths = candidate_paths(args.root, explicit)
    changes: list[FileChange] = []
    skipped = 0

    for path in paths:
        text = path.read_text(encoding="utf-8")
        changed, new_text, file_change = normalize_text(
            path, text, tag_only=args.tag_only, lanes=lanes
        )
        if file_change is None:
            skipped += 1
            continue
        if changed:
            changes.append(file_change)
            if args.apply:
                path.write_text(new_text, encoding="utf-8")

    mode = "Applied" if args.apply else "Dry-run"
    print(f"{mode}: {len(changes)} Napolitano transcript file(s) would change; {skipped} skipped.")
    for change in changes:
        flags: list[str] = []
        if change.cold_open_trimmed:
            flags.append("cold_open")
        if change.sponsor_trimmed:
            flags.append("sponsor")
        if change.close_promo_trimmed:
            flags.append("close_promo")
        if change.paragraphs_removed:
            flags.append(f"-{change.paragraphs_removed}p")
        joined = ", ".join(flags) if flags else "metadata"
        rel = change.path.relative_to(REPO_ROOT).as_posix()
        print(f"- {rel} [{joined}] tier={change.opening_tier}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
