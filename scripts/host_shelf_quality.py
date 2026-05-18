#!/usr/bin/env python3
"""Build WORK-layer host shelf quality summaries from raw-input files.

The summary is advisory and receipt-backed. It does not edit host shelves,
speaker objects, raw-input files, or Record surfaces.
"""

from __future__ import annotations

import argparse
import calendar
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_speaker_routing_queue as speaker_routing  # noqa: E402
from codex_paths import speakers_root, year_root  # noqa: E402


DEFAULT_OUT_ROOT = REPO_ROOT / "artifacts" / "host-shelf-quality"
DEFAULT_SPEAKERS_DIR = speakers_root()
GRADE_ORDER = [
    "transcript-grade",
    "cleaned-transcript",
    "transcript-bearing",
    "summary-grade",
    "legacy-appearance-only",
]
TRANSCRIPT_VALID_GRADES = {
    "transcript-grade",
    "cleaned-transcript",
    "transcript-bearing",
}
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WORD_RE = re.compile(r"\b[\w'-]+\b")
RESIDUAL_NOISE_TERMS = [
    "Barniel",
    "Bilkula",
    "Cining",
    "Cinping",
    "Hin Matal",
    "Jai Shanka",
    "Kaakalis",
    "Mandi",
    "Manny",
    "Naboo",
    "Rigul",
    "Sining",
    "TAD",
    "Tajjikistan",
    "Zalinski",
    "Zilinski",
    "chassis missiles",
    "helium sulfate",
    "non-coaching",
    "non-exchange",
    "sea of Azorov",
    "tourist missiles",
    "zero someum",
]


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _host_slug(value: str) -> str:
    return speaker_routing._canonical_host_slug(  # noqa: SLF001
        {"host": value, "show": value, "channel_slug": value, "thread": value}
    )


def _parse_month(year: int, raw_month: str) -> tuple[int, str]:
    text = str(raw_month).strip()
    if re.fullmatch(r"\d{4}-\d{2}", text):
        parsed_year, parsed_month = text.split("-", 1)
        if int(parsed_year) != year:
            raise ValueError(f"--year {year} does not match --month {text}")
        return int(parsed_month), text
    if re.fullmatch(r"\d{1,2}", text):
        month = int(text)
        return month, f"{year:04d}-{month:02d}"
    raise ValueError("--month must be MM or YYYY-MM")


def _month_bounds(year: int, month: int) -> tuple[date, date]:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, 1), date(year, month, last_day)


def _raw_date(path: Path, meta: dict[str, Any]) -> date | None:
    raw = str(meta.get("pub_date") or meta.get("ingest_date") or path.parent.name)
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def _body_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = FRONTMATTER_RE.match(text)
    if match:
        text = text[match.end() :]
    lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return "\n".join(lines)


def _word_count(path: Path) -> int:
    return len(WORD_RE.findall(_body_text(path)))


