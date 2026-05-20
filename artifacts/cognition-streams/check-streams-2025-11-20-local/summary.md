# Check Streams - 2025-11-20

Target day: `2025-11-20`
Run date: `2026-05-20`
Mode: local index + existing raw-input inspection, with live audit attempted.

## Discovery Status

- Local cached indexes found one clean date-tied Mercouris upload for `2025-11-20`; it was captured from the operator-pasted transcript on `2026-05-20`.
- Existing raw-input contains one Glenn Diesen / Chas Freeman file with a date-tied local cache hit; it was refreshed from the operator-pasted transcript on `2026-05-20`.
- Existing raw-input also contains one Dialogue Works / Andrei Martyanov file listed in local inventories for `2025-11-20`, but the transcript body opens with `Thursday, December 11th, 2025`; treat this as raw present but date/content-audit needed.
- Live audit command timed out after YouTube bot-check errors and stale/live-event interference; use the local trusted set below rather than the incomplete live-audit output.

## Aired / Trusted Set

| Channel | Status | Title | URL | Evidence |
|---|---|---|---|---|
| Alexander Mercouris | captured, operator-paste | Kiev Defeats Force US U Turn Accept Istanbul Plus; Kellogg Quits; Kiev/EU Stunned Say NO; War Crisis | https://www.youtube.com/watch?v=c8ldFIMPrx4 | `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md` has `2025-11-20`, duration `4724`; raw-input captured from operator paste |
| Glenn Diesen | captured, operator-paste | Chas Freeman: Fake Peace, Political Collapse & Major Wars | https://www.youtube.com/watch?v=rEeZPr0p6lI | raw-input refreshed from operator paste; `.codex-tmp/freeman-2025-helix-search/diesen.json` has `upload_date: 2025-11-20` |

## Raw-Input Already Present

| Channel | File | Quality |
|---|---|---|
| Alexander Mercouris | `codex/years/2026/raw-input/2025-11-20/youtube-alex-mercouris-kiev-defeats-force-us-u-turn-accept-istanbul-plus-kellogg-quits-kiev-eu-stunned-say-no-war-crisis-2025-11-20.md` | `transcript-bearing`; `8074` words; routeable no; unresolved speaker yes; residual noise none; exact operator-paste match before normalized repairs |
| Glenn Diesen | `codex/years/2026/raw-input/2025-11-20/youtube-glenn-diesen-chas-freeman-fake-peace-political-collapse-and-major-wars-2025-11-20.md` | `transcript-bearing`; `7054` words; routeable yes; unresolved speaker no; residual noise none; exact operator-paste match before normalized repairs |
| Dialogue Works | `codex/years/2026/raw-input/2025-11-20/transcript-dialogue-works-andrei-martyanov-it-s-all-over-iran-russia-and-china-move-in-together-2025-11-20.md` | `legacy-appearance-only`; transcript body present; `7246` words; routeable yes; unresolved speaker no; residual noise none; body-date mismatch needs audit |

## Date-Ambiguous / Unresolved

- Daniel Davis: live audit found no dated items for the window.
- Dialogue Works: live audit found no dated items; local inventory points to `rCalPQD48bc`, but existing body text conflicts with the `2025-11-20` date.
- Judging Freedom: live audit produced uploads-playlist items but dates were blank due YouTube bot-check failures; no item is trusted for `2025-11-20` from this run.
- Glenn Diesen: live audit found no dated items, but local cached speaker-search data verifies `rEeZPr0p6lI`.

## Manual-Fetch Queue

Highest-confidence direct YouTube watch URLs still needing cleanup/audit:

1. https://www.youtube.com/watch?v=rCalPQD48bc - Dialogue Works / Andrei Martyanov, raw-present but needs date/content audit before treating as clean.

## Live Audit Failure Note

Command attempted:

```powershell
py scripts/cognition_streams_audit.py --start 2025-11-20 --end 2025-11-20 --recent-start 2025-11-20
```

Result: timed out after `120s`. Output showed repeated YouTube `Sign in to confirm you're not a bot` failures and one live-event timing error. Partial discovery files were written under `.codex-tmp/cognition-streams/2025-11-20_to_2025-11-20/`.
