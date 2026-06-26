#!/usr/bin/env python3
"""Emit a SID Situation Brief delta block from day-over-day fork grade changes.

Reads wire-verify matrices and optional 72h watch-run executive tables under
``statecraft/notes/wire/`` and ``statecraft/notes/watch/``, diffs named fork grades vs a prior day, and prints a
paste-ready markdown section:

  ## Situation Brief — changes since YYYY-MM-DD

WORK only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WIRE_DIR = REPO_ROOT / "statecraft" / "notes" / "wire"
DEFAULT_WATCH_DIR = REPO_ROOT / "statecraft" / "notes" / "watch"
DEFAULT_DAILY_DIR = DEFAULT_WIRE_DIR  # legacy alias

FORK_ID_RE = re.compile(
    r"\*\*(J\d+(?:-[A-Za-z0-9]+)?)\*\*"
    r"|\*\*(Lebanon ops|UAE tranche|Mutual MOU text|§224[^|*]+|A['\u2019] south-tier)\*\*",
    re.IGNORECASE,
)
J_ID_LOOSE_RE = re.compile(r"\b(J\d+(?:-[A-Za-z0-9]+)?)\b")
GRADE_RE = re.compile(
    r"\*\*(Supported|Contested|Partial|Contradicted|Unclear|Open|Stressed|Fail|Settled|Developing)"
    r"(?:\s*/\s*(?:Partial|Contested|absent|[A-Za-z ]+))?\*\*",
    re.IGNORECASE,
)
DAY_FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")

METHOD_LINE = (
    "*Governed brief with source receipts and explicit falsifiers — not a wire summary.*"
)
DISCLAIMER_LINE = (
    "*Situation Brief (SID Brief) — judgment support for qualified professionals; "
    "not legal or investment advice.*"
)


@dataclass(frozen=True)
class ForkGrade:
    fork_id: str
    grade: str
    source: str


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value.strip())


def table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        if re.match(r"^\|\s*[-:| ]+\|", stripped):
            continue
        cells = [cell.strip() for cell in stripped.split("|")[1:-1]]
        if cells:
            rows.append(cells)
    return rows


def extract_fork_id(cell: str) -> str | None:
    match = FORK_ID_RE.search(cell)
    if match:
        for group in match.groups():
            if group:
                return group.strip()
    loose = J_ID_LOOSE_RE.search(cell)
    if loose:
        return loose.group(1)
    return None


def grade_from_row(cells: list[str]
) -> str | None:
    grades: list[str] = []
    for cell in cells:
        for match in GRADE_RE.finditer(cell):
            primary = match.group(1).title()
            grades.append(primary)
    if not grades:
        return None
    priority = {
        "Contradicted": 0,
        "Fail": 1,
        "Stressed": 2,
        "Contested": 3,
        "Partial": 4,
        "Partial/Contested": 4,
        "Supported/Partial": 5,
        "Supported": 6,
        "Unclear": 7,
        "Open": 8,
        "Settled": 9,
        "Developing": 10,
    }
    grades.sort(key=lambda g: priority.get(g.split("/")[0], 50))
    return grades[0]


def parse_fork_grades(text: str, source: str) -> dict[str, ForkGrade]:
    found: dict[str, ForkGrade] = {}
    for row in table_rows(text):
        if not row:
            continue
        fork_id = extract_fork_id(row[0])
        if fork_id is None:
            joined = " ".join(row)
            if not J_ID_LOOSE_RE.search(joined):
                continue
            fork_id = extract_fork_id(joined)
        if fork_id is None:
            continue
        grade = grade_from_row(row)
        if grade is None:
            continue
        found[fork_id] = ForkGrade(fork_id=fork_id, grade=grade, source=source)
    return found


def wire_matrix_for_day(wire_dir: Path, day: date) -> Path | None:
    day_str = day.isoformat()
    exact = wire_dir / f"{day_str}-news-verify-matrix.md"
    if exact.is_file():
        return exact
    candidates = sorted(
        p
        for p in wire_dir.glob(f"{day_str}*-news-verify-matrix.md")
        if p.is_file()
    )
    return candidates[-1] if candidates else None


def watch_run_for_day(watch_dir: Path, day: date) -> Path | None:
    day_str = day.isoformat()
    exact = watch_dir / f"{day_str}-72h-watch-run.md"
    if exact.is_file():
        return exact
    candidates = sorted(
        p for p in watch_dir.glob(f"{day_str}*-72h-watch-run.md") if p.is_file()
    )
    return candidates[-1] if candidates else None


def prior_day_with_matrix(
    wire_dir: Path, day: date, max_lookback: int = 14
) -> tuple[date, Path] | None:
    cursor = day - timedelta(days=1)
    for _ in range(max_lookback):
        path = wire_matrix_for_day(wire_dir, cursor)
        if path is not None:
            return cursor, path
        cursor -= timedelta(days=1)
    return None


def load_grades(path: Path, *, watch_dir: Path = DEFAULT_WATCH_DIR) -> dict[str, ForkGrade]:
    text = path.read_text(encoding="utf-8")
    grades = parse_fork_grades(text, source=path.name)
    day_match = DAY_FILE_RE.search(path.name)
    if day_match:
        day = parse_iso_date(day_match.group(1))
        watch = watch_run_for_day(watch_dir, day)
        if watch is not None and watch != path:
            watch_grades = parse_fork_grades(
                watch.read_text(encoding="utf-8"), source=watch.name
            )
            for fork_id, entry in watch_grades.items():
                grades.setdefault(fork_id, entry)
    return grades


def delta_implication(prior: str | None, current: str, changed: bool) -> str:
    if prior is None:
        return "New fork tracked today."
    if not changed:
        return "No grade movement."
    pairs = (prior.lower(), current.lower())
    if "fail" in pairs[1] and "fail" not in pairs[0]:
        return "Fork failed — escalation or pseudo-gate pressure."
    if "stressed" in pairs[1]:
        return "Fork stressed — enactment or review horizon tightening."
    if "contested" in pairs[1] and "supported" in pairs[0]:
        return "Fork downgraded — treat prior read as stale."
    if "supported" in pairs[1] and pairs[0] in {
        "contested",
        "partial",
        "unclear",
        "open",
    }:
        return "Fork upgraded — confirm before client-facing use."
    if "open" in pairs[1]:
        return "Still open — falsifier window active."
    return "Grade moved — reopen prior memo language."


def build_delta_block(
    *,
    prior_day: date,
    current_day: date,
    prior_grades: dict[str, ForkGrade],
    current_grades: dict[str, ForkGrade],
    prior_source: str,
    current_source: str,
) -> str:
    all_forks = sorted(set(prior_grades) | set(current_grades))
    lines: list[str] = [
        f"## Situation Brief — changes since {prior_day.isoformat()}",
        "",
        f"**SID Brief delta** · current day `{current_day.isoformat()}` · "
        f"prior `{prior_source}` -> current `{current_source}`",
        "",
        METHOD_LINE,
        "",
        "| Fork | Prior | Current | Delta | Implication |",
        "|------|-------|---------|-------|-------------|",
    ]

    movement_count = 0
    for fork_id in all_forks:
        prior = prior_grades.get(fork_id)
        current = current_grades.get(fork_id)
        prior_grade = prior.grade if prior else "—"
        current_grade = current.grade if current else "—"
        if prior is None:
            delta = "new"
            movement_count += 1
        elif current is None:
            delta = "dropped"
            movement_count += 1
        elif prior.grade != current.grade:
            delta = "changed"
            movement_count += 1
        else:
            delta = "unchanged"
        implication = delta_implication(
            prior.grade if prior else None,
            current_grade,
            delta != "unchanged",
        )
        lines.append(
            f"| **{fork_id}** | {prior_grade} | {current_grade} | {delta} | {implication} |"
        )

    lines.extend(["", "### Executive read", ""])
    if movement_count == 0:
        lines.append(
            f"No fork grade movement between {prior_day.isoformat()} and "
            f"{current_day.isoformat()}; carry forward prior Situation Brief with date stamp."
        )
    else:
        movers = [
            fork_id
            for fork_id in all_forks
            if (
                fork_id not in prior_grades
                or fork_id not in current_grades
                or prior_grades[fork_id].grade != current_grades[fork_id].grade
            )
        ]
        suffix = "; …" if len(movers) > 6 else ""
        lines.append(
            f"**{movement_count}** fork(s) moved ({', '.join(movers[:6])}{suffix}). "
            "Paste into daily synthesis or watch run; add pin-cites before external send."
        )

    lines.extend(["", DISCLAIMER_LINE, ""])
    return "\n".join(lines)


def resolve_inputs(
    *,
    wire_dir: Path,
    day: date | None,
    today_path: Path | None,
    prior_path: Path | None,
    prior_day: date | None,
) -> tuple[date, Path, date, Path]:
    if today_path is not None:
        today_file = today_path.resolve()
        if not today_file.is_file():
            raise FileNotFoundError(f"today file not found: {today_file}")
        day_match = DAY_FILE_RE.search(today_file.name)
        current_day = (
            parse_iso_date(day_match.group(1)) if day_match else day or date.today()
        )
    else:
        if day is None:
            raise ValueError("specify --day YYYY-MM-DD or --today-path")
        current_day = day
        today_file = wire_matrix_for_day(wire_dir, current_day)
        if today_file is None:
            raise FileNotFoundError(
                f"no news-verify matrix for {current_day.isoformat()} under {wire_dir}"
            )

    if prior_path is not None:
        prior_file = prior_path.resolve()
        if not prior_file.is_file():
            raise FileNotFoundError(f"prior file not found: {prior_file}")
        day_match = DAY_FILE_RE.search(prior_file.name)
        if day_match:
            resolved_prior_day = parse_iso_date(day_match.group(1))
        elif prior_day is not None:
            resolved_prior_day = prior_day
        else:
            resolved_prior_day = current_day - timedelta(days=1)
    elif prior_day is not None:
        resolved_prior_day = prior_day
        prior_file = wire_matrix_for_day(wire_dir, resolved_prior_day)
        if prior_file is None:
            raise FileNotFoundError(
                f"no news-verify matrix for prior day {resolved_prior_day.isoformat()}"
            )
    else:
        found = prior_day_with_matrix(wire_dir, current_day)
        if found is None:
            raise FileNotFoundError(
                f"no prior news-verify matrix within lookback before {current_day.isoformat()}"
            )
        resolved_prior_day, prior_file = found

    return current_day, today_file, resolved_prior_day, prior_file


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day", help="Current day YYYY-MM-DD (wire matrix lookup)")
    parser.add_argument("--prior-day", help="Prior day YYYY-MM-DD (default: auto lookback)")
    parser.add_argument(
        "--wire-dir",
        type=Path,
        default=DEFAULT_WIRE_DIR,
        help=f"news-verify matrix directory (default: {DEFAULT_WIRE_DIR})",
    )
    parser.add_argument(
        "--daily-dir",
        type=Path,
        default=None,
        help="Legacy alias for --wire-dir",
    )
    parser.add_argument("--today-path", type=Path, help="Explicit today wire matrix or watch file")
    parser.add_argument("--prior-path", type=Path, help="Explicit prior wire matrix or watch file")
    parser.add_argument("-o", "--output", type=Path, help="Write markdown to file instead of stdout")
    return parser.parse_args(argv)


def _ensure_utf8_stdout() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except (AttributeError, ValueError, OSError):
        pass


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    wire_dir = (args.daily_dir or args.wire_dir).resolve()
    watch_dir = DEFAULT_WATCH_DIR
    day = parse_iso_date(args.day) if args.day else None
    prior_day = parse_iso_date(args.prior_day) if args.prior_day else None

    try:
        current_day, today_file, resolved_prior_day, prior_file = resolve_inputs(
            wire_dir=wire_dir,
            day=day,
            today_path=args.today_path,
            prior_path=args.prior_path,
            prior_day=prior_day,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    prior_grades = load_grades(prior_file, watch_dir=watch_dir)
    current_grades = load_grades(today_file, watch_dir=watch_dir)
    if not prior_grades:
        print(f"warning: no fork rows parsed from {prior_file.name}", file=sys.stderr)
    if not current_grades:
        print(f"warning: no fork rows parsed from {today_file.name}", file=sys.stderr)
    if not prior_grades and not current_grades:
        print("error: no fork grades parsed from either file", file=sys.stderr)
        return 1

    block = build_delta_block(
        prior_day=resolved_prior_day,
        current_day=current_day,
        prior_grades=prior_grades,
        current_grades=current_grades,
        prior_source=prior_file.name,
        current_source=today_file.name,
    )

    if args.output:
        args.output.write_text(block, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        _ensure_utf8_stdout()
        print(block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
