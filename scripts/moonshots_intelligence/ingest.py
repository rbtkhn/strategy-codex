"""Read Moonshots archive captures — no transformation of verbatim body."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from prediction_lib import parse_frontmatter_dict

VERBATIM_HEADING = "## Verbatim Transcript"
REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class IngestResult:
    archive_path: Path
    meta: dict[str, Any]
    body: str


def ingest_archive(path: Path) -> IngestResult:
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = parse_frontmatter_dict(text, feature=str(path))
    body = extract_verbatim_body(text)
    return IngestResult(archive_path=path.resolve(), meta=meta, body=body)


def extract_verbatim_body(text: str) -> str:
    idx = text.find(VERBATIM_HEADING)
    if idx < 0:
        raise ValueError(f"missing {VERBATIM_HEADING!r} section")
    body = text[idx + len(VERBATIM_HEADING) :].lstrip("\r\n")
    return body.rstrip() + "\n"


def output_basename(meta: dict[str, Any]) -> str:
    episode_number = meta.get("episode_number")
    slug = str(meta.get("slug") or "unknown").strip()
    if episode_number is not None and str(episode_number).strip() != "":
        return f"moonshots-ep-{int(episode_number)}-intelligence"
    safe_slug = re.sub(r"[^a-z0-9-]+", "-", slug.lower()).strip("-") or "unknown"
    return f"moonshots-emerging-{safe_slug}-intelligence"


def default_out_dir() -> Path:
    return REPO_ROOT / "research" / "singularity-science" / "moonshots"
