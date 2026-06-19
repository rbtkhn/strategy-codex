# June Week Quote-Anchor Audit (Before)

WORK only; not Record.

- contract: explicit `Quote anchor:` lines with ≥12 quoted words
- window: `2026-06-03`, `2026-06-04`, `2026-06-06`, `2026-06-07`
- failing lines: `9`

## Failures

| File | Line | Defect |
| --- | ---: | --- |
| `2026-06-03.md` | 98 | 9 words |
| `2026-06-04.md` | 97 | 5 words |
| `2026-06-04.md` | 103 | missing quoted excerpt |
| `2026-06-06.md` | 118 | 5 words |
| `2026-06-06.md` | 122 | 9 words |
| `2026-06-06.md` | 124 | 6 words |
| `2026-06-06.md` | 126 | 8 words |
| `2026-06-07.md` | 122 | 10 words |
| `2026-06-07.md` | 124 | missing quoted excerpt |

## Repair Rule

Extend anchors from landed `source-archive/statecraft/2026-06-*` lines only — no new claims.
