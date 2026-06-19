# check-streams 2025-04-20 local receipt

Run date: 2026-05-20

## Status

Live `cognition_streams_audit.py` discovery for 2025-04-20 timed out after repeated YouTube bot-check responses. The audit wrote only a partial Daniel Davis discovery receipt under `.codex-tmp/cognition-streams/2025-04-20_to_2025-04-20/`, and that live receipt returned no items despite a date-tied local channel-index hit.

The trusted set below comes from local cached channel indexes. Glenn Diesen's same-day Michael Hudson item was also corroborated by secondary web/podcast listings, but the direct YouTube watch URL remains the preferred source for any later transcript capture.

One canonical raw-input file now exists under `codex/years/2026/raw-input/2025-04-20/`: `0LN-Y-kEgmY`, captured from operator-pasted transcript text.

## Sources Checked

- `.codex-tmp/cognition-streams/2025-04-20_to_2025-04-20/*.discovery.json`
- `.codex-tmp/davis-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/diesen-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/dialogue-works-full-latest/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/dialogue-works-latest20/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/check-streams-2025-03-08/freedom-flat/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/check-streams-2025-05-09/freedom-flat/CHANNEL-VIDEO-INDEX.md`
- web search for date/title corroboration
- `codex/years/2026/raw-input/2025-04-20/*.md`

## Aired / Trusted Set

| channel | youtube_id | class | duration | local status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `oXJesOnsPBE` | main / short standalone | 815 | not captured | Col Doug Macgregor: UKRAINE is Trump's War NOW |
| glenn-diesen | `0LN-Y-kEgmY` | main | 1915 | captured / transcript-bearing / full-operator-paste | Michael Hudson: The Industrial Capitalism of China and Russia versus US Neoliberalism |

## Suspected Clips / Highlights

No same-day clip/highlight candidate was trusted from local indexes in this pass.

## Date-Ambiguous / Unresolved

- Alexander Mercouris: local index has 2025-04-19 (`7gJDQfyIqdk`) and 2025-04-21 (`74TIFQg2e_w`) uploads bracketing the requested date, but no 2025-04-20 upload.
- Dialogue Works: no trusted same-day YouTube watch URL recovered from the available local indexes or web search.
- Judge Napolitano / Judging Freedom: no trusted same-day YouTube watch URL recovered from the available local indexes or web search.

## Operator-Paste Repair

- `0LN-Y-kEgmY` - raw input: `codex/years/2026/raw-input/2025-04-20/youtube-glenn-diesen-michael-hudson-the-industrial-capitalism-of-china-and-russia-versus-us-neoliberalism-2025-04-20.md`; receipt: `runtime/artifacts/cognition-streams/check-streams-2025-04-20-local/operator-paste-receipt-0LN-Y-kEgmY.md`
  - sourceChars/bodyChars: `24216` / `24216`
  - exactMatch: `true` against the local Codex session operator paste
  - bodyWordCount: `4434`
  - normalization: none required
  - quality: `transcript-bearing`; routeable: `yes`; unresolved speaker: `no`; residual noise: `none`

## Manual-Fetch Queue

Highest-confidence direct YouTube URLs tied to 2025-04-20:

- `oXJesOnsPBE` - https://www.youtube.com/watch?v=oXJesOnsPBE - Col Doug Macgregor: UKRAINE is Trump's War NOW
- `0LN-Y-kEgmY` - https://www.youtube.com/watch?v=0LN-Y-kEgmY - captured from operator paste; see Operator-Paste Repair above

Do not materialize as April 20 without fresh date evidence:

- Dialogue Works April 20 candidate: unresolved locally
- Judge Napolitano / Judging Freedom April 20 candidate: unresolved locally
- Alexander Mercouris April 20 candidate: no local same-day upload found
