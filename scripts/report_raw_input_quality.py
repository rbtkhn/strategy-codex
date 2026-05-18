#!/usr/bin/env python3
"""Report item-level raw-input quality with host-month purity context.

WORK-layer helper only. It reads raw-input and derived inventory surfaces; it
does not edit raw-input, host shelves, speaker objects, or Record surfaces.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_speaker_routing_queue as speaker_routing  # noqa: E402
import host_shelf_quality  # noqa: E402


def _rel(path: Path) -> str:
    return host_shelf_quality._rel(path)  # noqa: SLF001


def _default_notebook_root(path: Path, year: int) -> Path:
    parts = list(path.resolve().parts)
    for index, part in enumerate(parts[:-1]):
        if part == "codex" and index + 1 < len(parts) and parts[index + 1] == str(year):
            return Path(*parts[: index + 2])
    return REPO_ROOT / "codex" / str(year)


def _legacy_transcript_warning(artifact: dict[str, Any]) -> str:
    if artifact["evidence_grade"] != "legacy-appearance-only":
        return ""
    if int(artifact.get("body_word_count") or 0) < 50:
        return ""
    return (
        "Transcript body is present, but metadata classifies this as "
        "`legacy-appearance-only`; do not call it transcript-valid until "
        "source_type/transcript_type metadata is normalized."
    )


def _body_word_count(path: Path) -> int:
    text = path.read_text(encoding="utf-8-sig")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            text = parts[2]
    text = "\n".join(
        line
        for line in text.splitlines()
        if not line.lstrip().startswith("#") and not line.lstrip().startswith("**Watch:**")
    )
    return len(re.findall(r"\b[\w'-]+\b", text))


def build_report(
    raw_input_path: Path,
    *,
    notebook_root: Path | None = None,
    output_root: Path = host_shelf_quality.DEFAULT_OUT_ROOT,
) -> dict[str, Any]:
    path = raw_input_path.resolve()
    if not path.exists():
        raise FileNotFoundError(path)

    meta = speaker_routing._read_frontmatter(path)  # noqa: SLF001
    current = host_shelf_quality._raw_date(path, meta)  # noqa: SLF001
    if not current:
        raise ValueError(f"Could not determine raw-input date for {path}")

    host_slug = speaker_routing._canonical_host_slug(meta)  # noqa: SLF001
    if not host_slug:
        raise ValueError(f"Could not determine host slug for {path}")
    body_word_count = _body_word_count(path)

    month_label = current.strftime("%Y-%m")
    root = notebook_root or _default_notebook_root(path, current.year)
    previous_path = output_root / str(current.year) / host_slug / month_label / "quality-summary.json"
    raw_paths = host_shelf_quality.discover_raw_inputs(
        notebook_root=root,
        year=current.year,
        month_label=month_label,
    )
    summary = host_shelf_quality.build_quality_summary(
        host=host_slug,
        year=current.year,
        month_label=month_label,
        raw_paths=raw_paths,
        notebook_root=root,
        previous=host_shelf_quality._load_previous(previous_path),  # noqa: SLF001
        input_scope="full-host-month",
    )

    raw_rel = _rel(path)
    item = next(
        (artifact for artifact in summary["artifacts"] if artifact["raw_input_path"] == raw_rel),
        None,
    )
    if not item:
        item_summary = host_shelf_quality.build_quality_summary(
            host=host_slug,
            year=current.year,
            month_label=month_label,
            raw_paths=[path],
            notebook_root=root,
            input_scope="provided-paths",
        )
        if not item_summary["artifacts"]:
            raise ValueError(f"Could not build quality artifact for {path}")
        item = item_summary["artifacts"][0]

    return {
        "schema_version": 1,
        "work_layer": True,
        "raw_input_path": raw_rel,
        "source_url": str(meta.get("source_url") or "").strip(),
        "title": str(meta.get("title") or item.get("title") or path.stem),
        "host": host_slug,
        "year": current.year,
        "month": month_label,
        "evidence_grade": item["evidence_grade"],
        "word_count": item["word_count"],
        "body_word_count": body_word_count,
        "routeable": item["routeable"],
        "unresolved": item["unresolved"],
        "residual_noise_terms": item["residual_noise_terms"],
        "quality_note": item.get("quality_note") or "",
        "normalization_state": item.get("normalization_state") or "",
        "legacy_transcript_warning": _legacy_transcript_warning({**item, "body_word_count": body_word_count}),
        "host_month_closeout": summary["closeout_line"],
        "host_month_counts": summary["counts"],
        "host_month_transcript_valid_percent": summary["transcript_valid_percent"],
        "git_state": summary["git_state"],
    }


def render_markdown(report: dict[str, Any]) -> str:
    residual = report["residual_noise_terms"]
    residual_text = "none" if not residual else ", ".join(f"`{term}`" for term in residual)
    routeable = "yes" if report["routeable"] else "no"
    unresolved = "yes" if report["unresolved"] else "no"
    lines = [
        "## Transcript quality",
        f"- raw-input: `{report['raw_input_path']}`",
        f"- source: `{report['source_url']}`" if report["source_url"] else "- source: ``",
        f"- evidence grade: `{report['evidence_grade']}`",
        f"- word count: `{report['word_count']}`",
        f"- routeable: {routeable}; unresolved speaker: {unresolved}",
        f"- residual noise: {residual_text}",
        f"- quality note: {report['quality_note'] or '(none)'}",
        f"- host-month closeout: {report['host_month_closeout']}",
    ]
    if report["legacy_transcript_warning"]:
        lines.append(f"- warning: {report['legacy_transcript_warning']}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--path", required=True, type=Path, help="Raw-input Markdown file to report.")
    parser.add_argument("--notebook-root", type=Path, default=None)
    parser.add_argument("--output-root", type=Path, default=host_shelf_quality.DEFAULT_OUT_ROOT)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = build_report(
        args.path,
        notebook_root=args.notebook_root,
        output_root=args.output_root,
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=True))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
