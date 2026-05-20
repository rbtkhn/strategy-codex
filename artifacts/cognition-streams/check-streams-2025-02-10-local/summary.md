# check-streams 2025-02-10 local receipt

Run date: 2026-05-20

## Status

Live `cognition_streams_audit.py` discovery for 2025-02-10 timed out against YouTube anti-bot / upcoming-live responses. The date-tied trusted set below comes from local cached channel indexes. No canonical raw-input captures were found for the trusted February 10 IDs during this pass.

The live audit also wrote empty partial discovery receipts for Daniel Davis and Glenn Diesen from the uploads-playlist surface; the Daniel Davis empty result conflicts with a date-tied local channel index hit, so the cached local index is treated as the trusted source for that lane in this receipt.

## Sources Checked

- `.codex-tmp/davis-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/dialogue-works-full-latest/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/diesen*` / `.codex-tmp/youtube-glenn-diesen*` local index folders
- `.codex-tmp/*judg*` / `.codex-tmp/*napolitano*` local index folders
- `.codex-tmp/cognition-streams/2025-02-10_to_2025-02-10/*.discovery.json`

## Trusted February 10 Items

| channel | youtube_id | class | duration | status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `TBkvo7JDhWk` | main | 3047 | captured / transcript-bearing | What's Trump's Leverage Ending the Ukraine War? w/Col Jacques Baud |
| dialogue-works | `CgJyH1Mo1j4` | main | 1834 | needs-capture | Richard D. Wolff and Michael Hudson on the US Empire COLLAPSING - Europe Trapped, BRICS Emerging! |
| alex-mercouris | `mY3k77A4RKA` | main | 5268 | captured / transcript-bearing | Trump Confirms Putin Call; Putin Firm 4 Regions Russian: Ukraine Kursk Disaster; EU Gas Prices Surge |

## Hidden / Low Priority

No same-day clip/highlight candidate was trusted from local indexes in this pass.

## Unresolved

- Glenn Diesen: local Diesen indexes and the live partial discovery did not produce a trusted February 10 hit.
- Judging Freedom / Judge Napolitano: local Judging Freedom/Napolitano indexes did not produce a trusted February 10 hit; live audit timed out under anti-bot responses before producing a usable receipt.

## Manual-Fetch Queue

- `mY3k77A4RKA` - https://www.youtube.com/watch?v=mY3k77A4RKA
- `TBkvo7JDhWk` - https://www.youtube.com/watch?v=TBkvo7JDhWk
- `CgJyH1Mo1j4` - https://www.youtube.com/watch?v=CgJyH1Mo1j4
