# check-streams 2025-01-10 local receipt

Run date: 2026-05-20

## Status

Live `cognition_streams_audit.py` discovery for 2025-01-10 timed out against YouTube anti-bot responses and did not leave usable discovery receipts. The date-tied trusted set below comes from local cached channel indexes plus existing canonical raw-input paths.

Several January 10 raw-input files already exist, but item-level quality checks classify them as `legacy-appearance-only`, not transcript-bearing. They are listed as captured legacy stubs that still need transcript backfill.

## Sources Checked

- `.codex-tmp/davis-january/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/youtube-alex-mercouris-index/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/dialogue-works-full-latest/CHANNEL-VIDEO-INDEX.md`
- `.codex-tmp/diesen*` / `.codex-tmp/youtube-glenn-diesen*` local index folders
- `.codex-tmp/*judg*` / `.codex-tmp/*napolitano*` local index folders
- `codex/years/2026/raw-input/2025-01-10/*.md`

## Trusted January 10 Items

| channel | youtube_id | class | duration | status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `XrYqSMN6icw` | main | 3677 | captured / transcript-bearing | How Biden, NATO & the West DESTROYED UKRAINE |
| daniel-davis-deep-dive | `_AZiZJf5ZgQ` | main | 2737 | captured / transcript-bearing | How Will Trump End War in Ukraine w/Amb Chas Freeman |
| alex-mercouris | `W6ovr7VbO2k` | main | 5325 | captured / transcript-bearing | Putiin Trump Summit Coming; EU Frets Trump Will Cancel Sanctions; Zelensky Wants NATO Troops |

## Hidden / Low Priority

| channel | youtube_id | class | duration | status | title |
|---|---:|---|---:|---|---|
| daniel-davis-deep-dive | `K3dcHstbdrE` | short/update | 124 | legacy / low-priority | Drones UPDATE: Trump Promises Report in Days |

## Unresolved

- Glenn Diesen: local Diesen indexes did not produce a trusted January 10 hit; live audit timed out under anti-bot responses before producing a usable receipt.
- Dialogue Works: local Dialogue Works indexes did not produce a trusted January 10 hit; nearest local hits were January 11, not January 10.
- Judging Freedom / Judge Napolitano: local Judging Freedom/Napolitano indexes did not produce a trusted January 10 hit; live audit timed out under anti-bot responses before producing a usable receipt.

## Manual-Fetch Queue

- low-priority: `K3dcHstbdrE` - https://www.youtube.com/watch?v=K3dcHstbdrE
