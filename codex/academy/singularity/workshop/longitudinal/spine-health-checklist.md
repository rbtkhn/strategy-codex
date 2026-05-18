# Spine Health Checklist

WORK only; not Record.

Use this checklist when maintaining the Innermost Loop longitudinal spine or any similar deterministic review surface.

## Quick Checks

- Coverage still matches the raw-capture span.
- Date ordering is monotonic and no entry was dropped.
- Gaps are real gaps, not missing output from a broken rebuild.
- Review load is visible, not silently flattened.
- Bridge notes are isolated from generated chronology.
- External links point to source-bound workshop sheets, not to raw chat claims.
- The JSON spine and markdown spine agree on counts, dates, and source paths.

## Stress Checks

- A single item should not absorb too many fronts without review.
- Weak matches should stay marked as review items.
- High-frequency terms should not dominate interpretation without a second-pass check.
- The spine should still be legible when a new bridge note is added.
- A future maintainer should be able to rebuild the spine from the raw captures and know what changed.

## Maintenance Rule

If a rebuild changes coverage, review totals, or front density in a surprising way, stop and inspect the matching rules before treating the new spine as clean.

## Use

- Pair this with [The Innermost Loop longitudinal spine](innermost-loop.md).
- Pair this with [The Innermost Loop signals JSON](innermost-loop-signals.json).
- Use it before or after adding a new bridge note such as the Karpathy watchlist.
