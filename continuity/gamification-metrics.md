# strategy-codex â€” seam / â€œgamificationâ€ trial (WORK only)
<!-- word_count: 199 -->

**Purpose:** Optional **observability** for weave quality and verify-first discipline â€” **not** a leaderboard. If a metric becomes the target, it stops measuring seam health (Goodhart risk). Prefer **falsifiable watches** in [`forecast-watch-log.md`](forecast-watch-log.md) over raw counts.

## Fields (legacy on-disk index file â€” v4+)

| Field | Meaning |
|--------|---------|
| **`weave_count`** | Optional manual tally of **outgoing** cross-link targets, or copy from `python3 scripts/knot_seam_metrics.py` (`out_links` column). |
| **`seam_integrity`** | Optional subjective **0â€“1** self-grade: did registers, scope, and falsifiers stay honest on this page? **Not** comparable across topics. |
| **`qoi_check`**, **`kac_check`** | Optional booleans mirroring the **strategy-page** templateâ€™s **Quality of information** and **Key assumptions** checklists. |

All keys are **optional**; existing rows validate without them.

## Scripts

- **`python3 scripts/validate_knot_index.py`** â€” schema gate for the legacy on-disk index (filename unchanged on disk).
- **`python3 scripts/knot_seam_metrics.py`** â€” read-only table: computed outgoing cross-links vs optional `weave_count`. **`--strict-drift`** exits non-zero when YAML `weave_count` disagrees with computed counts (used in CI).

## When **not** to use

- Do **not** optimize **volume** of weaves or **maximize** `weave_count` as a goal.
- Do **not** treat `seam_integrity` as proof of correctness â€” it is a **reflection** hook only.
