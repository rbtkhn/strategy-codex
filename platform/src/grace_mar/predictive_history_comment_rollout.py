"""Predictive History single-phase YouTube comment rollout.

Phase 1 posts a trust-first chapter-folder doorway comment for each public
Predictive History video.

The rollout is review-gated:
- build a deterministic queue from the public source index
- mark entries approved or rejected
- post only approved, non-parked entries

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

from grace_mar.repo_io import repo_root

REPO_ROOT = repo_root()
PH_CIV_ROOT = REPO_ROOT / "codex" / "academy" / "ph-civ"
PH_CIV_SRC = PH_CIV_ROOT / "platform/src"
SOURCE_INDEX_PATH = PH_CIV_ROOT / "docs" / "source-video-index.md"
QUEUE_DIR = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "predictive-history-comment-rollout"
QUEUE_PATH = QUEUE_DIR / "queue.json"
DRAFTS_DIR = QUEUE_DIR / "drafts"
PH_CIV_GITHUB_BASE = "https://github.com/rbtkhn/ph-civ"
PH_CIV_TREE_BASE = f"{PH_CIV_GITHUB_BASE}/tree/main"
PH_CIV_BLOB_BASE = f"{PH_CIV_GITHUB_BASE}/blob/main"
YOUTUBE_INSERT_URL = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet"


@dataclass(frozen=True)
class SourceVideo:
    video_id: str
    source_id: str
    title: str
    youtube_url: str
    transcript_path: str


def _ensure_ph_civ_importable() -> None:
    if PH_CIV_SRC.exists() and str(PH_CIV_SRC) not in sys.path:
        sys.path.insert(0, str(PH_CIV_SRC))


def _ph_cli():
    _ensure_ph_civ_importable()
    from civ_ph import cli as ph_cli  # type: ignore

    return ph_cli


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _slugify_filename(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-").lower()
    return slug or "untitled"


def load_source_videos(path: Path = SOURCE_INDEX_PATH) -> list[SourceVideo]:
    """Parse the public source video index table into structured rows."""
    videos: list[SourceVideo] = []
    for line in _read_text(path).splitlines():
        if not line.startswith("|"):
            continue
        if line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        source_cell, title, youtube_cell, transcript_cell = cells
        source_match = re.match(r"`([^`]+)`", source_cell)
        youtube_match = re.match(r"\[video\]\(([^)]+)\)", youtube_cell)
        transcript_match = re.match(r"\[([^\]]+)\]\(([^)]+)\)", transcript_cell)
        if not (source_match and youtube_match and transcript_match):
            continue
        youtube_url = youtube_match.group(1)
        videos.append(
            SourceVideo(
                video_id=_video_id_from_url(youtube_url),
                source_id=source_match.group(1),
                title=title,
                youtube_url=youtube_url,
                transcript_path=transcript_match.group(2),
            )
        )
    return videos


def _existing_rows(queue_path: Path) -> dict[tuple[str, int], dict[str, Any]]:
    if not queue_path.exists():
        return {}
    data = json.loads(_read_text(queue_path))
    rows = data.get("rows", data if isinstance(data, list) else [])
    return {
        (row["source_id"], int(row["phase"])): row
        for row in rows
        if row.get("source_id") and row.get("phase") is not None
    }


def _chapter_folder_url(payload: dict[str, Any]) -> str | None:
    return payload.get("github_folder_url")


def _phase1_comment(payload: dict[str, Any]) -> str:
    return payload["suggested_youtube_comment"]


def _base_queue_entry(
    *,
    video: SourceVideo,
    phase: int,
    phase_name: str,
) -> dict[str, Any]:
    return {
        "video_id": video.video_id,
        "source_id": video.source_id,
        "title": video.title,
        "youtube_url": video.youtube_url,
        "transcript_path": video.transcript_path,
        "phase": phase,
        "phase_name": phase_name,
        "approval_state": "needs_review",
        "status": "parked",
        "park_reason": "",
        "comment_draft": "",
        "target_url": "",
        "source_link_type": "",
        "museum_status": "",
        "museum_exhibit_path": "",
        "chapter_folder_path": "",
        "review_status": "",
        "posted_comment_id": "",
        "posted_comment_url": "",
        "posted_at_utc": "",
        "post_receipt": {},
    }


def _merge_state(entry: dict[str, Any], existing: dict[str, Any] | None) -> dict[str, Any]:
    if not existing:
        return entry
    merged = {**entry}
    for key in (
        "approval_state",
        "status",
        "park_reason",
        "comment_draft",
        "target_url",
        "source_link_type",
        "museum_status",
        "museum_exhibit_path",
        "chapter_folder_path",
        "review_status",
        "posted_comment_id",
        "posted_comment_url",
        "posted_at_utc",
        "post_receipt",
    ):
        if key in existing and existing[key] not in (None, ""):
            merged[key] = existing[key]
    return merged


def build_queue_rows(
    *,
    queue_path: Path = QUEUE_PATH,
    source_index_path: Path = SOURCE_INDEX_PATH,
) -> list[dict[str, Any]]:
    ph_cli = _ph_cli()
    existing = _existing_rows(queue_path)
    rows: list[dict[str, Any]] = []

    for video in load_source_videos(source_index_path):
        try:
            card = ph_cli.get_card(video.source_id)
        except KeyError:
            card = None

        phase1 = _base_queue_entry(video=video, phase=1, phase_name="chapter_folder_doorway")
        phase1["source_link_type"] = "chapter_folder"
        if card is not None:
            payload = ph_cli.chapter_folder_link_payload(card)
            phase1["review_status"] = payload.get("review_status", "")
            if payload.get("folder_ready") and payload.get("github_folder_url"):
                phase1["status"] = "ready"
                phase1["target_url"] = payload["github_folder_url"]
                phase1["chapter_folder_path"] = payload.get("chapter_folder_path") or ""
                phase1["comment_draft"] = _phase1_comment(payload)
            else:
                phase1["status"] = "parked"
                phase1["park_reason"] = "chapter folder is not ready"
        else:
            phase1["status"] = "parked"
            phase1["park_reason"] = "no PH card found for source_id"
        phase1 = _merge_state(phase1, existing.get((video.source_id, 1)))
        rows.append(phase1)

    rows.sort(key=lambda row: (row["source_id"], int(row["phase"])))
    return rows


def save_queue(rows: list[dict[str, Any]], path: Path = QUEUE_PATH) -> None:
    payload = {"rows": rows, "generated_at_utc": datetime.now(timezone.utc).isoformat()}
    _write_text(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def _render_phase1_draft_markdown(row: dict[str, Any]) -> str:
    lines = [
        f"# {row['source_id']} - Phase 1 YouTube comment draft",
        "",
        "> Local-only draft review surface stored in `strategy-codex`.",
        "> Canonical workflow state lives in `queue.json`.",
        "",
        "## Metadata",
        "",
        f"- Source ID: `{row['source_id']}`",
        f"- Title: {row.get('title', '')}",
        f"- YouTube URL: {row.get('youtube_url', '')}",
        f"- Chapter-folder target URL: {row.get('target_url', '') or '(not ready)'}",
        f"- Packet review status: `{row.get('review_status', '') or 'n/a'}`",
        f"- Workflow status: `{row.get('status', '')}`",
        f"- Approval state: `{row.get('approval_state', '')}`",
        f"- Source link type: `{row.get('source_link_type', '') or 'chapter_folder'}`",
    ]
    if row.get("chapter_folder_path"):
        lines.append(f"- Chapter-folder path: `{row['chapter_folder_path']}`")
    if row.get("posted_comment_url"):
        lines.append(f"- Posted comment URL: {row['posted_comment_url']}")
    if row.get("posted_at_utc"):
        lines.append(f"- Posted at UTC: `{row['posted_at_utc']}`")
    if row.get("park_reason"):
        lines.append(f"- Park reason: {row['park_reason']}")
    lines.extend(
        [
            "",
            "## Draft",
            "",
        ]
    )
    if row.get("comment_draft"):
        lines.extend([row["comment_draft"], ""])
    else:
        lines.extend(
            [
                "_No draft text rendered yet._",
                "",
            ]
        )
    lines.extend(
        [
            "## Notes",
            "",
            "- These files are for human review readability only.",
            "- Edit workflow/posting state through the canonical queue, not by treating this file as a second source of truth.",
            "- Posted YouTube comments are public outputs, but the drafting workspace remains local to `strategy-codex`.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_phase1_drafts(rows: list[dict[str, Any]], drafts_dir: Path = DRAFTS_DIR) -> list[Path]:
    drafts_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    expected_names: set[str] = set()
    for row in rows:
        if int(row.get("phase", 0)) != 1:
            continue
        filename = f"{_slugify_filename(str(row['source_id']))}.md"
        expected_names.add(filename)
        path = drafts_dir / filename
        _write_text(path, _render_phase1_draft_markdown(row))
        written.append(path)
    for existing in drafts_dir.glob("*.md"):
        if existing.name not in expected_names:
            existing.unlink()
    return written


def load_queue(path: Path = QUEUE_PATH) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(_read_text(path))
    rows = payload.get("rows", payload if isinstance(payload, list) else [])
    return list(rows)


def _status_counts(rows: list[dict[str, Any]], *, phase: int | None = None) -> dict[str, int]:
    counts: dict[str, int] = {"ready": 0, "parked": 0, "approved": 0, "posted": 0, "needs_review": 0, "rejected": 0}
    for row in rows:
        if phase is not None and int(row.get("phase", 0)) != phase:
            continue
        counts.setdefault(str(row.get("status", "")), 0)
        counts[str(row.get("status", ""))] += 1
        counts.setdefault(str(row.get("approval_state", "")), 0)
        counts[str(row.get("approval_state", ""))] += 1
    return counts


def render_markdown_summary(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# Predictive History chapter-folder comment rollout",
        "",
        f"- Queue rows: {len(rows)}",
        f"- Phase 1 ready: {_status_counts(rows, phase=1).get('ready', 0)}",
        f"- Phase 1 parked: {_status_counts(rows, phase=1).get('parked', 0)}",
        "",
        "## Ready rows",
        "",
        "| Source | Phase | Status | Approval | Target |",
        "|---|---:|---|---|---|",
    ]
    for row in rows:
        if row.get("status") != "ready":
            continue
        target = row.get("target_url", "")
        lines.append(
            f"| {row['source_id']} | {row['phase']} | ready | {row.get('approval_state', '')} | {target} |"
        )
    lines.append("")
    lines.append("## Parked rows")
    lines.append("")
    lines.append("| Source | Phase | Park reason |")
    lines.append("|---|---:|---|")
    for row in rows:
        if row.get("status") != "parked":
            continue
        lines.append(f"| {row['source_id']} | {row['phase']} | {row.get('park_reason', '')} |")
    return "\n".join(lines)


def render_telegram_summary(rows: list[dict[str, Any]]) -> str:
    phase1 = _status_counts(rows, phase=1)
    return "\n".join(
        [
            "> Predictive History chapter-folder rollout update:",
            f"> - Phase 1 ready: {phase1.get('ready', 0)}",
            f"> - Phase 1 parked: {phase1.get('parked', 0)}",
            ">",
            "> Phase 1 uses the chapter-folder doorway comment only.",
        ]
    )


def _video_id_from_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.hostname in {"youtu.be"}:
        return parsed.path.lstrip("/")
    if parsed.hostname and "youtube.com" in parsed.hostname:
        query = parse_qs(parsed.query)
        if "v" in query and query["v"]:
            return query["v"][0]
    raise ValueError(f"Could not parse YouTube video id from URL: {url}")


def _youtube_insert_comment(*, video_id: str, text: str, access_token: str, timeout: int = 30) -> dict[str, Any]:
    payload = {
        "snippet": {
            "videoId": video_id,
            "topLevelComment": {"snippet": {"textOriginal": text}},
        }
    }
    data = json.dumps(payload).encode("utf-8")
    request = Request(
        YOUTUBE_INSERT_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def _comment_url(video_id: str, comment_id: str | int) -> str:
    return f"https://www.youtube.com/watch?v={video_id}&lc={comment_id}"


def set_entry_state(
    *,
    queue_path: Path,
    source_id: str,
    phase: int,
    approval_state: str,
) -> list[dict[str, Any]]:
    rows = load_queue(queue_path)
    updated = False
    for row in rows:
        if row.get("source_id") == source_id and int(row.get("phase", 0)) == phase:
            row["approval_state"] = approval_state
            updated = True
            break
    if not updated:
        raise KeyError(f"No queue row found for {source_id} phase {phase}")
    save_queue(rows, queue_path)
    return rows


def post_approved_rows(
    *,
    queue_path: Path,
    phase: int | None,
    access_token: str,
    dry_run: bool = False,
    source_id: str | None = None,
) -> list[dict[str, Any]]:
    rows = load_queue(queue_path)
    changed = False
    for row in rows:
        if source_id is not None and row.get("source_id") != source_id:
            continue
        if phase is not None and int(row.get("phase", 0)) != phase:
            continue
        if row.get("status") != "ready" or row.get("approval_state") != "approved":
            continue
        if row.get("posted_comment_id"):
            continue
        video_id = row.get("video_id") or _video_id_from_url(row["youtube_url"])
        if dry_run:
            print(f"would post phase {row['phase']} for {row['source_id']} -> {video_id}")
            continue
        response = _youtube_insert_comment(video_id=video_id, text=row["comment_draft"], access_token=access_token)
        comment_id = response.get("id") or response.get("snippet", {}).get("topLevelComment", {}).get("id")
        if not comment_id:
            raise SystemExit(f"YouTube API response missing comment id for {row['source_id']} phase {row['phase']}")
        row["posted_comment_id"] = str(comment_id)
        row["posted_comment_url"] = _comment_url(video_id, comment_id)
        row["posted_at_utc"] = datetime.now(timezone.utc).isoformat()
        row["post_receipt"] = response
        row["status"] = "posted"
        changed = True
    if changed and not dry_run:
        save_queue(rows, queue_path)
    return rows


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--queue", type=Path, default=QUEUE_PATH, help="Queue state file")
    p.add_argument("--source-index", type=Path, default=SOURCE_INDEX_PATH, help="Public source video index")
    sub = p.add_subparsers(dest="command", required=True)

    build = sub.add_parser("build", help="Rebuild the queue from public source data.")
    build.add_argument("--write", action="store_true", help="Write the queue file after rebuilding.")
    build.set_defaults(func=_cmd_build)

    report = sub.add_parser("report", help="Render a markdown and Telegram-ready status summary.")
    report.set_defaults(func=_cmd_report)

    draft = sub.add_parser("draft", help="Render one phase comment draft for a source id.")
    draft.add_argument("source_id")
    draft.add_argument("phase", type=int, choices=[1])
    draft.set_defaults(func=_cmd_draft)

    state = sub.add_parser("set-state", help="Mark a queue row as approved, rejected, or needs_review.")
    state.add_argument("source_id")
    state.add_argument("phase", type=int, choices=[1])
    state.add_argument("--state", choices=["approved", "rejected", "needs_review"], required=True)
    state.set_defaults(func=_cmd_set_state)

    post = sub.add_parser("post", help="Post approved rows to YouTube.")
    post.add_argument("--phase", type=int, choices=[1], default=None)
    post.add_argument("--source-id", default=None)
    post.add_argument("--access-token", default=os.environ.get("YOUTUBE_ACCESS_TOKEN", ""))
    post.add_argument("--dry-run", action="store_true")
    post.set_defaults(func=_cmd_post)
    return p


def _cmd_build(args: argparse.Namespace) -> int:
    rows = build_queue_rows(queue_path=args.queue, source_index_path=args.source_index)
    if args.write:
        save_queue(rows, args.queue)
        draft_paths = render_phase1_drafts(rows)
        print(f"wrote: {args.queue}")
        print(f"wrote phase 1 drafts: {len(draft_paths)} -> {DRAFTS_DIR}")
    else:
        print(render_markdown_summary(rows))
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    rows = load_queue(args.queue)
    if not rows:
        rows = build_queue_rows(queue_path=args.queue, source_index_path=args.source_index)
    print(render_markdown_summary(rows))
    print("")
    print(render_telegram_summary(rows))
    return 0


def _cmd_draft(args: argparse.Namespace) -> int:
    rows = build_queue_rows(queue_path=args.queue, source_index_path=args.source_index)
    matches = [row for row in rows if row["source_id"] == args.source_id and int(row["phase"]) == args.phase]
    if not matches:
        raise SystemExit(f"No row found for {args.source_id} phase {args.phase}")
    row = matches[0]
    if row.get("status") != "ready":
        print(f"status: {row.get('status')}")
        print(f"park_reason: {row.get('park_reason')}")
        return 0
    print(row["comment_draft"])
    return 0


def _cmd_set_state(args: argparse.Namespace) -> int:
    set_entry_state(queue_path=args.queue, source_id=args.source_id, phase=args.phase, approval_state=args.state)
    print(f"updated: {args.source_id} phase {args.phase} -> {args.state}")
    return 0


def _cmd_post(args: argparse.Namespace) -> int:
    if not args.access_token and not args.dry_run:
        raise SystemExit("Missing access token. Set YOUTUBE_ACCESS_TOKEN or pass --access-token.")
    rows = post_approved_rows(
        queue_path=args.queue,
        phase=args.phase,
        access_token=args.access_token,
        dry_run=args.dry_run,
        source_id=args.source_id,
    )
    if not args.dry_run:
        print(f"updated queue: {args.queue}")
    else:
        print(render_telegram_summary(rows))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