def _residual_noise_terms(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    found: list[str] = []
    for term in RESIDUAL_NOISE_TERMS:
        flags = 0 if any(ch.isupper() for ch in term) else re.IGNORECASE
        if re.search(rf"(?<!\w){re.escape(term)}(?!\w)", text, flags):
            found.append(term)
    return sorted(found, key=str.casefold)


def _quality_note(meta: dict[str, Any]) -> str:
    for key in ("quality_note", "normalization_note", "editorial_note", "source_note"):
        value = str(meta.get(key) or "").strip()
        if value:
            return value
    return ""


def _load_previous(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _delta(current: int | float, previous: int | float | None) -> int | float:
    if previous is None:
        return current
    return current - previous


def _signed(value: int | float, *, suffix: str = "") -> str:
    if isinstance(value, float):
        text = f"{value:+.1f}"
    else:
        text = f"{value:+d}"
    return f"{text}{suffix}"


def _run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def scoped_git_state(paths: list[Path]) -> dict[str, Any]:
    normalized: list[str] = []
    material_paths: list[Path] = []
    for path in paths:
        if not path:
            continue
        material_paths.append(path)
        rel = _rel(path)
        if rel not in normalized:
            normalized.append(rel)
    status_lines: list[str] = []
    status_ok = True
    if normalized:
        proc = _run_git(["status", "--porcelain", "--", *normalized])
        status_ok = proc.returncode == 0
        status_lines = [line for line in proc.stdout.splitlines() if line.strip()]
    upstream = _run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"])
    upstream_ref = upstream.stdout.strip() if upstream.returncode == 0 else ""
    ahead_count: int | None = None
    ahead_ok = True
    if upstream_ref:
        ahead = _run_git(["rev-list", "--count", f"{upstream_ref}..HEAD"])
        ahead_ok = ahead.returncode == 0 and ahead.stdout.strip().isdigit()
        if ahead_ok:
            ahead_count = int(ahead.stdout.strip())
    has_uncommitted = bool(status_lines)
    on_disk = all(path.exists() for path in material_paths)
    verified = bool(on_disk and status_ok and ahead_ok)
    committed = bool(verified and not has_uncommitted)
    pushed = bool(committed and upstream_ref and ahead_count == 0)
    return {
        "scoped_paths": normalized,
        "on_disk": on_disk,
        "verified": verified,
        "committed": committed,
        "pushed": pushed,
        "dirty_paths": status_lines,
        "dirty_path_count": len(status_lines),
        "upstream": upstream_ref,
        "ahead_count": ahead_count,
        "label": ("on-disk" if on_disk else "not-on-disk")
        + "/"
        + ("verified" if verified else "not-verified")
        + "/"
        + ("committed" if committed else "not-committed")
        + "/"
        + ("pushed" if pushed else "not-pushed"),
    }


def discover_raw_inputs(
    *,
    notebook_root: Path,
    year: int,
    month_label: str,
    raw_input_list: Path | None = None,
) -> list[Path]:
    if raw_input_list:
        candidates = speaker_routing.load_raw_input_list(raw_input_list)
    else:
        month = int(month_label.split("-", 1)[1])
        start, end = _month_bounds(year, month)
        candidates = speaker_routing._discover_raw_inputs(notebook_root / "raw-input", start, end)  # noqa: SLF001
    return speaker_routing.normalize_raw_input_paths(candidates)


def filter_host_month_paths(paths: list[Path], *, host: str, year: int, month_label: str) -> list[Path]:
    host_slug = _host_slug(host)
    out: list[Path] = []
    for path in paths:
        if not path.exists():
            continue
        meta = speaker_routing._read_frontmatter(path)  # noqa: SLF001
        current = _raw_date(path, meta)
        if not current or current.year != year or current.strftime("%Y-%m") != month_label:
            continue
        if speaker_routing._canonical_host_slug(meta) != host_slug:  # noqa: SLF001
            continue
        out.append(path)
    return out


def _naming_warnings(notebook_root: Path, host_slug: str) -> list[str]:
    host_dir = notebook_root / host_slug
    if not host_dir.exists():
        return []
    shelf_paths = sorted(host_dir.glob(f"{host_slug}-shelf-*.md"))
    book_paths = sorted(host_dir.glob(f"{host_slug}-book-*.md"))
    if not shelf_paths or not book_paths:
        return []
    books = ", ".join(_rel(path) for path in book_paths)
    return [
        f"{host_slug} has shelf-named files and book-named siblings; consider migrating these warnings-only paths: {books}"
    ]


def _closeout_line(summary: dict[str, Any]) -> str:
    deltas = summary["deltas"]
    return (
        f"Structure: {_signed(int(deltas['routeable_artifact_count']))} routeable | "
        f"Purity: {_signed(int(deltas['transcript_valid_count']))} transcript-valid / "
        f"{summary['transcript_valid_percent']:.1f}% "
        f"({_signed(float(deltas['transcript_valid_percent_points']), suffix='pp')}) | "
        f"Unresolved: {summary['unresolved_speaker_count']} | "
        f"Git: {summary['git_state']['label']}"
    )


def build_quality_summary(
    *,
    host: str,
    year: int,
    month_label: str,
    raw_paths: list[Path],
    notebook_root: Path,
    speakers_dir: Path,
    previous: dict[str, Any] | None = None,
    output_paths: list[Path] | None = None,
    input_scope: str = "provided-paths",
) -> dict[str, Any]:
    host_slug = _host_slug(host)
    raw_paths = filter_host_month_paths(raw_paths, host=host_slug, year=year, month_label=month_label)
    inventory = speaker_routing._discover_inventory(speakers_dir, notebook_root)  # noqa: SLF001
    routeable_rows = speaker_routing.build_rows(raw_paths, inventory, notebook_root)
    unresolved_rows = speaker_routing.build_unresolved_rows(raw_paths, inventory)
    routeable_paths = {row["raw_input_path"] for row in routeable_rows}
    unresolved_paths = {row["raw_input_path"] for row in unresolved_rows}

    counts = {grade: 0 for grade in GRADE_ORDER}
    total_words = 0
    artifacts: list[dict[str, Any]] = []
    for path in raw_paths:
        meta = speaker_routing._read_frontmatter(path)  # noqa: SLF001
        grade = speaker_routing.classify_evidence_grade(meta)
        if grade not in counts:
            grade = "legacy-appearance-only"
        counts[grade] += 1
        words = _word_count(path)
        total_words += words
        rel = _rel(path)
        residual_terms = _residual_noise_terms(path)
        artifacts.append(
            {
                "raw_input_path": rel,
                "pub_date": str(meta.get("pub_date") or meta.get("ingest_date") or path.parent.name),
                "title": str(meta.get("title") or path.stem),
                "evidence_grade": grade,
                "normalization_state": str(meta.get("normalization_state") or "").strip(),
                "quality_note": _quality_note(meta),
                "residual_noise_terms": residual_terms,
                "residual_noise": bool(residual_terms),
                "word_count": words,
                "routeable": rel in routeable_paths,
                "unresolved": rel in unresolved_paths,
            }
        )

    transcript_valid_count = sum(counts[grade] for grade in TRANSCRIPT_VALID_GRADES)
    total_artifact_count = len(raw_paths)
    transcript_valid_percent = (
        round((transcript_valid_count / total_artifact_count) * 100, 1) if total_artifact_count else 0.0
    )
    previous_counts = previous.get("counts", {}) if previous else {}
    previous_percent = previous.get("transcript_valid_percent") if previous else None
    deltas = {
        "routeable_artifact_count": int(
            _delta(len(routeable_rows), previous.get("routeable_artifact_count") if previous else None)
        ),
        "total_word_mass": int(_delta(total_words, previous.get("total_word_mass") if previous else None)),
        "transcript_valid_count": int(
            _delta(transcript_valid_count, previous.get("transcript_valid_count") if previous else None)
        ),
        "transcript_valid_percent_points": round(
            float(_delta(transcript_valid_percent, previous_percent if isinstance(previous_percent, (int, float)) else None)),
            1,
        ),
        "counts": {
            grade: int(_delta(counts[grade], previous_counts.get(grade) if isinstance(previous_counts, dict) else None))
            for grade in GRADE_ORDER
        },
    }
    summary: dict[str, Any] = {
        "schema_version": 1,
        "work_layer": True,
        "generated_date": date.today().isoformat(),
        "host": host_slug,
        "year": year,
        "month": month_label,
        "input_scope": input_scope,
        "raw_input_count": total_artifact_count,
        "routeable_artifact_count": len(routeable_rows),
        "total_word_mass": total_words,
        "counts": counts,
        "transcript-grade": counts["transcript-grade"],
        "cleaned-transcript": counts["cleaned-transcript"],
        "transcript-bearing": counts["transcript-bearing"],
        "summary-grade": counts["summary-grade"],
        "legacy-only": counts["legacy-appearance-only"],
        "legacy-appearance-only": counts["legacy-appearance-only"],
        "transcript_valid_count": transcript_valid_count,
        "transcript_valid_percent": transcript_valid_percent,
        "residual_noise_artifact_count": sum(1 for artifact in artifacts if artifact["residual_noise"]),
        "unresolved_speaker_count": len(unresolved_rows),
        "unresolved_speakers": unresolved_rows,
        "artifacts": artifacts,
        "deltas": deltas,
        "warnings": _naming_warnings(notebook_root, host_slug),
        "git_state": scoped_git_state(raw_paths + (output_paths or [])),
    }
    summary["closeout_line"] = _closeout_line(summary)
    return summary


def render_markdown(summary: dict[str, Any]) -> str:
    counts = summary["counts"]
    deltas = summary["deltas"]
    lines = [
        "# Host shelf quality summary",
        "",
        "WORK only; not Record.",
        "",
        f"- host: `{summary['host']}`",
        f"- month: `{summary['month']}`",
        f"- input scope: `{summary.get('input_scope', 'provided-paths')}`",
        f"- routeable artifact count: `{summary['routeable_artifact_count']}` ({_signed(int(deltas['routeable_artifact_count']))})",
        f"- total word mass: `{summary['total_word_mass']}` ({_signed(int(deltas['total_word_mass']))})",
        f"- transcript-valid percent: `{summary['transcript_valid_percent']:.1f}%` ({_signed(float(deltas['transcript_valid_percent_points']), suffix='pp')})",
        f"- residual-noise artifacts: `{summary.get('residual_noise_artifact_count', 0)}`",
        f"- unresolved speaker count: `{summary['unresolved_speaker_count']}`",
        f"- git: `{summary['git_state']['label']}`",
        f"- closeout: {summary['closeout_line']}",
        "",
        "## Grade Counts",
        "",
    ]
    for grade in GRADE_ORDER:
        lines.append(f"- `{grade}`: `{counts[grade]}` ({_signed(int(deltas['counts'][grade]))})")
    if summary["warnings"]:
        lines.extend(["", "## Warnings", ""])
        for warning in summary["warnings"]:
            lines.append(f"- {warning}")
    if summary["unresolved_speakers"]:
        lines.extend(["", "## Unresolved Speakers", ""])
        for row in summary["unresolved_speakers"]:
            lines.append(f"- `{row['pub_date']}` {row['title']} - `{row['raw_input_path']}`")
    noisy_artifacts = [artifact for artifact in summary["artifacts"] if artifact.get("residual_noise_terms")]
    if noisy_artifacts:
        lines.extend(["", "## Residual Noise", ""])
        for artifact in noisy_artifacts:
            terms = ", ".join(f"`{term}`" for term in artifact["residual_noise_terms"])
            lines.append(f"- `{artifact['pub_date']}` {terms} - `{artifact['raw_input_path']}`")
    lines.extend(["", "## Raw Inputs", ""])
    for artifact in summary["artifacts"]:
        flags = []
        if artifact["routeable"]:
            flags.append("routeable")
        if artifact["unresolved"]:
            flags.append("unresolved")
        flag_text = ", ".join(flags) if flags else "not-routeable"
        lines.append(
            f"- `{artifact['pub_date']}` `{artifact['evidence_grade']}` `{artifact['word_count']}` words "
            f"({flag_text}) - `{artifact['raw_input_path']}`"
        )
        if artifact.get("normalization_state") or artifact.get("quality_note"):
            note_bits = []
            if artifact.get("normalization_state"):
                note_bits.append(f"normalization `{artifact['normalization_state']}`")
            if artifact.get("quality_note"):
                note_bits.append(f"note: {artifact['quality_note']}")
            lines.append(f"  - {'; '.join(note_bits)}")
    return "\n".join(lines).rstrip() + "\n"


def write_quality_summary(
    *,
    host: str,
    year: int,
    month_label: str,
    raw_paths: list[Path],
    notebook_root: Path,
    speakers_dir: Path,
    output_root: Path = DEFAULT_OUT_ROOT,
    input_scope: str = "provided-paths",
) -> dict[str, Any]:
    host_slug = _host_slug(host)
    output_dir = output_root / str(year) / host_slug / month_label
    json_path = output_dir / "quality-summary.json"
    md_path = output_dir / "quality-summary.md"
    previous = _load_previous(json_path)
    summary = build_quality_summary(
        host=host_slug,
        year=year,
        month_label=month_label,
        raw_paths=raw_paths,
        notebook_root=notebook_root,
        speakers_dir=speakers_dir,
        previous=previous,
        output_paths=[json_path, md_path],
        input_scope=input_scope,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    summary["git_state"] = scoped_git_state(
        filter_host_month_paths(raw_paths, host=host_slug, year=year, month_label=month_label) + [json_path, md_path]
    )
    summary["closeout_line"] = _closeout_line(summary)
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(summary), encoding="utf-8")
    summary["json_path"] = str(json_path)
    summary["markdown_path"] = str(md_path)
    return summary


def write_quality_reports_for_paths(
    raw_paths: list[Path],
    *,
    notebook_root: Path,
    speakers_dir: Path = DEFAULT_SPEAKERS_DIR,
    output_root: Path = DEFAULT_OUT_ROOT,
    expand_to_month: bool = False,
) -> list[dict[str, Any]]:
    normalized = speaker_routing.normalize_raw_input_paths(raw_paths)
    grouped: dict[tuple[str, int, str], list[Path]] = {}
    for path in normalized:
        if not path.exists():
            continue
        meta = speaker_routing._read_frontmatter(path)  # noqa: SLF001
        host_slug = speaker_routing._canonical_host_slug(meta)  # noqa: SLF001
        current = _raw_date(path, meta)
        if not host_slug or not current:
            continue
        key = (host_slug, current.year, current.strftime("%Y-%m"))
        grouped.setdefault(key, []).append(path)
    summaries: list[dict[str, Any]] = []
    for (host_slug, year, month_label), paths in sorted(grouped.items()):
        report_paths = (
            discover_raw_inputs(notebook_root=notebook_root, year=year, month_label=month_label)
            if expand_to_month
            else paths
        )
        summaries.append(
            write_quality_summary(
                host=host_slug,
                year=year,
                month_label=month_label,
                raw_paths=report_paths,
                notebook_root=notebook_root,
                speakers_dir=speakers_dir,
                output_root=output_root,
                input_scope="full-host-month" if expand_to_month else "provided-paths",
            )
        )
    return summaries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--month", required=True, help="MM or YYYY-MM")
    parser.add_argument("--raw-input-list", type=Path, default=None)
    parser.add_argument("--notebook-root", type=Path, default=None)
    parser.add_argument("--speakers-dir", type=Path, default=DEFAULT_SPEAKERS_DIR)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUT_ROOT)
    parser.add_argument("--apply", action="store_true", help="Write quality-summary.json and .md.")
    parser.add_argument("--no-apply", action="store_false", dest="apply", help="Print only.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    month, month_label = _parse_month(args.year, args.month)
    notebook_root = args.notebook_root or year_root(args.year)
    speakers_dir = args.speakers_dir.resolve()
    raw_paths = discover_raw_inputs(
        notebook_root=notebook_root,
        year=args.year,
        month_label=month_label,
        raw_input_list=args.raw_input_list,
    )
    input_scope = "provided-paths" if args.raw_input_list else "full-host-month"
    if args.apply:
        summary = write_quality_summary(
            host=args.host,
            year=args.year,
            month_label=month_label,
            raw_paths=raw_paths,
            notebook_root=notebook_root,
            speakers_dir=speakers_dir,
            output_root=args.output_root,
            input_scope=input_scope,
        )
    else:
        host_slug = _host_slug(args.host)
        previous_path = args.output_root / str(args.year) / host_slug / month_label / "quality-summary.json"
        summary = build_quality_summary(
            host=args.host,
            year=args.year,
            month_label=f"{args.year:04d}-{month:02d}",
            raw_paths=raw_paths,
            notebook_root=notebook_root,
            speakers_dir=speakers_dir,
            previous=_load_previous(previous_path),
            input_scope=input_scope,
        )
    print(json.dumps(summary, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
