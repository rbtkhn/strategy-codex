# check-streams 2025-01-20 local receipt

Run date: 2026-05-20

## Status

Live `cognition_streams_audit.py` discovery for 2025-01-20 timed out against YouTube anti-bot / upcoming-live responses. The date-tied trusted set below comes from local cached channel indexes plus existing canonical raw-input paths.

The live audit wrote partial discovery receipts for Daniel Davis, Glenn Diesen, and Dialogue Works under `.codex-tmp/cognition-streams/2025-01-20_to_2025-01-20/`. Daniel Davis and Glenn Diesen returned empty uploads-playlist result sets; the Daniel Davis empty result conflicts with date-tied local channel-index hits, so the cached local index is treated as the trusted source for that lane. Dialogue Works returned one unresolved scheduled/live item without a trusted date.

The Daniel Davis `-M4iMZGaMH4` item and the Alex Mercouris `FerlWCEP3AM` item have been repaired from operator paste in the local Codex session log and now classify as `transcript-bearing`, `full-operator-paste`; both remain non-routeable because the speaker is unresolved. The Daniel Davis `cPwcothN9tI` item remains `legacy-appearance-only`, not transcript-bearing.

## Sources Checked

- `.codex-tmp/davis-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/diesen*` / `.codex-tmp/youtube-glenn-diesen*` local index folders
- `.codex-tmp/*dialogue*` local index folders
- `.codex-tmp/*judg*` / `.codex-tmp/*napolitano*` local index folders
- `.codex-tmp/cognition-streams/2025-01-20_to_2025-01-20/*.discovery.json`
- `codex/years/2026/raw-input/2025-01-20/*.md`

## Trusted January 20 Items

| channel | youtube_id | class | duration | status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `-M4iMZGaMH4` | main | 2233 | captured / transcript-bearing / full-operator-paste | UKRAINE Eastern Front in Danger of Collapse as Trump Takes Reigns |
| daniel-davis-deep-dive | `cPwcothN9tI` | main | 2027 | captured / legacy-appearance-only | Trump 2.0 Launches a Blizzard of ExecOrders |
| alex-mercouris | `FerlWCEP3AM` | main | 4395 | captured / transcript-bearing / full-operator-paste | Trump President, Biden Blinken Exit; Russia China Summits; Zelensky Fumes, Starmer Out |

## Operator-Paste Repair

`-M4iMZGaMH4` and `FerlWCEP3AM` were mechanically extracted from the local Codex session log after the operator pasted each transcript. The raw-input body after `## Transcript` exactly matches the pasted session text after `Transcripts:`.

### `-M4iMZGaMH4`

- receipt: `runtime/artifacts/cognition-streams/check-streams-2025-01-20-local/operator-paste-receipt--M4iMZGaMH4.md`
- raw input: `codex/years/2026/raw-input/2025-01-20/youtube-daniel-davis-deep-dive-ukraine-eastern-front-in-danger-of-collapse-as-trump-takes-reigns-2025-01-20.md`
- sourceChars: 38113
- bodyChars: 38113
- exactMatch: `true`
- bodyWordCount: 7224
- quality report: `transcript-bearing`; routeable: no; unresolved speaker: yes; residual noise: none

### `FerlWCEP3AM`

- receipt: `runtime/artifacts/cognition-streams/check-streams-2025-01-20-local/operator-paste-receipt-FerlWCEP3AM.md`
- raw input: `codex/years/2026/raw-input/2025-01-20/youtube-alex-mercouris-trump-president-biden-blinken-exit-russia-china-summits-zelensky-fumes-s-2025-01-20.md`
- sourceChars: 46902
- bodyChars: 46902
- exactMatch: `true`
- bodyWordCount: 8228
- quality report: `transcript-bearing`; routeable: no; unresolved speaker: yes; residual noise: none

## Hidden / Low Priority

No same-day clip/highlight candidate was trusted from local indexes in this pass.

## Unresolved

- Glenn Diesen: live audit returned an empty partial discovery receipt; no trusted January 20 local index hit was found.
- Dialogue Works: live audit returned one unresolved scheduled/live item, `FeTkzRHdYBQ` / `Matthew Hoh: The Pentagon's Biggest Lie About Iran`, with no trusted publication date in the receipt.
- Judging Freedom / Judge Napolitano: unresolved in live audit; no trusted January 20 local index hit was found.

## Manual-Fetch Queue

- `-M4iMZGaMH4` - https://www.youtube.com/watch?v=-M4iMZGaMH4 (captured from operator paste; no manual fetch needed unless independent subtitle verification is required)
- `cPwcothN9tI` - https://www.youtube.com/watch?v=cPwcothN9tI
- `FerlWCEP3AM` - https://www.youtube.com/watch?v=FerlWCEP3AM (captured from operator paste; no manual fetch needed unless independent subtitle verification is required)
- unresolved date: `FeTkzRHdYBQ` - https://www.youtube.com/watch?v=FeTkzRHdYBQ
