#!/usr/bin/env python3
"""Orchestrate post-land scaffold + ASR/proper-noun cleanup for statecraft captures.

WORK only; not Record. SSOT for operator ``source-clean`` skill.

Pipeline (in order):
  1. Caption wrapper + family scaffold (post_land_statecraft_family)
  2. ph-civ series tier (asr_light_clean)
  3. Common entity pass (fix_statecraft_common_asr_entities)
  4. Thread / channel tiers (source_clean_tiers)
  5. Frontmatter provenance patch
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
_WJ = _SCRIPTS / "work_jiang"
for p in (_WJ, _SCRIPTS):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from asr_light_clean import detect_series, normalize_transcript_text  # noqa: E402
from fix_statecraft_common_asr_entities import apply_replacements as apply_entity_re  # noqa: E402
from normalize_statecraft_source_asr import (  # noqa: E402
    FM_RE,
    split_transcript,
    patch_frontmatter,
)
from post_land_statecraft_family import apply_statecraft_capture_scaffold  # noqa: E402
from source_clean_tiers import (  # noqa: E402
    apply_tier_pairs,
    collect_tier_pairs,
    parse_frontmatter,
    resolve_tier_keys,
)
from statecraft_day_archive import DEFAULT_ROOT  # noqa: E402


def _has_source_clean_provenance(fm_block: str) -> bool:
    """True when capture already received a source-clean provenance patch."""
    return "source-clean pass" in fm_block or "AI-assisted source-clean" in fm_block


def _landed_files_for_day(day: str) -> list[Path]:
    day_dir = DEFAULT_ROOT / day
    if not day_dir.is_dir():
        raise FileNotFoundError(f"day folder not found: {day_dir}")
    files = sorted(p for p in day_dir.glob("source-*.md") if p.is_file())
    if not files:
        raise FileNotFoundError(f"no source-*.md under {day_dir}")
    return files


def clean_capture(
    path: Path,
    *,
    write: bool = False,
    scaffold: bool = True,
    series: str | None = "auto",
    dry_run: bool = False,
) -> int:
    path = path.resolve()
    if not path.is_file():
        print(f"Not a file: {path}", file=sys.stderr)
        return 1

    if scaffold:
        apply_statecraft_capture_scaffold(path, dry_run=dry_run or not write)

    raw = path.read_text(encoding="utf-8")
    head, body = split_transcript(raw)
    if body is None:
        print(f"{path}: no transcript heading found", file=sys.stderr)
        return 1

    meta = parse_frontmatter(raw)
    tier_pairs = collect_tier_pairs(meta)
    tier_key_preview = resolve_tier_keys(meta)

    series_resolved = detect_series(path) if series == "auto" else series
    new_body, series_n = normalize_transcript_text(body, series=series_resolved)
    new_body, entity_counts = apply_entity_re(new_body)
    entity_n = sum(entity_counts.values())
    new_body, tier_n, tier_detail = apply_tier_pairs(new_body, tier_pairs)

    total_n = series_n + entity_n + tier_n
    body_changed = new_body != body

    prior_editorial = None
    fm_match = FM_RE.match(raw)
    already_clean = bool(fm_match and _has_source_clean_provenance(fm_match.group(0)))
    if fm_match:
        for line in fm_match.group(0).splitlines():
            if line.startswith("editorial_note:"):
                raw_val = line.split(":", 1)[-1].strip().strip('"')
                prior_editorial = raw_val
                break

    needs_first_provenance = total_n > 0 and not already_clean
    should_patch_fm = (
        write
        and fm_match is not None
        and (body_changed or needs_first_provenance)
    )
    effective_n = total_n if body_changed else (total_n if needs_first_provenance else 0)
    if should_patch_fm:
        keys_label = ", ".join(tier_key_preview[:4]) or "none"
        detail = f"scaffold + ph-civ series + entity + thread tiers ({keys_label})"
        new_fm = patch_frontmatter(
            fm_match.group(0).rstrip("\n"),
            sub_count=effective_n if effective_n else total_n,
            prior_editorial=prior_editorial,
            pass_name="source-clean",
            pass_detail=detail,
            pass_note_prefix="source-clean pass",
        ) + "\n"
        head = new_fm + head[len(fm_match.group(0)) :]

    new_text = head + (new_body if body_changed else body)

    idempotent = already_clean and not body_changed and not needs_first_provenance
    print(
        f"{path}: source-clean total={effective_n} "
        f"(series={series_n}, entity={entity_n}, thread={tier_n}, series_key={series_resolved!r}); "
        f"matched={total_n}; body_changed={body_changed}; idempotent={idempotent}; "
        f"scaffold={scaffold}; write={write and not dry_run and (body_changed or should_patch_fm)}"
    )
    if tier_detail:
        print(f"  thread_hits={tier_detail}")

    if write and not dry_run and (body_changed or should_patch_fm):
        path.write_text(new_text, encoding="utf-8", newline="\n")
    elif dry_run and (body_changed or should_patch_fm):
        print(f"  dry-run: would write {path.name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--path", type=Path, help="One statecraft source-*.md capture")
    group.add_argument("--day", help="Clean all source-*.md for YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="Report only; no writes")
    parser.add_argument("--no-scaffold", action="store_true", help="Skip caption/family scaffold pass")
    parser.add_argument(
        "--series",
        default="auto",
        help="ph-civ series tier (auto from filename, or none, founding-members, …)",
    )
    parser.add_argument("--with-index", action="store_true", help="Rebuild day-index after batch")
    args = parser.parse_args()

    paths = [args.path] if args.path else _landed_files_for_day(args.day)
    series = None if args.series == "none" else args.series
    write = not args.dry_run
    exit_code = 0
    for p in paths:
        rc = clean_capture(
            p,
            write=write,
            scaffold=not args.no_scaffold,
            series=series,
            dry_run=args.dry_run,
        )
        if rc:
            exit_code = rc

    if args.with_index and args.day and write:
        from build_statecraft_day_indices import main as build_main  # noqa: E402

        sys.argv = ["build_statecraft_day_indices.py", "--day", args.day]
        build_main()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
