# check-streams 2025-02-20 local receipt

Run date: 2026-05-20

## Status

Live `cognition_streams_audit.py` discovery for 2025-02-20 timed out after repeated YouTube bot-check and upcoming-live responses. The date-tied trusted set below comes from local cached channel indexes plus the partial discovery receipts written by the live audit.

The live audit wrote partial discovery receipts for Daniel Davis, Glenn Diesen, Dialogue Works, and Judge Napolitano / Judging Freedom under `.codex-tmp/cognition-streams/2025-02-20_to_2025-02-20/`. Daniel Davis and Glenn Diesen returned empty uploads-playlist result sets. Dialogue Works returned one unresolved scheduled/live item without a trusted date. Napolitano returned many no-date items and bot-check errors; because the item cluster is not safely date-tied to 2025-02-20, it is excluded from the trusted set.

The Daniel Davis item `UnsiLktwK38` and the Alex Mercouris item `LFiaRW9d4uQ` have been repaired from operator paste in the local Codex session log and now classify as `transcript-bearing`, `full-operator-paste`; both remain non-routeable because the speaker is unresolved. The Daniel Davis items `o__mf5V-CwU` and `1oLsjGVIv7Y` remain uncaptured.

## Sources Checked

- `.codex-tmp/cognition-streams/2025-02-20_to_2025-02-20/*.discovery.json`
- `.codex-tmp/davis-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/**/CHANNEL-VIDEO-INDEX.md` local index scan for `2025-02-20`
- `codex/years/2026/raw-input/2025-02-20/*.md`

## Aired / Trusted Set

| channel | youtube_id | class | duration | local status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `UnsiLktwK38` | main | 2685 | captured / transcript-bearing / full-operator-paste | Trump FORCES Ukraine Strategy The World Rejects it |
| daniel-davis-deep-dive | `o__mf5V-CwU` | main | 4409 | not captured | Urgency of Peace Negotiations to End the Ukraine War Webinar |
| daniel-davis-deep-dive | `1oLsjGVIv7Y` | main / short standalone | 642 | not captured | Trump Zelensky War of Words |
| alex-mercouris | `LFiaRW9d4uQ` | main | 5564 | captured / transcript-bearing / full-operator-paste | Disastrous Zelensky Presser Angers Trump: Zelensky Dictator, US Aid Gravy Train, Hints Disengagement |

## Operator-Paste Repair

`UnsiLktwK38` and `LFiaRW9d4uQ` were mechanically extracted from the local Codex session log after the operator pasted each transcript. The raw-input body after `## Transcript` exactly matches the pasted session text after `Transcripts:`.

### `UnsiLktwK38`

- receipt: `runtime/artifacts/cognition-streams/check-streams-2025-02-20-local/operator-paste-receipt-UnsiLktwK38.md`
- raw input: `codex/years/2026/raw-input/2025-02-20/youtube-daniel-davis-deep-dive-trump-forces-ukraine-strategy-the-world-rejects-it-2025-02-20.md`
- sourceChars: 43198
- bodyChars: 43198
- exactMatch: `true`
- bodyWordCount: 8146
- quality report: `transcript-bearing`; routeable: no; unresolved speaker: yes; residual noise: none

### `LFiaRW9d4uQ`

- receipt: `runtime/artifacts/cognition-streams/check-streams-2025-02-20-local/operator-paste-receipt-LFiaRW9d4uQ.md`
- raw input: `codex/years/2026/raw-input/2025-02-20/youtube-alex-mercouris-disastrous-zelensky-presser-angers-trump-zelensky-dictator-us-aid-gravy-train-hints-disengagement-2025-02-20.md`
- sourceChars: 59609
- bodyChars: 59609
- exactMatch: `true`
- bodyWordCount: 10647
- quality report: `transcript-bearing`; routeable: no; unresolved speaker: yes; residual noise: none

## Suspected Clips / Highlights

| channel | youtube_id | reason | duration | title |
|---|---:|---|---:|---|
| daniel-davis-deep-dive | `-qBwADyWbfc` | 5:58 guest-fragment title; likely companion clip despite no explicit clip marker | 358 | Zelensky Should Beware/Trump's Global View Taking Shape: Larry Johnson |

## Date-Ambiguous / Unresolved

- Dialogue Works: live audit returned `FeTkzRHdYBQ` / `Matthew Hoh: The Pentagon's Biggest Lie About Iran`, but with no trusted publication date and an upcoming-live extractor error. It is not treated as a 2025-02-20 aired upload.
- Glenn Diesen: live audit returned an empty partial discovery receipt; no trusted 2025-02-20 local index hit was found.
- Judge Napolitano / Judging Freedom: live audit returned many bot-check/no-date items plus one upcoming-live item; no item is trusted for 2025-02-20 in this pass.

## Manual-Fetch Queue

Highest-confidence direct YouTube URLs tied to 2025-02-20:

- `UnsiLktwK38` - https://www.youtube.com/watch?v=UnsiLktwK38 - Trump FORCES Ukraine Strategy The World Rejects it (captured from operator paste; no manual fetch needed unless independent subtitle verification is required)
- `o__mf5V-CwU` - https://www.youtube.com/watch?v=o__mf5V-CwU - Urgency of Peace Negotiations to End the Ukraine War Webinar
- `1oLsjGVIv7Y` - https://www.youtube.com/watch?v=1oLsjGVIv7Y - Trump Zelensky War of Words
- `LFiaRW9d4uQ` - https://www.youtube.com/watch?v=LFiaRW9d4uQ - Disastrous Zelensky Presser Angers Trump: Zelensky Dictator, US Aid Gravy Train, Hints Disengagement (captured from operator paste; no manual fetch needed unless independent subtitle verification is required)

Clip / optional:

- `-qBwADyWbfc` - https://www.youtube.com/watch?v=-qBwADyWbfc - Zelensky Should Beware/Trump's Global View Taking Shape: Larry Johnson

Date-ambiguous / do not materialize as Feb 20 without fresh date evidence:

- `FeTkzRHdYBQ` - https://www.youtube.com/watch?v=FeTkzRHdYBQ - Matthew Hoh: The Pentagon's Biggest Lie About Iran
