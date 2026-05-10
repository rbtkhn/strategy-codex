"""Run full work-jiang rebuild: registry, renders, validators. Exit non-zero on first failure."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PYTHON = sys.executable

STEPS = [
    [PYTHON, "scripts/work_jiang/build_source_registry.py"],
    [PYTHON, "scripts/work_jiang/link_supporting_registries.py"],
    [PYTHON, "scripts/work_jiang/extract_concept_mentions.py"],
    [PYTHON, "scripts/work_jiang/render_concept_dictionary.py"],
    [PYTHON, "scripts/work_jiang/link_claims_to_thesis.py"],
    [PYTHON, "scripts/work_jiang/render_claims_overview.py"],
    [PYTHON, "scripts/work_jiang/render_book_architecture.py"],
    [PYTHON, "scripts/work_jiang/render_thesis_map.py"],
    [PYTHON, "scripts/work_jiang/render_chapter_queue.py"],
    [PYTHON, "scripts/work_jiang/build_all_evidence_packs.py"],
    [PYTHON, "scripts/work_jiang/render_status_dashboard.py"],
    [PYTHON, "scripts/work_jiang/extract_quote_candidates.py"],
    [PYTHON, "scripts/work_jiang/render_quote_bank.py"],
    [PYTHON, "scripts/work_jiang/link_quotes_to_chapters.py"],
    [PYTHON, "scripts/work_jiang/build_quote_index.py"],
    [PYTHON, "scripts/work_jiang/render_analysis_backlog.py"],
    [PYTHON, "scripts/work_jiang/render_counter_readings.py"],
    [PYTHON, "scripts/work_jiang/link_counter_readings.py"],
    [PYTHON, "scripts/work_jiang/render_intellectual_chronology.py"],
    [PYTHON, "scripts/work_jiang/validate_work_jiang.py", "--require-analysis-frontmatter"],
    [PYTHON, "scripts/work_jiang/validate_argument_layer.py"],
    [PYTHON, "scripts/work_jiang/validate_comparative_layer.py"],
    [PYTHON, "scripts/work_jiang/validate_patterns_registry.py"],
]


def main() -> int:
    for i, cmd in enumerate(STEPS):
        print(f"[{i + 1}/{len(STEPS)}] {' '.join(cmd)}", flush=True)
        r = subprocess.run(cmd, cwd=str(ROOT))
        if r.returncode != 0:
            print(f"FAILED: {' '.join(cmd)}", file=sys.stderr)
            return r.returncode
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
