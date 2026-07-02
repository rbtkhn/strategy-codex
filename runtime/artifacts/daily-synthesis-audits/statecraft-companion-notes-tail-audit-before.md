# Daily Synthesis Tail-Label Audit (Before)

- family: legacy `## Statecraft Notes` tail heading on migrated daily synthesis files
- contract: `scripts/validate_statecraft_daily_synthesis.py` expects optional tail `Companion Notes -> Archival Note`
- root: `statecraft/daily`
- migrated daily files with wrong tail label: `19`
- validator errors naming `Statecraft Notes`: `15` (June 04/06/07/08 hidden until section-order tranche opens)

## Files In Family

| File | Validator tail error visible |
| --- | --- |
| `2026-03-16.md` | yes (also quote-anchor) |
| `2026-03-19.md` | yes |
| `2026-03-23.md` | yes (also quote-anchor) |
| `2026-03-27.md` | yes (also quote-anchor) |
| `2026-03-31.md` | yes (also quote-anchor) |
| `2026-04-08.md` | yes |
| `2026-04-12.md` | yes |
| `2026-04-17.md` | yes (also quote-anchor) |
| `2026-04-20.md` | yes (also quote-anchor) |
| `2026-04-22.md` | yes (also quote-anchor) |
| `2026-04-30.md` | yes (also quote-anchor) |
| `2026-05-29.md` | yes (`Statecraft Notes -> Archival Note`) |
| `2026-05-30.md` | yes |
| `2026-05-31.md` | yes |
| `2026-06-01.md` | yes (also quote-anchor) |
| `2026-06-04.md` | deferred (section-order mismatch blocks tail check) |
| `2026-06-06.md` | deferred |
| `2026-06-07.md` | deferred |
| `2026-06-08.md` | deferred |

## Repair Scope (This Tranche)

One bounded mechanical fix only:

```text
## Statecraft Notes  ->  ## Companion Notes
```

Do not widen into quote-anchor repair, five-volume reorder, or monthly retrofit in the same pass.

## Opening Justification

The archive-index wedge (2026-06-08) restored navigation truth; this family restores **daily synthesis contract truth** on the optional tail label without pretending to close the full validator backlog.
